"""Rico-approved one-time pull (Nov 3 6:43 AM ET): main yardage lines only. Key from env, never printed. Stops: >2000 used or next call would drop below 1000."""
import os,json,requests,datetime as dt,pandas as pd,pathlib
K=os.environ['ODDS_API_KEY'];H='https://api.the-odds-api.com/v4'
OUT=pathlib.Path('backtests/yardage_markets_wk3_8/raw');log=open(OUT/'credits.log','a')
def L(s):print(s);log.write(dt.datetime.now().isoformat()+' '+s+'\n');log.flush()
r=requests.get(H+'/sports',params={'apiKey':K});rem=int(r.headers['x-requests-remaining']);start=rem;L(f'START remaining={rem}')
used=0
def get(path,params,tag,est):
    global used,rem
    if used+est>2000 or rem-est<1000: L(f'STOP before {tag}: used={used} rem={rem} est={est}');raise SystemExit
    r=requests.get(H+path,params={**params,'apiKey':K});c=int(r.headers.get('x-requests-last',0));rem=int(r.headers.get('x-requests-remaining',rem));used+=c
    L(f'{tag} status={r.status_code} cost={c} remaining={rem} used={used}');return r.json() if r.ok else None
p=pd.read_parquet('runs/2026-11-02_shared_src/play_by_play_2026.parquet');g=p[p.season_type=='REG'].drop_duplicates('game_id')
snap=lambda ct:(dt.datetime.fromisoformat(ct.replace('Z','+00:00'))-dt.timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
for w in range(3,9):
    dates=sorted(g[g.week==w].game_date.astype(str).unique());ef=OUT/f'events_w{w}.json'
    if ef.exists(): ev=json.load(open(ef))
    else:
        d0=dt.date.fromisoformat(dates[0])-dt.timedelta(days=1)
        j=get('/historical/sports/americanfootball_nfl/events',{'date':f'{d0}T12:00:00Z'},f'events w{w}',1)
        lo,hi=dates[0],(dt.date.fromisoformat(dates[-1])+dt.timedelta(days=1)).isoformat()
        ev=[e for e in j['data'] if lo<=e['commence_time'][:10]<=hi];json.dump(ev,open(ef,'w'))
    mk='player_rush_yds,player_reception_yds,player_rush_reception_yds' if w<=5 else 'player_rush_reception_yds'
    n=mk.count(',')+1
    for e in ev:
        f=OUT/f'w{w}_{e["id"]}.json'
        if f.exists():continue
        j=get(f'/historical/sports/americanfootball_nfl/events/{e["id"]}/odds',{'date':snap(e['commence_time']),'regions':'us','markets':mk,'oddsFormat':'american'},f'w{w} {e["away_team"]}@{e["home_team"]}',10*n)
        if j: json.dump(j,open(f,'w'))
L(f'END start={start} remaining={rem} used={used}')
