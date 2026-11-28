"""Declared contracts for one callable in a per-game run.

A module counts as analytical execution only when its class is analytical, it was
invoked, it returned PASS or PARTIAL, and the output is not a receipt-only stub.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ModuleSpec:
    module_id: str
    execution_class: str
    fn: Callable
    depends_on: tuple[str, ...] = ()
    critical: bool = False
    timeout_sec: float = 30.0
    retries: int = 0
    freshness: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    output_contract: str = ""
    required_inputs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        allowed = {"analytical", "adapter", "freshness", "gate", "stub"}
        if self.execution_class not in allowed:
            raise ValueError(f"{self.module_id}: execution_class {self.execution_class} not in {sorted(allowed)}")
        if not self.output_contract:
            raise ValueError(f"{self.module_id}: output_contract is required")
        if self.timeout_sec <= 0:
            raise ValueError(f"{self.module_id}: timeout_sec must be positive")
        if self.retries < 0:
            raise ValueError(f"{self.module_id}: retries must be >= 0")


@dataclass
class ModuleResult:
    status: str
    output: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)


@dataclass
class GameCall:
    game_id: str
    packet: dict
    context: dict
    artifact_dir: Path
    attempt: int
    module_id: str
    as_of: str
