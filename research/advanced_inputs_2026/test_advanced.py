"""Phase 3, item B: do Next Gen Stats / PFR advanced receiving inputs improve the receiver projection?

Base: the repo's yards and targets GLMs (research/opportunity_tiers_2026-11-14/equations.py inputs), fit 2022-2024.
Features, each as of BEFORE the game (season to date through the previous week, weighted by targets; players need 15+
prior targets in NGS weeks): NGS separation, cushion, YAC above expectation, share of team intended air yards; PFR drop
rate and broken tackles per reception. Each is standardized and tested as a multiplier on top of the projection
(Poisson GLM, offset log(projection)), fit 2022-2024, tested 2025-2026 on the same rows. Writes results.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "pregame" / ".cache"
sys.path.insert(0, str(ROOT / "research" / "opportunity_tiers_2026-11-14"))
import equations as E  # noqa: E402
import study as S  # noqa: E402

SEASONS = (2022, 2023, 2024, 2025, 2026)


def asof(df, key, cols, wcol):
    """Season-to-date weighted means through the previous week, keyed (season, week, key)."""
    df = df.sort_values(["season", key, "week"]).copy()
    for c in cols:
        df[f"_{c}"] = df[c] * df[wcol]
    g = df.groupby(["season", key])
    cum = {c: g[f"_{c}"].cumsum() - df[f"_{c}"] for c in cols}
    w = g[wcol].cumsum() - df[wcol]
    out = pd.DataFrame({"season": df.season, key: df[key], "week": df.week + 1, "prior_w": w})
    for c in cols:
        out[c] = cum[c] / w.replace(0, np.nan)
    return out


def ngs():
    n = pd.read_parquet(C / "ngs_receiving.parquet")
    n = n[(n.season_type == "REG") & (n.week > 0) & n.season.isin(SEASONS)]
    cols = ["avg_separation", "avg_cushion", "avg_yac_above_expectation", "percent_share_of_intended_air_yards"]
    a = asof(n, "player_gsis_id", cols, "targets").rename(columns={"player_gsis_id": "player"})
    return a[a.prior_w >= 15]


def pfr():
    rows = []
    for y in SEASONS:
        p = pd.read_parquet(C / f"advstats_week_rec_{y}.parquet")
        r = pd.read_parquet(C / f"roster_weekly_{y}.parquet", columns=["pfr_id", "gsis_id"]).dropna().drop_duplicates("pfr_id")
        p = p.merge(r, left_on="pfr_player_id", right_on="pfr_id", how="inner")
        rows.append(p[["season", "week", "gsis_id", "receiving_drop", "receiving_broken_tackles"]])
    p = pd.concat(rows)
    pbp = []
    for y in SEASONS:
        x = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["season", "week", "season_type", "receiver_player_id", "complete_pass", "pass_attempt"])
        x = x[(x.season_type == "REG") & x.receiver_player_id.notna()]
        pbp.append(x.groupby(["season", "week", "receiver_player_id"]).agg(tg=("pass_attempt", "size"), rec=("complete_pass", "sum")).reset_index())
    pbp = pd.concat(pbp).rename(columns={"receiver_player_id": "gsis_id"})
    p = p.merge(pbp, on=["season", "week", "gsis_id"], how="right").fillna({"receiving_drop": 0, "receiving_broken_tackles": 0})
    p = p.sort_values(["season", "gsis_id", "week"])
    g = p.groupby(["season", "gsis_id"])
    out = pd.DataFrame({"season": p.season, "player": p.gsis_id, "week": p.week + 1,
                        "drop_rate": (g.receiving_drop.cumsum() - p.receiving_drop) / (g.tg.cumsum() - p.tg).replace(0, np.nan),
                        "btk_per_rec": (g.receiving_broken_tackles.cumsum() - p.receiving_broken_tackles) / (g.rec.cumsum() - p.rec).replace(0, np.nan),
                        "prior_tg": g.tg.cumsum() - p.tg})
    return out[out.prior_tg >= 15].drop(columns="prior_tg")


def dev(y, mu):
    y, mu = np.asarray(y, float), np.asarray(mu, float)
    return float(2 * np.sum(np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0) - (y - mu)))


def main():
    r = E.prep(S.load())
    tr0 = r[r.season.isin(S.TRAIN)]
    Xy = ["log_tgt", "log_ypt", "imp_c", "log_def_pos"]
    Xt = ["log_tgt", "imp_c", "log_def_pos"]
    my = sm.GLM(tr0.y_yds, sm.add_constant(tr0[Xy]), family=sm.families.Poisson()).fit(scale="X2")
    mt = sm.GLM(tr0.y_tgt, sm.add_constant(tr0[Xt]), family=sm.families.Poisson()).fit(scale="X2")
    r["pred_yds"] = my.predict(sm.add_constant(r[Xy], has_constant="add"))
    r["pred_tgt"] = mt.predict(sm.add_constant(r[Xt], has_constant="add"))
    feats = ["avg_separation", "avg_cushion", "avg_yac_above_expectation", "percent_share_of_intended_air_yards", "drop_rate", "btk_per_rec"]
    # nearest earlier week's as-of value (players can miss NGS weeks): merge_asof per season
    base = r.assign(week=r.week.astype("int64"), season=r.season.astype("int64")).sort_values("week")
    for f_df in (ngs(), pfr()):
        f_df = f_df.assign(week=f_df.week.astype("int64"), season=f_df.season.astype("int64")).sort_values("week")
        base = pd.merge_asof(base, f_df.drop(columns=[c for c in ("prior_w",) if c in f_df.columns]), on="week", by=["season", "player"], direction="backward")
    out = {"rows": int(len(base)), "features": {}}
    for target, pred in (("y_yds", "pred_yds"), ("y_tgt", "pred_tgt")):
        res = {}
        for f in feats:
            d = base[base[f].notna()].copy()
            mu, sd = d.loc[d.season.isin(S.TRAIN), f].mean(), d.loc[d.season.isin(S.TRAIN), f].std()
            d["z"] = ((d[f] - mu) / sd).clip(-3, 3)
            tr, te = d[d.season.isin(S.TRAIN)], d[d.season.isin(S.TEST)]
            m = sm.GLM(tr[target], sm.add_constant(tr[["z"]]), family=sm.families.Poisson(), offset=np.log(tr[pred])).fit(scale="X2")
            mu1 = m.predict(sm.add_constant(te[["z"]], has_constant="add"), offset=np.log(te[pred]))
            mu0 = te[pred] * np.exp(np.log(tr[target].sum() / tr[pred].sum()))   # same rows, level-matched base
            b, se = m.params["z"], m.bse["z"]
            res[f] = {"rows_train": int(len(tr)), "rows_test": int(len(te)), "per_1sd_multiplier": round(float(np.exp(b)), 3),
                      "ci95": [round(float(np.exp(b - 1.96 * se)), 3), round(float(np.exp(b + 1.96 * se)), 3)], "significant": bool(abs(b / se) > 1.96),
                      "test_deviance_base": round(dev(te[target], mu0), 1), "test_deviance_with": round(dev(te[target], mu1), 1),
                      "improves_test": bool(dev(te[target], mu1) < dev(te[target], mu0))}
        out["features"][target] = res
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")
    for t, res in out["features"].items():
        print(f"\n{t}")
        for f, v in res.items():
            print(f"  {f:<38} train {v['rows_train']:>5} test {v['rows_test']:>4}  x{v['per_1sd_multiplier']:.3f}/SD  CI {v['ci95']}  "
                  f"{'SIG' if v['significant'] else '   '}  test dev {v['test_deviance_base']} -> {v['test_deviance_with']}  {'BETTER' if v['improves_test'] else 'worse'}")


if __name__ == "__main__":
    main()
