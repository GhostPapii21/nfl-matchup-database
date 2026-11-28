"""Run one game or a bounded slate. One game's failure is written and does not cancel the others."""
from __future__ import annotations

import json
import resource
import sys
import threading
import time
import tracemalloc
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from sunday import discover, preflight, report

CAP = 8


def bounded_workers(requested: int | None, n_games: int) -> tuple[int, int]:
    if requested is not None and requested < 1:
        raise ValueError("concurrency must be at least 1")
    req = 4 if requested is None else requested
    used = max(1, min(req, CAP, max(1, n_games)))
    return used, CAP


def rss_kb() -> int:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        rss //= 1024
    return int(rss)


class Flight:
    def __init__(self):
        self.n = 0
        self.peak = 0
        self._lock = threading.Lock()

    def __enter__(self):
        with self._lock:
            self.n += 1
            self.peak = max(self.peak, self.n)
        return self

    def __exit__(self, *exc):
        with self._lock:
            self.n -= 1
        return False


def _dump(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _read_packet(path: Path) -> tuple[dict | None, str | None, str | None]:
    try:
        raw = path.read_bytes()
    except OSError as e:
        return None, None, str(e)
    digest = preflight.sha256_bytes(raw)
    try:
        return json.loads(raw.decode()), digest, None
    except (UnicodeError, ValueError) as e:
        return None, digest, f"{path.name}: {e}"


def _memory(measure: bool, started: bool) -> dict:
    if measure and started:
        current, peak = tracemalloc.get_traced_memory()
        return {"tracemalloc_current_bytes": current, "tracemalloc_peak_bytes": peak,
                "process_max_rss_kb": rss_kb(),
                "detail": f"tracemalloc peak {peak} bytes; process max RSS {rss_kb()} KB"}
    return {"process_max_rss_kb": rss_kb(),
            "detail": "Per-game tracemalloc is off during fan-out. The slate index records process max RSS."}


def _write_game(out_dir: Path, packet: dict) -> dict:
    public = {k: v for k, v in packet.items() if k != "_disk_free_bytes"}
    runtime = public.get("runtime") or {}
    pre = {
        "schema": "sunday-preflight/1",
        "projection_ready": False,
        "research_only": True,
        "game_id": public.get("game_id"),
        "result": public.get("result"),
        "as_of_utc": public.get("as_of_utc"),
        "kickoff_utc": public.get("kickoff_utc"),
        "canonical_sha256": public.get("canonical_sha256"),
        "critical_ids": public.get("critical_ids"),
        "required_ids": public.get("required_ids"),
        "layer_gaps": public.get("layer_gaps"),
        "checks": public.get("checks"),
        "leakage": public.get("leakage"),
        "command": public.get("command"),
    }
    _dump(out_dir / "preflight.json", pre)
    _dump(out_dir / "packet.json", public)
    (out_dir / "report.md").write_text(report.render_game(public), encoding="utf-8")
    public["artifacts"] = {"preflight": "preflight.json", "packet": "packet.json", "report": "report.md"}
    public["runtime"] = runtime
    return public


def run_game(*, repo: Path, game_id: str, out_dir: Path, as_of: datetime, market: bool = False,
             min_free_mb: int = 64, entry: dict | None = None, measure_memory: bool = True,
             command: str | None = None, invoke_stack: bool = False, possession_n: int = 24,
             period_n: int = 400, player_n: int = 400) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    started = False
    if measure_memory:
        tracemalloc.start()
        started = True
    t0 = time.perf_counter()
    try:
        path = discover.packet_path(repo, game_id, entry)
        if path is None:
            pk, digest, load_error = None, None, "packet path is missing or leaves the repository"
            packet_rel = None
        else:
            pk, digest, load_error = _read_packet(path)
            try:
                packet_rel = str(path.resolve().relative_to(repo.resolve()))
            except ValueError:
                packet_rel = None
                pk, digest, load_error = None, None, "packet path leaves the repository"
        cmd = command or (
            f"python -m sunday game --game {game_id} --as-of {preflight.iso(as_of)}"
            + (" --market" if market else ""))
        packet = preflight.evaluate(
            repo=repo, game_id=game_id, pk=pk, packet_sha=digest, packet_rel=packet_rel,
            load_error=load_error, entry=entry, as_of=as_of, market=market, out_dir=out_dir,
            min_free_mb=min_free_mb, command=cmd)
        free = packet.pop("_disk_free_bytes", None)
        if invoke_stack and pk is not None:
            from sunday.stack import run_stack
            manifest = run_stack(repo=repo, game_id=game_id, packet=pk, out_dir=out_dir, as_of=as_of,
                                 command=cmd, possession_n=possession_n, period_n=period_n, player_n=player_n)
            packet["canonical_manifest"] = "manifest.json"
            if manifest.get("result") == "BLOCKED":
                packet["result"] = "BLOCKED"
            elif manifest.get("result") != "PASS" and packet.get("result") == "PASS":
                packet["result"] = "PARTIAL"
            packet["component_counts"] = manifest.get("counts")
        packet["runtime"] = {"wall_seconds": round(time.perf_counter() - t0, 6), "memory": _memory(measure_memory, started),
                             "disk_free_bytes": free}
        return _write_game(out_dir, packet)
    except Exception as e:
        fail = preflight.with_hash({
            "schema": "sunday-projection/1", "projection_ready": False, "research_only": True,
            "result": "BLOCKED", "game_id": game_id, "as_of_utc": preflight.iso(as_of),
            "command": command or f"python -m sunday game --game {game_id}",
            "critical_ids": ["runner"], "required_ids": [], "layer_gaps": [],
            "checks": [preflight.check("runner", "critical", "FAIL", repr(e))],
            "leakage": {"status": "FAIL", "late_stamps": [], "excluded": [], "inputs_read": []},
            "layers": [], "roles": {}, "freshness": [], "cited_outputs": {},
            "git_sha": preflight.git_sha(),
        })
        fail["runtime"] = {"wall_seconds": round(time.perf_counter() - t0, 6), "memory": _memory(measure_memory, started)}
        return _write_game(out_dir, fail)
    finally:
        if started:
            tracemalloc.stop()


def _guard(fn, kwargs, flight: Flight) -> dict:
    with flight:
        try:
            return fn(**kwargs)
        except Exception as e:
            return {"game_id": kwargs.get("game_id"), "result": "BLOCKED", "projection_ready": False,
                    "canonical_sha256": None, "critical_ids": ["runner"], "artifacts": {}, "error": repr(e)}


def run_slate(games: list[dict], *, repo: Path, out: Path, as_of: datetime, market: bool = False,
              min_free_mb: int = 64, concurrency: int | None = None, runner=None, command: str | None = None,
              possession_n: int = 24, period_n: int = 400, player_n: int = 400) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    used, cap = bounded_workers(concurrency, len(games))
    fn = runner or run_game
    flight = Flight()
    jobs = []
    for entry in games:
        gid = entry.get("game_id")
        jobs.append(dict(repo=repo, game_id=gid, out_dir=out / str(gid), as_of=as_of, market=market,
                         min_free_mb=min_free_mb, entry=entry, measure_memory=False, invoke_stack=True,
                         possession_n=possession_n, period_n=period_n, player_n=player_n))
    with ThreadPoolExecutor(max_workers=used) as pool:
        futures = [pool.submit(_guard, fn, job, flight) for job in jobs]
        done = [future.result() for future in futures]
    counts = {"PASS": 0, "PARTIAL": 0, "BLOCKED": 0}
    rows = []
    for entry, packet in zip(games, done):
        result = packet.get("result") if packet.get("result") in counts else "BLOCKED"
        counts[result] += 1
        rows.append({"game_id": entry.get("game_id"), "date": entry.get("date"), "kickoff_et": entry.get("kickoff_et"),
                     "result": result, "report_rel": f"{entry.get('game_id')}/report.md",
                     "canonical_sha256": packet.get("canonical_sha256"),
                     "critical_ids": packet.get("critical_ids"), "required_ids": packet.get("required_ids"),
                     "wall_seconds": (packet.get("runtime") or {}).get("wall_seconds"),
                     "component_counts": packet.get("component_counts")})
    if counts["BLOCKED"]:
        result = "BLOCKED"
    elif counts["PARTIAL"]:
        result = "PARTIAL"
    else:
        result = "PASS"
    slate = {
        "schema": "sunday-slate/1",
        "projection_ready": False,
        "research_only": True,
        "result": result,
        "as_of_utc": preflight.iso(as_of),
        "command": command or (f"python -m sunday slate --as-of {preflight.iso(as_of)}" + (" --market" if market else "")),
        "concurrency_requested": concurrency if concurrency is not None else 4,
        "concurrency_used": used,
        "concurrency_cap": cap,
        "peak_in_flight": flight.peak,
        "process_max_rss_kb": rss_kb(),
        "counts": counts,
        "games": rows,
        "git_sha": preflight.git_sha(),
    }
    preflight_index = dict(slate)
    (out / "INDEX.md").write_text(report.render_index(slate), encoding="utf-8")
    _dump(out / "index.json", preflight_index)
    return slate


def exit_code(result: str) -> int:
    if result == "BLOCKED":
        return 2
    return 0


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)
