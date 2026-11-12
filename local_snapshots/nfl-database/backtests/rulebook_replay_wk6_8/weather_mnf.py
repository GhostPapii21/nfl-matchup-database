import json,urllib.request,datetime as dt
w=json.load(open('weather_wk6_8.json')); la,lo=47.595,-122.332; k=dt.datetime(2026,11,3,1,15)
rec=dict(game='CHI@SEA',game_id='2026_MNF_CHI_SEA',stadium='Lumen Field',roof='outdoors',lat=la,lon=lo,kickoff_utc=k.isoformat()+'+00:00',note='roof from Lumen Field (open-air); pbp has no MNF row')
for lab,base,hv in (('kickoff','https://historical-forecast-api.open-meteo.com/v1/forecast','precipitation_probability,precipitation,wind_speed_10m,wind_gusts_10m'),
                    ('day_before','https://previous-runs-api.open-meteo.com/v1/forecast','precipitation_probability_previous_day1,wind_speed_10m_previous_day1,wind_gusts_10m_previous_day1')):
    u=f"{base}?latitude={la}&longitude={lo}&hourly={hv}&wind_speed_unit=mph&timezone=UTC&start_date=2026-11-01&end_date=2026-11-03"
    try: h=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'nfl-database research'}),timeout=40))['hourly']
    except Exception as x: rec[lab]=dict(status='MISSING',err=str(x),url=u); continue
    idx=[i for i,t in enumerate(h['time']) if k<=dt.datetime.fromisoformat(t)<k+dt.timedelta(hours=3,minutes=30)]
    ks=[x for x in h if x!='time']; f=lambda p:[x for x in ks if x.startswith(p)][0]; mx=lambda key:max([h[key][i] for i in idx if h[key][i] is not None],default=None)
    rec[lab]=dict(status='OK',precip_pct=mx(f('precipitation_probability')),wind_mph=mx(f('wind_speed')),gust_mph=mx(f('wind_gusts')),hours=len(idx),url=u)
w['CHI@SEA']=rec; json.dump(w,open('weather_wk6_8.json','w'),indent=1); print(rec)
