import re,glob,os,json,csv,collections,shutil,datetime
import pandas as pd
B='/workspace/nfl-database'; W=B+'/playlogs/2026_wk8'; STAMP='2026-11-01'
NV={'LAR':'LA','WSH':'WAS'}
pl=pd.read_parquet(B+'/runs/2026-11-01_shared_src/players.parquet')
pl=pl[pl.latest_team.notna()]
roster=collections.defaultdict(list)
for r in pl.itertuples():
  if isinstance(r.first_name,str) and isinstance(r.last_name,str): roster[r.latest_team].append((r.first_name,r.last_name,r.position_group,r.position,r.display_name))
BOX=collections.defaultdict(set)
for bf in glob.glob(W+'/*_box.json'):
  bj=json.load(open(bf))
  for tm,cats in bj['teams'].items():
    for k,v in cats.items():
      if isinstance(v,list):
        for r in v:
          if isinstance(r,dict) and r.get('player'): BOX[tm].add(r['player'])
DN={}
for r in pl.itertuples(): DN.setdefault(r.display_name,[]).append((r.first_name,r.last_name,r.position_group,r.position,r.display_name))
def lookup(team,ab):
  r=_lookup(team,ab)
  if r or '.' not in ab: return r
  c=[n for n in BOX[team] if full_match(ab,n)]
  if len(c)==1:
    d=DN.get(c[0]) or DN.get(c[0].replace(' Jr.','').replace(' II','').replace(' III',''))
    if d: return d[0]
  return None
def _lookup(team,ab):
  t=NV.get(team,team)
  if '.' not in ab: return None
  f,l=ab.split('.',1); l=l.strip()
  c=[x for x in roster[t] if x[1].replace(' ','').replace('.','').lower().startswith(l.replace('.','').lower()) and x[0].lower().startswith(f.lower())]
  if not c: c=[x for x in roster[t] if x[1].lower()==l.lower()]
  return c[0] if len(c)==1 else (c[0] if c and len({x[2] for x in c})==1 else None)
cov=json.load(open(B+'/week8/breakdown/coverage/coverage.json'))
mt={}
for g in cov['games']:
  for s in g['sides']:
    for m in s.get('matchups',[]): mt[(s['defense'],m['receiver'])]=m
def full_match(ab,full):
  f,l=ab.split('.',1); p=full.replace(' Jr.','').replace(' Sr.','').split(); return len(p)>1 and p[-1].lower().startswith(l.lower()) and p[0].lower().startswith(f.lower())
TEND={}
for f in glob.glob(B+'/week8/defense/*_at_*.md'):
  cur=None
  for ln in open(f):
    m=re.match(r'## (\w+) DEFENSE',ln)
    if m: cur=m.group(1)
    m=re.search(r'Man / Zone / MOFC / MOFO % \| ([\d./ ]+)\|',ln)
    if m and cur: TEND[cur]=m.group(1).strip()
games=[os.path.basename(p)[:-9] for p in sorted(glob.glob(W+'/*_box.json')) if os.path.exists(p.replace('_box.json','_plays.md'))]
plays=[]
for g in games:
  a,h=g.split('_'); key=f'{a}@{h}'; off=None
  for ln in open(f'{W}/{g}_plays.md'):
    m=re.match(r'## Drive: (\w+)',ln)
    if m: off=m.group(1); continue
    m=re.match(r'- (Q\d \d+:\d+) \[([^\]]*)\] (.*)',ln)
    if not m or not off: continue
    typ=m.group(2); t=m.group(3).split(' (score')[0]; d=h if off==a else a
    if 'No Play' in t or 'Kick' in typ or 'Punt' in typ or 'Field Goal' in typ or 'Interception Return' in typ: 
      if 'Interception Return' not in typ: continue
    rec=re.search(r'pass (\w+) (\w+) to ([A-Z][a-z]?\.[A-Za-z\'\-]+)[^.]*? for (-?\d+) yards',t)
    inc=re.search(r'pass incomplete (\w+) (\w+) to ([A-Z][a-z]?\.[A-Za-z\'\-]+)',t)
    rus=re.search(r'^(?:\([^)]*\) )*(?:[A-Z]\.[A-Za-z\-]+ reported in as eligible\.\s+)?([A-Z][a-z]?\.[A-Za-z\'\-]+) (?:up the middle|left \w+|right \w+|scrambles[^.]*|to )[^.]*? for (-?\d+) yards',t)
    intc=re.search(r'intended for ([A-Z][a-z]?\.[A-Za-z\'\-]+) INTERCEPTED by ([A-Z][a-z]?\.[A-Za-z\'\-]+)',t)
    pen=[x for x in re.findall(r'(?:PENALTY|Penalty) on '+d+r'-([A-Z][a-z]?\.[A-Za-z\'\-]+), (Defensive Pass Interference|Defensive Holding|Illegal Contact)',t)]
    paren=re.findall(r'\(([^()]*)\)',t); tk=[x.strip() for x in (paren[-1].split(';') if paren and re.match(r'^[A-Z][a-z]?\.',paren[-1]) else [])]
    base=dict(game=key,off=off,defn=d,when=m.group(1),text=t,pen=pen,tk=tk)
    if intc: plays.append(dict(base,kind='int',tgt=intc.group(1),dfr=intc.group(2),depth='',loc='',yds=0)); continue
    if rec and 'pass' in t and 'incomplete' not in t: plays.append(dict(base,kind='rec',depth=rec.group(1),loc=rec.group(2),tgt=rec.group(3),yds=int(rec.group(4))))
    elif inc: plays.append(dict(base,kind='inc',depth=inc.group(1),loc=inc.group(2),tgt=inc.group(3),yds=0))
    elif rus and 'pass' not in t and 'Rush' in typ: plays.append(dict(base,kind='rush',tgt=rus.group(1),yds=int(rus.group(2)),depth='',loc=''))
