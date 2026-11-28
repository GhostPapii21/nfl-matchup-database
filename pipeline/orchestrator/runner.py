"""Fan out registered modules per game and join their real statuses.

Cursor or a local shell runs this. It is not a scheduler and it does not write a
production database, change secrets, or flip projection_ready.

    python -m pipeline.orchestrator --game 2026_12_DEN_PIT --as-of 2026-11-27T16:00:00Z
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .spec import GameCall, ModuleResult, ModuleSpec

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "nfl87-game-run/1"
SLATE_SCHEMA = "nfl87-slate-run/1"
TERMINAL_OK = {"PASS", "NOT_APPLICABLE"}
ANALYTICAL_OK = {"PASS", "PARTIAL"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _canonical(payload) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def _digest(payload) -> str:
    return hashlib.sha256(_canonical(payload).encode()).hexdigest()


def _get(packet: dict, dotted: str):
    cur = packet
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _present(packet: dict, dotted: str) -> bool:
    cur = _get(packet, dotted)
    return cur is not None and cur != [] and cur != {} and cur != ""


def code_revision() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _public_spec(spec: ModuleSpec) -> dict:
    return {
        "module_id": spec.module_id,
        "execution_class": spec.execution_class,
        "depends_on": list(spec.depends_on),
        "critical": spec.critical,
        "timeout_sec": spec.timeout_sec,
        "retries": spec.retries,
        "freshness": list(spec.freshness),
        "inputs": list(spec.inputs),
        "output_contract": spec.output_contract,
        "required_inputs": list(spec.required_inputs),
    }


def registry_fingerprint(registry: list[ModuleSpec]) -> str:
    rows = [_public_spec(spec) for spec in sorted(registry, key=lambda s: s.module_id)]
    return _digest(rows)


def run_identity(game_id: str, as_of: str, revision: str, command: str, fingerprint: str) -> str:
    return _digest({
        "game_id": game_id,
        "as_of": as_of,
        "code_revision": revision,
        "command": command,
        "registry": fingerprint,
    })[:16]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")


def _attempt(n: int, status: str, started: str, finished: str, error: str | None) -> dict:
    return {"n": n, "status": status, "error": error, "started_at": started, "finished_at": finished}


def _missing_inputs(spec: ModuleSpec, packet: dict, game_id: str) -> list[str]:
    missing = []
    for path in spec.required_inputs:
        if not _present(packet, path):
            missing.append(path)
        elif path == "game.game_id" and _get(packet, path) != game_id:
            missing.append(path)
    return missing


def _analytical(spec: ModuleSpec, status: str, output: dict, warnings: list[str]) -> bool:
    if output.get("receipt_only") is True:
        if not any("receipt-only" in w for w in warnings):
            warnings.append("receipt-only result is not analytical execution")
        return False
    if spec.execution_class != "analytical":
        return False
    if status not in ANALYTICAL_OK:
        return False
    return bool(output)


def _invoke(spec: ModuleSpec, call: GameCall) -> tuple[str, dict, list[str], str | None, bool]:
    """Return status, output, warnings, error, retry."""
    holder: dict = {}

    def target() -> None:
        try:
            holder["result"] = spec.fn(call)
        except Exception as exc:  # noqa: BLE001 — the module's real exception is the status
            holder["exc"] = exc

    thread = threading.Thread(target=target, name=f"{call.game_id}:{spec.module_id}:{call.attempt}")
    thread.start()
    thread.join(spec.timeout_sec)
    if thread.is_alive():
        return "TIMEOUT", {}, [], f"timed out after {spec.timeout_sec}s", True
    if "exc" in holder:
        exc = holder["exc"]
        return "FAILED", {}, [], f"{type(exc).__name__}: {exc}", True
    result = holder.get("result")
    if not isinstance(result, ModuleResult):
        return "FAILED", {}, [], f"module returned {type(result).__name__}, not ModuleResult", False
    output = dict(result.output or {})
    warnings = list(result.warnings or [])
    return result.status, output, warnings, None, False


def _execute(spec: ModuleSpec, game_id: str, packet: dict, context: dict, module_dir: Path, as_of: str) -> dict:
    module_dir.mkdir(parents=True, exist_ok=True)
    attempts = []
    status, output, warnings, error = "FAILED", {}, [], "not attempted"
    for n in range(1, spec.retries + 2):
        call = GameCall(
            game_id=game_id,
            packet=copy.deepcopy(packet),
            context=copy.deepcopy(context),
            artifact_dir=module_dir,
            attempt=n,
            module_id=spec.module_id,
            as_of=as_of,
        )
        started = _now()
        status, output, warnings, error, retry = _invoke(spec, call)
        finished = _now()
        record = _attempt(n, status, started, finished, error)
        attempts.append(record)
        _write_json(module_dir / f"attempt-{n:03d}.json", {**record, "output": output, "warnings": warnings})
        if not retry:
            break
    warnings = list(warnings)
    analytical = _analytical(spec, status, output, warnings)
    return _module_row(spec, status, output, warnings, attempts, invoked=True, analytical=analytical)


def _module_row(spec: ModuleSpec, status: str, output: dict, warnings: list, attempts: list, *, invoked: bool, analytical: bool) -> dict:
    return {
        "module_id": spec.module_id,
        "execution_class": spec.execution_class,
        "critical": spec.critical,
        "depends_on": list(spec.depends_on),
        "freshness": list(spec.freshness),
        "timeout_sec": spec.timeout_sec,
        "retries": spec.retries,
        "inputs": list(spec.inputs),
        "output_contract": spec.output_contract,
        "required_inputs": list(spec.required_inputs),
        "status": status,
        "invoked": invoked,
        "analytical_executed": analytical,
        "output": output,
        "warnings": warnings,
        "attempts": attempts,
    }


def _blocked(spec: ModuleSpec, game_id: str, packet: dict) -> dict | None:
    missing = _missing_inputs(spec, packet, game_id)
    if not missing or not spec.critical:
        return None
    reason = "missing critical input: " + ", ".join(missing)
    if "game.game_id" in missing and _present(packet, "game.game_id"):
        reason = f"packet game_id {_get(packet, 'game.game_id')!r} does not match requested {game_id}"
    started = _now()
    return _module_row(
        spec, "FAILED", {"missing": missing, "reason": reason}, [reason],
        [_attempt(1, "FAILED", started, _now(), reason)], invoked=False, analytical=False,
    )


def _skipped(spec: ModuleSpec, dep_id: str, dep_status: str) -> dict:
    reason = f"critical dependency {dep_id} is {dep_status}"
    return _module_row(spec, "SKIPPED", {"reason": reason}, [reason], [], invoked=False, analytical=False)


def _critical_blocker(spec: ModuleSpec, done: dict[str, dict], by_id: dict[str, ModuleSpec]) -> tuple[str, str] | None:
    for dep in spec.depends_on:
        row = done.get(dep)
        if row is None:
            return dep, "MISSING"
        if by_id[dep].critical and row["status"] not in TERMINAL_OK:
            return dep, row["status"]
    return None


def _join_game(game_id: str, rows: list[dict], registry: list[ModuleSpec], *, artifact_dir: str, run_id: str,
               as_of: str, revision: str, command: str) -> dict:
    rows = sorted(rows, key=lambda row: row["module_id"])
    warnings = []
    for row in rows:
        for warning in row["warnings"]:
            text = f"{row['module_id']}: {warning}"
            if text not in warnings:
                warnings.append(text)
        if row["status"] not in TERMINAL_OK and row["attempts"]:
            err = row["attempts"][-1].get("error")
            if err and not any(err in w for w in warnings):
                warnings.append(f"{row['module_id']}: {err}")
    analytical = sorted(row["module_id"] for row in rows if row["analytical_executed"])
    classes = {spec.module_id: spec for spec in registry}
    critical_bad = any(row["critical"] and row["status"] not in TERMINAL_OK for row in rows)
    any_bad = any(row["status"] not in TERMINAL_OK for row in rows)
    analytical_specs = [spec.module_id for spec in registry if spec.execution_class == "analytical"]
    if critical_bad or not rows:
        status = "FAIL_CLOSED"
    elif any_bad or warnings or (analytical_specs and not analytical):
        status = "PARTIAL"
        if analytical_specs and not analytical and not any(w.endswith("no analytical module executed") for w in warnings):
            warnings.append("no analytical module executed")
    else:
        status = "COMPLETE"
    digest_body = {
        "modules": [
            {
                "module_id": row["module_id"],
                "status": row["status"],
                "analytical_executed": row["analytical_executed"],
                "output": row["output"],
                "warnings": row["warnings"],
            }
            for row in rows
        ]
    }
    return {
        "schema": SCHEMA,
        "game_id": game_id,
        "run_id": run_id,
        "as_of": as_of,
        "code_revision": revision,
        "command": command,
        "scheduler": "cursor-local",
        "projection_ready": False,
        "research_only": True,
        "status": status,
        "joined": True,
        "duplicate": False,
        "warnings": warnings,
        "analytical_executed": analytical,
        "not_analytical": sorted(row["module_id"] for row in rows if not row["analytical_executed"]),
        "modules": rows,
        "registry": [_public_spec(classes[row["module_id"]]) for row in rows if row["module_id"] in classes],
        "join_digest": _digest(digest_body),
        "artifact_dir": artifact_dir,
    }


def _closed_game(game_id: str, reason: str, *, as_of: str, revision: str, command: str) -> dict:
    return {
        "schema": SCHEMA,
        "game_id": game_id,
        "run_id": None,
        "as_of": as_of,
        "code_revision": revision,
        "command": command,
        "scheduler": "cursor-local",
        "projection_ready": False,
        "research_only": True,
        "status": "FAIL_CLOSED",
        "joined": True,
        "duplicate": False,
        "warnings": [reason],
        "analytical_executed": [],
        "not_analytical": [],
        "modules": [],
        "registry": [],
        "join_digest": _digest({"game_id": game_id, "reason": reason}),
        "artifact_dir": None,
    }


def _load_packet(game_id: str):
    from pipeline.phases import load_packet

    return load_packet(game_id)


def run_games(games: list[dict], *, registry: list[ModuleSpec], out_dir, as_of: str, code_revision: str,
              command: str) -> dict:
    """Run every game. One game's failure stays in the slate beside the others."""
    out = Path(out_dir)
    by_id = {spec.module_id: spec for spec in registry}
    if len(by_id) != len(registry):
        raise ValueError("module_id values must be unique")
    fingerprint = registry_fingerprint(registry)
    prepared = []
    early = []
    for entry in games:
        game_id = entry["game_id"]
        if "packet" in entry:
            packet = entry["packet"]
        else:
            try:
                packet = _load_packet(game_id)
            except (OSError, ValueError, KeyError) as exc:
                early.append(_closed_game(game_id, f"packet unreadable: {exc}", as_of=as_of, revision=code_revision, command=command))
                continue
        prepared.append({
            "game_id": game_id,
            "packet": packet,
            "context": entry.get("context") if entry.get("context") is not None else {},
            "run_id": run_identity(game_id, as_of, code_revision, command, fingerprint),
        })

    results: dict[str, dict] = {row["game_id"]: row for row in early}
    pending = {item["game_id"]: item for item in prepared}
    for item in prepared:
        art = out / item["game_id"] / item["run_id"]
        manifest_path = art / "manifest.json"
        if manifest_path.is_file():
            stored = json.loads(manifest_path.read_text())
            if stored.get("run_id") == item["run_id"] and stored.get("game_id") == item["game_id"]:
                copied = dict(stored)
                copied["duplicate"] = True
                results[item["game_id"]] = copied
                pending.pop(item["game_id"], None)

    done: dict[str, dict[str, dict]] = {game_id: {} for game_id in pending}
    remaining = {game_id: set(by_id) for game_id in pending}
    while any(remaining.values()):
        tasks = []
        for game_id, left in list(remaining.items()):
            item = pending[game_id]
            ready = [by_id[mid] for mid in left if set(by_id[mid].depends_on) <= set(done[game_id])]
            if not ready and left:
                for mid in sorted(left):
                    done[game_id][mid] = _module_row(
                        by_id[mid], "FAILED", {"reason": "dependency cycle or unknown dependency"},
                        ["dependency cycle or unknown dependency"], [], invoked=False, analytical=False,
                    )
                remaining[game_id] = set()
                continue
            for spec in ready:
                blocker = _critical_blocker(spec, done[game_id], by_id)
                if blocker:
                    done[game_id][spec.module_id] = _skipped(spec, blocker[0], blocker[1])
                    left.remove(spec.module_id)
                    continue
                blocked = _blocked(spec, game_id, item["packet"])
                if blocked is not None:
                    done[game_id][spec.module_id] = blocked
                    left.remove(spec.module_id)
                    continue
                tasks.append((game_id, spec))
                left.remove(spec.module_id)
        if not tasks:
            continue
        workers = max(1, len(tasks))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {}
            for game_id, spec in tasks:
                item = pending[game_id]
                module_dir = out / game_id / item["run_id"] / "modules" / spec.module_id
                futures[pool.submit(_execute, spec, game_id, item["packet"], item["context"], module_dir, as_of)] = (game_id, spec.module_id)
            for future in as_completed(futures):
                game_id, module_id = futures[future]
                try:
                    done[game_id][module_id] = future.result()
                except Exception as exc:  # noqa: BLE001 — one module must not drop the game
                    spec = by_id[module_id]
                    reason = f"{type(exc).__name__}: {exc}"
                    done[game_id][module_id] = _module_row(
                        spec, "FAILED", {"reason": reason}, [reason],
                        [_attempt(1, "FAILED", _now(), _now(), reason)], invoked=False, analytical=False,
                    )

    for game_id, item in pending.items():
        art = (out / game_id / item["run_id"]).resolve()
        manifest = _join_game(
            game_id, list(done[game_id].values()), registry,
            artifact_dir=str(art), run_id=item["run_id"], as_of=as_of, revision=code_revision, command=command,
        )
        _write_json(art / "manifest.json", manifest)
        _write_json(art / "context.json", {"game_id": game_id, "as_of": as_of, "isolated": True})
        results[game_id] = manifest

    ordered = []
    for entry in sorted(games, key=lambda item: item["game_id"]):
        ordered.append(results[entry["game_id"]])
    if any(game["status"] == "FAIL_CLOSED" for game in ordered):
        slate_status = "FAIL_CLOSED"
    elif any(game["status"] == "PARTIAL" for game in ordered):
        slate_status = "PARTIAL"
    else:
        slate_status = "COMPLETE"
    game_ids = [entry["game_id"] for entry in sorted(games, key=lambda item: item["game_id"])]
    slate_id = _digest({
        "games": game_ids, "as_of": as_of, "code_revision": code_revision,
        "command": command, "registry": fingerprint,
    })[:16]
    slate = {
        "schema": SLATE_SCHEMA,
        "slate_id": slate_id,
        "as_of": as_of,
        "code_revision": code_revision,
        "command": command,
        "scheduler": "cursor-local",
        "projection_ready": False,
        "research_only": True,
        "status": slate_status,
        "games": ordered,
    }
    _write_json(out / "slate" / slate_id / "manifest.json", slate)
    return slate


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m pipeline.orchestrator",
        description="Fan out existing NFL modules for one or more games and write a joined manifest. "
                    "Local Cursor execution. Not a scheduler. Research only; projection_ready stays false.",
    )
    parser.add_argument("--game", action="append", required=True, help="game id, repeatable")
    parser.add_argument("--as-of", required=True, help="ISO timestamp stored in the idempotent run id")
    parser.add_argument("--out", default="runs/orchestrator", help="artifact root (default runs/orchestrator)")
    parser.add_argument("--revision", default=None, help="code revision (default git HEAD)")
    args = parser.parse_args(argv)
    revision = args.revision or code_revision()
    raw = list(argv) if argv is not None else sys.argv[1:]
    command = "python -m pipeline.orchestrator " + " ".join(raw)
    from .modules import default_registry

    slate = run_games(
        [{"game_id": game_id} for game_id in args.game],
        registry=default_registry(),
        out_dir=args.out,
        as_of=args.as_of,
        code_revision=revision,
        command=command,
    )
    for game in slate["games"]:
        print(f"{game['game_id']}: {game['status']} analytical={','.join(game['analytical_executed']) or 'none'} "
              f"run_id={game.get('run_id')} warnings={len(game['warnings'])}")
    print(f"slate: {slate['status']} scheduler=cursor-local projection_ready=false")
    return 2 if slate["status"] == "FAIL_CLOSED" else 0
