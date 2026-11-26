"""Local-only extraction of cached NFL sportsbook observations. No network operations."""
import csv,json,re,hashlib,zipfile,collections
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
OUT=Path(__file__).parent; ET=ZoneInfo('America/New_York')
SCHED=Path('/workspace/nfl-database/backtests/v6_brainstorm_proedge/packs/nflverse_games.csv')
schedule=[r for r in csv.DictReader(SCHED.open()) if r['season']=='2026' and r['game_type']=='REG']
names={'Arizona Cardinals':'ARI','Atlanta Falcons':'ATL','Baltimore Ravens':'BAL','Buffalo Bills':'BUF','Carolina Panthers':'CAR','Chicago Bears':'CHI','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Dallas Cowboys':'DAL','Denver Broncos':'DEN','Detroit Lions':'DET','Green Bay Packers':'GB','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC','Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Los Angeles Rams':'LA','Miami Dolphins':'MIA','Minnesota Vikings':'MIN','New England Patriots':'NE','New Orleans Saints':'NO','New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI','Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF','Seattle Seahawks':'SEA','Tampa Bay Buccaneers':'TB','Tennessee Titans':'TEN','Washington Commanders':'WAS','LAR':'LA','WSH':'WAS','JAC':'JAX'}
def team(s):return names.get(s.strip(),s.strip())
def dt(s,local=False):
 if not s:return None
 try:
  d=datetime.fromisoformat(str(s).replace('Z','+00:00'))
  return d.replace(tzinfo=ET) if d.tzinfo is None and local else (d if d.tzinfo else None)
 except:return None
def iso(s,local=False):
 d=dt(s,local);return d.isoformat() if d else None
def et(s):
 d=dt(s);return d.astimezone(ET).isoformat() if d else None
def game_match(game='',start='',path='',gid=''):
 if gid:
  m=next((r for r in schedule if r['game_id']==gid),None)
  if m:return m
 game=game.split('_2026')[0]
 pp=re.split(r'\s*@\s*',game)
 if len(pp)!=2:
  mm=re.search(r'2026-\d\d-\d\d_([A-Z]{2,3})[@_]([A-Z]{2,3})(?:/|_|$)',path)
  if mm:pp=list(mm.groups())
 if len(pp)!=2:return None
 a,h=map(team,pp)
 cand=[r for r in schedule if r['away_team']==a and r['home_team']==h]
 day=dt(start)
 date=day.astimezone(ET).date().isoformat() if day else None
 if not date:
  mm=re.search(r'2026-\d\d-\d\d',path);date=mm[0] if mm else None
 if date:
  exact=[r for r in cand if r['gameday']==date]
  if len(exact)==1:return exact[0]
 # Do not map an odds event to a different calendar date.
 if date:return None
 return cand[0] if len(cand)==1 else None
def kickoff(r):
 return iso(r['gameday']+'T'+r['gametime'],True) if r.get('gametime') else None
def period(m):
 for s,p in [('_h1','H1'),('_h2','H2'),('_q1','Q1'),('_q2','Q2'),('_q3','Q3'),('_q4','Q4')]:
  if m.endswith(s):return p
 return 'FT'
def fmt(price):
 try:
  p=float(price)
  if abs(p)>=100:return 'american'
  if p>1:return 'decimal'
 except:pass
 return None
