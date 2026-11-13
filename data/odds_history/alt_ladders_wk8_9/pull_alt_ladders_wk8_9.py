#!/usr/bin/env python3
"""Weeks 8-9 2026 NFL historical alt-ladder pull (FanDuel only).
Markets: player_rush_yds_alternate, player_reception_yds_alternate. Snapshot T-90 min.
Never logs or writes the API key. Stops if the next call would drop remaining below 950.
Usage: python pull_alt_ladders_wk8_9.py events|first|rest
"""
from __future__ import annotations
import json, os, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
LOG = HERE / "pull_log.jsonl"
FLOOR = 950
SPORT = "americanfootball_nfl"
MARKETS = "player_rush_yds_alternate,player_reception_yds_alternate"
BOOKS = "fanduel"
SKIP = {"2026_09_DAL_IND", "2026_09_JAX_BAL", "2026_09_BUF_MIN"}  # already pulled in PR #41


def now():
    return datetime.now(timezone.utc)

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def call(path, params, key):
    q = dict(params); q["apiKey"] = key
    url = f"https://api.the-odds-api.com{path}?{urllib.parse.urlencode(q)}"
    safe = f"https://api.the-odds-api.com{path}?{urllib.parse.urlencode(params)}&apiKey=<REDACTED>"
    t0 = now()
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=90) as r:
            body, h, st = r.read(), {k.lower(): v for k, v in r.headers.items()}, r.status
    except urllib.error.HTTPError as e:
        body, h, st = (e.read() if e.fp else b""), {k.lower(): v for k, v in (e.headers or {}).items()}, e.code
    rec = {"path": path, "safe_url": safe, "status": st, "pulled_utc": iso(t0),
           "remaining": h.get("x-requests-remaining"), "used": h.get("x-requests-used"),
           "cost": h.get("x-requests-last")}
    try:
        parsed = json.loads(body.decode()) if body else None
    except Exception:
        parsed = {"_unparsed": body.decode(errors="replace")[:2000]}
    return rec, parsed

def log(entry):
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps(entry))

def remaining_now(key):
    rec, _ = call("/v4/sports", {}, key)
    log({"call": "sports_precheck_free", **rec})
    return int(rec["remaining"])

def main():
    key = os.environ.get("ODDS_API_KEY", "").strip()
    assert key, "NO_KEY"
    mode = sys.argv[1]
    RAW.mkdir(parents=True, exist_ok=True)
    if mode == "events":
        # Week 8 Odds API event ids (Week 9 ids already verified in PR #41 script)
        rem = remaining_now(key)
        if rem - 1 < FLOOR:
            print("STOP floor"); return 1
        date = sys.argv[2]
        rec, parsed = call(f"/v4/historical/sports/{SPORT}/events", {"date": date}, key)
        log({"call": "historical_events", "requested_date": date, **rec})
        (RAW / f"events_{date.replace(':','')}.json").write_text(json.dumps({"meta": rec, "response": parsed}, indent=1))
        return 0
    events = json.loads((HERE / "events_wk8_9.json").read_text())
    queue = [e for e in events if e["game_id"] not in SKIP]
    done = {p.name.split("__")[0] for p in RAW.glob("*__*.json")}
    queue = [e for e in queue if e["game_id"] not in done]
    if mode == "first":
        queue = queue[:1]
    est = int(sys.argv[2]) if len(sys.argv) > 2 else 40  # conservative until measured
    rem = remaining_now(key)
    for ev in queue:
        if rem - est < FLOOR:
            log({"call": "STOP", "game_id": ev["game_id"], "reason": f"remaining {rem} - est {est} < {FLOOR}"})
            return 3
        ko = datetime.fromisoformat(ev["commence_time"].replace("Z", "+00:00"))
        date = iso(ko - timedelta(minutes=90))
        params = {"date": date, "bookmakers": BOOKS, "markets": MARKETS, "oddsFormat": "american"}
        rec, parsed = call(f"/v4/historical/sports/{SPORT}/events/{ev['event_id']}/odds", params, key)
        entry = {"call": "historical_event_odds", "game_id": ev["game_id"], "event_id": ev["event_id"],
                 "requested_snapshot_utc": date, **rec}
        if isinstance(parsed, dict):
            entry["snapshot_timestamp"] = parsed.get("timestamp")
            d = parsed.get("data") or {}
            entry["n_outcomes"] = {m["key"]: len(m.get("outcomes", [])) for b in d.get("bookmakers", []) for m in b.get("markets", [])}
        log(entry)
        (RAW / f"{ev['game_id']}__{date.replace(':','')}.json").write_text(
            json.dumps({"meta": {**ev, **rec, "requested_snapshot_utc": date, "params": params}, "response": parsed}, indent=1))
        if rec["remaining"] is not None:
            rem = int(rec["remaining"])
        if rec["status"] != 200:
            print("non-200; stopping"); return 4
        if rec["cost"] is not None:
            est = max(int(rec["cost"]), 1)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
