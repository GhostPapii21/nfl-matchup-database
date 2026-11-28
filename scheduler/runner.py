"""Phase handlers.

The default handler records a scheduler receipt and does not run analytical
work. NFL-82 is still inventorying entrypoints and NFL-83 owns execution
receipts, so this package does not call pipeline.sim100k, snapshots.lock,
pregame builders, or any publisher. A handler that reports projection_ready,
betting, or publishing is rejected by the orchestrator.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Protocol


@dataclass
class HandlerResult:
    status: str  # recorded, refused, failed
    detail: str
    analytical_execution: bool = False
    projection_ready: bool = False
    betting_started: bool = False
    publishing_started: bool = False
    artifacts: dict[str, bytes] = field(default_factory=dict)


class JobContext:
    def __init__(self, job: dict, game: dict | None, now: datetime, heartbeat: Callable[[datetime], bool]):
        self.job = job
        self.game = game
        self.now = now
        self._heartbeat = heartbeat

    def heartbeat(self, now: datetime | None = None) -> bool:
        return self._heartbeat(now or self.now)


class Runner(Protocol):
    def run(self, ctx: JobContext) -> HandlerResult: ...


class UnwiredRunner:
    """Receipt-only handler. Analytical phases stay unwired on purpose."""

    detail = (
        "scheduler receipt only; analytical execution is not wired "
        "(waiting on NFL-82 inventory and NFL-83 execution receipts). "
        "projection_ready stays false. No betting and no publishing."
    )

    def run(self, ctx: JobContext) -> HandlerResult:
        body = {
            "game_id": ctx.job["game_id"],
            "phase": ctx.job["phase"],
            "attempt": ctx.job["attempt"],
            "schedule_version": ctx.job["schedule_version"],
            "analytical_execution": False,
            "projection_ready": False,
            "betting_started": False,
            "publishing_started": False,
            "detail": self.detail,
        }
        encoded = json.dumps(body, sort_keys=True).encode()
        return HandlerResult(
            status="recorded",
            detail=self.detail,
            analytical_execution=False,
            artifacts={"scheduler_receipt.json": encoded},
        )


def reject_reason(result: HandlerResult) -> str | None:
    if result.projection_ready:
        return "rejected: handler tried to set projection_ready true"
    if result.betting_started:
        return "rejected: handler tried to start betting"
    if result.publishing_started:
        return "rejected: handler tried to start publishing"
    return None
