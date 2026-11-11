"""Walk-forward comparison of period-engine sampling modes (research only, no prices).

Same as-of policy as walkforward.py: each 2026 week-W game uses only (season, week) < (2026, W).
Writes artifacts/sampling_comparison_2026_w1_8.json. W1-8 is development data, not a holdout.

  python3 compare_sampling.py [n_sims]
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from monte_carlo import simulate_game, stable_seed
from reconstruct import as_of_mask
from walkforward import build_history

ROOT = Path(__file__).resolve().parent
PERIODS = ("q1", "q2", "q3", "q4", "h1", "reg", "fg")
MODES = ("independent", "matchup_pair")


def score_mode(hist, p26, mode, n_sims, seed=20261105):
    rows = []
    for _, g in p26.sort_values(["week", "game_id"]).iterrows():
        asof = hist[as_of_mask(hist, int(g.season), int(g.week))]
        s = stable_seed(seed, int(g.week), str(g.game_id))
        sim = simulate_game(asof, g.home_team, g.away_team, n=n_sims, seed=s, sampling=mode)
        if sim.get("error"):
            continue
        A = sim["arrays"]
        for per in PERIODS:
            h, a = A[f"{per}_home"], A[f"{per}_away"]
            ah, aa = float(g[f"{per}_home"]), float(g[f"{per}_away"])
            m = h - a
            p3 = np.array([(m > 0).mean(), (m == 0).mean(), (m < 0).mean()])
            y = 0 if ah > aa else (1 if ah == aa else 2)
            rows.append(dict(period=per, week=int(g.week),
                             err_total=(h + a).mean() - (ah + aa), err_margin=m.mean() - (ah - aa),
                             brier_home=(p3[0] - (y == 0)) ** 2,
                             logloss3=-np.log(max(p3[y], 1e-6)),
                             p_tie=p3[1], tie=float(y == 1),
                             # rank of the actual margin in the simulated margin distribution (PIT); uniform if calibrated
                             pit_margin=float((m < ah - aa).mean() + 0.5 * (m == ah - aa).mean())))
    return pd.DataFrame(rows)


def summarise(df):
    out = {}
    for per, d in df.groupby("period"):
        pit = d.pit_margin.to_numpy()
        out[per] = dict(
            n=int(len(d)),
            mae_total=float(d.err_total.abs().mean()), bias_total=float(d.err_total.mean()),
            mae_margin=float(d.err_margin.abs().mean()),
            brier_home_win=float(d.brier_home.mean()), logloss_3way=float(d.logloss3.mean()),
            mean_p_tie=float(d.p_tie.mean()), actual_tie_rate=float(d.tie.mean()),
            # share of actual margins in the central 50% of the simulated margin distribution (0.50 if calibrated)
            margin_central50_coverage=float(((pit > 0.25) & (pit < 0.75)).mean()),
        )
    return out


def main(n_sims=20_000):
    hist, p26 = build_history()
    res = {mode: summarise(score_mode(hist, p26, mode, n_sims)) for mode in MODES}
    report = {
        "engine": "period_engine_v0", "n_sims_per_game": n_sims, "set_label": "development_inspected_w1_8_not_untouched_holdout",
        "modes": res,
        "limitations": ["no prices: accuracy and calibration only, no edge/ROI",
                        "121 games; differences of a few thousandths in Brier are within noise",
                        "W1-8 already inspected during development; confirm on later weeks before relying on it"],
    }
    (ROOT / "artifacts/sampling_comparison_2026_w1_8.json").write_text(json.dumps(report, indent=2) + "\n")
    cols = ["mae_total", "bias_total", "mae_margin", "brier_home_win", "logloss_3way", "mean_p_tie", "actual_tie_rate", "margin_central50_coverage"]
    for per in PERIODS:
        print(per, *[f"{c}: " + " / ".join(f"{res[m][per][c]:.4f}" for m in MODES) for c in cols], sep="\n  ")
    return report


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20_000)
