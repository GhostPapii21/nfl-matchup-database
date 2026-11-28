"""Per-game phases and idempotency keys.

Windows are measured from the UTC kickoff instant:

* injury_refresh opens at T-90, when clubs post official inactives
  (pipeline.freshness.INACTIVES_POST_MINUTES_BEFORE_KICKOFF) and closes at
  T-40, the same close pipeline.window uses so a late injury pull does not
  start after the lock has run out of time.
* prekick_lock opens at T-70 and is not claimable until a validated
  injury_refresh artifact exists for the same game and schedule version.
  A receipt-only or refused refresh does not count. Its deadline is the kickoff
  instant. A run that has not started by kickoff is missed and the handler
  is not called. snapshots.lock refuses now >= kickoff; this window matches
  that rule. A succeeded lock is immutable.
* postgame_grade opens at kickoff+3h, or immediately once the schedule says
  the game is final and kickoff has passed. It closes at kickoff+36h.

The prekick_lock job is the heavy slot reserved for a future 300k-trial
simulation. The scheduler does not start that simulation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

from .timeutil import ScheduleError, utc_iso

GAME_STATUSES = ("scheduled", "postponed", "cancelled", "final")
TERMINAL_FAILURE = ("missed", "dead", "refused", "cancelled", "blocked", "superseded")
INJURY_PHASE = "injury_refresh"
LOCK_PHASE = "prekick_lock"
POSTGAME_PHASE = "postgame_grade"


@dataclass(frozen=True)
class Phase:
    name: str
    heavy: bool
    immutable: bool
    open_offset: timedelta
    deadline_offset: timedelta


PHASES: tuple[Phase, ...] = (
    Phase(INJURY_PHASE, False, False, timedelta(minutes=-90), timedelta(minutes=-40)),
    Phase(LOCK_PHASE, True, True, timedelta(minutes=-70), timedelta(0)),
    Phase(POSTGAME_PHASE, False, False, timedelta(hours=3), timedelta(hours=36)),
)
PHASE_BY_NAME = {phase.name: phase for phase in PHASES}
HEAVY_PHASES = frozenset(phase.name for phase in PHASES if phase.heavy)
# A generic succeeded/recorded job status does not unlock the lock. The
# artifact below has to name this game and this schedule version.
INJURY_REFRESH_ARTIFACT = "injury_refresh.json"
INJURY_REFRESH_SCHEMA = "scheduler-injury-refresh/1"
OPEN_JOB_STATUSES = ("queued", "leased")


@dataclass(frozen=True)
class Game:
    game_id: str
    season: int
    week: int
    away: str
    home: str
    kickoff_utc: datetime
    status: str
    timezone: str = "America/New_York"

    def __post_init__(self) -> None:
        if not self.game_id or any(ch.isspace() for ch in self.game_id):
            raise ScheduleError("game_id must be a non-empty token")
        if self.status not in GAME_STATUSES:
            raise ScheduleError(f"status must be one of {GAME_STATUSES}")
        if self.kickoff_utc.tzinfo is None:
            raise ScheduleError("kickoff_utc must be timezone-aware")

    def version(self) -> str:
        """Identity of the kickoff instant. Status changes do not mint a new version."""
        return hashlib.sha256(utc_iso(self.kickoff_utc).encode()).hexdigest()[:16]


@dataclass(frozen=True)
class DesiredJob:
    game_id: str
    phase: str
    schedule_version: str
    not_before_utc: datetime
    deadline_utc: datetime
    heavy: bool
    immutable: bool
    idempotency_key: str
    payload_json: str


def phase_window(phase: Phase, game: Game, now: datetime) -> tuple[datetime, datetime]:
    open_at = game.kickoff_utc + phase.open_offset
    deadline = game.kickoff_utc + phase.deadline_offset
    if phase.name == POSTGAME_PHASE and game.status == "final" and now >= game.kickoff_utc:
        open_at = min(open_at, now)
    if deadline <= open_at:
        raise ScheduleError(f"{phase.name} deadline is not after its open time for {game.game_id}")
    return open_at, deadline


def injury_refresh_artifact(game_id: str, schedule_version: str) -> bytes:
    """Bytes a handler must store before the pre-kick lock may run."""
    return json.dumps({
        "schema": INJURY_REFRESH_SCHEMA,
        "game_id": game_id,
        "phase": INJURY_PHASE,
        "schedule_version": schedule_version,
        "work_completed": True,
    }, sort_keys=True).encode()


def injury_refresh_valid(body: bytes | str, game_id: str, schedule_version: str) -> bool:
    try:
        doc = json.loads(body)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
        return False
    if not isinstance(doc, dict):
        return False
    return (
        doc.get("schema") == INJURY_REFRESH_SCHEMA
        and doc.get("game_id") == game_id
        and doc.get("phase") == INJURY_PHASE
        and doc.get("schedule_version") == schedule_version
        and doc.get("work_completed") is True
    )


def idempotency_key(game_id: str, phase: str, schedule_version: str, replay: int = 0) -> str:
    base = f"{game_id}:{phase}:{schedule_version}"
    if replay:
        return f"{base}:replay:{replay}"
    return base
