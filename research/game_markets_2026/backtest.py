"""Backtest of dashboard/gamemodel.py: 2025-2026 games scored with neighbors drawn only from 2022-2024.
Compares against a no-information baseline (league rates in 2022-2024) and reports calibration."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from dashboard import gamemodel as G  # noqa: E402


def main():
    h = G.history()
    tr, te = h[h.season <= 2024], h[h.season >= 2025]
    rows = []
    for r in te.itertuples():
        nb = G.neighbors(r.home_imp, r.away_imp, hist=tr)
        for pre in ("q1_", "q2_", "q3_", "q4_", "h1_", "h2_"):
            hp, ap = G.period_points(nb, pre)
            qs = G.PERIODS[pre]
            ah = sum(getattr(r, f"h_{q}") for q in qs)
            aa = sum(getattr(r, f"a_{q}") for q in qs)
            m = hp - ap
            tot = hp + ap
            line = float(np.median(tot)) + 0.5 if pre.startswith("q") else float(np.median(tot)) + 0.5
            rows.append({"period": pre[:-1], "p_home": (m > 0).mean(), "p_tie": (m == 0).mean(), "y_home": int(ah > aa), "y_tie": int(ah == aa),
                         "p_over": (tot > line).mean(), "y_over": int(ah + aa > line),
                         "base_home": None, "fav_home": r.spread_line > 0})
    d = pd.DataFrame(rows)
    out = {}
    for per, x in d.groupby("period"):
        trp = tr  # baseline rates from training seasons
        qs = G.PERIODS[per + "_"]
        b_home = float((trp[[f"h_{q}" for q in qs]].sum(axis=1) > trp[[f"a_{q}" for q in qs]].sum(axis=1)).mean())
        brier = lambda p, y: float(np.mean((p - y) ** 2))
        out[per] = {"games": int(len(x)), "home_wins_period": round(float(x.y_home.mean()), 3), "ties": round(float(x.y_tie.mean()), 3),
                    "brier_home_win_model": round(brier(x.p_home, x.y_home), 4), "brier_home_win_baseline": round(brier(b_home, x.y_home), 4),
                    "brier_tie_model": round(brier(x.p_tie, x.y_tie), 4), "brier_tie_baseline": round(brier(float(x.y_tie.mean()), x.y_tie), 4),
                    "over_rate_at_model_median": round(float(x.y_over.mean()), 3),
                    "calibration_home_win": x.assign(b=pd.cut(x.p_home, [0, .3, .4, .5, .6, .7, 1])).groupby("b", observed=True)
                        .agg(n=("y_home", "size"), said=("p_home", "mean"), hit=("y_home", "mean")).round(3).reset_index().astype({"b": str}).to_dict("records")}
    (Path(__file__).resolve().parent / "backtest.json").write_text(json.dumps(out, indent=1))
    for per, v in out.items():
        print(f"{per}: n={v['games']} home wins {v['home_wins_period']} ties {v['ties']} | Brier home-win model {v['brier_home_win_model']} vs baseline {v['brier_home_win_baseline']} | over at model median {v['over_rate_at_model_median']}")
        print("   calib:", [(c['b'], c['n'], c['said'], c['hit']) for c in v['calibration_home_win']])


if __name__ == "__main__":
    main()
