"""Freshness policy for pregame inputs (NFL-56 item 2). Human-readable copy: docs/DATA_FRESHNESS.md.

Age is measured from the source's AS-OF time, never from our fetch time (NFL-56). Each source has a basis:
  publisher  the publisher's own update stamp for the exact copy in the packet: `source_updated_at` on the record,
             or one proven by pipeline/source_asof.py (nflverse asset digest / not-updated-since-pull, NWS
             updateTime). No proven stamp -> MISSING with reason UNKNOWN_NO_SOURCE_TIMESTAMP, never fresh, never zero.
  live_pull  live endpoints that serve the current state at request time and carry no feed-level stamp (book
             prices, ESPN live injury list). The pull time is the quote/as-of time. `retrieved_utc` is used here
             and is labelled as such in every row.
A publisher stamp later than our pull, or in the future, is rejected (MISSING).

Cadence (pipeline/cadence.py, Rico 2026-11-22, newest-release rule):
  latest_release  FRESH if this copy is still the latest published asset (digest match or asset not re-published
                  after our pull) AND it covers every completed game. Missing a completed game is GAP, not STALE.
                  A superseded copy (newer asset exists) is STALE. No flat max-age clock.
  live_window     book prices, ESPN injuries, and the schedule keep their pull-time / as-of age windows, which
                  tighten as kickoff approaches.
  nws_live_grid   FRESH if our updateTime is the current NWS grid (not superseded). No max-age clock.
  t90             official inactives: NOT_YET before T-90; must be pulled after they post.

Statuses:
  FRESH     current under the cadence rule for that source
  STALE     live window expired, or our copy has been superseded by a newer release  -> 100k refuses
  GAP       latest release, but missing coverage of a completed game                 -> 100k refuses
  MISSING   no record / not OK / no timestamp                                        -> 100k refuses
  NOT_YET   cannot exist yet (official inactives before T-90)                       -> 100k refuses
  NOT_REQUIRED  e.g. weather for an indoor game
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from . import cadence, coverage, hooks, matchup_sources, ngs_matchup, source_asof

ET = ZoneInfo("America/New_York")
INACTIVES_POST_MINUTES_BEFORE_KICKOFF = 90
CLOCK_SKEW = timedelta(minutes=2)
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "pregame" / ".cache"
NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download"

# name: (where in the packet, default max age minutes, [(within_hours_of_kickoff, max_age_minutes), ...], why)
# Max-age is used only for live_window sources. latest_release / nws_live_grid ignore it.
POLICY = {
    "schedule":        ("sources.games",        24 * 60, [],                       "Kickoff time, site, QB listing."),
    "play_by_play":    ("sources.pbp",          24 * 60, [],                       "Last week's games; must also have every completed game."),
    "rosters":         ("sources.rosters",      24 * 60, [],                       "Weekly rosters / positions."),
    "depth_charts":    ("sources.depth_charts", 24 * 60, [(48, 12 * 60)],          "Starters and roles."),
    "snap_counts":     ("sources.snap_counts",  24 * 60, [],                       "Weekly snap shares."),
    "ftn_charting":    ("sources.ftn",          24 * 60, [],                       "Blitz / play-action rates."),
    "pfr_defense":     ("sources.pfr_def",      24 * 60, [],                       "Per-defender coverage numbers."),
    "official_injuries": ("sources.injuries",   12 * 60, [(48, 6 * 60)],           "Official practice / game-status report."),
    "news_injuries":   ("sources.espn_injuries", 6 * 60, [(6, 2 * 60), (2, 45)],   "ESPN live injury list (the only news feed wired today)."),
    "weather":         ("weather",               6 * 60, [(12, 3 * 60), (3, 90)],  "NWS hourly forecast; outdoor games only."),
    "odds":            ("books",                 6 * 60, [(6, 60), (2, 20)],       "Book prices in the packet (direct lines or Odds API)."),
    "ngs_passing":     ("sources.ngs_passing",  24 * 60, [],                       "Public NGS weekly passing (CPOE, time to throw). No NFL Pro."),
    "ngs_receiving":   ("sources.ngs_receiving", 24 * 60, [],                      "Public NGS weekly receiving (separation, cushion, YAC OE). No NFL Pro."),
    "ngs_rushing":     ("sources.ngs_rushing",  24 * 60, [],                       "Public NGS weekly rushing (RYOE, 8+ in the box). No NFL Pro."),
}
# How each source is dated (see module docstring). Anything not listed is 'publisher'.
ASOF_BASIS = {"news_injuries": "live_pull", "odds": "live_pull", "schedule": "live_pull"}
ASOF_FIELDS = ("source_updated_at", "as_of_utc", "published_utc", "source_published_utc", "last_modified_utc")
# Inputs with no packet field yet, or a derived game-day check. See hooks.py / ngs_matchup.py.
HOOKED = {
    "official_inactives": "Final inactives, posted about 90 minutes before kickoff. Must be pulled after they post.",
    "four_book_prices":   "Newest pregame/price_freezes/*_AWAY@HOME/freeze_*.json (Blitz). Max age follows the 'odds' row.",
    "ngs_defender_matchup": "Public NGS route / throw-location / success-vs-defense inputs for both teams (main-defender step).",
}
CACHE_FILE = {
    "schedule": "games.parquet",
    "play_by_play": "play_by_play_{season}.parquet",
    "rosters": "roster_weekly_{season}.parquet",
    "depth_charts": "depth_charts_{season}.parquet",
    "snap_counts": "snap_counts_{season}.parquet",
    "ftn_charting": "ftn_charting_{season}.parquet",
    "pfr_defense": "advstats_week_def_{season}.parquet",
    "official_injuries": "injuries_{season}.parquet",
    "ngs_passing": "ngs_passing.parquet",
    "ngs_receiving": "ngs_receiving.parquet",
    "ngs_rushing": "ngs_rushing.parquet",
}
CACHE_URL = {
    "schedule": f"{NFLVERSE}/schedules/games.parquet",
    "play_by_play": f"{NFLVERSE}/pbp/play_by_play_{{season}}.parquet",
    "rosters": f"{NFLVERSE}/weekly_rosters/roster_weekly_{{season}}.parquet",
    "depth_charts": f"{NFLVERSE}/depth_charts/depth_charts_{{season}}.parquet",
    "snap_counts": f"{NFLVERSE}/snap_counts/snap_counts_{{season}}.parquet",
    "ftn_charting": f"{NFLVERSE}/ftn_charting/ftn_charting_{{season}}.parquet",
    "pfr_defense": f"{NFLVERSE}/pfr_advstats/advstats_week_def_{{season}}.parquet",
    "official_injuries": f"{NFLVERSE}/injuries/injuries_{{season}}.parquet",
    "ngs_passing": f"{NFLVERSE}/nextgen_stats/ngs_passing.parquet",
    "ngs_receiving": f"{NFLVERSE}/nextgen_stats/ngs_receiving.parquet",
    "ngs_rushing": f"{NFLVERSE}/nextgen_stats/ngs_rushing.parquet",
}


def _season(pk: dict) -> int:
    try:
        return int((pk.get("game") or {}).get("season") or 2026)
    except (TypeError, ValueError):
        return 2026


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


def _row(name, status, reason, retrieved=None, age=None, allowed=None, as_of=None, basis=None, evidence=None):
    return {"source": name, "status": status, "reason": reason, "retrieved_utc": retrieved, "as_of_utc": as_of,
            "as_of_basis": basis, "as_of_evidence": evidence,
            "age_minutes": None if age is None else round(age, 1), "max_age_minutes": allowed,
            "cadence": cadence.rule_for(name)}


def _asof_map(pk, hook_impls):
    """publisher stamps: hook_impls['source_asof'] (callable pk -> dict, or a dict) wins; else network resolution
    when enabled (CLI entry points); else {} (offline: only stamps already on the records count)."""
    impl = (hook_impls or {}).get("source_asof")
    if callable(impl):
        return impl(pk) or {}
    if isinstance(impl, dict):
        return impl
    if source_asof.enabled():
        return source_asof.resolve(pk, POLICY)
    return {}


def as_of(name, rec, asof_map, now):
    """-> (as_of datetime | None, basis, reason_if_unusable, evidence)"""
    got = parse_utc(rec.get("retrieved_utc"))
    if ASOF_BASIS.get(name) == "live_pull":
        if got is None:
            return None, "live_pull", f"no retrieved_utc; pull time unknown is treated as missing.", None
        if got > now + CLOCK_SKEW:
            return None, "live_pull", "pull is stamped in the future; not accepted.", None
        return got, "live_pull (live endpoint; pull time is the quote time)", None, None
    if got is None:
        return None, None, "no retrieved_utc; pull time unknown is treated as missing (every figure needs a pull time).", None
    raw = next((rec.get(f) for f in ASOF_FIELDS if rec.get(f)), None)
    basis, ev = ("record:" + next(f for f in ASOF_FIELDS if rec.get(f))) if raw else None, None
    if raw is None and name in asof_map:
        a = asof_map[name]
        raw, basis, ev = a.get("source_updated_at"), a.get("as_of_basis"), a.get("evidence")
        if raw is None:
            return None, basis, "UNKNOWN_NO_SOURCE_TIMESTAMP: " + str(a.get("reason")), ev
    if raw is None:
        return None, "UNKNOWN_NO_SOURCE_TIMESTAMP", ("UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; "
                                                     "our fetch time alone does not show the data is current."), None
    d = parse_utc(raw)
    if d is None:
        return None, basis, f"UNKNOWN_NO_SOURCE_TIMESTAMP: unparseable as-of stamp {raw!r}.", ev
    if d > now + CLOCK_SKEW:
        return None, basis, "as-of stamp is in the future; not accepted.", ev
    if got is not None and d > got + CLOCK_SKEW:
        return None, basis, "as-of stamp is after our pull, so it cannot describe our copy.", ev
    return d, basis, None, ev


def cache_path(name: str, pk: dict) -> Path:
    season = _season(pk)
    return CACHE / CACHE_FILE[name].format(season=season)


def cache_fallback(name: str, pk: dict, rec) -> dict | None:
    """If the packet has no OK record, use a local pregame/.cache copy when present (no pregame.py change)."""
    if isinstance(rec, dict) and str(rec.get("status", "")).startswith("OK"):
        if not rec.get("path") and name in CACHE_FILE:
            p = cache_path(name, pk)
            if p.is_file():
                rec = dict(rec, path=str(p))
        return rec
    if name not in CACHE_FILE:
        return rec if isinstance(rec, dict) else None
    p = cache_path(name, pk)
    if not p.is_file():
        return rec if isinstance(rec, dict) else None
    b = p.read_bytes()
    mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds")
    return {"status": "OK", "path": str(p), "url": CACHE_URL[name].format(season=_season(pk)),
            "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "retrieved_utc": mtime,
            "note": "packet had no OK record; used pregame/.cache copy"}


def _coverage_missing(name: str, rec: dict, pk: dict, hook_impls) -> list[str] | None:
    """None = coverage not asserted; list (possibly empty) = inspected; non-empty = GAP ids."""
    if cadence.coverage_for(name) != "completed_games":
        return None
    hi = hook_impls or {}
    if name == "play_by_play" and pk.get("data_freshness"):
        lag = [t for t, v in pk["data_freshness"].items() if isinstance(v, dict) and v.get("status") != "OK"]
        return lag  # may be empty (= covered)
    if name == "play_by_play" and not pk.get("data_freshness"):
        # Existing contract: no data_freshness block means we cannot confirm completed games are in the file.
        # If a file can still be inspected, prefer that; otherwise GAP with unknown teams.
        pass
    if callable(hi.get("completed_games")):
        completed = hi["completed_games"](pk)
    else:
        sched = coverage.source_path(_get(pk, "sources.games"), [cache_path("schedule", pk)])
        g = pk.get("game") or {}
        stype = g.get("season_type") or g.get("game_type") or "REG"
        completed = coverage.completed_games_from_schedule(
            sched, hook=None, season=_season(pk), season_type=stype)
    if callable(hi.get("source_coverage")):
        found = hi["source_coverage"](name, rec, pk)
    else:
        path = coverage.source_path(rec, [cache_path(name, pk)] if name in CACHE_FILE else [])
        found = coverage.ids_in_file(path) if path else None
    if name == "play_by_play" and not pk.get("data_freshness") and found is None:
        return ["unknown teams"]
    if completed is None or found is None:
        return None
    return coverage.missing_completed(completed, found)


def check(pk: dict, now: datetime | None = None, hook_impls=None) -> list[dict]:
    """Freshness row for every source in POLICY plus the hooked inputs. Never raises on bad packets."""
    now = now or datetime.now(timezone.utc)
    # Make cache fallbacks visible to source_asof.resolve (needs url + sha256 on the records).
    pk_eff = pk
    if any(name in CACHE_FILE for name in POLICY):
        src = dict(pk.get("sources") or {})
        weather = pk.get("weather")
        changed = False
        for name, (path, *_r) in POLICY.items():
            rec = cache_fallback(name, pk, _get(pk, path))
            if rec is not None and rec is not _get(pk, path):
                if path.startswith("sources."):
                    src[path.split(".", 1)[1]] = rec
                    changed = True
                elif path == "weather" and rec is not weather:
                    weather = rec
                    changed = True
        if changed:
            pk_eff = dict(pk, sources=src)
            if weather is not pk.get("weather"):
                pk_eff["weather"] = weather
    asof_map = _asof_map(pk_eff, hook_impls)
    ko = kickoff_utc(pk)
    htk = None if ko is None else (ko - now).total_seconds() / 3600
    rows = []
    for name, (path, *_rest) in POLICY.items():
        rec = cache_fallback(name, pk, _get(pk, path))
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
        d, basis, why, ev = as_of(name, rec, asof_map, now)
        rule = cadence.rule_for(name)
        if d is None:
            # A newer release / regenerated NWS grid after our pull means our copy is not current: STALE, not a missing stamp.
            # Lookup failures stay MISSING (UNKNOWN_NO_SOURCE_TIMESTAMP). Live-window sources keep their
            # pull-time clock instead of this latest-release superseded rule.
            s = str(why or "").lower()
            if rule in ("latest_release", "nws_live_grid") and (
                "superseded" in s or "re-published after our pull" in s or "regenerated after our pull" in s
            ):
                rows.append(_row(name, "STALE", f"'{path}': not the latest published asset: {why}",
                                 rec.get("retrieved_utc"), basis=basis, evidence=ev))
            else:
                rows.append(_row(name, "MISSING", f"'{path}': {why}", rec.get("retrieved_utc"), basis=basis, evidence=ev))
            continue
        age = (now - d).total_seconds() / 60
        allowed = max_age_minutes(name, htk)
        stamp = d.isoformat(timespec="seconds")
        if rule in ("latest_release", "nws_live_grid"):
            gap = _coverage_missing(name, rec, pk, hook_impls) if rule == "latest_release" else None
            if gap:
                rows.append(_row(name, "GAP",
                                 f"latest published asset (as-of {stamp}, {basis}) is missing completed-game coverage for: "
                                 + ", ".join(gap) + ".",
                                 rec.get("retrieved_utc"), age, None, stamp, basis, ev))
            else:
                why_ok = (f"latest published asset as-of {stamp} ({basis}); newest-release rule, no max-age clock."
                          if rule == "latest_release"
                          else f"NWS updateTime {stamp} ({basis}) matches the current grid (or is the stamp on this copy); no max-age clock.")
                rows.append(_row(name, "FRESH", why_ok, rec.get("retrieved_utc"), age, None, stamp, basis, ev))
            continue
        if age > allowed:
            rows.append(_row(name, "STALE", f"as-of {stamp} ({basis}) is {age:.0f} min old; limit is {allowed} min at {_fmt_htk(htk)}.",
                             rec.get("retrieved_utc"), age, allowed, stamp, basis, ev))
        else:
            rows.append(_row(name, "FRESH", f"as-of {stamp} ({basis}) is {age:.0f} min old; limit {allowed} min.",
                             rec.get("retrieved_utc"), age, allowed, stamp, basis, ev))
    rows.append(inactives_row(pk, now, ko, hook_impls))
    rows.append(four_book_row(pk, now, htk, hook_impls))
    rows.append(ngs_matchup_row(pk_eff, hook_impls, rows))
    return rows


def ngs_matchup_row(pk, hook_impls=None, prior_rows=None):
    """Game-day check: public NGS route / throw-location / success inputs for both teams (main-defender step)."""
    hi = hook_impls or {}
    if callable(hi.get("ngs_defender_matchup")):
        res = hi["ngs_defender_matchup"](pk)
        return _row("ngs_defender_matchup", res.get("status", "MISSING"), res.get("reason", "hook returned no reason."),
                    evidence=res)
    g = pk.get("game") or {}
    teams = [t for t in (g.get("away"), g.get("home")) if t]
    paths, records_ok = {}, {}
    for name, fn in ngs_matchup.NGS_FILES.items():
        rec = cache_fallback(name, pk, _get(pk, f"sources.{name}"))
        p = coverage.source_path(rec, [cache_path(name, pk)])
        if p:
            paths[name] = p
        records_ok[name] = isinstance(rec, dict) and str(rec.get("status", "")).startswith("OK")
    completed_missing = []
    for name in ("ngs_passing", "ngs_receiving", "ngs_rushing"):
        rec = cache_fallback(name, pk, _get(pk, f"sources.{name}"))
        if not isinstance(rec, dict):
            continue
        gap = _coverage_missing(name, rec, pk, hook_impls)
        if gap:
            completed_missing.extend(f"{name}:{x}" for x in gap)
    # unique, stable
    seen, miss = set(), []
    for x in completed_missing:
        if x not in seen:
            seen.add(x)
            miss.append(x)
    res = ngs_matchup.check(teams, g.get("week"), paths, completed_missing=miss, records_ok=records_ok)
    reason = res["reason"]
    if len(teams) == 2 and g.get("week") is not None:
        # Fill the wanted main-defender fields from sources that carry them (pipeline/matchup_sources.py).
        pbp_row = next((r for r in (prior_rows or []) if r.get("source") == "play_by_play"), {}) or {}
        pbp_rec = cache_fallback("play_by_play", pk, _get(pk, "sources.pbp"))
        pbp_path = coverage.source_path(pbp_rec, [cache_path("play_by_play", pk)]) if isinstance(pbp_rec, dict) else None
        part = CACHE / f"pbp_participation_{_season(pk)}.parquet"
        try:
            mf = matchup_sources.fields(teams, _season(pk), int(g["week"]), pbp_path=pbp_path,
                                        pbp_status=pbp_row.get("status", "unknown"), pbp_as_of=pbp_row.get("as_of_utc"),
                                        part_path=part if part.is_file() else None,
                                        pff_base=(hook_impls or {}).get("pff_matchups_dir"))
        except Exception as e:  # never invent: an adapter failure leaves every field MISSING
            mf = {k: {"field": k, "status": "MISSING", "value": "unknown", "reason": f"matchup adapter failed: {e!r}"}
                  for k in matchup_sources.FIELDS}
        res["matchup_fields"] = mf
        res["fields"]["missing"] = [m for m in res["fields"]["missing"]
                                    if not (m.get("source") == "public_ngs" and mf.get(m["field"], {}).get("status") not in (None, "MISSING"))]
        summary = "; ".join(f"{k}={v['status']}" for k, v in mf.items())
        reason = (f"Public NGS weekly files: {res['status']}. Main-defender fields: {summary}. "
                  "MISSING = no source carries it (unknown, never zero); PFF_PROJECTED = candidate only, not verified.")
    return _row("ngs_defender_matchup", res["status"], reason, evidence=res)


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
    return _row("official_inactives", "FRESH", f"Official inactives pulled after T-90 at {got.isoformat(timespec='seconds')}.",
                res.get("retrieved_utc"), (now - got).total_seconds() / 60 if got else None, None,
                got.isoformat(timespec="seconds") if got else None, "t90")


def inactives_pull_time_problem(got, posts, ko, now) -> str | None:
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
    return [r for r in rows if r["status"] in ("STALE", "GAP", "MISSING", "NOT_YET")]
