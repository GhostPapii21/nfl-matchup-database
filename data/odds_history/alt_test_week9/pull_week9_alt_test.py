#!/usr/bin/env python3
"""Week 9 historical alt-line test pull. Never logs or writes the API key."""
from __future__ import annotations

import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

OUT = Path(os.environ.get("ALT_TEST_OUT", "/tmp/wt-odds-hist/data/odds_history/alt_test_week9"))
JOB_LIMIT = 150
REMAINING_FLOOR = 950  # 800 hard floor + 150 Sunday live reserve
SPORT = "americanfootball_nfl"
MARKETS = [
    "player_rush_yds",
    "player_rush_yds_alternate",
    "player_reception_yds",
    "player_reception_yds_alternate",
]
# bookmakers takes precedence over regions; 2 books count as 1 region-equivalent
BOOKMAKERS = "fanduel,pinnacle"
ODDS_FORMAT = "american"
EST_COST_PER_CALL = 10 * len(MARKETS) * 1  # official: 10 * markets * regions

# Odds API event IDs from week9_verified_pregame.csv (32-char hex, not ESPN ids)
# kickoff_et is America/New_York local ISO; snapshot is 90 minutes before kickoff UTC
EVENTS = [
    # Sunday 1pm ET representative first
    {"game_id": "2026_09_DAL_IND", "event_id": "415fc42e72888c63e82f7bce24c65391",
     "away": "DAL", "home": "IND", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_JAX_BAL", "event_id": "c75744790b7acf6260c78ba5e739c0e5",
     "away": "JAX", "home": "BAL", "kickoff_et": "2026-11-05T20:15:00-05:00"},
    {"game_id": "2026_09_CIN_ATL", "event_id": "dc56d980f527ffeef89940133b211b13",
     "away": "CIN", "home": "ATL", "kickoff_et": "2026-11-08T09:30:00-05:00"},
    {"game_id": "2026_09_DEN_CAR", "event_id": "014282b888c741b7d70c857c09f40aa7",
     "away": "DEN", "home": "CAR", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_NYJ_KC", "event_id": "e354e6a04b1cb9c96e549b863debb92e",
     "away": "NYJ", "home": "KC", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_DET_MIA", "event_id": "44d8c37868b700e90f816db7c5df5cdd",
     "away": "DET", "home": "MIA", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_CLE_NO", "event_id": "e571bab6736f9338130a78a4f75c3231",
     "away": "CLE", "home": "NO", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_NYG_PHI", "event_id": "fe93e6ab1e553c0169936a0a983c324f",
     "away": "NYG", "home": "PHI", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_LA_WAS", "event_id": "89de07377e0aa8ffaa2ae6a7dc0855cc",
     "away": "LA", "home": "WAS", "kickoff_et": "2026-11-08T13:00:00-05:00"},
    {"game_id": "2026_09_HOU_LAC", "event_id": "39aeac43cea7b12558b91cdab1255a10",
     "away": "HOU", "home": "LAC", "kickoff_et": "2026-11-08T16:05:00-05:00"},
    {"game_id": "2026_09_LV_SF", "event_id": "ac9d38a18d5c92814233a31aa9a48d78",
     "away": "LV", "home": "SF", "kickoff_et": "2026-11-08T16:05:00-05:00"},
    {"game_id": "2026_09_GB_NE", "event_id": "2922c573ec3df8466c4a34975e446898",
     "away": "GB", "home": "NE", "kickoff_et": "2026-11-08T16:25:00-05:00"},
    {"game_id": "2026_09_ARI_SEA", "event_id": "240e23b02b1e3fef655d04a286b5a623",
     "away": "ARI", "home": "SEA", "kickoff_et": "2026-11-08T16:25:00-05:00"},
    {"game_id": "2026_09_TB_CHI", "event_id": "9760d8f19f84bfee300a74ceb656c95d",
     "away": "TB", "home": "CHI", "kickoff_et": "2026-11-08T20:20:00-05:00"},
    {"game_id": "2026_09_BUF_MIN", "event_id": "17ad7eff2f7875e20a8109abe40470e3",
     "away": "BUF", "home": "MIN", "kickoff_et": "2026-11-09T20:15:00-05:00"},
]

CREDIT_LOG = []
JOB_USED = 0
LAST_REMAINING = None
MEASURED_COST = None  # set from first event-odds call's x-requests-last


def now_utc():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def redact(s: str, key: str) -> str:
    return s.replace(key, "<REDACTED>") if key else s


def credit_headers(headers) -> dict:
    h = {k.lower(): v for k, v in headers.items()}
    return {
        "x-requests-remaining": h.get("x-requests-remaining"),
        "x-requests-used": h.get("x-requests-used"),
        "x-requests-last": h.get("x-requests-last"),
    }


