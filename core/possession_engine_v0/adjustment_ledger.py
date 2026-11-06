"""Adjustment ledger — prevent injury/role/pace/market double counting."""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any
import json
from pathlib import Path


@dataclass
class LedgerEntry:
    group: str
    applied_in: str  # config_id or 'none'
    mechanism: str
    forbids: list[str]
    status: str


def build_ledger(cfg: dict) -> list[LedgerEntry]:
    mode = cfg["mode"]
    cid = cfg["config_id"]
    entries = [
        LedgerEntry(
            "base_pbp",
            cid,
            "team W1–8 empirical catalog",
            ["league_silent_pool", "future_weeks"],
            "ACTIVE",
        ),
        LedgerEntry(
            "qb_injury_role",
            cid if cfg.get("adjustments", {}).get("enabled") else "none",
            "forward QB starter filter / OUT exclusions",
            ["also_apply_lamar_passing_priors", "fabricated_fagnano_career", "market_implied_qb_downgrade_as_second_hit"],
            "ACTIVE" if cfg.get("adjustments", {}).get("enabled") else "INACTIVE_DATA_ONLY",
        ),
        LedgerEntry(
            "situational_offense",
            cid,
            "audit tables only unless later wired as sampler weights",
            ["reweight_same_3rd_down_twice", "add_narrative_rz_boost_without_param"],
            "AUDIT_ONLY",
        ),
        LedgerEntry(
            "qb_pressure_proxy",
            cid,
            "qb_hit completion audit — PROXY",
            ["treat_as_measured_blitz", "stack_with_unknown_pressure_penalty"],
            "AUDIT_PROXY",
        ),
        LedgerEntry(
            "availability_workload",
            cid if mode == "script_adjusted" else "none",
            "stub notes only — no numeric weights",
            ["arbitrary_workload_penalty", "double_count_with_qb_filter"],
            "STUB_NO_WEIGHTS",
        ),
        LedgerEntry(
            "environment",
            "none",
            "weather not ingested",
            ["arbitrary_weather_boost"],
            "UNKNOWN",
        ),
        LedgerEntry(
            "market_conditioning",
            cid if mode == "market_informed" else "none",
            "spread/total conditioning only in market_informed config",
            ["contaminate_data_only_baseline", "claim_independent_market_beating_edge"],
            "ACTIVE" if mode == "market_informed" else "SEPARATE_ONLY",
        ),
        LedgerEntry(
            "pace_totals_narrative",
            "none",
            "narrative comments require auditable param map or sensitivity label",
            ["free_text_auto_calibration", "unsupported_pace_weight"],
            "FORBIDDEN_UNMAPPED",
        ),
    ]
    return entries


def write_ledger(path: Path, entries: list[LedgerEntry]) -> None:
    path.write_text(json.dumps([asdict(e) for e in entries], indent=2) + "\n")
