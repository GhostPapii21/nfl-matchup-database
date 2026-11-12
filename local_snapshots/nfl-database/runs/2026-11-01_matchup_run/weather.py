import json,urllib.request,datetime
ST={"BUF":(42.7738,-78.7870,"open",18,1),"CIN":(39.0954,-84.5160,"open",18,1),"DAL":(32.7473,-97.0945,"retractable",18,1),"DET":(42.3400,-83.0456,"dome",18,1),
"NYJ":(40.8135,-74.0745,"open",18,1),"PIT":(40.4468,-80.0158,"open",18,1),"TB":(27.9759,-82.5033,"open",18,1),"JAX":(30.3239,-81.6373,"open",18,1),
"LAR":(33.9535,-118.3392,"indoor",21,1),"DEN":(39.7439,-105.0201,"open",21,1),"MIA":(25.9580,-80.2389,"open (canopy)",21,1),"WSH":(38.9078,-76.8645,"open",1,2),"SEA":(47.5952,-122.3316,"open",1,3)}
out={"pulled_et":f"{datetime.datetime.now():%Y-%m-%dT%H:%M}"}
for t,(la,lo,roof,h,d) in ST.items():
    rec={"roof":roof}
    try:
        u=f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability,precipitation&wind_speed_unit=mph&temperature_unit=fahrenheit&timezone=UTC&start_date=2026-11-01&end_date=2026-11-03"
        hh=json.load(urllib.request.urlopen(u,timeout=20))["hourly"]; ko=f"2026-11-0{d}T{h:02d}:00"
        i=hh["time"].index(ko); s=slice(i,i+4)
        rec.update(src=u,temp=hh["temperature_2m"][s],wind=hh["wind_speed_10m"][s],gust=hh["wind_gusts_10m"][s],pop=hh["precipitation_probability"][s],precip=hh["precipitation"][s])
    except Exception as e: rec["err"]=str(e)
    out[t]=rec
json.dump(out,open("weather_0810.json","w"),indent=1)
for t,r in out.items():
    if t!="pulled_et": print(t,r.get("roof"),r.get("temp"),r.get("wind"),r.get("gust"),r.get("pop"),r.get("err",""))
