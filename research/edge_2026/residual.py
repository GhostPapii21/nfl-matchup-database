"""Book-offset residual model for player props, with explicit data gates."""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.special import expit, logit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
NV = ROOT / "data" / "historical" / "nflverse"
PARTICIPATION_ROOT = ROOT / "data" / "gamebooks" / "2026" / "wk09"
GRADE_CSV = ROOT / "data" / "odds_history" / "alt_ladders_wk8_9" / "backtest" / "graded_rungs.csv"
FEATURES = [
    "teammate_out_share",
    "tprr_l4_minus_season",
    "route_share_change",
    "explosive_rate_l6",
    "our_mean_minus_line_over_sd",
]
COEF_NAMES = {
    "teammate_out_share": "b1_teammate_out_share",
    "tprr_l4_minus_season": "b2_tprr_l4_minus_season",
    "route_share_change": "b3_route_share_change",
    "explosive_rate_l6": "b4_explosive_rate_l6",
    "our_mean_minus_line_over_sd": "b5_our_mean_minus_line_over_sd",
}
BOOT_REPS = 5000
BOOT_SEED = 20261119


def _cluster_roi_ci(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {"ci95": [None, None], "clusters": 0}
    group_cols = [c for c in ("game_id", "player", "market") if c in frame.columns]
    clusters = frame.groupby(group_cols, dropna=False).profit.apply(list).tolist()
    if len(clusters) < 2:
        return {"ci95": [None, None], "clusters": len(clusters)}
    rng = np.random.default_rng(BOOT_SEED)
    idx = rng.integers(0, len(clusters), size=(BOOT_REPS, len(clusters)))
    boot = np.empty(BOOT_REPS, dtype=float)
    arrays = [np.asarray(v, dtype=float) for v in clusters]
    for i, sample in enumerate(idx):
        selected = [arrays[j] for j in sample]
        boot[i] = np.concatenate(selected).mean()
    low, high = np.quantile(boot, [0.025, 0.975])
    return {"ci95": [float(low), float(high)], "clusters": len(clusters), "method": "player-game-market cluster bootstrap", "reps": BOOT_REPS, "seed": BOOT_SEED}


def fit_offset_glm(train: pd.DataFrame, test: pd.DataFrame) -> dict[str, Any]:
    """Fit the requested Binomial GLM with fair-book logit as an offset."""
    required = set(FEATURES + ["hit", "p_fair_book", "break_even"])
    if not required.issubset(train.columns) or not required.issubset(test.columns):
        raise ValueError(f"missing required model columns: {sorted(required - set(train.columns) | required - set(test.columns))}")
    train = train.dropna(subset=FEATURES + ["hit", "p_fair_book"]).copy()
    test = test.dropna(subset=FEATURES + ["hit", "p_fair_book"]).copy()
    if len(train) < 100 or len(test) < 30:
        raise ValueError("insufficient chronological train/test sample")
    x_train = train[FEATURES].astype(float)
    x_test = test[FEATURES].astype(float)
    p_train = train["p_fair_book"].astype(float).clip(1e-6, 1 - 1e-6)
    p_test = test["p_fair_book"].astype(float).clip(1e-6, 1 - 1e-6)
    fit = sm.GLM(
        train["hit"].astype(float), x_train,
        family=sm.families.Binomial(), offset=logit(p_train),
    ).fit()
    model_p = expit(logit(p_test) + x_test.to_numpy() @ fit.params.to_numpy())
    book_p = p_test.to_numpy()
    y = test["hit"].to_numpy(dtype=float)
    be = test["break_even"].to_numpy(dtype=float)
    bet = model_p - be >= 0.03
    profit = np.where(y > 0.5, 1.0 / np.maximum(be, 1e-6) - 1.0, -1.0)
    selected = test.loc[bet].copy()
    selected["profit"] = profit[bet]
    roi_ci = _cluster_roi_ci(selected)
    return {
        "status": "fit",
        "coefficients": {
            COEF_NAMES[name]: {
                "estimate": float(fit.params[name]), "se": float(fit.bse[name]),
                "p_value": float(fit.pvalues[name]), "significant_05": bool(fit.pvalues[name] < 0.05),
            }
            for name in FEATURES
        },
        "n_train": int(len(train)), "n_test": int(len(test)),
        "test": {
            "book_brier": float(np.mean((book_p - y) ** 2)),
            "model_brier": float(np.mean((model_p - y) ** 2)),
            "brier_difference_model_minus_book": float(np.mean((model_p - y) ** 2) - np.mean((book_p - y) ** 2)),
            "n_bets": int(bet.sum()), "roi": float(np.mean(profit[bet])) if bet.any() else None,
            "roi_ci95": roi_ci,
        },
    }


def _available_participation_columns() -> list[str]:
    files = sorted(PARTICIPATION_ROOT.glob("**/parsed/participation.csv"))
    if not files:
        return []
    with files[0].open(newline="") as handle:
        return next(csv.reader(handle), [])


def _data_audit(clv: dict[str, Any]) -> dict[str, Any]:
    participation_columns = _available_participation_columns()
    has_route_counts = any("route" in column.lower() for column in participation_columns)
    try:
        pbp = pd.read_parquet(NV / "pbp_2026_w1_9_pulled_20261112T1116ET.parquet", columns=["week"])
        pbp_weeks = sorted(int(w) for w in pbp["week"].dropna().unique())
    except (OSError, ImportError, ValueError):
        pbp_weeks = []
    try:
        weekly = pd.read_parquet(NV / "stats_player_week_2026.parquet", columns=["week"])
        weekly_weeks = sorted(int(w) for w in weekly["week"].dropna().unique())
    except (OSError, ImportError, ValueError):
        weekly_weeks = []
    try:
        injury = pd.read_parquet(NV / "injuries_2026_pulled_20261113T0526Z.parquet", columns=["week", "report_status"])
        injury_weeks = sorted(int(w) for w in injury["week"].dropna().unique())
    except (OSError, ImportError, ValueError):
        injury_weeks = []
    closed_rows = sum(row.get("status") == "closed" and row.get("clv") is not None for row in clv.get("rows", []))
    alt_rows = 0
    if GRADE_CSV.exists():
        with GRADE_CSV.open(newline="") as handle:
            alt_rows = sum(1 for _ in csv.DictReader(handle))
    return {
        "closed_direct_line_rows": int(closed_rows),
        "archived_alt_rows_with_outcomes": int(alt_rows),
        "archived_alt_feature_coverage": "alt prices/outcomes are available, but they are one-sided ladders without the required route and pregame team-absence features",
        "pbp_2026_weeks_available": pbp_weeks,
        "weekly_stats_2026_weeks_available": weekly_weeks,
        "injury_report_2026_weeks_available": injury_weeks,
        "participation_columns": participation_columns,
        "route_run_columns_available": has_route_counts,
        "missing_required_inputs": [
            "A multi-season historical set of two-way player-prop prices matched to settled outcomes is not present in direct_lines history.",
            "The available participation.csv files list game participation substitutions and do not include route runs; tprr and route_share_change cannot be computed without inventing routes.",
            "The 2026 direct-line history is a small set of recent snapshots, and upcoming games have no settled outcomes yet.",
        ],
        "feature_status": {
            "teammate_out_share": "injury reports exist for some seasons, but no eligible closed prop sample is available to fit and validate this feature",
            "tprr_l4_minus_season": "unavailable; route-run denominators are absent",
            "route_share_change": "unavailable; route counts and team dropback route denominators are absent",
            "explosive_rate_l6": "derivable from play-by-play, but not sufficient to fit the model by itself",
            "our_mean_minus_line_over_sd": "derivable from player history and direct lines, but not sufficient to fit the model by itself",
        },
    }


def main() -> dict[str, Any]:
    clv_path = OUT / "clv.json"
    clv = json.loads(clv_path.read_text()) if clv_path.exists() else {"rows": [], "summary": {"n": 0}}
    audit = _data_audit(clv)
    coefficients = {
        COEF_NAMES[name]: {"estimate": None, "se": None, "p_value": None, "significant_05": None}
        for name in FEATURES
    }
    result = {
        "schema_version": 1,
        "status": "not_fit",
        "fit_seasons": [],
        "test": {
            "status": "not_estimable",
            "n": 0,
            "book_brier": None,
            "model_brier": None,
            "roi_when_model_edge_ge_0_03": None,
            "roi_ci95": [None, None],
            "significant_coefficients": [],
        },
        "coefficients": coefficients,
        "data_audit": audit,
        "reason": "The available files do not contain an eligible multi-season, two-way book-prop outcome panel or route-run features. No coefficients or ROI are estimated from incomplete inputs.",
        "model_spec": {
            "family": "statsmodels GLM Binomial with offset=logit(p_fair_book)",
            "features": FEATURES,
            "test_split": "chronological; fit before test season",
            "bet_rule": "model probability minus break_even >= 0.03",
            "roi_ci": "bootstrap over game-player-market clusters",
        },
    }
    model_payload = {
        "coef": {key: None for key in coefficients},
        "fit_seasons": [],
        "test": result["test"],
        "status": "not_fit",
        "reason": result["reason"],
    }
    (OUT / "residual.json").write_text(json.dumps(result, indent=1, allow_nan=False))
    (OUT / "residual_model.json").write_text(json.dumps(model_payload, indent=1, allow_nan=False))
    print(json.dumps({"status": result["status"], "test": result["test"], "data_audit": audit}, indent=1))
    return result


if __name__ == "__main__":
    main()
