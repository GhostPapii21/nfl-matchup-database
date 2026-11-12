"""r6 targeted single-event pull (Rico go via Ghost6 2026-11-04 14:59 ET). Key from env, never printed."""
import os,json,csv,urllib.request,datetime as dt
EV='c75744790b7acf6260c78ba5e739c0e5'
MK=['player_reception_yds','player_reception_yds_alternate','player_receptions','player_receptions_alternate','player_rush_yds','player_rush_yds_alternate','player_pass_interceptions','team_totals','spreads_h1','h2h_h1','spreads_q1','h2h_q1']
u=f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{EV}/odds?apiKey={os.environ['ODDS_API_KEY']}&bookmakers=fanduel,draftkings,pinnacle&markets={','.join(MK)}&oddsFormat=american"
r=urllib.request.urlopen(u,timeout=60); js=json.load(r); h={k:r.headers.get(k) for k in ['x-requests-used','x-requests-remaining','x-requests-last']}
now=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
json.dump(dict(pulled_utc=now,event=EV,markets=MK,headers=h),open('odds/odds_r6_meta.json','w'),indent=1)
with open('odds/odds_r6.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['book','market','player','side','point','price','last_update_utc','pulled_utc'])
    for b in js.get('bookmakers',[]):
        for m in b['markets']:
            for o in m['outcomes']:
                pl=o.get('description',''); w.writerow([b['key'],m['key'],pl if pl else ('' if m['key'] not in('team_totals',) else o.get('description','')),o['name'],o.get('point',''),o['price'],m.get('last_update',''),now])
print(h)
