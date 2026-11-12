"""Single-event TNF JAX@BAL pre-kick pull (lean budget: 1 event x <=9 markets x 1 region unit; FD/DK/Pinnacle).
Key from env ODDS_API_KEY, never printed. Usage: python3 pull_odds_tnf.py <tag>. Writes odds_<tag>.csv + odds_<tag>_meta.json and
appends to quota_log.csv. Read-only: never places bets. Pre-kick check: drops rows if now >= kickoff (SRC-4)."""
import os, sys, json, csv, urllib.request, datetime as dt
sys.path.insert(0, '/workspace/nfl-database/tools'); import odds_quota as Q
EV = 'c75744790b7acf6260c78ba5e739c0e5'; KO_UTC = dt.datetime(2026, 11, 6, 1, 15, tzinfo=dt.timezone.utc)
MK = ['player_rush_yds','player_rush_yds_alternate','player_reception_yds','player_reception_yds_alternate','player_receptions',
      'spreads','totals','team_totals','spreads_h1']
BK = 'fanduel,draftkings,pinnacle'; tag = sys.argv[1]
now = dt.datetime.now(dt.timezone.utc)
if now >= KO_UTC: sys.exit('kickoff passed: in-play rows are never priced (SRC-4)')
est = Q.plan_cost(1, MK, bookmakers=BK)['estimate']; print('estimate', est)
u = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{EV}/odds?apiKey={os.environ['ODDS_API_KEY']}&bookmakers={BK}&markets={','.join(MK)}&oddsFormat=american"
r = urllib.request.urlopen(u, timeout=60); js = json.load(r)
h = {k: r.headers.get(k) for k in ['x-requests-used','x-requests-remaining','x-requests-last']}
et = (now - dt.timedelta(hours=5)).strftime('%Y-%m-%dT%H:%M')
json.dump(dict(pulled_utc=now.strftime('%Y-%m-%dT%H:%M:%SZ'), pulled_et=et, event=EV, commence=js.get('commence_time'), markets=MK, books=BK, estimate=est, headers=h,
               season=2026, data_week=9), open(f'odds_{tag}_meta.json','w'), indent=1)
with open(f'odds_{tag}.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['book','market','player','side','point','price','last_update_utc','pulled_et'])
    for b in js.get('bookmakers', []):
        for m in b['markets']:
            for o in m['outcomes']:
                w.writerow([b['key'], m['key'], o.get('description',''), o['name'], o.get('point',''), o['price'], m.get('last_update',''), et])
Q.log_headers('quota_log.csv', 'tnf_jaxbal_run', 'event-odds', h, label=tag, estimate=est)
print(h, 'rows written')
