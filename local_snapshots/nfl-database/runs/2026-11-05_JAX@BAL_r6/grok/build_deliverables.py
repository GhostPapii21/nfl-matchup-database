import json,re,csv,os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
ROOT=Path('/workspace/nfl-database');R=ROOT/'runs/2026-11-05_JAX@BAL_r6';D=R/'grok';F=R/'film'
# Rebuilding saved evidence is not a fresh injury/news acquisition.
now=json.loads((D/'injury_refresh.json').read_text())['pulled_et'];stamp=now.replace('T',' ')
def file_stamp(path):return datetime.fromtimestamp(Path(path).stat().st_mtime,ZoneInfo('America/New_York')).strftime('%Y-%m-%dT%H:%M')
def dump(n,j): (D/n).write_text(json.dumps(j,indent=2)+'\n')
def src(p):return str(ROOT/p)
pbp='runs/2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet';p=pd.read_parquet(ROOT/pbp);p=p[(p.season_type=='REG')&(p.game_date<'2026-11-05')]
j=p[(p.posteam=='JAX')&(p.two_point_attempt!=1)&(p.pass_attempt==1)&p.receiver_player_name.notna()]
weeks=sorted(j[j.passer_player_name=='T.Lawrence'].week.unique())[-3:]; l3=j[j.week.isin(weeks)]
counts=j.receiver_player_name.value_counts(); c3=l3.receiver_player_name.value_counts()
names={'P.Washington':'Parker Washington','B.Strange':'Brenton Strange','J.Meyers':'Jakobi Meyers','Bri.Thomas':'Brian Thomas Jr.','B.Tuten':'Bhayshul Tuten','J.Cameron':'Jalen Cameron','N.Boerkircher':'Nate Boerkircher','T.Hunter':'Travis Hunter','L.Allen':'LeQuint Allen','C.Rodriguez':'Chris Rodriguez','A.Abdullah':'Ameer Abdullah','Q.Morris':'Quintin Morris','T.Koziol':'Tanner Koziol'}
players=[]
for n,c in counts.items():
 s=c/len(j);s3=int(c3.get(n,0))/len(l3);q=dict(name=n,team='JAX',targets=int(c),team_targets=len(j),share_season=s,share_l3_current_qb=s3,targets_l3=int(c3.get(n,0)),team_targets_l3=len(l3),qb_weeks=[int(x) for x in weeks],qualifies=max(s,s3)>=.22)
 if n=='P.Washington':q['leg']='Washington rec yds o63.5';q['skip_reason']='If this leg is absent from slip B: omitted by user-defined slip B; do not substitute another market.'
 elif n=='B.Strange':q['leg']='Strange 4+ rec (o3.5)';q['skip_reason']='Below 22% in both windows; receiving legs evaluated separately (slip C uses Strange 40+).'
 else:q['skip_reason']='Below 22% in both season and last-three current-QB-week windows; no requested leg.'
 players.append(q)
dump('target_share_pool.json',dict(source='nflverse pbp: '+src(pbp),pulled_et=file_stamp(ROOT/pbp),threshold=.22,team='JAX',current_qb='T.Lawrence',season=2026,data_week=8,method='Named-target pass plays, REG, exclude two-point attempts. Last-three weeks with Lawrence includes all JAX targets in those weeks, matching rico4_rules.target_share_pool.',players=players))
# Save exact official injury table cells and public-news extracts, not inferred statuses.
from bs4 import BeautifulSoup
inj={}
for key in ['jax_injury','bal_injury']:
 soup=BeautifulSoup((D/(key+'.html')).read_text(),'html.parser');inj[key]=[[c.get_text(' ',strip=True) for c in tr.find_all(['th','td'])] for tr in soup.select('table tr')]
