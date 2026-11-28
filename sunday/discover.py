"""Slate discovery from pregame/packets/latest.json. No network."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


def index_path(repo: Path) -> Path:
    return repo / "pregame" / "packets" / "latest.json"


def load_index(repo: Path) -> tuple[list[dict] | None, str | None]:
    path = index_path(repo)
    try:
        data = json.loads(path.read_text())
        games = data["games"]
        if not isinstance(games, list):
            raise TypeError("games is not a list")
    except (OSError, ValueError, KeyError, TypeError) as e:
        return None, f"schedule index {path}: {e}"
    return games, None


def index_kickoff(entry: dict) -> datetime | None:
    """Kickoff from the index date and ET clock. None when either field is missing."""
    try:
        hh, mm = str(entry["kickoff_et"]).split(":")[:2]
        day = datetime.fromisoformat(str(entry["date"]))
    except (KeyError, ValueError):
        return None
    local = day.replace(hour=int(hh), minute=int(mm), tzinfo=ET)
    return local.astimezone(timezone.utc)


def select(games: list[dict], *, week: int | None = None, on_date: str | None = None, slot: str | None = None,
           only: list[str] | None = None, as_of: datetime | None = None, include_started: bool = False,
           all_games: bool = False) -> list[dict]:
    """Games to run.

    An explicit `--game` list is kept even if that kickoff has passed (the game command then blocks a post-kickoff
    as-of). Otherwise, games whose index kickoff is at or before as-of are left out unless `--all` or
    `--include-started` is set. A missing kickoff on the index is kept; the game command resolves it from the packet.
    """
    wanted = set(only or [])
    chosen = []
    for entry in games:
        gid = entry.get("game_id")
        if wanted and gid not in wanted:
            continue
        if not wanted:
            if week is not None and int(entry.get("week") or -1) != int(week):
                continue
            if on_date and str(entry.get("date") or "") != on_date:
                continue
            if slot and slot.casefold() not in str(entry.get("slot") or "").casefold():
                continue
            if not all_games and not include_started and as_of is not None:
                kick = index_kickoff(entry)
                if kick is not None and as_of >= kick:
                    continue
        chosen.append(entry)
    return chosen


def packet_path(repo: Path, game_id: str, entry: dict | None) -> Path | None:
    """Packet path inside the repository. None when the id or the relative path would leave it."""
    from sunday.preflight import valid_game_id
    if not valid_game_id(str(game_id or "")):
        return None
    rel = (entry or {}).get("packet") or f"pregame/packets/{game_id}/packet.json"
    parts = Path(str(rel)).parts
    if Path(str(rel)).is_absolute() or ".." in parts:
        return None
    path = (repo / rel).resolve()
    try:
        path.relative_to(repo.resolve())
    except ValueError:
        return None
    return path
