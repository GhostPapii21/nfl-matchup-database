"""Read-only partition of an EXISTING engine's per-trial score arrays into the three branches.

This is not a simulation: it takes arrays the possession engine already wrote (snapshots/<game>/<ts>/sim_arrays.npz,
keys fg_home/fg_away/q1_home.../reg_home...) and groups trials by the branch_definition. Because the engine's play
selection does not depend on score state (see docs/audits/game_script_integrity_audit.md), every dimension produced
this way is "derived" (trial selection), never "modeled". Dimensions the arrays do not carry are "not_modeled".
"""
from __future__ import annotations

from typing import Optional

import numpy as np

from .schema import BRANCH_IDS, DIMENSIONS, SCHEMA_VERSION
from .allocation import classify_margin


def _dist(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    q = np.percentile(x, [10, 25, 50, 75, 90]) if len(x) else [0.0] * 5
    return {"samples": x.tolist(), "mean": float(x.mean()) if len(x) else None,
            "sd": float(x.std()) if len(x) else None,
            "quantiles": dict(zip(("p10", "p25", "p50", "p75", "p90"), map(float, q)))}


def partition_score_arrays(arrays: dict, *, game_id: str, home: str, away: str, favorite: str,
                           favorite_source: str, definition: dict, source_engine: str,
                           source_ref: Optional[str] = None, limit: Optional[int] = None,
                           pregame_spread_favorite: Optional[float] = None) -> dict:
    fav_is_home = favorite == home
    underdog = away if fav_is_home else home
    n = len(arrays["fg_home"]) if limit is None else min(limit, len(arrays["fg_home"]))
    A = {k: np.asarray(v)[:n] for k, v in arrays.items()}
    sign = 1 if fav_is_home else -1
    var = definition["classifier_variable"]
    if var == "final_margin_favorite":
        m = sign * (A["fg_home"].astype(float) - A["fg_away"])
    elif var == "regulation_margin_favorite":
        m = sign * (A["reg_home"].astype(float) - A["reg_away"])
    else:
        m = sign * sum(A[f"q{i}_home"].astype(float) - A[f"q{i}_away"] for i in (1, 2, 3))
    labels = np.array([classify_margin(x, definition) for x in m])
    status = {d: {"status": "not_modeled", "reason": "not present in the engine's committed per-trial arrays",
                  "source": None} for d in DIMENSIONS}
    for d in ("score_distribution", "quarter_scoring"):
        status[d] = {"status": "derived", "reason": "trials partitioned by final margin; engine play selection is "
                     "not score-state aware, so in-branch behaviour is unchanged", "source": source_engine}
    nulls = {"plays": None, "possessions": None, "pass_attempts": None, "rush_attempts": None, "sec_per_play": None,
             "red_zone_trips": None, "touchdowns": None, "pressure_rate_faced": None, "coverage_mix_faced": None,
             "starters_rested_prob": None}
    branches = {}
    for b in BRANCH_IDS:
        idx = labels == b
        teams = {}
        for team, side in ((home, "home"), (away, "away")):
            qp = {f"q{i}": _dist(A[f"q{i}_{side}"][idx]) for i in (1, 2, 3, 4)}
            qp["ot"] = _dist(A[f"ot_{side}"][idx]) if f"ot_{side}" in A and idx.any() else None
            teams[team] = {"points": _dist(A[f"fg_{side}"][idx]), "quarter_points": qp, **nulls}
        if not idx.any():  # an empty branch cannot carry samples; mark everything not_modeled
            teams = {t: {"points": None, "quarter_points": None, **nulls} for t in (home, away)}
        st = {k: dict(v) for k, v in status.items()} if idx.any() else \
            {d: {"status": "not_modeled", "reason": "branch has zero trials", "source": None} for d in DIMENSIONS}
        branches[b] = {"branch_id": b, "probability": float(idx.sum()) / n, "n_trials": int(idx.sum()),
                       "dimension_status": st, "teams": teams, "players": []}
    return {"schema_version": SCHEMA_VERSION,
            "game": {"game_id": game_id, "home": home, "away": away, "favorite": favorite, "underdog": underdog,
                     "favorite_source": favorite_source, "pregame_spread_favorite": pregame_spread_favorite,
                     "asof_utc": None},
            "provenance": {"source_engine": source_engine, "source_ref": source_ref, "config_id": None, "seed": None,
                           "n_trials_total": int(n), "probability_basis": "trial_partition", "generated_at_utc": None,
                           "research_only": True, "synthetic": False},
            "branch_definition": dict(definition), "branches": branches}
