import json,re,csv,os,glob,shutil,collections
B='/workspace/nfl-database'; PL=B+'/playlogs'; W=PL+'/2026_wk8'
cov=json.load(open(B+'/week8/breakdown/coverage/coverage.json'))
prof=json.load(open(B+'/week8/defense/defense_profiles.json'))['teams']
games=sorted(set(os.path.basename(p)[:-9] for p in glob.glob(W+'/*_box.json')))
# pregame matchups: (defense, receiver) -> info ; also secondary list per defense
mt={};sec={};shell={}
for g in cov['games']:
  for s in g['sides']:
    sec[s['defense']]=s.get('secondary',[]); shell[s['defense']]=s.get('sharp_ypt',{})
    for m in s.get('matchups',[]):
      mt[(s['defense'],m['receiver'])]=m
def abbr_match(ab,full):
  # ESPN 'J.Dotson' / 'Bi.Robinson' vs 'Jahan Dotson'
  if '.' not in ab: return False
  f,l=ab.split('.',1); parts=full.replace(' Jr.','').replace(' Sr.','').replace(' III','').replace(' II','').split()
  return len(parts)>=2 and parts[-1].lower().startswith(l.lower().strip()) and parts[0].lower().startswith(f.lower())
DBPOS={}
for d,lst in sec.items():
  for x in lst:
    if any(k in x.get('depth','') for k in ('CB','NB','S1','S2','FS','SS')): DBPOS[(d,x['name'])]=x['depth']
def db_of(defense,abbr):
  for (d,n),dep in DBPOS.items():
    if d==defense and abbr_match(abbr,n): return n,dep
  return None
# ---------- archetype taxonomy (mapped from week8/player_types labels + this week's usage)
def archetype(pos,types,line):
  t=(types or '').lower()
  if pos=='QB':
    if 'scramb' in t or 'rush' in t: return 'QB-scrambler'
    if 'checkdown' in t or 'short-area' in t: return 'QB-checkdown game-manager'
    return 'QB-pocket'
  if pos=='RB':
    if 'scat' in t or ('receiv' in t and 'lead' not in t): return 'RB-receiving/scat'
    if 'elite rusher' in t or 'explosive' in t: return 'RB-home-run zone runner'
    if 'committee' in t or 'backup' in t: return 'RB-committee/change-of-pace'
    return 'RB-power/volume early-down'
  if pos=='TE':
    if 'primary' in t or 'seam' in t or 'move' in t or 'red-zone' in t: return 'TE-move/seam'
    return 'TE-inline'
  if 'explosive/deep' in t and 'volume' not in t: return 'WR-deep speed'
  if 'slot' in t: return 'WR-slot separator'
  if 'yac' in t or 'screen' in t: return 'WR-YAC/screen'
  if 'contested' in t or 'big' in t: return 'WR-contested-catch big'
  if 'volume' in t or 'possession' in t: return 'WR-X outside volume'
  if 'rotational' in t: return 'WR-rotational depth'
  return 'WR-unclassified'
PT={}
for f in glob.glob(B+'/week8/player_types/*.md'):
  team=os.path.basename(f)[:-3]; pos=None
  for ln in open(f):
    m=re.match(r'## (WR|TE|RB|QB)\s*$',ln.strip());
    if m: pos=m.group(1); continue
    if pos and ln.startswith('| ') and not ln.startswith('| player') and not ln.startswith('| QB |'):
      c=[x.strip() for x in ln.split('|')[1:-1]]
      if len(c)>2 and not set(c[0])<=set('-'): PT[(team,c[0])]=(pos,c[1].replace('*',''))
def ptype(team,name,pos_hint=None):
  for (t,n),v in PT.items():
    if t==team and (n==name or n.split()[-1]==name.split()[-1] and n[0]==name[0]): return v
  for (t,n),v in PT.items():  # QB abbr like M.Penix
    if t==team and '.' in n and abbr_match(n,name): return v
  return (pos_hint,'')
TEAMALIAS={'LAR':'LA'}
# ---------- explosives: parse existing table
src=PL+'/explosives_allowed.md'
rows=[]; defplays=[]
have=set()  # always rebuild from plays files; offense = drive possession team, defense = the other team
for g in games:
  key=g.replace('_','@')
  if key in have: continue
  a,h=g.split('_'); off=None
  for ln in open(f'{W}/{g}_plays.md'):
    m=re.match(r'## Drive: (\w+)',ln)
    if m: off=m.group(1); continue
    m=re.match(r'- (Q\d \d+:\d+) \[(Rush|Pass Reception|Passing Touchdown|Rushing Touchdown)\] (.*)',ln)
    if not m or not off: continue
    if 'INTERCEPTED' in m.group(3) or 'FUMBLE' in m.group(3) and 'RECOVERED by '+off not in m.group(3) and re.search(r'for \d+ yards, TOUCHDOWN',m.group(3).split('RECOVERED')[-1] if 'RECOVERED' in m.group(3) else ''):
      if 'INTERCEPTED' in m.group(3): defplays.append([key,h if off==a else a,off,m.group(1),m.group(3).split(' (score')[0]])
      continue
    y=re.search(r'for (-?\d+) yards',m.group(3));
    if not y: continue
    y=int(y.group(1)); typ='rush' if 'Rush' in m.group(2) else 'pass'
    if (typ=='pass' and y>=20) or (typ=='rush' and y>=10):
      tk=re.findall(r'\(([^()]*)\)\.',m.group(3)); dfn=h if off==a else a
      rows.append(['2026 W8',key,dfn,off,m.group(1),typ,str(y),tk[-1] if tk else '',m.group(3).split(' (score')[0]])
