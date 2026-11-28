"""Schedule discovery. No network.

`games_from_packet_index` reads the committed `pregame/packets/latest.json`
shape: date plus kickoff_et in America/New_York. It does not pull a feed and
it does not start a phase.
"""
from __future__ import annotations

from .model import Game
from .timeutil import ScheduleError, parse_kickoff


def games_from_packet_index(doc: dict, *, status: str = "scheduled") -> tuple[list[Game], list[tuple[str, str]]]:
    season = int(doc["season"])
    games: list[Game] = []
    problems: list[tuple[str, str]] = []
    for row in doc.get("games") or []:
        game_id = str(row.get("game_id") or "")
        try:
            kickoff = parse_kickoff(f"{row['date']}T{row['kickoff_et']}", tz="America/New_York")
            games.append(Game(
                game_id=game_id,
                season=season,
                week=int(row["week"]),
                away=str(row["away"]),
                home=str(row["home"]),
                kickoff_utc=kickoff,
                status=str(row.get("status") or status),
                timezone="America/New_York",
            ))
        except (KeyError, ScheduleError, TypeError, ValueError) as exc:
            problems.append((game_id or "?", str(exc)))
    return games, problems


def games_from_slate(doc: dict) -> tuple[list[Game], list[str] | None]:
    """Manual slate file used by the CLI.

    kickoff is either an aware ISO instant or a naive local time plus timezone.
    """
    expected = doc.get("expected_ids")
    games = []
    for row in doc.get("games") or []:
        fold = row.get("fold")
        kickoff = parse_kickoff(str(row["kickoff"]), tz=str(row.get("timezone") or "America/New_York"),
                                fold=None if fold is None else int(fold))
        games.append(Game(
            game_id=str(row["game_id"]),
            season=int(row["season"]),
            week=int(row["week"]),
            away=str(row["away"]),
            home=str(row["home"]),
            kickoff_utc=kickoff,
            status=str(row.get("status") or "scheduled"),
            timezone=str(row.get("timezone") or "America/New_York"),
        ))
    return games, None if expected is None else [str(item) for item in expected]


def parse_now(value: str | None) -> datetime:
    from datetime import datetime, timezone
    if not value:
        return datetime.now(timezone.utc)
    aware = parse_kickoff(value, tz="UTC")
    return aware
