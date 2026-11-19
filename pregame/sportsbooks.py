"""FanDuel, DraftKings, Pinnacle and Caesars NFL lines straight from the books' public web endpoints (no Odds API, no credits).

    python -m pregame.sportsbooks                 # every listed NFL game -> pregame/direct_lines/<game_id>.json
    python -m pregame.sportsbooks --probe         # also keep truncated raw responses in pregame/direct_lines/_probe/

These are the JSON feeds the books' own websites load. They are unofficial: no key, no published schema, and they can
change or block a client without notice. A book that refuses a request (DraftKings answers 403 to GitHub's servers) is
recorded as refused; this module does not try to get around a refusal (FanDuel serves by US state; requests from outside the US are refused). The
parser looks for markets by name, so a renamed market is skipped, never guessed. Every run records what each book
returned, and a book that fails is listed as failed, not filled in. Research only.

Markets kept: spread, total, moneyline, and player receiving yards, receptions, rushing yards, and alternate (X+)
receiving and rushing yards. Each row: book, market, player (props), side, line, American price, break-even.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pregame" / "direct_lines"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept": "application/json", "Accept-Language": "en-US,en;q=0.9"}
DK = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkusnj/v1/leagues/88808"
FD_STATES = ("nj", "pa", "ny", "il")
FD_AK = "FhMFpcPWXMeyZxOx"
FD_PAGE = "https://sbapi.{st}.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nfl&pbHorizontal=false&_ak={ak}&timezone=America%2FNew_York"
FD_EVENT = "https://sbapi.{st}.sportsbook.fanduel.com/api/event-page?_ak={ak}&eventId={eid}&tab={tab}&timezone=America%2FNew_York"
FD_TABS = ("player-receiving", "player-rushing", "receiving-props", "rushing-props", "player-props")
PAUSE = 0.6     # seconds between calls: a handful of requests a run, nothing more

TEAMS = {"ARI": "Cardinals", "ATL": "Falcons", "BAL": "Ravens", "BUF": "Bills", "CAR": "Panthers", "CHI": "Bears", "CIN": "Bengals",
         "CLE": "Browns", "DAL": "Cowboys", "DEN": "Broncos", "DET": "Lions", "GB": "Packers", "HOU": "Texans", "IND": "Colts",
         "JAX": "Jaguars", "KC": "Chiefs", "LA": "Rams", "LAC": "Chargers", "LV": "Raiders", "MIA": "Dolphins", "MIN": "Vikings",
         "NE": "Patriots", "NO": "Saints", "NYG": "Giants", "NYJ": "Jets", "PHI": "Eagles", "PIT": "Steelers", "SEA": "Seahawks",
         "SF": "49ers", "TB": "Buccaneers", "TEN": "Titans", "WAS": "Commanders"}
NICK = {v.lower(): k for k, v in TEAMS.items()}


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def american(x):
    if x is None:
        return None
    s = str(x).replace("−", "-").replace("+", "").strip()
    if s.upper() in ("EVEN", "EV"):
        return 100
    try:
        return int(float(s))
    except ValueError:
        return None


def break_even(a):
    if a is None or a == 0:
        return None
    return round(100 / (a + 100), 4) if a > 0 else round(-a / (-a + 100), 4)


def kind_of(name: str) -> str | None:
    """Market kind from a book's market name; None when it is not one we keep."""
    n = (name or "").lower()
    if "rush" in n and "rec" in n:            # combined rushing + receiving yards: not a market we model
        return None
    if re.search(r"\balt(ernate)?\b|\d+\+", n) and "receiving" in n and "yd" in n.replace("yard", "yd"):
        return "alt_receiving_yards"
    if re.search(r"\balt(ernate)?\b|\d+\+", n) and "rush" in n and "yd" in n.replace("yard", "yd"):
        return "alt_rushing_yards"
    if "receiving yards" in n or "receiving yds" in n or n.endswith("rec yds"):
        return "receiving_yards"
    if "receptions" in n:
        return "receptions"
    if ("rushing yards" in n or "rushing yds" in n or "rush yds" in n) and "passing" not in n:
        return "rushing_yards"
    if n in ("spread", "point spread") or n.startswith("spread") or "handicap" in n:
        return "spread"
    if n in ("total", "total points") or n.startswith("total points") or n == "game total":
        return "total"
    if n in ("moneyline", "money line") or "moneyline" in n:
        return "moneyline"
    return None


