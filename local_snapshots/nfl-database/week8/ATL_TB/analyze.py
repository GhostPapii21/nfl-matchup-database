import json,re,collections,glob
N=r"([A-Z][a-z]?\.[A-Za-z'\-]+(?: Jr\.)?)"
pos={}
for f in glob.glob('raw/roster_*.json'):
  d=json.load(open(f)); ab=d['team']['abbreviation']
  for g in d['athletes']:
    for a in g['items']:
      k=(ab,a['firstName'][0]+'.'+a['lastName'].split()[0]); pos[k]=a['position']['abbreviation']
def tk(t):
  out=[]
  for g in re.findall(r'\(([^)]*)\)',t):
    if 'Shotgun' in g or 'Huddle' in g or 'No Huddle' in g: continue
    out+=[x.strip() for x in re.split('[;,]',g) if x.strip()]
  return out
G=[]
for f in sorted(glob.glob('raw/summary_*.json')):
  d=json.load(open(f))
  if not d.get('drives'): continue
  c=d['header']['competitions'][0]; tm={x['homeAway']:x['team']['abbreviation'] for x in c['competitors']}
  wk=d['header']['week']; seen=set()
  for dr in d['drives']['previous']:
    off=dr['team']['abbreviation']; de=tm['home'] if off==tm['away'] else tm['away']
    for p in dr['plays']:
      if p['id'] in seen: continue
      seen.add(p['id']); t=p['text']
      if 'REVERSED.' in t: t=t.split('REVERSED.')[-1]
      s=p.get('start',{})
      G.append(dict(wk=wk,g=f"{tm['away']}@{tm['home']}",off=off,de=de,q=p['period']['number'],clk=p['clock']['displayValue'],dd=s.get('shortDownDistanceText',''),down=s.get('down',0),t=t.strip(),nul='No Play' in t))
DB=[]
for p in G:
  t=p['t']; hit=re.findall(r'\[([^\]]+)\]',t)
  m=re.search(r"([A-Z][a-z]?\.[A-Za-z'\-]+) pass (incomplete )?(short|deep) (left|middle|right)(?: (?:to|intended for) "+N+")?",t)
  sk=re.search(r"([A-Z][a-z]?\.[A-Za-z'\-]+) sacked .*?for (-?\d+|no gain)",t)
  scr=re.search(r"([A-Z][a-z]?\.[A-Za-z'\-]+) scrambles (left end|right end|left tackle|right tackle|left guard|right guard|up the middle)[^.]*?for (-?\d+|no gain)",t)
  if not(m or sk or scr): continue
  x=dict(p,hit=hit,qb=(m or sk or scr).group(1))
  if m:
    inc=bool(m.group(2)) or 'INTERCEPTED' in t; ym=re.search(r'for (-?\d+) yards',t)
    x.update(kind='target',rcv=m.group(5) or '?',depth=m.group(3),dir=m.group(4),yds=0 if inc or not ym else int(ym.group(1)),
      res='INT' if 'INTERCEPTED' in t else 'inc' if inc else 'TD' if 'TOUCHDOWN' in t else 'rec',dfn=tk(t.split('PENALTY')[0]))
    if 'INTERCEPTED' in t:
      mm=re.search(r'INTERCEPTED by '+N,t); x['dfn']=[mm.group(1)] if mm else ['?']
  elif sk: x.update(kind='sack',yds=0 if sk.group(2)=='no gain' else int(sk.group(2)),dfn=tk(t.split('PENALTY')[0]))
  else: x.update(kind='scramble',dir=scr.group(2),yds=0 if scr.group(3)=='no gain' else int(scr.group(3)),dfn=tk(t.split('PENALTY')[0]))
  DB.append(x)
