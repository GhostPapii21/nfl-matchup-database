"""Read-only partition of an EXISTING engine's per-trial score arrays into the three branches.

This is not a simulation: it takes arrays the possession engine already wrote (snapshots/<game>/<ts>/sim_arrays.npz,
keys fg_home/fg_away/q1_home.../reg_home...) and groups trials by the branch_definition. Because the engine's play
selection does not depend on score state (see docs/audits/game_script_integrity_audit.md), every dimension produced
this way is "derived" (trial selection), never "modeled". Dimensions the arrays do not carry are "not_modeled".

Classification uses only end-of-Q3 and regulation margins (fields already in the arrays). Mid-quarter path and
overtime are not inputs.
"""
from __future__ import annotations

from typing import Optional

import numpy as np

from .allocation import classify_trials
from .schema import BRANCH_IDS, DEFAULT_BRANCH_DEFINITION, DIMENSIONS, SCHEMA_VERSION


def _dist(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    q = np.percentile(x, [10, 25, 50, 75, 90]) if len(x) else [0.0] * 5
    return {"samples": x.tolist(), "mean": float(x.mean()) if len(x) else None,
            "sd": float(x.std()) if len(x) else None,
            "quantiles": dict(zip(("p10", "p25", "p50", "p75", "p90"), map(float, q)))}


def favorite_margins(arrays: dict, *, favorite_is_home: bool, n: Optional[int] = None):
    """Favorite-perspective end-of-Q3 and regulation margins from engine score arrays."""
    A = {k: np.asarray(v, dtype=float)[:n] for k, v in arrays.items()}
    sign = 1.0 if favorite_is_home else -1.0
    m_q3 = sign * sum(A[f"q{i}_home"] - A[f"q{i}_away"] for i in (1, 2, 3))
    m_reg = sign * (A["reg_home"] - A["reg_away"])
    return m_q3, m_reg


def composition_of_competitive(labels: np.ndarray, m_q3: np.ndarray, definition: dict) -> dict:
    """Break branch B into the underdog-ahead-by-threshold sub-case and the rest. Not a fourth branch."""
    q3t = float(definition["q3_control_margin"])
    b = labels == "competitive"
    ahead = b & (m_q3 <= -q3t)
    other = b & ~ahead
    n = len(labels)
    n_b = int(b.sum())

    def slice_(mask, rule):
        k = int(mask.sum())
        return {"rule": rule, "n_trials": k, "share_of_all": k / n,
                "share_of_competitive": (k / n_b) if n_b else None}
    return {
        "underdog_ahead_end_q3_by_control_margin": slice_(
            ahead, f"end-Q3 favorite margin <= -{q3t:g} (underdog led by {q3t:g}+ entering Q4); sub-case of competitive, not a fourth branch"),
        "other_competitive": slice_(
            other, f"end-Q3 favorite margin in ({-q3t:g}, {q3t:g}) — close game or modest underdog lead"),
    }


def partition_score_arrays(arrays: dict, *, game_id: str, home: str, away: str, favorite: str,
                           favorite_source: str, definition: Optional[dict] = None, source_engine: str,
                           source_ref: Optional[str] = None, limit: Optional[int] = None,
                           pregame_spread_favorite: Optional[float] = None) -> dict:
    definition = dict(DEFAULT_BRANCH_DEFINITION if definition is None else definition)
    if favorite not in (home, away):
        raise ValueError(f"favorite {favorite!r} is not home {home!r} or away {away!r}")
    fav_is_home = favorite == home
    underdog = away if fav_is_home else home
    n = len(arrays["fg_home"]) if limit is None else min(limit, len(arrays["fg_home"]))
    A = {k: np.asarray(v)[:n] for k, v in arrays.items()}
    m_q3, m_reg = favorite_margins(A, favorite_is_home=fav_is_home, n=n)
    labels = classify_trials(m_q3, m_reg, definition)
    if len(labels) != n:
        raise RuntimeError("classifier did not label every trial")
    status = {d: {"status": "not_modeled", "reason": "not present in the engine's committed per-trial arrays",
                  "source": None} for d in DIMENSIONS}
    for d in ("score_distribution", "quarter_scoring"):
        status[d] = {"status": "derived",
                     "reason": "trials partitioned by end-of-Q3 lead held or chased in Q4; engine play selection "
                               "is not score-state aware, so in-branch behaviour is unchanged",
                     "source": source_engine}
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
            "branch_definition": definition, "branches": branches,
            "competitive_composition": composition_of_competitive(labels, m_q3, definition)}
