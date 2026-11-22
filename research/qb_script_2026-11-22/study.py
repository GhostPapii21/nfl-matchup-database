"""Two pregame adjustments tested on past seasons (asked after Week 11 Sunday, 2026-11-22).

A. Backup QB: when a team starts someone other than its usual QB, do its receivers fall short of the board's own
   simulation? Rows: the opportunity backtest (pregame/.cache/opportunity_backtest_rows.parquet: the board's simulation
   run on 2024-2026 receiver-games, no QB adjustment). Usual QB = the QB who started the most of the team's earlier games
   that season (2+ earlier games needed). Measured: actual / projected for yards, targets and yards per target, and the
   80+ yard hit rate vs the simulated chance. Fit on 2024-25, checked on 2026.

B. Game script: does a big favorite really throw less, and is the board's rule (pass attempts x (1 - 0.01 x margin),
   margin capped at +/-10) right? Rows: every 2022-2026 regular-season team-game with 3+ earlier games that season.
   Prediction as on the board: plays = mean(team plays, opponent plays allowed) to date, x team pass ratio to date,
   x script multiplier. Compared: no script, the current rule, a refit slope (with and without the cap), and a refit
   that lets the slope depend on the team's passing quality to date (EPA per dropback). Fit 2022-24, test 2025-26.

    python3 research/qb_script_2026-11-22/study.py      # writes results.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
C = ROOT / "pregame" / ".cache"
H = ROOT / "data" / "historical" / "nflverse"


def games():
    g = pd.read_parquet(C / "games.parquet")
    return g[(g.game_type == "REG") & (g.season >= 2022) & g.home_score.notna()].copy()


def team_games(g):
    rows = []
    for r in g.itertuples():
        for team, opp, qb, margin in ((r.home_team, r.away_team, r.home_qb_id, r.spread_line), (r.away_team, r.home_team, r.away_qb_id, -r.spread_line)):
            rows.append({"season": r.season, "week": r.week, "game_id": r.game_id, "team": team, "opp": opp, "qb": qb, "margin": margin})
    t = pd.DataFrame(rows).sort_values(["season", "team", "week"])
    usual, n_prior = [], []
    for (s, tm), grp in t.groupby(["season", "team"], sort=False):
        seen = {}
        for q in grp.qb:
            usual.append(max(seen, key=seen.get) if seen else None)
            n_prior.append(sum(seen.values()))
            seen[q] = seen.get(q, 0) + 1
    t["usual_qb"], t["n_prior"] = usual, n_prior
    t["backup"] = (t.n_prior >= 2) & t.usual_qb.notna() & (t.qb != t.usual_qb)
    return t


# ------------------------------------------------------------------------------------------------------- A. backup QB
def study_backup(t):
    bt = pd.read_parquet(C / "opportunity_backtest_rows.parquet")
    bt = bt[bt.kind == "rec"].copy()
    fr = []                       # player -> team each week, from play-by-play (the weekly stats file stops early in 2026)
    for y in (2024, 2025, 2026):
        q = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["season", "week", "season_type", "posteam", "receiver_player_id", "rusher_player_id"])
        q = q[q.season_type == "REG"]
        for col in ("receiver_player_id", "rusher_player_id"):
            fr.append(q[["season", "week", "posteam", col]].dropna().rename(columns={col: "player_id", "posteam": "team"}))
    st = pd.concat(fr).drop_duplicates(["player_id", "season", "week"])
    bt = bt.merge(st, left_on=["player", "season", "week"], right_on=["player_id", "season", "week"], how="inner")
    bt = bt.merge(t[["season", "week", "team", "backup", "n_prior"]], on=["season", "week", "team"], how="inner")
    bt = bt[bt.n_prior >= 2]

    def summ(d):
        y, p = d.actual_yards.sum(), d.pred_yards_mean.sum()
        tg, pt = d.actual_targets.sum(), d.exp_targets.sum()
        return {"rows": int(len(d)), "yards_ratio": round(y / p, 3), "targets_ratio": round(tg / pt, 3),
                "yards_per_target_ratio": round((y / tg) / (p / pt), 3) if tg and pt else None,
                "hit80": round(float(d.a_y80.mean()), 3), "sim80": round(float(d.p_y80.mean()), 3)}

    def boot(d, b=2000, seed=0):
        rng = np.random.default_rng(seed)
        a, p = d.actual_yards.to_numpy(), d.pred_yards_mean.to_numpy()
        r = [a[i].sum() / p[i].sum() for i in (rng.integers(0, len(d), len(d)) for _ in range(b))]
        return [round(float(np.percentile(r, 2.5)), 3), round(float(np.percentile(r, 97.5)), 3)]

    def rel_ci(bk, us, b=2000, seed=1):
        rng = np.random.default_rng(seed)
        A, P, a, p = bk.actual_yards.to_numpy(), bk.pred_yards_mean.to_numpy(), us.actual_yards.to_numpy(), us.pred_yards_mean.to_numpy()
        r = []
        for _ in range(b):
            i, j = rng.integers(0, len(A), len(A)), rng.integers(0, len(a), len(a))
            r.append((A[i].sum() / P[i].sum()) / (a[j].sum() / p[j].sum()))
        return [round(float(np.percentile(r, 2.5)), 3), round(float(np.percentile(r, 97.5)), 3)]
    out = {}
    for name, d in (("train_2024_25", bt[bt.season <= 2025]), ("test_2026", bt[bt.season == 2026]), ("all", bt)):
        bk, us = d[d.backup], d[~d.backup]
        out[name] = {"backup": summ(bk) | {"yards_ratio_ci95": boot(bk)}, "usual": summ(us) | {"yards_ratio_ci95": boot(us)},
                     "relative_yards": round(summ(bk)["yards_ratio"] / summ(us)["yards_ratio"], 3),
                     "relative_yards_ci95": rel_ci(bk, us),
                     "relative_hit80_over_sim": round((bk.a_y80.mean() / bk.p_y80.mean()) / (us.a_y80.mean() / us.p_y80.mean()), 3),
                     "relative_targets": round(summ(bk)["targets_ratio"] / summ(us)["targets_ratio"], 3),
                     "relative_ypt": round(summ(bk)["yards_per_target_ratio"] / summ(us)["yards_per_target_ratio"], 3)}
    # does scaling the backup-game yards by the train multiplier improve 80+ calibration on the test year?
    tr = out["train_2024_25"]["relative_yards"]
    te = bt[(bt.season == 2026) & bt.backup]
    if len(te):
        def p80_scaled(row, m):     # shift the chance as a lognormal-ish yards model would: z shift by log(m)/sigma, sigma~0.75
            from math import log
            from scipy.stats import norm
            p = min(max(row.p_y80, 1e-4), 1 - 1e-4)
            return float(norm.cdf(norm.ppf(p) + log(m) / 0.75))
        te = te.assign(adj=[p80_scaled(r, tr) for r in te.itertuples()])
        brier = lambda p: round(float(((p - te.a_y80) ** 2).mean()), 5)
        out["test_2026_80plus"] = {"rows": int(len(te)), "hit": round(float(te.a_y80.mean()), 3), "sim": round(float(te.p_y80.mean()), 3),
                                   "adjusted": round(float(te.adj.mean()), 3), "brier_sim": brier(te.p_y80), "brier_adjusted": brier(te.adj)}
    return out


# ------------------------------------------------------------------------------------------------------ B. game script
def study_script(t):
    frames = []
    for y in range(2022, 2027):
        f = C / f"play_by_play_{y}.parquet"
        if f.exists():
            p = pd.read_parquet(f, columns=["game_id", "season", "week", "season_type", "posteam", "defteam", "play_type", "pass_attempt", "rush_attempt", "qb_dropback", "epa"])
            frames.append(p[(p.season_type == "REG") & p.play_type.isin(["pass", "run"])])
    p = pd.concat(frames)
    tg = p.groupby(["season", "week", "game_id", "posteam", "defteam"]).agg(plays=("play_type", "size"), att=("pass_attempt", "sum"), rush=("rush_attempt", "sum"),
                                                                           db=("qb_dropback", "sum"), epa_db=("epa", lambda e: np.nan)).reset_index()
    epa = p[p.qb_dropback == 1].groupby(["game_id", "posteam"]).epa.sum().rename("epa_sum").reset_index()
    tg = tg.drop(columns="epa_db").merge(epa, on=["game_id", "posteam"], how="left")
    tg = tg.sort_values(["season", "posteam", "week"])
    for col in ("plays", "att", "rush", "db", "epa_sum"):
        tg[f"{col}_todate"] = tg.groupby(["season", "posteam"])[col].transform(lambda s: s.shift().expanding().sum())
    tg["n_prior"] = tg.groupby(["season", "posteam"]).cumcount()
    allowed = tg.sort_values(["season", "defteam", "week"]).copy()
    allowed["opp_plays_allowed_todate"] = allowed.groupby(["season", "defteam"]).plays.transform(lambda s: s.shift().expanding().mean())
    allowed["opp_n"] = allowed.groupby(["season", "defteam"]).cumcount()
    tg = tg.merge(allowed[["game_id", "defteam", "opp_plays_allowed_todate", "opp_n"]], on=["game_id", "defteam"])
    tg = tg.merge(t[["game_id", "team", "margin"]], left_on=["game_id", "posteam"], right_on=["game_id", "team"])
    tg = tg[(tg.n_prior >= 3) & (tg.opp_n >= 3)].copy()
    tg["plays_pg"] = tg.plays_todate / tg.n_prior
    tg["base"] = (tg.plays_pg + tg.opp_plays_allowed_todate) / 2 * (tg.att_todate / tg.plays_todate)
    tg["qb_epa"] = tg.epa_sum_todate / tg.db_todate
    tg["ratio"] = tg.att / tg.base
    train, test = tg[tg.season <= 2024], tg[tg.season >= 2025]

    def mae(d, mult):
        return round(float(np.abs(d.att - d.base * mult(d)).mean()), 3)

    def bias(d, mult):
        return round(float((d.att - d.base * mult(d)).mean()), 3)
    cur = lambda d: 1 - 0.01 * d.margin.clip(-10, 10)
    # refit: ratio = 1 + b*m (least squares on train), capped and uncapped
    def fit(cap, qb=False):
        m = train.margin.clip(-cap, cap) if cap else train.margin
        X = np.column_stack([np.ones(len(train)), m] + ([m * (train.qb_epa - train.qb_epa.mean())] if qb else []))
        w = train.base.to_numpy()
        coef, *_ = np.linalg.lstsq(X * w[:, None], train.att.to_numpy(), rcond=None)
        return coef
    res = {"team_games": {"train": int(len(train)), "test": int(len(test))}}
    models = {"no_script": lambda d: 1.0, "current_rule": cur}
    for cap in (10, None):
        c = fit(cap)
        models[f"refit_cap{cap or 'none'}"] = (lambda c, cap: lambda d: c[0] + c[1] * (d.margin.clip(-cap, cap) if cap else d.margin))(c, cap)
        res[f"refit_cap{cap or 'none'}_coef"] = [round(float(x), 4) for x in c]
    c = fit(10, qb=True)
    mu = train.qb_epa.mean()
    models["refit_cap10_qb"] = lambda d, c=c, mu=mu: c[0] + c[1] * d.margin.clip(-10, 10) + c[2] * d.margin.clip(-10, 10) * (d.qb_epa - mu)
    res["refit_cap10_qb_coef"] = [round(float(x), 4) for x in c]
    res["test_mae"] = {k: mae(test, f) for k, f in models.items()}
    res["test_bias"] = {k: bias(test, f) for k, f in models.items()}
    # by margin bucket on the test years: actual / base, and what the current rule says
    b = pd.cut(test.margin, [-40, -10, -6, -3, 3, 6, 10, 40])
    res["test_by_margin"] = [{"margin": str(k), "games": int(len(d)), "actual_over_base": round(float(d.att.sum() / d.base.sum()), 3),
                              "current_rule": round(float((d.base * cur(d)).sum() / d.base.sum()), 3)} for k, d in test.groupby(b, observed=True)]
    # big favourites with a good passing offense (top third of EPA per dropback to date)
    hi = test.qb_epa > train.qb_epa.quantile(2 / 3)
    for name, d in (("fav10_good_passing", test[(test.margin >= 10) & hi]), ("fav10_other", test[(test.margin >= 10) & ~hi])):
        res[name] = {"games": int(len(d)), "actual_over_base": round(float(d.att.sum() / d.base.sum()), 3) if len(d) else None,
                     "current_rule": round(float((d.base * cur(d)).sum() / d.base.sum()), 3) if len(d) else None}
    # rushing side of the same rule: team rush attempts x (1 + 0.012 x margin), margin capped at +/-10
    tg["base_r"] = (tg.plays_pg + tg.opp_plays_allowed_todate) / 2 * (tg.rush_todate / tg.plays_todate)
    train, test = tg[tg.season <= 2024], tg[tg.season >= 2025]
    X = np.column_stack([np.ones(len(train)), train.margin.clip(-10, 10)]) * train.base_r.to_numpy()[:, None]
    cr, *_ = np.linalg.lstsq(X, train.rush.to_numpy(), rcond=None)
    rm = {"no_script": lambda d: 1.0, "current_rule": lambda d: 1 + 0.012 * d.margin.clip(-10, 10),
          "refit_cap10": lambda d: cr[0] + cr[1] * d.margin.clip(-10, 10)}
    res["rush_refit_cap10_coef"] = [round(float(x), 4) for x in cr]
    res["rush_test_mae"] = {k: round(float(np.abs(test.rush - test.base_r * f(test)).mean()), 3) for k, f in rm.items()}
    b = pd.cut(test.margin, [-40, -10, -6, -3, 3, 6, 10, 40])
    res["rush_test_by_margin"] = [{"margin": str(k), "games": int(len(d)), "actual_over_base": round(float(d.rush.sum() / d.base_r.sum()), 3),
                                   "current_rule": round(float((d.base_r * rm["current_rule"](d)).sum() / d.base_r.sum()), 3)} for k, d in test.groupby(b, observed=True)]
    return res


def main():
    t = team_games(games())
    out = {"A_backup_qb": study_backup(t), "B_game_script": study_script(t)}
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
