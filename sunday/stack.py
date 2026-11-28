"""Call the registered Sunday components in one order and write one manifest.

Statuses are EXECUTED, BLOCKED, REFUSED, FAILED, or NOT_REGISTERED.
A status other than EXECUTED is never stored as EXECUTED and never counts as PASS.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from sunday import kickoff

ORDER = (
    "schedule",
    "orchestrator",
    "matchup_research",
    "script_models",
    "player_board",
    "decision",
)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def _sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha_file(path: Path) -> str | None:
    try:
        return _sha_bytes(path.read_bytes())
    except OSError:
        return None


def _dump(path: Path, payload) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, indent=1, sort_keys=True, default=str).encode()
    path.write_bytes(raw + b"\n")
    return _sha_bytes(raw)


def git_state(repo: Path) -> dict:
    def run(*args: str) -> str:
        try:
            return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=5, check=True).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""

    return {"commit": run("rev-parse", "HEAD") or None,
            "dirty": bool(run("status", "--porcelain", "--untracked-files=no"))}


def _row(cid: str, module: str, function: str, kind: str, status: str, reason: str, started: datetime,
         ended: datetime, inputs: list, outputs: list, **extra) -> dict:
    body = {
        "id": cid,
        "module": module,
        "function": function,
        "kind": kind,
        "analytical_execution": kind == "analytical" and status == "EXECUTED",
        "status": status if status in {"EXECUTED", "BLOCKED", "REFUSED", "FAILED", "NOT_REGISTERED"} else "FAILED",
        "reason": reason,
        "started_utc": _iso(started),
        "ended_utc": _iso(ended),
        "duration_seconds": round((ended - started).total_seconds(), 6),
        "inputs": inputs,
        "outputs": outputs,
        "seed": extra.get("seed"),
        "trials": extra.get("trials"),
        "model_identity": extra.get("model_identity"),
        "calibration_status": extra.get("calibration_status"),
    }
    if body["status"] != "EXECUTED":
        body["analytical_execution"] = False
    return body


def _call(module: str, function: str, *args, **kwargs):
    try:
        mod = importlib.import_module(module)
    except ModuleNotFoundError as exc:
        return "NOT_REGISTERED", None, str(exc)
    fn = getattr(mod, function, None)
    if fn is None:
        return "NOT_REGISTERED", None, f"{module}.{function} is absent"
    try:
        return "RETURNED", fn(*args, **kwargs), ""
    except Exception as exc:
        return "FAILED", None, f"{type(exc).__name__}: {exc}"


def _status_from_payload(payload) -> str | None:
    if not isinstance(payload, dict):
        return None
    raw = str(payload.get("status") or payload.get("invocation_status") or "")
    upper = raw.upper()
    if upper in {"BLOCKED", "REFUSED", "FAILED", "NOT_REGISTERED"}:
        return upper
    if "BLOCKED" in upper:
        return "BLOCKED"
    if "REFUSED" in upper:
        return "REFUSED"
    if payload.get("subject_invoked") is False or payload.get("called") is False:
        return "BLOCKED"
    return None


def _stable_research(packet: dict, as_of: datetime) -> dict:
    """Drop wall-clock and thread labels so a repeat run hashes the same research."""
    kept = json.loads(json.dumps(packet, default=str))
    kept["generated_utc"] = _iso(as_of)
    for receipt in kept.get("receipts") or []:
        if isinstance(receipt, dict):
            receipt.pop("elapsed_ms", None)
            receipt.pop("thread", None)
    return kept


def _decision_packet(game: dict, kick: str | None, packet: dict) -> dict:
    """Lines from the pregame packet. No pooled model probability is invented from separate branches."""
    books = packet.get("books") if isinstance(packet.get("books"), dict) else {}
    markets = books.get("markets") if isinstance(books.get("markets"), dict) else {}
    lines = []
    theses = []
    for market in ("spread", "total"):
        block = markets.get(market) if isinstance(markets.get(market), dict) else None
        if not block:
            theses.append({
                "thesis_id": f"team:{market}:missing",
                "subject": "GAME",
                "subject_kind": "team",
                "market": market,
                "side": game.get("home"),
                "line": None,
                "models": [],
                "sample_quality": {"withheld": True, "blocks_reads": True, "limitation": "no line in the packet"},
            })
            continue
        line = block.get("line")
        for book, row in sorted((block.get("books") or {}).items()):
            if not isinstance(row, dict):
                continue
            lines.append({
                "book": book,
                "market": market,
                "side": game.get("home"),
                "line": row.get("line", line),
                "price": (row.get("prices") or {}).get(game.get("home")),
                "timestamp_utc": row.get("last_update") or books.get("retrieved_utc"),
            })
        theses.append({
            "thesis_id": f"team:{market}:{game.get('home')}:{line}",
            "subject": "GAME" if market == "total" else game.get("home"),
            "subject_kind": "team",
            "market": market,
            "side": game.get("home"),
            "line": line,
            "models": [],
            "role_tag": "team_score",
            "script_sensitive": True,
            "evidence_for": [],
            "evidence_against": [{
                "severity": "material",
                "text": "Script branches were retained separately and were not pooled into one probability.",
            }],
            "sample_quality": {
                "withheld": True,
                "blocks_reads": True,
                "limitation": "no single model probability; branches were not averaged",
            },
        })
    return {
        "game_id": game.get("game_id"),
        "home": game.get("home"),
        "away": game.get("away"),
        "kickoff_utc": kick,
        "projection_ready": False,
        "theses": theses,
        "lines": lines,
    }


def run_stack(*, repo: Path, game_id: str, packet: dict | None, out_dir: Path, as_of: datetime,
              command: str, possession_n: int = 24, period_n: int = 400, player_n: int = 400) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    components = []
    game = (packet or {}).get("game") or {}

    started = datetime.now(timezone.utc)
    resolution = kickoff.resolve(repo, game_id, packet)
    ended = datetime.now(timezone.utc)
    res_path = out_dir / "kickoff.json"
    digest = _dump(res_path, resolution)
    components.append(_row(
        "schedule", "sunday.kickoff", "resolve", "identity",
        "EXECUTED" if resolution["resolved"] else "BLOCKED",
        resolution["reason"], started, ended,
        [{"source": name, "kickoff_utc": row.get("kickoff_utc")} for name, row in resolution["originals"].items()],
        [{"path": "kickoff.json", "sha256": digest}],
    ))
    if not resolution["resolved"]:
        return _manifest(repo, game_id, as_of, command, resolution, components, out_dir, blocked=True)

    # Orchestrator. Its own manifest separates analytical calls from freshness checks.
    started = datetime.now(timezone.utc)
    try:
        from pipeline.orchestrator import default_registry, run_games
        payload = run_games(
            [{"game_id": game_id, "packet": packet or {}}],
            registry=default_registry(),
            out_dir=out_dir / "orchestrator",
            as_of=_iso(as_of),
            code_revision=git_state(repo).get("commit") or "",
            command=command,
        )
        state, err = "RETURNED", ""
    except ModuleNotFoundError as exc:
        state, payload, err = "NOT_REGISTERED", None, str(exc)
    except Exception as exc:
        state, payload, err = "FAILED", None, f"{type(exc).__name__}: {exc}"
    ended = datetime.now(timezone.utc)
    orch_status = "NOT_REGISTERED" if state == "NOT_REGISTERED" else ("FAILED" if state == "FAILED" else "EXECUTED")
    if isinstance(payload, dict):
        game_row = next((g for g in payload.get("games") or [] if g.get("game_id") == game_id), {})
        inner = str(game_row.get("status") or "")
        if inner in {"FAIL_CLOSED", "REFUSED"}:
            orch_status = "REFUSED"
        summary = [{"module_id": m.get("module_id"), "status": m.get("status"),
                    "analytical_execution": m.get("analytical_execution")} for m in game_row.get("modules") or []]
    else:
        summary = []
    components.append(_row(
        "orchestrator", "pipeline.orchestrator.runner", "run_games", "orchestration",
        orch_status, err or "existing modules joined in module-id order", started, ended,
        [{"game_id": game_id, "as_of": _iso(as_of)}],
        [{"path": "orchestrator", "module_statuses": summary}],
    ))

    started = datetime.now(timezone.utc)
    state, research, err = _call("pipeline.matchup_research.build", "build_packet", game_id, root=repo, workers=4)
    ended = datetime.now(timezone.utc)
    outputs = []
    mstatus = "NOT_REGISTERED" if state == "NOT_REGISTERED" else ("FAILED" if state == "FAILED" else "EXECUTED")
    if isinstance(research, dict):
        forced = _status_from_payload(research)
        if forced:
            mstatus = forced
        research = _stable_research(research, as_of)
        outputs.append({"path": "matchup_research.json", "sha256": _dump(out_dir / "matchup_research.json", research)})
    components.append(_row(
        "matchup_research", "pipeline.matchup_research.build", "build_packet", "analytical",
        mstatus, err or "prior-week matchup packet", started, ended,
        [{"game_id": game_id}], outputs,
    ))

    started = datetime.now(timezone.utc)
    script_dir = out_dir / "script_models"
    state, script, err = _call(
        "sunday.script_models", "run_historical_replay",
        packet or {"game": game}, script_dir, root=repo, possession_n=possession_n, period_n=period_n,
    )
    ended = datetime.now(timezone.utc)
    sstatus = "NOT_REGISTERED" if state == "NOT_REGISTERED" else ("FAILED" if state == "FAILED" else "EXECUTED")
    trials = seed = calibration = identity = None
    if isinstance(script, dict):
        forced = _status_from_payload(script)
        if forced:
            sstatus = forced
        models = script.get("models") or []
        identity = ",".join(str(m) for m in models) if models and isinstance(models[0], str) else None
        if script.get("sim_v6_three_method_claimed"):
            sstatus = "FAILED"
            err = "script_models claimed the absent sim_v6 triad"
    manifest_path = script_dir / "manifest.json"
    outputs = [{"path": "script_models/manifest.json", "sha256": _sha_file(manifest_path)}] if manifest_path.is_file() else []
    components.append(_row(
        "script_models", "sunday.script_models", "run_historical_replay", "analytical",
        sstatus, err or "each engine and branch kept its own record", started, ended,
        [{"possession_n": possession_n, "period_n": period_n}], outputs,
        trials=trials, seed=seed, model_identity=identity, calibration_status=calibration,
    ))

    started = datetime.now(timezone.utc)
    state, board, err = _call("sunday.player_board", "from_packet", packet or {}, n=player_n, seed=89)
    ended = datetime.now(timezone.utc)
    bstatus = "NOT_REGISTERED" if state == "NOT_REGISTERED" else ("FAILED" if state == "FAILED" else "EXECUTED")
    outputs = []
    if isinstance(board, dict):
        forced = _status_from_payload(board)
        if forced:
            bstatus = forced
        outputs.append({"path": "player_board.json", "sha256": _dump(out_dir / "player_board.json", board)})
    components.append(_row(
        "player_board", "sunday.player_board", "from_packet", "analytical",
        bstatus, err or "volume kept separate from efficiency", started, ended,
        [{"n": player_n, "seed": 89}], outputs, trials=player_n, seed=89,
    ))

    started = datetime.now(timezone.utc)
    decision_input = _decision_packet(game, resolution["canonical_kickoff_utc"], packet or {})
    state, decision, err = _call("sunday.decision.board", "build_board", decision_input)
    ended = datetime.now(timezone.utc)
    dstatus = "NOT_REGISTERED" if state == "NOT_REGISTERED" else ("FAILED" if state == "FAILED" else "EXECUTED")
    outputs = []
    if isinstance(decision, dict):
        if decision.get("projection_ready") is not False:
            dstatus = "FAILED"
            err = "decision board set projection_ready true"
        else:
            outputs.append({"path": "decision_board.json", "sha256": _dump(out_dir / "decision_board.json", decision)})
            from sunday.decision.report import render_markdown
            text = render_markdown(decision)
            (out_dir / "decision_board.md").write_text(text)
            outputs.append({"path": "decision_board.md", "sha256": _sha_bytes(text.encode())})
    components.append(_row(
        "decision", "sunday.decision.board", "build_board", "analytical",
        dstatus, err or "red team consumed joined lines; empty sections stay empty", started, ended,
        [{"theses": len(decision_input["theses"]), "lines": len(decision_input["lines"])}], outputs,
    ))
    return _manifest(repo, game_id, as_of, command, resolution, components, out_dir, blocked=False)


def _manifest(repo, game_id, as_of, command, resolution, components, out_dir, blocked: bool) -> dict:
    counts = {}
    for row in components:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    if blocked or any(row["status"] == "BLOCKED" and row["id"] == "schedule" for row in components):
        result = "BLOCKED"
    elif any(row["status"] != "EXECUTED" for row in components):
        result = "PARTIAL"
    else:
        result = "PASS"
    git = git_state(repo)
    packet_path = repo / "pregame" / "packets" / game_id / "packet.json"
    body = {
        "schema": "sunday-canonical-manifest/1",
        "projection_ready": False,
        "research_only": True,
        "result": result,
        "run_id": hashlib.sha256(f"{game_id}|{_iso(as_of)}|{command}|{git.get('commit')}".encode()).hexdigest()[:16],
        "command": command,
        "git": git,
        "game_id": game_id,
        "as_of_utc": _iso(as_of),
        "kickoff": {
            "source": resolution.get("source"),
            "kickoff_utc": resolution.get("canonical_kickoff_utc"),
            "timezone": "UTC",
            "originals": resolution.get("originals"),
            "conflicts": resolution.get("conflicts"),
            "config_file_rewritten": False,
        },
        "hashes": {
            "packet": _sha_file(packet_path),
            "nflverse_games_csv": _sha_file(repo / "data" / "historical" / "nflverse" / "games.csv"),
        },
        "components": components,
        "component_order": list(ORDER),
        "counts": counts,
        "pass_requires_every_component_executed": True,
    }
    _dump(out_dir / "manifest.json", body)
    return body


def stable_components(manifest: dict) -> list:
    """Drop wall-clock fields so two runs can be compared."""
    kept = []
    for row in manifest.get("components") or []:
        kept.append({k: v for k, v in row.items() if k not in {"started_utc", "ended_utc", "duration_seconds"}})
    return kept
