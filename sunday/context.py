"""Game identity, schedule read, and the as-of boundary for one Sunday run.

Final scores are never copied out of the schedule file. Predictions require
``as_of`` to be strictly before kickoff, and the play-by-play file to stop
at the previous week.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
GAMES_CSV = ROOT / "data" / "historical" / "nflverse" / "games.csv"
PACKETS = ROOT / "pregame" / "packets"
PBP_DIR = ROOT / "data" / "historical" / "nflverse"
ET = ZoneInfo("America/New_York")

# nflverse schedule columns that are results, not pregame identity.
SCORE_COLUMNS = frozenset({
    "away_score", "home_score", "result", "total", "overtime",
})
SCHEDULE_KEEP = (
    "game_id", "season", "game_type", "week", "gameday", "weekday", "gametime",
    "away_team", "home_team", "location", "roof", "surface", "stadium", "stadium_id",
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def sha256_file(path: Path | None) -> str | None:
    if path is None or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_revision(root: Path = ROOT) -> dict:
    def _run(*args: str) -> str:
        try:
            return subprocess.run(
                ["git", *args], cwd=root, capture_output=True, text=True, check=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return ""

    commit = _run("rev-parse", "HEAD")
    dirty = bool(_run("status", "--porcelain"))
    return {"commit": commit or None, "dirty": dirty}


def _kickoff_utc(date: str, gametime: str) -> datetime | None:
    if not date or not gametime:
        return None
    try:
        local = datetime.fromisoformat(f"{date}T{gametime}").replace(tzinfo=ET)
    except ValueError:
        return None
    return local.astimezone(timezone.utc)


def iter_schedule(path: Path = GAMES_CSV):
    """Yield identity rows. Result columns are dropped here and never returned."""
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if (row.get("game_type") or "REG") not in ("REG", ""):
                continue
            kept = {k: row.get(k) or None for k in SCHEDULE_KEEP}
            for banned in SCORE_COLUMNS:
                kept.pop(banned, None)
            if kept.get("season"):
                kept["season"] = int(kept["season"])
            if kept.get("week"):
                kept["week"] = int(kept["week"])
            kept["kickoff_utc"] = None
            kick = _kickoff_utc(kept.get("gameday") or "", kept.get("gametime") or "")
            if kick is not None:
                kept["kickoff_utc"] = kick.isoformat()
            yield kept


def schedule_games(*, game_id: str | None = None, on_date: str | None = None,
                   season: int | None = None, week: int | None = None,
                   weekday: str | None = None, path: Path = GAMES_CSV) -> list[dict]:
    out = []
    for row in iter_schedule(path):
        if game_id and row["game_id"] != game_id:
            continue
        if on_date and row.get("gameday") != on_date:
            continue
        if season is not None and row.get("season") != int(season):
            continue
        if week is not None and row.get("week") != int(week):
            continue
        if weekday and (row.get("weekday") or "").lower() != weekday.lower():
            continue
        out.append(row)
    return out


def asof_pbp(season: int, week: int, root: Path = ROOT) -> Path | None:
    """Committed play-by-play whose name is weeks 1..week-1. Newest name wins."""
    files = sorted(PBP_DIR.glob(f"pbp_{int(season)}_w1_{int(week) - 1}_pulled_*.parquet"))
    return files[-1] if files else None


def possession_config(game_id: str, root: Path = ROOT) -> dict:
    """The single data_only possession config for this game, or a refusal to choose."""
    hits = []
    cfg_dir = root / "core" / "possession_engine_v0" / "config"
    for path in sorted(cfg_dir.glob("*.json")):
        try:
            cfg = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if (cfg.get("game") or {}).get("game_id") == game_id and cfg.get("mode") == "data_only":
            hits.append((path, cfg))
    if not hits:
        return {"status": "ABSENT", "reason": f"no data_only possession config for {game_id}"}
    if len(hits) > 1:
        names = ", ".join(p.name for p, _ in hits)
        return {"status": "AMBIGUOUS", "reason": f"{len(hits)} data_only configs for {game_id}: {names}"}
    path, cfg = hits[0]
    return {"status": "OK", "path": path, "cfg": cfg}


def load_packet(game_id: str, root: Path = ROOT) -> tuple[Path | None, dict | None, str | None]:
    path = root / "pregame" / "packets" / game_id / "packet.json"
    if not path.is_file():
        return None, None, f"missing {path.relative_to(root)}"
    try:
        return path, json.loads(path.read_text()), None
    except (OSError, ValueError) as exc:
        return path, None, f"unreadable packet: {exc}"


def kickoff_from_packet(packet: dict, cfg: dict | None) -> datetime | None:
    game = (cfg or {}).get("game") or {}
    stamped = parse_utc(game.get("kickoff_et"))
    if stamped is not None and "T" in str(game.get("kickoff_et")):
        return stamped
    g = packet.get("game") or {}
    return _kickoff_utc(str(g.get("date") or ""), str(g.get("kickoff_et") or ""))


def pbp_leakage(path: Path, season: int, week: int, game_id: str) -> dict:
    """Read week and game_id only. A target-week or target-game row is leakage."""
    import pandas as pd

    frame = pd.read_parquet(path, columns=["game_id", "week", "season"])
    frame = frame[frame["season"] == int(season)]
    weeks = sorted({int(w) for w in frame["week"].dropna().unique()})
    max_week = max(weeks) if weeks else None
    contains_game = bool((frame["game_id"] == game_id).any())
    future = [w for w in weeks if w >= int(week)]
    ok = not contains_game and not future and max_week is not None
    return {
        "ok": ok,
        "max_week": max_week,
        "weeks": weeks,
        "contains_target_game": contains_game,
        "weeks_at_or_after_target": future,
        "rows": int(len(frame)),
    }


def build_context(spec: dict, root: Path = ROOT) -> dict:
    """Resolve one game. ``spec`` is a plain dict so a process pool can carry it."""
    game_id = spec["game_id"]
    packet_path, packet, packet_error = load_packet(game_id, root)
    sched = schedule_games(game_id=game_id)
    schedule = sched[0] if sched else None
    cfg_hit = possession_config(game_id, root)
    cfg = cfg_hit.get("cfg") if cfg_hit.get("status") == "OK" else None
    game = (packet or {}).get("game") or {}
    season = int(game.get("season") or (schedule or {}).get("season") or spec.get("season") or 0)
    week = int(game.get("week") or (schedule or {}).get("week") or spec.get("week") or 0)
    away = game.get("away") or (schedule or {}).get("away_team")
    home = game.get("home") or (schedule or {}).get("home_team")
    kickoff = kickoff_from_packet(packet, cfg) if packet else parse_utc((schedule or {}).get("kickoff_utc"))
    as_of = parse_utc(spec.get("as_of")) or utcnow()
    pbp = asof_pbp(season, week, root) if season and week else None
    if cfg and "T" in str((cfg.get("game") or {}).get("kickoff_et") or ""):
        kickoff_source = "possession_config"
    elif packet is not None:
        kickoff_source = "packet"
    else:
        kickoff_source = "schedule"
    return {
        "root": root,
        "spec": spec,
        "game_id": game_id,
        "season": season,
        "week": week,
        "away": away,
        "home": home,
        "packet_path": packet_path,
        "packet": packet,
        "packet_error": packet_error,
        "schedule": schedule,
        "config_hit": {k: v for k, v in cfg_hit.items() if k != "cfg"} | (
            {"config_id": cfg.get("config_id")} if cfg else {}
        ),
        "config_path": cfg_hit.get("path"),
        "config": cfg,
        "kickoff_utc": kickoff,
        "kickoff_source": kickoff_source,
        "as_of": as_of,
        "pbp_path": pbp,
        "trials": int(spec.get("trials") or 200),
        "command": spec.get("command"),
    }
