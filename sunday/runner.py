"""Run one game, or many games, without letting one failure erase the others."""
from __future__ import annotations

import multiprocessing
import traceback
import uuid
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from sunday.assemble import manifest as build_manifest
from sunday.assemble import refusal_manifest, render_report
from sunday.components import PARALLEL
from sunday.context import build_context
from sunday.jsonutil import sha256_obj, write_json
from sunday.preflight import critical_preflight


def _invoke(name: str, entrypoint: str, fn, ctx: dict) -> dict:
    started = datetime.now(timezone.utc)
    t0 = started.timestamp()
    error = None
    try:
        output = fn(ctx)
        status = output.get("status", "OK") if isinstance(output, dict) else "OK"
        ran = bool(output.get("ran")) if isinstance(output, dict) else False
        error = output.get("error") if isinstance(output, dict) else None
    except Exception as exc:  # one component must not kill the game
        output = {}
        status = "FAILED"
        ran = False
        error = f"{type(exc).__name__}: {exc}"
        output["traceback"] = traceback.format_exc(limit=8)
    try:
        digest = sha256_obj(output)
    except TypeError as exc:
        output = {"status": "FAILED", "ran": False, "error": f"output not serializable: {exc}"}
        digest = sha256_obj(output)
        status, ran, error = "FAILED", False, output["error"]
    finished = datetime.now(timezone.utc)
    return {
        "component": name,
        "status": status,
        "ran": ran,
        "entrypoint": entrypoint,
        "started_utc": started.isoformat(timespec="seconds"),
        "finished_utc": finished.isoformat(timespec="seconds"),
        "duration_sec": round(finished.timestamp() - t0, 3),
        "error": error,
        "output_sha256": digest,
        "output": output,
    }


def _fanout(ctx: dict, threads: int) -> dict:
    receipts = {}
    workers = max(1, int(threads or 1))
    if workers == 1:
        for name, entry, fn in PARALLEL:
            receipts[name] = _invoke(name, entry, fn, ctx)
        return receipts
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_invoke, name, entry, fn, ctx): name
            for name, entry, fn in PARALLEL
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                receipts[name] = future.result()
            except Exception as exc:  # the wrapper already catches; this is a pool failure
                receipts[name] = {
                    "component": name, "status": "FAILED", "ran": False, "error": f"{type(exc).__name__}: {exc}",
                    "entrypoint": name, "output": {}, "output_sha256": None, "duration_sec": None,
                }
    return receipts


def _attach_gaps(pre: dict, receipts: dict) -> dict:
    gaps = list(pre.get("noncritical_so_far") or [])
    freshness = ((receipts.get("phase_ledger") or {}).get("output") or {}).get("freshness") or []
    for row in freshness:
        if row.get("status") not in ("FRESH", "NOT_REQUIRED"):
            gaps.append({
                "item": row.get("source"),
                "severity": "noncritical",
                "detail": f"{row.get('status')}: {row.get('reason')}",
            })
    roster = (receipts.get("engine_roster") or {}).get("output") or {}
    sim_v6 = roster.get("documented_sim_v6") or {}
    if not sim_v6.get("ran"):
        gaps.append({"item": "documented_sim_v6", "severity": "noncritical", "detail": sim_v6.get("reason")})
    if not (roster.get("lightning") or {}).get("ran"):
        gaps.append({"item": "lightning", "severity": "noncritical",
                     "detail": (roster.get("lightning") or {}).get("reason")})
    pre = dict(pre)
    pre["noncritical_gaps"] = gaps
    return pre


def _run_id(ctx: dict) -> str:
    spec = ctx.get("spec") or {}
    if spec.get("run_id"):
        return str(spec["run_id"])
    stamp = ctx["as_of"].strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}_{ctx['game_id']}_{uuid.uuid4().hex[:8]}"


def _out_dir(ctx: dict, run_id: str) -> Path:
    base = Path((ctx.get("spec") or {}).get("out") or (ctx["root"] / "sunday_runs" / run_id))
    return base / ctx["game_id"]


