#!/usr/bin/env python3
"""Build pregame research packets for upcoming NFL games.

    python3 -m pregame.build_packets                      # next slate: Thursday, Sunday and Monday games not yet played
    python3 -m pregame.build_packets --week 10            # every unplayed game of week 10
    python3 -m pregame.build_packets --game 2026_10_LAC_BAL
    python3 -m pregame.build_packets --weekdays all       # include Saturday / Friday / holiday games

Writes pregame/packets/<game_id>/packet.json and brief.md, plus pregame/packets/INDEX.md and latest.json.
Research only: nothing here places, prices or recommends a bet, and projection_ready stays false.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from pregame import metrics as M, packet as PK, render as R, sources as S  # noqa: E402

OUT = ROOT / "pregame" / "packets"
DEFAULT_DAYS = ("Thursday", "Sunday", "Monday")


def season_for(day: date) -> int:
    return day.year if day.month >= 3 else day.year - 1


def pick_games(games, *, season, today, week=None, game=None, weekdays=DEFAULT_DAYS, horizon_days=8):
    g = games[(games.season == season) & (games.game_type == "REG")].copy()
    if game:
        return g[g.game_id == game]
    g = g[g.home_score.isna() & (g.gameday >= str(today))]
    if week is not None:
        g = g[g.week == week]
    else:
        g = g[g.gameday <= str(today + timedelta(days=horizon_days))]
        if len(g):
            g = g[g.week == g.week.min()]
    if weekdays != "all":
        g = g[g.weekday.isin(weekdays)]
    return g.sort_values(["gameday", "gametime", "game_id"])


def _clean(o):
    """JSON-safe: NaN -> None, numpy scalars -> python."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_clean(v) for v in o]
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        o = o.item()
    if isinstance(o, float) and o != o:
        return None
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--season", type=int)
    ap.add_argument("--week", type=int)
    ap.add_argument("--game", help="one nflverse game_id, e.g. 2026_10_LAC_BAL")
    ap.add_argument("--weekdays", default=",".join(DEFAULT_DAYS), help="comma list of weekdays, or 'all'")
    ap.add_argument("--window", type=int, default=8, help="games per team in the trend window (default 8)")
    ap.add_argument("--today", help="YYYY-MM-DD (default: today, US Eastern)")
    ap.add_argument("--cache", default=str(ROOT / "pregame" / ".cache"))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--offline", action="store_true", help="use cached downloads only")
    a = ap.parse_args(argv)

    today = date.fromisoformat(a.today) if a.today else (datetime.now(timezone.utc) - timedelta(hours=5)).date()
    season = a.season or (int(a.game.split("_")[0]) if a.game else season_for(today))
    src = S.fetch_all(season, Path(a.cache), offline=a.offline)
    read = lambda k: pd.read_parquet(src[k]["path"]) if src[k].get("path") else None
    games, pbp, rosters = read("games"), read("pbp"), read("rosters")
    weekdays = "all" if a.weekdays == "all" else tuple(x.strip().capitalize() for x in a.weekdays.split(","))
    slate = pick_games(games, season=season, today=today, week=a.week, game=a.game, weekdays=weekdays)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    if not len(slate):
        print(f"pregame: no unplayed {a.weekdays} games found from {today} (season {season}); nothing written")
        return 0
    data = {"games": games, "rosters": rosters, "plays": M.prepare(pbp, rosters, read("ftn")),
            "injuries": read("injuries"), "depth_charts": read("depth_charts"), "snap_counts": read("snap_counts"), "pfr_def": read("pfr_def")}
    espn = S.espn_injuries(offline=a.offline)
    src_pub = {k: {kk: vv for kk, vv in v.items() if kk != "path"} for k, v in src.items()}
    src_pub["espn_injuries"] = {"status": espn["status"], "url": S.ESPN_INJURIES, "retrieved_utc": espn.get("retrieved_utc")}
    index = []
    for g in slate.itertuples():
        pk = _clean(PK.build(g, data=data, window=a.window, espn=espn, pbp_path=src["pbp"]["path"], sources=src_pub))
        d = out / g.game_id; d.mkdir(exist_ok=True)
        (d / "packet.json").write_text(json.dumps(pk, indent=1, allow_nan=False) + "\n")
        (d / "brief.md").write_text(R.brief(pk))
        index.append({"game_id": g.game_id, "week": int(g.week), "slot": pk["game"]["slot"], "date": pk["game"]["date"], "kickoff_et": pk["game"]["kickoff_et"],
                      "away": g.away_team, "home": g.home_team, "brief": f"pregame/packets/{g.game_id}/brief.md",
                      "packet": f"pregame/packets/{g.game_id}/packet.json", "generated_utc": pk["generated_utc"],
                      "phases": {str(p["phase"]): p["status"] for p in pk["phase_ledger"]}})
        print(f"pregame: wrote {g.game_id} ({pk['game']['slot']})")
    (out / "latest.json").write_text(json.dumps({"schema": "pregame-index/1", "season": season, "games": index}, indent=1) + "\n")
    lines = ["# Pregame packets: current slate", "",
             "Research only. `projection_ready` is false. Start with `pregame/ANALYST_PROMPT.md`, then open a brief.", "",
             R.table(["Game", "Slot", "Kickoff (ET)", "Brief", "Data", "Updated (UTC)"],
                     [[f"{i['away']} at {i['home']} (week {i['week']})", i["slot"], f"{i['date']} {i['kickoff_et']}",
                       f"[brief]({i['game_id']}/brief.md)", f"[json]({i['game_id']}/packet.json)", i["generated_utc"]] for i in index]), ""]
    (out / "INDEX.md").write_text("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
