"""Same-game slip (SGP) probability from the simulation's joint per-trial outcomes. Research only, not validated.

Rico's Nov 12 list, item 8: stop multiplying legs as if independent. A slip's probability is the share of simulated
trials in which EVERY leg hits (empirical joint hit rate). The independent product of the per-leg marginals is reported
next to it, only for comparison, together with the lift (joint / independent).

Inputs are the outputs of core/possession_engine_v0/simulate.simulate_games:
  * sim["arrays"]["fg_home"], ["fg_away"]: final points per trial (game legs);
  * sim["player_samples"]: one dict per trial, key "kind|TEAM|player" -> yards (player legs). A player absent from a
    trial's dict recorded 0 of that stat in that trial. A player absent from EVERY trial is an error, never 0.
No prices are read or produced here. A missing quote is not an opportunity; this module only gives probabilities.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

GAME_KEYS = ("home_pts", "away_pts", "total", "home_margin")
PLAYER_KINDS = ("pass_yards", "rush_yards", "rec_yards")
OPS = {">=": np.greater_equal, ">": np.greater, "<=": np.less_equal, "<": np.less}


@dataclass(frozen=True)
class Leg:
    """kind: "game" (key in GAME_KEYS) or a player stat kind (key "TEAM|player"). op in OPS. line: threshold.
    Example: Leg("rec_yards", "NYG|M.Nabers", ">=", 40) ; Leg("game", "total", "<", 54.5)."""
    kind: str
    key: str
    op: str
    line: float

    def __post_init__(self):
        if self.op not in OPS:
            raise ValueError(f"unknown op {self.op!r}")
        if self.kind == "game":
            if self.key not in GAME_KEYS:
                raise ValueError(f"unknown game key {self.key!r}")
        elif self.kind not in PLAYER_KINDS:
            raise ValueError(f"unknown leg kind {self.kind!r}")
        elif self.key.count("|") != 1:
            raise ValueError(f"player key must be 'TEAM|player', got {self.key!r}")

    @property
    def label(self) -> str:
        return f"{self.kind}:{self.key} {self.op} {self.line:g}"


def game_values(arrays: dict, key: str) -> np.ndarray:
    h = np.asarray(arrays["fg_home"], dtype=float)
    a = np.asarray(arrays["fg_away"], dtype=float)
    return {"home_pts": h, "away_pts": a, "total": h + a, "home_margin": h - a}[key]


def player_values(player_samples: Sequence[dict], kind: str, key: str) -> np.ndarray:
    full = f"{kind}|{key}"
    if not any(full in t for t in player_samples):
        raise KeyError(f"{full} never appears in the simulation; refusing to treat it as 0")
    return np.array([float(t.get(full, 0.0)) for t in player_samples])


def leg_values(sim: dict, leg: Leg) -> np.ndarray:
    if leg.kind == "game":
        return game_values(sim["arrays"], leg.key)
    return player_values(sim["player_samples"], leg.kind, leg.key)


def leg_hits(sim: dict, legs: Iterable[Leg]) -> np.ndarray:
    """Boolean matrix, shape (n_trials, n_legs): leg j hit in trial i."""
    legs = list(legs)
    if not legs:
        raise ValueError("a slip needs at least one leg")
    cols = [OPS[l.op](leg_values(sim, l), l.line) for l in legs]
    n = {len(c) for c in cols}
    if len(n) != 1:
        raise ValueError(f"legs disagree on trial count: {sorted(n)}")
    return np.column_stack(cols)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def joint_from_hits(hits: np.ndarray) -> dict:
    hits = np.asarray(hits, dtype=bool)
    if hits.ndim != 2 or hits.shape[0] == 0:
        raise ValueError("hits must be a non-empty (n_trials, n_legs) matrix")
    n = hits.shape[0]
    marg = hits.mean(axis=0)
    k = int(hits.all(axis=1).sum())
    pj = k / n
    pi = float(np.prod(marg))
    return {
        "n_trials": n,
        "joint_hits": k,
        "p_joint": pj,                       # empirical joint hit rate across trials: the slip probability
        "p_joint_wilson95": wilson(k, n),
        "p_independent": pi,                 # product of marginals: comparison only, NOT the slip probability
        "lift_joint_over_independent": (pj / pi) if pi > 0 else None,
        "marginals": [float(x) for x in marg],
        "method": "empirical_joint_hit_rate_across_sim_trials",
    }


def slip_probability(sim: dict, legs: Sequence[Leg]) -> dict:
    """Slip probability from the sim's joint outcomes, with the independent product alongside for comparison."""
    out = joint_from_hits(leg_hits(sim, legs))
    out["legs"] = [l.label for l in legs]
    return out


def actual_hits(actual: dict, legs: Sequence[Leg]) -> list[bool] | None:
    """Grade legs against a realized game. actual = {"home_pts", "away_pts", "players": {"kind|TEAM|player": yds}}.
    Returns None (void) if a player leg's player did not record a credited play in the game (book void rule proxy)."""
    res = []
    for l in legs:
        if l.kind == "game":
            v = game_values({"fg_home": [actual["home_pts"]], "fg_away": [actual["away_pts"]]}, l.key)[0]
        else:
            full = f"{l.kind}|{l.key}"
            if full not in actual["players"] and not actual.get("played", {}).get(l.key.split("|", 1)[1], False):
                return None
            v = float(actual["players"].get(full, 0.0))
        res.append(bool(OPS[l.op](v, l.line)))
    return res
