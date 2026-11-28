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
    scored_paths = sorted((repo / "grading" / "results").glob("*.summary.json"))
    previously_scored = [path.name[: -len(".summary.json")] for path in scored_paths]
    training_rows = 0
    games_csv = repo / "data" / "historical" / "nflverse" / "games.csv"
    if games_csv.is_file():
        import csv
        with games_csv.open(newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("season") in {"2024", "2025"}:
                    training_rows += 1
    return {
        "schema": "sunday-lock-ledger/1",
        "projection_ready": False,
        "locks_rewritten": False,
        "new_locks_created": 0,
        "games": len(games),
        "locked_ungraded": sum(1 for game in games if game["state"] == "locked_ungraded"),
        "scored_from_lock_sidecar": sum(1 for game in games if game["state"] == "scored"),
        "previously_scored": previously_scored,
        "previously_scored_count": len(previously_scored),
        "training_seasons": [2024, 2025],
        "training_game_rows": training_rows,
        "training_rows_are_locks": False,
        "rows": games,
        "note": "LOCK.json files are read only. Previously scored games are the committed grading summaries. 2024 and 2025 games.csv rows are training counts, not new locks.",
    }
