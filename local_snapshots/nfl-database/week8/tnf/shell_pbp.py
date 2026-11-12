import json,re,collections,csv,os
d=json.load(open('raw/live_summary_401873023.json'))
seen=set();rows=[]
for dr in d['drives']['previous']:
  for p in dr.get('plays',[]):
    if p['id'] in seen: continue
    seen.add(p['id']);t=p.get('text','')
    m=re.search(r'J\.Love pass (incomplete )?(short|deep) (left|middle|right)(?: (?:to|intended for) ([A-Z]\.[A-Za-z\'-]+))?',t)
    if not m: continue
    inc=bool(m.group(1)) or 'INTERCEPTED' in t
    ym=re.search(r'for (-?\d+) yards',t); y=0 if inc or not ym else int(ym.group(1))
    dm=re.search(r'\(([A-Z]\.[A-Za-z\'-]+)(?:; ([A-Z]\.[A-Za-z\'-]+))?\)',t)
    dfn=[x for x in (dm.groups() if dm else []) if x]
    res='INT' if 'INTERCEPTED' in t else ('DPI-nullified' if 'No Play' in t and 'Interference' in t else ('nullified(GB pen)' if 'No Play' in t else ('inc' if inc else ('TD' if 'TOUCHDOWN' in t else 'rec'))))
    if 'INTERCEPTED' in t: dfn=['Z.Wheatley']
    if 'Interference' in t: dfn=list(dict.fromkeys(dfn+['W.Lee']))
    rows.append(dict(q=p['period']['number'],clk=p['clock']['displayValue'],dd=p.get('start',{}).get('shortDownDistanceText',''),depth=m.group(2),dir=m.group(3),rcv=m.group(4) or '?',yds=y,res=res,dfn='; '.join(dfn) or '—'))
json.dump(rows,open('gb_targets.json','w'),indent=1)
L=['| Q | clk | D&D | rcv | depth | dir | yds | result | named defender |','|-|-|-|-|-|-|-|-|-|']
for r in rows: L.append('| {q} | {clk} | {dd} | {rcv} | {depth} | {dir} | {yds} | {res} | {dfn} |'.format(**r))
L.append('\n| rcv | tgt | rec | yds | L | M | R | short | deep | catches L/M/R |\n|-|-|-|-|-|-|-|-|-|-|')
for who in ['C.Watson','M.Golden','T.Kraft','J.Jacobs','S.Williams','*ALL*']:
  rr=[r for r in rows if who=='*ALL*' or r['rcv']==who]; rr=[r for r in rr if not r['res'].startswith('nullified')]
  c=[r for r in rr if r['res'] in('rec','TD')]
  cnt=lambda s,k,v:sum(x[k]==v for x in s)
  L.append(f"| {who} | {len(rr)} | {len(c)} | {sum(r['yds'] for r in c)} | {cnt(rr,'dir','left')} | {cnt(rr,'dir','middle')} | {cnt(rr,'dir','right')} | {cnt(rr,'depth','short')} | {cnt(rr,'depth','deep')} | {cnt(c,'dir','left')}/{cnt(c,'dir','middle')}/{cnt(c,'dir','right')} |")
open('gb_targets.md','w').write('# GB pass targets vs CAR — ESPN PBP (direction/depth = ESPN charting; defender = tackler/PBU/penalty, NOT coverage)\n\n'+'\n'.join(L)+'\n')
print('\n'.join(L[-8:]))
# defender agg
D=collections.defaultdict(lambda:dict(rec=0,yds=0,exp=0,inc=0,pen=0,intc=0,rcv=collections.Counter()))
for r in rows:
  for x in r['dfn'].split('; '):
    if x=='—':continue
    a=D[x]
    if r['res'] in('rec','TD'): a['rec']+=1;a['yds']+=r['yds'];a['exp']+=r['yds']>=20;a['rcv'][r['rcv']]+=1
    elif r['res']=='INT':a['intc']+=1
    elif 'DPI' in r['res'] or 'Interference' in r['dfn']:a['pen']+=1
    elif r['res']=='inc':a['inc']+=1
json.dump({k:{**v,'rcv':dict(v['rcv'])} for k,v in D.items()},open('car_def_tonight.json','w'),indent=1)
for k,v in sorted(D.items(),key=lambda x:-x[1]['yds']): print(k,v['rec'],v['yds'],v['exp'],'inc',v['inc'],'int',v['intc'],dict(v['rcv']))
