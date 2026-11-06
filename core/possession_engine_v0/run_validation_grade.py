#!/usr/bin/env python3
"""Reproducible validation + grading after P1/P2/P3 fixes. Research only. Not an approved pick."""
from __future__ import annotations
import json, time, hashlib
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from config_load import load_config
from validation.accounting import run_accounting_checks
from validation.asof_grade import list_jaxbal_games, grade_week_games
from pbp_filter import load_involvement_plays
from effects.evidence_tables import load_ftn_join, explosive_tables, qb_completion_splits, recent_form_miss_audit

ROOT = Path(__file__).resolve().parent
PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"
ART = ROOT / "artifacts/validation"
ART.mkdir(parents=True, exist_ok=True)

N_ACCT = 100
N_GRADE = 150  # practical per game ×13 ≈ runtime budget


def refresh_freeze():
    import subprocess
    repo_root = Path(__file__).resolve().parents[2]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True).strip()
    files = [
        "simulate.py", "state.py", "pbp_filter.py", "validation/asof_grade.py",
        "validation/accounting.py", "effects/apply_supported.py", "effects/evidence_tables.py",
        "config/jax_bal_tnf_2026-11-05_data_only.json",
    ]
    h = hashlib.sha256()
    rows = []
    for f in files:
        b = (ROOT / f).read_bytes()
        fh = hashlib.sha256(b).hexdigest()
        h.update(fh.encode()); h.update(b)
        rows.append({"path": f, "sha256": fh})
    man = {
        "frozen_at_et": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "git_commit_pre_this_run": commit,
        "bundle_sha256": h.hexdigest(),
        "files": rows,
        "prior_0of15_preserved": "artifacts/validation/pre_fix_b7b5796_0of15/",
        "evaluation_label": "development_w1_8_inspected_not_untouched_holdout",
        "approved_pick": False,
        "prior_year_pooling": False,
        "league_pooling": False,
        "historical_opponents_allowed": True,
    }
    (ART / "MODEL_FREEZE_POST_P1P2.json").write_text(json.dumps(man, indent=2) + "\n")
    return man


