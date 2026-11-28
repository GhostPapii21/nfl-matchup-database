"""Read committed snapshot locks. This module does not write or replace a lock.

A game with a LOCK.json is locked. A game is scored only when a sibling grade
file is already next to that lock. Otherwise it stays ungraded.
"""
from __future__ import annotations

import json
from pathlib import Path


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def ledger(repo: Path) -> dict:
    locks = sorted((repo / "snapshots").glob("*/**/LOCK.json"))
    by_game: dict[str, list] = {}
    for path in locks:
        body = _load(path)
        game_id = body.get("game_id") or path.parents[1].name
        grade = path.with_name("GRADE.json")
        by_game.setdefault(game_id, []).append({
            "path": str(path.relative_to(repo)),
            "locked_utc": body.get("locked_utc"),
            "kickoff_utc": body.get("kickoff_utc"),
            "code_commit": body.get("code_commit"),
            "projection_ready": body.get("projection_ready"),
            "sim_n": (body.get("sim") or {}).get("n"),
            "sim_runtime_sec": (body.get("sim") or {}).get("runtime_sec"),
            "grade_path": str(grade.relative_to(repo)) if grade.is_file() else None,
            "state": "scored" if grade.is_file() else "locked_ungraded",
        })
    games = []
    for game_id, rows in sorted(by_game.items()):
        states = {row["state"] for row in rows}
        games.append({
            "game_id": game_id,
            "locks": len(rows),
            "state": "scored" if "scored" in states else "locked_ungraded",
            "snapshots": rows,
            "rewritten": False,
        })
    return {
        "schema": "sunday-lock-ledger/1",
        "projection_ready": False,
        "locks_rewritten": False,
        "games": len(games),
        "locked_ungraded": sum(1 for game in games if game["state"] == "locked_ungraded"),
        "scored": sum(1 for game in games if game["state"] == "scored"),
        "rows": games,
        "note": "Counts are committed LOCK.json files. A second snapshot of the same game is not a new game and is not a retroactive lock.",
    }
