"""One kickoff for a game, with the disagreeing clocks kept visible.

The canonical clock is the ESPN event `date` on the committed event file when that
file exists. This repository already uses ESPN to correct nflverse slots that were
swapped (`pipeline/kickoffs.py`). For LV@CLE, TEN@JAX, and NE@LAC that ESPN instant
matches the possession-engine config and the pregame packet, and it does not match
`data/historical/nflverse/games.csv`.

The config file and the csv are not rewritten. The manifest records both original
values and this resolution.
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
DATE_RE = re.compile(r'"date"\s*:\s*"([^"]+)"')


def parse_utc(value) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        got = datetime.fromisoformat(text)
    except ValueError:
        return None
    if got.tzinfo is None:
        return None
    return got.astimezone(timezone.utc).replace(microsecond=0)


def _et_wall(date: str, clock: str) -> datetime | None:
    if not date or not clock or "T" in str(clock):
        return None
    try:
        hh, mm = str(clock).split(":")[:2]
        local = datetime.fromisoformat(str(date)).replace(hour=int(hh), minute=int(mm), tzinfo=ET)
    except (TypeError, ValueError):
        return None
    return local.astimezone(timezone.utc).replace(microsecond=0)


def _iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def packet_kickoff(packet: dict | None) -> datetime | None:
    game = (packet or {}).get("game") or {}
    stamped = parse_utc(game.get("kickoff_utc"))
    if stamped:
        return stamped
    weather = (packet or {}).get("weather") or {}
    stamped = parse_utc(weather.get("kickoff_utc"))
    if stamped:
        return stamped
    return _et_wall(str(game.get("date") or ""), str(game.get("kickoff_et") or ""))


def config_kickoff(repo: Path, game_id: str) -> dict:
    folder = repo / "core" / "possession_engine_v0" / "config"
    hits = []
    if folder.is_dir():
        for path in sorted(folder.glob("*.json")):
            try:
                cfg = json.loads(path.read_text())
            except (OSError, ValueError):
                continue
            game = cfg.get("game") or {}
            if game.get("game_id") == game_id and cfg.get("mode") == "data_only":
                hits.append((path, parse_utc(game.get("kickoff_et"))))
    if not hits:
        return {"status": "ABSENT", "path": None, "kickoff_utc": None}
    if len(hits) > 1:
        return {"status": "AMBIGUOUS", "path": None, "kickoff_utc": None,
                "paths": [str(p.relative_to(repo)) for p, _ in hits]}
    path, kick = hits[0]
    return {"status": "OK", "path": str(path.relative_to(repo)), "kickoff_utc": kick}


def schedule_csv_kickoff(repo: Path, game_id: str) -> dict:
    path = repo / "data" / "historical" / "nflverse" / "games.csv"
    if not path.is_file():
        return {"status": "ABSENT", "path": None, "kickoff_utc": None, "gametime": None, "gameday": None}
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("game_id") != game_id:
                continue
            kick = _et_wall(row.get("gameday") or "", row.get("gametime") or "")
            return {
                "status": "OK",
                "path": "data/historical/nflverse/games.csv",
                "kickoff_utc": kick,
                "gameday": row.get("gameday"),
                "gametime": row.get("gametime"),
                "timezone_assumed": "America/New_York",
            }
    return {"status": "ABSENT", "path": "data/historical/nflverse/games.csv", "kickoff_utc": None,
            "gametime": None, "gameday": None}


def espn_event_kickoff(repo: Path, game_id: str) -> dict:
    """Read only the event `date` field. Scores in the same file are not loaded."""
    folder = repo / "grading" / "results" / "sources"
    if not folder.is_dir():
        return {"status": "ABSENT", "path": None, "kickoff_utc": None}
    hits = sorted(folder.glob(f"espn_summary_{game_id}_*.json"))
    if not hits:
        return {"status": "ABSENT", "path": None, "kickoff_utc": None}
    path = hits[-1]
    kick = None
    with path.open() as fh:
        for line in fh:
            match = DATE_RE.search(line)
            if match:
                kick = parse_utc(match.group(1))
                break
    rel = str(path.relative_to(repo))
    if kick is None:
        return {"status": "UNREADABLE", "path": rel, "kickoff_utc": None}
    return {"status": "OK", "path": rel, "kickoff_utc": kick, "field": "date",
            "note": "ESPN event date only. The rest of the file, including any score, was not parsed."}


def _same(a: datetime | None, b: datetime | None) -> bool:
    if a is None or b is None:
        return False
    return abs((a - b).total_seconds()) <= 60


def resolve(repo: Path, game_id: str, packet: dict | None = None) -> dict:
    espn = espn_event_kickoff(repo, game_id)
    cfg = config_kickoff(repo, game_id)
    csv_row = schedule_csv_kickoff(repo, game_id)
    pkt = packet_kickoff(packet)
    originals = {
        "espn_event_date": {**{k: v for k, v in espn.items() if k != "kickoff_utc"}, "kickoff_utc": _iso(espn["kickoff_utc"])},
        "possession_config": {**{k: v for k, v in cfg.items() if k != "kickoff_utc"}, "kickoff_utc": _iso(cfg["kickoff_utc"])},
        "nflverse_games_csv": {**{k: v for k, v in csv_row.items() if k != "kickoff_utc"}, "kickoff_utc": _iso(csv_row["kickoff_utc"])},
        "pregame_packet": {"kickoff_utc": _iso(pkt), "timezone": "America/New_York wall clock when the packet stores kickoff_et"},
    }
    chosen = None
    source = None
    reason = ""
    if espn["kickoff_utc"] is not None and _same(espn["kickoff_utc"], cfg["kickoff_utc"]):
        chosen = espn["kickoff_utc"]
        source = "espn_event_date"
        reason = ("ESPN event date matches the possession-engine config. "
                  "That instant is the canonical kickoff. nflverse games.csv is kept as a recorded original "
                  "and is not applied when it differs.")
    elif espn["kickoff_utc"] is not None:
        chosen = espn["kickoff_utc"]
        source = "espn_event_date"
        reason = "ESPN event date is present. The possession config does not match it, so the config clock is not used."
    elif cfg["kickoff_utc"] is not None:
        chosen = cfg["kickoff_utc"]
        source = "possession_config"
        reason = "No ESPN event date was found. The possession-engine config kickoff is the canonical clock."
    elif pkt is not None:
        chosen = pkt
        source = "pregame_packet"
        reason = "No ESPN event date and no possession config kickoff. The packet wall clock is the canonical kickoff."
    conflicts = []
    for name, row in originals.items():
        other = parse_utc(row.get("kickoff_utc"))
        if chosen is not None and other is not None and not _same(chosen, other):
            conflicts.append({"source": name, "kickoff_utc": row.get("kickoff_utc")})
    return {
        "game_id": game_id,
        "canonical_kickoff_utc": _iso(chosen),
        "timezone": "UTC",
        "source": source,
        "source_timestamp": originals.get(source, {}).get("kickoff_utc") if source else None,
        "reason": reason if chosen else "no kickoff could be resolved",
        "resolved": chosen is not None,
        "originals": originals,
        "conflicts": conflicts,
        "config_file_rewritten": False,
        "schedule_file_rewritten": False,
        "adapter": "sunday.kickoff.resolve",
    }
