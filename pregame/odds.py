"""Book prices, no-vig probabilities and line movement for a pregame packet.

Source: The Odds API (the-odds-api.com), key from the ODDS_API_KEY environment variable / repository secret. Books: FanDuel,
DraftKings, Hard Rock Bet, Caesars (williamhill_us), and Pinnacle as the sharp reference (never in a consensus). Every paid
call is estimated first and refused if it would leave fewer than ODDS_CREDIT_FLOOR (default 800) credits.
Without a key every function returns a labelled "NO_KEY" status and the packet carries no book prices: nothing
is ever invented. De-vigging is done here, in code, so a chat model never does the arithmetic.

Line movement is "first seen by this pipeline -> now": each run appends a snapshot to
pregame/line_history/<game_id>.jsonl. It is not the true opening line unless the pipeline was running at open.
"""
from __future__ import annotations

import json
import math
import os
import re
import statistics
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl"
SHARP = "pinnacle"                                   # reference only: never part of a consensus
RETAIL = ("fanduel", "draftkings", "hardrockbet", "williamhill_us")   # williamhill_us = Caesars on The Odds API
BOOKS = (SHARP,) + RETAIL
BOOK_LABEL = {"pinnacle": "Pinnacle", "fanduel": "FanDuel", "draftkings": "DraftKings", "hardrockbet": "Hard Rock Bet",
              "williamhill_us": "Caesars"}
GAME_MARKETS = ("h2h", "spreads", "totals")
PROP_MARKETS = ("player_pass_yds", "player_pass_attempts", "player_pass_completions", "player_rush_yds", "player_rush_attempts",
                "player_reception_yds", "player_receptions")
PROP_STAT = {"player_pass_yds": "passing_yards", "player_pass_attempts": "passing_attempts", "player_pass_completions": "completions",
             "player_rush_yds": "rushing_yards", "player_rush_attempts": "carries", "player_reception_yds": "receiving_yards",
             "player_receptions": "receptions"}
NEVER_A_LEG = {"passing_yards": "Rico rule: passing-yards legs are banned. Kept as a reference field only."}
DEFAULT_FLOOR = int(os.environ.get("ODDS_CREDIT_FLOOR", "800") or 800)
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


QUOTA = {}   # last credit counters reported by the provider (x-requests-* response headers)


def _get(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "nfl-pregame-packet/1.0"}), timeout=timeout) as r:
        for k, name in (("x-requests-remaining", "credits_remaining"), ("x-requests-used", "credits_used"), ("x-requests-last", "last_call_cost")):
            v = r.headers.get(k)
            if v is not None:
                try:
                    QUOTA[name] = int(float(v))
                except ValueError:
                    pass
        return json.loads(r.read())


def quota(calls_this_run=None) -> dict:
    """Credits left on the key, as last reported by the provider. Empty when no call was made."""
    q = dict(QUOTA)
    if q.get("credits_remaining") is not None:
        q["warning"] = ("LOW: under 100 credits left; props and prices will stop when it reaches 0" if q["credits_remaining"] < 100 else None)
    return q


def _q(key, **params):
    return urllib.parse.urlencode({"apiKey": key, "oddsFormat": "american", "bookmakers": ",".join(BOOKS), **params})


def estimate_cost(n_markets: int, n_books: int = len(BOOKS)) -> int:
    """The Odds API charge for one odds call: markets x region units (each 10 bookmakers is one unit). It is an upper
    bound: the provider bills only markets it returns. The bulk /odds call costs the same for one game or the slate."""
    return int(n_markets) * max(1, math.ceil(n_books / 10))


def floor_check(remaining, estimate: int, floor: int = DEFAULT_FLOOR):
    """Fail closed: an unknown balance, or a call that would leave fewer than `floor` credits, is refused."""
    if remaining is None:
        return False, "SKIPPED_UNKNOWN_BALANCE: credit balance unknown; paid call refused"
    if remaining - estimate < floor:
        return False, f"SKIPPED_CREDIT_FLOOR: {remaining} - {estimate} < floor {floor}"
    return True, f"OK: {remaining} - {estimate} = {remaining - estimate} >= floor {floor}"


def read_balance(key, fetch=_get):
    """Read the live balance from the free /events list (costs 0 credits). None when it cannot be read."""
    QUOTA.pop("credits_remaining", None)          # never trust an earlier reading: unknown stays unknown
    fetch(f"{API}/events?{urllib.parse.urlencode({'apiKey': key})}")   # a network failure propagates as UNAVAILABLE
    return QUOTA.get("credits_remaining")


CREDIT_LOG = []   # one entry per paid-call decision this process made: estimate, floor check, balance after