def team_of(text: str) -> str | None:
    t = (text or "").lower()
    for nick, ab in NICK.items():
        if nick in t:
            return ab
    return None


def _row(book, ev, kind, player, side, line, price):
    a = american(price)
    return {"book": book, "event": ev, "market": kind, "player": player, "side": side,
            "line": None if line is None else float(line), "american": a, "break_even": break_even(a)}


# ----------------------------------------------------------------------------------------------- DraftKings
def draftkings(probe: dict | None = None) -> dict:
    out = {"status": None, "rows": [], "events": {}}
    try:
        lg = _get(DK)
    except Exception as e:  # noqa: BLE001 - recorded, never filled in
        out["status"] = f"FAILED: {type(e).__name__}: {e}"[:200]
        return out
    if probe is not None:
        probe["draftkings_league"] = lg
    pages = [lg]
    subs = lg.get("subcategories") or []
    want = [s for s in subs if re.search(r"receiv|recept|rush", str(s.get("name", "")), re.I)]
    for s in want[:8]:
        time.sleep(PAUSE)
        try:
            pages.append(_get(f"{DK}/categories/{s.get('categoryId')}/subcategories/{s.get('id')}"))
        except Exception as e:  # noqa: BLE001
            out.setdefault("errors", []).append(f"subcategory {s.get('name')}: {type(e).__name__}"[:120])
    if probe is not None and len(pages) > 1:
        probe["draftkings_subcategory"] = pages[1]
    for pg in pages:
        evs = {str(e["id"]): e for e in pg.get("events", []) if "id" in e}
        for e in evs.values():
            parts = e.get("participants") or []
            home = next((p.get("name") for p in parts if str(p.get("venueRole", "")).lower() == "home"), None)
            away = next((p.get("name") for p in parts if str(p.get("venueRole", "")).lower() == "away"), None)
            out["events"][str(e["id"])] = {"name": e.get("name"), "home": team_of(home or ""), "away": team_of(away or ""),
                                           "start": e.get("startEventDate")}
        mk = {str(m["id"]): m for m in pg.get("markets", []) if "id" in m}
        for s in pg.get("selections", []):
            m = mk.get(str(s.get("marketId")))
            if not m:
                continue
            mname = (m.get("marketType") or {}).get("name") or m.get("name") or ""
            kind = kind_of(mname) or kind_of(m.get("name", ""))
            if not kind:
                continue
            ev = str(m.get("eventId"))
            players = [p.get("name") for p in (s.get("participants") or []) if str(p.get("type", "")).lower() == "player"]
            player = players[0] if players else (m.get("name", "").split(" Receiving")[0].split(" Rushing")[0].split(" Receptions")[0]
                                                 if kind not in ("spread", "total", "moneyline") else None)
            side = s.get("outcomeType") or s.get("label")
            line = s.get("points")
            if line is None and kind.startswith("alt_"):
                mm = re.search(r"(\d+)\+", str(s.get("label", "")))
                line = float(mm.group(1)) - 0.5 if mm else None
                side = "Over"
            out["rows"].append(_row("draftkings", ev, kind, player, side, line, (s.get("displayOdds") or {}).get("american")))
    out["status"] = "OK" if out["rows"] else "NO_ROWS: endpoint answered but no kept markets were found (format may have changed)"
    return out


# ----------------------------------------------------------------------------------------------- FanDuel
def _fd_markets(doc):
    att = doc.get("attachments") or {}
    return att.get("events") or {}, att.get("markets") or {}


