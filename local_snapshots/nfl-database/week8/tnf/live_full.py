#!/usr/bin/env python3
"""Full live state for CAR@GB from ESPN public summary API. Writes live_state.md (overwrite) and appends a short line to live_log.md.
--final also writes the postmortem actuals block + defender_ledger.csv rows. Method notes: defenders = names in PBP parentheses (tackler) or
'pass incomplete ... (Name)' (defended/broke up) or penalty text. PBP does NOT give coverage. YAC not in ESPN public PBP -> n/a."""
import json,re,sys,urllib.request,datetime,collections as C,csv,os
EID='401873023'
d=json.load(urllib.request.urlopen(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={EID}'))
json.dump(d,open(f'raw/live_summary_{EID}.json','w'))
hc=d['header']['competitions'][0];st=hc['status']['type'];det=st['detail']
sc={c['team']['abbreviation']:int(c.get('score',0) or 0) for c in hc['competitors']}
plays=[];seen=set()
for dr in d['drives'].get('previous',[])+([d['drives']['current']] if d['drives'].get('current') else []):
  off=dr['team']['abbreviation']
  for p in dr['plays']:
    if p['id'] in seen: continue
    seen.add(p['id']);plays.append((off,p))
plays.sort(key=lambda x:int(x[1].get('sequenceNumber',0)))
DEF={'CAR':'GB','GB':'CAR'}
PL=C.defaultdict(C.Counter);DL=C.defaultdict(C.Counter);G=C.defaultdict(C.Counter);INJ=[];LED=[];TG=[];WI=[]
NAME=r"([A-Z]\.[A-Za-z\'\-]+(?: (?:Jr|Sr|III|II)\.?)?)"
for off,p in plays:
  tx=p['text'];q=p['period']['number'];s=p.get('start',{});ytg=s.get('yardsToEndzone',99);dn=s.get('down',0);dist=s.get('distance',0)
  dfn=DEF.get(off,'?')
  for m in re.finditer(r'(GB|CAR)-'+NAME+r' was injured',tx): INJ.append(f"Q{q} {p['clock']['displayValue']} {m.group(1)} {m.group(2)}")
  pen=re.findall(r'Penalty on (CAR|GB)-'+NAME+r', ([A-Za-z ]+?)(?:,|\.)',tx)
  for t,n,k in pen:
    if 'Pass Interference' in k or 'Holding' in k and t==dfn: DL[(n,t)]['penalties']+=1;LED.append((n,t,'',0,0,'penalty:'+k.strip()))
  if 'No Play' in tx: continue
  typ=p.get('type',{}).get('text','')
  if 'Kickoff' in typ or 'Punt' in typ or 'Field Goal' in typ or 'Extra Point' in typ or 'Timeout' in typ or 'End ' in typ: continue
  isrun=bool(re.search(r' (left|right|up the middle) (end|tackle|guard)?.*for|up the middle',tx)) and ' pass ' not in tx and 'sacked' not in tx and 'kneels' not in tx
  m=re.search(r'pass (incomplete )?(short|deep)? ?(left|right|middle)? ?(?:to|intended for) '+NAME,tx)
  sack=' sacked ' in tx
  if m or sack or 'scrambles' in tx: G[(off,q)]['pass']+=1
  elif isrun: G[(off,q)]['run']+=1
  else: continue
  lead=sc and 0
  if dn==3:
    G[(off,'all')]['3rd att']+=1
    gain=re.search(r'for (-?\d+) yards?',tx)
    if (gain and int(gain.group(1))>=dist and not (m and m.group(1))) or 'TOUCHDOWN' in tx: G[(off,'all')]['3rd conv']+=1
  if ytg<=20: G[(off,'all')]['RZ plays']+=1
  if sack: G[(off,'all')]['sacks']+=1
  if re.search(r'\bhit\b|pressur|hurr',tx,re.I): G[(off,'all')]['hit/press txt']+=1
  if not m: continue
  inc=bool(m.group(1));intc='INTERCEPT' in tx.upper();r=m.group(4)
  if any(k in tx for k in ('C.Watson was injured',)): WI.append(int(p.get('sequenceNumber',0)))
  TG.append((int(p.get('sequenceNumber',0)),q,p['clock']['displayValue'],off,r,m.group(2) or '?',m.group(3) or '?',not(inc or intc),tx))
  y=re.search(r'for (-?\d+) yards?',tx);y=0 if (inc or intc or not y) else int(y.group(1))
  dep=m.group(2) or '?';c=PL[(off,r)]
  c['tgt']+=1;c[f'Q{q} tgt']+=1;c['rec']+=0 if (inc or intc) else 1;c['yds']+=y;c[dep]+=1
  if ytg<=20: c['RZ tgt']+=1
  if 'TOUCHDOWN' in tx and not inc: c['TD']+=1
  par=re.findall(r'\(([^)]*)\)',tx.split('Penalty')[0])
  names=[n for grp in par for n in re.findall(NAME,grp)]
  for n in names:
    k=DL[(n,dfn)]
    if inc or intc: k['PD/INT']+=1;LED.append((n,dfn,r,0,0,'defended (pass incomplete/INT credit)'))
    else: k['rec after']+=1;k['yds after']+=y;k[dep]+=1;LED.append((n,dfn,r,1,y,'tackler after catch'))
    if not (inc or intc) and y>=15: k['beaten 15+ (tackler)']+=1
now=datetime.datetime.now().strftime('%I:%M %p ET')
O=[f'# CAR@GB live state — {now} — GB {sc.get("GB")} CAR {sc.get("CAR")} — {det}\n','Method: PBP text only. Defender = tackler / pass-defensed credit / penalty; NOT coverage. YAC: n/a in public PBP.\n',
'## Players','| off | player | tgt | rec | catch% | yds | TD | short/deep | RZ tgt | Q1/Q2/Q3/Q4 tgt |','|-|-|-|-|-|-|-|-|-|-|']
for (o,r),c in sorted(PL.items(),key=lambda x:(x[0][0],-x[1]['tgt'])):
  O.append(f"| {o} | {r} | {c['tgt']} | {c['rec']} | {c['rec']/c['tgt']:.0%} | {c['yds']} | {c['TD']} | {c['short']}/{c['deep']} | {c['RZ tgt']} | {c['Q1 tgt']}/{c['Q2 tgt']}/{c['Q3 tgt']}/{c['Q4 tgt']} |")
O+=['\n## Defender ledger (team = defense)','| defender | team | rec after | yds after | short/deep | 15+ as tackler | PD/INT | DPI/hold |','|-|-|-|-|-|-|-|-|']
for (n,t),k in sorted(DL.items(),key=lambda x:-x[1]['yds after']):
  O.append(f"| {n} | {t} | {k['rec after']} | {k['yds after']} | {k['short']}/{k['deep']} | {k['beaten 15+ (tackler)']} | {k['PD/INT']} | {k['penalties']} |")
O+=['\n## Game script','| off | Q | run | pass | pass% |','|-|-|-|-|-|']
for o in ('GB','CAR'):
  for q in (1,2,3,4,5):
    g=G[(o,q)];t=g['run']+g['pass']
    if t: O.append(f"| {o} | {q} | {g['run']} | {g['pass']} | {g['pass']/t:.0%} |")
for o in ('GB','CAR'): O.append(f"- {o}: {dict(G[(o,'all')])}")
O.append('- Injuries (PBP): '+('; '.join(INJ) or 'none'))
# proj vs actual
box=C.defaultdict(dict)
for t in d['boxscore'].get('players',[]):
  for s in t['statistics']:
    for a in s['athletes']: box[a['athlete']['displayName']][s['name']]=dict(zip(s['labels'],a['stats']))
cmp=json.load(open('tnf_compare.json'))['main']
def act(pl,stat):
  b=box.get(pl,{});rec=b.get('receiving',{});ru=b.get('rushing',{})
  f=lambda x:float(x) if x not in (None,'') else 0
  return {'rec':f(rec.get('REC')),'recyds':f(rec.get('YDS')),'rushyds':f(ru.get('YDS')),'rr':f(rec.get('YDS'))+f(ru.get('YDS'))}.get(stat)
LEANS={('Darren Waller','rec'):'U2.5',('Tucker Kraft','rec'):'U4.5',('Savion Williams','rec'):'U2.5',('Jalen Coker','recyds'):'U62.5',('Christian Watson','rec'):'U4.5'}
O+=['\n## Projection vs actual (FD line; lo/med/hi from proj.py)','| player | stat | line | lo | med | hi | actual | lean | result |','|-|-|-|-|-|-|-|-|-|']
PV=[]
for r in cmp:
  if r['player'] not in box and act(r['player'],r['stat']) is None: continue
  a=act(r['player'],r['stat'])
  if a is None: continue
  ln=LEANS.get((r['player'],r['stat']),'');res=''
  if ln: res=('WIN' if a<r['line'] else 'LOSS') if st['completed'] else ('on track' if a<r['line'] else 'LOST')
  PV.append((r,a,ln,res))
  O.append(f"| {r['player']} | {r['stat']} | {r['line']} | {r['lo']} | {r['median']} | {r['hi']} | {a:g} | {ln} | {res} |")
EX=[]
for off,p in plays:
  tx=p['text'];y=re.search(r'for (\d+) yards',tx)
  if 'No Play' in tx or 'incomplete' in tx or not y or re.search('kick|punt',tx,re.I): continue
  y=int(y.group(1));ps=' pass ' in tx
  if (ps and y>=20) or (not ps and 'sacked' not in tx and y>=10): EX.append(f"| Q{p['period']['number']} {p['clock']['displayValue']} | {off} | {'pass' if ps else 'run'} | {y} | {tx[:160]} |")
O+=['\n## Explosives (pass 20+, run 10+; parens = tackler)','| time | off | type | yds | text |','|-|-|-|-|-|']+EX
wi=WI[0] if WI else None
O+=['\n## Low-target WRs (snaps: not in public ESPN feed -> n/a)']
for who in ('J.Coker','M.Golden','C.Watson'):
  t=[x for x in TG if x[4]==who]
  byq=C.Counter(x[1] for x in t)
  near=[re.findall(NAME,' '.join(re.findall(r'\(([^)]*)\)',x[8].split('Penalty')[0]))) for x in t]
  pre=sum(1 for x in t if wi and x[0]<=wi);post=sum(1 for x in t if wi and x[0]>wi)
  O.append(f"- {who}: tgt by Q {dict(sorted(byq.items()))}; rec {sum(x[7] for x in t)}; locs {[x[5]+' '+x[6] for x in t]}; defenders named (tackler/PD, not coverage) {near}; tgt before/after Watson injury {pre}/{post}")
O+=['\n## Watson-exit target redistribution (pre/post injury play)']
for who in ('M.Golden','T.Kraft','S.Williams','J.Jacobs','M.Lloyd','Bo Melton'):
  t=[x for x in TG if x[4]==who and x[3]=='GB']
  if wi: O.append(f"- {who}: pre {sum(x[0]<=wi for x in t)} tgt / post {sum(x[0]>wi for x in t)} tgt (post rec {sum(x[7] for x in t if x[0]>wi)})")
def B(n,cat,k):
  try: return float(box[n][cat][k])
  except: return 0.0
tot=sum(sc.values());gbw=sc.get('GB',0)>sc.get('CAR',0)
LEGS=[('Golden 70+ rec yds',B('Matthew Golden','receiving','YDS'),70),('Kraft 30+ rec yds',B('Tucker Kraft','receiving','YDS'),30),('Hubbard 50+ rush yds',B('Chuba Hubbard','rushing','YDS'),50),
('M.Lloyd 10+ rush yds',B('MarShawn Lloyd','rushing','YDS'),10),('Golden 5+ rec',B('Matthew Golden','receiving','REC'),5),('Savion 2+ rec',B('Savion Williams','receiving','REC'),2),
('Kraft 5+ rec',B('Tucker Kraft','receiving','REC'),5),('Over 44.5',tot,44.5),('McMillan 3+ rec',B('Tetairoa McMillan','receiving','REC'),3)]
O+=['\n## User SGP (FD +922, $28)','| leg | now | need | status |','|-|-|-|-|']
for n,v,need in LEGS: O.append(f"| {n} | {v:g} | {need} | {'HIT' if v>=need else ('FAIL' if st['completed'] else 'pending')} |")
O.append(f"| GB ML | GB {sc.get('GB')}-{sc.get('CAR')} | win | {('HIT' if gbw else 'FAIL') if st['completed'] else ('leading' if gbw else 'trailing/tied')} |")
open('live_state.md','w').write('\n'.join(O)+'\n')
open('live_log.md','a').write(f"\n- {now} GB {sc.get('GB')} CAR {sc.get('CAR')} {det} — full table in live_state.md\n")
if st['completed'] and '--final' in sys.argv:
  fn='/workspace/nfl-database/defender_ledger.csv';new=not os.path.exists(fn)
  with open(fn,'a',newline='') as f:
    w=csv.writer(f)
    if new: w.writerow(['date','game','defender','team','pos','receiver','rec','yds','method'])
    for n,t,r,rc,y,mth in LED: w.writerow(['2026-10-29','CAR@GB',n,t,'',r,rc,y,mth])
  json.dump([dict(player=r['player'],stat=r['stat'],line=r['line'],lo=r['lo'],med=r['median'],hi=r['hi'],actual=a,lean=ln,result=res) for r,a,ln,res in PV],open('final_actuals.json','w'),indent=1)
print('\n'.join(O)); print('COMPLETED' if st['completed'] else 'LIVE')