def _guard(key, fetch, n_markets, floor, what):
    """None when the call may go ahead; otherwise the refusal status. floor=None disables the guard (tests only)."""
    if floor is None:
        return None
    est = estimate_cost(n_markets)
    before = read_balance(key, fetch)
    ok, why = floor_check(before, est, floor)
    CREDIT_LOG.append({"call": what, "estimate_credits": est, "balance_before": before, "floor": floor, "decision": why})
    return None if ok else why


def fetch_game_lines(key=None, fetch=_get, floor=DEFAULT_FLOOR) -> dict:
    """All upcoming games, main markets, all five books. One request (3 credits)."""
    key = key if key is not None else os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        return {"status": "NO_KEY: set the ODDS_API_KEY repository secret to include book prices", "events": {}}
    try:
        refused = _guard(key, fetch, len(GAME_MARKETS), floor, "game_lines")
        if refused:
            return {"status": refused, "events": {}}
        data = fetch(f"{API}/odds?{_q(key, markets=','.join(GAME_MARKETS))}")
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}".replace(key, "***"), "events": {}}
    if CREDIT_LOG and floor is not None:
        CREDIT_LOG[-1].update(balance_after=QUOTA.get("credits_remaining"), actual_credits=QUOTA.get("last_call_cost"))
    events = {}
    for e in data:
        h, a = TEAM.get(e.get("home_team")), TEAM.get(e.get("away_team"))
        if h and a:
            events[(a, h)] = e
    return {"status": "OK", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "events": events}


