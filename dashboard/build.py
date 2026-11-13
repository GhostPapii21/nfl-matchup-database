#!/usr/bin/env python3
"""Build the NFL game board from the pregame packets.

    python3 -m dashboard.build                 # every game in pregame/packets/latest.json
    python3 -m dashboard.build --offline       # cached nflverse files only

Writes dashboard/data/<game_id>.json (one file per game, readable by ChatGPT or Grok), dashboard/data/slate.json,
and dashboard/site/index.html: one self-contained page with every game embedded, so a click shows a game at once.
Research only. Nothing here places, prices or recommends a bet.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from dashboard import extras as X  # noqa: E402

PACKETS = ROOT / "pregame" / "packets"
OUT = ROOT / "dashboard"
UA = {"User-Agent": "nfl-game-board/1.0 (research; public data)"}


def _get(url: str, timeout: int = 120) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={**UA, "Accept": "application/geo+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_clean(v) for v in o]
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        o = o.item()
    if isinstance(o, float) and o != o:
        return None
    return o


def side(pk: dict, off: str, dfn: str, ex: dict) -> dict:
    """Everything for one direction of the matchup: `off` offense against `dfn` defense."""
    to, td = pk["teams"][off], pk["teams"][dfn]
    m = pk["matchup"].get(f"{off}_offense_vs_{dfn}_defense", {})
    return {
        "offense": off, "defense": dfn,
        "defense_allowed": td["defense"]["allowed"], "defense_rank": td["defense"]["rank"],
        "defense_by_game": td["defense"]["by_game"], "top_lines_allowed": td["defense"].get("top_lines_allowed", []),
        "run_defense_by_direction": td["defense"].get("run_defense_by_direction", []),
        "offense_produced": to["offense"]["produced"], "offense_rank": to["offense"]["rank"],
        "offense_by_game": to["offense"]["by_game"], "run_game_by_direction": to["offense"].get("run_game_by_direction", []),
        "pass_zones": {"offense": to.get("formation_zone_splits", {}).get("offense_pass_zones", []),
                       "defense_allowed": td.get("formation_zone_splits", {}).get("defense_pass_zones_allowed", [])},
        "edges": m.get("edges", []), "baselines": m.get("player_baselines", {}), "rain": m.get("rain_adjusted", {}),
        "quarterbacks": to["offense"]["players"].get("quarterbacks", []),
        **ex,
    }


def build_game(pk: dict, data: X.Data, games: pd.DataFrame, *, offline: bool) -> dict:
    g = pk["game"]
    season, away, home = int(g["season"]), g["away"], g["home"]
    row = games[games.game_id == g["game_id"]]
    grow = row.iloc[0] if len(row) else pd.Series({"season": season, "gameday": g["date"], "away_team": away, "home_team": home,
                                                    "location": g.get("site"), "stadium": g.get("stadium_id")})
    rosters = data.get("rosters", season)
    snaps = data.get("snaps", season)
    pfr_def = data.get("pfr_def", season)
    id_to_name = {}
    if rosters is not None:
        id_to_name = dict(zip(rosters.gsis_id, rosters.full_name))
    ex_team = {}
    for team, opp in ((away, home), (home, away)):
        tp = pk["teams"][team]
        weeks = tp["window"]["weeks"]
        wids = games[(games.season == season) & games.week.isin(weeks) & ((games.home_team == team) | (games.away_team == team))].game_id
        snap_off = tp["offense"].get("offense_snap_share", {})
        snap_def = X.defense_snap_share(snaps, team, wids)
        ex_team[team] = {
            "qb": X.qb_profile(data, season, team, g.get("listed_qbs", {}).get(team), weeks),
            "roles": X.receiver_roles(tp["offense"]["players"], snap_off, id_to_name),
            "returning": X.returning_players(snaps, games, season, team, g["date"]),
            "injuries": X.injury_impact(tp, snap_off, snap_def),
            "roster_moves": tp.get("roster_moves", {}),
            "defenders": X.defenders_with_positions(tp["defense"].get("defenders", {}), rosters, team, pfr_def, weeks),
            "coverage_profile": X.coverage_profile(data, season, team),
            "window": tp["window"],
            "depth_chart": tp.get("depth_chart", {}),
        }
    sides = {}
    for off, dfn in ((away, home), (home, away)):
        e_off, e_def = ex_team[off], ex_team[dfn]
        sides[f"{off}_vs_{dfn}"] = side(pk, off, dfn, {
            "qb": e_off["qb"], "roles": e_off["roles"], "offense_injuries": e_off["injuries"], "returning": e_off["returning"],
            "defenders": e_def["defenders"], "coverage_profile": e_def["coverage_profile"],
            "defense_injuries": e_def["injuries"], "defense_returning": e_def["returning"],
        })
    result = None
    if len(row) and pd.notna(grow.get("home_score")):
        result = {"away_score": int(grow["away_score"]), "home_score": int(grow["home_score"])}
    alerts = X.nws_alerts(home, g.get("roof"), offline=offline, fetch_json=_get_json)
    return _clean({
        "schema": "game-board/1",
        "game": g, "result": result, "generated_utc": pk["generated_utc"], "board_built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "market": pk.get("market", {}), "books": pk.get("books", {}), "weather": pk.get("weather", {}),
        "weather_verdict": X.weather_verdict(pk.get("weather", {}), g.get("roof"), alerts), "weather_alerts": alerts,
        "context": X.schedule_context(games, grow, pk),
        "h2h": X.head_to_head(games, data, grow, pk, rosters),
        "sides": sides,
        "teams": {t: {"name": X.TEAM_NAMES.get(t, t), "roster_moves": ex_team[t]["roster_moves"], "window": ex_team[t]["window"],
                      "depth_chart": ex_team[t]["depth_chart"]} for t in (away, home)},
        "team_projection": pk.get("team_projection", {}),
        "phase_ledger": pk.get("phase_ledger", []),
        "sources": pk.get("sources", {}),
        "data_gaps": data.missing,
        "status": "RESEARCH_ONLY_NOT_BETTING_ADVICE",
    })


def render_site(boards: list[dict], built: str) -> str:
    tpl = (OUT / "template.html").read_text()
    payload = json.dumps({"built_utc": built, "games": boards}, separators=(",", ":"), allow_nan=False)
    payload = payload.replace("</", "<\\/")   # safe inside a <script> element
    return tpl.replace("/*__BOARD_DATA__*/null", payload)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", default=str(ROOT / "pregame" / ".cache"))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--game", action="append", help="only these game ids")
    a = ap.parse_args(argv)
    idx = json.loads((PACKETS / "latest.json").read_text())
    ids = [x["game_id"] for x in idx["games"] if not a.game or x["game_id"] in a.game]
    data = X.Data(Path(a.cache), offline=a.offline, fetch=_get)
    games = data.get("games")
    if games is None:
        print("board: schedule not available; nothing built")
        return 1
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    (OUT / "site").mkdir(parents=True, exist_ok=True)
    boards = []
    for gid in ids:
        p = PACKETS / gid / "packet.json"
        if not p.exists():
            continue
        pk = json.loads(p.read_text())
        b = build_game(pk, data, games, offline=a.offline)
        (OUT / "data" / f"{gid}.json").write_text(json.dumps(b, indent=1, allow_nan=False) + "\n")
        boards.append(b)
        print(f"board: built {gid}")
    built = datetime.now(timezone.utc).isoformat(timespec="seconds")
    slate = [{"game_id": b["game"]["game_id"], "away": b["game"]["away"], "home": b["game"]["home"], "date": b["game"]["date"],
              "kickoff_et": b["game"]["kickoff_et"], "slot": b["game"]["slot"], "data": f"dashboard/data/{b['game']['game_id']}.json"}
             for b in boards]
    (OUT / "data" / "slate.json").write_text(json.dumps({"schema": "game-board-slate/1", "built_utc": built, "games": slate}, indent=1) + "\n")
    html = render_site(boards, built)
    (OUT / "site" / "index.html").write_text("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
                                             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">"
                                             "</head><body>\n" + html + "\n</body></html>\n")
    (OUT / "site" / "board.html").write_text(html)   # the same page without the document wrapper (for an Artifact)
    if data.missing:
        print("board: data gaps: " + "; ".join(f"{k}: {v}" for k, v in data.missing.items()))
    print(f"board: {len(boards)} games -> dashboard/site/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
