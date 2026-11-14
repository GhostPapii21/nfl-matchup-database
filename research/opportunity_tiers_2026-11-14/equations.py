"""The compact equations behind the calculator, plus three checks: true (full-season) defense quality, missing teammates,
and the game total. Fit 2022-2024, tested 2025-2026. Writes equations.json."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
import statsmodels.api as sm

import study as S


def prep(r):
    r = r.copy()
    r["log_tgt"] = np.log(r.tgt_blend.clip(0.5))
    r["ypt_s"] = (r.ypt * r.tgt_pg * r.games_prior + 8.0 * 30) / (r.tgt_pg * r.games_prior + 30)
    r["log_ypt"] = np.log(r.ypt_s.clip(2))
    pa = r.groupby(["season", "week", "pos"]).opp_pos_ypg.transform("mean")
    r["def_ratio"] = (r.opp_pos_ypg / pa).clip(0.4, 2.5).fillna(1.0)
    r["log_def_pos"] = np.log(r.def_ratio)
    r["imp_c"] = r.implied - 22.0
    r["adot_c"] = r.adot - 9.0
    return r


def missing_share(r):
    raw = pd.read_parquet(S.ROWS).sort_values(["season", "team", "week"])
    miss = {}
    for (s, t), g in raw.groupby(["season", "team"]):
        weeks = sorted(g.week.unique())
        for i, w in enumerate(weeks[1:], 1):
            prev = g[g.week == weeks[i - 1]].set_index("player").share
            now = set(g[g.week == w].player)
            miss[(s, t, w)] = float(prev[[p not in now for p in prev.index]].sum())
    return [miss.get(k, np.nan) for k in zip(r.season, r.team, r.week)]


def main():
    r = prep(S.load())
    tr, te = r[r.season.isin(S.TRAIN)], r[r.season.isin(S.TEST)]
    out = {}
    Xy = ["log_tgt", "log_ypt", "imp_c", "log_def_pos"]
    my = sm.GLM(tr.y_yds, sm.add_constant(tr[Xy]), family=sm.families.Poisson()).fit(scale="X2")
    Xr = ["log_tgt", "adot_c", "imp_c", "log_def_pos"]
    mr = sm.GLM(tr.y_rec, sm.add_constant(tr[Xr]), family=sm.families.Poisson()).fit(scale="X2")
    r["pred_yds"] = my.predict(sm.add_constant(r[Xy], has_constant="add"))
    r["pred_rec"] = mr.predict(sm.add_constant(r[Xr], has_constant="add"))
    r["log_pred"] = np.log(r.pred_yds)
    tr, te = r[r.season.isin(S.TRAIN)], r[r.season.isin(S.TEST)]
    out["yards"] = {"coef": my.params.round(4).to_dict(), "se": my.bse.round(4).to_dict(),
                    "test_corr": S.r1(np.corrcoef(te.pred_yds, te.y_yds)[0, 1]), "baseline_corr": S.r1(np.corrcoef(te.yds_avg, te.y_yds)[0, 1])}
    out["receptions"] = {"coef": mr.params.round(4).to_dict(), "se": mr.bse.round(4).to_dict(),
                         "test_corr": S.r1(np.corrcoef(te.pred_rec, te.y_rec)[0, 1])}
    for k in (80, 100):
        X = ["log_pred", "adot_c"]
        lm = sm.GLM((tr.y_yds >= k).astype(float), sm.add_constant(tr[X]), family=sm.families.Binomial()).fit()
        p = lm.predict(sm.add_constant(te[X], has_constant="add"))
        nm = te.yds_avg.between(*S.NORMAL)
        out[f"p{k}"] = {"coef": lm.params.round(4).to_dict(), "test_auc": S.auc(p, te.y_yds >= k),
                        "normal_test_auc": S.auc(p[nm], te[nm].y_yds >= k), "calibration": S.calib(p.values, (te.y_yds >= k).values)}
    # true defense quality: full-season yards per attempt allowed vs league
    pb = []
    for y in sorted(r.season.unique()):
        p = pd.read_parquet(S.C / f"play_by_play_{y}.parquet", columns=["season_type", "defteam", "pass_attempt", "sack", "passing_yards"])
        p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.sack != 1)]
        s = p.groupby("defteam").passing_yards.apply(lambda x: x.fillna(0).sum() / len(x))
        pb.append(pd.DataFrame({"season": y, "opp": s.index, "hs_ratio": (s / s.mean()).values}))
    h = r.merge(pd.concat(pb), on=["season", "opp"])
    h["log_hs"] = np.log(h.hs_ratio)
    htr = h[h.season.isin(S.TRAIN)]
    a = sm.GLM(htr.y_yds, sm.add_constant(htr[["log_tgt", "log_ypt", "imp_c", "log_hs"]]), family=sm.families.Poisson()).fit(scale="X2")
    b = sm.GLM(htr.y_tgt, sm.add_constant(htr[["log_tgt", "imp_c", "log_hs"]]), family=sm.families.Poisson()).fit(scale="X2")
    out["true_defense"] = {"yards_elasticity": S.r1(a.params.log_hs), "yards_se": S.r1(a.bse.log_hs),
                           "targets_elasticity": S.r1(b.params.log_hs), "targets_se": S.r1(b.bse.log_hs),
                           "pregame_tier_ratio": h.groupby("tier").opp_ypa.mean().round(3).to_dict(),
                           "season_tier_ratio": h.groupby("season_tier").hs_ratio.mean().round(3).to_dict()}
    # tier effect early vs late season
    late = []
    for lo, hi in ((4, 7), (8, 18)):
        x = r[r.week.between(lo, hi)]
        for t, z in x.groupby("tier"):
            late.append({"weeks": f"{lo}-{hi}", "tier": t, "n": int(len(z)), "yards_vs_avg": S.r1(z.y_yds.mean() / z.yds_avg.mean()),
                         "ypt_vs_his": S.r1(z.y_yds.sum() / (z.ypt * z.y_tgt).sum()), "targets_vs_avg": S.r1(z.y_tgt.mean() / z.tgt_pg.mean())})
    out["tier_by_season_phase"] = late
    # missing teammates
    r["missing"] = missing_share(r)
    m = r[r.missing.notna()].copy()
    m["mb"] = pd.cut(m.missing, [-0.01, 0.0001, 0.10, 0.20, 1], labels=["none", "under 10%", "10-20%", "20%+"])
    out["missing_teammates"] = [{"missing": str(k), "n": int(len(z)), "targets_vs_avg": S.r1(z.y_tgt.mean() / z.tgt_pg.mean()),
                                 "yards_vs_avg": S.r1(z.y_yds.mean() / z.yds_avg.mean()), "p80": S.r1((z.y_yds >= 80).mean())}
                                for k, z in m.groupby("mb", observed=True)]
    # game total for normal receivers
    n = r[r.yds_avg.between(*S.NORMAL)].copy()
    n["tl"] = pd.cut(n.total_line, [0, 40.5, 44.5, 48.5, 70], labels=["40.5 or less", "41-44.5", "45-48.5", "49+"])
    out["total_line_normal"] = [{"total": str(k), "n": int(len(z)), "catches": S.r1(z.y_rec.mean(), 2), "yards": S.r1(z.y_yds.mean(), 1),
                                 "p80": S.r1((z.y_yds >= 80).mean())} for k, z in n.groupby("tl", observed=True)]
    # targets needed for a median-80 projection at a given YPT
    c = my.params
    need = {}
    for ypt in (7.0, 8.0, 9.0, 10.0):
        t = np.exp((np.log(80) - c.const - c.log_ypt * np.log(ypt)) / c.log_tgt)
        need[str(ypt)] = S.r1(t, 1)
    out["targets_for_80_mean"] = need
    (S.HERE / "equations.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
