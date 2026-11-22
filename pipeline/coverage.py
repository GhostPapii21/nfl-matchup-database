"""Completed-game coverage for latest-release freshness sources (NFL-56).

A weekly/sporadic file that is still the latest published asset but is missing a completed
game is GAP, not STALE. If coverage cannot be inspected, it is left unknown — never invented.
"""
from __future__ import annotations

from pathlib import Path

GAME_ID_COLS = ("game_id", "nflverse_game_id")
WEEK_COLS = ("week",)
TEAM_COLS = ("team", "team_abbr", "recent_team", "posteam")
SEASON_COLS = ("season",)


def _read_table(path):
    """-> (column names, list of row dicts) or None if the file cannot be read."""
    p = Path(path) if path else None
    if p is None or not p.is_file():
        return None
    try:
        import pyarrow.parquet as pq
        t = pq.read_table(p)
        cols = list(t.column_names)
        # Only pull columns we need
        want = [c for c in cols if c in GAME_ID_COLS + WEEK_COLS + TEAM_COLS + SEASON_COLS
                or c in ("home_score", "away_score", "home_team", "away_team")]
        if not want:
            want = cols[:8]
        return cols, t.select([c for c in want if c in cols]).to_pylist()
    except Exception:
        return None


def _col(rows, *names):
    if not rows:
        return None
    for n in names:
        if n in rows[0]:
            return n
    return None


def completed_games_from_schedule(path, hook=None) -> list[dict] | None:
    """Completed games as {game_id, season, week, teams} from an nflverse schedule file.

    A game is completed when both home_score and away_score are present (the schedule's own
    final-score fields). Returns None if the file cannot be read (unknown, not empty).
    """
    if callable(hook):
        got = hook()
        return got
    tbl = _read_table(path)
    if tbl is None:
        return None
    cols, rows = tbl
    gid = _col(rows, *GAME_ID_COLS)
    if "home_score" not in (rows[0] if rows else {}) or "away_score" not in (rows[0] if rows else {}):
        return None
    out = []
    for r in rows:
        if r.get("home_score") is None or r.get("away_score") is None:
            continue
        teams = [t for t in (r.get("away_team"), r.get("home_team")) if t]
        out.append({"game_id": r.get(gid) if gid else None, "season": r.get("season"),
                    "week": r.get("week"), "teams": teams})
    return out


def ids_in_file(path) -> dict | None:
    """What game/week/team keys a source parquet contains. None if unreadable."""
    tbl = _read_table(path)
    if tbl is None:
        return None
    cols, rows = tbl
    gid = _col(rows, *GAME_ID_COLS)
    week = _col(rows, *WEEK_COLS)
    team = _col(rows, *TEAM_COLS)
    games, weeks, pairs = set(), set(), set()
    for r in rows:
        if gid and r.get(gid):
            games.add(str(r[gid]))
        if week is not None and r.get(week) is not None:
            weeks.add(int(r[week]))
            if team and r.get(team):
                pairs.add((int(r[week]), str(r[team])))
    return {"columns": cols, "game_ids": games, "weeks": weeks, "week_teams": pairs,
            "has_game_id": bool(gid), "has_week_team": bool(week and team)}


def missing_completed(completed: list[dict] | None, found: dict | None) -> list[str]:
    """Human-readable gaps. Empty list = covered (or coverage not inspectable)."""
    if completed is None or found is None:
        return []  # unknown is not a gap we can assert
    missing = []
    if found["has_game_id"]:
        for g in completed:
            gid = g.get("game_id")
            if gid and str(gid) not in found["game_ids"]:
                missing.append(str(gid))
        return missing
    if found["has_week_team"]:
        for g in completed:
            w = g.get("week")
            if w is None:
                continue
            for t in g.get("teams") or []:
                if (int(w), str(t)) not in found["week_teams"]:
                    missing.append(f"{t} week {int(w)}")
        return missing
    return []  # file has neither game_id nor week+team; cannot assert a gap


def source_path(rec: dict | None, cache_names=()) -> str | None:
    if not isinstance(rec, dict):
        return None
    p = rec.get("path")
    if p and Path(p).is_file():
        return p
    for c in cache_names:
        if c and Path(c).is_file():
            return str(c)
    return None