rows={}; provenance=[]; sources={}; skipped=collections.Counter(); observations=0
core=['season','week','game_id','event_id','game_date_et','away_team','home_team','bookmaker','platform_type','market','period','player','selection','line','price','odds_format','snapshot_timestamp','book_update_timestamp','market_update_timestamp','event_start_timestamp','snapshot_et','event_start_et','pregame_status','flags','upstream_source']
def add(r,path,pointer):
 global observations
 m=game_match(r.get('game',''),r.get('event_start_timestamp',''),str(path),r.get('game_id',''))
 if not m:skipped['unmapped_game_rows']+=1;return
 if not 1<=int(m['week'])<=9:skipped['outside_weeks1_9_rows']+=1;return
 r.update(season=2026,week=int(m['week']),game_id=m['game_id'],game_date_et=m['gameday'],away_team=m['away_team'],home_team=m['home_team'])
 flags=list(r.get('flags',[]))
 if not r.get('event_start_timestamp'):r['event_start_timestamp']=kickoff(m);flags.append('kickoff_from_saved_schedule')
 b=r.get('bookmaker') or None
 if b:b={'DraftKings':'draftkings','FanDuel':'fanduel','BetMGM':'betmgm','BetRivers':'betrivers','Pinnacle':'pinnacle'}.get(b,b)
 r['bookmaker']=b;r['platform_type']='pickem_or_exchange_not_sportsbook' if b in ['prizepicks','underdog','prophetx','novig','betfair_ex_eu','betfair_ex_uk'] else ('sportsbook' if b else 'unspecified_feed')
 if not r.get('odds_format'):r['odds_format']=fmt(r.get('price'));flags.append('odds_format_inferred_from_numeric_scale')
 start=dt(r.get('event_start_timestamp'));snap=dt(r.get('snapshot_timestamp'));upd=dt(r.get('market_update_timestamp') or r.get('book_update_timestamp'))
 if r.get('historical_feed'):status='retrospective_feed_not_point_in_time'
 elif snap and start:status='verified_capture_before_start' if snap<start else 'capture_at_or_after_start'
 elif upd and start:status='update_before_start_capture_unknown' if upd<start else 'update_at_or_after_start_capture_unknown'
 else:status='unknown'
 r['pregame_status']=status;r['snapshot_et']=et(r.get('snapshot_timestamp'));r['event_start_et']=et(r.get('event_start_timestamp'))
 if upd and snap and upd>snap:flags.append('update_later_than_capture_check_source')
 r['flags']=';'.join(sorted(set(flags)));r['period']=r.get('period') or period(r.get('market',''))
 clean={k:r.get(k) if r.get(k)!='' else None for k in core}
 # Numeric scale harmonization for deduplication; preserve price and line values, no conversions.
 for k in ['line','price']:
  if clean[k] is not None:
   try:clean[k]=float(clean[k])
   except:pass
 key=hashlib.sha256(json.dumps(clean,sort_keys=True).encode()).hexdigest()[:24]
 if key not in rows:rows[key]={'observation_id':key,**clean,'source_filepath':str(path),'source_row_id':pointer,'source_occurrences':0}
 rows[key]['source_occurrences']+=1;provenance.append({'observation_id':key,'source_filepath':str(path),'source_row_id':pointer});observations+=1
 sources.setdefault(str(path),{'source_filepath':str(path),'rows_extracted':0})['rows_extracted']+=1

def walk(x,path,ptr='$',snap=None):
 if isinstance(x,dict):
  snap=x.get('timestamp') or x.get('pulled_utc') or snap
  if isinstance(x.get('bookmakers'),list) and x.get('commence_time'):
   if x.get('sport_key') and x['sport_key']!='americanfootball_nfl':return
   for bi,b in enumerate(x['bookmakers']):
    for mi,m in enumerate(b.get('markets',[])):
     for oi,o in enumerate(m.get('outcomes',[])):
      add({'game':x.get('away_team','')+' @ '+x.get('home_team',''),'event_id':x.get('id'),'bookmaker':b.get('key'),'market':m.get('key'),'player':o.get('description'),'selection':o.get('name'),'line':o.get('point'),'price':o.get('price'),'snapshot_timestamp':iso(snap),'book_update_timestamp':iso(b.get('last_update')),'market_update_timestamp':iso(m.get('last_update')),'event_start_timestamp':iso(x.get('commence_time')),'flags':['cached_source_not_independently_revalidated']},path,f'{ptr}.bookmakers[{bi}].markets[{mi}].outcomes[{oi}]')
   return
  for k,v in x.items():walk(v,path,ptr+'.'+k,snap)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path,f'{ptr}[{i}]',snap)
for item in json.loads((OUT/'discovery.json').read_text()):
 p=Path(item['path']);walk(json.loads(p.read_text()),p)
