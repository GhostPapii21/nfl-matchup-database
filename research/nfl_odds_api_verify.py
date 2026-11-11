"""Read-only, fail-closed NFL odds provider verification. Never print keys or odds payloads."""
import json, os, sys
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

HOST = "https://api.the-odds-api.com"
SPORT = "americanfootball_nfl"
BOOKS = {"draftkings", "fanduel", "pinnacle"}
MARKETS = {"h2h", "spreads", "totals"}
MAX_AGE_SECONDS = 7200

def validate(events, now):
    if not isinstance(events, list):
        return {"ok": False, "reason": "UNEXPECTED_SCHEMA"}
    counts = {"events": len(events), "markets": 0, "fresh_quotes": 0}
    books = set()
    failures = set()
    for event in events:
        if not isinstance(event, dict) or not all(isinstance(event.get(k), str) and event[k] for k in ("id", "home_team", "away_team", "commence_time")):
            failures.add("INVALID_EVENT_IDENTITY")
            continue
        for book in event.get("bookmakers", []):
            if not isinstance(book, dict):
                failures.add("INVALID_BOOKMAKER")
                continue
            key = book.get("key")
            if key not in BOOKS:
                continue
            books.add(key)
            for market in book.get("markets", []):
                if not isinstance(market, dict) or market.get("key") not in MARKETS:
                    continue
                counts["markets"] += 1
                stamp = market.get("last_update") or book.get("last_update")
                try:
                    parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                    age = (now - parsed).total_seconds()
                    if age < -300 or age > MAX_AGE_SECONDS:
                        failures.add("STALE_OR_FUTURE_QUOTE")
                        continue
                except (ValueError, AttributeError, TypeError):
                    failures.add("MISSING_OR_INVALID_TIMESTAMP")
                    continue
                outcomes = market.get("outcomes")
                if not isinstance(outcomes, list) or not outcomes:
                    failures.add("MISSING_OUTCOMES")
                    continue
                for o in outcomes:
                    if not isinstance(o, dict) or not isinstance(o.get("name"), str) or not o["name"] or isinstance(o.get("price"), bool) or not isinstance(o.get("price"), (int, float)) or o["price"] <= 1:
                        failures.add("INVALID_PRICE_OR_SELECTION")
                        continue
                    if market["key"] in ("spreads", "totals") and (isinstance(o.get("point"), bool) or not isinstance(o.get("point"), (int, float))):
                        failures.add("MISSING_EXACT_LINE")
                        continue
                    counts["fresh_quotes"] += 1
    if not counts["events"]:
        failures.add("NO_NFL_EVENTS")
    if not counts["fresh_quotes"]:
        failures.add("NO_VALID_FRESH_QUOTES")
    return {"ok": not failures, "checks": counts, "books_seen": sorted(books), "failures": sorted(failures)}

def run():
    token = os.environ.get("ODDS_API_KEY")
    if not token:
        return {"status": "FAIL", "reason": "SECRET_MISSING", "secret_name": "ODDS_API_KEY"}
    params = urlencode({"apiKey": token, "regions": "us,us2", "markets": ",".join(sorted(MARKETS)), "oddsFormat": "decimal", "dateFormat": "iso"})
    url = HOST + "/v4/sports/" + SPORT + "/odds/?" + params
    try:
        with urlopen(Request(url, headers={"Accept": "application/json"}), timeout=20) as response:
            raw = response.read(2_000_001)
            status = response.status
            remaining = response.headers.get("x-requests-remaining")
        if len(raw) > 2_000_000:
            return {"status": "FAIL", "reason": "OVERSIZED_RESPONSE"}
        if status != 200:
            return {"status": "FAIL", "reason": "HTTP_NON_200", "http_status": status}
        verdict = validate(json.loads(raw), datetime.now(timezone.utc))
        return {"status": "PASS" if verdict["ok"] else "FAIL", "authentication": "HTTP_200", "sport": SPORT, "remaining_quota": remaining, **verdict}
    except HTTPError as exc:
        return {"status": "FAIL", "reason": "PROVIDER_HTTP_ERROR", "http_status": exc.code}
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "reason": "REQUEST_OR_SCHEMA_ERROR", "error_class": type(exc).__name__}

if __name__ == "__main__":
    result = run()
    print("ODDS_API_VERIFICATION=" + json.dumps(result, sort_keys=True))
    sys.exit(0 if result["status"] == "PASS" else 1)
