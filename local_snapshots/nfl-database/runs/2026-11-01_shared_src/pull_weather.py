import json,urllib.request,datetime
ST={"BUF":(42.7738,-78.7870,"open"),"CIN":(39.0954,-84.5160,"open"),"DAL":(32.7473,-97.0945,"retractable"),"DET":(42.3400,-83.0456,"dome"),
"NYJ":(40.8135,-74.0745,"open"),"PIT":(40.4468,-80.0158,"open"),"TB":(27.9759,-82.5033,"open"),"JAX":(30.3239,-81.6373,"open"),
"LAR":(33.9535,-118.3392,"fixed translucent roof (indoor)"),"DEN":(39.7439,-105.0201,"open"),"MIA":(25.9580,-80.2389,"open (canopy)"),"WSH":(38.9078,-76.8645,"open")}
KO={"BUF":18,"CIN":18,"DAL":18,"DET":18,"NYJ":18,"PIT":18,"TB":18,"JAX":18,"LAR":21,"DEN":21,"MIA":21,"WSH":25}  # UTC hour of kickoff (25 = 01 UTC next day)
H={"User-Agent":"nfl-database research (box) contact: none"}
out={}
for t,(la,lo,roof) in ST.items():
    rec={"roof":roof}
    try:
        pt=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.weather.gov/points/{la},{lo}",headers=H),timeout=20))
        hr=json.load(urllib.request.urlopen(urllib.request.Request(pt["properties"]["forecastHourly"],headers=H),timeout=20))
        per=hr["properties"]["periods"]; rec["nws_url"]=pt["properties"]["forecastHourly"]
        ko=datetime.datetime(2026,11,1,tzinfo=datetime.timezone.utc)+datetime.timedelta(hours=KO[t])
        win=[p for p in per if 0<= (datetime.datetime.fromisoformat(p["startTime"]).astimezone(datetime.timezone.utc)-ko).total_seconds()/3600 <4]
        rec["nws"]=[dict(t=p["startTime"],temp=p["temperature"],wind=p["windSpeed"],dir=p["windDirection"],pop=(p.get("probabilityOfPrecipitation") or {}).get("value"),sf=p["shortForecast"]) for p in win]
    except Exception as e: rec["nws_err"]=str(e)
    try:
        u=f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability,precipitation&wind_speed_unit=mph&temperature_unit=fahrenheit&timezone=UTC&start_date=2026-11-01&end_date=2026-11-02"
        om=json.load(urllib.request.urlopen(u,timeout=20)); hh=om["hourly"]; rec["om_url"]=u
        idx=[i for i,x in enumerate(hh["time"]) if 0<=(datetime.datetime.fromisoformat(x)-datetime.datetime(2026,11,1)).total_seconds()/3600-KO[t]<4]
        rec["om"]=[dict(t=hh["time"][i],temp=hh["temperature_2m"][i],wind=hh["wind_speed_10m"][i],gust=hh["wind_gusts_10m"][i],pop=hh["precipitation_probability"][i],mm=hh["precipitation"][i]) for i in idx]
    except Exception as e: rec["om_err"]=str(e)
    out[t]=rec
out["_pulled_et"]=f"{datetime.datetime.now():%Y-%m-%dT%H:%M}"
json.dump(out,open("weather.json","w"),indent=1)
for t,r in out.items():
    if t.startswith("_"): continue
    om=r.get("om",[]); print(t,r["roof"],"NWS",[(x["temp"],x["wind"],x["pop"]) for x in r.get("nws",[])][:4], "OM maxwind",max([x["wind"] for x in om] or [None]),"gust",max([x["gust"] for x in om] or [None]),"pop",max([x["pop"] or 0 for x in om] or [None]), r.get("nws_err",""),r.get("om_err",""))
open("pull_log.txt","a").write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} python urllib api.weather.gov hourly + api.open-meteo.com for 12 stadiums -> weather.json\n")
