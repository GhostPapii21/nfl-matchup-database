#!/usr/bin/env python3
"""Period grading vs actuals + pace realism. Research/development only. Not an approved pick."""
from __future__ import annotations
import json, time
from pathlib import Path
import pandas as pd
from validation.asof_grade import grade_week_games
from validation.period_grade import grade_periods_for_games
from validation.realism import compare_sim_vs_actual_pace
from validation.weather_hook import weather_scenario_from_parent
from config_load import load_config

ROOT = Path(__file__).resolve().parent
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"
ART = ROOT / "artifacts/validation"
ART.mkdir(parents=True, exist_ok=True)

N_SIMS = 150


def main():
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    t0 = time.perf_counter()
    rows = grade_week_games(PBP, weeks=list(range(1, 9)), n_sims=N_SIMS, seed_base=20261105)
    # FG-level already in rows; now period grade for GRADED_FULL
    t1 = time.perf_counter()
    period = grade_periods_for_games(PBP, rows, n_sims=N_SIMS, seed_base=20261105)
    period_sec = time.perf_counter() - t1
    asof_sec = t1 - t0

    pd.DataFrame(rows).to_csv(ART / "asof_grade_per_game.csv", index=False)
    pd.DataFrame(period["by_game"]).to_csv(ART / "period_grade_per_game.csv", index=False)

    t2 = time.perf_counter()
    realism = compare_sim_vs_actual_pace(cfg, pbp_path=PBP, n_sims=200, seed=11)
    realism_sec = time.perf_counter() - t2
    (ART / "realism_pace_diagnostics.json").write_text(json.dumps(realism, indent=2) + "\n")

    weather = weather_scenario_from_parent(None)
    (ART / "weather_scenario_hook.json").write_text(json.dumps(weather, indent=2) + "\n")

    n_full = sum(1 for r in rows if r["grade_status"] == "GRADED_FULL")
    n_period = period["metrics"]["n_games_period_graded"]
    out = {
        "approved_pick": False,
        "evaluation_label": "development_w1_8_inspected_not_untouched_holdout",
        "prior_artifacts_preserved": "artifacts/validation/pre_period_grade_12a7768/",
        "n_sims": N_SIMS,
        "runtime_sec": {"asof_fg_grade": asof_sec, "period_grade": period_sec, "realism": realism_sec},
        "fg_grade_coverage": {"graded_full": n_full, "denominator": len(rows)},
        "period_metrics": period["metrics"],
        "realism": realism,
        "weather": weather,
        "residual_matrix": {
            "true_pressure_qbp": "MISSING_paid_FTN",
            "man_zone_mofo_routes": "MISSING_free_FTN_29col",
            "cb_s_dt_replacement_coeffs": "MISSING_UNVERIFIED_notes_only",
            "weather_auto_prop_downgrade": "DISABLED_pending_NWS",
        },
    }
    (ART / "period_realism_metrics.json").write_text(json.dumps(out, indent=2) + "\n")

    m = period["metrics"]
    summary = f"""# Period grading + realism (post-12a7768 continuation)

**Not an approved pick.** Development W1–8 only. Prior FG 0/15 and 13/15 artifacts preserved.

## As-of FG coverage
GRADED_FULL: {n_full}/{len(rows)} (W1 skips remain)

## Period grading (N={N_SIMS}/game, {n_period} games, {period_sec:.1f}s)
| Period | MAE home | MAE away | Brier home-win |
|---|---:|---:|---:|
| Q1 | {m.get('mae_q1_home')} | {m.get('mae_q1_away')} | (see H1+) |
| H1 | {m.get('mae_h1_home'):.2f} | {m.get('mae_h1_away'):.2f} | {m.get('brier_h1_home_win'):.3f} |
| H2 | {m.get('mae_h2_home'):.2f} | {m.get('mae_h2_away'):.2f} | {m.get('brier_h2_home_win'):.3f} |
| Reg | {m.get('mae_reg_home'):.2f} | {m.get('mae_reg_away'):.2f} | {m.get('brier_reg_home_win'):.3f} |
| FG  | {m.get('mae_fg_home'):.2f} | {m.get('mae_fg_away'):.2f} | {m.get('brier_fg_home_win'):.3f} |

Period metrics are **separate** from FG (FG row repeated for comparison).

## Realism (development diagnostic)
Actual combined offense snaps (apples-to-apples): {realism['actual_combined_offense_snaps']['mean_combined_offense_snaps']:.1f} (n_games={realism['actual_combined_offense_snaps']['n_games']})
Actual per-team offense snaps mean: {realism['actual']['mean_offense_snaps_per_team_game']:.1f} (legacy; n_team_games={realism['actual']['n_team_games']})
≈2× actual (approx only): {realism['actual_both_offenses_snaps_approx']:.1f}
Sim mean snaps/game: {realism['sim']['mean_snaps_per_game']:.1f}
Drive length plays actual mean/median: {realism['actual']['drive_length_plays']['mean']:.2f} / {realism['actual']['drive_length_plays']['median']:.1f} (n_drives={realism['actual']['drive_length_plays']['n_drives']})
Delta sim − combined actual: {realism['comparison']['sim_minus_actual_combined']:.1f}
Delta sim − 2×actual snaps (approx): {realism['comparison']['sim_snaps_minus_2x_team_snaps']:.1f}

## Residual blockers (unchanged / no invent)
- True pressure (FTN qbp): MISSING paid
- Man/zone/MOFO/routes: MISSING free FTN 29-col
- CB/S/DT replacement coeffs: MISSING
- Weather: hook only PENDING_NWS — no DK auto-downgrade
"""
    (ART / "SUMMARY.md").write_text(summary)
    # also keep metrics.json pointer
    prev = {}
    mp = ART / "metrics.json"
    if mp.exists():
        prev = json.loads(mp.read_text())
    prev["period_realism_extension"] = out
    prev["summary_updated_et"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    mp.write_text(json.dumps(prev, indent=2) + "\n")
    print(summary)


if __name__ == "__main__":
    main()
