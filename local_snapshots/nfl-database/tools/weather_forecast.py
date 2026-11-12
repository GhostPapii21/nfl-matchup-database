#!/usr/bin/env python3
"""Multi-day game-window weather forecast at slip-build time (Rico 2026-11-01, BUG-2026-11-01-WXDAYS).
Slips are built days before kickoff, so this runs when slips are built and with the Mon-Sat 10 AM refresh; the
existing pre-kickoff NWS rechecks stay. Sources: NWS hourly (api.weather.gov, ~7 days) + Open-Meteo (16 days).
Window = kickoff to kickoff+3.5h (ET). Worse of the two sources is used. Flag (inclusive): precip >=50%, gusts >=20 mph,
sustained >=15 mph. Unknown/retractable roofs count as open-air. Blank wind = unknown, never 0.
Usage: python3 weather_forecast.py --week 9 [--out-dir DIR]   -> DIR/forecast_YYYY-MM-DD_HHMM.json (never overwrites)"""
import argparse, json, os, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
HERE = os.path.dirname(os.path.abspath(__file__))
PRECIP, GUST, WIND = 50, 20, 15
CLOSED = ("dome", "indoor", "closed", "retractable_closed")
UA = {"User-Agent": "nfl-database research (box)"}
def is_open_air(roof): return not any(x in str(roof).lower() for x in CLOSED)
def _win(ko):
    k = datetime.fromisoformat(ko); return k, k + timedelta(hours=3, minutes=30)
def _mx(v):
    v = [x for x in v if isinstance(x, (int, float))]; return max(v) if v else None
def summarize_om(h, ko):
    a, b = _win(ko); idx = [i for i, t in enumerate(h["time"]) if a <= datetime.fromisoformat(t) < b]
    if not idx: return None
    g = lambda k: _mx([h[k][i] for i in idx])
    return dict(precip_pct=g("precipitation_probability"), wind_mph=g("wind_speed_10m"), gust_mph=g("wind_gusts_10m"),
                precip_in=round(sum(h["precipitation"][i] or 0 for i in idx), 2), hours=len(idx))
def _nws_wind(s):
    n = re.findall(r"\d+", str(s or "")); return int(n[-1]) if n else None
def summarize_nws(periods, ko):
    a, b = _win(ko); w = []
    for p in periods:
        t = datetime.fromisoformat(p["startTime"])
        if t.tzinfo: t = t.astimezone(timezone(timedelta(hours=-5))).replace(tzinfo=None)   # ET (EST after Nov 1 2026)
        if a <= t < b: w.append(p)
    if not w: return None
    return dict(precip_pct=_mx([(p.get("probabilityOfPrecipitation") or {}).get("value") for p in w]),
                wind_mph=_mx([_nws_wind(p.get("windSpeed")) for p in w]), gust_mph=_mx([_nws_wind(p.get("windGust")) for p in w]),
                short=sorted({p.get("shortForecast") for p in w if p.get("shortForecast")}), hours=len(w))
def flags(pp, gu, wi):
    out = []
    if isinstance(pp, (int, float)) and pp >= PRECIP: out.append(f"precip {pp:g}%")
    if isinstance(gu, (int, float)) and gu >= GUST: out.append(f"gusts {gu:g} mph")
    if isinstance(wi, (int, float)) and wi >= WIND: out.append(f"sustained wind {wi:g} mph")
    return out
def combine(roof, nws, om):
    e = dict(roof=roof, nws=nws, open_meteo=om, notes=[])
    if not is_open_air(roof):
        return dict(e, status="INDOOR", flag=False, why=[], precip_pct=None, gust_mph=None, wind_mph=None)
    if nws is None: e["notes"].append("nws missing")
    if om is None: e["notes"].append("open_meteo missing")
    src = [s for s in (nws, om) if s]
    if not src: return dict(e, status="MISSING", flag=None, why=[], precip_pct=None, gust_mph=None, wind_mph=None)
    v = {k: _mx([s.get(k) for s in src]) for k in ("precip_pct", "gust_mph", "wind_mph")}
    if any(x is None for x in v.values()): e["notes"].append(f"unknown {[k for k, x in v.items() if x is None]} (not treated as 0)")
    why = flags(v["precip_pct"], v["gust_mph"], v["wind_mph"])
    return dict(e, status="OK" if v["precip_pct"] is not None else "MISSING", flag=bool(why) if v["precip_pct"] is not None else None, why=why, **v)
def load_schedule(week):
    return json.load(open(os.path.join(HERE, f"schedule_2026_wk{week}.json")))["games"]
def _get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25))
def fetch_game(g):
    nws = om = None; err = []
    if -125 < g["lon"] < -66:
        try:
            pt = _get(f"https://api.weather.gov/points/{g['lat']},{g['lon']}")
            nws = summarize_nws(_get(pt["properties"]["forecastHourly"])["properties"]["periods"], g["kickoff_et"])
            if nws is None: err.append("nws: kickoff beyond hourly range")
        except Exception as x: err.append(f"nws: {type(x).__name__}")
    try:
        u = (f"https://api.open-meteo.com/v1/forecast?latitude={g['lat']}&longitude={g['lon']}&hourly=precipitation_probability,precipitation,"
             "wind_speed_10m,wind_gusts_10m,temperature_2m&wind_speed_unit=mph&precipitation_unit=inch&timezone=America/New_York&forecast_days=16")
        om = summarize_om(_get(u)["hourly"], g["kickoff_et"])
    except Exception as x: err.append(f"open_meteo: {type(x).__name__}")
    return nws, om, err
def run(games, out_dir, now=None, fetch=True):
    now = now or f"{datetime.now():%Y-%m-%dT%H:%M}"; out = {}
    for g in games:
        nws, om, err = fetch_game(g) if fetch and is_open_air(g["roof"]) else (None, None, [])
        e = combine(g["roof"], nws, om); e["notes"] += err; e["kickoff_et"] = g["kickoff_et"]; out[g["game"]] = e
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, f"forecast_{now[:10]}_{now[11:13]}{now[14:16]}.json"); i = 1
    while os.path.exists(p): p = p.replace(".json", f"_{i}.json") if i == 1 else re.sub(r"_\d+\.json$", f"_{i}.json", p); i += 1
    json.dump(dict(pulled_et=now, source="tools/weather_forecast.py (api.weather.gov hourly + api.open-meteo.com)", thresholds=dict(precip_pct=PRECIP, gust_mph=GUST, wind_mph=WIND),
                   window="kickoff to kickoff+3.5h ET; worse source", games=out), open(p, "w"), indent=1)
    return p
def latest(out_dir):
    f = sorted(x for x in os.listdir(out_dir) if x.startswith("forecast_") and x.endswith(".json")) if os.path.isdir(out_dir) else []
    return os.path.join(out_dir, f[-1]) if f else None
if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--week", type=int, default=9); a.add_argument("--out-dir"); o = a.parse_args()
    d = o.out_dir or f"/workspace/nfl-database/week{o.week}/weather_forecast"
    p = run(load_schedule(o.week), d); j = json.load(open(p)); print(f"wrote {p} (pulled {j['pulled_et']} ET)")
    for g, e in j["games"].items():
        print(f"{g:9} {e['kickoff_et']} {e['status']:7} {'FLAG ' + ', '.join(e['why']) if e['flag'] else ('-' if e['flag'] is False else 'UNKNOWN')}"
              f"  precip {e['precip_pct']} gust {e['gust_mph']} wind {e['wind_mph']}  {'; '.join(e['notes'])}")
