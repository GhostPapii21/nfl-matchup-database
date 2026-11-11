"""Book prices, no-vig probabilities and line movement for a pregame packet.

Source: The Odds API (the-odds-api.com), key from the ODDS_API_KEY environment variable / repository secret.
Without a key every function returns a labelled "NO_KEY" status and the packet carries no book prices: nothing
is ever invented. De-vigging is done here, in code, so a chat model never does the arithmetic.

Line movement is "first seen by this pipeline -> now": each run appends a snapshot to
pregame/line_history/<game_id>.jsonl. It is not the true opening line unless the pipeline was running at open.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl"
BOOKS = ("pinnacle", "draftkings", "fanduel")
SHARP = "pinnacle"
GAME_MARKETS = ("h2h", "spreads", "totals")
PROP_MARKETS = ("player_pass_yds", "player_rush_yds", "player_reception_yds", "player_receptions", "player_rush_attempts")
PROP_STAT = {"player_pass_yds": "passing_yards", "player_rush_yds": "rushing_yards", "player_reception_yds": "receiving_yards",
             "player_receptions": "receptions", "player_rush_attempts": "carries"}
TEAM = {"Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF", "Carolina Panthers": "CAR",
        "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL", "Denver Broncos": "DEN",
        "Detroit Lions": "DET", "Green Bay Packers": "GB", "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX",
        "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LA", "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG", "New York Jets": "NYJ",
        "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA",
        "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS"}


def implied(american: float) -> float:
    a = float(american)
    if -100 < a < 100:
        raise ValueError(f"invalid American price {american!r}")
    return 100 / (a + 100) if a > 0 else -a / (-a + 100)


def devig(price_a: float, price_b: float) -> tuple[float, float, float]:
    """Two-way no-vig: (fair_a, fair_b, hold). Probabilities are each side's implied share of the total."""
    pa, pb = implied(price_a), implied(price_b)
    return pa / (pa + pb), pb / (pa + pb), pa + pb - 1.0


def _get(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "nfl-pregame-packet/1.0"}), timeout=timeout) as r:
        return json.loads(r.read())


def _q(key, **params):
    return urllib.parse.urlencode({"apiKey": key, "oddsFormat": "american", "bookmakers": ",".join(BOOKS), **params})


def fetch_game_lines(key=None, fetch=_get) -> dict:
    """All upcoming games, main markets, the three books. One request."""
    key = key if key is not None else os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        return {"status": "NO_KEY: set the ODDS_API_KEY repository secret to include book prices", "events": {}}
    try:
        data = fetch(f"{API}/odds?{_q(key, markets=','.join(GAME_MARKETS))}")
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}".replace(key, "***"), "events": {}}
    events = {}
    for e in data:
        h, a = TEAM.get(e.get("home_team")), TEAM.get(e.get("away_team"))
        if h and a:
            events[(a, h)] = e
    return {"status": "OK", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "events": events}


def fetch_props(event_id, key=None, fetch=_get, markets=PROP_MARKETS) -> dict:
    key = key if key is not None else os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        return {"status": "NO_KEY", "event": None}
    try:
        return {"status": "OK", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "event": fetch(f"{API}/events/{event_id}/odds?{_q(key, markets=','.join(markets))}")}
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}".replace(key, "***"), "event": None}