dump('injury_refresh.json',dict(pulled_et=now,season=2026,data_week=9,tables=inj,notes=['Both official pages show three practice columns; UNSPECIFIED is preserved verbatim, not converted to active.','Austin Johnson is a practice-squad DT per saved Nov 3 Jaguars news article, not Antonio Johnson (S, ankle). No Austin Johnson injury designation found in official table.','Final active/inactive check remains outstanding.']))
# Film records use verified yt-dlp metadata only; caption excerpts are retrieval evidence, not full-film analysis.
entries=[];lines=['# Verified public film index',f'Pulled {stamp} ET. Official NFL channel ID checked against yt-dlp metadata. Downloads selected with bv*[height<=720]+ba/b[height<=720].','Auto-captions can misspell names. Excerpts below are caption evidence; no invented play timestamps or coverage assignments.']
roles={'3xMS3qL2KwY':'Fagnano relief vs BUF; BAL defense vs slot/TE (Shakir/Kincaid).','rxtoNOhAf4o':'Fagnano preseason TD to Lajohntay Wester; title establishes play.','WtEBwfTGkyI':'Fagnano preseason TD to JaKobi Lane; title establishes play.','R7zUguz0Aag':'Recent JAX passing, Strange/Washington; first-half game script.','LJRRMbR4BrE':'BAL defense vs Bengals TE/slot; Henry first-half usage.'}
for ident,role in roles.items():
 mp=F/(ident+'.info.json')
 if not mp.exists():continue
 m=json.loads(mp.read_text());assert m['channel_id']=='UCDVYQ4Zhbm3S2dlz7P1GBDg'
 subs=F/(ident+'.en.vtt'); excerpts=[];t=''
 if subs.exists():
  seen=set()
  for line in subs.read_text().splitlines():
   if '-->' in line:t=line.split(' -->')[0]
   elif re.search(r'Fagnano|Strange|Washington|Gesicki|Kincaid|Shakir|Henry|Wester|Lane',line,re.I):
    clean=re.sub('<[^>]+>','',line).strip()
    if clean not in seen:excerpts.append(dict(timestamp=t,text=clean));seen.add(clean)
 fm=F/(ident+'.mp4');e=dict(url=m['webpage_url'],title=m['title'],channel=m['channel'],channel_id=m['channel_id'],date=m['upload_date'],relevance=role,description=m.get('description'),caption_excerpts=excerpts,local_file=str(fm),downloaded=fm.exists(),bytes=fm.stat().st_size if fm.exists() else None,height=m.get('height'))
 entries.append(e);lines += ['',f"## {m['title']}",f"- URL: {m['webpage_url']}",f"- Channel: {m['channel']} ({m['channel_id']}); upload date {m['upload_date']}",f'- Target: {role}',f"- Local: {fm}; downloaded={fm.exists()}; metadata height={m.get('height')}"]
 for ex in excerpts:lines.append(f"- Auto-caption {ex['timestamp']}: {ex['text']}")
 if not excerpts:lines.append('- Relevant play supported by title only; description is generic NFL boilerplate. No extra play claims.')
