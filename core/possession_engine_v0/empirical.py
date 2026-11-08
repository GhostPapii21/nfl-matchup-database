"""Empirical state → play lookup with explicit sparse statuses (no silent pool)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd


def dist_bucket(ydstogo: float) -> str:
    y = float(ydstogo) if ydstogo == ydstogo else 10.0
    if y <= 3:
        return "short"
    if y <= 7:
        return "med"
    if y <= 10:
        return "long"
    return "xlong"


def yl_bucket(yardline_100: float) -> str:
    y = float(yardline_100) if yardline_100 == yardline_100 else 75.0
    if y <= 20:
        return "RZ"
    if y <= 50:
        return "opp50to20"
    if y <= 80:
        return "own20to50"
    return "backed"


@dataclass
class StateKey:
    posteam: str
    down: int
    dist_bucket: str
    yl_bucket: str


@dataclass
class Evidence:
    status: str  # OK | SPARSE_STATE | EMPTY_STATE
    n_evidence: int
    plays: Optional[pd.DataFrame]
    pooling_applied: bool = False
    pool_proposal: Optional[str] = None
    key: Optional[StateKey] = None


def _snap_plays(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"])].copy()


def lookup_plays(
    df: pd.DataFrame,
    key: StateKey,
    *,
    min_n: int = 5,
    allow_pool: bool = False,
    proposed_pool_teams: Optional[list[str]] = None,
) -> Evidence:
    if df is None:
        return Evidence("EMPTY_STATE", 0, None, False, "PBP_MISSING_NOT_ZERO", key)
    snaps = _snap_plays(df)
    snaps = snaps[snaps["posteam"] == key.posteam]
    snaps = snaps[snaps["down"] == key.down]
    if snaps.empty:
        return Evidence("EMPTY_STATE", 0, None, False, "PROPOSED_coarser_down_or_team_pool_NOT_APPLIED", key)
    # annotate buckets
    d = snaps.copy()
    d["_db"] = d["ydstogo"].map(dist_bucket)
    d["_yl"] = d["yardline_100"].map(yl_bucket)
    cell = d[(d["_db"] == key.dist_bucket) & (d["_yl"] == key.yl_bucket)]
    n = int(len(cell))
    if n >= min_n:
        return Evidence("OK", n, cell.drop(columns=["_db", "_yl"]), False, None, key)
    # sparse — never silent pool
    proposal = (
        f"PROPOSED_coarser_bins_or_same_team_down_pool n={n}<{min_n}; "
        f"allow_pool={allow_pool} proposed_teams={proposed_pool_teams}"
    )
    if allow_pool and proposed_pool_teams:
        # still require explicit allow_pool True from config — vertical slice documents this path
        pooled = d  # same team all dist/yl for this down — still team-only
        if len(pooled) >= min_n:
            return Evidence(
                "OK_POOLED_EXPLICIT",
                int(len(pooled)),
                pooled.drop(columns=["_db", "_yl"]),
                True,
                proposal,
                key,
            )
    return Evidence("SPARSE_STATE", n, cell.drop(columns=["_db", "_yl"]) if n else None, False, proposal, key)


def sample_play(rng: np.random.Generator, ev: Evidence) -> tuple[Optional[pd.Series], Evidence]:
    if ev.status not in {"OK", "OK_POOLED_EXPLICIT"} or ev.plays is None or len(ev.plays) == 0:
        return None, ev
    idx = int(rng.integers(0, len(ev.plays)))
    return ev.plays.iloc[idx], ev


def lookup_special(
    df: pd.DataFrame,
    posteam: str,
    kind: str,
) -> Evidence:
    """kind: punt | field_goal | extra_point | kickoff"""
    if kind == "punt":
        sub = df[(df["posteam"] == posteam) & (df["play_type"] == "punt")]
    elif kind == "field_goal":
        sub = df[(df["posteam"] == posteam) & (df["play_type"] == "field_goal")]
    elif kind == "extra_point":
        sub = df[(df["posteam"] == posteam) & (df["play_type"] == "extra_point")]
    elif kind == "kickoff":
        sub = df[df["play_type"] == "kickoff"]
    else:
        raise ValueError(kind)
    n = int(len(sub))
    if n == 0:
        return Evidence("EMPTY_STATE", 0, None, False, f"PROPOSED_league_{kind}_NOT_APPLIED")
    status = "OK" if n >= 3 else "SPARSE_STATE"
    return Evidence(status if status == "OK" else "SPARSE_STATE", n, sub if n >= 3 else (sub if n else None), False,
                    None if n >= 3 else f"PROPOSED_league_{kind}_NOT_APPLIED n={n}")