def _pairs(market, home, away):
    """Group a book market's outcomes into two-sided pairs: [(label, point, side_a, price_a, side_b, price_b)]."""
    out, key = [], market["key"]
    oc = market.get("outcomes", [])
    if key == "h2h":
        p = {TEAM.get(o["name"]): o["price"] for o in oc}
        if home in p and away in p:
            out.append(("moneyline", None, home, p[home], away, p[away]))
    elif key == "spreads":
        p = {TEAM.get(o["name"]): o for o in oc}
        if home in p and away in p:
            out.append(("spread", p[home].get("point"), home, p[home]["price"], away, p[away]["price"]))
    elif key == "totals":
        p = {o["name"]: o for o in oc}
        if "Over" in p and "Under" in p and p["Over"].get("point") == p["Under"].get("point"):
            out.append(("total", p["Over"].get("point"), "Over", p["Over"]["price"], "Under", p["Under"]["price"]))
    else:                                                    # player props: outcome.description is the player
        by = {}
        for o in oc:
            by.setdefault((o.get("description"), o.get("point")), {})[o["name"]] = o["price"]
        for (player, point), sides in by.items():
            if "Over" in sides and "Under" in sides:
                out.append((f"{PROP_STAT.get(key, key)}|{player}", point, "Over", sides["Over"], "Under", sides["Under"]))
    return out


def summarize_event(event, home, away) -> dict:
    """Per market: each book's line, prices, no-vig probabilities and hold; the sharp reference; best price per side."""
    markets = {}
    for b in (event or {}).get("bookmakers", []):
        if b["key"] not in BOOKS:
            continue
        for m in b.get("markets", []):
            for label, point, sa, pa, sb, pb in _pairs(m, home, away):
                try:
                    fa, fb, hold = devig(pa, pb)
                except ValueError:
                    continue
                markets.setdefault(label, {"sides": [sa, sb], "books": {}})["books"][b["key"]] = {
                    "line": point, "prices": {sa: pa, sb: pb}, "no_vig": {sa: round(fa, 4), sb: round(fb, 4)},
                    "hold": round(hold, 4), "last_update": m.get("last_update") or b.get("last_update")}
    for label, m in markets.items():
        sa, sb = m["sides"]
        ref = m["books"].get(SHARP)
        m["reference"] = ({"book": SHARP, "line": ref["line"], "no_vig": ref["no_vig"]} if ref else
                          {"book": None, "note": "Pinnacle did not list this market; no sharp reference"})
        lines = {b["line"] for b in m["books"].values()}
        m["books_agree_on_line"] = len(lines) == 1
        best = {}
        for side in (sa, sb):
            cand = [(b["prices"][side], name, b["line"]) for name, b in m["books"].items() if name != SHARP]   # books the user can bet
            if cand:
                price, name, line = max(cand, key=lambda c: 1 / implied(c[0]))
                best[side] = {"book": name, "price": price, "line": line, "break_even": round(implied(price), 4)}
        m["best_retail_price"] = best
    return markets


def record_and_movement(game_id, markets, history_dir: Path, now=None) -> dict:
    """Append this snapshot of main markets, then report first-seen -> current for each book."""
    history_dir.mkdir(parents=True, exist_ok=True)
    f = history_dir / f"{game_id}.jsonl"
    now = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    snap = {"t": now, "markets": {k: {b: {"line": v["line"], "prices": v["prices"]} for b, v in m["books"].items()}
                                  for k, m in markets.items() if k in ("moneyline", "spread", "total")}}
    prev = [json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.exists() else []
    if snap["markets"] and (not prev or prev[-1]["markets"] != snap["markets"]):
        with f.open("a") as fh:
            fh.write(json.dumps(snap) + "\n")
        prev.append(snap)
    if not prev:
        return {"status": "NO_HISTORY", "snapshots": 0}
    first, last, moves = prev[0], prev[-1], []
    for mk, books in last["markets"].items():
        for book, cur in books.items():
            o = first["markets"].get(mk, {}).get(book)
            if not o:
                continue
            row = {"market": mk, "book": book, "first_line": o["line"], "current_line": cur["line"], "first_prices": o["prices"], "current_prices": cur["prices"]}
            if o["line"] is not None and cur["line"] is not None:
                row["line_move"] = round(cur["line"] - o["line"], 2)
            moves.append(row)
    return {"status": "OK", "snapshots": len(prev), "first_seen_utc": first["t"], "current_utc": last["t"], "moves": moves,
            "note": "First seen by this pipeline, not the true opening line. Snapshots are only as frequent as the workflow runs."}
