import json,re,collections,csv
d=json.load(open('raw/summary_401872964.json'));seen=set();P=[]
N=r"([A-Z][a-z]?\.[A-Za-z'\-]+(?: Jr\.)?)"
for dr in d['drives']['previous']:
  off=dr['team']['abbreviation']
  for p in dr['plays']:
    if p['id'] in seen: continue
    seen.add(p['id']);t=p['text']
    if 'REVERSED.' in t: t=t.split('REVERSED.')[-1]
    P.append(dict(off=off,q=p['period']['number'],clk=p['clock']['displayValue'],dd=p.get('start',{}).get('shortDownDistanceText',''),down=p.get('start',{}).get('down',0),sc=f"PIT {p['awayScore']}-CLE {p['homeScore']}",t=t.strip(),nul='No Play' in t))
def tk(t):
  m=re.search(r'\((?:[^)]*?)\)',t.split(' for ')[-1] if ' for ' in t else t)
  m=re.findall(r'\(([^)]*)\)',t)
  out=[]
  for g in m:
    if 'Shotgun' in g or 'Huddle' in g: continue
    out+= [x.strip() for x in re.split('[;,]',g)]
  return out
dropbacks=[];targets=[];runs=[];L=[]
for p in P:
  t=p['t']
  hit=re.findall(r'\[([^\]]+)\]',t)
  m=re.search(r'([A-Z]\.[A-Za-z]+) pass (incomplete )?(short|deep) (left|middle|right)(?: (?:to|intended for) '+N+')?',t)
  sk=re.search(r'([A-Z]\.[A-Za-z]+) sacked .*?for (-?\d+) yards \(([^)]*)\)',t)
  scr=re.search(r'([A-Z]\.[A-Za-z]+) scrambles (\w+ \w+|up the middle) .*?for (-?\d+) yards',t)
  if m or sk or scr or re.search(r'pass incomplete\.?$',t):
    dbk=dict(p,hit=hit)
    if m:
      inc=bool(m.group(2)) or 'INTERCEPTED' in t; ym=re.search(r'for (-?\d+) yards',t); y=0 if inc or not ym else int(ym.group(1))
      r='INT' if 'INTERCEPTED' in t else 'inc' if inc else ('TD' if 'TOUCHDOWN' in t else 'rec')
      dfn=tk(t.split('PENALTY')[0]); 
      if 'INTERCEPTED' in t: dfn=[re.search(r'INTERCEPTED by '+N,t).group(1)]
      tg=dict(p,qb=m.group(1),depth=m.group(3),dir=m.group(4),rcv=m.group(5) or '?',yds=y,res=r+(' (nullified: '+re.search(r'PENALTY on (\S+ ?\S*), ([^,]+)',t).group(0)+')' if p['nul'] else ''),dfn=[x for x in dfn],hit=hit)
      targets.append(tg); dbk.update(kind='target',desc=f"{tg['rcv']} {tg['depth']} {tg['dir']} {r} {y}")
    elif sk: dbk.update(qb=sk.group(1),kind='sack',desc=f"SACK {sk.group(2)} ({sk.group(3)})"+(' [nullified]' if p['nul'] else ''))
    elif scr: dbk.update(qb=scr.group(1),kind='scramble',desc=f"SCRAMBLE {scr.group(2)} {scr.group(3)} yds ({', '.join(tk(t.split('PENALTY')[0]))})"+(' + '+t.split('PENALTY')[1][:60] if 'PENALTY' in t else ''))
    else: dbk.update(qb='?',kind='other',desc=t[:80])
    dropbacks.append(dbk); continue
  rm=re.search(r'^(?:\([^)]*\) )*([A-Z]\.[A-Za-z\'-]+) (left end|left tackle|left guard|up the middle|right guard|right tackle|right end) .*?for (-?\d+|no gain)',t)
  if rm and 'kneels' not in t:
    y=0 if 'no gain' in rm.group(3) else int(rm.group(3)); runs.append(dict(p,rb=rm.group(1),gap=rm.group(2),yds=y,dfn=tk(t.split('PENALTY')[0])))
