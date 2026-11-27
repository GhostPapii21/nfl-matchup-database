"""Rule 3, HOURLY WEATHER GRADE (flag only). NWS (api.weather.gov) and Open-Meteo ONLY; never PFF weather.

For each hour of the game window (kickoff hour + the next 3 by default):
  rain rate (in/hr): none (0) | light (> 0 and < 0.05) | moderate (0.05 to 0.3 inclusive) | heavy (> 0.3)
  sustained wind and gusts (mph), per source, side by side. Sources are never silently averaged.
Dome / closed roof -> "indoor, not graded". A failed or missing pull -> "unknown", never calm or dry.
Then one stated run-tilt read per team. The read is a flag, not a cut.
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Callable

from pipeline.read_rules import UNKNOWN

LIGHT_MAX, MODERATE_MAX = 0.05, 0.3
WIND_TILT, GUST_TILT = 15.0, 25.0
UA = {"User-Agent": "nfl-read-rules/1.0 (research; public data)", "Accept": "application/geo+json"}
MM_PER_IN = 25.4


def grade_rain(rate_in_hr) -> str:
    if rate_in_hr is None or rate_in_hr == UNKNOWN:
        return UNKNOWN
    r = float(rate_in_hr)
    if r != r or r < 0:
        return UNKNOWN
    if r == 0:
        return "none"
    if r < LIGHT_MAX:
        return "light"
    if r <= MODERATE_MAX:
        return "moderate"
    return "heavy"


def _default_fetch(url: str, timeout: int = 30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return json.loads(r.read())


def _hours(kickoff_utc: datetime, n_hours: int) -> list[datetime]:
    k = kickoff_utc.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return [k + timedelta(hours=i) for i in range(n_hours)]


def open_meteo_hourly(lat: float, lon: float, hours: list[datetime], fetch: Callable = _default_fetch) -> dict:
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f&hourly=precipitation,wind_speed_10m,"
           "wind_gusts_10m&wind_speed_unit=mph&precipitation_unit=inch&timezone=UTC&forecast_days=16" % (lat, lon))
    pulled = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        j = fetch(url)
        h = j["hourly"]
        idx = {t: i for i, t in enumerate(h["time"])}
        out = {}
        for hr in hours:
            i = idx.get(hr.strftime("%Y-%m-%dT%H:00"))
            out[hr] = (dict(precip_in=h["precipitation"][i], wind_mph=h["wind_speed_10m"][i], gust_mph=h["wind_gusts_10m"][i])
                       if i is not None else None)
        return dict(ok=True, source="Open-Meteo forecast API", url=url, pulled_at=pulled, hours=out)
    except Exception as e:  # noqa: BLE001 - never raise; unknown instead
        return dict(ok=False, source="Open-Meteo forecast API", url=url, pulled_at=pulled, error=str(e)[:200], hours={})


def _iso_dur_hours(s: str) -> float:
    """PT1H / PT3H / P1DT2H -> hours."""
    s = s.upper()
    days = float(s.split("P")[1].split("D")[0]) if "D" in s else 0.0
    t = s.split("T")[1] if "T" in s else ""
    hrs = float(t.split("H")[0]) if "H" in t else 0.0
    return days * 24 + hrs


def _nws_series(prop: dict, conv) -> list[tuple[datetime, float, float]]:
    out = []
    for v in (prop or {}).get("values", []):
        start, dur = v["validTime"].split("/")
        t0 = datetime.fromisoformat(start.replace("Z", "+00:00"))
        if v.get("value") is None:
            continue
        out.append((t0, _iso_dur_hours(dur) or 1.0, conv(v["value"])))
    return out


def _at(series, hr):
    for t0, dur, val in series:
        if t0 <= hr < t0 + timedelta(hours=dur):
            return t0, dur, val
    return None


def nws_hourly(lat: float, lon: float, hours: list[datetime], fetch: Callable = _default_fetch) -> dict:
    """NWS gridpoint raw forecast: quantitativePrecipitation (mm per period, spread evenly per hour), windSpeed and
    windGust (km/h -> mph). NWS QPF periods are often 6 h long; the period total is spread evenly over its hours
    (precip_period_hours says how long), so an NWS hourly rate is a period average, not a peak."""
    pulled = datetime.now(timezone.utc).isoformat(timespec="seconds")
    url = f"https://api.weather.gov/points/{lat:.4f},{lon:.4f}"
    try:
        grid_url = fetch(url)["properties"]["forecastGridData"]
        g = fetch(grid_url)["properties"]
        kmh = lambda x: float(x) * 0.621371  # noqa: E731
        qpf = _nws_series(g.get("quantitativePrecipitation"), lambda x: float(x) / MM_PER_IN)
        ws = _nws_series(g.get("windSpeed"), kmh)
        wg = _nws_series(g.get("windGust"), kmh)
        out = {}
        for hr in hours:
            q, w, gu = _at(qpf, hr), _at(ws, hr), _at(wg, hr)
            out[hr] = dict(precip_in=(q[2] / q[1]) if q else None, wind_mph=w[2] if w else None,
                           gust_mph=gu[2] if gu else None,
                           precip_period_hours=q[1] if q else None)
        return dict(ok=True, source="NWS api.weather.gov gridpoint forecast", url=grid_url, pulled_at=pulled, hours=out)
    except Exception as e:  # noqa: BLE001
        return dict(ok=False, source="NWS api.weather.gov gridpoint forecast", url=url, pulled_at=pulled,
                    error=str(e)[:200], hours={})


def _num(v, nd: int = 3):
    return UNKNOWN if v is None else round(float(v), nd)


def grade_window(kickoff_utc: datetime, lat: float | None, lon: float | None, roof: str | None = None,
                 n_hours: int = 4, fetch: Callable = _default_fetch, sources=None) -> dict:
    """Hour-by-hour grade for the window. `sources` (list of already-fetched source dicts) skips the network."""
    if (roof or "").lower() in ("dome", "closed"):
        return dict(graded=False, status="indoor, not graded", roof=roof, hours=[], sources=[])
    if lat is None or lon is None:
        return dict(graded=False, status=UNKNOWN, note="stadium not mapped; check by hand", hours=[], sources=[])
    hrs = _hours(kickoff_utc, n_hours)
    srcs = sources if sources is not None else [nws_hourly(lat, lon, hrs, fetch), open_meteo_hourly(lat, lon, hrs, fetch)]
    rows = []
    for hr in hrs:
        row = {"hour_utc": hr.isoformat(timespec="minutes")}
        for s in srcs:
            key = "nws" if s["source"].startswith("NWS") else "open_meteo"
            v = (s.get("hours") or {}).get(hr) if s.get("ok") else None
            row[key] = dict(rain_in_hr=_num(v and v.get("precip_in")), rain_grade=grade_rain(v and v.get("precip_in")),
                            wind_mph=_num(v and v.get("wind_mph"), 1), gust_mph=_num(v and v.get("gust_mph"), 1),
                            source=s["source"], pulled_at=s.get("pulled_at", UNKNOWN))
        grades = {row[k]["rain_grade"] for k in ("nws", "open_meteo") if k in row}
        row["sources_disagree"] = len(grades - {UNKNOWN}) > 1
        rows.append(row)
    return dict(graded=True, status="graded", roof=roof or UNKNOWN, hours=rows,
                sources=[{k: s.get(k) for k in ("source", "url", "pulled_at", "ok", "error") if k in s} for s in srcs])


def worst(grade_rows: list[dict]) -> dict:
    """Worst rain grade, max sustained wind and max gust across hours and sources (unknown if nothing known)."""
    order = ["none", "light", "moderate", "heavy"]
    g, w, gu = [], [], []
    for r in grade_rows:
        for k in ("nws", "open_meteo"):
            v = r.get(k)
            if not v:
                continue
            if v["rain_grade"] in order:
                g.append(order.index(v["rain_grade"]))
            if v["wind_mph"] != UNKNOWN:
                w.append(v["wind_mph"])
            if v["gust_mph"] != UNKNOWN:
                gu.append(v["gust_mph"])
    return dict(rain=order[max(g)] if g else UNKNOWN, wind_mph=max(w) if w else UNKNOWN, gust_mph=max(gu) if gu else UNKNOWN)


def run_tilt(grade: dict, team: str, team_rush_rate: float | None = None, league_rush_rate: float | None = None) -> str:
    """One plain stated read per team. Flag only."""
    if not grade.get("graded"):
        return f"{team}: {grade.get('status', UNKNOWN)}; no weather run-tilt."
    w = worst(grade["hours"])
    if w["rain"] == UNKNOWN and w["wind_mph"] == UNKNOWN:
        return f"{team}: weather unknown (pulls failed); no run-tilt read."
    bad = w["rain"] in ("moderate", "heavy") or (w["wind_mph"] != UNKNOWN and w["wind_mph"] >= WIND_TILT) or (
        w["gust_mph"] != UNKNOWN and w["gust_mph"] >= GUST_TILT)
    base = (f"worst hour rain {w['rain']}, sustained {w['wind_mph']} mph, gusts {w['gust_mph']} mph")
    lean = ""
    if team_rush_rate is not None and league_rush_rate is not None:
        lean = (" Already run-leaning offense (rush rate %.0f%% vs league %.0f%%)." if team_rush_rate > league_rush_rate
                else " Pass-leaning offense (rush rate %.0f%% vs league %.0f%%), so the shift matters more.") % (
            100 * team_rush_rate, 100 * league_rush_rate)
    if bad:
        return f"{team}: run-tilt UP; deep passing and kicking down ({base}).{lean} Flag only."
    return f"{team}: no weather run-tilt ({base}).{lean} Flag only."