def attrib(r):
  _,game,dfn,off,when,typ,yds,tack,play=r[:9]
  if typ=='rush':
    tks=[t.strip() for t in tack.split(';') if t.strip()]
    if tks: return ('run-fit: '+'; '.join(tks),'confirmed-tackler (ESPN play text; tackler of record, not gap assignment)','')
    return ('','unknown','TD/no tackler listed')
  m=re.search(r'pass \w+ \w+ to ([A-Z][a-z]?\.[A-Za-z\'\-]+)',play); tgt=m.group(1) if m else ''
  pen=re.search(r'(?:PENALTY|Penalty) on '+dfn+r'-([A-Z][a-z]?\.[A-Za-z\'\-]+), Defensive (Pass Interference|Holding|Illegal Contact)',play) or re.search(r'PENALTY on '+dfn+r'-([A-Z][a-z]?\.[A-Za-z\'\-]+), Defensive (Pass Interference|Holding)',play,re.I) or re.search(r'Penalty on '+dfn+r'-([A-Z][a-z]?\.[A-Za-z\'\-]+), Defensive (Pass Interference|Holding)',play)
  if pen: return (pen.group(1)+' (flagged on play)','confirmed (ESPN play text: defensive penalty on the play)',tgt)
  # pregame matchup
  for (d,rec),mm in mt.items():
    if d==dfn and abbr_match(tgt,rec):
      e=mm.get('espn',{}); prim=e.get('primary_defender') or mm.get('likely_defender')
      tk=[t.strip() for t in tack.split(';')]; tkdb=[t for t in tk if db_of(dfn,t)]
      note=f"pregame primary {prim} ({mm.get('inferred_alignment')}; ESPN alignment {e.get('alignment','?')})"
      if tkdb and abbr_match(tkdb[0],prim or ''): return (prim,'inferred (pregame alignment + same DB is tackler)',tgt)
      return (prim+(' | tackler '+', '.join(tkdb) if tkdb else ''),'inferred (pregame alignment: '+note+')',tgt)
  tk=[t.strip() for t in tack.split(';') if t.strip()]; tkdb=[f"{t} ({db_of(dfn,t)[1]})" for t in tk if db_of(dfn,t)]
  if tkdb: return ('tackler '+', '.join(tkdb)+' (coverage unverified)','unknown (DB tackler only)',tgt)
  return ('','unknown',tgt)
out=[]
for r in rows:
  d,conf,tgt=attrib(r); out.append(r[:9]+[d,conf])
with open(src,'w') as f:
  f.write('# Explosives allowed (pass 20+, rush 10+)\n\nExisting rows kept; columns Coverage/run-fit defender + Confidence added 2026-11-01 by build_edges_wk8.py. Confidence: confirmed (defensive penalty named on the play) | confirmed-tackler (run plays: ESPN tackler of record) | inferred (pregame WR/CB alignment from week8/breakdown/coverage, ESPN Mike Clay cheat sheet) | unknown. No defender invented. Rebuilt from 2026_wk8/*_plays.md drive possession (defense = non-possession team); asserted by tools/test_explosives.py. Interception/fumble returns moved to 2026_wk8/defensive_returns.md. nflverse pbp/FTN 2026 checked 16:20 ET: Week 8 has only CAR@GB; participation file 404. Free recaps (PFT, steelers.com, NFL.com, VAVEL, NY Post) checked: none name the coverage defender.\n\n')
  f.write('| Season/Wk | Game | Defense | Offense | When | Type | Yds | Defender/tackler (ESPN) | Play | Coverage/run-fit defender | Confidence |\n|'+'---|'*11+'\n')
  for r in out: f.write('| '+' | '.join(x.replace('|','/') for x in r)+' |\n')
# per-defense table
cnt=collections.defaultdict(lambda:[0,0,0]); conf=collections.Counter()
for r in out:
  k=(r[1],r[2]); cnt[k][0 if r[5]=='pass' else 1]+=1; cnt[k][2]+=int(r[6])
  c=r[10].split(' ')[0]; conf[('pass' if r[5]=='pass' else 'rush',c)]+=1
unknown=[r for r in out if r[5]=='pass' and not r[10].startswith(('confirmed','inferred'))]
with open(W+'/defensive_returns.md','w') as f:
  f.write('# Defensive scoring/return plays (not offensive explosives)\n\n| Game | Defense | Offense | When | Play |\n|---|---|---|---|---|\n')
  for d in defplays: f.write('| '+' | '.join(d)+' |\n')
