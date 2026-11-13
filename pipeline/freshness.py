"""Freshness policy for pregame inputs (NFL-56 item 2). Human-readable copy: docs/DATA_FRESHNESS.md.

Each source has a maximum age. Some tighten as kickoff approaches (a list of (hours_to_kickoff, max_age_minutes)
steps: the first step whose window contains the current time-to-kickoff wins). Age is measured from the source's
own `retrieved_utc` stamp in the packet. A source with no stamp is MISSING, never assumed fresh.

Statuses:
  FRESH     retrieved within the allowed age
  STALE     retrieved, but older than the allowed age            -> 100k entry point refuses
  MISSING   no record / not OK / no timestamp                    -> 100k entry point refuses
  NOT_YET   cannot exist yet (official inactives before T-90)   -> 100k entry point refuses
  NOT_REQUIRED  e.g. weather for an indoor game
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from . import hooks

ET = ZoneInfo("America/New_York")
INACTIVES_POST_MINUTES_BEFORE_KICKOFF = 90

# name: (where in the packet, default max age minutes, [(within_hours_of_kickoff, max_age_minutes), ...], why)
POLICY = {
    "schedule":        ("sources.games",        24 * 60, [],                       "Kickoff time, site, QB listing."),
    "play_by_play":    ("sources.pbp",          24 * 60, [],                       "Last week's games; must also have every completed game (data_freshness OK)."),
    "rosters":         ("sources.rosters",      24 * 60, [],                       "Weekly rosters / positions."),
    "depth_charts":    ("sources.depth_charts", 24 * 60, [(48, 12 * 60)],          "Starters and roles."),
    "snap_counts":     ("sources.snap_counts",  24 * 60, [],                       "Weekly snap shares."),
    "ftn_charting":    ("sources.ftn",          24 * 60, [],                       "Blitz / play-action rates."),
    "pfr_defense":     ("sources.pfr_def",      24 * 60, [],                       "Per-defender coverage numbers."),
    "official_injuries": ("sources.injuries",   12 * 60, [(48, 6 * 60)],           "Official practice / game-status report."),
    "news_injuries":   ("sources.espn_injuries", 6 * 60, [(6, 2 * 60), (2, 45)],   "ESPN live injury list (the only news feed wired today)."),
    "weather":         ("weather",               6 * 60, [(12, 3 * 60), (3, 90)],  "NWS hourly forecast; outdoor games only."),
    "odds":            ("books",                 6 * 60, [(6, 60), (2, 20)],       "Book prices in the packet (Odds API, existing builder)."),
}
# Inputs with no packet field yet. They come from hooks and are checked separately (see hooks.py).
HOOKED = {
    "official_inactives": "Final inactives, posted about 90 minutes before kickoff. Must be pulled after they post.",
    "four_book_prices":   "Newest pregame/price_freezes/*_AWAY@HOME/freeze_*.json (Blitz). Max age follows the 'odds' row.",
}


def _get(pk: dict, dotted: str):
    cur = pk
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def parse_utc(s) -> datetime | None:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def kickoff_utc(pk: dict) -> datetime | None:
    k = parse_utc(_get(pk, "weather.kickoff_utc"))
    if k:
        return k
    g = pk.get("game") or {}
    try:
        hh, mm = str(g["kickoff_et"]).split(":")[:2]
        d = datetime.fromisoformat(str(g["date"])).replace(hour=int(hh), minute=int(mm), tzinfo=ET)
        return d.astimezone(timezone.utc)
    except (KeyError, ValueError):
        return None


def max_age_minutes(name: str, hours_to_kickoff: float | None) -> int:
    _, default, steps, _ = POLICY[name]
    allowed = default
    if hours_to_kickoff is not None:
        for within_h, m in sorted(steps, key=lambda s: -s[0]):
            if hours_to_kickoff <= within_h:
                allowed = m
    return allowed


def _row(name, status, reason, retrieved=None, age=None, allowed=None):
    return {"source": name, "status": status, "reason": reason, "retrieved_utc": retrieved,
            "age_minutes": None if age is None else round(age, 1), "max_age_minutes": allowed}


def check(pk: dict, now: datetime | None = None, hook_impls=None) -> list[dict]:
    """Freshness row for every source in POLICY plus the hooked inputs. Never raises on bad packets."""
    now = now or datetime.now(timezone.utc)
    ko = kickoff_utc(pk)
    htk = None if ko is None else (ko - now).total_seconds() / 3600
    rows = []
    for name, (path, *_rest) in POLICY.items():
        rec = _get(pk, path)
        if name == "weather" and isinstance(rec, dict) and rec.get("status") == "INDOOR":
            rows.append(_row(name, "NOT_REQUIRED", "Indoor game."))
            continue
        if not isinstance(rec, dict):
            rows.append(_row(name, "MISSING", f"No '{path}' record in the packet."))
            continue
        st = str(rec.get("status", ""))
        if not st.startswith("OK"):
            rows.append(_row(name, "MISSING", f"'{path}' status is {st or 'blank'}, not OK."))
            continue
        got = parse_utc(rec.get("retrieved_utc"))
        if got is None:
            rows.append(_row(name, "MISSING", f"'{path}' has no retrieved_utc timestamp; age unknown is treated as missing."))
            continue
        age = (now - got).total_seconds() / 60
        allowed = max_age_minutes(name, htk)
        if age > allowed:
            rows.append(_row(name, "STALE", f"{age:.0f} min old; limit is {allowed} min at {_fmt_htk(htk)}.", rec.get("retrieved_utc"), age, allowed))
        else:
            rows.append(_row(name, "FRESH", f"{age:.0f} min old; limit {allowed} min.", rec.get("retrieved_utc"), age, allowed))
    pbp = next((r for r in rows if r["source"] == "play_by_play" and r["status"] == "FRESH"), None)
    if pbp:
        lag = [t for t, v in (pk.get("data_freshness") or {}).items() if v.get("status") != "OK"]
        if lag or not pk.get("data_freshness"):
            pbp.update(status="STALE", reason="Play-by-play file is recent but is missing completed games for: " + (", ".join(lag) or "unknown teams") + ".")
    rows.append(inactives_row(pk, now, ko, hook_impls))
    rows.append(four_book_row(pk, now, htk, hook_impls))
    return rows


def _fmt_htk(htk):
    return "unknown time to kickoff" if htk is None else f"{htk:.1f} h to kickoff"


def inactives_row(pk, now, ko, hook_impls=None):
    if ko is None:
        return _row("official_inactives", "MISSING", "Kickoff time unknown, so the inactive window cannot be placed.")
    posts = ko - timedelta(minutes=INACTIVES_POST_MINUTES_BEFORE_KICKOFF)
    if now < posts:
        return _row("official_inactives", "NOT_YET", f"Inactives post about {posts.astimezone(ET):%a %I:%M %p} ET (T-90); not available yet.")
    res = hooks.official_inactives(pk, impl=(hook_impls or {}).get("official_inactives"))
    if res.get("status") != "OK":
        return _row("official_inactives", "MISSING", res.get("reason", "No inactives source."))
    got = parse_utc(res.get("retrieved_utc"))
    bad = inactives_pull_time_problem(got, posts, ko, now)
    if bad:
        return _row("official_inactives", "STALE" if got is not None and got < posts else "MISSING", bad, res.get("retrieved_utc"))
    return _row("official_inactives", "FRESH", "Pulled after the T-90 posting time.", res.get("retrieved_utc"))


CLOCK_SKEW = timedelta(minutes=2)


def inactives_pull_time_problem(got, posts, ko, now) -> str | None:
    """Shared by freshness and the Phase 15 ledger: a usable official-inactives pull is posts <= pulled < kickoff and
    not in the future (pulled <= now + 2 min clock skew). Returns the reason it is not usable, or None."""
    if got is None:
        return "Official inactives pull has no retrieved_utc; pull time unknown is treated as missing."
    if got < posts:
        return "Inactives were pulled before they post (T-90); pull again."
    if got >= ko:
        return "Inactives pull is stamped at/after kickoff; not a pregame freeze."
    if got > now + CLOCK_SKEW:
        return "Inactives pull is stamped in the future; not accepted."
    return None


def four_book_row(pk, now, htk, hook_impls=None):
    hi = hook_impls or {}
    res = hooks.four_book_prices(pk, impl=hi.get("four_book_prices"), base=hi.get("price_freeze_dir"))
    if res.get("status") != "OK":
        return _row("four_book_prices", "MISSING", res.get("reason", "No four-book feed."))
    missing = [b for b in hooks.REQUIRED_BOOKS if b not in (res.get("books") or {})]
    # A book that offers no line is listed absent by the feed; the gate needs all four.
    if missing:
        return _row("four_book_prices", "MISSING", "Feed is missing books: " + ", ".join(missing) + ".")
    got = parse_utc(res.get("retrieved_utc"))
    if got is None:
        return _row("four_book_prices", "MISSING", "Feed has no retrieved_utc timestamp.")
    age = (now - got).total_seconds() / 60
    allowed = max_age_minutes("odds", htk)
    if age > allowed:
        return _row("four_book_prices", "STALE", f"{age:.0f} min old; limit is {allowed} min.", res.get("retrieved_utc"), age, allowed)
    return _row("four_book_prices", "FRESH", f"{age:.0f} min old; limit {allowed} min.", res.get("retrieved_utc"), age, allowed)


def blocking(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["status"] in ("STALE", "MISSING", "NOT_YET")]