# CSV observations: avoid filtered model/backtest line selections. Raw sportsbook snapshots only.
for item in json.loads((OUT/'csv_discovery.json').read_text()):
 p=Path(item['path'])
 if 'v7_openai' in str(p):continue
 meta={};mp=p.with_name(p.stem+'_meta.json')
 if mp.exists():
  try:meta=json.loads(mp.read_text())
  except:pass
 snap=iso(meta.get('pulled_utc')) or iso(meta.get('pulled_et'),True)
 for i,r in enumerate(csv.DictReader(p.open()),2):
  if not r.get('price'):continue
  add({'game':r.get('game',''),'game_id':r.get('game_id'),'event_id':r.get('event_id'),'bookmaker':r.get('book'),'market':r.get('market'),'player':r.get('player'),'selection':r.get('side') or r.get('name'),'line':r.get('point'),'price':r.get('price'),'snapshot_timestamp':iso(r.get('pulled_utc')) or iso(r.get('pulled_et'),True) or snap,'book_update_timestamp':iso(r.get('last_update_utc')) or iso(r.get('timestamp')),'event_start_timestamp':iso(r.get('commence_utc')) or iso(r.get('kickoff')),'flags':['cached_source_not_independently_revalidated']+(['source_marks_inplay'] if r.get('inplay','').lower()=='true' else []),'upstream_source':r.get('source')},p,f'csv_line:{i}')
 if str(p) in sources and mp.exists():sources.setdefault(str(mp),{'source_filepath':str(mp),'rows_extracted':0})
# Custom game-line JSON captures preserve explicit pulled_et; no file mtime used.
for p in Path('/workspace/nfl-database/runs/2026-11-01_shared_src').glob('lines*.json'):
 try:d=json.loads(p.read_text())
 except:continue
 if not isinstance(d,dict) or not isinstance(d.get('games'),dict):continue
 for game,books in d['games'].items():
  for book,markets in books.items():
   if not isinstance(markets,dict):continue
   for market,os in markets.items():
    if not isinstance(os,list):continue
    for i,o in enumerate(os):
     add({'game':game,'bookmaker':book,'market':market,'selection':o.get('name'),'line':o.get('point'),'price':o.get('price'),'snapshot_timestamp':iso(d.get('pulled_et'),True),'flags':['transformed_game_line_capture']},p,f'$.games.{game}.{book}.{market}[{i}]')
# Existing Week9 normalized line-watch ledger: available rows only; retain source feed and timing.
p=Path('/workspace/research/nfl_dk_fd_line_watch_2026-11-06/ledger/quotes.jsonl')
if p.exists():
 for i,l in enumerate(p.open(),1):
  r=json.loads(l)
  if r.get('availability')!='available' or r.get('price') is None:skipped['ledger_unavailable_or_missing_price']+=1;continue
  game,date=r['canonicalGameId'].rsplit('_',1)
  # Match exact scheduled date from canonical source; kickoff resolved from schedule.
  m=game_match(game,date+'T12:00:00-05:00')
  if not m:skipped['ledger_unmapped']+=1;continue
  add({'game_id':m['game_id'],'event_id':r.get('eventId'),'bookmaker':r.get('book'),'market':r.get('market'),'period':r.get('period'),'player':r.get('player'),'selection':r.get('side'),'line':r.get('line'),'price':r.get('price'),'snapshot_timestamp':iso(r.get('fetchTime')),'book_update_timestamp':iso(r.get('bookLastUpdate')),'flags':['normalized_existing_line_watch','not_opener_or_closing']+(['upstream_observed_at='+r['statshawkObservedAt']] if r.get('statshawkObservedAt') else []),'upstream_source':r.get('source')},p,f'jsonl_line:{i}')
# Retrospective saved nflverse feed: explicit missing bookmaker/capture time, separate file.
for r in schedule:
 if not 1<=int(r['week'])<=9:continue
 for market,sel,linefield,pricefield in [('h2h',r['home_team'],None,'home_moneyline'),('h2h',r['away_team'],None,'away_moneyline'),('spreads',r['home_team'],'spread_line','home_spread_odds'),('spreads',r['away_team'],'spread_line','away_spread_odds'),('totals','Under','total_line','under_odds'),('totals','Over','total_line','over_odds')]:
  price=r.get(pricefield);line=r.get(linefield) if linefield else None
  if not price and not line:continue
  # nflverse spread_line is home-favorite margin; translate to home handicap and away handicap.
  if line and market=='spreads':line=-float(line) if sel==r['home_team'] else float(line)
  add({'game_id':r['game_id'],'market':market,'selection':sel,'line':line,'price':price,'odds_format':'american' if price else None,'historical_feed':True,'flags':['saved_nflverse_retrospective_feed','bookmaker_and_capture_timestamp_not_available','not_independently_verified_closing'],'upstream_source':'saved nflverse_games.csv'},SCHED,'game_id:'+r['game_id']+'|'+pricefield)