def fanduel(probe: dict | None = None) -> dict:
    out = {"status": None, "rows": [], "events": {}}
    page, st_used, err = None, None, None
    for st in FD_STATES:
        try:
            page = _get(FD_PAGE.format(st=st, ak=FD_AK))
            st_used = st
            break
        except Exception as e:  # noqa: BLE001
            err = f"{st}: {type(e).__name__}: {e}"[:160]
            time.sleep(PAUSE)
    if page is None:
        out["status"] = f"FAILED: {err}"
        return out
    if probe is not None:
        probe["fanduel_page"] = page
    docs = [page]
    evs, _ = _fd_markets(page)
    for eid in list(evs)[:20]:
        for tab in FD_TABS:
            time.sleep(PAUSE)
            try:
                d = _get(FD_EVENT.format(st=st_used, ak=FD_AK, eid=eid, tab=tab))
            except Exception:  # noqa: BLE001 - a missing tab is normal
                continue
            if _fd_markets(d)[1]:
                docs.append(d)
                if probe is not None and "fanduel_event" not in probe:
                    probe["fanduel_event"] = d
    for d in docs:
        e2, mk = _fd_markets(d)
        for eid, e in e2.items():
            nm = e.get("name") or ""
            a, _, h = nm.partition(" @ ")
            out["events"][str(e.get("eventId", eid))] = {"name": nm, "away": team_of(a), "home": team_of(h), "start": e.get("openDate")}
        for m in mk.values():
          try:
            kind = kind_of(m.get("marketName", "")) or kind_of(m.get("marketType", "").replace("_", " "))
            if not kind:
                continue
            ev = str(m.get("eventId"))
            for rn in m.get("runners", []):
                odds = (((rn.get("winRunnerOdds") or {}).get("americanDisplayOdds") or {}).get("americanOdds"))
                name = rn.get("runnerName") or ""
                line = rn.get("handicap")
                side, player = name, None
                lad = re.search(r"(\d+)\+\s*(receptions|yds|yards)", name, re.I)
                if lad:                                  # ladder runner, e.g. "David Njoku 3+ Receptions"
                    player = name[:lad.start()].strip()
                    line, side = float(lad.group(1)) - 0.5, "Over"
                elif kind in ("receiving_yards", "receptions", "rushing_yards"):
                    player = re.sub(r"\s*-\s*.*$", "", m.get("marketName", ""))
                    side = "Over" if "over" in name.lower() else "Under" if "under" in name.lower() else name
                    mm = re.search(r"(\d+(?:\.\d+)?)", name)
                    line = float(mm.group(1)) if (not line and mm) else line
                elif kind.startswith("alt_"):
                    mm = re.search(r"(\d+)\+", name) or re.search(r"(\d+)\+", m.get("marketName", ""))
                    player = re.sub(r"\s*\d+\+.*$", "", name).strip() or None
                    line, side = (float(mm.group(1)) - 0.5 if mm else None), "Over"
                out["rows"].append(_row("fanduel", ev, kind, player, side, line, odds))
          except Exception as e:  # noqa: BLE001 - one odd market never sinks the run
            out.setdefault("errors", []).append(f"{m.get('marketName')}: {type(e).__name__}"[:120])
    out["status"] = "OK" if out["rows"] else "NO_ROWS: endpoint answered but no kept markets were found (format may have changed)"
    out["state"] = st_used
    return out



# ----------------------------------------------------------------------------------------------- Pinnacle
PIN = "https://guest.api.arcadia.pinnacle.com/0.1/leagues/889"
CZR = "https://api.americanwagering.com/regions/us/locations/nj/brands/czr/sb/v3/sports/americanfootball/events/schedule"


def _dec_to_american(p):
    """Pinnacle's guest feed gives American prices already; keep the helper for decimal fallbacks."""
    try:
        p = float(p)
    except (TypeError, ValueError):
        return None
    if abs(p) >= 100:
        return int(p)
    return int(round((p - 1) * 100)) if p >= 2 else int(round(-100 / (p - 1))) if p > 1 else None


