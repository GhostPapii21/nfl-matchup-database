"""Durable per-game scheduler.

This package decides when a game's injury refresh, pre-kick lock, and postgame
grade are due, and it keeps a lease so a crashed worker can retry without a
second overlapping run. It does not set projection_ready and it does not start
betting or publishing. GitHub Actions is not invoked.

Local state is SQLite. The production target is a dedicated Render Postgres
plus an always-on background worker, documented in docs/automation/SCHEDULER.md
and not created from here.
"""

from .model import Game
from .orchestrator import Orchestrator, open_store
from .timeutil import ScheduleError, parse_kickoff

__all__ = ["Game", "Orchestrator", "ScheduleError", "open_store", "parse_kickoff"]