def execute_game(spec: dict) -> dict:
    """Run one game in isolation. Exceptions become a FAILED result for this game only."""
    ctx = build_context(spec)
    run_id = _run_id(ctx)
    out = _out_dir(ctx, run_id)
    pre = critical_preflight(ctx)
    if not pre["ok"]:
        body = refusal_manifest(ctx, pre, run_id)
        write_json(out / "manifest.json", body)
        (out / "report.md").write_text(render_report(body))
        return {
            "game_id": ctx["game_id"], "status": "REFUSED", "exit": 2, "run_id": run_id,
            "manifest": str(out / "manifest.json"), "critical": pre["critical"],
        }
    receipts = _fanout(ctx, int(spec.get("threads") or 4))
    pre = _attach_gaps(pre, receipts)
    for name, receipt in receipts.items():
        write_json(out / "components" / f"{name}.json", receipt)
    body = build_manifest(ctx, pre, receipts, run_id)
    write_json(out / "manifest.json", body)
    (out / "report.md").write_text(render_report(body))
    exit_code = 0 if body["status"] == "COMPLETE" else 2
    return {
        "game_id": ctx["game_id"], "status": body["status"], "exit": exit_code, "run_id": run_id,
        "manifest": str(out / "manifest.json"),
        "projection_ready": body["projection_ready"],
    }


def _guard(worker, spec: dict) -> dict:
    try:
        return worker(spec)
    except Exception as exc:
        return {
            "game_id": spec.get("game_id"),
            "status": "FAILED",
            "exit": 2,
            "error": f"{type(exc).__name__}: {exc}",
        }


def run_isolated(specs: list[dict], worker=execute_game, max_workers: int = 1) -> list[dict]:
    """Each spec is a separate game. A failed worker still leaves the other results in the list."""
    if not specs:
        return []
    if max_workers <= 1 or len(specs) < 2 or worker is not execute_game:
        return [_guard(worker, spec) for spec in specs]
    results = []
    # spawn: the parent may already have run threaded component fan-out, and fork after threads can deadlock.
    with ProcessPoolExecutor(max_workers=max_workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        futures = {pool.submit(execute_game, spec): spec for spec in specs}
        for future in as_completed(futures):
            spec = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({
                    "game_id": spec.get("game_id"),
                    "status": "FAILED",
                    "exit": 2,
                    "error": f"{type(exc).__name__}: {exc}",
                })
    return results


def preflight_only(spec: dict) -> dict:
    """Critical checks plus the real ledger and 100k preflight. No simulator."""
    from sunday.components import phase_ledger, sim100k_preflight

    ctx = build_context(spec)
    pre = critical_preflight(ctx)
    gaps = list(pre.get("noncritical_so_far") or [])
    phase_summary = None
    gate = None
    if ctx.get("packet") is not None and pre["ok"]:
        try:
            led = phase_ledger(ctx)
            phase_summary = led.get("summary")
            for row in led.get("freshness") or []:
                if row.get("status") not in ("FRESH", "NOT_REQUIRED"):
                    gaps.append({"item": row.get("source"), "severity": "noncritical",
                                 "detail": f"{row.get('status')}: {row.get('reason')}"})
        except Exception as exc:
            gaps.append({"item": "phase_ledger", "severity": "noncritical", "detail": f"{type(exc).__name__}: {exc}"})
        try:
            gate = sim100k_preflight(ctx)
        except Exception as exc:
            gate = {"status": "FAILED", "ran": False, "error": f"{type(exc).__name__}: {exc}"}
    return {
        "game_id": ctx["game_id"],
        "ok": pre["ok"],
        "exit": 0 if pre["ok"] else 2,
        "critical": pre["critical"],
        "noncritical_gaps": gaps,
        "leakage": pre.get("leakage"),
        "phase_summary": phase_summary,
        "sim100k_preflight": gate,
        "projection_ready": False,
        "as_of": None if ctx.get("as_of") is None else ctx["as_of"].isoformat(),
        "kickoff_utc": None if ctx.get("kickoff_utc") is None else ctx["kickoff_utc"].isoformat(),
    }
