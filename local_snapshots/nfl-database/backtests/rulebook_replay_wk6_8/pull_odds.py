"""Odds API historical pulls for the rulebook replay (key from env, never printed). Hard stop: 3,000 credits used or <6,000 remaining."""
import os,json,requests,datetime as dt,sys,collections
K=os.environ['ODDS_API_KEY']; B='https://api.the-odds-api.com/v4/historical/sports/americanfootball_nfl'
EV=json.load(open('../current_rules_wk6_8/raw/events.json'))
LO,HI=dt.datetime(2026,10,15,tzinfo=dt.timezone.utc),dt.datetime(2026,11,3,6,tzinfo=dt.timezone.utc)
ev=[e for e in EV.values() if LO<=dt.datetime.fromisoformat(e['commence_time'].replace('Z','+00:00'))<=HI]
used=0; log=open('raw/credits.log','a')
def get(url,params,tag):
    global used
    r=requests.get(url,params={**params,'apiKey':K},timeout=60)
    c=int(r.headers.get('x-requests-last') or 0); rem=int(r.headers.get('x-requests-remaining') or 0); used+=c
    log.write(f"{tag} status={r.status_code} cost={c} remaining={rem} total_used_this_run={used}\n"); log.flush(); print(tag,r.status_code,c,rem,used,flush=True)
    if used>=3000 or rem<6000: print('BUDGET STOP'); sys.exit(0)
    return r
snap=lambda ct:(dt.datetime.fromisoformat(ct.replace('Z','+00:00'))-dt.timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
# 1 game lines: one featured call per distinct kickoff snapshot
for ct in sorted({e['commence_time'] for e in ev}):
    f=f"raw/game_{ct.replace(':','')}.json"
    if os.path.exists(f): continue
    r=get(B+'/odds',{'date':snap(ct),'regions':'us','markets':'h2h,spreads,totals','oddsFormat':'american'},f'game {ct}')
    if r.status_code==200: json.dump(r.json(),open(f,'w'))
# 2 CHI@SEA main props
for e in ev:
    if e['commence_time'].startswith('2026-11-03'):
        f=f"raw/props_{e['id']}.json"
        if not os.path.exists(f):
            r=get(f"{B}/events/{e['id']}/odds",{'date':snap(e['commence_time']),'regions':'us','markets':'player_reception_yds,player_receptions,player_rush_yds,player_pass_yds','oddsFormat':'american'},'mnf props')
            if r.status_code==200: json.dump(r.json(),open(f,'w'))
# 3 alt player lines every event
AM='player_reception_yds_alternate,player_receptions_alternate,player_rush_yds_alternate,player_pass_yds_alternate'
for e in sorted(ev,key=lambda e:e['commence_time']):
    f=f"raw/alt_{e['id']}.json"
    if os.path.exists(f): continue
    r=get(f"{B}/events/{e['id']}/odds",{'date':snap(e['commence_time']),'regions':'us','markets':AM,'oddsFormat':'american'},f"alt {e['away_team']}@{e['home_team']}")
    if r.status_code==200: json.dump(r.json(),open(f,'w'))
print('DONE used',used)
