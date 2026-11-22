"""Kickoff cross-check against ESPN's public scoreboard.

Our packets take kickoff times from the nflverse schedule. On 2026-11-22 two games had swapped slots there
(PIT@PHI listed 4:25 PM ET, really 1:00 PM; JAX@NYG listed 1:00 PM, really 4:25 PM), so the game-day window opened at the
wrong time and the lock tool's "before kickoff?" check compared against the wrong time.

    python -m pipeline.kickoffs            # writes pregame/kickoffs/latest.json (today and tomorrow, ET)

`lookup(game_id, near)` returns ESPN's kickoff for that matchup when the file has one within 3 days of `near`.
Free, no keys; fail-soft (a failed fetch leaves the previous file and returns {}).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={d}"
ALIAS = {"WSH": "WAS", "LAR": "LA"}          # ESPN -> nflverse codes
NEAR = timedelta(days=3)


def path() -> Path:
    return Path(os.environ.get("NFL_KICKOFF_FILE") or ROOT / "pregame" / "kickoffs" / "latest.json")


def _utc(s):
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def parse(scoreboard: dict) -> dict:
    """ESPN scoreboard JSON -> {"AWAY_HOME": kickoff ISO UTC}."""
    out = {}
    for e in scoreboard.get("events") or []:
        try:
            c = e["competitions"][0]
            t = {x["homeAway"]: ALIAS.get(x["team"]["abbreviation"], x["team"]["abbreviation"]) for x in c["competitors"]}
            ko = _utc(e.get("date") or c.get("date"))
        except (KeyError, IndexError, TypeError):
            continue
        if ko and "away" in t and "home" in t:
            out[f"{t['away']}_{t['home']}"] = ko.isoformat()
    return out


def refresh(now: datetime | None = None, get=None) -> dict:
    now = now or datetime.now(timezone.utc)
    get = get or (lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "nfl-research"}), timeout=20).read())
    games, raw = {}, {}
    for day in sorted({(now.astimezone(ET) + timedelta(days=k)).strftime("%Y%m%d") for k in (0, 1)}):
        u = URL.format(d=day)
        try:
            b = get(u)
            games.update(parse(json.loads(b)))
            raw[u] = hashlib.sha256(b).hexdigest()
        except Exception as ex:          # fail-soft: keep the previous file
            raw[u] = f"error: {type(ex).__name__}: {ex}"
    if not games:
        return {}
    rec = {"source": "ESPN public scoreboard", "retrieved_utc": now.isoformat(timespec="seconds"), "raw_sha256": raw, "games": games}
    p = path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    return rec


def lookup(game_id: str | None, near: datetime | None) -> datetime | None:
    """ESPN kickoff for e.g. 2026_11_PIT_PHI, if the file has that matchup within 3 days of `near`."""
    if not game_id:
        return None
    parts = str(game_id).split("_")
    if len(parts) < 4:
        return None
    try:
        games = json.loads(path().read_text()).get("games") or {}
    except (OSError, ValueError):
        return None
    ko = _utc(games.get(f"{parts[-2]}_{parts[-1]}"))
    if ko is None or (near is not None and abs(ko - near) > NEAR):
        return None
    return ko


def main(argv=None) -> int:
    rec = refresh()
    if not rec:
        print("kickoffs: ESPN fetch failed; previous file kept", file=sys.stderr)
        return 0
    print(f"kickoffs: {len(rec['games'])} games from ESPN -> {path()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
