import json, hashlib, os, shutil, pandas as pd, datetime as dt
files=[l.strip()[2:] for l in open('/tmp/oddsfiles.txt')]
games=pd.read_csv('/workspace/research/nfl_week9_usage_2026-11-07/raw/games.csv'); g26=games[games.season==2026]
NM={'Arizona Cardinals':'ARI','Atlanta Falcons':'ATL','Baltimore Ravens':'BAL','Buffalo Bills':'BUF','Carolina Panthers':'CAR','Chicago Bears':'CHI','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Dallas Cowboys':'DAL','Denver Broncos':'DEN','Detroit Lions':'DET','Green Bay Packers':'GB','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC','Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Los Angeles Rams':'LA','Miami Dolphins':'MIA','Minnesota Vikings':'MIN','New England Patriots':'NE','New Orleans Saints':'NO','New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI','Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF','Seattle Seahawks':'SEA','Tampa Bay Buccaneers':'TB','Tennessee Titans':'TEN','Washington Commanders':'WAS'}
seen={}; rows=[]; man=[]
def period(k):
  for s,p in [('_q1','Q1'),('_q2','Q2'),('_q3','Q3'),('_q4','Q4'),('_h1','H1'),('_h2','H2'),('_1st_1_innings','?')]:
    if k.endswith(s): return p
  return 'FULL_GAME'
for f in files:
  path='/workspace/'+f
  try: b=open(path,'rb').read()
  except: continue
  h=hashlib.sha256(b).hexdigest()
  man.append(dict(source_path=path,sha256=h,bytes=len(b),duplicate_of=seen.get(h)))
  if h in seen: continue
  seen[h]=path
  try: d=json.loads(b)
  except Exception as e: man[-1]['parse']='FAIL';continue
  snap=None; evs=d
  if isinstance(d,dict) and 'data' in d: snap=d.get('timestamp'); evs=d['data']
  if isinstance(evs,dict): evs=[evs]
  if not isinstance(evs,list): man[-1]['parse']='NO_EVENTS';continue
  n=0
  for e in evs:
    if not isinstance(e,dict) or e.get('sport_key')!='americanfootball_nfl': continue
    for bk in e.get('bookmakers',[]):
      for m in bk.get('markets',[]):
        for o in m.get('outcomes',[]):
          rows.append(dict(provider='the-odds-api (v4 JSON format)',event_id=e.get('id'),home_team=e.get('home_team'),away_team=e.get('away_team'),commence_time_utc=e.get('commence_time'),book=bk.get('key'),book_title=bk.get('title'),market=m.get('key'),period=period(m.get('key','')),outcome=o.get('name'),player=o.get('description'),line=o.get('point'),price=o.get('price'),price_format='american' if isinstance(o.get('price'),int) or abs(o.get('price') or 0)>=100 else 'decimal?',
            snapshot_ts_utc=snap,book_last_update_utc=bk.get('last_update'),market_last_update_utc=m.get('last_update'),raw_sha256=h,source_path=path)); n+=1
  man[-1]['quote_rows']=n
  if n: shutil.copy(path,f'raw_oddsapi/{h[:16]}_{os.path.basename(path)}')
R=pd.DataFrame(rows); M=pd.DataFrame(man)
R['home']=R.home_team.map(NM); R['away']=R.away_team.map(NM)
ct=pd.to_datetime(R.commence_time_utc,utc=True)
R['kick_date_et']=ct.dt.tz_convert('America/New_York').dt.date.astype(str)
k=g26[['game_id','week','gameday','home_team','away_team','gametime']]
R=R.merge(k,left_on=['home','away','kick_date_et'],right_on=['home_team','away_team','gameday'],how='left',suffixes=('','_sched')).drop(columns=['home_team_sched','away_team_sched'],errors='ignore')
R['season_status']=R.game_id.map(lambda x:'2026_SCHEDULE_MATCH' if isinstance(x,str) else 'NO_2026_MATCH_OUTSIDE_SCOPE')
q=pd.to_datetime(R.market_last_update_utc.fillna(R.book_last_update_utc),utc=True,errors='coerce')
s=pd.to_datetime(R.snapshot_ts_utc,utc=True,errors='coerce')
qt=q.fillna(s)
R['quote_time_basis']=R.market_last_update_utc.notna().map({True:'market_last_update',False:'book_last_update_or_snapshot'})
R['pregame_status']=['UNKNOWN' if pd.isna(a) else ('PREGAME' if a<c else 'AT_OR_AFTER_KICK') for a,c in zip(qt,ct)]
R['in_requested_scope']=R.week.between(1,9)&(R.season_status=='2026_SCHEDULE_MATCH')
R['record_class']='RAW_BOOK_QUOTE'
key=['event_id','book','market','outcome','player','line','price','market_last_update_utc','book_last_update_utc']
R['dup_n']=R.groupby(key,dropna=False).event_id.transform('size')
R=R.sort_values('snapshot_ts_utc').drop_duplicates(key,keep='first')
R.to_csv('ODDS_RAW_QUOTES_NORMALIZED.csv',index=False); M.to_csv('SOURCE_FILE_MANIFEST.csv',index=False)
S=R[R.in_requested_scope]
cov=S.groupby(['week','book','period','market']).agg(quotes=('price','size'),events=('event_id','nunique'),pregame=('pregame_status',lambda x:(x=='PREGAME').sum())).reset_index()
cov.to_csv('COVERAGE_BY_WEEK_BOOK_MARKET_PERIOD.csv',index=False)
print(len(M),M.duplicate_of.isna().sum(),len(R),R.season_status.value_counts().to_dict(),R.pregame_status.value_counts().to_dict())
print(S.groupby('week').agg(ev=('event_id','nunique'),q=('price','size'),books=('book','nunique')).to_string()); print(S.period.value_counts().to_dict()); print(S.market.value_counts().head(30).to_dict())
