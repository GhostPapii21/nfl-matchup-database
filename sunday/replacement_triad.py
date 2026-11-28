"""A versioned stand-in for the nine-cell run. It is not sim_v6.

The recovered sim_v6 source cannot express three scripts. This module does not
borrow that name. It runs one empirical bootstrap of nflverse final scores
from weeks before the target week, 100000 draws, and it records the period and
possession engines as not executed in this command. Historical home margin is
not labeled favorite_controls: games.csv has no closing spread, so the script
bins stay blocked.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import numpy as np

TRIALS = 100_000
IDENTITY = "sunday-replacement-triad/1"
GAMES = "data/historical/nflverse/games.csv"
LOCK_BENCHMARK = {
    "path": "snapshots/2026_12_DEN_PIT/20261127T111648Z/LOCK.json",
    "engine": "core.possession_engine_v0",
    "n": 100_000,
    "runtime_sec": 819.2,
    "note": "Committed lock. This command did not repeat that run and did not multiply it by nine.",
}


def _prior_margins(repo: Path, season: int, week: int) -> list[float]:
    path = repo / GAMES
    margins = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("season") != str(season) or row.get("game_type") not in {None, "", "REG"}:
                continue
            try:
                row_week = int(row["week"])
                home = float(row["home_score"]) if row.get("home_score") not in {None, ""} else None
                away = float(row["away_score"]) if row.get("away_score") not in {None, ""} else None
            except (TypeError, ValueError):
                continue
            if row_week >= week or home is None or away is None:
                continue
            margins.append(home - away)
    return margins


def empirical_cell(margins: list[float], *, seed: int, n: int = TRIALS) -> dict:
    if len(margins) < 2:
        return {
            "identity": "nflverse_games_bootstrap",
            "status": "BLOCKED",
            "trials_executed": 0,
            "trials_required": n,
            "sample_size": len(margins),
            "reason": "fewer than two completed prior games; no draw was invented",
        }
    rng = np.random.default_rng(seed)
    draws = rng.choice(np.asarray(margins, dtype=float), size=n, replace=True)
    digest = hashlib.sha256(draws.tobytes()).hexdigest()
    return {
        "identity": "nflverse_games_bootstrap",
        "mechanism": "resample realized home margin from nflverse games.csv",
        "status": "EXECUTED",
        "trials_executed": int(n),
        "trials_required": n,
        "sample_size": len(margins),
        "seed": seed,
        "mean": float(draws.mean()),
        "p50": float(np.percentile(draws, 50)),
        "draws_sha256": digest,
        "evidence_tier": "inferred",
        "scripts_assigned": False,
        "reason": "Home margin is not favorite margin. games.csv has no closing spread, so script bins were not assigned.",
        "not_sim_v6": True,
        "projection_ready": False,
    }


def receipt(repo: Path, *, season: int, week: int, seed: int = 20261129) -> dict:
    margins = _prior_margins(repo, season, week) if (repo / GAMES).is_file() else []
    empirical = empirical_cell(margins, seed=seed)
    return {
        "schema": IDENTITY,
        "projection_ready": False,
        "not_sim_v6": True,
        "methods": [
            {
                "identity": "core.period_engine_v0",
                "mechanism": "quarter bootstrap, independent of the possession play engine",
                "status": "NOT_EXECUTED_THIS_RUN",
                "trials_executed": 0,
                "trials_required_per_script": TRIALS,
                "scripts": ["favorite_controls", "competitive", "underdog_chases"],
                "reason": "A 100k period cell was not started. The 24/400 Sunday smoke is not this cell.",
            },
            {
                "identity": "core.possession_engine_v0",
                "mechanism": "play-level simulation",
                "status": "NOT_EXECUTED_THIS_RUN",
                "trials_executed": 0,
                "trials_required_per_script": TRIALS,
                "committed_benchmark": LOCK_BENCHMARK,
                "reason": "The committed DEN@PIT lock records one 100k possession run at 819.2 seconds. Nine such cells were not started.",
            },
            empirical,
        ],
        "walk_forward": walk_forward(repo),
    }


def walk_forward(repo: Path) -> dict:
    """Score the committed W4-7 backtest file. Do not refit it."""
    path = repo / "calibration" / "simv56" / "engines" / "sim_v6_backtest.csv"
    if not path.is_file():
        return {"status": "UNAVAILABLE", "evidence_tier": "unavailable"}
    by_market: dict[str, list] = {}
    weeks = set()
    rows = 0
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            rows += 1
            week = int(row["week"])
            weeks.add(week)
            actual = float(row["actual"])
            market = row["market"]
            slot = by_market.setdefault(market, [])
            slot.append({
                "week": week,
                "mc": abs(float(row["pred_mc"]) - actual),
                "bias": abs(float(row["pred_bias"]) - actual),
                "gr": abs(float(row["pred_gr"]) - actual),
            })
    markets = {}
    for market, items in sorted(by_market.items()):
        markets[market] = {
            "rows": len(items),
            "median_abs_error": {
                name: float(np.median([item[name] for item in items]))
                for name in ("mc", "bias", "gr")
            },
            "by_week": {
                str(week): {
                    "rows": sum(1 for item in items if item["week"] == week),
                    "median_abs_error_mc": float(np.median([item["mc"] for item in items if item["week"] == week])),
                }
                for week in sorted({item["week"] for item in items})
            },
        }
    return {
        "status": "SCORED_COMMITTED_FILE",
        "path": "calibration/simv56/engines/sim_v6_backtest.csv",
        "rows": rows,
        "weeks": sorted(weeks),
        "refit": False,
        "holdout_scorecard": None,
        "later_weeks_than_file": "not in this file" if max(weeks) <= 7 else "present",
        "markets": markets,
        "identity": "committed backtest columns pred_mc, pred_bias, pred_gr; not relabeled as the Sunday script triad",
        "projection_ready": False,
    }