film_complete=len(entries)>=3 and all(e['downloaded'] for e in entries)
lines+=['','## Limits','Highlights omit unsuccessful snaps and do not establish alignment, man/zone or shell rates. First-half sequencing comes from pbp and miss_audit_1H.md. No private API or NFL Pro used.']
(D/'film_index.md').write_text('\n'.join(lines)+'\n');dump('film_verified.json',entries)
# Full-game drive estimates cannot be silently rebranded as a 1H probability.
audit='runs/2026-11-05_JAX@BAL_r6/miss_audit_1H.md'; drive='week10/fagnano/drive_sim.txt'
n3=dict(leg='JAX 1H -6.5',pulled_et=now,status='MISSING',missing=['No joint JAX/BAL first-half drive scoring model in drive_sim.py; no supported probability for -6.5.','Final inactives and turnover/red-zone execution remain unknown.'],sources=[src(drive),src('week10/fagnano/drive_sim.py'),src(audit),src('runs/2026-11-05_JAX@BAL_r5/read_addendum_2026-11-04.md')],script_read=dict(expected_winner='JAX',period='1H',source=src(audit),pulled_et=now,reason='Sourced qualitative early-control thesis; not a quantitative cover probability'),historical_1h_margins=[24,7,11,10,-7,-3,28],historical_cover_count=5,historical_games=7,last4_margins=[10,-7,-3,28],last4_covers=2,probability=None,full_game_estimates={'base':{'BAL_drives':10.5,'BAL_points':16.0,'three_and_out':4.4,'turnovers':1.47},'rico':{'BAL_drives':11.0,'BAL_points':13.5,'three_and_out':5.5,'turnovers':1.87},'flip':{'BAL_drives':10.5,'BAL_points':20.0,'three_and_out':3.5,'turnovers':1.16}},script={'base':'JAX pressure/sacks produce BAL stalled drives and field-position chances; JAX must convert those into a halftime lead of at least seven. Receiver volume can concentrate early, then shrink in a run-out second half.','failure_paths':['JAX red-zone turnover or turnover on downs (both historical misses).','BAL defense stalls Lawrence and Henry sustains long drives, reducing first-half possessions.','Explosive or late-half BAL score; Fagnano one-game sample does not rule it out.'],'correlation':'JAX 1H and JAX receiving overs need early scoring drives together. Henry 40+ can coexist through early volume but a severe run-out limits BAL carries.'},cautions=['drive_sim.py labels ESTIMATES throughout; N=100000 seed=9 is full-game BAL simulation only.','Blitz alone is not the edge: local Fagnano split is better blitzed (5.2 YPA) than unblitzed (3.1); pressure/sack angle is a small-sample proxy.','Historical 2/4 is a flag against the script, not an automatic read cut.'])
dump('n3_1h_script.json',n3)
(D/'n3_1h_script.md').write_text('# N3: JAX 1H -6.5\n\n'+n3['script']['base']+'\n\nHistorical margins: '+str(n3['historical_1h_margins'])+'; 5/7 cover, last four 2/4. These are descriptive frequencies, not a priced probability.\n\n'+ '\n'.join('- '+x for x in n3['script']['failure_paths'])+'\n\nFull-game BAL estimates from drive_sim.txt: base 10.5 drives / 16.0 points; rico 11.0 / 13.5; flip 10.5 / 20.0. Do not divide by two or infer a first-half cover probability.\n\nStatus MISSING for a quantitative first-half model. '+n3['script']['correlation']+'\n\nSources:\n'+'\n'.join('- '+x for x in n3['sources'])+'\n')
# Categories retain truthful original feed times; inspection timestamp is separate.
sources=[]
def source(cat,name,path,time,**extra):sources.append(dict(category=cat,name=name,url_or_file=path,pulled_et=time,tool='local verified evidence' if not path.startswith('http') else 'urllib public HTTP',season=2026,data_week=8,**extra))
source('coverage_matchups','PFR BAL defender extraction (shell/man-zone missing)',src('week10/bal_secondary/pfr_bal_defense_advanced.csv'),'2026-11-04T07:05')
source('coverage_matchups','nflverse pbp position/area allowed; location is not alignment',src('week10/brainstorm_layers/L6_bal_allowed_by_pos_area.csv'),'2026-11-04T05:30')
source('ngs','Existing NGS route screenshots; numeric separation/cushion/RYOE missing',src('week10/ngs'),now,status='MISSING',note='Inspected existing screenshots; original retrieval timestamp/provenance not established. Not a fresh NGS statistics pull.')
source('film','Official NFL YouTube: metadata, auto-captions and actual <=720p files',str(D/'film_verified.json'),now,**({} if film_complete else {'status':'MISSING','note':'Local film downloads absent; metadata alone is not downloaded film'}))
for name,url in [('Jaguars official injury report','https://www.jaguars.com/team/injury-report/'),('Ravens official injury report','https://www.baltimoreravens.com/team/injury-report/'),('Jaguars Austin Johnson practice-squad news','https://www.jaguars.com/news/responding-to-change-important-just-to-stay-ready')]:source('injuries_news',name,url,now)
source('weather','NWS hourly + Open-Meteo via tools/weather_forecast.py',str(D/'weather_forecast.json'),json.loads((D/'weather_forecast.json').read_text())['pulled_et'])
source('target_share_pool','nflverse JAX target pool',str(D/'target_share_pool.json'),file_stamp(ROOT/pbp))
dump('sources.json',sources)
# Checklist: evaluate supplied read honestly. FAIL means check disagrees, never instructs assembler to cut.
legs=['Strange 4+ rec (o3.5)','Strange 40+ rec yds (o39.5)','Washington rec yds o63.5','JAX 1H -6.5','Henry 40+ rush (o39.5)']
C={n:{} for n in legs}
def row(n,ph,status,number,path,t=now):C[n][str(ph)]=dict(status=status,number=number,source=src(path) if not path.startswith('/') and not path.startswith('http') else path,pulled_et=t.replace('T',' '))
for n in legs:
 is_s=n.startswith('Strange');is_w=n.startswith('Washington');is_h=n.startswith('Henry');is_g=n.startswith('JAX');who='B.Strange' if is_s else 'P.Washington' if is_w else 'D.Henry'
 z=p[(p.receiver_player_name==who)] if not (is_h or is_g) else p[(p.rusher_player_name==who)&(p.rush_attempt==1)] if is_h else p[p.posteam=='JAX']
 row(n,1,'PASS',f'{z.game_id.nunique()} REG games in pbp; Fagnano opponent inference is only one relief game' if is_g or is_h else f'{z.game_id.nunique()} REG games in pbp',pbp,'2026-11-03T19:13')
 if is_s or is_w:
  g=j[j.receiver_player_name==who].groupby(['week','game_id']).size().tail(4);tt=g.tolist();line='5+ targets in >=3/4' if n==legs[0] else '4+ targets each last three'
  ok=sum(x>=5 for x in tt)>=3 if n==legs[0] else all(x>=4 for x in tt[-3:])
  row(n,2,'PASS' if ok else 'FAIL',f'last4 targets {tt}; {line}; historical volume flag, not a read cut',pbp,'2026-11-03T19:13')
 elif is_h:
  extra=json.loads((R/'codex/legs_extra.json').read_text())[n]['carry_share'];row(n,2,'PASS',f"RB-only carry share {extra['numerator']}/{extra['denominator']}={extra['value']:.6f}; current QB {extra['current_qb']}, {len(extra['games'])} game(s); QB carries excluded",str(R/'codex/legs_extra.json'),extra['pulled_et'])
 else:row(n,2,'MISSING','No sourced first-half possession/opportunity projection; full-game BAL drive estimates are not 1H opportunities','week10/fagnano/drive_sim.py')
 if is_s:row(n,3,'PASS','Right-side TE fit supported; BAL TE right short/intermediate 16 targets/171 yards per addendum 4. Not a deep seam thesis.','runs/2026-11-05_JAX@BAL_r5/read_addendum4_2026-11-04.md','2026-11-04T05:30')
 elif is_w:row(n,3,'PASS','Outside/left target role supported; pass_location is ball location, not verified alignment','runs/2026-11-05_JAX@BAL_r5/read_addendum2_2026-11-04.md','2026-11-04T05:20')
 elif is_h:row(n,3,'FAIL','JAX RB run defense 3.28 YPC / 123 carries opposes rush over; original read was Henry UNDER. Flag only.','runs/2026-11-05_JAX@BAL_r2/brainstorm_read.md','2026-11-03T19:20')
 else:row(n,3,'PASS','Pressure/sack thesis supports JAX control; blitz-only claim refuted by Fagnano splits','runs/2026-11-05_JAX@BAL_r5/read_addendum_2026-11-04.md','2026-11-04T05:20')
 row(n,4,'MISSING' if not is_h else 'N/A','Defender table available but man/zone and MOFO/MOFC unavailable; mapping is conditional on injuries' if not is_h else 'Pure rushing leg: receiving defender mapping not applicable','week10/bal_secondary/defender_table.csv','2026-11-04T07:05')
 if is_s or is_w:row(n,5,'PASS','BAL defense 300 charted dropbacks, blitz .33, qbhit-or-sack .17 PROXY. Lawrence pressured proxy: 56 DB, sack rate .232; target counts recorded in L2. Real time-to-throw remains missing.','week10/brainstorm_layers/L2_bal_pressure.csv','2026-11-04T05:30')
 else:row(n,5,'PASS','JAX blitz 30.4%, pressure 21.5% PROXY. Fagnano 3 sacks / 24 DB; 3 / 9 pressured proxy. Small sample.','runs/2026-11-05_JAX@BAL_r2/brainstorm_read.md','2026-11-03T19:20')
 row(n,6,'PASS' if is_s or is_w else 'MISSING','Lawrence 210 DB, 66% completions, 8.58 YPA; pressure proxy risk documented' if is_s or is_w else 'Fagnano confirmed starter, but only one relief game; no three-game current-QB baseline. Run/script thesis remains a hypothesis.','week10/brainstorm_layers/L2_lawrence_splits.csv' if is_s or is_w else 'runs/2026-11-05_JAX@BAL_r5/read_addendum_2026-11-04.md','2026-11-04T05:30')
 row(n,8,'PASS','Official refresh: Hawkins OUT; Wiggins QUESTIONABLE; Fagnano FP; Jackson/Huntley OUT; Jenkins/Rosengarten/Simpson FP, no designation. Tuten QUESTIONABLE DNP; Meyers LP UNSPECIFIED. Austin Johnson practice squad, no injury designation found. Final inactives pending.',str(D/'injury_refresh.json'))
 row(n,9,'MISSING','Route screenshots exist for Strange/Washington/Meyers; no verified numeric NGS separation/cushion/YAC-over-expected or Henry RYOE/box rate, no original screenshot pull timestamp. Pbp proxy cannot substitute.',src('week10/ngs'))
 row(n,10,'MISSING','Five official NFL videos downloaded and metadata/captions verified; no rigorous caption-to-pbp play-ID mapping yet. Retrieval fulfilled, formal phase10 remains incomplete.',str(D/'film_index.md'))
 wx=json.loads((D/'weather_forecast.json').read_text());w=wx['games']['JAX@BAL'];row(n,11,'PASS' if w['status']=='OK' and not w['flag'] else 'MISSING',f"Build forecast: precip {w['precip_pct']}%, gust {w['gust_mph']} mph, wind {w['wind_mph']} mph; flag={w['flag']}. Pre-kick refresh pending.",str(D/'weather_forecast.json'),wx['pulled_et'])
 row(n,12,'MISSING','Source audit incomplete: NGS numeric data, shell rates, final inactives and full quantitative 1H model absent. Odds 14:59 ET preserved; no new API call.',str(D/'sources.json'))
 if is_g:row(n,13,'PASS','JAX early-control thesis; 5/7 historical covers, last4 2/4 is a contrary flag. No invented cover probability.',str(D/'n3_1h_script.json'))
 elif is_h:row(n,13,'FAIL','Henry over conflicts with original trailing/run-volume read; low rung may coexist through early carries. Game-script disagreement flagged, not a cut.','runs/2026-11-05_JAX@BAL_r2/brainstorm_read.md','2026-11-03T19:20')
 else:row(n,13,'PASS' if is_s else 'FAIL','Strange volume/right-side case can clear early before run-out; correlation with JAX 1H acknowledged' if is_s else 'Original read avoids JAX WR yardage overs in run-out; remapped outside-WR1 target role argues for volume. Conflict flag only.','runs/2026-11-05_JAX@BAL_r5/read_addendum4_2026-11-04.md','2026-11-04T05:30')
 sims=json.loads((R/'codex/sims.json').read_text());vals=[s['legs'][n] for s in sims];ps=[v['p'] for v in vals];med=[v['median'] for v in vals];nv={legs[0]:(119/219)/(119/219+105/205),legs[2]:(115/215)/(115/215+109/209),legs[3]:(101/201)/(101/201+112/212)}.get(n)
 if nv is None: status='MISSING';detail='two-way no-vig at exact alt rung missing'
 elif is_g:status='MISSING';detail='wrapper flags unverified extension, not native sim_v6 spread_h1; flag against read'
 else:
  line=3.5 if n==legs[0] else 63.5; avg=sum(ps)/len(ps);ok=avg-nv>=.03 and min(ps)>=.45 and all(v>line for v in med);status='PASS' if ok else 'FAIL';detail=f'avg-no_vig={avg-nv:.6f}; stat disagreement is a flag, not a read cut'
 row(n,14,status,f'p={ps}; medians={med}; {detail}',str(R/'codex/sims.json'))
 row(n,15,'MISSING','Pre-kick inactive/price/weather and placed-ticket audit unavailable. Slip B has two Strange stats: correlated same-player exposure; no joint probability supplied. No ticket approval inferred.','runs/2026-11-05_JAX@BAL_r6/briefs/CONTRACT.md')
