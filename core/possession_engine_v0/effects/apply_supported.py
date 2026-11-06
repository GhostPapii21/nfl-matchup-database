"""Apply ONLY supported effects to the snap catalog — must change joint sampled events.

Supported:
  - annotate snaps with explosive flag (definition-based)
  - annotate pass snaps with is_blitz_ftn when FTN joined
  - optional script_adjusted: down-weight (not invent coeffs) by excluding extreme
    historical explosive long TDs? NO — don't invent.

Actual sim effect that is testable without invented coefficients:
  - When effects_enabled, pass-play sampling can stratify: with probability p_blitz
    sample from blitz-joined rows when available for that team; else fall back with flag.
  - p_blitz estimated empirically as team's faced/own blitz rate from FTN join — data-driven rate, not hand weight.
"""
from __future__ import annotations
from typing import Any, Optional
import numpy as np
import pandas as pd
from effects.definitions import EXPLOSIVE_PASS_YARDS, EXPLOSIVE_RUSH_YARDS


def annotate_snaps(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    yg = pd.to_numeric(out.get("yards_gained"), errors="coerce").fillna(0)
    out["is_explosive"] = (
        ((out["play_type"] == "pass") & (yg >= EXPLOSIVE_PASS_YARDS))
        | ((out["play_type"] == "run") & (yg >= EXPLOSIVE_RUSH_YARDS))
    )
    if "qb_hit" in out.columns:
        out["pressure_proxy_qb_hit"] = out["qb_hit"].fillna(0).astype(int) == 1
    else:
        out["pressure_proxy_qb_hit"] = False
    if "is_blitz_ftn" not in out.columns:
        out["is_blitz_ftn"] = False
        out["ftn_joined"] = False
    return out


class EffectsCatalog:
    """Wraps PlayCatalog-like sampling with optional blitz stratification (empirical rate)."""

    def __init__(self, base_catalog, annotated: pd.DataFrame, *, enable_blitz_strata: bool):
        self.base = base_catalog
        self.df = annotated
        self.enable_blitz_strata = enable_blitz_strata
        self.min_n = base_catalog.min_n
        self.specials = base_catalog.specials
        self.fourth_probs = base_catalog.fourth_probs
        self.cells = base_catalog.cells
        self.by_down = base_catalog.by_down
        self.by_team = base_catalog.by_team
        # Duck-type PlayCatalog attributes used by simulate_one / _clock_cost / defense
        self.clock_map = getattr(base_catalog, "clock_map", None)
        self.clock_meta = getattr(base_catalog, "clock_meta", {"source": "fixed_defaults"})
        self._defense_cond = getattr(base_catalog, "_defense_cond", False)
        self.by_team_vs_def = getattr(base_catalog, "by_team_vs_def", {})
        # empirical blitz rate by posteam among joined passes
        self.blitz_rate = {}
        passes = annotated[(annotated["play_type"] == "pass") & (annotated.get("ftn_joined", False) == True)]
        for team, g in passes.groupby("posteam"):
            self.blitz_rate[team] = float(g["is_blitz_ftn"].mean()) if len(g) else 0.0
        self.defense_blitz_rate = {}
        self.blitz_pools = {}
        self.noblitz_pools = {}
        for team, g in annotated[annotated["play_type"] == "pass"].groupby("posteam"):
            bj = g[g["is_blitz_ftn"] & g["ftn_joined"]]
            nj = g[(~g["is_blitz_ftn"]) & g["ftn_joined"]]
            if len(bj) >= 5:
                self.blitz_pools[team] = bj
            if len(nj) >= 5:
                self.noblitz_pools[team] = nj

    def set_empirical_clock(self, cost_map: dict) -> None:
        self.base.set_empirical_clock(cost_map)
        self.clock_map = self.base.clock_map
        self.clock_meta = self.base.clock_meta

    def enable_defense_conditioning(self, enabled: bool = True) -> None:
        self.base.enable_defense_conditioning(enabled)
        self._defense_cond = self.base._defense_cond

    def set_defense_blitz_rates(self, rates: dict):
        """Empirical FTN blitz rates allowed by defense team (data-driven, not hand weights)."""
        self.defense_blitz_rate = dict(rates or {})

    def __getattr__(self, name):
        # Delegate any PlayCatalog attribute (fourth_cells, def_allowed_*, ...) to base.
        if name == "base":
            raise AttributeError(name)
        return getattr(self.base, name)

    def sample_snap(self, rng: np.random.Generator, st, allow_pool: bool):
        """Base sampler decides run/pass (and DEF_* interaction). Blitz only re-draws a CALLED pass
        from same-down blitz / non-blitz joined pools, with empirical rate."""
        row, tag = self.base.sample_snap(rng, st, allow_pool)
        if (
            row is None or not self.enable_blitz_strata or str(row.get("play_type")) != "pass"
            or str(tag).startswith("DEF_")
        ):
            return row, tag
        off = st.possession
        defense = st.home if off == st.away else st.away
        if defense in self.defense_blitz_rate:
            p, pre = self.defense_blitz_rate[defense], "EFFECT_DEF_BLITZ"
        elif off in self.blitz_rate:
            p, pre = self.blitz_rate[off], "EFFECT_BLITZ"
        else:
            return row, tag
        use_blitz = bool(rng.random() < p)
        pools = self.blitz_pools if use_blitz else self.noblitz_pools
        team_pool = pools.get(off)
        if team_pool is None:
            return row, f"{tag}|BLITZ_NO_POOL"
        same_down = team_pool[team_pool["down"] == st.down]
        pool, sfx = (same_down, "") if len(same_down) >= 5 else (team_pool, f"|COARSE_BLITZ_DOWN_n={len(team_pool)}")
        new = pool.iloc[int(rng.integers(0, len(pool)))]
        return new, f"{tag}|{pre}_{'STRATA' if use_blitz else 'NO_STRATA'}{sfx}"
