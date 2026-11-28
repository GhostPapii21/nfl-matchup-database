"""Typed Python mirror of schemas/game_script/scenario_output.schema.json.

The JSON Schema is the source of truth for structure; these dataclasses document the same shape for Python callers and
give `from_dict` loaders. Semantic rules (probabilities total 100%, branch partition, no pooling, no duplication) are
in allocation.py.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

SCHEMA_VERSION = "game-script-scenario-output/1"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "game_script" / "scenario_output.schema.json"

BranchId = Literal["favorite_controls", "competitive", "underdog_chases"]
BRANCH_IDS: tuple[str, ...] = ("favorite_controls", "competitive", "underdog_chases")
DimensionStatus = Literal["modeled", "derived", "not_modeled"]

# The ten dimensions the assignment requires, and the payload fields that carry each one.
# ("team", field) lives in branch.teams[TEAM]; ("player", field) lives in branch.players[i].
DIMENSIONS: dict[str, tuple[tuple[str, str], ...]] = {
    "score_distribution": (("team", "points"),),
    "quarter_scoring": (("team", "quarter_points"),),
    "plays_possessions": (("team", "plays"), ("team", "possessions")),
    "pass_run": (("team", "pass_attempts"), ("team", "rush_attempts")),
    "pace": (("team", "sec_per_play"),),
    "player_opportunity": (("player", "targets"), ("player", "receptions"), ("player", "carries"),
                           ("player", "rush_opportunities")),
    "red_zone": (("team", "red_zone_trips"), ("player", "red_zone_targets"), ("player", "red_zone_carries")),
    "touchdown_opportunity": (("team", "touchdowns"), ("player", "td_opportunities")),
    "pressure_coverage": (("team", "pressure_rate_faced"), ("team", "coverage_mix_faced")),
    "late_game_rotation": (("team", "starters_rested_prob"), ("player", "snap_share_q4")),
}


def load_json_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


@dataclass
class Distribution:
    samples: Optional[list[float]] = None
    pmf: Optional[dict[str, float]] = None
    mean: Optional[float] = None
    sd: Optional[float] = None
    quantiles: Optional[dict[str, float]] = None

    @classmethod
    def from_dict(cls, d: Optional[dict]) -> Optional["Distribution"]:
        return None if d is None else cls(**d)


@dataclass
class DimensionEntry:
    status: DimensionStatus
    reason: str
    source: Optional[str] = None


@dataclass
class CoverageMix:
    man: float
    zone: float
    two_high_shell: Optional[float] = None
    prevent: Optional[float] = None


@dataclass
class TeamBlock:
    points: Optional[Distribution]
    quarter_points: Optional[dict[str, Optional[Distribution]]]
    plays: Optional[Distribution]
    possessions: Optional[Distribution]
    pass_attempts: Optional[Distribution]
    rush_attempts: Optional[Distribution]
    sec_per_play: Optional[Distribution]
    red_zone_trips: Optional[Distribution]
    touchdowns: Optional[Distribution]
    pressure_rate_faced: Optional[Distribution]
    coverage_mix_faced: Optional[CoverageMix]
    starters_rested_prob: Optional[float]

    @classmethod
    def from_dict(cls, d: dict) -> "TeamBlock":
        D = Distribution.from_dict
        qp = d.get("quarter_points")
        return cls(points=D(d["points"]),
                   quarter_points=None if qp is None else {k: D(v) for k, v in qp.items()},
                   plays=D(d["plays"]), possessions=D(d["possessions"]), pass_attempts=D(d["pass_attempts"]),
                   rush_attempts=D(d["rush_attempts"]), sec_per_play=D(d["sec_per_play"]),
                   red_zone_trips=D(d["red_zone_trips"]), touchdowns=D(d["touchdowns"]),
                   pressure_rate_faced=D(d["pressure_rate_faced"]),
                   coverage_mix_faced=None if d["coverage_mix_faced"] is None else CoverageMix(**d["coverage_mix_faced"]),
                   starters_rested_prob=d["starters_rested_prob"])


@dataclass
class PlayerBlock:
    player_id: str
    team: str
    targets: Optional[Distribution]
    receptions: Optional[Distribution]
    carries: Optional[Distribution]
    rush_opportunities: Optional[Distribution]
    red_zone_targets: Optional[Distribution]
    red_zone_carries: Optional[Distribution]
    td_opportunities: Optional[Distribution]
    snap_share_q4: Optional[Distribution]
    name: Optional[str] = None
    position: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "PlayerBlock":
        D = Distribution.from_dict
        stats = ("targets", "receptions", "carries", "rush_opportunities", "red_zone_targets", "red_zone_carries",
                 "td_opportunities", "snap_share_q4")
        return cls(player_id=d["player_id"], team=d["team"], name=d.get("name"), position=d.get("position"),
                   **{s: D(d[s]) for s in stats})


@dataclass
class Branch:
    branch_id: BranchId
    probability: float
    n_trials: int
    dimension_status: dict[str, DimensionEntry]
    teams: dict[str, TeamBlock]
    players: list[PlayerBlock] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "Branch":
        return cls(branch_id=d["branch_id"], probability=d["probability"], n_trials=d["n_trials"],
                   dimension_status={k: DimensionEntry(**v) for k, v in d["dimension_status"].items()},
                   teams={k: TeamBlock.from_dict(v) for k, v in d["teams"].items()},
                   players=[PlayerBlock.from_dict(p) for p in d["players"]])


@dataclass
class BranchDefinition:
    classifier_variable: Literal["final_margin_favorite", "regulation_margin_favorite", "end_q3_margin_favorite"]
    favorite_controls_min_margin: float
    underdog_chases_max_margin: float
    interpretation_note: Optional[str] = None


@dataclass
class ScenarioOutput:
    schema_version: str
    game: dict
    provenance: dict
    branch_definition: BranchDefinition
    branches: dict[str, Branch]

    @classmethod
    def from_dict(cls, d: dict) -> "ScenarioOutput":
        return cls(schema_version=d["schema_version"], game=d["game"], provenance=d["provenance"],
                   branch_definition=BranchDefinition(**d["branch_definition"]),
                   branches={k: Branch.from_dict(v) for k, v in d["branches"].items()})
