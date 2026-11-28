"""Run the 15-phase execution contract and persist immutable receipts.

A freshness row, however current, is recorded as a prerequisite with satisfies_execution false.
Absent canonical modules stay BLOCKED. pipeline.sim100k is not called and is not sim_v6.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .schema import (
    RECEIPT_SCHEMA,
    aggregate_status,
    claim_not_applicable,
    config_hash,
    content_hash,
    contract_document,
    verify_receipt,
)
from .slate import render_slate, slate_summary
from .store import ReceiptStore

INDOOR_ROOFS = {"dome", "closed", "indoors", "indoor", "retractable"}
_OK = {"FRESH", "NOT_REQUIRED"}
_RANK = {"MISSING": 4, "STALE": 3, "GAP": 2, "BLOCKED": 2, "NOT_YET": 1}
_RUN_RANK = {"FAILED": 7, "MISSING": 6, "STALE": 5, "BLOCKED": 4, "NOT_YET": 3, "PARTIAL": 2, "NOT_APPLICABLE": 1, "PASS": 0}
_GATE_FAILURE = {
    "MISSING": "MISSING_INPUT",
    "STALE": "STALE_INPUT",
    "GAP": "FRESHNESS_GAP",
    "BLOCKED": "FRESHNESS_GAP",
    "NOT_YET": "NOT_YET_INPUT",
    "DISCOVERED": "DISCOVERED_NOT_EXECUTED",
}


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def _indoor(packet: dict) -> bool:
    game = packet.get("game") or {}
    weather = packet.get("weather") or {}
    roof = str(game.get("roof") or "").strip().lower()
    return str(weather.get("status") or "").upper() == "INDOOR" or roof in INDOOR_ROOFS


def _policy_applies(task: dict, packet: dict) -> bool:
    policy = task.get("not_applicable_when")
    if not isinstance(policy, dict):
        return False
    when = policy.get("when")
    if when == "always":
        return True
    if when == "indoor":
        return _indoor(packet)
    if when == "outdoor":
        return not _indoor(packet)
    return False


_BINDING_CODE = {
    "absent": "MODULE_ABSENT",
    "source_unavailable": "SOURCE_UNAVAILABLE",
    "unbound": "UNBOUND",
}
_COUNT_METRICS = {
    "players", "games", "count", "defenders", "depth_groups", "markets", "official", "espn_live",
    "players_with_snap_share", "dropbacks_charted", "site", "players_with_baseline",
}


def default_registry() -> dict:
    """Bind adapters that call real equation modules. Absent tasks are not given stand-ins."""
    from . import canonical

    registry = {}
    for phase in contract_document()["phases"]:
        for task in phase["tasks"]:
            if task.get("binding") == "canonical" and task.get("adapter"):
                registry[task["task_id"]] = getattr(canonical, task["adapter"])
    return registry


def _reject_non_analytic(result: dict, task: dict) -> dict | None:
    if not task.get("require_analytic", True):
        return None
    expected = f"{task.get('module')}.{task.get('function')}"
    equation = result.get("equation_id")
    if not isinstance(equation, str) or equation != expected:
        return {
            "code": "ANALYTIC_OUTPUT_MISSING",
            "message": f"{task['task_id']} did not return equation_id {expected}. A summary row is not that equation.",
        }
    if result.get("module_id") != task.get("module"):
        return {
            "code": "ANALYTIC_OUTPUT_MISSING",
            "message": f"{task['task_id']} module_id does not match canonical module {task.get('module')}",
        }
    metrics = result.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        return {"code": "COUNT_ONLY", "message": f"{task['task_id']} emitted no equation metrics"}
    numeric = [key for key, value in metrics.items() if isinstance(value, (int, float)) and not isinstance(value, bool)]
    if not numeric or all(key in _COUNT_METRICS or key.endswith("_count") for key in numeric):
        return {"code": "COUNT_ONLY", "message": f"{task['task_id']} metrics are only counts or metadata"}
    for key in task.get("required_metrics") or []:
        if key not in metrics:
            return {"code": "ANALYTIC_OUTPUT_MISSING", "message": f"{task['task_id']} missing metric {key}"}
    if not isinstance(result.get("provenance"), str) or not result["provenance"].strip():
        return {"code": "PROVENANCE", "message": f"{task['task_id']} analytic output has no provenance"}
    return None


def _rows_by_source(rows: list[dict] | None) -> dict[str, dict]:
    found = {}
    for row in rows or []:
        if isinstance(row, dict) and row.get("source"):
            found[row["source"]] = row
    return found


def _gate(sources: list[str], by_source: dict[str, dict]) -> str:
    if not sources:
        return "OK"
    worst = "OK"
    worst_rank = 0
    for source in sources:
        row = by_source.get(source)
        status = None if row is None else row.get("status")
        if status in _OK:
            continue
        if status not in _RANK:
            status = "MISSING"
        if _RANK[status] > worst_rank:
            worst, worst_rank = status, _RANK[status]
    return worst


def _inputs(packet: dict, sources: list[str], by_source: dict[str, dict], *, discovered: bool) -> list[dict]:
    game_id = (packet.get("game") or {}).get("game_id")
    inputs = [{
        "artifact_id": "packet",
        "content_hash": content_hash(packet),
        "source": "packet",
        "provenance": "pregame packet presented to this run; hash is the packet body, not a freshness claim",
        "as_of": packet.get("generated_utc"),
    }]
    for source in sources:
        row = by_source.get(source) or {}
        payload = {
            "source": source,
            "freshness_status": None if discovered else row.get("status"),
            "as_of": None if discovered else row.get("as_of_utc"),
            "game_id": game_id,
        }
        inputs.append({
            "artifact_id": f"src:{source}",
            "content_hash": content_hash(payload),
            "source": source,
            "provenance": f"freshness source {source}; publisher or pull as-of from the freshness row, separate from execution",
            "as_of": None if discovered else row.get("as_of_utc"),
        })
    return inputs


def _command(game_id: str, run_id: str, phase_id: int, task_id: str | None = None) -> str:
    text = f"python -m pipeline.execution --game {game_id} --run-id {run_id} --phase {phase_id}"
    if task_id:
        text += f" --task {task_id}"
    return text


def _invoke(task: dict, ctx: dict, fn, stamp: str) -> tuple[dict, dict | None, dict | None]:
    """Return (invocation, output or None, failure or None)."""
    started = stamp
    try:
        result = fn(ctx)
    except Exception as exc:  # noqa: BLE001 — the receipt must record the task error, not crash the slate
        failure = {"code": "TASK_RAISED", "message": f"{task['task_id']} raised {type(exc).__name__}: {exc}"}
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, failure
    if not isinstance(result, dict):
        failure = {"code": "EMPTY_OUTPUT", "message": f"{task['task_id']} returned {type(result).__name__}, not an object"}
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, failure
    if result.get("projection_ready") is True:
        failure = {"code": "PROJECTION_READY_REFUSED", "message": f"{task['task_id']} tried to set projection_ready true"}
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, failure
    if result.get("blocked"):
        code = str(result.get("code") or "UNBOUND")
        message = str(result.get("message") or f"{task['task_id']} is blocked")
        return _call(task, stamp, started, "BLOCKED", "EXECUTED"), None, {"code": code, "message": message}
    if result.get("game_id") != ctx["game_id"]:
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, {
            "code": "GAME_MISMATCH",
            "message": f"{task['task_id']} returned game_id {result.get('game_id')!r}",
        }
    if result.get("run_id") != ctx["run_id"]:
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, {
            "code": "RUN_MISMATCH",
            "message": f"{task['task_id']} returned run_id {result.get('run_id')!r}",
        }
    rows = result.get("rows")
    try:
        denominator = int(result.get("denominator"))
    except (TypeError, ValueError):
        denominator = -1
    min_rows = int(task.get("min_rows") or 1)
    min_denominator = int(task.get("min_denominator") or 1)
    if not isinstance(rows, list) or len(rows) < min_rows or denominator < min_denominator:
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, {
            "code": "EMPTY_OUTPUT",
            "message": f"{task['task_id']} returned {0 if not isinstance(rows, list) else len(rows)} rows "
                       f"and denominator {result.get('denominator')!r}; minimum is {min_rows} rows and {min_denominator}",
        }
    analytic = _reject_non_analytic(result, task)
    if analytic:
        return _call(task, stamp, started, "FAILED", "EXECUTED"), None, analytic
    output = {
        "artifact_id": task["task_id"],
        "content_hash": content_hash(result),
        "row_count": len(rows),
        "denominator": denominator,
        "body": result,
    }
    return _call(task, stamp, started, "PASS", "VALIDATED"), output, None


def _call(task: dict, started: str, finished: str, status: str, evidence: str) -> dict:
    return {
        "task_id": task["task_id"],
        "module": task["module"],
        "function": task["function"],
        "mandatory": bool(task["mandatory"]),
        "command": task["command"],
        "started_at": started,
        "finished_at": finished,
        "status": status,
        "evidence_class": evidence,
    }


def _evidence_for(status: str, invocations: list[dict]) -> str | None:
    if status == "PASS":
        return "VALIDATED"
    if invocations:
        return "EXECUTED"
    return None


def _phase_failure(status: str, task_failure: dict | None, gate: str) -> dict | None:
    if status == "PASS":
        return None
    if status == "NOT_APPLICABLE":
        return None
    if task_failure and status in {"FAILED", "BLOCKED", "PARTIAL"}:
        if status == "PARTIAL":
            return {"code": "OPTIONAL_FAILED", "message": task_failure["message"]}
        return task_failure
    if status == "PARTIAL":
        return {"code": "OPTIONAL_FAILED", "message": "an optional task failed"}
    code = _GATE_FAILURE.get(gate, "FAILED")
    if status == "BLOCKED" and gate == "DISCOVERED":
        code = "DISCOVERED_NOT_EXECUTED"
    return {"code": code, "message": f"phase prerequisite is {gate}; analytical execution was not accepted"}


def run_game(
    packet: dict,
    *,
    run_id: str,
    store: ReceiptStore,
    registry: dict | None = None,
    freshness_rows: list[dict] | None = None,
    now: datetime | None = None,
    code_revision: str = "UNKNOWN",
    phases: list[int] | None = None,
    skip_tasks: set[str] | None = None,
    discover_only: bool = False,
) -> dict:
    now = now or datetime.now(timezone.utc)
    stamp = _iso(now)
    registry = default_registry() if registry is None else registry
    skip_tasks = set(skip_tasks or ())
    doc = contract_document()
    cfg = config_hash(doc)
    game_id = (packet.get("game") or {}).get("game_id")
    selected = [p for p in doc["phases"] if phases is None or p["phase_id"] in phases]
    by_source = {} if discover_only else _rows_by_source(freshness_rows)
    receipts = []
    replayed = []
    for phase in selected:
        sources = list(phase["freshness_sources"])
        inputs = _inputs(packet, sources, by_source, discovered=discover_only)
        prior = store.attempts(game_id, run_id, phase["phase_id"])
        if prior:
            latest = prior[-1]
            same_inputs = [item["content_hash"] for item in latest.get("inputs") or []] == [item["content_hash"] for item in inputs]
            if (latest.get("status") == "PASS" and latest.get("code_revision") == code_revision
                    and latest.get("config_hash") == cfg and same_inputs):
                receipts.append(latest)
                replayed.append(phase["phase_id"])
                continue
        gate = "DISCOVERED" if discover_only else _gate(sources, by_source)
        if discover_only or not sources or gate != "OK":
            evidence = "DISCOVERED"
        else:
            evidence = "FRESH"
        provenance_gap = (
            not discover_only and gate == "OK"
            and any(not isinstance(item.get("as_of"), str) or not item["as_of"].strip() for item in inputs)
        )
        invocations: list[dict] = []
        outputs = []
        na_records = []
        optional_records = []
        blocked_tasks: list[dict] = []
        warnings: list[str] = []
        task_rows = []
        task_failure = None
        if discover_only or gate != "OK" or provenance_gap:
            pass
        else:
            for task in phase["tasks"]:
                task = dict(task)
                task["command"] = _command(game_id, run_id, phase["phase_id"], task["task_id"])
                applies = _policy_applies(task, packet)
                present = task["task_id"] in registry
                skipped = task["task_id"] in skip_tasks
                if task["mandatory"] and applies:
                    claimed = claim_not_applicable(task, task["not_applicable_when"]["reason"])
                    na_records.append(claimed)
                    task_rows.append({"mandatory": True, "status": "NOT_APPLICABLE", "allows_phase_pass": claimed["allows_phase_pass"]})
                    continue
                if (not task["mandatory"]) and applies and (skipped or not present):
                    claimed = claim_not_applicable(task, task["not_applicable_when"]["reason"])
                    na_records.append(claimed)
                    optional_records.append(claimed)
                    task_rows.append({"mandatory": False, "status": "NOT_APPLICABLE", "allows_phase_pass": claimed["allows_phase_pass"]})
                    continue
                if task.get("binding") in _BINDING_CODE:
                    code = _BINDING_CODE[task["binding"]]
                    message = task.get("absence_reason") or code
                    blocked_tasks.append({
                        "task_id": task["task_id"], "status": "BLOCKED", "code": code,
                        "message": message, "satisfies_execution": False, "mandatory": True,
                    })
                    task_rows.append({"mandatory": True, "status": "BLOCKED", "allows_phase_pass": False})
                    task_failure = task_failure or {"code": code, "message": message}
                    continue
                if skipped or not present:
                    if task["mandatory"]:
                        task_rows.append({"mandatory": True, "status": "FAILED", "allows_phase_pass": False})
                        task_failure = task_failure or {
                            "code": "NOT_INVOKED",
                            "message": f"mandatory task {task['task_id']} was not invoked",
                        }
                    else:
                        optional_records.append({
                            "task_id": task["task_id"], "status": "NOT_RUN", "mandatory": False, "satisfies_execution": False,
                        })
                        task_rows.append({"mandatory": False, "status": "NOT_RUN", "allows_phase_pass": True})
                    continue
                ctx = {
                    "game_id": game_id, "run_id": run_id, "phase_id": phase["phase_id"],
                    "task_id": task["task_id"], "packet": packet, "now": stamp, "inputs": inputs,
                }
                call, output, failure = _invoke(task, ctx, registry[task["task_id"]], stamp)
                invocations.append(call)
                if output:
                    outputs.append(output)
                    body_warnings = output["body"].get("warnings")
                    if failure is None and isinstance(body_warnings, list):
                        warnings.extend(str(item) for item in body_warnings)
                if failure:
                    if call["status"] == "BLOCKED":
                        blocked_tasks.append({
                            "task_id": task["task_id"], "status": "BLOCKED", "code": failure["code"],
                            "message": failure["message"], "satisfies_execution": False, "mandatory": bool(task["mandatory"]),
                        })
                    if task["mandatory"]:
                        task_failure = task_failure or failure
                    else:
                        optional_records.append({
                            "task_id": task["task_id"], "status": "FAILED", "mandatory": False,
                            "satisfies_execution": False, "failure": failure,
                        })
                task_rows.append({
                    "mandatory": bool(task["mandatory"]),
                    "status": call["status"],
                    "allows_phase_pass": True,
                })
        if provenance_gap and gate == "OK" and not discover_only:
            status = "FAILED"
            task_failure = {"code": "PROVENANCE", "message": "a required input is missing its as-of timestamp or provenance"}
        elif discover_only or gate != "OK":
            status = aggregate_status(gate if not discover_only else "DISCOVERED", task_rows)
        else:
            status = aggregate_status("FRESH", task_rows)
        failure = _phase_failure(status, task_failure, "DISCOVERED" if discover_only else (gate if not provenance_gap else "OK"))
        if status == "NOT_APPLICABLE":
            not_applicable = {
                "policy_id": na_records[0]["policy_id"] if na_records else "",
                "reason": na_records[0]["reason"] if na_records else "",
            }
        else:
            not_applicable = None
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "contract_version": doc["contract_version"],
            "game_id": game_id,
            "phase_id": phase["phase_id"],
            "run_id": run_id,
            "attempt": (prior[-1]["attempt"] + 1) if prior else 1,
            "started_at": stamp,
            "finished_at": stamp,
            "status": status,
            "evidence_class": _evidence_for(status, invocations),
            "code_revision": code_revision,
            "config_hash": cfg,
            "command": _command(game_id, run_id, phase["phase_id"]),
            "entrypoint": "pipeline.execution:run_game",
            "inputs": inputs,
            "prerequisite": {
                "kind": "freshness",
                "evidence_class": evidence,
                "satisfies_execution": False,
                "rows": [] if discover_only else [by_source[s] for s in sources if s in by_source],
            },
            "invocations": invocations,
            "outputs": outputs,
            "validation": {"passed": status == "PASS", "checks": [{"name": "phase_status", "passed": status == "PASS"}]},
            "warnings": warnings,
            "failure": failure,
            "not_applicable": not_applicable,
            "tasks_not_applicable": na_records,
            "optional_tasks": optional_records,
            "blocked_tasks": blocked_tasks,
            "projection_ready": False,
            "research_only": True,
        }
        store.write_new(receipt)
        receipts.append(receipt)
    status = max(receipts, key=lambda item: _RUN_RANK.get(item["status"], 7))["status"] if receipts else "FAILED"
    accepted = bool(receipts) and status == "PASS" and all(item["status"] == "PASS" for item in receipts)
    result = {
        "schema": "nfl83-phase-execution-run/1",
        "contract_version": doc["contract_version"],
        "game_id": game_id,
        "run_id": run_id,
        "status": status,
        "accepted": accepted,
        "projection_ready": False,
        "research_only": True,
        "code_revision": code_revision,
        "config_hash": cfg,
        "phases": receipts,
        "replayed_phases": replayed,
        "refusal_reasons": [
            f"phase {item['phase_id']}: {(item.get('failure') or {}).get('code', item['status'])}"
            for item in receipts if item["status"] != "PASS"
        ],
    }
    return result


def accept_stored_run(store: ReceiptStore, game_id: str, run_id: str, *, code_revision: str, config_hash: str,
                      phases: list[int] | None = None) -> dict:
    """Re-read receipts from disk and fail closed on anything missing, stale, or altered."""
    reasons = []
    for phase_id in list(phases or range(1, 16)):
        attempts = store.attempts(game_id, run_id, phase_id)
        if not attempts:
            reasons.append(f"MISSING: phase {phase_id} receipt")
            continue
        latest = attempts[-1]
        reasons.extend(
            f"phase {phase_id}: {reason}"
            for reason in verify_receipt(latest, game_id=game_id, run_id=run_id,
                                         code_revision=code_revision, config_hash=config_hash)
        )
        if latest.get("status") != "PASS":
            reasons.append(f"phase {phase_id}: status {latest.get('status')} is not PASS")
    return {"accepted": not reasons, "reasons": reasons, "projection_ready": False, "research_only": True}


def summary_text(result: dict) -> str:
    return render_slate(slate_summary([result]))
