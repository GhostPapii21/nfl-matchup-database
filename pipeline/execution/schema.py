"""Receipt schema, hashes, and status rules for NFL-83.

Freshness statuses stay on the prerequisite block. A phase PASS is VALIDATED execution only.
Research only: projection_ready is false on every accepted receipt.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

CONTRACT_VERSION = "nfl83-phase-execution/2"
RECEIPT_SCHEMA = "nfl83-execution-receipt/1"
STATUSES = ("PASS", "PARTIAL", "MISSING", "STALE", "BLOCKED", "FAILED", "NOT_YET", "NOT_APPLICABLE")
EVIDENCE_CLASSES = ("DISCOVERED", "FRESH", "EXECUTED", "VALIDATED")
_HASH = re.compile(r"^sha256:[0-9a-f]{64}$")
_CONTRACT_PATH = Path(__file__).with_name("contract.json")

_REQUIRED = (
    "schema", "contract_version", "game_id", "phase_id", "run_id", "attempt",
    "started_at", "finished_at", "status", "evidence_class", "code_revision", "config_hash",
    "command", "entrypoint", "inputs", "prerequisite", "invocations", "outputs",
    "validation", "warnings", "failure", "not_applicable", "projection_ready", "research_only",
)


class ExecutionPolicyError(ValueError):
    """NOT_APPLICABLE was claimed without a policy or an explicit reason."""


def _finite_tree(obj):
    """Reject NaN and infinity so a hash cannot treat a non-number as a stable metric."""
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, float):
        if not math.isfinite(obj):
            raise ValueError("non-finite number")
        return obj
    if isinstance(obj, dict):
        return {key: _finite_tree(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_finite_tree(value) for value in obj]
    return obj


def canonical(obj) -> str:
    return json.dumps(_finite_tree(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def content_hash(obj) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode()).hexdigest()


def contract_document() -> dict:
    return json.loads(_CONTRACT_PATH.read_text())


def config_hash(doc: dict | None = None) -> str:
    return content_hash(doc if doc is not None else contract_document())


def contract_problems(doc: dict | None = None) -> list[str]:
    """Reject placeholder analytics and N/A policies that waive missing core work."""
    doc = doc if doc is not None else contract_document()
    root = Path(__file__).resolve().parents[2]
    problems = []
    if doc.get("contract_version") != CONTRACT_VERSION:
        problems.append("contract_version")
    if [p.get("phase_id") for p in doc.get("phases") or []] != list(range(1, 16)):
        problems.append("phases must be 1..15")
    for phase in doc.get("phases") or []:
        tasks = phase.get("tasks") or []
        if not any(t.get("mandatory") for t in tasks):
            problems.append(f"phase {phase.get('phase_id')} has no mandatory task")
        for task in tasks:
            if task.get("module") == "pipeline.execution.analytics":
                problems.append(f"{task.get('task_id')} uses the placeholder analytics module")
            policy = task.get("not_applicable_when")
            if isinstance(policy, dict) and policy.get("when") == "always":
                problems.append(f"{task.get('task_id')} marks source unavailability as always N/A")
            if isinstance(policy, dict) and policy.get("allows_phase_pass") and policy.get("when") != "indoor":
                problems.append(f"{task.get('task_id')} allows PASS without an indoor condition")
            path = task.get("canonical_path")
            binding = task.get("binding")
            if binding == "canonical":
                if not path or not (root / path).is_file():
                    problems.append(f"{task.get('task_id')} canonical file is missing")
            elif binding == "absent" and path and (root / path).is_file():
                problems.append(f"{task.get('task_id')} is marked absent but {path} exists")
            if task.get("task_id") == "phase14.sim_v6" and task.get("module") == "pipeline.sim100k":
                problems.append("phase 14 must not treat pipeline.sim100k as sim_v6")
    return problems


def mandatory_task_ids(doc: dict | None = None) -> set[str]:
    doc = doc if doc is not None else contract_document()
    return {t["task_id"] for p in doc["phases"] for t in p["tasks"] if t["mandatory"]}


def _malformed(msg: str) -> str:
    return f"MALFORMED: {msg}"


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_receipt_schema(receipt: dict) -> list[str]:
    """Structural checks. Empty means the receipt has the required shape."""
    if not isinstance(receipt, dict):
        return [_malformed("receipt is not an object")]
    errors = []
    for key in _REQUIRED:
        if key not in receipt:
            errors.append(_malformed(f"missing {key}"))
    if errors:
        return errors
    if receipt["schema"] != RECEIPT_SCHEMA:
        errors.append(_malformed("schema"))
    if receipt["contract_version"] != CONTRACT_VERSION:
        errors.append(_malformed("contract_version"))
    if not _nonempty(receipt["game_id"]) or not _nonempty(receipt["run_id"]):
        errors.append(_malformed("game_id or run_id"))
    if not isinstance(receipt["phase_id"], int) or isinstance(receipt["phase_id"], bool):
        errors.append(_malformed("phase_id"))
    if not isinstance(receipt["attempt"], int) or isinstance(receipt["attempt"], bool) or receipt["attempt"] < 1:
        errors.append(_malformed("attempt"))
    if not _nonempty(receipt["started_at"]) or not _nonempty(receipt["finished_at"]):
        errors.append(_malformed("timestamps"))
    if receipt["status"] not in STATUSES:
        errors.append(_malformed("status"))
    if receipt["evidence_class"] is not None and receipt["evidence_class"] not in EVIDENCE_CLASSES:
        errors.append(_malformed("evidence_class"))
    if not _nonempty(receipt["code_revision"]) or not _HASH.match(str(receipt["config_hash"] or "")):
        errors.append(_malformed("code_revision or config_hash"))
    if not _nonempty(receipt["command"]) or not _nonempty(receipt["entrypoint"]):
        errors.append(_malformed("command or entrypoint"))
    if receipt["projection_ready"] is not False:
        errors.append(_malformed("projection_ready must be false"))
    if receipt["research_only"] is not True:
        errors.append(_malformed("research_only must be true"))
    errors.extend(_inputs(receipt.get("inputs")))
    errors.extend(_prerequisite(receipt.get("prerequisite")))
    errors.extend(_invocations(receipt.get("invocations")))
    errors.extend(_outputs(receipt.get("outputs")))
    validation = receipt.get("validation")
    if not isinstance(validation, dict) or not isinstance(validation.get("passed"), bool) or not isinstance(validation.get("checks"), list):
        errors.append(_malformed("validation"))
    if not isinstance(receipt.get("warnings"), list):
        errors.append(_malformed("warnings"))
    errors.extend(_failure(receipt))
    errors.extend(_not_applicable(receipt))
    return errors


def _inputs(inputs) -> list[str]:
    if not isinstance(inputs, list):
        return [_malformed("inputs")]
    errors = []
    for i, item in enumerate(inputs):
        if not isinstance(item, dict):
            errors.append(_malformed(f"inputs[{i}]"))
            continue
        if not _nonempty(item.get("artifact_id")) or not _nonempty(item.get("source")):
            errors.append(_malformed(f"inputs[{i}] id or source"))
        if not _HASH.match(str(item.get("content_hash") or "")):
            errors.append(_malformed(f"inputs[{i}] content_hash"))
        if not _nonempty(item.get("provenance")):
            errors.append(_malformed(f"inputs[{i}] provenance"))
        if item.get("as_of") is not None and not _nonempty(item.get("as_of")):
            errors.append(_malformed(f"inputs[{i}] as_of"))
    return errors


def _prerequisite(pre) -> list[str]:
    if not isinstance(pre, dict):
        return [_malformed("prerequisite")]
    errors = []
    if not _nonempty(pre.get("kind")):
        errors.append(_malformed("prerequisite.kind"))
    if pre.get("evidence_class") is not None and pre.get("evidence_class") not in EVIDENCE_CLASSES:
        errors.append(_malformed("prerequisite.evidence_class"))
    if not isinstance(pre.get("satisfies_execution"), bool):
        errors.append(_malformed("prerequisite.satisfies_execution"))
    return errors


def _invocations(invocations) -> list[str]:
    if not isinstance(invocations, list):
        return [_malformed("invocations")]
    errors = []
    need = ("task_id", "module", "function", "mandatory", "command", "started_at", "finished_at", "status", "evidence_class")
    for i, item in enumerate(invocations):
        if not isinstance(item, dict) or any(k not in item for k in need):
            errors.append(_malformed(f"invocations[{i}]"))
            continue
        if item["status"] not in STATUSES or not isinstance(item["mandatory"], bool):
            errors.append(_malformed(f"invocations[{i}] status"))
        if item["evidence_class"] is not None and item["evidence_class"] not in EVIDENCE_CLASSES:
            errors.append(_malformed(f"invocations[{i}] evidence_class"))
    return errors


def _outputs(outputs) -> list[str]:
    if not isinstance(outputs, list):
        return [_malformed("outputs")]
    errors = []
    for i, item in enumerate(outputs):
        if not isinstance(item, dict):
            errors.append(_malformed(f"outputs[{i}]"))
            continue
        if not _nonempty(item.get("artifact_id")) or not _HASH.match(str(item.get("content_hash") or "")):
            errors.append(_malformed(f"outputs[{i}] hash"))
        if not isinstance(item.get("row_count"), int) or not isinstance(item.get("denominator"), int):
            errors.append(_malformed(f"outputs[{i}] counts"))
        if not isinstance(item.get("body"), dict):
            errors.append(_malformed(f"outputs[{i}] body"))
    return errors


def _failure(receipt: dict) -> list[str]:
    failure = receipt.get("failure")
    status = receipt.get("status")
    if status in {"PASS", "NOT_APPLICABLE"}:
        if failure is not None:
            return [_malformed("failure must be null when status is PASS or NOT_APPLICABLE")]
        return []
    if not isinstance(failure, dict) or not _nonempty(failure.get("code")) or not _nonempty(failure.get("message")):
        return [_malformed("failure")]
    return []


def _not_applicable(receipt: dict) -> list[str]:
    block = receipt.get("not_applicable")
    if receipt.get("status") == "NOT_APPLICABLE":
        if not isinstance(block, dict) or not _nonempty(block.get("policy_id")) or not _nonempty(block.get("reason")):
            return [_malformed("NOT_APPLICABLE requires policy_id and reason")]
        return []
    if block is not None:
        return [_malformed("not_applicable set on a status that is not NOT_APPLICABLE")]
    return []


def verify_receipt(receipt: dict, *, game_id: str, run_id: str, code_revision: str, config_hash: str) -> list[str]:
    """Fail closed. A fresh prerequisite, a wrong id, a stale revision, or a hash mismatch cannot pass."""
    reasons = list(validate_receipt_schema(receipt))
    if not isinstance(receipt, dict):
        return reasons
    if receipt.get("game_id") != game_id:
        reasons.append("WRONG_GAME")
    if receipt.get("run_id") != run_id:
        reasons.append("WRONG_RUN")
    if receipt.get("code_revision") != code_revision:
        reasons.append("STALE_CODE")
    if receipt.get("config_hash") != config_hash:
        reasons.append("STALE_CONFIG")
    for item in receipt.get("outputs") or []:
        if isinstance(item, dict) and isinstance(item.get("body"), dict):
            if item.get("content_hash") != content_hash(item["body"]):
                reasons.append("HASH_MISMATCH")
            rows = item["body"].get("rows")
            if isinstance(rows, list) and item.get("row_count") != len(rows):
                reasons.append("HASH_MISMATCH")
    if receipt.get("status") == "PASS":
        if receipt.get("evidence_class") != "VALIDATED":
            reasons.append("EVIDENCE_NOT_VALIDATED")
        pre = receipt.get("prerequisite") or {}
        if pre.get("satisfies_execution") is not False:
            reasons.append("PREREQUISITE_USED_AS_EXECUTION")
        if pre.get("evidence_class") in {"DISCOVERED", "FRESH"} and receipt.get("evidence_class") in {"DISCOVERED", "FRESH"}:
            reasons.append("FRESHNESS_IS_NOT_EXECUTION")
        for item in receipt.get("inputs") or []:
            if isinstance(item, dict) and not _nonempty(item.get("as_of")):
                reasons.append("PROVENANCE")
        invocations = receipt.get("invocations") or []
        if not invocations:
            reasons.append("NOT_INVOKED")
        for call in invocations:
            if isinstance(call, dict) and call.get("mandatory") and call.get("status") != "PASS":
                reasons.append("NOT_VALIDATED")
            if isinstance(call, dict) and call.get("mandatory") and call.get("evidence_class") != "VALIDATED":
                reasons.append("NOT_VALIDATED")
        if not receipt.get("outputs"):
            reasons.append("MISSING_OUTPUT")
    return reasons


def aggregate_status(prerequisite_status: str, tasks: list[dict]) -> str:
    """Fold a freshness gate and task outcomes into one phase status.

    FRESH is not a phase status. DISCOVERED, STALE, MISSING, GAP, and NOT_YET block PASS
    even when every task result says PASS.
    """
    blocked = {
        "MISSING": "MISSING",
        "STALE": "STALE",
        "GAP": "BLOCKED",
        "BLOCKED": "BLOCKED",
        "NOT_YET": "NOT_YET",
        "DISCOVERED": "BLOCKED",
    }
    if prerequisite_status in blocked:
        return blocked[prerequisite_status]
    mandatory = [t for t in tasks if t.get("mandatory")]
    optional = [t for t in tasks if not t.get("mandatory")]
    if any(t.get("status") == "FAILED" for t in mandatory):
        return "FAILED"
    if any(t.get("status") == "BLOCKED" for t in mandatory):
        return "BLOCKED"
    if any(t.get("status") in {"MISSING", "NOT_RUN"} for t in mandatory):
        return "FAILED"
    not_applicable = [t for t in mandatory if t.get("status") == "NOT_APPLICABLE"]
    passed = [t for t in mandatory if t.get("status") == "PASS"]
    other = [t for t in mandatory if t.get("status") not in {"NOT_APPLICABLE", "PASS"}]
    if other:
        return "FAILED"
    if not_applicable and not passed:
        return "NOT_APPLICABLE"
    if not_applicable and any(not t.get("allows_phase_pass") for t in not_applicable):
        return "FAILED"
    if any(t.get("status") == "FAILED" for t in optional):
        return "PARTIAL"
    if not passed:
        return "FAILED"
    return "PASS"


def claim_not_applicable(task: dict, reason: str) -> dict:
    policy = task.get("not_applicable_when") if isinstance(task, dict) else None
    if not isinstance(policy, dict) or not _nonempty(policy.get("policy_id")):
        raise ExecutionPolicyError("NOT_APPLICABLE requires a policy_id")
    if "allows_phase_pass" not in policy:
        raise ExecutionPolicyError("NOT_APPLICABLE policy must say whether the phase may still pass")
    if policy.get("when") == "always":
        raise ExecutionPolicyError("source unavailability is not NOT_APPLICABLE; when=always cannot waive a task")
    if policy.get("allows_phase_pass") and policy.get("when") != "indoor":
        raise ExecutionPolicyError("only an indoor-weather policy may allow the rest of a phase to pass")
    if not _nonempty(reason):
        raise ExecutionPolicyError("NOT_APPLICABLE requires an explicit reason")
    return {
        "task_id": task.get("task_id"),
        "status": "NOT_APPLICABLE",
        "policy_id": policy["policy_id"],
        "reason": reason.strip(),
        "satisfies_execution": False,
        "allows_phase_pass": bool(policy["allows_phase_pass"]),
    }
