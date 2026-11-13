"""NFL-75 Phase 2b (opt-in research, default off): team interception rate pooled toward a league rate.

Why. The engine resamples the offense's own historical rows (2026 weeks before the game). A team whose pool has no
interception row can never throw one in the sim: P(QB throws >= 1 INT) = 0 for every simulated game. On the
Phase 2 W4-9 backtest that is 10 of 178 QB-games (Stroud x3, Goff x4, G.Smith x3); the real rate is ~2-3% per
attempt for every team. Small pools also over-state INTs (a team with 3 INTs in 60 attempts plays at 5%).

What. For the offense's row pool (catalog.by_team[team], the same rows the engine samples from), count pass
attempts n (play_type == "pass", sack != 1) and interceptions k. The pooled target is the empirical-Bayes rate
    p* = (k + m * p_league) / (n + m)
with p_league and m supplied by the caller (fitted walk-forward on data before the eval week; see
calibration/opportunity_intcap.py). Every sampled pass attempt then gets ONE uniform draw from this module's own RNG
stream (SeedSequence([seed, SALT])):
  * p* > p_team: a non-INT attempt becomes an interception with q_up = (p* - p_team) / (1 - p_team): the same row
    with interception=1, complete_pass=0, touchdown=0, fumble_lost=0, yards_gained=0 (nflverse INT rows carry
    yards 0; the engine's turnover spot and league-rate defensive return then apply as for any INT row), the
    defender name blanked (no defender is credited);
  * p* < p_team: an INT attempt becomes an incompletion with q_down = (p_team - p*) / p_team (interception=0,
    complete_pass=0, yards_gained=0).
In expectation the team's per-attempt INT rate becomes p* exactly (p_team*(1-q_down) + (1-p_team)*q_up = p*), for
the team pool; cell / down pools inherit the same per-attempt adjustment (their own INT mix is otherwise kept).
Sacks, runs and non-pass rows are never touched and draw nothing.

Default None = off: no object, no draws, bit-identical output (golden-digest test). Research only; refused by the
lock / 100k path (simulate.simulate_games caps n at RESEARCH_MAX_N and refuses it from a config)."""
from __future__ import annotations

import math
from typing import Optional

import numpy as np
import pandas as pd

SCHEMA = "nfl75-int-pool/1"
SALT = 75003


def _num(df: pd.DataFrame, c: str) -> pd.Series:
    if c not in df.columns:
        return pd.Series(0, index=df.index)
    return pd.to_numeric(df[c], errors="coerce").fillna(0)


def team_counts(pool: Optional[pd.DataFrame]) -> tuple[int, int]:
    """(pass attempts, interceptions) in a row pool (sacks excluded)."""
    if pool is None or not len(pool) or "play_type" not in pool.columns:
        return 0, 0
    att = (pool["play_type"] == "pass") & (_num(pool, "sack") != 1)
    return int(att.sum()), int((att & (_num(pool, "interception") == 1)).sum())


def validate(spec: dict) -> dict:
    if not isinstance(spec, dict) or spec.get("schema") != SCHEMA:
        raise ValueError(f"int_pool schema must be {SCHEMA}")
    p, m = float(spec["league_rate"]), float(spec["m"])
    if not (0.0 < p < 0.5) or not (m >= 0.0) or math.isnan(m):
        raise ValueError(f"int_pool needs 0 < league_rate < 0.5 and m >= 0 (got {p}, {m})")
    return {"schema": SCHEMA, "league_rate": p, "m": m, **{k: v for k, v in spec.items()
                                                           if k not in ("schema", "league_rate", "m")}}


class IntPool:
    def __init__(self, spec: dict, by_team: dict, rng: np.random.Generator):
        self.spec = validate(spec)
        self.rng = rng
        p, m = self.spec["league_rate"], self.spec["m"]
        self.table = {}
        for team, pool in (by_team or {}).items():
            n, k = team_counts(pool)
            pt = k / n if n else p
            ps = (k + m * p) / (n + m) if (n + m) > 0 else p
            q_up = max(0.0, ps - pt) / (1.0 - pt) if pt < 1 else 0.0
            q_down = max(0.0, pt - ps) / pt if pt > 0 else 0.0
            self.table[team] = {"att": n, "int": k, "p_team": pt, "p_star": ps, "q_up": q_up, "q_down": q_down}
        self.counts = {"attempts_seen": 0, "to_int": 0, "to_incomplete": 0}

    def apply(self, st, row):
        if str(row.get("play_type")) != "pass":
            return row
        sk = row.get("sack")
        if sk is not None and not pd.isna(sk) and int(sk) == 1:
            return row
        t = self.table.get(st.possession)
        if t is None:
            return row
        self.counts["attempts_seen"] += 1
        u = self.rng.random()
        iv = row.get("interception")
        is_int = iv is not None and not pd.isna(iv) and int(iv) == 1
        if is_int and u < t["q_down"]:
            r = row.copy()
            for c, v in (("interception", 0), ("complete_pass", 0), ("yards_gained", 0.0), ("touchdown", 0),
                         ("fumble_lost", 0)):
                if c in r.index:
                    r[c] = v
            if "interception_player_name" in r.index:
                r["interception_player_name"] = None
            self.counts["to_incomplete"] += 1
            return r
        if (not is_int) and u < t["q_up"]:
            r = row.copy()
            for c, v in (("interception", 1), ("complete_pass", 0), ("yards_gained", 0.0), ("touchdown", 0),
                         ("fumble_lost", 0)):
                r[c] = v
            for c in ("interception_player_name", "pass_defense_1_player_name", "fumbled_1_player_name"):
                if c in r.index:
                    r[c] = None
            self.counts["to_int"] += 1
            return r
        return row
