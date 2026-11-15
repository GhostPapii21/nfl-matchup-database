"""Which games are due for the game-day chain right now (NFL-56).

    python -m pipeline.window                 # human-readable
    python -m pipeline.window --github        # also writes `due`, `matrix` and `count` to $GITHUB_OUTPUT
    python -m pipeline.window --games 2026_10_PIT_CIN,2026_10_SF_DAL   # manual run: only these, window still applies

A game is due when official inactives can exist and there is still time to lock a 100k before kickoff:

    CLOSE_MINUTES <= minutes to kickoff <= OPEN_MINUTES        (default 40 .. 88)

and the 100k entry point has not already run for it (pipeline/ledgers/<game>.sim100k.json status RAN_RESEARCH_ONLY)
and exactly one data_only possession-engine config plus the as-of play-by-play exist for it.

The scheduler calls this every few minutes on game days. GitHub starts scheduled jobs late (hours, on this repo), so
the schedule is dense and this module decides; a tick with nothing due costs no credits and a few seconds.
No network, no API keys. Kickoff times come from the committed packets (pregame/packets/latest.json).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import freshness, phases as PH, sim100k

OPEN_MINUTES = 88     # inactives post at T-90; start just after
CLOSE_MINUTES = 40    # a 100k lock must finish before kickoff


def _already_ran(gid: str, ledgers: Path) -> bool:
    try:
        return json.loads((ledgers / f"{gid}.sim100k.json").read_text()).get("status") == "RAN_RESEARCH_ONLY"
    except (OSError, ValueError):
        return False


def _kickoff(entry: dict, packets: Path):
    try:
        return freshness.kickoff_utc(json.loads((packets / entry["game_id"] / "packet.json").read_text()))
    except (OSError, ValueError, KeyError):
        return freshness.kickoff_utc({"game": {"date": entry.get("date"), "kickoff_et": entry.get("kickoff_et")}})


def evaluate(now: datetime | None = None, only: list[str] | None = None, root: Path | None = None,
             open_minutes: int = OPEN_MINUTES, close_minutes: int = CLOSE_MINUTES) -> dict:
    """One row per game in the slate index with a decision and the reason. Never raises on a bad packet."""
    now = now or datetime.now(timezone.utc)
    root = Path(root or PH.ROOT)
    packets, ledgers = root / "pregame" / "packets", root / "pipeline" / "ledgers"
    try:
        games = json.loads((packets / "latest.json").read_text())["games"]
    except (OSError, ValueError, KeyError) as e:
        return {"checked_utc": now.isoformat(timespec="seconds"), "error": f"cannot read {packets / 'latest.json'}: {e}", "games": [], "due": []}
    rows, due = [], []
    for g in games:
        gid = g.get("game_id")
        if not gid or (only and gid not in only):
            continue
        ko = _kickoff(g, packets)
        row = {"game_id": gid, "kickoff_utc": ko.isoformat() if ko else None, "minutes_to_kickoff": None, "due": False}
        if ko is None:
            row["why"] = "kickoff time unknown"
        else:
            m = (ko - now).total_seconds() / 60
            row["minutes_to_kickoff"] = round(m, 1)
            if m > open_minutes:
                row["why"] = f"opens at T-{open_minutes} min (inactives post at T-90)"
            elif m < close_minutes:
                row["why"] = "kicked off" if m <= 0 else f"closed at T-{close_minutes} min (no time left to lock 100k before kickoff)"
            elif _already_ran(gid, ledgers):
                row["why"] = "100k already ran for this game"
            else:
                ec = sim100k.engine_config(gid, root)
                pbp = sim100k.asof_pbp(ec["cfg"], root) if ec["status"] == "OK" else None
                if ec["status"] != "OK":
                    row["why"] = ec["reason"]
                elif pbp is None:
                    row["why"] = "no as-of play-by-play file for this week under data/historical/nflverse"
                else:
                    row.update(due=True, why="inside the game-day window", config=str(Path(ec["path"]).relative_to(root)),
                               pbp=str(pbp.relative_to(root)))
                    due.append({"game_id": gid, "config": row["config"], "pbp": row["pbp"]})
        rows.append(row)
    return {"checked_utc": now.isoformat(timespec="seconds"), "open_minutes": open_minutes, "close_minutes": close_minutes,
            "games": rows, "due": due}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Games due for the game-day chain now.")
    ap.add_argument("--now", help="ISO time (default: now, UTC)")
    ap.add_argument("--games", default="", help="comma list: only consider these game ids")
    ap.add_argument("--open", type=int, default=OPEN_MINUTES)
    ap.add_argument("--close", type=int, default=CLOSE_MINUTES)
    ap.add_argument("--github", action="store_true", help="write due / matrix / count to $GITHUB_OUTPUT")
    a = ap.parse_args(argv)
    now = freshness.parse_utc(a.now) if a.now else None
    only = [x.strip() for x in a.games.split(",") if x.strip()] or None
    res = evaluate(now, only, open_minutes=a.open, close_minutes=a.close)
    if res.get("error"):
        print("window: " + res["error"])
    for r in res["games"]:
        m = r["minutes_to_kickoff"]
        print(f"window: {r['game_id']}: {'DUE' if r['due'] else 'skip'} ({'?' if m is None else f'{m:.0f}'} min to kickoff; {r['why']})")
    print(f"window: {len(res['due'])} game(s) due at {res['checked_utc']}")
    if a.github and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"count={len(res['due'])}\n")
            f.write("due=" + ",".join(d["game_id"] for d in res["due"]) + "\n")
            f.write("matrix=" + json.dumps({"include": res["due"]}) + "\n")
    return 1 if res.get("error") else 0


if __name__ == "__main__":
    sys.exit(main())
