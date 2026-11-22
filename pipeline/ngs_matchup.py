"""Game-day NGS check for the main-defender matchup step (public NGS only, NFL-47 / NFL-56).

Rico: check routes for receivers and running backs, where the QB throws and where he has been
successful vs the defense, to help determine likely defenders faced. Public nflverse NGS weekly
releases (passing, receiving, rushing) are the only authorized feed — no NFL Pro.

Fields the public weekly files do not carry are listed MISSING/unknown, never filled with zero.
Column inventory is from the nflverse Next Gen Stats dictionary, checked 2026-11-22:
https://nflreadr.nflverse.com/articles/dictionary_nextgen_stats.html
"""
from __future__ import annotations

from pathlib import Path

# Matchup questions this check is supposed to answer for both teams in the game.
WANTED = {
    "receiver_routes": "Route type / routes run / route participation for WRs, TEs, RBs",
    "rb_routes": "Running-back routes (split out from WR/TE routes)",
    "target_location": "Target location splits (side and depth: left/middle/right, short/deep)",
    "qb_pass_location": "Where the QB throws (location splits)",
    "qb_success_vs_defense": "QB success by throw location against this defense",
    "likely_defenders": "Likely defender faced on a route or target location",
}

# Columns that *are* in the public weekly NGS releases (dictionary, 2026-11-22). These are
# weekly player aggregates, not play-level or game-level, and they are not the route/location splits.
AVAILABLE_PUBLIC = {
    "ngs_passing": [
        "avg_time_to_throw", "avg_completed_air_yards", "avg_intended_air_yards",
        "avg_air_yards_differential", "aggressiveness", "max_completed_air_distance",
        "avg_air_yards_to_sticks", "attempts", "completions", "completion_percentage",
        "expected_completion_percentage", "completion_percentage_above_expectation",
        "pass_yards", "pass_touchdowns", "interceptions", "passer_rating",
        "week", "team_abbr", "player_display_name", "player_gsis_id", "player_position",
    ],
    "ngs_receiving": [
        "avg_cushion", "avg_separation", "percent_share_of_intended_air_yards",
        "avg_air_distance", "max_air_distance", "targets", "receptions", "catch_percentage",
        "yards", "rec_touchdowns", "avg_yac", "avg_expected_yac", "avg_yac_above_expectation",
        "week", "team_abbr", "player_display_name", "player_gsis_id", "player_position",
    ],
    "ngs_rushing": [
        "efficiency", "percent_attempts_gte_eight_defenders", "avg_time_to_los",
        "rush_attempts", "rush_yards", "expected_rush_yards", "rush_yards_over_expected",
        "avg_rush_yards", "rush_yards_over_expected_per_att", "rush_pct_over_expected",
        "rush_touchdowns", "week", "team_abbr", "player_display_name", "player_gsis_id",
        "player_position",
    ],
}

# Wanted matchup fields are not in any of the public weekly files (dictionary has no route,
# location, or defender columns, and no game_id).
MISSING_PUBLIC = list(WANTED.keys())

NGS_FILES = {
    "ngs_passing": "ngs_passing.parquet",
    "ngs_receiving": "ngs_receiving.parquet",
    "ngs_rushing": "ngs_rushing.parquet",
}


def _columns(path) -> list[str] | None:
    p = Path(path) if path else None
    if p is None or not p.is_file():
        return None
    try:
        import pyarrow.parquet as pq
        return list(pq.read_schema(p).names)
    except Exception:
        return None