json.dump(DB,open('raw/dropbacks.json','w'))
J=lambda a:'; '.join(a) if a else '—'
L=[]
pct=lambda c:', '.join(f"{k} {v}/{sum(c.values())} ({v/sum(c.values()):.0%})" for k,v in c.most_common()) if c else 'none'
# QB trees
for qb,team in (('B.Mayfield','TB'),('J.Daniels','TB'),('M.Penix','ATL')):
  db=[x for x in DB if x['qb']==qb and not x['nul']]
  if not db: continue
  L+=[f"## {qb} ({team}) pressure / 3rd-down tree, 2026 games (PBP)",'']
  for g in sorted(set(x['g'] for x in db),key=lambda g:[x['wk'] for x in db if x['g']==g][0]):
    s=[x for x in db if x['g']==g]; wk=s[0]['wk']
    L.append(f"- Wk{wk} {g}: dropbacks {len(s)}, sacks {sum(x['kind']=='sack' for x in s)}, hit plays {sum(bool(x['hit']) for x in s)}, scrambles {sum(x['kind']=='scramble' for x in s)} for {sum(x['yds'] for x in s if x['kind']=='scramble')} yds")
  L+=['','| wk | Q | clk | D&D | play | result | defender (tackler/PBU) | hit by | tag |','|-|-|-|-|-|-|-|-|-|']
  t3=collections.Counter();tpr=collections.Counter()
  prevg=None;prev=None
  for x in db:
    if x['g']!=prevg: prev=None;prevg=x['g']
    tags=[]
    if x['down'] in(3,4): tags.append('3rd/4th')
    pr=x['kind'] in('sack','scramble') or x['hit']
    if pr: tags.append('pressure')
    if prev and (prev['kind'] in('sack','scramble') or prev['hit']) and x['kind']=='target': tags.append('next-after-pressure')
    prev=x
    if not tags: continue
    desc=f"{x['rcv']} {x['depth']} {x['dir']}" if x['kind']=='target' else x['kind'].upper()+(' '+x.get('dir','') if x['kind']=='scramble' else '')
    L.append(f"| {x['wk']} | {x['q']} | {x['clk']} | {x['dd']} | {desc} | {x.get('res','')} {x['yds']} | {J(x['dfn'])} | {J(x['hit'])} | {', '.join(tags)} |")
    if x['kind']=='target':
      b=x['rcv']
      if '3rd/4th' in tags: t3[b]+=1
      if 'pressure' in tags or 'next-after-pressure' in tags: tpr[b]+=1
  L+=['',f"- 3rd/4th-down target share: {pct(t3)}",f"- Under pressure (QB hit on throw) or next throw after sack/hit/scramble: {pct(tpr)}",'']
# receiver usage per team
for team in ('TB','ATL'):
  tg=[x for x in DB if x['off']==team and x['kind']=='target' and not x['nul']]
  wks=sorted(set(x['wk'] for x in tg)); l3=wks[-3:]
  L+=[f"## {team} target usage, PBP (season Wk{wks[0]}-{wks[-1]}; last 3 = Wk{l3[0]}-{l3[-1]})",'','| rcv | pos | tgt | share | rec | yds | deep tgt% | 20+ rec | L3 tgt | L3 share | L3 rec | 3rd/4th tgt |','|-|-|-|-|-|-|-|-|-|-|-|-|']
  tot=len(tg); tl3=sum(x['wk'] in l3 for x in tg)
  for r,c in collections.Counter(x['rcv'] for x in tg).most_common():
    s=[x for x in tg if x['rcv']==r]; cc=[x for x in s if x['res'] in('rec','TD')]; s3=[x for x in s if x['wk'] in l3]
    L.append(f"| {r} | {pos.get((team,r),'?')} | {c} | {c/tot:.0%} | {len(cc)} | {sum(x['yds'] for x in cc)} | {sum(x['depth']=='deep' for x in s)/c:.0%} | {sum(x['yds']>=20 for x in cc)} | {len(s3)} | {len(s3)/tl3:.0%} | {sum(x['res'] in('rec','TD') for x in s3)} | {sum(x['down'] in(3,4) for x in s)} |")
  L.append('')