def fetch_props(event_id, key=None, fetch=_get, markets=PROP_MARKETS, floor=DEFAULT_FLOOR) -> dict:
    """One game's player props, all five books (at most len(markets) credits)."""
    key = key if key is not None else os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        return {"status": "NO_KEY", "event": None}
    try:
        refused = _guard(key, fetch, len(markets), floor, f"props:{event_id}")
        if refused:
            return {"status": refused, "event": None}
        ev = fetch(f"{API}/events/{event_id}/odds?{_q(key, markets=','.join(markets))}")
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}".replace(key, "***"), "event": None}
    if CREDIT_LOG and floor is not None:
        CREDIT_LOG[-1].update(balance_after=QUOTA.get("credits_remaining"), actual_credits=QUOTA.get("last_call_cost"))
    return {"status": "OK", "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "event": ev}


def credit_line(start_remaining=None) -> str:
    """'credits used this run=X remaining=Y'; either is 'unknown' when not reported by the provider."""
    rem = QUOTA.get("credits_remaining")
    first = start_remaining if start_remaining is not None else next((c["balance_before"] for c in CREDIT_LOG if c.get("balance_before") is not None), None)
    used = (first - rem) if None not in (first, rem) else None
    return f"odds credits used this run={'unknown' if used is None else used} remaining={'unknown' if rem is None else rem}"


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


# ---------------------------------------------------------------------------------------------------------------
# Same-line consensus, player matching and timestamped freezes. One pull (fetch_game_lines + fetch_props) feeds the
# packet's book-price section and the freeze; there is no second credit spend.

_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
_SUFFIX = {"jr", "sr", "ii", "iii", "iv", "v"}


def norm_name(name) -> str:
    """'D'Andre Swift Jr.' -> 'dandre swift'. Accents, punctuation and generational suffixes are dropped."""
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`\u2019]", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s).split()
    while s and s[-1] in _SUFFIX:
        s.pop()
    return " ".join(s)


def _is_full_name(name) -> bool:
    """'J.J. McCarthy' and 'Malik Nabers' are full names; the play-by-play form 'S.Diggs' (one token) is not."""
    return len(str(name).split()) >= 2


def roster_from_packet(pk) -> dict:
    """{team: {normalized full name: {display names}}} from the packet's own player lists: depth chart (starters, second
    string), the official injury report and ESPN's live injury list. Abbreviated play-by-play names ('S.Diggs') are not
    used, so every match is on a full name."""
    out = {}
    for team, t in (pk.get("teams") or {}).items():
        names = {}
        dc = t.get("depth_chart") or {}
        inj = t.get("injuries") or {}
        for lst in (dc.get("starters"), dc.get("second_string"), dc.get("third_string"), inj.get("official_report"), inj.get("espn_live")):
            for r in lst or []:
                n = r.get("player") if isinstance(r, dict) else None
                if n and _is_full_name(n):
                    names.setdefault(norm_name(n), set()).add(str(n).strip())
        out[team] = names
    return out


def match_player(name, roster, home=None, away=None) -> dict:
    """Full-name + team match. Fail closed: a name on both teams, on neither, or spelled two different ways on one team
    (two people) is not matched, and its market gets no consensus."""
    n = norm_name(name)
    hits = [team for team, names in roster.items() if n in names]
    if not hits:
        return {"status": "UNMATCHED", "team": None, "reason": f"'{name}' is not on either team's packet player list"}
    if len(hits) > 1:
        return {"status": "AMBIGUOUS", "team": None, "reason": f"'{name}' matches players on {', '.join(sorted(hits))}"}
    spellings = roster[hits[0]][n]
    if len({s.replace(".", "").lower() for s in spellings}) > 1:
        return {"status": "AMBIGUOUS", "team": None, "reason": f"'{name}' matches {len(spellings)} differently written names on {hits[0]}: {sorted(spellings)}"}
    return {"status": "MATCHED", "team": hits[0], "reason": None}


def _books_with_props(markets) -> set:
    return {b for label, m in markets.items() if "|" in label for b in m["books"]}


def consensus(markets: dict, roster: dict | None = None) -> dict:
    """Per market: each retail book's own line, then a consensus from books at the SAME line only.

    The consensus line is the line quoted by the most retail books. Its no-vig probability is the mean of those books'
    no-vig probabilities, all at that one line; probabilities quoted at different lines are never averaged and no line is
    adjusted. Fewer than two books on one line, or a tie between lines, gives the literal 'no consensus' with a reason.
    Pinnacle is shown as a reference and never counted. Player props need a full-name + team match first."""
    with_props = _books_with_props(markets)
    out = {}
    for label, m in markets.items():
        is_prop = "|" in label
        stat, player = label.split("|", 1) if is_prop else (label, None)
        a, b = m["sides"]
        own = {}
        for book in RETAIL:
            q = m["books"].get(book)
            if q:
                own[book] = q["line"]
            elif is_prop and book not in with_props:
                own[book] = "no props"
            else:
                own[book] = "not offered"
        quoting = [bk for bk in RETAIL if bk in m["books"]]
        n = len(quoting)
        kind = "prop" if is_prop else "game-line"
        rec = {"market": label, "stat": stat, "player": player, "sides": [a, b], "book_lines": own, "n_books_quoting": n,
               "label": f"{_WORDS.get(n, str(n))}-book {kind} consensus" if n else f"no retail {kind} quotes",
               "reference": ({"book": SHARP, "line": m["books"][SHARP]["line"], "no_vig": m["books"][SHARP]["no_vig"]}
                             if SHARP in m["books"] else {"book": None, "note": "Pinnacle did not list this market"})}
        if stat in NEVER_A_LEG:
            rec["never_a_leg"] = True
            rec["never_a_leg_reason"] = NEVER_A_LEG[stat]
        if is_prop:
            mt = match_player(player, roster or {}) if roster is not None else {"status": "UNMATCHED", "team": None, "reason": "no packet roster supplied"}
            rec.update(team=mt["team"], match=mt["status"], match_reason=mt["reason"])
            if mt["status"] != "MATCHED":
                rec.update(consensus="no consensus", reason=f"player match failed closed: {mt['reason']}")
                out[label] = rec
                continue
        by_line = {}
        for bk in quoting:
            by_line.setdefault(m["books"][bk]["line"], []).append(bk)
        if not by_line:
            rec.update(consensus="no consensus", reason="no retail book quotes this market")
        else:
            top = max(len(v) for v in by_line.values())
            lead = [ln for ln, v in by_line.items() if len(v) == top]
            if top < 2:
                rec.update(consensus="no consensus", reason=f"fewer than 2 books share a line ({', '.join(f'{BOOK_LABEL[bk]} {own[bk]}' for bk in quoting)})")
            elif len(lead) > 1:
                rec.update(consensus="no consensus", reason=f"books split evenly between lines {sorted(lead, key=lambda x: (x is None, x))}")
            else:
                ln, at = lead[0], by_line[lead[0]]
                rec.update(consensus={"line": ln, "n_books_at_line": len(at), "books_at_line": at,
                                      "no_vig": {s: round(statistics.mean(m["books"][bk]["no_vig"][s] for bk in at), 4) for s in (a, b)},
                                      "books_off_line": {bk: own[bk] for bk in quoting if bk not in at}},
                           reason=None)
        out[label] = rec
    return out


def write_freeze(game_id, away, home, markets, cons, raw, out_dir: Path, meta=None, now=None) -> dict:
    """Write raw_<UTC>.json (response bodies, never the key), freeze_<UTC>.json and table_<UTC>.md for one game."""
    from zoneinfo import ZoneInfo
    now = now or datetime.now(timezone.utc)
    et = now.astimezone(ZoneInfo("America/New_York"))
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    d = Path(out_dir) / f"{et:%Y-%m-%d}_{away}@{home}"
    d.mkdir(parents=True, exist_ok=True)
    raw_b = json.dumps(raw, indent=1, sort_keys=True).encode()
    import hashlib
    m = {"schema": "price-freeze/2", "game_id": game_id, "game": f"{away}@{home}", "source": "The Odds API v4 (the-odds-api.com)",
         "pulled_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "pulled_et": f"{et:%Y-%m-%d %I:%M %p} ET", "books": list(BOOKS),
         "consensus_books": list(RETAIL), "reference_book": SHARP, "devig": "two-way multiplicative (proportional)",
         "consensus_rule": "same line only; mean no-vig of books at the modal line; <2 books or a tie = 'no consensus'",
         "credits": list(CREDIT_LOG), "credit_summary": credit_line(), "raw_sha256": hashlib.sha256(raw_b).hexdigest(),
         "projection_ready": False, "research_only": True, **(meta or {})}
    (d / f"raw_{stamp}.json").write_bytes(raw_b)
    (d / f"freeze_{stamp}.json").write_text(json.dumps({"meta": m, "markets": markets, "consensus": cons}, indent=1, sort_keys=True, default=str) + "\n")
    (d / f"table_{stamp}.md").write_text(consensus_table(m, cons))
    m["files"] = [str(d / f"{p}_{stamp}.{x}") for p, x in (("raw", "json"), ("freeze", "json"), ("table", "md"))]
    return m


def _fmt(x):
    return "" if x is None else (f"{x:g}" if isinstance(x, (int, float)) else str(x))


def consensus_table(meta, cons) -> str:
    L = [f"# {meta['game']} price freeze ({meta['pulled_et']}; {meta['pulled_utc']} UTC)", "",
         f"Source: {meta['source']}. Research only, projection_ready=false. De-vig: {meta['devig']}. Consensus: {meta['consensus_rule']}. "
         f"Pinnacle is reference only. {meta['credit_summary']}.", "",
         "| Market | Team | Label | " + " | ".join(BOOK_LABEL[b] for b in RETAIL) + " | Consensus line | n at line | No-vig A | Pinnacle line | Pinnacle no-vig A | Note |",
         "|" + "---|" * (9 + len(RETAIL))]
    for label, c in sorted(cons.items(), key=lambda kv: ("|" in kv[0], kv[0])):
        a = c["sides"][0]
        cc = c["consensus"]
        ref = c["reference"]
        note = "; ".join(x for x in (c.get("reason"), "NEVER A LEG (reference only)" if c.get("never_a_leg") else None) if x)
        L.append(f"| {label} | {c.get('team') or ''} | {c['label']} | " + " | ".join(_fmt(c["book_lines"][b]) for b in RETAIL)
                 + f" | {cc if isinstance(cc, str) else _fmt(cc['line'])} {'' if isinstance(cc, str) else a} | {'' if isinstance(cc, str) else cc['n_books_at_line']} | "
                 + f"{'' if isinstance(cc, str) else cc['no_vig'][a]} | {_fmt(ref.get('line')) if ref.get('book') else 'n/a'} | "
                 + f"{ref['no_vig'].get(a, '') if ref.get('book') else 'n/a'} | {note} |")
    return "\n".join(L) + "\n"


def _old_freeze_markets(f) -> dict:
    """Map a schema-1 multibook freeze (11:14 AM ET, rows with full team names, away-side spread) to summarize_event's shape."""
    out = {}
    for r in f.get("rows", []):
        mk = {"h2h": "moneyline", "spreads": "spread", "totals": "total"}.get(r["market"]) or f"{PROP_STAT.get(r['market'], r['market'])}|{r['player']}"
        sa, sb = TEAM.get(r["side_a"], r["side_a"]), TEAM.get(r["side_b"], r["side_b"])
        line = r["line"]
        if mk == "spread":   # schema 1 stored the away line; summarize_event stores the home line
            line = -line if line is not None else None
        out.setdefault(mk, {"books": {}})["books"][r["book"]] = {"line": line, "prices": {sa: r["price_a"], sb: r["price_b"]},
                                                                  "no_vig": {sa: r["novig_a"], sb: r["novig_b"]}}
    return out


def movement_vs_freeze(markets: dict, old_freeze: dict) -> list[dict]:
    """Per market and book: line, prices and no-vig in an earlier freeze against now. Reads schema 1 and 2 freezes."""
    old = old_freeze.get("markets") or _old_freeze_markets(old_freeze)
    rows = []
    for label, m in markets.items():
        for book, q in m["books"].items():
            o = (old.get(label) or {}).get("books", {}).get(book)
            if not o:
                rows.append({"market": label, "book": book, "then": "not quoted", "now_line": q["line"], "now_prices": q["prices"]})
                continue
            r = {"market": label, "book": book, "then_line": o["line"], "now_line": q["line"], "then_prices": o["prices"], "now_prices": q["prices"],
                 "then_no_vig": o["no_vig"], "now_no_vig": q["no_vig"]}
            if isinstance(o["line"], (int, float)) and isinstance(q["line"], (int, float)):
                r["line_move"] = round(q["line"] - o["line"], 2)
            rows.append(r)
    return rows
