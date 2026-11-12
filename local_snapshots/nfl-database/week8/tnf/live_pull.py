#!/usr/bin/env python3
"""Live CAR@GB pull (ESPN public summary API). Usage: python3 live_pull.py [event_id]
Appends a timestamped snapshot to live_log.md. 'Tackler' = name(s) in parentheses in ESPN play text (NOT coverage)."""
import json,re,sys,urllib.request,datetime,collections
EID=sys.argv[1] if len(sys.argv)>1 else '401873023'
d=json.load(urllib.request.urlopen(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={EID}'))
json.dump(d,open(f'raw/live_summary_{EID}.json','w'))
hc=d['header']['competitions'][0]; st=hc['status']['type']['detail']
score=' '.join(f"{c['team']['abbreviation']} {c.get('score','?')}" for c in hc['competitors'])
pos={}
for t in d.get('boxscore',{}).get('players',[]):
  for s in t['statistics']:
    for a in s['athletes']: pos[a['athlete']['displayName']]=t['team']['abbreviation']
rows=[];seen=set()
for dr in d.get('drives',{}).get('previous',[])+([d['drives']['current']] if d.get('drives',{}).get('current') else []):
  off=dr.get('team',{}).get('abbreviation','?')
  for p in dr.get('plays',[]):
    tx=p.get('text','')
    if p.get('id') in seen: continue
    seen.add(p.get('id'))
    m=re.search(r'pass (?:short|deep)?\s*(?:left|right|middle)? ?to ([A-Z]\.[\w\'-]+(?: (?:Jr|III|II)\.?)?).*?for (-?\d+|no gain)',tx)
    if not m or 'incomplete' in tx.lower(): continue
    yd=0 if m.group(2)=='no gain' else int(m.group(2))
    tk=re.search(r'for (?:-?\d+ yards?|no gain)[^(]*\(([^)]*)\)',tx)
    tk=tk.group(1) if tk else ('TD/oob/none' if 'TOUCHDOWN' in tx or 'out of bounds' in tx else 'none')
    rows.append(dict(q=p['period']['number'],clock=p['clock']['displayValue'],off=off,dd=p.get('start',{}).get('downDistanceText',''),rec=m.group(1),yds=yd,tackler=tk,text=tx))
now=datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p ET')
L=[f'\n## Snapshot {now} — {score} — {st}\n','| Q | clock | off | down | receiver | yds | tackler (per PBP text; not coverage) |','|-|-|-|-|-|-|-|']
for r in rows: L.append(f"| {r['q']} | {r['clock']} | {r['off']} | {r['dd']} | {r['rec']} | {r['yds']} | {r['tackler']} |")
D=collections.defaultdict(lambda:[0,0])
for r in rows:
  for t in re.split(r'[;,] ?',r['tackler']):
    if t and t not in('none','TD/oob/none'): D[(t.strip(),r['off'])][0]+=1; D[(t.strip(),r['off'])][1]+=r['yds']
L+=['\n**Tacklers after catches (defense = opponent of "off")**\n','| tackler | vs offense | catches | yds |','|-|-|-|-|']
for (t,o),(c,y) in sorted(D.items(),key=lambda x:-x[1][1]): L.append(f'| {t} | {o} | {c} | {y} |')
B=[]
for t in d.get('boxscore',{}).get('players',[]):
  for s in t['statistics']:
    if s['name'] in('receiving','rushing'):
      for a in s['athletes']: B.append(f"{t['team']['abbreviation']} {s['name']} {a['athlete']['displayName']}: "+' '.join(f'{k}={v}' for k,v in zip(s['labels'],a['stats'])))
L+=['\n**Box**\n']+['- '+b for b in B]
open('live_log.md','a').write('\n'.join(L)+'\n'); print('\n'.join(L))
