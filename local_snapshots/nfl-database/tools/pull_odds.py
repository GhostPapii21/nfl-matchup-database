#!/usr/bin/env python3
"""Canonical NFL odds puller (2026-11-03, replaces runs/*/pull_odds.py copies, which are now deprecated).
The Odds API v4, documented public API; key from env ODDS_API_KEY, never printed.
Pulls per pregame event in the slate window: player props + alts (as before), game h2h/spreads/totals, alt lines,
team totals, and 1H/2H/Q1-Q4 h2h/spreads/totals (the API only bills markets a book returns).
Books: fanduel (price of record), draftkings, pinnacle (sharp / no-vig), prizepicks, underdog.
Outputs in --out (default: cwd), format in docs/pull_odds_format.md:
  odds_<tag>.csv (props; first 9 columns unchanged), odds_<tag>_game.csv, odds_<tag>_stale.csv,
  odds_<tag>_inplay_dropped.csv, odds_<tag>_meta.json, snapshots/odds_snapshots.csv (append, open->close), quota_log.csv.
Guards: pregame only, max quote age (default 30 min), call planner prints cost first and stops at the 10% quota floor.
Usage: python3 tools/pull_odds.py <tag> --start 2026-11-06T00:00:00Z --end 2026-11-06T06:00:00Z [--out DIR]
       [--week 9] [--season 2026] [--label open|T-120|T-60|T-30|close|manual] [--max-age 30] [--dry-run] [--props-only]"""
import argparse, csv, datetime as dt, json, os, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import odds_quota as Q
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")

SPORT = "americanfootball_nfl"; BASE = "https://api.the-odds-api.com/v4"
_P = ["player_pass_yds", "player_pass_completions", "player_rush_yds", "player_receptions", "player_reception_yds", "player_rush_reception_yds"]
PROP_MARKETS = _P + [m + "_alternate" for m in _P if m != "player_pass_completions"]
GAME_MARKETS = ["h2h", "spreads", "totals", "alternate_spreads", "alternate_totals", "team_totals"] + \
    [f"{b}_{p}" for p in ("h1", "h2", "q1", "q2", "q3", "q4") for b in ("h2h", "spreads", "totals")]
BOOKS = ["fanduel", "draftkings", "pinnacle", "prizepicks", "underdog"]
COLS = ["game", "book", "market", "player", "side", "point", "price", "last_update_utc", "inplay",
        "event_id", "commence_utc", "pulled_utc", "quote_age_min", "snapshot"]
SNAP_COLS = COLS
MAX_AGE_MIN = 30; PRE = [120, 60, 30]; TOL = 15; CLOSE_WITHIN = 15