def request(path: str, params: dict, key: str, timeout=60):
    global LAST_REMAINING
    q = dict(params)
    q["apiKey"] = key
    url = f"https://api.the-odds-api.com{path}?{urllib.parse.urlencode(q)}"
    # safe URL for logs/files
    safe_params = dict(params)
    safe_url = f"https://api.the-odds-api.com{path}?{urllib.parse.urlencode(safe_params)}&apiKey=<REDACTED>"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    pull_started = now_utc()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            creds = credit_headers(resp.headers)
            status = resp.status
    except urllib.error.HTTPError as e:
        body = e.read() if e.fp else b""
        creds = credit_headers(e.headers or {})
        status = e.code
    pull_ended = now_utc()
    remaining = creds.get("x-requests-remaining")
    last = creds.get("x-requests-last")
    if remaining is not None:
        LAST_REMAINING = int(remaining)
    cost = int(last) if last not in (None, "") else None
    return {
        "status": status,
        "credits": creds,
        "cost": cost,
        "body": body,
        "safe_url": safe_url,
        "path": path,
        "params": params,
        "pull_started_utc": iso(pull_started),
        "pull_ended_utc": iso(pull_ended),
    }


def can_afford(est: int) -> tuple[bool, str]:
    if JOB_USED + est > JOB_LIMIT:
        return False, f"job limit: used {JOB_USED} + est {est} would exceed {JOB_LIMIT}"
    if LAST_REMAINING is None:
        return False, "remaining unknown; refuse"
    if LAST_REMAINING - est < REMAINING_FLOOR:
        return False, f"floor: remaining {LAST_REMAINING} - est {est} would drop below {REMAINING_FLOOR}"
    return True, "ok"


def snapshot_utc(kickoff_et: str) -> str:
    ko = datetime.fromisoformat(kickoff_et)
    snap = ko.astimezone(timezone.utc) - timedelta(hours=1, minutes=30)
    return iso(snap)


def summarize_event_body(obj: dict) -> dict:
    data = obj.get("data") if isinstance(obj, dict) and "data" in obj else obj
    books = []
    if not isinstance(data, dict):
        return {"parse": "unexpected", "type": type(data).__name__}
    for b in data.get("bookmakers") or []:
        markets = []
        for m in b.get("markets") or []:
            outs = m.get("outcomes") or []
            sides = {}
            rungs = {}
            for o in outs:
                name = (o.get("name") or "").lower()  # over/under
                point = o.get("point")
                desc = o.get("description")  # player
                sides.setdefault(name, 0)
                sides[name] += 1
                rungs.setdefault(name, set()).add(point)
            markets.append({
                "key": m.get("key"),
                "n_outcomes": len(outs),
                "n_over": sides.get("over", 0),
                "n_under": sides.get("under", 0),
                "over_rungs": sorted(x for x in rungs.get("over", set()) if x is not None),
                "under_rungs": sorted(x for x in rungs.get("under", set()) if x is not None),
                "n_players": len({(o.get("description") or o.get("name")) for o in outs}),
            })
        books.append({"key": b.get("key"), "title": b.get("title"), "markets": markets})
    return {
        "event_id": data.get("id"),
        "sport_key": data.get("sport_key"),
        "commence_time": data.get("commence_time"),
        "home_team": data.get("home_team"),
        "away_team": data.get("away_team"),
        "snapshot_timestamp": obj.get("timestamp") if isinstance(obj, dict) else None,
        "previous_timestamp": obj.get("previous_timestamp") if isinstance(obj, dict) else None,
        "next_timestamp": obj.get("next_timestamp") if isinstance(obj, dict) else None,
        "bookmakers": books,
    }