# enrich
for p in plays:
  r=lookup(p['off'],p['tgt']); p['pos']=r[2] if r else ('?')
  p['fullname']=r[4] if r else p['tgt']
  if p['kind']=='inc' and p['tk']: p['pbu']=p['tk'][0]
  # alignment
  al='?'
  if p['pos']=='RB': al='backfield (position default)'
  elif p['pos']=='TE': al='TE: inline/slot not charted (no public alignment)'
  elif p['pos']=='WR':
    for (d,rn),mm in mt.items():
      if d==p['defn'] and full_match(p['tgt'],rn):
        al=f"{mm.get('inferred_alignment')} (pregame target-side proxy; ESPN season split {mm.get('espn',{}).get('alignment','?')})"; p['mm']=mm
    if al=='?': al=f"{'middle' if p['loc']=='middle' else 'outside'} (this-play pass_location proxy)" if p['loc'] else '?'
  p['align']=al
  # defender attribution
  dfr,conf,src='','unknown',''
  if p['pen']: dfr=p['pen'][0][0]; conf='confirmed'; src='ESPN play text: '+p['pen'][0][1]+' on play (single-source)'
  elif p['kind']=='int': dfr=p['dfr']; conf='confirmed (INT)'; src='ESPN play text (single-source)'
  elif p['kind']=='rush':
    if p['tk']: dfr='; '.join(p['tk']); conf='tackler-of-record'; src='ESPN play text (single-source; not fit assignment)'
  else:
    mm=p.get('mm')
    if mm:
      prim=mm.get('espn',{}).get('primary_defender') or mm.get('likely_defender')
      dfr=prim; conf='inferred'; src='pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)' if prim==mm.get('likely_defender') else 'pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said '+str(mm.get('likely_defender'))+')'
    elif p['kind']=='inc' and p.get('pbu'): dfr=p['pbu']; conf='confirmed (PBU named)'; src='ESPN play text (single-source)'
  p['dfr'],p['conf'],p['src']=dfr,conf,src
  p['shell_tend']=f"{p['defn']} season tendency man/zone/MOFC/MOFO {TEND.get(p['defn'],'n/a')} (Sharp, data thru Oct 27; tendency, not this play)"
  p['x']= (p['kind']=='rush' and p['yds']>=15) or (p['kind']=='rec' and p['yds']>=20)
json.dump(plays,open(W+'/_dissect_plays.json','w'),indent=0)
# ---- QB-adjusted position allowances (same residual method as runs/2026-11-01_shared_src/features.py rb_ypt_qbadj)
pbp=pd.read_parquet(B+'/runs/2026-11-01_shared_src/play_by_play_2026.parquet'); pbp=pbp[(pbp.season_type=='REG')&(pbp.week<=7)]
pos=pd.read_parquet(B+'/runs/2026-11-01_shared_src/players.parquet').set_index('gsis_id').position_group.to_dict()
att=pbp[(pbp.pass_attempt==1)&(pbp.sack!=1)].copy(); att['rpg']=att.receiver_player_id.map(pos)
att['grp']=att.rpg.where(att.rpg!='WR',att.pass_location.map({'middle':'WR_mid','left':'WR_out','right':'WR_out'}))
qbname=att.groupby('passer_player_id').passer_player_name.first().to_dict()
lgypt=att.groupby('grp').receiving_yards.apply(lambda s:s.fillna(0).sum()/len(s)).to_dict()
def qbbase(qbabbr,team,grp):
  t=NV.get(team,team); c=att[(att.posteam==t)&(att.passer_player_name.str.split('.').str[-1]==qbabbr.split('.')[-1])&(att.grp==grp)]
  return (c.receiving_yards.fillna(0).sum()/len(c),len(c)) if len(c)>=8 else (lgypt.get(grp,0),0)
