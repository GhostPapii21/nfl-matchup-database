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
    "sim_v6",
    "replacement_triad",
    "ngs_verify",
    "td_outputs",
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
        "status": status if status in {"EXECUTED", "BLOCKED", "REFUSED", "FAILED", "NOT_REGISTERED", "MISSING", "TIMEOUT"} else "FAILED",
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
    schedule_status = "EXECUTED" if resolution.get("verification") == "VERIFIED" else "BLOCKED"
    components.append(_row(
        "schedule", "sunday.kickoff", "resolve", "identity",
        schedule_status,
        resolution["reason"], started, ended,
        [{"source": name, "kickoff_utc": row.get("kickoff_utc")} for name, row in resolution["originals"].items()],
        [{"path": "kickoff.json", "sha256": digest}],
    ))

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
        summary = list(game_row.get("modules") or [])
    else:
        summary = []
    components.append(_row(
        "orchestrator", "pipeline.orchestrator.runner", "run_games", "orchestration",
        orch_status, err or "existing modules joined in module-id order", started, ended,
        [{"game_id": game_id, "as_of": _iso(as_of)}],
        [{"path": "orchestrator"}],
    ))
    components.extend(_child_rows(summary))

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
    script_sha = _sha_file(manifest_path) if manifest_path.is_file() else None
    outputs = [{"path": "script_models/manifest.json", "sha256": script_sha}] if script_sha else []
    components.append(_row(
        "script_models", "sunday.script_models", "run_historical_replay", "analytical",
        sstatus, err or "each engine and branch kept its own record", started, ended,
        [{"possession_n": possession_n, "period_n": period_n, "acceptance_100k": False}], outputs,
        trials=trials, seed=seed, model_identity=identity, calibration_status=calibration,
    ))

    started = datetime.now(timezone.utc)
    from tools.sim_v6 import acceptance_receipt
    sim_receipt = acceptance_receipt()
    sim_sha = _dump(out_dir / "sim_v6_receipt.json", sim_receipt)
    ended = datetime.now(timezone.utc)
    components.append(_row(
        "sim_v6", "tools.sim_v6", "acceptance_receipt", "analytical",
        "REFUSED", sim_receipt["reason"], started, ended,
        [{"cells": sim_receipt["cells_required"], "trials_required": sim_receipt["trials_required"],
          "trials_executed": sim_receipt["trials_executed"], "fallback_used": False}],
        [{"path": "sim_v6_receipt.json", "sha256": sim_sha}],
        trials=0, calibration_status=sim_receipt["bias"]["calibration_status"],
    ))

    started = datetime.now(timezone.utc)
    from sunday.replacement_triad import receipt as triad_receipt
    season = int(game.get("season") or 0)
    week = int(game.get("week") or 0)
    triad = triad_receipt(repo, season=season, week=week)
    triad_sha = _dump(out_dir / "replacement_triad.json", triad)
    ended = datetime.now(timezone.utc)
    empirical = next(row for row in triad["methods"] if row.get("identity") == "nflverse_games_bootstrap")
    triad_status = "REFUSED"
    triad_reason = (
        f"empirical bootstrap trials {empirical.get('trials_executed')}; "
        "period and possession 100k script cells were not started and were not labeled sim_v6"
    )
    components.append(_row(
        "replacement_triad", "sunday.replacement_triad", "receipt", "analytical",
        triad_status, triad_reason, started, ended,
        [{"not_sim_v6": True, "empirical_trials": empirical.get("trials_executed")}],
        [{"path": "replacement_triad.json", "sha256": triad_sha}],
        trials=empirical.get("trials_executed"),
    ))

    started = datetime.now(timezone.utc)
    from sunday.ngs_verify import verify as verify_ngs
    ngs = verify_ngs(repo)
    ngs_sha = _dump(out_dir / "ngs_verify.json", ngs)
    ended = datetime.now(timezone.utc)
    components.append(_row(
        "ngs_verify", "sunday.ngs_verify", "verify", "check",
        "REFUSED", ngs["reason"], started, ended,
        [{"week_12": ngs["week_12"]}],
        [{"path": "ngs_verify.json", "sha256": ngs_sha}],
    ))

    started = datetime.now(timezone.utc)
    from sunday.td_outputs import collect as collect_td
    td = collect_td(script_dir)
    td_sha = _dump(out_dir / "td_outputs.json", td)
    ended = datetime.now(timezone.utc)
    td_status = "EXECUTED" if td["rows"] else "BLOCKED"
    components.append(_row(
        "td_outputs", "sunday.td_outputs", "collect", "analytical",
        td_status,
        f"pass_td rows {td['players_with_pass_td']}; rush_td rows {td['players_with_rush_td']}",
        started, ended,
        [{"pooled": False, "acceptance_100k": False}],
        [{"path": "td_outputs.json", "sha256": td_sha}],
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
        player_sha = _dump(out_dir / "player_board.json", board)
        outputs.append({"path": "player_board.json", "sha256": player_sha})
    else:
        player_sha = None
    components.append(_row(
        "player_board", "sunday.player_board", "from_packet", "analytical",
        bstatus, err or "volume kept separate from efficiency", started, ended,
        [{"n": player_n, "seed": 89}], outputs, trials=player_n, seed=89,
    ))

    started = datetime.now(timezone.utc)
    from sunday.joinflow import build_joined_decision_input, hashes_match
    research_row = next(row for row in components if row["id"] == "matchup_research")
    research_sha = next((item.get("sha256") for item in research_row["outputs"] if item.get("sha256")), None)
    recorded = {"research": research_sha, "script": script_sha, "player_board": player_sha}
    on_disk = {
        "research": _sha_file(out_dir / "matchup_research.json"),
        "script": _sha_file(script_dir / "manifest.json"),
        "player_board": _sha_file(out_dir / "player_board.json"),
    }
    base = _decision_packet(game, resolution.get("canonical_kickoff_utc"), packet or {})
    decision_input = build_joined_decision_input(
        game=game,
        kickoff_utc=resolution.get("canonical_kickoff_utc"),
        kickoff_verification=resolution.get("verification"),
        as_of=as_of,
        research=research if isinstance(research, dict) else None,
        script=script if isinstance(script, dict) else None,
        players=board if isinstance(board, dict) else None,
        market_packet=packet or {},
        hashes=recorded,
        base_packet=base,
    )
    if not hashes_match(recorded, on_disk):
        decision_input["joined"]["problems"].append("artifact hash does not match the file on disk")
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
    join_problems = decision_input["joined"]["problems"]
    if join_problems and dstatus == "EXECUTED":
        dstatus = "REFUSED"
        err = "; ".join(join_problems)
    components.append(_row(
        "decision", "sunday.decision.board", "build_board", "analytical",
        dstatus, err or "red team consumed the joined research, script, player, and market rows", started, ended,
        [{"theses": len(decision_input["theses"]), "lines": len(decision_input["lines"])}], outputs,
    ))
    return _manifest(repo, game_id, as_of, command, resolution, components, out_dir, blocked=False)


_BLOCKING = {"BLOCKED", "REFUSED", "FAILED", "NOT_REGISTERED", "MISSING", "TIMEOUT"}
_CHECK_CLASSES = {"freshness", "gate", "stub", "adapter"}


def _child_status(raw: str) -> str:
    upper = str(raw or "").upper()
    if upper in {"PASS", "PARTIAL"}:
        return "EXECUTED"
    if upper == "REFUSED" or upper == "FAIL_CLOSED":
        return "REFUSED"
    if upper in {"BLOCKED", "MISSING", "FAILED", "TIMEOUT", "NOT_REGISTERED"}:
        return upper
    return "FAILED"


def _child_rows(modules: list[dict]) -> list[dict]:
    """One manifest row per orchestrator child. The parent EXECUTED row does not cover these."""
    rows = []
    now = datetime.now(timezone.utc)
    for module in modules:
        if not isinstance(module, dict):
            continue
        execution_class = str(module.get("execution_class") or "")
        raw = str(module.get("status") or "")
        status = _child_status(raw)
        analytical = execution_class == "analytical" and status == "EXECUTED" and module.get("analytical_executed") is True
        kind = "check" if execution_class in _CHECK_CLASSES or execution_class != "analytical" else "analytical"
        if execution_class in {"freshness", "gate"}:
            kind = "check"
            analytical = False
        reason = raw if status == "EXECUTED" else f"orchestrator child status {raw}"
        row = _row(
            f"orchestrator.{module.get('module_id')}",
            "pipeline.orchestrator.modules",
            str(module.get("module_id") or ""),
            kind, status, reason, now, now, [], [],
        )
        row["analytical_execution"] = analytical
        row["orchestrator_status"] = raw
        row["execution_class"] = execution_class or None
        rows.append(row)
    return rows


def acceptance_result(components: list[dict]) -> str:
    """PASS only when identity is verified and no child is blocked, refused, missing, or failed.

    A freshness or ledger row may be EXECUTED with orchestrator_status PARTIAL. That row is a
    check, not analytical execution, and it is not a PASS by itself.
    """
    if any(row.get("id") == "schedule" and row.get("status") != "EXECUTED" for row in components):
        return "BLOCKED"
    if any(row.get("status") in _BLOCKING for row in components):
        return "PARTIAL"
    if any(row.get("kind") == "analytical" and row.get("status") != "EXECUTED" for row in components):
        return "PARTIAL"
    return "PASS"


def _manifest(repo, game_id, as_of, command, resolution, components, out_dir, blocked: bool) -> dict:
    counts = {}
    for row in components:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    result = "BLOCKED" if blocked else acceptance_result(components)
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
            "authoritative_source": resolution.get("authoritative_source"),
            "authoritative_status": resolution.get("authoritative_status"),
            "verification": resolution.get("verification"),
            "pregame_capture": resolution.get("pregame_capture"),
            "capture_before_this_kickoff": resolution.get("capture_before_this_kickoff"),
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
