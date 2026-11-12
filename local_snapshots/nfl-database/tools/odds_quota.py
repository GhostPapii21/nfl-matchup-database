"""Odds API call planner + quota guard (Rico 2026-11-03: size pulls to the slate).
Cost model (The Odds API v4 docs): cost = events x markets returned x region units, where a region unit is one
region, or each group of 10 bookmakers when `bookmakers=` is used. Estimates are upper bounds (only markets a
book actually returns are billed). Stop before a pull would leave remaining below FLOOR_PCT of the plan (used+remaining)."""
import csv, math, os, datetime as dt
FLOOR_PCT = 0.10
LOG_COLS = ["ts_et", "ts_utc", "job", "endpoint", "checkpoint", "estimate", "cost", "used", "remaining"]

def region_units(regions="", bookmakers=""):
    books = [b for b in (bookmakers or "").split(",") if b.strip()]
    if books: return math.ceil(len(books) / 10)
    return max(1, len([r for r in (regions or "").split(",") if r.strip()]))

def plan_cost(events, markets, regions="", bookmakers=""):
    u = region_units(regions, bookmakers); n = len(list(markets))
    return {"events": events, "markets": n, "region_units": u, "estimate": events * n * u}

def _int(v):
    try: return int(float(v))
    except (TypeError, ValueError): return None

def quota_from_headers(h):
    h = {k.lower(): v for k, v in (h or {}).items()}
    return _int(h.get("x-requests-used")), _int(h.get("x-requests-remaining"))

def floor(used, remaining): return math.ceil(FLOOR_PCT * (used + remaining))

def check(estimate, used, remaining):
    if used is None or remaining is None:
        return True, f"quota unknown (no x-requests headers yet); estimate {estimate}"
    f = floor(used, remaining); left = remaining - estimate
    if left < f:
        return False, f"stop: estimate {estimate} would leave {left} < floor {f} (10% of plan {used + remaining})"
    return True, f"ok: estimate {estimate}, remaining {remaining} -> {left} (floor {f})"

def log_headers(path, job, endpoint, headers, label="", estimate=""):
    used, rem = quota_from_headers(headers)
    h = {k.lower(): v for k, v in (headers or {}).items()}
    new = not os.path.exists(path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    et = now.astimezone(dt.timezone(dt.timedelta(hours=-5)))
    try:
        from zoneinfo import ZoneInfo; et = now.astimezone(ZoneInfo("America/New_York"))
    except Exception: pass
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(LOG_COLS)
        w.writerow([et.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%dT%H:%M:%SZ"), job, endpoint, label, estimate,
                    h.get("x-requests-last", ""), "" if used is None else used, "" if rem is None else rem])
    return used, rem
