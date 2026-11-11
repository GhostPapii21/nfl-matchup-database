"""Kickoff forecast from the US National Weather Service (api.weather.gov; free, no key). Never raises.

Only outdoor (or unknown-roof) games at a US home stadium get a forecast. Neutral-site and international games
are labelled NOT_MAPPED so the analyst checks by hand.
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timedelta, timezone

# Home stadium coordinates (degrees). Approximate to the stadium; NWS resolves them to a 2.5 km forecast cell.
STADIUM = {"ARI": (33.5276, -112.2626), "ATL": (33.7554, -84.4009), "BAL": (39.2780, -76.6227), "BUF": (42.7738, -78.7870), "CAR": (35.2258, -80.8528),
           "CHI": (41.8623, -87.6167), "CIN": (39.0955, -84.5161), "CLE": (41.5061, -81.6995), "DAL": (32.7473, -97.0945), "DEN": (39.7439, -105.0201),
           "DET": (42.3400, -83.0456), "GB": (44.5013, -88.0622), "HOU": (29.6847, -95.4107), "IND": (39.7601, -86.1639), "JAX": (30.3239, -81.6373),
           "KC": (39.0489, -94.4839), "LV": (36.0909, -115.1833), "LAC": (33.9535, -118.3392), "LA": (33.9535, -118.3392), "MIA": (25.9580, -80.2389),
           "MIN": (44.9737, -93.2575), "NE": (42.0909, -71.2643), "NO": (29.9511, -90.0812), "NYG": (40.8135, -74.0745), "NYJ": (40.8135, -74.0745),
           "PHI": (39.9008, -75.1675), "PIT": (40.4468, -80.0158), "SF": (37.4033, -121.9694), "SEA": (47.5952, -122.3316), "TB": (27.9759, -82.5033),
           "TEN": (36.1665, -86.7713), "WAS": (38.9076, -76.8645)}
INDOOR = {"dome", "closed"}
UA = {"User-Agent": "nfl-pregame-packet/1.0 (research; public data)", "Accept": "application/geo+json"}


def _get(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return json.loads(r.read())


def kickoff_utc(gameday: str, gametime_et: str) -> datetime:
    """Schedule times are US Eastern. EST (UTC-5) from the first Sunday of November to the second Sunday of March."""
    d = datetime.fromisoformat(f"{gameday}T{gametime_et}:00")
    nov1 = datetime(d.year, 11, 1); first_sun_nov = nov1 + timedelta(days=(6 - nov1.weekday()) % 7)
    mar1 = datetime(d.year, 3, 1); second_sun_mar = mar1 + timedelta(days=(6 - mar1.weekday()) % 7 + 7)
    dst = second_sun_mar <= d < first_sun_nov
    return (d + timedelta(hours=4 if dst else 5)).replace(tzinfo=timezone.utc)


def forecast(home, roof, site, gameday, gametime_et, *, offline=False, fetch=_get) -> dict:
    if (roof or "").lower() in INDOOR:
        return {"status": "INDOOR", "roof": roof}
    if str(site) != "Home" or home not in STADIUM:
        return {"status": "NOT_MAPPED_NEUTRAL_OR_INTERNATIONAL_SITE: check the forecast by hand"}
    if offline:
        return {"status": "SKIPPED_OFFLINE"}
    try:
        ko = kickoff_utc(str(gameday), str(gametime_et))
        lat, lon = STADIUM[home]
        url = fetch(f"https://api.weather.gov/points/{lat},{lon}")["properties"]["forecastHourly"]
        periods = fetch(url)["properties"]["periods"]
        game = [p for p in periods if ko - timedelta(minutes=59) <= datetime.fromisoformat(p["startTime"]).astimezone(timezone.utc) < ko + timedelta(hours=3, minutes=30)]
        if not game:
            return {"status": "KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days", "kickoff_utc": ko.isoformat()}
        wind = [float(str(p.get("windSpeed", "0")).split()[0]) for p in game]
        pop = [(p.get("probabilityOfPrecipitation") or {}).get("value") or 0 for p in game]
        return {"status": "OK", "source": "US National Weather Service hourly forecast", "url": url,
                "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kickoff_utc": ko.isoformat(),
                "roof": roof or "not listed (may be retractable: confirm open or closed)",
                "at_kickoff": {"temp_f": game[0].get("temperature"), "wind_mph": wind[0], "wind_dir": game[0].get("windDirection"),
                               "precip_chance_pct": pop[0], "summary": game[0].get("shortForecast")},
                "during_game": {"temp_f_min": min(p.get("temperature") for p in game), "wind_mph_max": max(wind), "precip_chance_pct_max": max(pop)},
                "flags": [x for x in ("WIND_15_PLUS" if max(wind) >= 15 else None, "PRECIP_50_PLUS" if max(pop) >= 50 else None,
                                      "FREEZING" if min(p.get("temperature") for p in game) <= 32 else None) if x]}
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}"}
