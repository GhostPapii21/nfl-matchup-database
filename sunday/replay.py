"""Run one historical game twice at the packet's own generated time and compare the canonical hash."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline import freshness
from sunday import discover, execute, preflight, report


def as_of_for(pk: dict | None, override: datetime | None) -> tuple[datetime | None, str | None]:
    if override is not None:
        return override, None
    if not pk:
        return None, "packet could not be read, so the replay has no pregame as-of"
    generated = freshness.parse_utc(pk.get("generated_utc"))
    if generated is None:
        return None, "packet has no generated_utc"
    return generated.astimezone(timezone.utc).replace(microsecond=0), None


def run_replay(*, repo: Path, game_id: str, out: Path, as_of: datetime | None = None, market: bool = False,
               min_free_mb: int = 64) -> dict:
    games, err = discover.load_index(repo)
    entry = None
    if games is not None:
        entry = next((g for g in games if g.get("game_id") == game_id), None)
    path = discover.packet_path(repo, game_id, entry)
    if path is None:
        pk, load_error = None, "packet path is missing or leaves the repository"
    else:
        pk, _digest, load_error = execute._read_packet(path)
    when, why = as_of_for(pk, as_of)
    out.mkdir(parents=True, exist_ok=True)
    if when is None or err:
        detail = err or why or load_error or "replay could not start"
        record = {"schema": "sunday-replay/1", "projection_ready": False, "research_only": True,
                  "game_id": game_id, "result": "BLOCKED", "reproducibility": "FAIL", "detail": detail,
                  "leakage": {"status": "FAIL"}}
        (out / "replay.json").write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
        (out / "replay.md").write_text(report.render_replay(record))
        return record
    command = f"python -m sunday replay --game {game_id} --as-of {preflight.iso(when)}" + (" --market" if market else "")
    first = execute.run_game(repo=repo, game_id=game_id, out_dir=out / "run_a" / game_id, as_of=when, market=market,
                             min_free_mb=min_free_mb, entry=entry, measure_memory=True, invoke_stack=True)
    second = execute.run_game(repo=repo, game_id=game_id, out_dir=out / "run_b" / game_id, as_of=when, market=market,
                              min_free_mb=min_free_mb, entry=entry, measure_memory=True, invoke_stack=True)
    same = bool(first.get("canonical_sha256")) and first.get("canonical_sha256") == second.get("canonical_sha256")
    same = same and first.get("result") == second.get("result")
    if not same:
        result = "BLOCKED"
        detail = "The two runs did not produce the same canonical projection."
        reproducibility = "FAIL"
    else:
        result = first.get("result") or "BLOCKED"
        reproducibility = "PASS"
        detail = "Both runs share one canonical sha256. Runtime and RSS are recorded and are not part of that hash."
    leak = (first.get("leakage") or {})
    record = {
        "schema": "sunday-replay/1",
        "projection_ready": False,
        "research_only": True,
        "game_id": game_id,
        "result": result,
        "reproducibility": reproducibility,
        "detail": detail,
        "as_of_utc": preflight.iso(when),
        "command": command,
        "canonical_sha256": first.get("canonical_sha256") if same else None,
        "git_sha": preflight.git_sha(),
        "leakage": {"status": leak.get("status"), "late_stamps": leak.get("late_stamps"),
                    "excluded_count": len(leak.get("excluded") or []),
                    "inputs_read": leak.get("inputs_read")},
        "run_a": {"result": first.get("result"), "canonical_sha256": first.get("canonical_sha256"),
                  "wall_seconds": (first.get("runtime") or {}).get("wall_seconds"),
                  "memory": ((first.get("runtime") or {}).get("memory") or {}).get("detail"),
                  "critical_ids": first.get("critical_ids"), "required_ids": first.get("required_ids"),
                  "report": f"run_a/{game_id}/report.md"},
        "run_b": {"result": second.get("result"), "canonical_sha256": second.get("canonical_sha256"),
                  "wall_seconds": (second.get("runtime") or {}).get("wall_seconds"),
                  "memory": ((second.get("runtime") or {}).get("memory") or {}).get("detail"),
                  "report": f"run_b/{game_id}/report.md"},
    }
    (out / "replay.json").write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    (out / "replay.md").write_text(report.render_replay(record))
    return record