def main():
    freeze = refresh_freeze()
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    t0 = time.perf_counter()
    acct = run_accounting_checks(cfg, pbp_path=PBP, n=N_ACCT, seed=20261105)
    acct_sec = time.perf_counter() - t0

    t1 = time.perf_counter()
    grade_rows = grade_week_games(PBP, weeks=list(range(1, 9)), n_sims=N_GRADE, seed_base=20261105)
    grade_sec = time.perf_counter() - t1
    gdf = pd.DataFrame(grade_rows)
    gdf.to_csv(ART / "asof_grade_per_game.csv", index=False)

    status_counts = gdf["grade_status"].value_counts().to_dict()
    graded = gdf[gdf["grade_status"] == "GRADED_FULL"]
    n_games = len(gdf)
    n_graded = len(graded)

    metrics_grade = {
        "n_games_denominator": n_games,
        "n_graded_full": int(n_graded),
        "n_ungradable": int(n_games - n_graded),
        "status_counts": status_counts,
        "n_sims_per_graded_game": N_GRADE,
        "grade_runtime_sec": grade_sec,
    }
    if n_graded:
        metrics_grade.update({
            "mae_home": float(graded["abs_err_home"].mean()),
            "mae_away": float(graded["abs_err_away"].mean()),
            "mae_total_points_side_avg": float(0.5 * (graded["abs_err_home"].mean() + graded["abs_err_away"].mean())),
            "baseline_mae_home": float(graded["baseline_abs_err_home"].dropna().mean()) if graded["baseline_abs_err_home"].notna().any() else None,
            "baseline_mae_away": float(graded["baseline_abs_err_away"].dropna().mean()) if graded["baseline_abs_err_away"].notna().any() else None,
            "mean_pred_home": float(graded["pred_home_mean"].mean()),
            "mean_pred_away": float(graded["pred_away_mean"].mean()),
            "mean_actual_home": float(graded["actual_home"].mean()),
            "mean_actual_away": float(graded["actual_away"].mean()),
            "mean_pred_h1_home": float(graded["pred_h1_home_mean"].mean()),
            "mean_pred_h1_away": float(graded["pred_h1_away_mean"].mean()),
        })
        # beat baseline?
        if metrics_grade["baseline_mae_home"] is not None:
            metrics_grade["engine_vs_baseline_home"] = (
                "engine_mae_lower" if metrics_grade["mae_home"] < metrics_grade["baseline_mae_home"]
                else "baseline_mae_lower_or_tie"
            )
            metrics_grade["engine_vs_baseline_away"] = (
                "engine_mae_lower" if metrics_grade["mae_away"] < metrics_grade["baseline_mae_away"]
                else "baseline_mae_lower_or_tie"
            )
        metrics_grade["note"] = "Development set — not tuned to beat baseline; not accuracy claim"

    inv = load_involvement_plays(PBP, teams=["JAX", "BAL"], season=2026, weeks=(1, 8))
    joined = load_ftn_join(inv)
    expl = explosive_tables(inv)
    qb = qb_completion_splits(joined["joined"]) if joined.get("joined") is not None else {}

    (ART / "accounting_report.json").write_text(json.dumps(acct, indent=2) + "\n")
    (ART / "effects_explosive.json").write_text(json.dumps(expl, indent=2) + "\n")
    (ART / "effects_qb_splits.json").write_text(json.dumps(qb, indent=2) + "\n")
    (ART / "effects_ftn_join_meta.json").write_text(json.dumps(joined["meta"], indent=2) + "\n")

    metrics = {
        "freeze": freeze,
        "approved_pick": False,
        "evaluation_label": "development_w1_8_inspected_not_untouched_holdout",
        "prior_artifact_0of15": "artifacts/validation/pre_fix_b7b5796_0of15/",
        "accounting": {k: acct[k] for k in acct if k != "checks"},
        "accounting_checks_fail": [c for c in acct["checks"] if not c["ok"]],
        "accounting_runtime_sec": acct_sec,
        "grading": metrics_grade,
        "market_status": "NO_MATCHING_PREKICK_PINNACLE_QUOTES — no edge/ROI",
        "effects_summary": {
            "ftn": joined["meta"],
            "period_scoreboards": "IMPLEMENTED",
            "true_pressure": "MISSING_paid_FTN_qbp",
            "coverage_man_zone_mofo": "MISSING_not_in_nflverse_FTN_29col",
            "attribution": "FTN Data via nflverse (CC-BY-SA)",
        },
        "blockers_residual": [
            "True pressure (FTN qbp) and routes (rte) require paid FTN — not pulled",
            "Man/zone/MOFO/MOFC absent from free FTN subset (nflreadr dictionary confirms)",
            "CB/S/DT replacement effects remain UNVERIFIED notes — no coefficients",
            "Actual H1/period outcomes not fully reconstructed for MAE vs actual periods in this CSV (FG graded; H1 pred reported)",
            "sparse_rate still high; development set only",
        ],
    }
    (ART / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")

    summary = f"""# Validation/grading after P1/P2/P3 (not an approved pick)

Freeze bundle: {freeze['bundle_sha256'][:16]}… | prior 0/15 preserved under pre_fix_b7b5796_0of15/

## Accounting N={N_ACCT}
Status **{acct['overall_status']}** pass={acct['n_checks_pass']} fail={acct['n_checks_fail']}
Fails: {[c['name'] for c in acct['checks'] if not c['ok']]}
Score means: {acct['score_means']} sparse={acct['sparse_rate']}

## As-of grade (denom={n_games}, n_sims={N_GRADE}/game, runtime={grade_sec:.1f}s)
GRADED_FULL: **{n_graded}** | Ungradable: {n_games - n_graded}
Statuses: {status_counts}
"""
    if n_graded:
        summary += f"""MAE home/away: {metrics_grade.get('mae_home'):.2f} / {metrics_grade.get('mae_away'):.2f}
Baseline PPG MAE home/away: {metrics_grade.get('baseline_mae_home')} / {metrics_grade.get('baseline_mae_away')}
Engine vs baseline: {metrics_grade.get('engine_vs_baseline_home')} / {metrics_grade.get('engine_vs_baseline_away')}
"""
    summary += f"""
## Effects
FTN join {joined['meta'].get('status')} rate={joined['meta'].get('join_rate')}
True pressure/coverage MOFO: MISSING (free FTN 29-col only). Blitz strata IMPLEMENTED.
Shaan numbers: attributed not verified.

Market: no pre-kick Pin → no ROI. W1–8 = development.
"""
    (ART / "SUMMARY.md").write_text(summary)
    print(summary)


if __name__ == "__main__":
    main()