def main():
    global JOB_USED, MEASURED_COST, LAST_REMAINING
    key = os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        print("NO_KEY", file=sys.stderr)
        return 2
    mode = sys.argv[1] if len(sys.argv) > 1 else "first"
    OUT.mkdir(parents=True, exist_ok=True)
    raw_dir = OUT / "raw"
    raw_dir.mkdir(exist_ok=True)

    # 0-cost remaining check
    ok, why = True, "precheck"
    # We already know remaining from prior /v4/sports; still re-check at 0 cost
    pre = request("/v4/sports", {}, key)
    cost0 = pre["cost"] if pre["cost"] is not None else 0
    JOB_USED += cost0
    CREDIT_LOG.append({"call": "sports_precheck", **pre["credits"], "job_used": JOB_USED,
                       "pulled_utc": pre["pull_started_utc"], "status": pre["status"]})
    print("precheck", json.dumps({k: pre[k] for k in ("status", "credits", "cost", "pull_started_utc")}))
    if pre["status"] != 200:
        print("precheck failed; abort")
        return 1

    if mode == "first":
        queue = EVENTS[:1]
    elif mode == "rest":
        queue = EVENTS[1:]
    else:
        queue = EVENTS

    results = []
    for ev in queue:
        est = MEASURED_COST if MEASURED_COST is not None else EST_COST_PER_CALL
        affordable, why = can_afford(est)
        if not affordable:
            print("STOP before", ev["game_id"], why)
            results.append({"game_id": ev["game_id"], "status": "skipped", "reason": why})
            break
        date = snapshot_utc(ev["kickoff_et"])
        params = {
            "date": date,
            "bookmakers": BOOKMAKERS,
            "markets": ",".join(MARKETS),
            "oddsFormat": ODDS_FORMAT,
        }
        path = f"/v4/historical/sports/{SPORT}/events/{ev['event_id']}/odds"
        print(f"PULL {ev['game_id']} date={date} est={est} remaining={LAST_REMAINING} job_used={JOB_USED}")
        resp = request(path, params, key)
        cost = resp["cost"] if resp["cost"] is not None else 0
        JOB_USED += cost
        if MEASURED_COST is None and resp["status"] == 200 and resp["cost"] is not None:
            MEASURED_COST = resp["cost"]
        CREDIT_LOG.append({
            "call": "historical_event_odds",
            "game_id": ev["game_id"],
            "event_id": ev["event_id"],
            "requested_snapshot_utc": date,
            **resp["credits"],
            "job_used": JOB_USED,
            "pulled_utc": resp["pull_started_utc"],
            "status": resp["status"],
        })
        # persist raw (no key)
        stamp = resp["pull_started_utc"].replace(":", "").replace("-", "")
        raw_path = raw_dir / f"{ev['game_id']}_{stamp}.json"
        try:
            parsed = json.loads(resp["body"].decode("utf-8")) if resp["body"] else None
        except json.JSONDecodeError:
            parsed = {"_unparsed_text": resp["body"].decode("utf-8", errors="replace")[:2000]}
        # strip any accidental key
        blob = {
            "meta": {
                "game_id": ev["game_id"],
                "event_id": ev["event_id"],
                "away": ev["away"],
                "home": ev["home"],
                "kickoff_et": ev["kickoff_et"],
                "requested_snapshot_utc": date,
                "snapshot_offset": "90 minutes before kickoff",
                "request_path": path,
                "request_params": params,  # no key
                "safe_url": resp["safe_url"],
                "http_status": resp["status"],
                "credits": resp["credits"],
                "pull_started_utc": resp["pull_started_utc"],
                "pull_ended_utc": resp["pull_ended_utc"],
            },
            "response": parsed,
        }
        raw_path.write_text(json.dumps(blob, indent=2))
        summary = summarize_event_body(parsed) if isinstance(parsed, dict) else {"parse": "failed"}
        rec = {
            "game_id": ev["game_id"],
            "event_id": ev["event_id"],
            "http_status": resp["status"],
            "cost": cost,
            "credits": resp["credits"],
            "raw_file": str(raw_path.relative_to(OUT)),
            "summary": summary,
        }
        results.append(rec)
        print("RESULT", ev["game_id"], "status", resp["status"], "cost", cost,
              "remaining", resp["credits"].get("x-requests-remaining"), "job_used", JOB_USED)
        if resp["status"] != 200:
            # still count credits; do not blindly continue if cost unknown and remaining dropped oddly
            print("non-200, will continue only if credits known and limits allow")

    ledger = {
        "job": "week9_alt_price_test",
        "pulled_at_et_zone": "America/New_York",
        "job_limit_credits": JOB_LIMIT,
        "remaining_floor": REMAINING_FLOOR,
        "markets": MARKETS,
        "bookmakers": BOOKMAKERS,
        "estimated_cost_formula": "10 * n_markets * n_region_equivalents (bookmakers=fanduel,pinnacle => 1 region-equivalent)",
        "estimated_cost_before_measure": EST_COST_PER_CALL,
        "measured_cost_per_event_call": MEASURED_COST,
        "job_credits_used": JOB_USED,
        "credits_remaining_last": LAST_REMAINING,
        "credit_log": CREDIT_LOG,
        "results": [{"game_id": r.get("game_id"), "http_status": r.get("http_status"), "cost": r.get("cost"),
                     "credits": r.get("credits"), "raw_file": r.get("raw_file"), "reason": r.get("reason"),
                     "status": r.get("status"), "summary": r.get("summary")} for r in results],
    }
    out_name = "ledger_first.json" if mode == "first" else "ledger.json"
    (OUT / out_name).write_text(json.dumps(ledger, indent=2))
    print("WROTE", OUT / out_name, "job_used", JOB_USED, "remaining", LAST_REMAINING, "measured", MEASURED_COST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
