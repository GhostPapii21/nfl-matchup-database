"""Receiver opportunity against top-5 and bottom-5 pass defenses, and what turns a 50-60 yard receiver into an 80-100 game.

Uses research/receiver_volatility_2026-11-14/rows.parquet (pre-game information only, 2022 to week 9 of 2026) plus final
scores and full-season defense numbers from pregame/.cache. Fits the equations on 2022-2024 and tests them on 2025-2026.
Writes results.json next to this file.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "pregame" / ".cache"
ROWS = ROOT / "research" / "receiver_volatility_2026-11-14" / "rows.parquet"
TRAIN = (2022, 2023, 2024)
TEST = (2025, 2026)
NORMAL = (45, 65)            # "normal 50-60 yard receiver": season average coming in


def r1(x, d=3):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), d)


def load():
    r = pd.read_parquet(ROWS)
    r = r[r.pos.isin(["WR", "TE"]) & (r.games_prior >= 3) & r.implied.notna() & (r.share > 0)].copy()
    g = pd.read_parquet(C / "games.parquet")
    g = g[g.game_type == "REG"][["game_id", "home_team", "away_team", "home_score", "away_score", "total_line"]]
    r = r.merge(g, on="game_id", how="left")
    home = r.team == r.home_team
    r["pts"] = np.where(home, r.home_score, r.away_score)
    r["opp_pts"] = np.where(home, r.away_score, r.home_score)
    r["margin"] = r.pts - r.opp_pts                     # final margin (in-game environment, not known pre-game)
    r["total_vs_line"] = (r.pts + r.opp_pts) - r.total_line
    r["team_tpg"] = r.tgt_pg / r.share                  # team targets per game coming in
    r["tgt_blend"] = 0.6 * r.tgt_pg + 0.4 * r.share_l3 * r.team_tpg
    r["dome"] = r.roof.isin(["dome", "closed"]).astype(int)
    r["windy"] = (r.wind.fillna(0) >= 15).astype(int)
    # receiver catch rate coming in is not in the table; aDOT stands in for it (short targets are caught more often)
    # pre-game defense tier by pass yards per attempt allowed (relative to league) ranked within each season-week
    d = r[["season", "week", "opp", "opp_ypa", "opp_ex_rate"]].drop_duplicates(["season", "week", "opp"])
    d["ypa_rank"] = d.groupby(["season", "week"]).opp_ypa.rank(ascending=True, method="first")   # 1 = stingiest
    d["n_def"] = d.groupby(["season", "week"]).opp.transform("size")
    r = r.merge(d[["season", "week", "opp", "ypa_rank", "n_def"]], on=["season", "week", "opp"], how="left")
    r["tier"] = np.select([r.ypa_rank <= 5, r.ypa_rank > r.n_def - 5], ["top5", "bottom5"], "middle")
    # position-specific tier: yards allowed per game to this position, ranked within season-week-position
    dp = r[["season", "week", "opp", "pos", "opp_pos_ypg"]].drop_duplicates(["season", "week", "opp", "pos"])
    dp["pos_rank"] = dp.groupby(["season", "week", "pos"]).opp_pos_ypg.rank(ascending=True, method="first")
    dp["n_dp"] = dp.groupby(["season", "week", "pos"]).opp.transform("size")
    r = r.merge(dp[["season", "week", "opp", "pos", "pos_rank", "n_dp"]], on=["season", "week", "opp", "pos"], how="left")
    r["pos_tier"] = np.select([r.pos_rank <= 5, r.pos_rank > r.n_dp - 5], ["top5", "bottom5"], "middle")
    # hindsight tier: the defense's full-season pass yards per attempt (what the defense really was)
    hs = []
    for y in sorted(r.season.unique()):
        p = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["season_type", "defteam", "pass_attempt", "sack", "passing_yards"])
        p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.sack != 1)]
        s = p.groupby("defteam").passing_yards.apply(lambda x: x.fillna(0).sum() / len(x)).rank(method="first")
        hs.append(pd.DataFrame({"season": y, "opp": s.index, "season_rank": s.values}))
    r = r.merge(pd.concat(hs), on=["season", "opp"], how="left")
    r["season_tier"] = np.select([r.season_rank <= 5, r.season_rank > 27], ["top5", "bottom5"], "middle")
    r["adot_type"] = pd.cut(r.adot, [-50, 8, 11.5, 100], labels=["short (aDOT<8)", "intermediate", "deep (aDOT 11.5+)"])
    return r


def tier_table(df, col):
    out = []
    for t in ("top5", "middle", "bottom5"):
        x = df[df[col] == t]
        if not len(x):
            continue
        out.append({"tier": t, "n": int(len(x)),
                    "targets_vs_avg": r1(x.y_tgt.mean() / x.tgt_pg.mean()),
                    "catches": r1(x.y_rec.mean(), 2), "targets": r1(x.y_tgt.mean(), 2),
                    "catch_rate": r1(x.y_rec.sum() / max(x.y_tgt.sum(), 1)),
                    "yards_per_target_vs_his": r1((x.y_yds.sum() / max(x.y_tgt.sum(), 1)) / (x.ypt * x.y_tgt).sum() * x.y_tgt.sum()),
                    "yards_vs_avg": r1(x.y_yds.mean() / x.yds_avg.mean()), "yards": r1(x.y_yds.mean(), 1),
                    "explosive_pg": r1(x.y_ex20.mean(), 2), "p80": r1((x.y_yds >= 80).mean()), "p100": r1((x.y_yds >= 100).mean()),
                    "team_targets": r1(x.y_team_tgts.mean(), 1)})
    return out


def glm(df_tr, df_te, y, X, family, offset=None, label=""):
    Xtr = sm.add_constant(df_tr[X].astype(float))
    Xte = sm.add_constant(df_te[X].astype(float), has_constant="add")
    m = sm.GLM(df_tr[y].astype(float), Xtr, family=family, offset=None if offset is None else df_tr[offset]).fit()
    pred = m.predict(Xte, offset=None if offset is None else df_te[offset])
    obs = df_te[y].astype(float)
    corr = float(np.corrcoef(pred, obs)[0, 1])
    mae = float(np.mean(np.abs(pred - obs)))
    return m, pred, {"label": label, "coef": {k: r1(v, 4) for k, v in m.params.items()},
                     "se": {k: r1(v, 4) for k, v in m.bse.items()}, "test_corr": r1(corr), "test_mae": r1(mae, 2), "n_train": int(len(df_tr)), "n_test": int(len(df_te))}


def calib(p, y, bins=10):
    q = pd.qcut(p, bins, labels=False, duplicates="drop")
    t = pd.DataFrame({"p": p, "y": y, "q": q}).groupby("q").agg(pred=("p", "mean"), hit=("y", "mean"), n=("y", "size"))
    return [{"pred": r1(a.pred), "hit": r1(a.hit), "n": int(a.n)} for a in t.itertuples()]


def auc(p, y):
    from sklearn.metrics import roc_auc_score
    return r1(roc_auc_score(y, p))


def main():
    r = load()
    res = {"n_rows": int(len(r)), "seasons": sorted(int(s) for s in r.season.unique())}
    normal = r[r.yds_avg.between(*NORMAL)]
    res["normal_def"] = f"WR/TE averaging {NORMAL[0]}-{NORMAL[1]} yards a game coming in (n={len(normal)})"

    # 1. tiers
    res["tiers_pregame_all"] = tier_table(r, "tier")
    res["tiers_pregame_normal"] = tier_table(normal, "tier")
    res["tiers_hindsight_normal"] = tier_table(normal, "season_tier")
    res["tiers_position_normal"] = tier_table(normal, "pos_tier")
    res["tier_agreement"] = {"pregame_bottom5_that_finished_bottom5": r1((r[r.tier == "bottom5"].season_tier == "bottom5").mean()),
                             "pregame_top5_that_finished_top5": r1((r[r.tier == "top5"].season_tier == "top5").mean())}
    by_type = []
    for ty, x in normal.groupby("adot_type", observed=True):
        for t in ("top5", "bottom5"):
            z = x[x.tier == t]
            mid = x[x.tier == "middle"]
            by_type.append({"type": str(ty), "tier": t, "n": int(len(z)), "yards": r1(z.y_yds.mean(), 1), "middle_yards": r1(mid.y_yds.mean(), 1),
                            "p80": r1((z.y_yds >= 80).mean()), "middle_p80": r1((mid.y_yds >= 80).mean()),
                            "catches": r1(z.y_rec.mean(), 2), "middle_catches": r1(mid.y_rec.mean(), 2)})
    res["tiers_by_receiver_type"] = by_type

    # 2. equations (fit 2022-24, test 2025-26)
    r["log_tgt"] = np.log(r.tgt_blend.clip(0.5))
    r["log_ypt"] = np.log(((r.ypt * r.tgt_pg * r.games_prior + 8.0 * 30) / (r.tgt_pg * r.games_prior + 30)).clip(2))   # ypt shrunk toward 8.0 with 30 targets
    r["log_def_ypa"] = np.log(r.opp_ypa.clip(0.6, 1.5))
    pos_avg = r.groupby(["season", "week", "pos"]).opp_pos_ypg.transform("mean")
    r["log_def_pos"] = np.log((r.opp_pos_ypg / pos_avg).clip(0.4, 2.5)).fillna(0)
    r["log_def_ex"] = np.log(r.opp_ex_rate.clip(0.4, 2.5))
    r["imp_c"] = r.implied - 22.0
    r["spread_c"] = r.spread          # positive = favored
    r["adot_c"] = r.adot - 9.0
    r["log_team_tpg"] = np.log(r.team_tpg)
    tr, te = r[r.season.isin(TRAIN)], r[r.season.isin(TEST)]
    eq = {}
    m_t, pt, eq["targets"] = glm(tr, te, "y_tgt", ["log_tgt", "imp_c", "spread_c", "log_def_ypa", "log_def_pos", "dome", "windy"],
                                 sm.families.Poisson(), label="Targets")
    m_c, pc, eq["catch_rate"] = glm(tr[tr.y_tgt > 0].assign(cr=lambda d: d.y_rec / d.y_tgt), te[te.y_tgt > 0].assign(cr=lambda d: d.y_rec / d.y_tgt),
                                    "cr", ["adot_c", "log_def_ypa", "log_def_pos", "imp_c", "spread_c", "windy"],
                                    sm.families.Binomial(), label="Catch rate (weighted by targets)")
    trp = tr[tr.y_tgt > 0].copy(); tep = te[te.y_tgt > 0].copy()
    trp["ypt_obs"] = trp.y_yds / trp.y_tgt; tep["ypt_obs"] = tep.y_yds / tep.y_tgt
    m_y, py, eq["yards_per_target"] = glm(trp, tep, "ypt_obs", ["log_ypt", "log_def_ypa", "log_def_pos", "log_def_ex", "imp_c", "adot_c", "dome", "windy"],
                                          sm.families.Gaussian(sm.families.links.Log()), label="Yards per target")
    m_yd, pyd, eq["yards"] = glm(tr, te, "y_yds", ["log_tgt", "log_ypt", "log_def_ypa", "log_def_pos", "log_def_ex", "imp_c", "spread_c", "dome", "windy"],
                                 sm.families.Poisson(), label="Receiving yards")
    m_r, pr, eq["receptions"] = glm(tr, te, "y_rec", ["log_tgt", "adot_c", "imp_c", "spread_c", "log_def_ypa", "log_def_pos", "windy"],
                                    sm.families.Poisson(), label="Receptions")
    base_corr = float(np.corrcoef(te.yds_avg, te.y_yds)[0, 1])
    eq["yards"]["baseline_season_avg_corr"] = r1(base_corr)
    eq["receptions"]["baseline_season_avg_corr"] = r1(float(np.corrcoef(te.tgt_pg * (te.y_rec.sum() / te.y_tgt.sum()), te.y_rec)[0, 1]))
    res["equations"] = eq

    # 3. P(80+) and P(100+) for normal receivers from the yards equation plus volatility
    r["pred_yds"] = m_yd.predict(sm.add_constant(r[["log_tgt", "log_ypt", "log_def_ypa", "log_def_pos", "log_def_ex", "imp_c", "spread_c", "dome", "windy"]].astype(float), has_constant="add"))
    r["log_pred"] = np.log(r.pred_yds)
    r["ex_rate_c"] = r.ex20_rate - 0.1
    feats = ["log_pred", "adot_c", "ex_rate_c"]
    out80 = {}
    for k in (80, 100):
        trn, tst = r[r.season.isin(TRAIN)], r[r.season.isin(TEST)]
        lm = sm.GLM((trn.y_yds >= k).astype(float), sm.add_constant(trn[feats]), family=sm.families.Binomial()).fit()
        p = lm.predict(sm.add_constant(tst[feats], has_constant="add"))
        tn = tst.y_yds.between(*NORMAL) | tst.yds_avg.between(*NORMAL)
        out80[str(k)] = {"coef": {a: r1(b, 4) for a, b in lm.params.items()}, "test_auc": auc(p, (tst.y_yds >= k)),
                         "test_calibration": calib(p.values, (tst.y_yds >= k).values),
                         "normal_test_auc": auc(p[tst.yds_avg.between(*NORMAL)], (tst[tst.yds_avg.between(*NORMAL)].y_yds >= k))}
        r[f"p{k}"] = lm.predict(sm.add_constant(r[feats], has_constant="add"))
    res["breakout_model"] = out80

    # 4. what the 80+ games of normal receivers looked like (in-game)
    normal = r[r.yds_avg.between(*NORMAL)].copy()
    normal["tgt_gain"] = normal.y_tgt - normal.tgt_pg
    normal["team_vol"] = normal.y_team_tgts / normal.team_tpg
    hi, lo = normal[normal.y_yds >= 80], normal[normal.y_yds < 80]
    res["breakout_anatomy"] = {
        "n_normal": int(len(normal)), "n_80": int(len(hi)), "rate_80": r1(len(hi) / len(normal)), "rate_100": r1((normal.y_yds >= 100).mean()),
        "targets": {"80_games": r1(hi.y_tgt.mean(), 2), "others": r1(lo.y_tgt.mean(), 2), "his_avg": r1(normal.tgt_pg.mean(), 2)},
        "targets_gain_3plus_share": r1((hi.tgt_gain >= 3).mean()), "others_targets_gain_3plus_share": r1((lo.tgt_gain >= 3).mean()),
        "catches": {"80_games": r1(hi.y_rec.mean(), 2), "others": r1(lo.y_rec.mean(), 2)},
        "yards_per_target": {"80_games": r1(hi.y_yds.sum() / hi.y_tgt.sum(), 2), "others": r1(lo.y_yds.sum() / lo.y_tgt.sum(), 2), "his_avg": r1(normal.ypt.mean(), 2)},
        "had_30plus_catch": r1((hi.y_ex30 > 0).mean()), "others_had_30plus_catch": r1((lo.y_ex30 > 0).mean()),
        "had_2plus_20yd": r1((hi.y_ex20 >= 2).mean()), "others_had_2plus_20yd": r1((lo.y_ex20 >= 2).mean()),
        "longest": {"80_games_median": r1(hi.y_long.median(), 0), "others_median": r1(lo.y_long.median(), 0)},
        "team_volume_vs_avg": {"80_games": r1(hi.team_vol.mean()), "others": r1(lo.team_vol.mean())},
        "trailing_share": {"80_games": r1((hi.margin < 0).mean()), "others": r1((lo.margin < 0).mean())},
        "shootout_share": {"80_games": r1((hi.total_vs_line >= 7).mean()), "others": r1((lo.total_vs_line >= 7).mean())},
    }
    # paths: volume only, big play only, both
    v = normal.tgt_gain >= 2; b = normal.y_ex30 > 0
    paths = []
    for lab, m in (("More targets (+2 or more) and a 30+ catch", v & b), ("More targets, no 30+ catch", v & ~b), ("Usual targets, a 30+ catch", ~v & b), ("Neither", ~v & ~b)):
        x = normal[m]
        paths.append({"path": lab, "share_of_games": r1(m.mean()), "p80": r1((x.y_yds >= 80).mean()), "share_of_80_games": r1((x.y_yds >= 80).sum() / max(len(hi), 1))})
    res["breakout_paths"] = paths

    # 5. in-game environment tables (for reasoning, not pre-game inputs)
    env = []
    for lab, m in (("Trailing by 8+ at the end", normal.margin <= -8), ("Within 7", normal.margin.abs() <= 7), ("Leading by 8+", normal.margin >= 8)):
        x = normal[m]
        env.append({"script": lab, "n": int(len(x)), "targets": r1(x.y_tgt.mean(), 2), "catches": r1(x.y_rec.mean(), 2), "yards": r1(x.y_yds.mean(), 1),
                    "p80": r1((x.y_yds >= 80).mean()), "team_targets": r1(x.y_team_tgts.mean(), 1)})
    res["script_in_game"] = env

    # 6. pre-game boosters for a normal receiver
    nb = normal.copy()
    nb["b_implied"] = nb.implied >= 24
    nb["b_def"] = nb.tier == "bottom5"
    nb["b_def10"] = nb.ypa_rank > nb.n_def - 10
    nb["b_role"] = (nb.share_l3 - nb.share) >= 0.03
    nb["b_volume"] = nb.tgt_blend >= 7.5
    nb["b_dog"] = nb.spread <= -3
    boost = []
    for lab, c in (("Team implied 24+", "b_implied"), ("Defense bottom 5 (pass yds/att)", "b_def"), ("Defense bottom 10", "b_def10"),
                   ("Target share up 3+ pts over last 3", "b_role"), ("7.5+ blended targets a game", "b_volume"), ("Underdog by 3+", "b_dog")):
        y, n_ = nb[nb[c]], nb[~nb[c]]
        boost.append({"factor": lab, "n_with": int(len(y)), "p80_with": r1((y.y_yds >= 80).mean()), "p80_without": r1((n_.y_yds >= 80).mean()),
                      "rec_with": r1(y.y_rec.mean(), 2), "rec_without": r1(n_.y_rec.mean(), 2), "tgt_with": r1(y.y_tgt.mean(), 2), "tgt_without": r1(n_.y_tgt.mean(), 2)})
    res["boosters"] = boost
    nb["n_boost"] = nb[["b_implied", "b_def10", "b_role", "b_volume"]].sum(axis=1)
    res["booster_stack"] = [{"boosters": int(k), "n": int(len(x)), "p80": r1((x.y_yds >= 80).mean()), "p100": r1((x.y_yds >= 100).mean()),
                             "catches": r1(x.y_rec.mean(), 2), "yards": r1(x.y_yds.mean(), 1)} for k, x in nb.groupby("n_boost")]
    # 7. receptions: what lifts catches
    rec = []
    for lab, m in (("Short aDOT (<8)", r.adot < 8), ("Intermediate", r.adot.between(8, 11.5)), ("Deep (11.5+)", r.adot > 11.5)):
        x = r[m]
        rec.append({"type": lab, "n": int(len(x)), "catch_rate": r1(x.y_rec.sum() / x.y_tgt.sum()), "catches_per_target_pg": r1(x.y_rec.mean() / x.tgt_pg.mean())})
    res["receptions_by_type"] = rec
    rs = []
    for lab, m in (("Big favorite (−7 or more)", r.spread >= 7), ("Favorite (−3 to −6.5)", r.spread.between(3, 6.9)), ("Close (within 2.5)", r.spread.abs() < 3),
                   ("Underdog (+3 to +6.5)", r.spread.between(-6.9, -3)), ("Big underdog (+7 or more)", r.spread <= -7)):
        x = r[m]
        rs.append({"spread": lab, "n": int(len(x)), "targets_vs_avg": r1(x.y_tgt.mean() / x.tgt_pg.mean()), "catches": r1(x.y_rec.mean(), 2),
                   "team_targets": r1(x.y_team_tgts.mean(), 1), "yards_vs_avg": r1(x.y_yds.mean() / x.yds_avg.mean())})
    res["receptions_by_spread"] = rs
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, indent=1, default=str)[:20000])


if __name__ == "__main__":
    main()