def pinnacle(probe: dict | None = None) -> dict:
    """Pinnacle's public guest feed (the one its website reads): game lines and the player specials it posts."""
    out = {"status": None, "rows": [], "events": {}}
    try:
        mu = _get(f"{PIN}/matchups")
        time.sleep(PAUSE)
        mk = _get(f"{PIN}/markets/straight")
    except Exception as e:  # noqa: BLE001 - recorded, never filled in or worked around
        out["status"] = f"FAILED: {type(e).__name__}: {e}"[:200]
        return out
    if probe is not None:
        probe["pinnacle_matchups"], probe["pinnacle_markets"] = mu[:30], mk[:30]
    games, specials = {}, {}
    for m in mu:
        parts = m.get("participants") or []
        if m.get("type") == "matchup" or (parts and all(p.get("alignment") in ("home", "away") for p in parts)):
            home = next((p.get("name") for p in parts if p.get("alignment") == "home"), None)
            away = next((p.get("name") for p in parts if p.get("alignment") == "away"), None)
            if home and away:
                games[m["id"]] = m["id"]
                out["events"][str(m["id"])] = {"name": f"{away} @ {home}", "away": team_of(away), "home": team_of(home), "start": m.get("startTime")}
        elif m.get("special"):
            desc = (m.get("special") or {}).get("description") or ""
            par = (m.get("parent") or {}).get("id")
            mm = re.match(r"(.+?)\s*\((.+)\)", desc) or re.match(r"(.+?)\s+Total\s+(.+)", desc)   # "Chris Olave Total Receiving Yards"
            kind = kind_of(mm.group(2)) if mm else None
            if kind and par:
                specials[m["id"]] = {"event": str(par), "player": mm.group(1).strip(), "kind": kind,
                                     "names": {p.get("id"): p.get("name") for p in parts}}
    for x in mk:
        if x.get("period") not in (0, None) or x.get("isAlternate"):
            continue
        mid = x.get("matchupId")
        if mid in games:
            kind = {"spread": "spread", "total": "total", "moneyline": "moneyline"}.get(x.get("type"))
            if not kind:
                continue
            ev = out["events"].get(str(mid), {})
            for pr in x.get("prices", []):
                d = pr.get("designation")
                side = {"home": ev.get("home"), "away": ev.get("away"), "over": "Over", "under": "Under"}.get(d, d)
                out["rows"].append(_row("pinnacle", str(mid), kind, None, side, pr.get("points"), _dec_to_american(pr.get("price"))))
        elif mid in specials:
            sp = specials[mid]
            for pr in x.get("prices", []):
                side = sp["names"].get(pr.get("participantId")) or pr.get("designation")
                out["rows"].append(_row("pinnacle", sp["event"], sp["kind"], sp["player"], side, pr.get("points"), _dec_to_american(pr.get("price"))))
    out["status"] = "OK" if out["rows"] else "NO_ROWS: endpoint answered but no kept markets were found (format may have changed)"
    return out


# ----------------------------------------------------------------------------------------------- Caesars
def caesars(probe: dict | None = None) -> dict:
    """Caesars' public schedule feed (game lines). Plain request only: a refusal is recorded, not worked around."""
    out = {"status": None, "rows": [], "events": {}}
    try:
        doc = _get(CZR)
    except Exception as e:  # noqa: BLE001
        out["status"] = f"FAILED: {type(e).__name__}: {e}"[:200]
        return out
    if probe is not None:
        probe["caesars_schedule"] = doc
    for comp in doc.get("competitions", []) or []:
        if "nfl" not in str(comp.get("name", "")).lower():
            continue
        for e in comp.get("events", []) or []:
            nm = e.get("name") or ""
            a, _, h = nm.replace("|", "").partition(" at ")
            out["events"][str(e.get("id"))] = {"name": nm, "away": team_of(a), "home": team_of(h), "start": e.get("startTime")}
            for m in e.get("markets", []) or []:
                kind = kind_of(str(m.get("name", "")).replace("|", ""))
                if not kind:
                    continue
                for sel in m.get("selections", []) or []:
                    price = (sel.get("price") or {}).get("a")
                    line = m.get("line") if m.get("line") is not None else sel.get("line")
                    out["rows"].append(_row("caesars", str(e.get("id")), kind, None, str(sel.get("name", "")).replace("|", ""), line, price))
    out["status"] = "OK" if out["rows"] else "NO_ROWS: endpoint answered but no kept markets were found (format may have changed)"
    return out

