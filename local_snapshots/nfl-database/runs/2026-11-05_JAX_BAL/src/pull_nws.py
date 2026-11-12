"""Phase 11 pre-kick weather: NWS hourly (api.weather.gov) for M&T Bank Stadium, game window 20:00-23:00 ET (kick 20:15 + 3.5h)."""
import json, urllib.request, datetime as dt
UA = {"User-Agent": "nfl-database research (box)"}
g = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
fh = g("https://api.weather.gov/points/39.278,-76.623")["properties"]["forecastHourly"]
d = g(fh); now = dt.datetime.now().strftime("%Y-%m-%dT%H:%M")
json.dump(d, open(f"nws_hourly_{now.replace(':','').replace('-','')}.json", "w"))
win = [p for p in d["properties"]["periods"] if "T20:00" <= p["startTime"][10:16] <= "T23:00" and p["startTime"].startswith("2026-11-05")]
import re
meta = dict(url=fh, pulled_et=now, nws_update=d["properties"].get("updateTime"), window=[(p["startTime"], p["probabilityOfPrecipitation"]["value"], p["windSpeed"], p["shortForecast"]) for p in win],
            window_max_precip=max(p["probabilityOfPrecipitation"]["value"] or 0 for p in win), window_max_wind=max(int(re.findall(r"\d+", p["windSpeed"])[-1]) for p in win),
            temp_f=min(p["temperature"] for p in win))
json.dump(meta, open("nws_hourly_meta.json", "w"), indent=1); print(json.dumps(meta, indent=1))
