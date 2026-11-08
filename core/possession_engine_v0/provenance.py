"""Per-input provenance: definition, as-of, freshness, n, reproducibility, status.
No arbitrary blanket trust scores — status is evidential, not a 0–100 score.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Optional
import json
from pathlib import Path


@dataclass
class InputProvenance:
    input_id: str
    definition: str
    source_path_or_url: str
    as_of_et: str
    freshness_note: str
    sample_size: Optional[int]
    sample_unit: str
    reproducibility: str  # deterministic_filter | seeded_sim | manual_note | unknown
    status: str  # OK | SPARSE | PROXY | MISSING | UNKNOWN | SCENARIO_ONLY
    used_in_configs: list[str]
    double_count_group: Optional[str] = None  # ledger group key
    notes: str = ""

    def to_dict(self):
        return asdict(self)


def build_default_registry(*, hist_evidence: dict, adj_meta: dict, situational_ns: dict) -> list[InputProvenance]:
    rows = [
        InputProvenance(
            "pbp_2026_team_w1_8",
            "nflfastR-shaped play-by-play rows for games involving JAX or BAL, season 2026 weeks 1–8; offense catalog posteam in {JAX,BAL}",
            "research/period_engine_v0/data/play_by_play_2026.parquet → nfl-database r2 src",
            "2026-11-05 (local file)",
            "Static local parquet; not re-pulled this run",
            hist_evidence.get("n_plays"),
            "offense_plays",
            "deterministic_filter",
            "OK",
            ["data_only", "script_adjusted", "market_informed"],
            "base_pbp",
        ),
        InputProvenance(
            "qb_adjustment_bal_fagnano",
            "Forward-only starter filter: BAL pass plays limited to J.Fagnano; L.Jackson OUT excluded; Huntley doubtful excluded from starter pool",
            "config/jax_bal_tnf_2026-11-05_script_adjusted.json + runs/.../brainstorm_read.md notes dated 2026-11-03",
            "2026-11-05T13:00:00-05:00",
            "Notes from 2026-11-03; confirm inactives separately before any bet use (not authorized here)",
            (adj_meta.get("BAL") or {}).get("n_pass_after"),
            "BAL_pass_plays_after_filter",
            "deterministic_filter",
            "SPARSE" if (adj_meta.get("BAL") or {}).get("sparse_qb") else "OK",
            ["script_adjusted"],
            "qb_injury_role",
            "Does not fabricate Fagnano history; does not rewrite W1–8 rows for data_only",
        ),
        InputProvenance(
            "third_down_conversion",
            "Frequency of 3rd-down opportunities and P(convert|3rd) from PBP third_down_converted/failed",
            "same PBP",
            "2026-11-05",
            "Derived this run from W1–8 filter",
            situational_ns.get("third_down_n"),
            "third_down_plays",
            "deterministic_filter",
            "OK" if (situational_ns.get("third_down_n") or 0) >= 20 else "SPARSE",
            ["data_only", "script_adjusted"],
            "situational_offense",
        ),
        InputProvenance(
            "red_zone",
            "RZ opportunity (play or drive yardline_100<=20) and score/TD conditional rates",
            "same PBP",
            "2026-11-05",
            "Derived this run",
            situational_ns.get("rz_n"),
            "rz_plays",
            "deterministic_filter",
            "OK" if (situational_ns.get("rz_n") or 0) >= 20 else "SPARSE",
            ["data_only", "script_adjusted"],
            "situational_offense",
        ),
        InputProvenance(
            "qb_hit_completion_proxy",
            "Completion rate split by qb_hit==1 vs 0 — PROXY for pressure; NOT measured blitz/pressure",
            "PBP column qb_hit",
            "2026-11-05",
            "Derived this run",
            situational_ns.get("qb_hit_n"),
            "pass_attempts_with_qb_hit_flag",
            "deterministic_filter",
            "PROXY",
            ["script_adjusted", "data_only"],
            "qb_pressure_proxy",
            "blitz/was_pressure columns MISSING — do not treat as true pressure",
        ),
        InputProvenance(
            "coverage_routes_man_zone",
            "Actual coverage shell, route tree, man/zone, middle-open, primary CB/S",
            "NOT IN LOCAL PBP",
            "2026-11-05",
            "n/a",
            0,
            "plays",
            "unknown",
            "MISSING",
            [],
            None,
            "PBP alone cannot establish; pass_location is not route-vs-CB",
        ),
        InputProvenance(
            "weather",
            "Game-time weather (wind/temp/precip)",
            "NOT INGESTED in this module yet",
            "2026-11-05",
            "unknown",
            None,
            "games",
            "unknown",
            "UNKNOWN",
            [],
            "environment",
            "No unsupported weather weights",
        ),
        InputProvenance(
            "road_rest_travel_practice",
            "Road/rest/travel/practice availability uncertainty",
            "Schedule implied by PBP game_id + miss_audit practice DNP notes",
            "notes 2026-11-03–05",
            "Qualitative stub",
            None,
            "notes",
            "manual_note",
            "UNKNOWN",
            ["script_adjusted"],
            "availability_workload",
            "Evidence stub only — no numeric boosts",
        ),
        InputProvenance(
            "market_spread_total",
            "Spread/total quotes for conditioning",
            "Screenshot/API quotes external — only via market_informed config",
            "varies",
            "Must not enter data_only",
            None,
            "markets",
            "manual_note",
            "SCENARIO_ONLY",
            ["market_informed"],
            "market_conditioning",
            "Not independent market-beating evidence; separate config",
        ),
    ]
    return rows


def write_registry(path: Path, rows: list[InputProvenance]) -> None:
    path.write_text(json.dumps([r.to_dict() for r in rows], indent=2) + "\n")