dump('checklist_rows.json',C)
# Caption/pbp matches supported by unique player outcome and caption wording.
matches=[]
for name,play,ts,why in [('B.Strange',1151,'00:04:53.134','Caption names Strange and says pick up nine; only nine-yard Strange reception in IND@JAX.'),('P.Washington',1711,'00:06:48.615','Only Washington completion in IND@JAX; caption says Lawrence hit on release, pbp includes Latu QB hit.')]:
 z=p[(p.game_id=='2026_08_IND_JAX')&(p.play_id==play)].iloc[0]
 matches.append(dict(player=name,game_id=z.game_id,play_id=play,qtr=int(z.qtr),clock=z.time,yards=float(z.yards_gained),desc=z.desc,video_url='https://www.youtube.com/watch?v=R7zUguz0Aag',video_timestamp=ts,evidence=why,source=src(pbp)))
dump('film_play_matches.json',matches)
with (D/'film_index.md').open('a') as f:
 f.write('\n## Caption-to-pbp matches\n')
 for m in matches:f.write(f"- {m['player']}: {m['video_timestamp']} -> {m['game_id']} play {m['play_id']}, Q{m['qtr']} {m['clock']}, {m['yards']:g} yards. {m['evidence']}\n")
for n in legs[:3]:row(n,10,'PASS' if film_complete else 'MISSING','Official NFL video downloaded, metadata verified; unique caption/pbp match for '+('B.Strange play 1151 (9 yards)' if n.startswith('Strange') else 'P.Washington play 1711 (16 yards, QB hit)')+' in 2026_08_IND_JAX. Highlights do not establish route/shell rates.',str(D/'film_play_matches.json'))
dump('checklist_rows.json',C)
for s in sources:
 if s['category'] in ['injuries_news','weather','target_share_pool']:s['data_week']=9 if s['category']=='injuries_news' else 8
# Keep weather sample current-week label (schedule week 9), not a results-data week.
for s in sources:
 if s['category']=='weather':s['data_week']=9
 if s['category']=='ngs':s['note']+=' Not valid numeric NGS evidence; category remains flagged.'
dump('sources.json',sources)

with (D/'film_index.md').open('a') as f:
 f.write('\n## Fagnano relief context (auto-caption caveat)\nIn the BUF video, 00:05:59.014–00:06:14.965 explicitly introduces the emergency third quarterback, NFL debut, rookie from UConn (auto-caption renders it “Yukon” and misrenders the name). At 00:06:14.975 the caption describes a low incomplete throw; at 00:06:29.335 it names a catch by Lane. These establish the relief sequence without trusting a mis-transcribed name. No claim about a coverage shell follows from this clip.\n')
