"""Real pre-kickoff NFL player-prop prices, Weeks 6-8 2026 (Odds API historical). Key from env, never printed."""
import os,json,requests,datetime as dt,pandas as pd,sys
K=os.environ['ODDS_API_KEY']; B='https://api.the-odds-api.com/v4/historical/sports/americanfootball_nfl'
MK='player_reception_yds,player_receptions,player_rush_yds,player_pass_yds'
P=pd.read_parquet('/workspace/nfl-database/runs/2026-11-02_shared_src/play_by_play_2026.parquet',columns=['week','game_id','home_team','away_team','game_date','start_time'])
G=P[P.week.isin([6,7,8])].drop_duplicates('game_id')
os.makedirs('raw',exist_ok=True); log=[]
def get(url,params):
    r=requests.get(url,params={**params,'apiKey':K},timeout=60)
    rem=r.headers.get('x-requests-remaining'); used=r.headers.get('x-requests-last')
    return r,rem,used
# one events list per game date at 11:00 ET-ish snapshot (16:00Z) covers that day's slate
evs={}
for d in sorted(G.game_date.unique()):
    snap=f"{d}T16:00:00Z"
    r,rem,used=get(B+'/events',{'date':snap})
    if r.status_code!=200: print('events',d,r.status_code,r.text[:200]); continue
    for e in r.json()['data']: evs[e['id']]=e
    print('events',d,len(r.json()['data']),'remaining',rem,flush=True)
json.dump(evs,open('raw/events.json','w'))
dates=set(G.game_date)
todo=[e for e in evs.values() if e['commence_time'][:10] in dates or (dt.datetime.fromisoformat(e['commence_time'][:-1])-dt.timedelta(hours=5)).date().isoformat() in dates]
print('events to price',len(todo))
for e in todo:
    ct=dt.datetime.fromisoformat(e['commence_time'].replace('Z','+00:00'))
    if ct>dt.datetime(2026,11,3,tzinfo=dt.timezone.utc) or ct<dt.datetime(2026,10,14,tzinfo=dt.timezone.utc): continue
    f=f"raw/{e['id']}.json"
    if os.path.exists(f): continue
    snap=(ct-dt.timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
    r,rem,used=get(f"{B}/events/{e['id']}/odds",{'date':snap,'regions':'us','markets':MK,'oddsFormat':'american'})
    print(e['away_team'],'@',e['home_team'],snap,r.status_code,'cost',used,'remaining',rem,flush=True)
    if r.status_code==200: json.dump(r.json(),open(f,'w'))
    if rem and int(rem)<7000: print('FLOOR STOP'); sys.exit(0)