for r in runs:
  if 'no gain' in r['t']: r['yds']=0
J=lambda x:'; '.join(x) if x else '—'
L+=['# PIT @ CLE, 2026 Week 4 (Thu Oct 1, 8:15 PM ET), CLE 27, PIT 24. ESPN event 401872964','',
'Source: ESPN summary API play-by-play and box score (raw/). Depth and direction are ESPN charting. "Defender" means the name in parentheses (tackler or PBU) on the play, NOT a coverage assignment. Brackets [X] are QB hits. The PBP does not record blitzes, hurries, coverage shell, or yards before or after contact.','']
L+=['## Box score (ESPN)','']
for tm in d['boxscore']['players']:
  for st in tm['statistics']:
    if st['name'] in('passing','rushing','receiving'):
      L.append(f"**{tm['team']['abbreviation']} {st['name']}** ({', '.join(st['labels'])})")
      for a in st['athletes']: L.append(f"- {a['athlete']['displayName']}: {' / '.join(a['stats'])}")
  L.append('')
L+=['## Runs by gap (all RBs; Warren detail below)','','| team | Q | clk | D&D | score | rb | gap | yds | tacklers |','|-|-|-|-|-|-|-|-|-|']
for r in runs: L.append(f"| {r['off']} | {r['q']} | {r['clk']} | {r['dd']} | {r['sc']} | {r['rb']} | {r['gap']} | {r['yds']}{' (nullified)' if r['nul'] else ''} | {J(r['dfn'])} |")
w=[r for r in runs if r['rb']=='J.Warren' and not r['nul']]
g=collections.defaultdict(list)
for r in w: g[r['gap']].append(r['yds'])
L+=['',f"**Warren: {len(w)} counted carries in PBP, {sum(r['yds'] for r in w)} yards.** By gap: "+'; '.join(f"{k} {len(v)} carries/{sum(v)} yds" for k,v in g.items()),
f"- 10+ runs: "+', '.join(f"Q{r['q']} {r['clk']} {r['gap']} {r['yds']}" for r in w if r['yds']>=10),
f"- By half: H1 {sum(r['yds'] for r in w if r['q']<=2)} yds on {sum(r['q']<=2 for r in w)} carries; H2 {sum(r['yds'] for r in w if r['q']>2)} yds on {sum(r['q']>2 for r in w)} carries",
f"- CLE tacklers on Warren runs: "+', '.join(f"{k} {v}" for k,v in collections.Counter(x for r in w for x in r['dfn']).most_common()),'']
L+=['## Every target','','| team | Q | clk | D&D | QB | rcv | depth | dir | yds | result | named defender | QB hit |','|-|-|-|-|-|-|-|-|-|-|-|-|']
for x in targets: L.append(f"| {x['off']} | {x['q']} | {x['clk']} | {x['dd']} | {x['qb']} | {x['rcv']} | {x['depth']} | {x['dir']} | {x['yds']} | {x['res']} | {J(x['dfn'])} | {J(x['hit'])} |")
L+=['','### Target summary (penalty-nullified targets excluded)','','| team | rcv | tgt | rec | yds | 20+ | short | deep | L/M/R | top named defenders |','|-|-|-|-|-|-|-|-|-|-|']
for tm in ('PIT','CLE'):
  for rcv,c in collections.Counter(x['rcv'] for x in targets if x['off']==tm and not x['nul']).most_common():
    s=[x for x in targets if x['off']==tm and x['rcv']==rcv and not x['nul']];cc=[x for x in s if x['res'] in('rec','TD')]
    L.append(f"| {tm} | {rcv} | {c} | {len(cc)} | {sum(x['yds'] for x in cc)} | {sum(x['yds']>=20 for x in cc)} | {sum(x['depth']=='short' for x in s)} | {sum(x['depth']=='deep' for x in s)} | {sum(x['dir']=='left' for x in s)}/{sum(x['dir']=='middle' for x in s)}/{sum(x['dir']=='right' for x in s)} | {', '.join(f'{a} {b}' for a,b in collections.Counter(y for x in s for y in x['dfn']).most_common(3))} |")
