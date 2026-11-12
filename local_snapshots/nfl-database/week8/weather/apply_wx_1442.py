"""BUG-2026-11-01-WX: add Phase 11 weather blocks + placed_legs to 4 PM+ manifests; refresh weather sources (and odds b1442 where legs are pregame). Backups *.bak_1442."""
import json,shutil,re,os
R='/workspace/nfl-database/runs/'; W=json.load(open('/workspace/nfl-database/week8/weather/nws_20261101_1440.json'))
T='2026-11-01T14:41'; WF='/workspace/nfl-database/week8/weather/nws_20261101_1440.json'
ROOF={'LAC@LAR':'dome','KC@DEN':'open','NE@MIA':'open','PHI@WSH':'open','LV@NYJ':'open','MIN@DET':'dome'}
def blk(g):
    if ROOF[g]=='dome': return dict(roof='dome',note='SoFi fixed roof / Ford Field (nflverse roof=dome)' ,source='nflverse play_by_play_2026.parquet roof field + '+WF,pulled_et=T)
    w=W[g]; return dict(roof='open',precip_pct=w['precip_pct'],gust_mph=w['gust_mph'],wind_mph=w['wind_mph'],source=w['source'],nws_update_utc=w['update'],pulled_et=T)
PL={'LAC@LAR':["PP $40: Matthew Stafford Pass Completions 22.5","PP $20: Matthew Stafford Pass Completions 22.5","UD $20: Puka Nacua Receiving Yards 69.5","PP $25: Kyren Williams Anytime TD 0.5","PP $20: K. Walker III + K. Williams Anytime TDs combo 1.5","FD7: Kyren Williams or Blake Corum anytime TD","FD 8-leg: Puka 60+ yds"],
 'KC@DEN':["PP $40: Kenneth Walker III Rush Yards 97.5","UD $20: Kenneth Walker III Rush Yards 69.5","PP $20: K. Walker III + K. Williams Anytime TDs combo 1.5","PP $20: Patrick Mahomes Pass Yards 0.5","FD7: Kenneth Walker III anytime TD (being replaced)","Placed 07:54: Kenneth Walker III 80+ rush+rec","FD 8-leg: K. Walker 80+ rush+rec"],
 'NE@MIA':[],'PHI@WSH':[],'LV@NYJ':["PP $40/UD $20/PP $20/FD7/FD8: Brock Bowers legs (Rec Targets 8.5, Rec Yds 49.5, Halves 25+, 50+ yds)"],'MIN@DET':["PP $40: Amon-Ra St. Brown Receptions 5.5","UD: St. Brown Rec Yds 49.5","PP $25: St. Brown Receptions 7"]}
F={'LAC@LAR':['LAC@LAR'],'KC@DEN':['KC@DEN'],'NE@MIA':['NE@MIA'],'PHI@WSH':['PHI@WSH'],'BONUS_SLIP_4PM':['KC@DEN','PHI@WSH'],
   'BONUS_SLIP':['LV@NYJ','LAC@LAR','PHI@WSH','MIN@DET'],'FD7_REPLACEMENTS':['LV@NYJ','LAC@LAR','PHI@WSH'],'DFS_SLIPS':['LAC@LAR']}
PREGAME={'LAC@LAR','KC@DEN','NE@MIA','PHI@WSH','BONUS_SLIP_4PM','DFS_SLIPS'}
for f,gs in F.items():
    p=f'{R}2026-11-01_{f}/run_manifest.json'; shutil.copy(p,p+'.bak_1442'); m=json.load(open(p))
    m['weather']={g:blk(g) for g in gs}
    m['placed_legs']=[dict(game=g,leg=x,source='/workspace/nfl-database/week8/slips/slips_2026-11-01.md') for g in gs for x in PL[g]]
    m['sources']=[s for s in m['sources'] if s['category']!='weather']+[dict(category='weather',name='NWS gridpoint forecast (api.weather.gov) kickoff..+3.5h max PoP/wind/gust; Open-Meteo cross-check DEN/MIA',url_or_file=WF,tool='week8/weather/pull_wx_1440.py',pulled_et=T)]
    if f in PREGAME:
        for s in m['sources']:
            if s['category']=='odds_props':
                s['url_or_file']=re.sub(r'b\d{4}','b1442',s['url_or_file']); s['name']=re.sub(r'b\d{4}','b1442',s['name']); s['pulled_et']='2026-11-01T14:42'
    for l in m['legs']:
        if len(gs)==1: l.setdefault('game',gs[0])
    json.dump(m,open(p,'w'),indent=1,default=float)
    print(f,'ok')
