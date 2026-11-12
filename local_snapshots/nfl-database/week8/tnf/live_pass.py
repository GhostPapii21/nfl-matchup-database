#!/usr/bin/env python3
"""Per-target breakdown from ESPN PBP (re-runs live_pull.py data fetch). Usage: python3 live_pass.py [event_id]"""
import json,re,sys,urllib.request,datetime,collections as C
EID=sys.argv[1] if len(sys.argv)>1 else '401873023'
d=json.load(urllib.request.urlopen(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={EID}'))
hc=d['header']['competitions'][0];st=hc['status']['type']['detail']
score=' '.join(f"{c['team']['abbreviation']} {c.get('score','?')}" for c in hc['competitors'])
plays=[];seen=set()
for dr in d['drives'].get('previous',[])+([d['drives']['current']] if d['drives'].get('current') else []):
  off=dr['team']['abbreviation']
  for p in dr['plays']:
    if p['id'] in seen: continue
    seen.add(p['id']);plays.append((off,p))
P=C.defaultdict(lambda:C.Counter());LOC=C.defaultdict(C.Counter);PR=C.defaultdict(C.Counter)
for off,p in plays:
  tx=p['text'];ytg=p.get('start',{}).get('yardsToEndzone',99)
  if 'No Play' in tx or 'NULLIFIED' in tx.upper(): continue
  if ' sacked ' in tx: PR[off]['sacks']+=1
  if 'scrambles' in tx: PR[off]['scrambles']+=1
  if re.search(r'\bhit\b|pressure',tx,re.I): PR[off]['hit/pressure text']+=1
  m=re.search(r'pass (incomplete )?(short|deep)? ?(left|right|middle)? ?(?:to|intended for) ([A-Z]\.[\w\'-]+(?: (?:Jr|III|II)\.?)?)',tx)
  if not m: continue
  PR[off]['dropbacks']+=1
  inc=bool(m.group(1)) or 'INTERCEPT' in tx.upper();r=m.group(4)
  y=re.search(r'for (-?\d+) yards?',tx);y=0 if inc or not y else int(y.group(1))
  dep=m.group(2) or '?';di=m.group(3) or '?'
  c=P[(off,r)];c['tgt']+=1;c['rec']+=0 if inc else 1;c['yds']+=y;c[dep]+=1;c[di]+=1
  if ytg<=20: c['RZ tgt']+=1
  LOC[off][f'{dep} {di}']+=1;LOC[off][f'{dep} {di} yds']+=y
now=datetime.datetime.now().strftime('%I:%M %p ET')
L=[f'\n## Targets snapshot {now} — {score} — {st}\n','| off | player | tgt | rec | yds | short/deep | L/M/R | RZ tgt |','|-|-|-|-|-|-|-|-|']
for (o,r),c in sorted(P.items(),key=lambda x:(x[0][0],-x[1]['tgt'])):
  L.append(f"| {o} | {r} | {c['tgt']} | {c['rec']} | {c['yds']} | {c['short']}/{c['deep']} | {c['left']}/{c['middle']}/{c['right']} | {c['RZ tgt']} |")
L+=['\n**Pass location by offense (attempts, yds)**']
for o,c in LOC.items(): L.append(f"- {o}: "+', '.join(f"{k} {v}att/{c[k+' yds']}y" for k,v in sorted(c.items(),key=lambda x:-x[1]) if not k.endswith('yds')))
L+=['\n**Pressure proxies (PBP text only; live blitz/zone % NOT publicly available)**']
for o,c in PR.items(): L.append(f"- {o} offense: {dict(c)}")
open('live_log.md','a').write('\n'.join(L)+'\n');print('\n'.join(L))