L+=['','### Defenses: names on completions (tackler, PBP)','']
for tm in ('PIT','CLE'):
  c=collections.defaultdict(lambda:[0,0,0])
  for x in targets:
    if x['off']==tm and not x['nul'] and x['res'] in('rec','TD'):
      for y in x['dfn']: c[y][0]+=1;c[y][1]+=x['yds'];c[y][2]+=x['yds']>=20
  L.append(f"- vs {tm} passing: "+'; '.join(f"{k} {v[0]} rec/{v[1]} yds/{v[2]} 20+" for k,v in sorted(c.items(),key=lambda z:-z[1][1])))
  lo=collections.Counter(f"{x['depth']} {x['dir']}" for x in targets if x['off']==tm and not x['nul'])
  L.append(f"- {tm} target locations: "+', '.join(f'{k} {v}' for k,v in lo.most_common()))
L+=['','## QB pressure / 3rd-down tree (pressure proxies = sack, [QB hit], scramble; blitz/hurry NOT in PBP)','']
for tm in ('PIT','CLE'):
  db=[x for x in dropbacks if x['off']==tm]
  live=[x for x in db if not x['nul']]
  L+=[f"### {tm}: {len(live)} dropbacks counted ({len(db)} incl. nullified); sacks {sum(x['kind']=='sack' for x in live)}; QB-hit plays {sum(bool(x['hit']) for x in live)}; scrambles {sum(x['kind']=='scramble' for x in live)}",'','| Q | clk | D&D | score | play | hit by | tag |','|-|-|-|-|-|-|-|']
  tree=collections.Counter();tp=collections.Counter()
  for i,x in enumerate(db):
    tags=[]
    if x['down'] in(3,4): tags.append('3rd/4th')
    if x['kind'] in('sack','scramble') or x['hit']: tags.append('pressure')
    prev=db[i-1] if i else None
    if prev and (prev['kind'] in('sack','scramble') or prev['hit']) and x['kind']=='target': tags.append('next-after-pressure')
    if not tags: continue
    L.append(f"| {x['q']} | {x['clk']} | {x['dd']} | {x['sc']} | {x['desc']}{' [nullified]' if x['nul'] and x['kind']=='target' else ''} | {J(x['hit'])} | {', '.join(tags)} |")
    if x['kind']=='target':
      r=x['desc'].split()[0]
      if '3rd/4th' in tags: tree[r]+=1
      if 'pressure' in tags or 'next-after-pressure' in tags: tp[r]+=1
  f=lambda c:', '.join(f"{k} {v}/{sum(c.values())} ({v/sum(c.values()):.0%})" for k,v in c.most_common()) if c else 'none'
  L+=['',f"- 3rd/4th-down target share: {f(tree)}",f"- Under pressure (hit on throw) or next throw after a sack/hit/scramble: {f(tp)}",'']
open('game1_core.md','w').write('\n'.join(L)+'\n')
rows=[]
for x in targets:
  if x['nul'] or x['res'] not in('rec','TD'): 
    if x['res']=='inc' and x['dfn'] and not x['nul']:
      for y in x['dfn']: rows.append(['2026-10-01','PIT@CLE',y,'CLE' if x['off']=='PIT' else 'PIT','',x['rcv'],0,0,'PBP tackler/PBU (not coverage)'])
    continue
  for y in x['dfn']: rows.append(['2026-10-01','PIT@CLE',y,'CLE' if x['off']=='PIT' else 'PIT','',x['rcv'],1,x['yds'],'PBP tackler/PBU (not coverage)'])
json.dump(rows,open('raw/ledger_rows.json','w'))
print(len(targets),len(runs),len(rows))
