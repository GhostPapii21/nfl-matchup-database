"""Kickoff-window weather (Phase 11) + day-before forecast for Wk6-8 games, Open-Meteo only (approved source).
Phase 11 = Open-Meteo historical-forecast API at the kickoff window (what the forecast said for that hour, model run nearest kickoff).
Forecast block = Open-Meteo previous-runs API, forecast issued ~1 day before (Day-1 run)."""
import json,urllib.request,datetime as dt,pandas as pd,time
C={'SoFi Stadium':(33.953,-118.339),'Huntington Bank Field':(41.506,-81.700),'Allegiant Stadium':(36.091,-115.184),'Lincoln Financial Field':(39.901,-75.168),
'Mercedes-Benz Stadium':(33.755,-84.401),'Lambeau Field':(44.501,-88.062),'Wembley Stadium':(51.556,-0.280),'Arrowhead Stadium':(39.049,-94.484),
'MetLife Stadium':(40.814,-74.074),'Gillette Stadium':(42.091,-71.264),'Raymond James Stadium':(27.976,-82.503),'Empower Field at Mile High':(39.744,-105.020),
'Lucas Oil Stadium':(39.760,-86.164),"Levi's® Stadium":(37.403,-121.970),'M&T Bank Stadium':(39.278,-76.623),'Nissan Stadium':(36.166,-86.771),
'State Farm Stadium':(33.528,-112.263),'Ford Field':(42.340,-83.046),'U.S. Bank Stadium':(44.974,-93.258),'Lumen Field':(47.595,-122.332),
'Soldier Field':(41.862,-87.617),'Reliant Stadium':(29.685,-95.411),'Stade de France':(48.924,2.360),'Bank of America Stadium':(35.226,-80.853),
'AT&T Stadium':(32.748,-97.093),'Highmark Stadium':(42.774,-78.787),'Acrisure Stadium':(40.447,-80.016),'EverBank Stadium':(30.324,-81.637),
'Hard Rock Stadium':(25.958,-80.239),'Northwest Stadium':(38.908,-76.864),'Paycor Stadium':(39.095,-84.516)}
P=pd.read_parquet('/workspace/nfl-database/runs/2026-11-02_shared_src/play_by_play_2026.parquet',columns=['week','game_id','stadium','roof','home_team','away_team'])
G=P[P.week.isin([6,7,8])].drop_duplicates('game_id')
L=pd.read_csv('../current_rules_wk6_8/real_lines_wk6_8.csv').drop_duplicates('event')
AB=json.load(open('abbr.json'))
ko={}
for _,e in L.iterrows(): ko[(AB[e.away],AB[e.home])]=e.commence
H='precipitation_probability,precipitation,wind_speed_10m,wind_gusts_10m'
def get(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'nfl-database research'}),timeout=40))
        except Exception as x: err=x; time.sleep(2)
    raise err
out={}
for _,g in G.iterrows():
    k=dt.datetime.fromisoformat(ko[(g.away_team,g.home_team)].replace('Z','+00:00')); la,lo=C[g.stadium]
    d0=(k-dt.timedelta(days=2)).date(); d1=(k+dt.timedelta(hours=4)).date()
    rec=dict(game=f"{g.away_team}@{g.home_team}",game_id=g.game_id,stadium=g.stadium,roof=g.roof,lat=la,lon=lo,kickoff_utc=k.isoformat())
    for lab,base,extra in (('kickoff','https://historical-forecast-api.open-meteo.com/v1/forecast',''),('day_before','https://previous-runs-api.open-meteo.com/v1/forecast','')):
        hv=H if lab=='kickoff' else 'precipitation_probability_previous_day1,wind_speed_10m_previous_day1,wind_gusts_10m_previous_day1'
        u=f"{base}?latitude={la}&longitude={lo}&hourly={hv}&wind_speed_unit=mph&timezone=UTC&start_date={d0}&end_date={d1}"
        try: h=get(u)['hourly']
        except Exception as x: rec[lab]=dict(status='MISSING',err=type(x).__name__,url=u); continue
        idx=[i for i,t in enumerate(h['time']) if k.replace(tzinfo=None)<=dt.datetime.fromisoformat(t)<k.replace(tzinfo=None)+dt.timedelta(hours=3,minutes=30)]
        mx=lambda key:max([h[key][i] for i in idx if h[key][i] is not None],default=None)
        ks=[x for x in h if x!='time']; pk=[x for x in ks if x.startswith('precipitation_probability')][0]; wk_=[x for x in ks if x.startswith('wind_speed')][0]; gk=[x for x in ks if x.startswith('wind_gusts')][0]
        rec[lab]=dict(status='OK',precip_pct=mx(pk),wind_mph=mx(wk_),gust_mph=mx(gk),hours=len(idx),url=u)
    out[rec['game']]=rec; print(rec['game'],g.roof,rec['kickoff'].get('wind_mph'),rec['kickoff'].get('gust_mph'),rec['kickoff'].get('precip_pct'),'| d-1',rec['day_before'].get('wind_mph'),rec['day_before'].get('precip_pct'),flush=True)
json.dump(out,open('weather_wk6_8.json','w'),indent=1)
