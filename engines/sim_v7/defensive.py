"""Research-only matchup adjustments from existing pregame board splits + Sharp/NGS.

Builds:
  1) QB-level coverage/pressure/blitz completion & attempt factors (commits ba5d34a/70d5198/08bc8c1)
  2) Player-specific coverage target allocation (coverage_alloc.py) — measured vs inferred
  3) Pressure-induced scramble profiles (scramble.py)
  4) Opponent-defense descriptors for Game Randomness reweighting

Status is always EXPERIMENTAL_UNVALIDATED after defensive integration; never inherited as validated.
"""
from __future__ import annotations

import numpy as np

from . import coverage_alloc as CA
from . import data as D
from . import scramble as SC


def mixture(a, b, w, key):
    return (1 - w) * float(a[key]) + w * float(b[key])


def ratio(a, b):
    return float(np.clip(a / b, .75, 1.25)) if b > 0 else 1.


def _qb_split_profile(side: dict) -> dict:
    q = side.get("qb") or {}
    c = side.get("coverage_profile") or {}
    old = q.get("last_season") or {}
    now = q.get("this_season") or {}
    p = {"qb_id": q.get("player_id"), "completion": 1., "yards_per_completion": 1., "attempts": 1.,
         "evidence": {}, "pressure_rate": c.get("pressure_rate")}
    # Prefer Sharp rates for the defense when available (offense faces that defense)
    offense = side.get("offense")
    # coverage_profile on the board side is the OPPOSING defense's look vs this offense
    man_rate = c.get("man_rate")
    cts = c.get("coverage_this_season") or {}
    mofo = cts.get("two_high_rate")
    mofc = cts.get("one_high_rate")
    for label, lo, hi, weight in (
        ("coverage", old.get("vs_zone"), old.get("vs_man"), man_rate),
        ("pressure", old.get("clean"), old.get("pressured"), c.get("pressure_rate")),
        ("blitz", now.get("no_blitz"), now.get("vs_blitz"), (c.get("blitz_this_season") or {}).get("blitz_rate")),
    ):
        if not lo or not hi or weight is None or not 0 <= weight <= 1:
            continue
        if min(lo.get("attempts", 0), hi.get("attempts", 0)) < 30:
            continue
        baseline = hi["dropbacks"] / (lo["dropbacks"] + hi["dropbacks"])
        cr = ratio(mixture(lo, hi, weight, "completion_pct"), mixture(lo, hi, baseline, "completion_pct"))
        yp = ratio(mixture(lo, hi, weight, "yards_per_attempt"), mixture(lo, hi, baseline, "yards_per_attempt"))
        ar = ratio(1 - mixture(lo, hi, weight, "sack_rate"), 1 - mixture(lo, hi, baseline, "sack_rate"))
        p["evidence"][label] = {
            "expected_rate": weight, "historical_rate": baseline,
            "completion_factor": cr, "yards_per_attempt_factor": yp, "attempt_factor": ar,
            "samples": [lo["attempts"], hi["attempts"]], "kind": "measured_split_x_board_rate",
        }
    # MOF shell tilt on yards (measured Sharp/board rates × QB zone/man already handled)
    if mofo is not None and "coverage" in p["evidence"]:
        # two-high slightly suppresses deep YPA; mild inferred tilt
        mof_tilt = float(np.clip(1.0 - 0.06 * (float(mofo) - 0.45), 0.90, 1.08))
        p["evidence"]["mof"] = {
            "two_high_rate": mofo, "one_high_rate": mofc, "yards_tilt": mof_tilt,
            "kind": "inferred", "basis": "board/Sharp two_high_rate",
        }
        p["yards_per_completion"] *= mof_tilt
    # Pressure preferred over blitz when both exist
    for label in ("coverage", "pressure" if "pressure" in p["evidence"] else "blitz"):
        e = p["evidence"].get(label)
        if e:
            p["completion"] *= e["completion_factor"]
            p["yards_per_completion"] *= e["yards_per_attempt_factor"] / e["completion_factor"]
            p["attempts"] *= e["attempt_factor"]
    p["status"] = "EXPERIMENTAL_UNVALIDATED" if p["evidence"] else "MISSING"
    p["offense"] = offense
    return p


def _defense_strength(side: dict) -> dict:
    """Opponent defense descriptors for GR reweighting — measured board ranks/allowances."""
    da = side.get("defense_allowed") or side.get("defense") or {}
    rank = side.get("defense_rank") or {}
    cp = side.get("coverage_profile") or {}
    return {
        "kind": "measured",
        "pressure_rate": cp.get("pressure_rate"),
        "man_rate": cp.get("man_rate"),
        "pass_yards_allowed_rank": rank.get("pass") or rank.get("passing") or da.get("pass_rank"),
        "rush_yards_allowed_rank": rank.get("rush") or rank.get("rushing") or da.get("rush_rank"),
        "points_allowed_rank": rank.get("points") or da.get("points_rank"),
        "raw": {k: da.get(k) for k in list(da)[:12]} if isinstance(da, dict) else {},
    }


def profiles(board: dict, cutoff: str = "2026-11-24") -> dict:
    """Full defensive integration profiles keyed by offense team code (nflverse)."""
    out = {}
    alloc = CA.profiles_from_board(board, cutoff=cutoff)
    for s in board.get("sides", {}).values():
        offense = s.get("offense")
        if not offense:
            continue
        team = D.NV.get(offense, offense)
        p = _qb_split_profile(s)
        # Sharp overlay for the defense this offense faces
        home = D.NV.get((board.get("game") or {}).get("home"), (board.get("game") or {}).get("home"))
        away = D.NV.get((board.get("game") or {}).get("away"), (board.get("game") or {}).get("away"))
        defense = away if team == home else home if team == away else None
        sharp = CA.sharp_for(defense) if defense else {"status": "MISSING"}
        p["sharp_defense"] = sharp
        p["coverage_allocation"] = alloc.get(team) or alloc.get(offense) or {"status": "MISSING"}
        p["scramble"] = SC.qb_scramble_profile(
            p.get("qb_id"), cutoff, board_pressure_rate=p.get("pressure_rate")
        )
        p["opponent_defense"] = _defense_strength(s)
        p["calibration_status"] = "EXPERIMENTAL_UNVALIDATED_DEFENSE_CHANGED"
        p["integration"] = {
            "qb_split_factors": p["status"],
            "coverage_allocation": (p["coverage_allocation"] or {}).get("status"),
            "scramble": (p["scramble"] or {}).get("status"),
            "sharp": sharp.get("status"),
        }
        out[team] = p
    return out