def _t(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
def _z(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def checkpoint(now, commence, done=()):
    m = (commence - now).total_seconds() / 60
    if m <= 0: return None
    if not done: return "open"
    if m <= CLOSE_WITHIN: return None if "close" in done else "close"
    for p in PRE:
        if abs(m - p) <= TOL and f"T-{p}" not in done: return f"T-{p}"
    return None

def rows_from_event(js, now, label, max_age_min=MAX_AGE_MIN):
    """-> (prop_rows, game_rows, stale_rows). Quotes at/after kickoff are dropped (never written as pregame)."""
    c = _t(js["commence_time"]); game = f"{js['away_team']} @ {js['home_team']}"
    props, gl, stale = [], [], []
    if now >= c: return props, gl, stale
    for b in js.get("bookmakers", []):
        for m in b.get("markets", []):
            upd = m.get("last_update") or b.get("last_update")
            age = round((now - _t(upd)).total_seconds() / 60, 1) if upd else None
            for o in m.get("outcomes", []):
                r = dict(game=game, book=b["key"], market=m["key"], player=o.get("description"), side=o.get("name"),
                         point=o.get("point"), price=o.get("price"), last_update_utc=upd, inplay=False, event_id=js["id"],
                         commence_utc=js["commence_time"], pulled_utc=_z(now), quote_age_min=age, snapshot=label)
                if upd and _t(upd) >= c: continue
                if age is None or age > max_age_min: stale.append(r); continue
                (props if m["key"].startswith("player_") else gl).append(r)
    return props, gl, stale

def plan(events, markets, books):
    p = Q.plan_cost(len(events), markets, bookmakers=",".join(books)); return p

def _fetch(path, **q):
    key = os.environ["ODDS_API_KEY"]
    u = f"{BASE}{path}?" + urllib.parse.urlencode(dict(q, apiKey=key))
    try:
        r = urllib.request.urlopen(u, timeout=30)
        return json.load(r), {k.lower(): v for k, v in r.headers.items()}
    except Exception as e:
        raise RuntimeError(f"{type(e).__name__}: {str(e).replace(key, '***')}") from None

def _write(path, rows, cols=COLS, append=False):
    new = not (append and os.path.exists(path))
    with open(path, "a" if append else "w", newline="") as f:
        w = csv.DictWriter(f, cols); new and w.writeheader(); w.writerows(rows)

def run(tag, start, end, out=".", fetch=_fetch, now=None, label=None, max_age_min=MAX_AGE_MIN, dry_run=False,
        props_only=False, books=None, week=None, season=None):
    now = now or dt.datetime.now(dt.timezone.utc); books = books or BOOKS
    os.makedirs(os.path.join(out, "snapshots"), exist_ok=True)
    qlog = os.path.join(out, "quota_log.csv"); key = os.environ.get("ODDS_API_KEY") or "\0"
    events, h = fetch(f"/sports/{SPORT}/events")   # events endpoint: 0 credits
    used, rem = Q.quota_from_headers(h)
    if h: Q.log_headers(qlog, "nfl_pull_odds", "/events", h, "-", 0)
    stf = os.path.join(out, "snapshots", "state.json"); state = json.load(open(stf)) if os.path.exists(stf) else {}
    todo = []
    for e in events:
        if not (start <= e["commence_time"] < end): continue
        lab = label or checkpoint(now, _t(e["commence_time"]), state.get(e["id"], []))
        if lab and _t(e["commence_time"]) > now: todo.append((e, lab))
    markets = PROP_MARKETS + ([] if props_only else GAME_MARKETS)
    p = plan([e for e, _ in todo], markets, books)
    ok, why = Q.check(p["estimate"], used, rem)
    print(f"plan: {p['events']} events x {p['markets']} markets x {p['region_units']} region units = {p['estimate']} credits max; {why}")
    meta = dict(pulled_et=now.astimezone(ET).strftime("%Y-%m-%dT%H:%M"), pulled_utc=_z(now),
                season=season, data_week=week, plan=p, events=[], remaining=None, used=None, max_quote_age_min=max_age_min)
    if dry_run: return dict(status="dry_run", plan=p, why=why)
    if not ok:
        json.dump(dict(meta, status="stopped_quota_floor", why=why), open(os.path.join(out, f"odds_{tag}_meta.json"), "w"), indent=1)
        return dict(status="stopped_quota_floor", plan=p, why=why)
    P_, G_, S_ = [], [], []
    for e, lab in todo:
        est = Q.plan_cost(1, markets, bookmakers=",".join(books))["estimate"]
        ok, why = Q.check(est, used, rem)
        if not ok: meta["events"].append(dict(id=e["id"], skipped=why)); continue
        try:
            js, h = fetch(f"/sports/{SPORT}/events/{e['id']}/odds", markets=",".join(markets), bookmakers=",".join(books), oddsFormat="american")
        except Exception as ex:
            meta["events"].append(dict(id=e["id"], err=str(ex).replace(key, "***"))); continue
        used, rem = Q.log_headers(qlog, "nfl_pull_odds", f"/events/{e['id']}/odds", h, lab, est)
        meta["remaining"], meta["used"] = h.get("x-requests-remaining"), h.get("x-requests-used")
        pr, gr, st = rows_from_event(js, now, lab, max_age_min); P_ += pr; G_ += gr; S_ += st
        meta["events"].append(dict(id=e["id"], game=f"{e['away_team']} @ {e['home_team']}", snapshot=lab,
                                   books=[b["key"] for b in js.get("bookmakers", [])], props=len(pr), game_rows=len(gr), stale=len(st)))
        state.setdefault(e["id"], []).append(lab)
    _write(os.path.join(out, f"odds_{tag}.csv"), P_); _write(os.path.join(out, f"odds_{tag}_game.csv"), G_)
    _write(os.path.join(out, f"odds_{tag}_stale.csv"), S_)
    _write(os.path.join(out, "snapshots", "odds_snapshots.csv"), P_ + G_, append=True)
    json.dump(state, open(stf, "w"), indent=1)
    json.dump(meta, open(os.path.join(out, f"odds_{tag}_meta.json"), "w"), indent=1)
    return dict(status="ok", props=len(P_), game=len(G_), stale=len(S_), plan=p)

def main():
    a = argparse.ArgumentParser(); a.add_argument("tag"); a.add_argument("--start", required=True); a.add_argument("--end", required=True)
    a.add_argument("--out", default="."); a.add_argument("--label"); a.add_argument("--max-age", type=float, default=MAX_AGE_MIN)
    a.add_argument("--dry-run", action="store_true"); a.add_argument("--props-only", action="store_true")
    a.add_argument("--week", type=int); a.add_argument("--season", type=int, default=2026); a = a.parse_args()
    r = run(a.tag, a.start, a.end, a.out, label=a.label, max_age_min=a.max_age, dry_run=a.dry_run, props_only=a.props_only, week=a.week, season=a.season)
    print(json.dumps({k: v for k, v in r.items() if k != "plan"}))
    sys.exit(0 if r["status"] in ("ok", "dry_run") else 2)

if __name__ == "__main__": main()
