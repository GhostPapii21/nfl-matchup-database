"""Per-game parallel fan-out of existing NFL modules (NFL-87).

Research only. projection_ready stays false. This package does not schedule work
and does not depend on GitHub Actions.
"""
from .modules import default_registry
from .runner import run_games
from .spec import GameCall, ModuleResult, ModuleSpec

__all__ = ["GameCall", "ModuleResult", "ModuleSpec", "default_registry", "run_games"]
