"""Download the public datasets a pregame packet needs, with provenance.

All sources are free and public. nflverse data keep their own terms (see SOURCES.md); FTN charting via
nflverse is CC-BY-SA and must be attributed. Nothing here needs a key. ESPN is optional enrichment: when
it cannot be reached the packet says so and carries on.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download"
DATASETS = {
    "games": "schedules/games.parquet",
    "pbp": "pbp/play_by_play_{season}.parquet",
    "rosters": "weekly_rosters/roster_weekly_{season}.parquet",
    "injuries": "injuries/injuries_{season}.parquet",
    "depth_charts": "depth_charts/depth_charts_{season}.parquet",
    "snap_counts": "snap_counts/snap_counts_{season}.parquet",
    "ftn": "ftn_charting/ftn_charting_{season}.parquet",
    "pfr_def": "pfr_advstats/advstats_week_def_{season}.parquet",
}
REQUIRED = ("games", "pbp", "rosters")
ESPN_INJURIES = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries"
UA = {"User-Agent": "nfl-pregame-packet/1.0 (research; public data)"}


def _get(url: str, timeout: int = 120) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def fetch_all(season: int, cache: Path, *, offline: bool = False, fetch=_get) -> dict:
    """Return {name: {path, url, status, sha256, bytes, retrieved_utc}}. Required datasets raise when missing."""
    cache.mkdir(parents=True, exist_ok=True)
    out = {}
    for name, rel in DATASETS.items():
        url = f"{NFLVERSE}/{rel.format(season=season)}"
        path = cache / Path(rel.format(season=season)).name
        rec = {"url": url, "path": str(path), "status": "OK", "retrieved_utc": None}
        if not offline:
            try:
                data = fetch(url)
                path.write_bytes(data)
                rec["retrieved_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            except Exception as exc:  # network, 404 (dataset not posted yet), proxy
                rec["status"] = f"FETCH_FAILED: {type(exc).__name__}: {str(exc)[:120]}"
        if path.exists():
            b = path.read_bytes()
            rec.update(sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
            if rec["status"] != "OK":
                rec["status"] = "STALE_CACHE_USED; " + rec["status"]
            elif offline:
                rec["status"] = "OFFLINE_CACHE"
        else:
            rec["path"] = None
            if rec["status"] == "OK":
                rec["status"] = "MISSING_OFFLINE"
        if name in REQUIRED and rec["path"] is None:
            raise SystemExit(f"pregame: required dataset '{name}' unavailable ({rec['status']}); no packet written")
        out[name] = rec
    return out


def espn_injuries(*, offline: bool = False, fetch=_get) -> dict:
    """Live league injury list from ESPN, keyed by team abbreviation. Never raises."""
    if offline:
        return {"status": "SKIPPED_OFFLINE", "teams": {}}
    try:
        j = json.loads(fetch(ESPN_INJURIES, timeout=30))
        teams = {}
        for t in j.get("injuries", []):
            rows = []
            for i in t.get("injuries", []):
                a = i.get("athlete", {})
                abbr = (a.get("team") or {}).get("abbreviation")
                rows.append({"player": a.get("displayName"), "position": (a.get("position") or {}).get("abbreviation"),
                             "status": i.get("status"), "date": i.get("date"), "comment": (i.get("shortComment") or "")[:200],
                             "team": abbr})
            for r in sorted(rows, key=lambda r: (str(r["status"]).lower() == "active", str(r["date"] or "")), reverse=False):
                if r["team"]:
                    teams.setdefault(ESPN_TO_NFLVERSE.get(r["team"], r["team"]), []).append(r)
        return {"status": "OK", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "url": ESPN_INJURIES, "teams": teams,
                "note": "ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation."}
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}", "url": ESPN_INJURIES, "teams": {}}


ESPN_TO_NFLVERSE = {"WSH": "WAS", "LAR": "LA"}