def write(name,rs,fields=None):
 rs=list(rs)
 if fields is None:fields=list(rs[0]) if rs else ['empty']
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rs)
allrows=list(rows.values())
sports=[r for r in allrows if r['platform_type']=='sportsbook']
feeds=[r for r in allrows if r['platform_type']=='unspecified_feed']
other=[r for r in allrows if r['platform_type']=='pickem_or_exchange_not_sportsbook']
write('sportsbook_observations.csv',sports);write('retrospective_game_lines_book_unknown.csv',feeds);write('non_sportsbook_platform_observations.csv',other);write('provenance.csv',provenance)
coverage=collections.defaultdict(lambda: {'observation_rows':0,'games':set(),'verified_capture_before_start':0})
for r in allrows:
 key=(r['week'],r['platform_type'],r['bookmaker'],r['market'],r['period'])
 c=coverage[key];c['observation_rows']+=1;c['games'].add(r['game_id']);c['verified_capture_before_start']+=r['pregame_status']=='verified_capture_before_start'
write('coverage_by_week_book_market.csv',[dict(week=k[0],platform_type=k[1],bookmaker=k[2],market=k[3],period=k[4],observation_rows=v['observation_rows'],distinct_games=len(v['games']),verified_capture_before_start=v['verified_capture_before_start']) for k,v in sorted(coverage.items(),key=lambda x:str(x[0]))])
write('schedule_2026_weeks1_9.csv',[r for r in schedule if int(r['week'])<=9])
# Serialize only identified source data, with structural/URL credential redaction, content dedup.
secretkey=re.compile(r'^(api_?key|access_?token|refresh_?token|authorization|cookie|password|secret|client_secret)$',re.I)
urlsecret=re.compile(r'(?i)([?&](?:api_?key|token|access_token)=)[^&\s"\']+')
def sanitize(x):
 if isinstance(x,dict):return {k:('[REDACTED]' if secretkey.match(k) else sanitize(v)) for k,v in x.items()}
 if isinstance(x,list):return [sanitize(v) for v in x]
 if isinstance(x,str):return urlsecret.sub(r'\1[REDACTED]',x)
 return x
rawdir=OUT/'source_artifacts';rawdir.mkdir(exist_ok=True)
for s in sources.values():
 p=Path(s['source_filepath']);raw=p.read_bytes();s['original_sha256']=hashlib.sha256(raw).hexdigest();s['original_bytes']=len(raw)
 if p==SCHED:packed=(OUT/'schedule_2026_weeks1_9.csv').read_bytes();s['copy_note']='filtered 2026 REG weeks1-9 only'
 elif p.suffix=='.json':packed=json.dumps(sanitize(json.loads(raw)),separators=(',',':')).encode();s['copy_note']='JSON canonicalized; credential-key and credential-query redaction'
 elif p.suffix=='.jsonl':packed=('\n'.join(json.dumps(sanitize(json.loads(l)),separators=(',',':')) for l in raw.decode().splitlines() if l)+'\n').encode();s['copy_note']='JSONL canonicalized; credential redaction'
 else:packed=urlsecret.sub(r'\1[REDACTED]',raw.decode()).encode();s['copy_note']='credential-query redaction'
 h=hashlib.sha256(packed).hexdigest();dest=rawdir/(h[:20]+p.suffix);dest.write_bytes(packed);s['packaged_path']=str(dest.relative_to(OUT));s['packaged_sha256']=h;s['packaged_bytes']=len(packed)
write('source_manifest.csv',sources.values())
summary={'sportsbook_rows':len(sports),'sportsbook_games':len({r['game_id'] for r in sports}),'sportsbook_books':sorted({r['bookmaker'] for r in sports}),'sportsbook_weeks':sorted({r['week'] for r in sports}),'sportsbook_pregame_status_counts':dict(collections.Counter(r['pregame_status'] for r in sports)),'retrospective_feed_rows':len(feeds),'non_sportsbook_rows':len(other),'source_occurrences':observations,'unique_observations_all_types':len(allrows),'source_paths':len(sources),'unique_packaged_source_files':len(list(rawdir.iterdir())),'skipped':dict(skipped),'by_week':{str(w):{'rows':sum(r['week']==w for r in sports),'games':len({r['game_id'] for r in sports if r['week']==w}),'pregame_rows':sum(r['week']==w and r['pregame_status']=='verified_capture_before_start' for r in sports)} for w in range(1,10)}}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
