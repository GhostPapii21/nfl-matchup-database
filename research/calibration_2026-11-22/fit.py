"""Calibration layer for the opportunity simulation (Phase 3, item A).

Data: pregame/.cache/opportunity_backtest_rows.parquet (dashboard/backtest_opportunity.py; every projection uses only
earlier weeks). For each (kind, stat) one logistic recalibration pooled over thresholds, so it works at any line:
    logit(p_cal) = a + b * logit(p_sim) + c * log(threshold)
Fit on 2024-2025, tested on 2026. Kept per (kind, stat) only if 2026 Brier improves at the pooled level.
Writes dashboard/calibration.json and research/calibration_2026-11-22/results.json."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STATS = {("rec", "y"): "receiving_yards", ("rec", "r"): "receptions", ("rush", "y"): "rushing_yards", ("rush", "c"): "carries"}
EPS = 1e-3


def logit(p):
    p = np.clip(p, EPS, 1 - EPS)
    return np.log(p / (1 - p))


def long_rows(df, kind, pre):
    d = df[df.kind == kind]
    out = []
    for c in d.columns:
        if c.startswith(f"p_{pre}") and c[len(pre) + 2:].isdigit():
            t = int(c[len(pre) + 2:])
            out.append(pd.DataFrame({"season": d.season, "t": t, "p": d[c], "a": d[f"a_{pre}{t}"]}))
    return pd.concat(out, ignore_index=True).dropna()


def brier(p, a):
    return float(np.mean((p - a) ** 2))


def main():
    df = pd.read_parquet(ROOT / "pregame" / ".cache" / "opportunity_backtest_rows.parquet")
    model, res = {}, {"source_rows": int(len(df)), "seasons": sorted(int(s) for s in df.season.unique()), "stats": {}}
    for (kind, pre), name in STATS.items():
        L = long_rows(df, kind, pre)
        L["lp"], L["lt"] = logit(L.p), np.log(L.t)
        tr, te = L[L.season < 2026], L[L.season == 2026]
        m = sm.GLM(tr.a, sm.add_constant(tr[["lp", "lt"]]), family=sm.families.Binomial()).fit()
        pc = m.predict(sm.add_constant(te[["lp", "lt"]], has_constant="add"))
        per_t = []
        for t, x in te.assign(pc=pc).groupby("t"):
            per_t.append({"threshold": int(t), "n": int(len(x)), "hit_rate": round(float(x.a.mean()), 3), "avg_sim": round(float(x.p.mean()), 3),
                          "avg_calibrated": round(float(x.pc.mean()), 3), "brier_sim": round(brier(x.p, x.a), 4), "brier_calibrated": round(brier(x.pc, x.a), 4)})
        b0, b1 = brier(te.p, te.a), brier(pc, te.a)
        keep = b1 < b0 and all(r["brier_calibrated"] <= r["brier_sim"] + 0.0005 for r in per_t)
        bins = pd.cut(te.p, [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0001], right=False)
        tab = te.assign(pc=pc, bin=bins).groupby("bin", observed=True).agg(n=("a", "size"), sim=("p", "mean"), calibrated=("pc", "mean"), actual=("a", "mean")).round(3).reset_index()
        tab["bin"] = tab["bin"].astype(str)
        res["stats"][name] = {"coef": {k: round(float(v), 4) for k, v in m.params.items()}, "train_rows": int(len(tr)), "test_rows": int(len(te)),
                              "brier_2026_sim": round(b0, 5), "brier_2026_calibrated": round(b1, 5), "kept": bool(keep), "by_threshold_2026": per_t,
                              "calibration_2026": tab.to_dict("records")}
        model[name] = {"const": float(m.params["const"]), "lp": float(m.params["lp"]), "lt": float(m.params["lt"]), "enabled": bool(keep)}
    model["_meta"] = {"form": "logit(p_cal) = const + lp*logit(p_sim) + lt*log(threshold)", "fit": "2024-2025", "tested": "2026",
                      "source": "research/calibration_2026-11-22/fit.py"}
    (ROOT / "dashboard" / "calibration.json").write_text(json.dumps(model, indent=1) + "\n")
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    for n, r in res["stats"].items():
        print(f"{n}: Brier 2026 {r['brier_2026_sim']} -> {r['brier_2026_calibrated']}  kept={r['kept']}  coef={r['coef']}")
        for x in r["by_threshold_2026"]:
            print(f"   {x['threshold']:>4}: hit {x['hit_rate']:.3f} sim {x['avg_sim']:.3f} cal {x['avg_calibrated']:.3f} | Brier {x['brier_sim']} -> {x['brier_calibrated']}")


if __name__ == "__main__":
    main()
