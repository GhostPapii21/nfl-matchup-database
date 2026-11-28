"""NFL-83 phase execution receipts.

The NFL-56 freshness ledger remains the prerequisite check. This package records whether
the required analytical task for each phase was invoked and whether its output validated.
Research only. projection_ready stays false.
"""
from .runner import accept_stored_run, default_registry, run_game
from .schema import (
    CONTRACT_VERSION,
    ExecutionPolicyError,
    aggregate_status,
    claim_not_applicable,
    config_hash,
    content_hash,
    contract_document,
    contract_problems,
    mandatory_task_ids,
    validate_receipt_schema,
    verify_receipt,
)
from .slate import render_slate, slate_summary
from .store import ReceiptStore

__all__ = [
    "CONTRACT_VERSION",
    "ExecutionPolicyError",
    "ReceiptStore",
    "accept_stored_run",
    "aggregate_status",
    "claim_not_applicable",
    "config_hash",
    "content_hash",
    "contract_document",
    "contract_problems",
    "default_registry",
    "mandatory_task_ids",
    "render_slate",
    "run_game",
    "slate_summary",
    "validate_receipt_schema",
    "verify_receipt",
]