# defenses
for team in ('ATL','TB'):
  tg=[x for x in DB if x['de']==team and x['kind']=='target' and not x['nul']]
  dbs=[x for x in DB if x['de']==team and not x['nul']]
  L+=[f"## {team} pass defense, PBP-derived (2026 Wk1-7)",'',f"- Opp dropbacks {len(dbs)}, sacks {sum(x['kind']=='sack' for x in dbs)} ({sum(x['kind']=='sack' for x in dbs)/len(dbs):.1%}), QB-hit plays {sum(bool(x['hit']) for x in dbs)}, scrambles allowed {sum(x['kind']=='scramble' for x in dbs)}"]
  bp=collections.defaultdict(lambda:[0,0,0,0])
  for x in tg:
    p=pos.get((x['off'],x['rcv']),'?'); bp[p][0]+=1
    if x['res'] in('rec','TD'): bp[p][1]+=1;bp[p][2]+=x['yds'];bp[p][3]+=x['yds']>=20
  L.append('- Allowed by receiver position (tgt/rec/yds/20+): '+'; '.join(f"{k} {v[0]}/{v[1]}/{v[2]}/{v[3]}" for k,v in sorted(bp.items(),key=lambda z:-z[1][2])))
  lo=collections.defaultdict(lambda:[0,0,0])
  for x in tg:
    k=f"{x['depth']} {x['dir']}"; lo[k][0]+=1
    if x['res'] in('rec','TD'): lo[k][1]+=1; lo[k][2]+=x['yds']
  L.append('- By location (tgt/rec/yds): '+'; '.join(f"{k} {v[0]}/{v[1]}/{v[2]}" for k,v in sorted(lo.items(),key=lambda z:-z[1][2])))
  ex=[x for x in tg if x['res'] in('rec','TD') and x['yds']>=20]
  L.append(f"- 20+ yd completions allowed: {len(ex)} — "+'; '.join(f"Wk{x['wk']} {x['rcv']}({x['off']}) {x['depth']} {x['dir']} {x['yds']} [{J(x['dfn'])}]" for x in ex))
  dd=collections.defaultdict(lambda:[0,0,0])
  for x in tg:
    if x['res'] in('rec','TD'):
      for y in x['dfn']: dd[y][0]+=1;dd[y][1]+=x['yds'];dd[y][2]+=x['yds']>=20
  L.append('- Named on completions (tackler, NOT coverage): '+'; '.join(f"{k} {v[0]}/{v[1]}/{v[2]}x20+" for k,v in sorted(dd.items(),key=lambda z:-z[1][1])[:10]))
  pbu=collections.Counter(y for x in tg if x['res'] in('inc','INT') for y in x['dfn'])
  L.append('- Named on incompletions/INTs (PBU/INT): '+', '.join(f"{k} {v}" for k,v in pbu.most_common(8)))
  sk=collections.Counter(y for x in dbs if x['kind']=='sack' for y in x['dfn']); ht=collections.Counter(y for x in dbs for y in x['hit'])
  L.append('- Sackers: '+', '.join(f"{k} {v}" for k,v in sk.most_common())+' | QB hits: '+', '.join(f"{k} {v}" for k,v in ht.most_common(8)))
  for g in sorted(set(x['g'] for x in dbs),key=lambda g:[x['wk'] for x in dbs if x['g']==g][0]):
    s=[x for x in dbs if x['g']==g]; t2=[x for x in s if x['kind']=='target']; c2=[x for x in t2 if x['res'] in('rec','TD')]
    L.append(f"  - Wk{s[0]['wk']} {g}: {len(s)} db, {len(c2)}/{len(t2)} for {sum(x['yds'] for x in c2)}, sacks {sum(x['kind']=='sack' for x in s)}, hit plays {sum(bool(x['hit']) for x in s)}, QBs {','.join(sorted(set(x['qb'] for x in s)))}")
  L.append('')
open('pbp_core.md','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
