"""Compare every recorded kickoff. Only an offline NFL.com schedule capture is authoritative.

That capture is `data/schedule/nfl_official_schedule.json` and must name
`https://www.nfl.com/schedules/...`, plus `retrieved_utc` and `as_of`. ESPN, the
nflverse `games.csv` clock, the possession-engine config, and the pregame packet are
recorded originals. They are not the NFL schedule. When the capture is absent, the
resolution stays UNVERIFIED and no clock is promoted because it matches another one.

Config files and `games.csv` are not rewritten.
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
NFL_SCHEDULE_REL = "data/schedule/nfl_official_schedule.json"


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


def nfl_official_kickoff(repo: Path, game_id: str, path: Path | None = None) -> dict:
    """The only authoritative clock: an offline NFL.com schedule capture with retrieval metadata."""
    path = path or (repo / NFL_SCHEDULE_REL)
    rel = str(path.relative_to(repo)) if path.is_relative_to(repo) else str(path)
    if not path.is_file():
        return {
            "status": "UNAVAILABLE",
            "path": rel,
            "kickoff_utc": None,
            "source": None,
            "retrieved_utc": None,
            "as_of": None,
            "reason": (
                "No offline NFL.com schedule capture is in this checkout. "
                f"Expected {NFL_SCHEDULE_REL} with source https://www.nfl.com/schedules/..., retrieved_utc, and as_of. "
                "ESPN, nflverse games.csv, and the possession config are not that source."
            ),
        }
    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return {"status": "UNAVAILABLE", "path": rel, "kickoff_utc": None, "source": None,
                "retrieved_utc": None, "as_of": None, "reason": f"NFL schedule file unreadable: {exc}"}
    source = str(payload.get("source") or "")
    retrieved = payload.get("retrieved_utc")
    as_of = payload.get("as_of")
    games = payload.get("games") if isinstance(payload.get("games"), dict) else {}
    if "nfl.com/schedules" not in source or not retrieved or not as_of:
        return {
            "status": "UNAVAILABLE", "path": rel, "kickoff_utc": None, "source": source or None,
            "retrieved_utc": retrieved, "as_of": as_of,
            "reason": "NFL schedule file is missing source https://www.nfl.com/schedules/..., retrieved_utc, or as_of.",
        }
    kick = parse_utc(games.get(game_id))
    if kick is None:
        return {
            "status": "UNAVAILABLE", "path": rel, "kickoff_utc": None, "source": source,
            "retrieved_utc": retrieved, "as_of": as_of,
            "reason": f"{game_id} is not in the offline NFL.com schedule capture.",
        }
    return {
        "status": "OK", "path": rel, "kickoff_utc": kick, "source": source,
        "retrieved_utc": retrieved, "as_of": as_of, "reason": "Offline NFL.com schedule capture.",
    }


def _clock_conflicts(originals: dict) -> list[dict]:
    named = [(name, parse_utc(row.get("kickoff_utc"))) for name, row in originals.items()]
    conflicts = []
    for i, (left, left_at) in enumerate(named):
        for right, right_at in named[i + 1:]:
            if left_at is not None and right_at is not None and not _same(left_at, right_at):
                conflicts.append({
                    "left": left, "right": right,
                    "left_kickoff_utc": _iso(left_at), "right_kickoff_utc": _iso(right_at),
                })
    return conflicts


def resolve(repo: Path, game_id: str, packet: dict | None = None, nfl_schedule_path: Path | None = None) -> dict:
    espn = espn_event_kickoff(repo, game_id)
    cfg = config_kickoff(repo, game_id)
    csv_row = schedule_csv_kickoff(repo, game_id)
    pkt = packet_kickoff(packet)
    nfl = nfl_official_kickoff(repo, game_id, nfl_schedule_path)
    originals = {
        "nfl_official_schedule": {k: ( _iso(v) if k == "kickoff_utc" else v) for k, v in nfl.items()},
        "espn_event_date": {**{k: v for k, v in espn.items() if k != "kickoff_utc"}, "kickoff_utc": _iso(espn["kickoff_utc"])},
        "possession_config": {**{k: v for k, v in cfg.items() if k != "kickoff_utc"}, "kickoff_utc": _iso(cfg["kickoff_utc"])},
        "nflverse_games_csv": {**{k: v for k, v in csv_row.items() if k != "kickoff_utc"}, "kickoff_utc": _iso(csv_row["kickoff_utc"])},
        "pregame_packet": {"kickoff_utc": _iso(pkt), "timezone": "America/New_York wall clock when the packet stores kickoff_et"},
    }
    conflicts = _clock_conflicts(originals)
    if nfl["status"] != "OK":
        return {
            "game_id": game_id,
            "canonical_kickoff_utc": None,
            "timezone": "UTC",
            "source": None,
            "authoritative_source": "nfl_official_schedule",
            "authoritative_status": "UNAVAILABLE",
            "verification": "UNVERIFIED",
            "resolved": False,
            "reason": nfl["reason"],
            "originals": originals,
            "conflicts": conflicts,
            "config_file_rewritten": False,
            "schedule_file_rewritten": False,
            "adapter": "sunday.kickoff.resolve",
        }
    return {
        "game_id": game_id,
        "canonical_kickoff_utc": _iso(nfl["kickoff_utc"]),
        "timezone": "UTC",
        "source": "nfl_official_schedule",
        "source_timestamp": nfl.get("as_of"),
        "authoritative_source": "nfl_official_schedule",
        "authoritative_status": "OK",
        "verification": "VERIFIED",
        "resolved": True,
        "reason": (
            f"Canonical kickoff is the offline NFL.com schedule capture retrieved {nfl.get('retrieved_utc')} "
            f"as of {nfl.get('as_of')}. Other clocks are recorded and are not the authority."
        ),
        "originals": originals,
        "conflicts": conflicts,
        "config_file_rewritten": False,
        "schedule_file_rewritten": False,
        "adapter": "sunday.kickoff.resolve",
    }