# ----------------------------------------------------------------------------------------------- run
def _truncate(o, depth=0):
    if depth > 6:
        return "..."
    if isinstance(o, dict):
        return {k: _truncate(v, depth + 1) for k, v in list(o.items())[:25]}
    if isinstance(o, list):
        return [_truncate(v, depth + 1) for v in o[:4]]
    return o


SCHEDULE = "https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv"


def game_ids(index: Path) -> dict:
    """(away, home) -> nflverse game_id for every unplayed game this season (schedule), else the current slate index."""
    ids = {}
    try:
        import csv
        import io
        txt = urllib.request.urlopen(urllib.request.Request(SCHEDULE, headers={"User-Agent": "nfl-matchup-database"}), timeout=30).read().decode()
        rows = list(csv.DictReader(io.StringIO(txt)))
        season = max(int(r["season"]) for r in rows)
        for r in rows:
            if int(r["season"]) == season and not r.get("home_score"):
                ids.setdefault((r["away_team"], r["home_team"]), r["game_id"])
    except Exception:  # noqa: BLE001 - fall back to the slate index
        pass
    try:
        for g in json.loads(index.read_text())["games"]:
            ids.setdefault((g["away"], g["home"]), g["game_id"])
    except (OSError, ValueError, KeyError):
        pass
    return ids


def run(probe=False, out_dir: Path = OUT, index: Path = ROOT / "pregame" / "packets" / "latest.json") -> dict:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    pr = {} if probe else None
    books = {"draftkings": draftkings(pr), "fanduel": fanduel(pr), "pinnacle": pinnacle(pr), "caesars": caesars(pr)}
    ids = game_ids(index)
    per_game = {}
    for name, b in books.items():
        for r in b["rows"]:
            ev = b["events"].get(r["event"], {})
            gid = ids.get((ev.get("away"), ev.get("home")))
            if gid:
                rr = {k: v for k, v in r.items() if k != "event"}
                key = tuple(rr.get(k) for k in ("book", "market", "player", "side", "line"))
                per_game.setdefault(gid, {}).setdefault(key, rr)      # the same market appears on several pages
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {"retrieved_utc": now, "books": {k: {"status": v["status"], "rows": len(v["rows"]), "events": len(v["events"]),
                                                   **({"errors": v["errors"]} if v.get("errors") else {}), **({"state": v["state"]} if v.get("state") else {})}
                                               for k, v in books.items()}, "games": {}}
    for gid, rows in per_game.items():
        rows = list(rows.values())
        rec = {"game_id": gid, "retrieved_utc": now, "source": "book websites' public JSON (unofficial)", "rows": rows}
        (out_dir / f"{gid}.json").write_text(json.dumps(rec, indent=1) + "\n")
        summary["games"][gid] = {b: sum(1 for r in rows if r["book"] == b) for b in books}
    (out_dir / "latest.json").write_text(json.dumps(summary, indent=1) + "\n")
    if probe:
        (out_dir / "_probe").mkdir(exist_ok=True)
        (out_dir / "_probe" / "samples.json").write_text(json.dumps(_truncate(pr), indent=1, default=str)[:400_000] + "\n")
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--probe", action="store_true", help="also keep truncated raw responses for checking the parser")
    a = ap.parse_args(argv)
    s = run(probe=a.probe)
    for k, v in s["books"].items():
        print(f"sportsbooks: {k}: {v['status']} ({v['rows']} rows, {v['events']} events)")
    print(f"sportsbooks: {len(s['games'])} slate games matched")
    return 0 if any(v["rows"] for v in s["books"].values()) else 3


if __name__ == "__main__":
    sys.exit(main())