rows=[]
for g in sorted({p['game'] for p in plays}):
  for d in g.split('@'):
    pp=[p for p in plays if p['game']==g and p['defn']==d and p['kind'] in('rec','inc','int')]
    out={}
    for grp in ['WR_out','WR_mid','TE','RB']:
      def gg(p):
        if p['pos']=='WR': return 'WR_mid' if p['loc']=='middle' else 'WR_out'
        return p['pos']
      xs=[p for p in pp if gg(p)==grp]
      if not xs: out[grp]=(0,0,0,None,''); continue
      yds=sum(p['yds'] for p in xs if p['kind']=='rec'); n=len(xs); rc=sum(p['kind']=='rec' for p in xs)
      qb=re.search(r'([A-Z][a-z]?\.[A-Za-z\'\-]+) pass',xs[0]['text']); off=xs[0]['off']
      b,nb=qbbase(qb.group(1) if qb else '',off,grp)
      out[grp]=(n,rc,yds,round(yds/n-b,2),f"{qb.group(1) if qb else '?'} base {b:.1f} ({'QB n='+str(nb) if nb else 'league fallback'})")
    ru=[p for p in plays if p['game']==g and p['defn']==d and p['kind']=='rush' and p['pos']=='RB']
    rows.append(dict(game=g,defn=d,out=out,rbrush=(len(ru),sum(p['yds'] for p in ru))))
json.dump(rows,open(W+'/_dissect_posallow.json','w'),indent=0,default=str)
# ---- defender tallies (ESPN text proxy, CAR ledger method)
tal=collections.defaultdict(lambda:dict(rec=0,yds=0,x=0,pbu=0,int=0,pen=0,recv=collections.Counter(),team='',pos=''))
led=[]
for p in plays:
  if p['kind']=='rush': continue
  if p['kind']=='rec' and p['tk']:
    t=tal[(p['game'],p['tk'][0])]; t['rec']+=1; t['yds']+=p['yds']; t['x']+=p['x']; t['recv'][p['tgt']]+=1; t['team']=p['defn']
    led.append([STAMP,p['game'],p['tk'][0],p['defn'],'',p['tgt'],1,p['yds'],'tackler after catch (ESPN text, wk8 dissect)'+('; EXPL20' if p['x'] else '')])
  if p['kind']=='inc' and p.get('pbu'):
    t=tal[(p['game'],p['pbu'])]; t['pbu']+=1; t['team']=p['defn']; led.append([STAMP,p['game'],p['pbu'],p['defn'],'',p['tgt'],0,0,'named on incompletion/PBU (ESPN text)'])
  if p['kind']=='int':
    t=tal[(p['game'],p['dfr'])]; t['int']+=1; t['team']=p['defn']; led.append([STAMP,p['game'],p['dfr'],p['defn'],'',p['tgt'],0,0,'INT (ESPN text)'])
  for nm,why in p['pen']:
    t=tal[(p['game'],nm)]; t['pen']+=1; t['team']=p['defn']; led.append([STAMP,p['game'],nm,p['defn'],'',p['tgt'],0,0,'penalty on pass play: '+why])
for (g,nm),t in tal.items():
  r=lookup(t['team'],nm); t['pos']=r[3] if r else '?'
for l in led:
  r=lookup(l[3],l[2]); l[4]=r[3] if r else ''
json.dump({f'{g}|{n}':dict(v,recv=dict(v['recv'])) for (g,n),v in tal.items()},open(W+'/_dissect_defenders.json','w'),indent=0)
# ledger append (dedupe on stamp+game)
L=B+'/defender_ledger.csv'
ex={(r['date'],r['game']) for r in csv.DictReader(open(L))}
with open(L,'a',newline='') as f:
  w=csv.writer(f); n=0
  for l in led:
    if (l[0],l[1]) in ex: continue
    w.writerow(l); n+=1
print('ledger rows',n,'plays',len(plays),'expl',sum(p['x'] for p in plays))
