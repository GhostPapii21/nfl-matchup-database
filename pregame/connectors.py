"""Which keyed data sources this run can actually use. Reports names and statuses only, never a key or a payload.

A key saved inside ChatGPT or Grok is invisible here: scheduled runs only see GitHub repository secrets.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

KEYS = (("ODDS_API_KEY", "The Odds API", "Pinnacle / DraftKings / FanDuel prices, props and line movement in every packet"),
        ("NFL_BDL_API_KEY", "BallDontLie NFL", "second-source check of the slate (schedule and teams)"),
        ("NFL_API_SPORTS_KEY", "API-Sports NFL", "access check only; not used in the packet"))


def _bdl_slate(season, week, fetch_http):
    ev = fetch_http("balldontlie_nfl", "games", enabled=True, params={"season": season, "week": week, "per_page": 100})
    rows = ev["data"].get("data") if isinstance(ev["data"], dict) else None
    if not isinstance(rows, list):
        return None
    out = set()
    for g in rows:
        h, a = (g.get("home_team") or {}).get("abbreviation"), (g.get("visitor_team") or {}).get("abbreviation")
        if h and a:
            out.add((FIX.get(a, a), FIX.get(h, h)))
    return out


FIX = {"LAR": "LA", "WSH": "WAS", "JAC": "JAX"}


def check(season, week, slate, *, offline=False, env=None, fetch_http=None) -> dict:
    """slate: iterable of (away, home) the packet builder is about to use."""
    env = os.environ if env is None else env
    out = {"checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "sources": {},
           "note": "Scheduled runs only see GitHub repository secrets. A key connected inside a chat tool is not visible here."}
    for name, label, use in KEYS:
        out["sources"][name] = {"provider": label, "used_for": use,
                                "status": "KEY_PRESENT" if env.get(name, "").strip() else "KEY_NOT_CONFIGURED_IN_THIS_RUN"}
    if offline:
        return out
    if fetch_http is None:
        try:
            from source_adapters.nfl_external_sources import fetch_http
        except Exception:
            return out
    bdl = out["sources"]["NFL_BDL_API_KEY"]
    if bdl["status"] == "KEY_PRESENT":
        try:
            theirs = _bdl_slate(season, week, fetch_http)
            mine = set(slate)
            if theirs is None:
                bdl["status"] = "KEY_PRESENT_UNEXPECTED_RESPONSE"
            else:
                missing = sorted(f"{a}@{h}" for a, h in mine - theirs)
                bdl.update(status="OK", slate_check="MATCH" if not missing else "MISMATCH",
                           games_not_found_at_provider=missing, provider_games_this_week=len(theirs))
        except Exception as exc:
            bdl["status"] = f"KEY_PRESENT_REQUEST_FAILED: {type(exc).__name__}"
    aps = out["sources"]["NFL_API_SPORTS_KEY"]
    if aps["status"] == "KEY_PRESENT":
        try:
            ev = fetch_http("api_sports_nfl", "games", enabled=True, params={"season": season})
            d = ev["data"]
            if isinstance(d, dict) and isinstance(d.get("response"), list) and not d.get("errors"):
                aps.update(status="OK", games_returned=len(d["response"]))
            else:
                aps["status"] = "KEY_PRESENT_PROVIDER_ERROR"
                err = d.get("errors") if isinstance(d, dict) else None       # the provider's own explanation (plan, season, quota)
                key = env.get("NFL_API_SPORTS_KEY", "")
                aps["provider_message"] = str(err)[:300].replace(key, "***") if err else "no error text returned"
        except Exception as exc:
            aps["status"] = f"KEY_PRESENT_REQUEST_FAILED: {type(exc).__name__}"
    return out
