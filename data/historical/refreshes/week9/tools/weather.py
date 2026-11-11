"""Week 9 rolling weather. RERUN DAILY through Sun Nov 8 (and ~2h before each kick).
Source: Open-Meteo forecast API (hourly, mph, America/New_York). Appends a dated table to weather/WEATHER_<date>.md"""
import json, urllib.request, datetime, os
G=[("JAX@BAL","2026-11-05T20:15",39.278,-76.623,"Open-air"),
("CIN vs ATL (Madrid)","2026-11-08T09:30",40.453,-3.688,"Retractable roof (Bernabeu) - status TBD"),
("NYJ@KC","2026-11-08T13:00",39.049,-94.484,"Open-air"),
("DET@MIA","2026-11-08T13:00",25.958,-80.239,"Open-air (canopy over seats)"),
("NYG@PHI","2026-11-08T13:00",39.901,-75.168,"Open-air"),
("LAR@WSH","2026-11-08T13:00",38.908,-76.864,"Open-air"),
("DEN@CAR","2026-11-08T13:00",35.226,-80.853,"Open-air"),
("HOU@LAC","2026-11-08T16:05",33.953,-118.339,"Fixed translucent roof, open sides (minimal weather)"),
("GB@NE","2026-11-08T16:25",42.091,-71.264,"Open-air"),
("LV@SF","2026-11-08T16:25",37.403,-121.970,"Open-air"),
("ARI@SEA","2026-11-08T16:25",47.595,-122.332,"Open-air (partial roof)"),
("TB@CHI","2026-11-08T20:20",41.862,-87.617,"Open-air")]
DOMES="DAL@IND (Lucas Oil, retractable), CLE@NO (Superdome), BUF@MIN (US Bank, fixed)"
now=datetime.datetime.now(); rows=[]
for name,ko,la,lo,roof in G:
    u=f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&hourly=precipitation_probability,precipitation,wind_speed_10m,wind_gusts_10m,temperature_2m&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch&timezone=America/New_York&forecast_days=9"
    h=json.load(urllib.request.urlopen(u))["hourly"]
    k=datetime.datetime.fromisoformat(ko); idx=[i for i,t in enumerate(h["time"]) if k<=datetime.datetime.fromisoformat(t)<k+datetime.timedelta(hours=3,minutes=30)]
    if not idx: rows.append((name,ko,roof,None)); continue
    pp=max(h["precipitation_probability"][i] or 0 for i in idx); pr=sum(h["precipitation"][i] or 0 for i in idx)
    ws=max(h["wind_speed_10m"][i] for i in idx); wg=max(h["wind_gusts_10m"][i] for i in idx); tt=sum(h["temperature_2m"][i] for i in idx)/len(idx)
    fl=[]; 
    if pp>=50: fl.append("PRECIP50")
    if wg>=20: fl.append("GUST20")
    if ws>=15: fl.append("WIND15")
    if "Retractable" in roof or "Fixed" in roof: fl=[f+"(roof-mitigated)" for f in fl]
    rows.append((name,ko,roof,(pp,pr,ws,wg,tt,fl)))
os.makedirs("weather",exist_ok=True); fn=f"weather/WEATHER_{now:%Y-%m-%d}.md"
with open(fn,"a") as f:
    f.write(f"\n## Pull {now:%Y-%m-%d %H:%M} ET — Open-Meteo hourly (kick to kick+3.5h, ET)\n> RERUN DAILY through Sunday Nov 8; final check ~2h before each kick (NWS hourly per skill rain rule). Forecasts >3 days out are low-confidence.\n\n| Game | Kick (ET) | Roof | Max precip % | Precip in | Max sustained mph | Max gust mph | Temp F | Flags |\n|---|---|---|---|---|---|---|---|---|\n")
    for n,ko,roof,v in rows:
        if v is None: f.write(f"| {n} | {ko} | {roof} | MISSING (beyond forecast window) |||||| |\n"); continue
        pp,pr,ws,wg,tt,fl=v; f.write(f"| {n} | {ko[5:].replace('T',' ')} | {roof} | {pp} | {pr:.2f} | {ws:.0f} | {wg:.0f} | {tt:.0f} | {' '.join(fl) or '-'} |\n")
    f.write(f"\nDomes / roof games (no weather): {DOMES}.\nThresholds: precip ≥50%, gusts ≥20 mph, sustained ≥15 mph. A flag here = Phase-11 review flag and triggers the approved game-script RB rule (weather branch) only if it persists to the kickoff-window check.\n")
print(open(fn).read())