with open(W+'/PFF_UNKNOWN_PLAYS.md','w') as f:
  f.write('# Explosive pass plays with no confirmed/inferred coverage defender (fill from PFF)\n\n| Game | Defense | Q/clock | Yds | Play | Lead |\n|---|---|---|---|---|---|\n')
  for r in unknown: f.write(f'| {r[1]} | {r[2]} | {r[4]} | {r[6]} | {r[8]} | {r[9]} |\n')
  f.write('\nRun plays: tackler of record is logged; gap/fit responsibility (who missed the fit) needs PFF/film for every rush explosive too.\n')
json.dump({'per_def':{f'{k[0]}|{k[1]}':v for k,v in cnt.items()},'conf':{f'{a}|{b}':n for (a,b),n in conf.items()}},open(W+'/_explosive_summary.json','w'),indent=1)
# ---------- edge players
lines=collections.defaultdict(dict)
for fn in ['props_2026-10-30_prizepicks.csv','props_2026-10-30_fanduel.csv']:
  for r in csv.DictReader(open(B+'/week8/lines/'+fn)):
    mk=r['market']
    if any(x in mk for x in ('demon','goblin','alt')): continue
    try: lines[r['player']][mk]=float(r['line'])
    except: pass
expl_by=collections.defaultdict(list)
for r in out:
  m=re.search(r'(?:to|^\(Shotgun\) |^)\s*([A-Z][a-z]?\.[A-Za-z\'\-]+) (?:up the middle|left|right|scrambles|to )',r[8]) if r[5]=='rush' else re.search(r'pass \w+ \w+ to ([A-Z][a-z]?\.[A-Za-z\'\-]+)',r[8])
  if r[5]=='rush': m=re.search(r'([A-Z][a-z]?\.[A-Za-z\'\-]+) (?:up the middle|left \w+|right \w+|scrambles|to )',r[8].replace('(Shotgun) ',''))
  if m: expl_by[(r[3],m.group(1))].append((r,))
def nint(x):
  try: return int(x)
  except: return 0
edges=[]
for g in games:
  bx=json.load(open(f'{W}/{g}_box.json')); a,h=g.split('_')
  for team,st in bx['teams'].items():
    opp=h if team==a else a; stat=collections.defaultdict(dict)
    for cat in ('passing','rushing','receiving'):
      for p in st.get(cat,[]): stat[p['player']][cat]=p
    for name,s in stat.items():
      ru=s.get('rushing',{}); re_=s.get('receiving',{}); pa=s.get('passing',{})
      td=nint(ru.get('TD'))+nint(re_.get('TD')); ptd=nint(pa.get('TD'))
      ex=[e[0] for (o,ab),e2 in expl_by.items() if o==team and abbr_match(ab,name) for e in e2]
      beats=[]
      for mk,ln in lines.get(name,{}).items():
        v=None
        if mk in('rec_yds','receiving_yds','rec_yards'): v=nint(re_.get('YDS'))
        elif mk in('receptions','rec'): v=nint(re_.get('REC'))
        elif mk in('rush_yds','rushing_yds'): v=nint(ru.get('YDS'))
        elif mk in('pass_yds',): v=nint(pa.get('YDS'))
        elif mk in('rush_rec_yds','rush+rec_yds'): v=nint(ru.get('YDS'))+nint(re_.get('YDS'))
        if v is not None and v>ln: beats.append(f'{mk} {v}>{ln}')
      big=nint(ru.get('YDS'))>=70 or nint(re_.get('YDS'))>=70 or nint(re_.get('REC'))>=6 or nint(pa.get('YDS'))>=250 or ptd>=2
      if not (td or ex or beats or big): continue
      pos,types=ptype(TEAMALIAS.get(team,team),name)
      if not pos: pos='QB' if pa else ('RB' if nint(ru.get('CAR'))>=5 else 'WR/TE')
      if pos=='WR/TE': arch='unprofiled receiver (no week8 player_types row)'
      else: arch=archetype(pos,types,None)
      line=[]
      if pa: line.append(f"{pa['C/ATT']} {pa['YDS']}y {pa['TD']}TD {pa['INT']}INT")
      if ru: line.append(f"{ru['CAR']}-{ru['YDS']} {ru['TD']}TD")
      if re_: line.append(f"{re_['REC']}/{re_.get('TGTS','?')}tgt {re_['YDS']}y {re_['TD']}TD")
      edges.append(dict(game=g.replace('_','@'),team=team,opp=opp,name=name,pos=pos,types=types,arch=arch,line='; '.join(line),td=td+ptd,ex=ex,beats=beats,ru=ru,re=re_,pa=pa))
json.dump(edges,open(W+'/_edges_raw.json','w'),indent=1,default=str)
print(len(out),'explosives',dict(conf)); print(len(edges),'edge players')
for k,v in sorted(cnt.items()): print(k,v)