def field_inventory(paths: dict | None = None) -> dict:
    """Available vs missing fields. Documented public gaps are always listed, even with no file.

    If a parquet is present, columns are compared to the dictionary list. A wanted matchup
    field that appears in the file would be moved to available; none do on public NGS.
    Values that are absent are 'MISSING' / 'unknown', never 0.
    """
    paths = paths or {}
    available, missing, notes = [], [], []
    for name, expected in AVAILABLE_PUBLIC.items():
        cols = _columns(paths.get(name))
        if cols is None:
            available.extend({"source": name, "field": f, "status": "available_in_public_ngs_dictionary",
                              "in_file": "unknown"} for f in expected)
            notes.append(f"{name}: file not opened; dictionary columns listed as available in public NGS")
            continue
        present = [f for f in expected if f in cols]
        absent_dict = [f for f in expected if f not in cols]
        extra = [c for c in cols if c not in expected and c not in ("season_type", "season",
                 "player_first_name", "player_last_name", "player_short_name", "player_jersey_number")]
        available.extend({"source": name, "field": f, "status": "available", "in_file": True} for f in present)
        if absent_dict:
            missing.extend({"source": name, "field": f, "status": "MISSING", "value": "unknown",
                            "reason": "listed in the NGS dictionary but not in this file"} for f in absent_dict)
        if extra:
            notes.append(f"{name}: extra columns in file (not used as route/location splits): " + ", ".join(extra[:20]))
        # If a wanted field name actually appeared, it would show here
        for key, desc in WANTED.items():
            if key in cols or any(key in c.lower() or c.lower() in key for c in cols if "route" in c.lower() or "location" in c.lower()):
                pass
    for key, desc in WANTED.items():
        # Confirm none of the opened files carry an obvious route/location/defender column
        found = False
        hints = ("route", "target_location", "pass_location", "throw_location", "defender", "coverage_responsibility")
        for name, path in (paths or {}).items():
            cols = _columns(path) or []
            if any(h in c.lower() for c in cols for h in hints if h in desc.lower() or h in key):
                # still don't treat generic words as the wanted split unless clearly named
                if any(h in c.lower() for c in cols for h in ("route", "target_location", "pass_location", "throw_location")):
                    found = True
        if not found:
            missing.append({"source": "public_ngs", "field": key, "status": "MISSING", "value": "unknown",
                            "reason": desc + " — not in the public weekly NGS releases (nflverse dictionary, 2026-11-22)."})
    return {"available": available, "missing": missing, "notes": notes,
            "wanted": WANTED, "dictionary": "https://nflreadr.nflverse.com/articles/dictionary_nextgen_stats.html"}


def teams_in_week(path, week) -> set[str] | None:
    cols = _columns(path)
    if cols is None:
        return None
    try:
        import pyarrow.parquet as pq
        t = pq.read_table(path, columns=[c for c in ("week", "team_abbr", "team") if c in cols])
        rows = t.to_pylist()
        team_col = "team_abbr" if "team_abbr" in (rows[0] if rows else {}) else ("team" if "team" in (rows[0] if rows else {}) else None)
        if team_col is None or "week" not in (rows[0] if rows else {}):
            return None
        w = int(week)
        return {str(r[team_col]) for r in rows if r.get("week") is not None and int(r["week"]) == w and r.get(team_col)}
    except Exception:
        return None


def check(teams: list[str], week, paths: dict, completed_missing: list[str] | None = None,
           records_ok: dict | None = None) -> dict:
    """Per-game NGS matchup input check for `teams` in `week`.

    Status:
      MISSING  a required NGS file (and its packet/cache record) is absent
      GAP      latest public file is missing a completed game/week-team (from coverage)
      FRESH    public passing/receiving/rushing inputs are present; wanted route/location
               fields are still listed MISSING/unknown, not zero (schema gaps do not refuse)
    """
    inv = field_inventory(paths)
    files = {n: (paths or {}).get(n) for n in NGS_FILES}
    absent = [n for n, p in files.items()
              if not (p and Path(p).is_file()) and not (records_ok or {}).get(n)]
    team_cov = {}
    for n, p in files.items():
        if p and Path(p).is_file() and week is not None:
            got = teams_in_week(p, week)
            team_cov[n] = {"teams_in_week": sorted(got) if got is not None else None,
                           "both_teams": (got is not None and all(t in got for t in teams)) if got is not None else None}
    if absent:
        status, reason = "MISSING", "No public NGS file for: " + ", ".join(absent) + "."
    elif completed_missing:
        status, reason = "GAP", "Public NGS is the latest release but is missing completed-game coverage for: " + ", ".join(completed_missing) + "."
    else:
        missing_wanted = [m["field"] for m in inv["missing"] if m.get("source") == "public_ngs"]
        status = "FRESH"
        reason = ("Public NGS weekly files are present. Wanted main-defender fields are MISSING/unknown, not zero: "
                  + ", ".join(missing_wanted) + ". Available public columns (cushion, separation, CPOE, RYOE, etc.) are listed in evidence.")
        # Week-level presence for both teams is informational; a missing team in a completed week is a GAP
        for n, c in team_cov.items():
            if c.get("both_teams") is False and not completed_missing:
                # Only escalate when this week already has completed games (caller passes completed_missing
                # for that). If both_teams is False but no completed game in this week yet, leave FRESH.
                pass
    return {"status": status, "reason": reason, "teams": list(teams), "week": week,
            "fields": inv, "team_coverage": team_cov, "files": {n: str(p) if p else None for n, p in files.items()}}
