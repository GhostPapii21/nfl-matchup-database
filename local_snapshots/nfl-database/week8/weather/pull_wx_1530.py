"""NWS gridpoint pull for remaining Nov 1 open-air games. Max over kickoff..+3.5h of PoP, sustained wind, gusts."""
import json,urllib.request,re
from datetime import datetime,timedelta,timezone
UA={'User-Agent':'nfl-database weather check (research)','Accept':'application/geo+json'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
G={'LAC@LAR':(33.9535,-118.3392,'2026-11-01T21:05:00Z'),'KC@DEN':(39.7439,-105.0201,'2026-11-01T21:25:00Z'),
   'NE@MIA':(25.9580,-80.2389,'2026-11-01T21:25:00Z'),'PHI@WSH':(38.9078,-76.8645,'2026-11-02T01:20:00Z')}
def series(vals,t0,t1):
    out=[]
    for v in vals:
        s,d=v['validTime'].split('/'); s=datetime.fromisoformat(s)
        h=int(re.search(r'(\d+)H',d).group(1)) if 'H' in d else 0; days=int(re.search(r'P(\d+)D',d).group(1)) if 'D' in d.split('T')[0] else 0
        e=s+timedelta(hours=h,days=days)
        if e>t0 and s<t1 and v['value'] is not None: out.append(v['value'])
    return out
R={}
for g,(la,lo,ko) in G.items():
    p=get(f'https://api.weather.gov/points/{la},{lo}')['properties']; gp=get(p['forecastGridData'])['properties']
    t0=datetime.fromisoformat(ko.replace('Z','+00:00')); t1=t0+timedelta(hours=3.5)
    pop=series(gp['probabilityOfPrecipitation']['values'],t0,t1); ws=series(gp['windSpeed']['values'],t0,t1); wg=series(gp['windGust']['values'],t0,t1)
    k=0.621371
    R[g]=dict(precip_pct=max(pop) if pop else None,wind_mph=round(max(ws)*k,1) if ws else None,gust_mph=round(max(wg)*k,1) if wg else None,
      source=p['forecastGridData'],update=gp.get('updateTime'),window_utc=[ko,t1.isoformat()])
    print(g,R[g])
json.dump(R,open('nws_20261101_1530.json','w'),indent=1)
