"""Four-book pregame price feed with per-book no-vig, consensus and timestamped freezes (research only).

Books: FanDuel, DraftKings, Hard Rock Bet, Caesars (The Odds API key williamhill_us), plus Pinnacle as the
sharp reference (kept out of the consensus). Source: The Odds API v4, key from the ODDS_API_KEY environment
variable. The key is never written to disk, logged or printed; raw freezes store the response bodies only.

Credits: an event-odds call costs (number of markets) x ceil(books / 10). Five books is one unit, so game lines
(h2h, spreads, totals) cost 3 and the two prop markets (rush yds, receiving yds) cost 2: 5 per full pull.
The /events list is free and is used to read the live balance first. Before each paid call the estimate is
checked against a credit floor (default 800); if remaining - estimate < floor the call is skipped and the
freeze says SKIPPED_CREDIT_FLOOR. Nothing is invented when a book or market is missing: it is reported absent.

No-vig is two-way multiplicative (each side's implied probability divided by the pair's sum), per book, per
line. Consensus uses only the four target books: median line, and the mean no-vig probability of the books
quoting that exact line. projection_ready stays false; this module produces prices, not picks.

    python -m pregame.multibook --home NYG --away WAS --out pregame/price_freezes [--floor 800] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import statistics
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from pregame.odds import TEAM, devig, implied
except ImportError:  # run as a script from inside pregame/
    from odds import TEAM, devig, implied  # type: ignore

API = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl"
TARGET_BOOKS = ("fanduel", "draftkings", "hardrockbet", "williamhill_us")
REFERENCE_BOOK = "pinnacle"
ALL_BOOKS = TARGET_BOOKS + (REFERENCE_BOOK,)
BOOK_LABEL = {"fanduel": "FanDuel", "draftkings": "DraftKings", "hardrockbet": "Hard Rock Bet",
              "williamhill_us": "Caesars", "pinnacle": "Pinnacle (reference)"}
GAME_MARKETS = ("h2h", "spreads", "totals")
PROP_MARKETS = ("player_rush_yds", "player_reception_yds")
DEFAULT_FLOOR = 800
ET = ZoneInfo("America/New_York")

# Key props in use for WAS@NYG (Week 10 TNF). Matched on the book's player description.
# (market, last name, optional first-name prefix)
WAS_NYG_PROPS = (
    ("player_rush_yds", "Skattebo", None),
    ("player_rush_yds", "Daniels", "Jayden"),
    ("player_reception_yds", "Nabers", None),
    ("player_reception_yds", "Likely", None),
    ("player_reception_yds", "Fields", None),
    ("player_reception_yds", "Diggs", None),
    ("player_reception_yds", "Okonkwo", None),
    ("player_reception_yds", "Williams", "A"),
)


def estimate_cost(n_markets: int, n_books: int = len(ALL_BOOKS)) -> int:
    """The Odds API charge for one event-odds call: markets x region units (10 bookmakers per unit)."""
    return int(n_markets) * max(1, math.ceil(n_books / 10))


def floor_check(remaining, estimate: int, floor: int = DEFAULT_FLOOR) -> tuple[bool, str]:
    """Fail closed: unknown balance or a pull that would end below the floor is refused."""
    if remaining is None:
        return False, "UNKNOWN_BALANCE: credit balance not read; refusing paid call"
    if remaining - estimate < floor:
        return False, f"SKIPPED_CREDIT_FLOOR: {remaining} - {estimate} < floor {floor}"
    return True, f"OK: {remaining} - {estimate} = {remaining - estimate} >= floor {floor}"


class Client:
    """Thin HTTP client. Records credit headers; never exposes the key."""

    def __init__(self, key=None, opener=None):
        self._key = (key if key is not None else os.environ.get("ODDS_API_KEY", "")).strip()
        self._open = opener or self._urlopen
        self.quota = {}
        self.calls = []

    @property
    def has_key(self):
        return bool(self._key)

    @staticmethod
    def _urlopen(url):
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "nfl-multibook/1.0"}), timeout=30) as r:
            return dict(r.headers), r.read()

    def get(self, path, **params):
        q = urllib.parse.urlencode({"apiKey": self._key, **params})
        headers, body = self._open(f"{API}{path}?{q}")
        h = {k.lower(): v for k, v in headers.items()}
        for k, name in (("x-requests-remaining", "remaining"), ("x-requests-used", "used"), ("x-requests-last", "last")):
            if h.get(k) is not None:
                try:
                    self.quota[name] = int(float(h[k]))
                except ValueError:
                    pass
        self.calls.append({"path": path, "markets": params.get("markets"), "last_cost": self.quota.get("last"),
                           "remaining_after": self.quota.get("remaining"), "utc": _utc()})
        return json.loads(body)


def _utc(now=None):
    return (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_event(events, home: str, away: str):
    for e in events:
        if TEAM.get(e.get("home_team")) == home and TEAM.get(e.get("away_team")) in (away, "WSH" if away == "WAS" else away):
            return e
    return None


def _pair_outcomes(market_key, outcomes, home_name, away_name):
    """Yield (selection_a, selection_b, line, price_a, price_b, player) two-way pairs from one book market."""
    if market_key == "h2h":
        by = {o["name"]: o for o in outcomes}
        if home_name in by and away_name in by:
            yield (away_name, home_name, None, by[away_name]["price"], by[home_name]["price"], None)
    elif market_key == "spreads":
        by = {o["name"]: o for o in outcomes}
        if home_name in by and away_name in by and by[home_name].get("point") is not None:
            if abs(by[home_name]["point"] + by[away_name]["point"]) < 1e-9:
                yield (away_name, home_name, by[away_name]["point"], by[away_name]["price"], by[home_name]["price"], None)
    else:  # totals and player props: Over/Under at the same point (and same player)
        groups = {}
        for o in outcomes:
            groups.setdefault((o.get("description"), o.get("point")), {})[o["name"]] = o
        for (player, point), sides in groups.items():
            if "Over" in sides and "Under" in sides:
                yield ("Over", "Under", point, sides["Over"]["price"], sides["Under"]["price"], player)


def normalize(event_json, home_abbr: str, away_abbr: str) -> list[dict]:
    """Flatten one event-odds response into per-book two-way rows with multiplicative no-vig."""
    home_name, away_name = event_json["home_team"], event_json["away_team"]
    rows = []
    for bm in event_json.get("bookmakers", []):
        for m in bm.get("markets", []):
            for a, b, line, pa, pb, player in _pair_outcomes(m["key"], m.get("outcomes", []), home_name, away_name):
                try:
                    fa, fb, hold = devig(pa, pb)
                except (ValueError, ZeroDivisionError):
                    continue
                rows.append({"book": bm["key"], "book_label": BOOK_LABEL.get(bm["key"], bm["key"]),
                             "reference_only": bm["key"] == REFERENCE_BOOK, "market": m["key"], "player": player,
                             "line": line, "side_a": a, "side_b": b, "price_a": pa, "price_b": pb,
                             "implied_a": round(implied(pa), 4), "implied_b": round(implied(pb), 4),
                             "novig_a": round(fa, 4), "novig_b": round(fb, 4), "hold": round(hold, 4),
                             "book_last_update": m.get("last_update") or bm.get("last_update")})
    return rows


def _main_line(rows):
    """Per book, the line whose two prices are closest to even (the book's main line for alt-heavy markets)."""
    best = {}
    for r in rows:
        k = r["book"]
        score = abs(r["novig_a"] - 0.5)
        if k not in best or score < best[k][0]:
            best[k] = (score, r)
    return [v[1] for v in best.values()]


def consensus(rows: list[dict]) -> list[dict]:
    """One row per (market, player): the four target books' median main line and mean no-vig at that line,
    with Pinnacle's main line shown alongside as the reference."""
    out = []
    keys = sorted({(r["market"], r["player"] or "") for r in rows})
    for market, player in keys:
        grp = [r for r in rows if r["market"] == market and (r["player"] or "") == player]
        mains = _main_line(grp)
        tgt = [r for r in mains if not r["reference_only"]]
        ref = [r for r in mains if r["reference_only"]]
        rec = {"market": market, "player": player or None, "books_quoting": sorted(r["book"] for r in tgt),
               "books_missing": sorted(set(TARGET_BOOKS) - {r["book"] for r in tgt})}
        if tgt:
            lines = [r["line"] for r in tgt if r["line"] is not None]
            med = statistics.median(lines) if lines else None
            at = [r for r in tgt if r["line"] == med] if med is not None else tgt
            if not at:  # median falls between two quoted lines: use all main lines
                at = tgt
            rec.update({"consensus_line": med, "side_a": tgt[0]["side_a"], "side_b": tgt[0]["side_b"],
                        "consensus_novig_a": round(statistics.mean(r["novig_a"] for r in at), 4),
                        "n_books_at_line": len([r for r in tgt if r["line"] == med]),
                        "line_range": [min(lines), max(lines)] if lines else None})
        if ref:
            rec.update({"pinnacle_line": ref[0]["line"], "pinnacle_novig_a": ref[0]["novig_a"]})
        out.append(rec)
    return out


def select_props(rows, wanted=WAS_NYG_PROPS):
    keep = []
    for r in rows:
        if r["market"] in GAME_MARKETS:
            continue
        name = (r["player"] or "").split()
        for market, last, first in wanted:
            if r["market"] == market and name and name[-1] == last and (first is None or name[0].startswith(first)):
                keep.append(r)
                break
    return keep


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(home="NYG", away="WAS", out="pregame/price_freezes", floor=DEFAULT_FLOOR, client=None, now=None,
        dry_run=False, props=WAS_NYG_PROPS) -> dict:
    """Pull game lines then props for one game, freeze raw + normalized JSON and a CSV table. Fail closed."""
    client = client or Client()
    now = now or datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    meta = {"game": f"{away}@{home}", "pulled_utc": _utc(now), "pulled_et": now.astimezone(ET).strftime("%Y-%m-%d %I:%M %p ET"),
            "books": list(ALL_BOOKS), "consensus_books": list(TARGET_BOOKS), "reference_book": REFERENCE_BOOK,
            "floor": floor, "devig": "two-way multiplicative (proportional)", "projection_ready": False,
            "research_only": True, "steps": []}
    if not client.has_key:
        meta["status"] = "NO_KEY: ODDS_API_KEY not set; no prices"
        return meta
    events = client.get("/events")  # free; also returns the live balance
    meta["credits_before"] = client.quota.get("remaining")
    ev = find_event(events, home, away)
    if ev is None:
        meta["status"] = f"EVENT_NOT_FOUND: {away}@{home} not in /events"
        return meta
    meta.update(event_id=ev["id"], commence_utc=ev["commence_time"],
                commence_et=datetime.fromisoformat(ev["commence_time"].replace("Z", "+00:00")).astimezone(ET).strftime("%Y-%m-%d %I:%M %p ET"))
    if datetime.fromisoformat(ev["commence_time"].replace("Z", "+00:00")) <= now:
        meta["status"] = "IN_PLAY_OR_STARTED: pregame freeze refused"
        return meta
    odir = Path(out) / f"{now.astimezone(ET).strftime('%Y-%m-%d')}_{away}@{home}"
    rows, raw = [], {}
    for label, markets in (("game_lines", GAME_MARKETS), ("props", PROP_MARKETS)):
        est = estimate_cost(len(markets))
        ok, why = floor_check(client.quota.get("remaining"), est, floor)
        step = {"step": label, "markets": list(markets), "estimate_credits": est, "floor_check": why}
        meta["steps"].append(step)
        if not ok or dry_run:
            step["status"] = "DRY_RUN" if (ok and dry_run) else why.split(":")[0]
            continue
        js = client.get(f"/events/{ev['id']}/odds", regions="us", oddsFormat="american",
                        bookmakers=",".join(ALL_BOOKS), markets=",".join(markets))
        step.update(status="PULLED", actual_credits=client.quota.get("last"), remaining_after=client.quota.get("remaining"),
                    books_returned=sorted(b["key"] for b in js.get("bookmakers", [])))
        raw[label] = js
        got = normalize(js, home, away)
        rows += got if label == "game_lines" else select_props(got, props)
    meta["credits_after"] = client.quota.get("remaining")
    meta["credits_used_this_run"] = (meta["credits_before"] - meta["credits_after"]) if None not in (meta.get("credits_before"), meta.get("credits_after")) else None
    meta["status"] = "OK" if all(s.get("status") == "PULLED" for s in meta["steps"]) else "PARTIAL_OR_SKIPPED"
    meta["consensus"] = consensus(rows)
    wanted_found = {(r["market"], r["player"]) for r in rows if r["player"]}
    meta["props_missing"] = [f"{m}:{(f + '. ') if f else ''}{l}" for m, l, f in props
                             if not any(k[0] == m and k[1].split()[-1] == l for k in wanted_found)]
    if dry_run:
        return meta
    odir.mkdir(parents=True, exist_ok=True)
    raw_b = json.dumps(raw, indent=1, sort_keys=True).encode()
    (odir / f"raw_{stamp}.json").write_bytes(raw_b)
    meta["raw_sha256"] = _sha(raw_b)
    norm = {"meta": meta, "rows": rows}
    norm_b = json.dumps(norm, indent=1, sort_keys=True, default=str).encode()
    (odir / f"freeze_{stamp}.json").write_bytes(norm_b)
    (odir / f"table_{stamp}.md").write_text(render_table(meta, rows))
    meta["files"] = [str(odir / f"{p}_{stamp}.{x}") for p, x in (("raw", "json"), ("freeze", "json"), ("table", "md"))]
    return meta


def _am(p):
    return f"+{p}" if p > 0 else str(p)


def render_table(meta, rows) -> str:
    L = [f"# {meta['game']} price freeze ({meta['pulled_et']}; {meta['pulled_utc']})", "",
         f"Research only, projection_ready=false. De-vig: {meta['devig']}. Consensus = FanDuel, DraftKings, Hard Rock Bet, "
         f"Caesars; Pinnacle is reference only. Credits {meta.get('credits_before')} -> {meta.get('credits_after')}.", "",
         "| Market | Player | Book | Line | Side A | Price A | Side B | Price B | No-vig A | No-vig B | Hold |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    order = {b: i for i, b in enumerate(ALL_BOOKS)}
    for r in sorted(rows, key=lambda r: (r["market"], r["player"] or "", order.get(r["book"], 9), r["line"] or 0)):
        L.append(f"| {r['market']} | {r['player'] or ''} | {r['book_label']} | {'' if r['line'] is None else r['line']} | {r['side_a']} | "
                 f"{_am(r['price_a'])} | {r['side_b']} | {_am(r['price_b'])} | {r['novig_a']:.3f} | {r['novig_b']:.3f} | {r['hold']:.3f} |")
    L += ["", "## Consensus (main line per book)", "", "| Market | Player | Line | No-vig A | Books | Missing | Pinnacle line | Pinnacle no-vig A |",
          "|---|---|---|---|---|---|---|---|"]
    for c in meta.get("consensus", []):
        L.append(f"| {c['market']} | {c['player'] or ''} | {'' if c.get('consensus_line') is None else c['consensus_line']} {c.get('side_a', '')} | {c.get('consensus_novig_a', '')} | "
                 f"{', '.join(c['books_quoting'])} | {', '.join(c['books_missing'])} | {'' if c.get('pinnacle_line') is None else c['pinnacle_line']} | {c.get('pinnacle_novig_a', 'n/a')} |")
    if meta.get("props_missing"):
        L += ["", "Props not offered by any of the five books at pull time: " + ", ".join(meta["props_missing"])]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--home", default="NYG"); ap.add_argument("--away", default="WAS")
    ap.add_argument("--out", default="pregame/price_freezes"); ap.add_argument("--floor", type=int, default=DEFAULT_FLOOR)
    ap.add_argument("--dry-run", action="store_true", help="read the free balance and print the cost plan; no paid call")
    a = ap.parse_args(argv)
    meta = run(a.home, a.away, a.out, a.floor, dry_run=a.dry_run)
    print(json.dumps({k: v for k, v in meta.items() if k != "consensus"}, indent=1, default=str))
    return 0 if meta.get("status") in ("OK",) or a.dry_run else 2


if __name__ == "__main__":
    sys.exit(main())
