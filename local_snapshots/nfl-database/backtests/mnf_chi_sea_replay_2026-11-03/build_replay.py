"""MNF CHI@SEA (Nov 2 2026) replay at FanDuel 16:38 ET prices (r3 odds_m1638) under the fixed rules.
Template = backtests/rulebook_replay_wk6_8/runs/wk9_CHI_SEA (leak-free point-in-time fields: form, coverage, depth, scheme_edge).
Replaced: line/price/no_vig with FanDuel m1638, sims with a re-run of CURRENT tools/sim_v6.py (3x100k, seed 20261101) on a scratch copy of r3/src
(+Kalif Raymond). Added: FanDuel alt-over rungs for Loveland, Burden, Odunze, Raymond (rec + yds) with a PROXY no-vig (alt implied / FD main overround).
Mirror overs = both sides of every main line are built. Gate = real tools/run_gate.py in-process, rules forced active (harness monkeypatch, no tool file edited)."""
import os,sys,json,copy,shutil,re
from datetime import datetime,timedelta
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT='/workspace/nfl-database'
TPL=f'{ROOT}/backtests/rulebook_replay_wk6_8/runs/wk9_CHI_SEA'; RUN=f'{HERE}/run'
S=json.load(open(f'{HERE}/sims_m1638_current_simv6.json'))['sims']; LG={(l['player'],l['market']):l for l in json.load(open('/tmp/mnf/replay/run/src/legs_m1638.json'))}
MOD={'mc':'monte_carlo','bias':'bias','gr':'game_randomness'}
imp=lambda a:(100/(a+100)) if a>0 else (-a/(-a+100))
ALTP={'Colston Loveland','Luther Burden III','Rome Odunze','Kalif Raymond','Jaxon Smith-Njigba','Cooper Kupp','AJ Barner',"D'Andre Swift",'Roschon Johnson'}  # 4 asked-for players + every player on Rico's slips that has FD alts
os.makedirs(RUN,exist_ok=True)
for f in ('checklist.md','report.md'): shutil.copy(f'{TPL}/{f}',RUN)
m=json.load(open(f'{TPL}/run_manifest.json')); CK=open(f'{TPL}/checklist.md').read().splitlines()
hdr=[x for x in CK[:2]]; rows={}
for x in CK[2:]:
    c=x.split('|');
    if len(c)>3: rows.setdefault(c[1].strip(),[]).append(x)
def simp(key,line,side):
    s=S[key]['sims']; out={}
    for k,mn in MOD.items():
        r=s[k]['rungs']; po=r.get(str(float(line)))
        if po is None: return None
        out[mn]=dict(p=round(po if side=='over' else 1-po,4),median=round(float(s[k]['median']),2))
    return out
def form_trend(L,line):
    v=L['recent_form']['values']; import numpy as np
    if len(v)<2: return False,'fewer than 2 current-QB games'
    l2,l4=np.mean(v[-2:]),np.mean(v[-4:]); ok=(l2>=l4 and l2>line) if L['side']=='over' else (l2<=l4 and l2<line)
    return bool(ok),f'last2 {l2:.1f} vs last4 {l4:.1f} vs line {line:g}'
def retag(L,line,price,nv,note,rung,book='fanduel'):
    L=copy.deepcopy(L); old=L['name']; L['line']=float(line); L['price']=float(price); L['no_vig']=round(nv,4); L['no_vig_note']=note; L['book']=book; L['rung']=rung
    L['name']=f"{L['player']} {L['market']} {L['side']} {line:g}"+('' if rung=='main' else f' [{rung}]')
    se=L.get('scheme_edge')
    if se:
        ok,d=form_trend(L,float(line)); se['form_trend'].update(ok=ok,detail=d); se.pop('explanation',None)
        keys=('matchup','scheme_fit','script','form_trend')
        if all(se[k]['ok'] for k in keys): se['explanation']='AUTO-GENERATED (replay harness, not analyst): '+'; '.join(se[k]['detail'] for k in keys)+'.'
    return old,L
legs=[];sims={mn:{} for mn in MOD.values()};ck=[];tplsim={x['model']:x['legs'] for x in m['sims']}
for L in m['legs']:
    key=f"{L['player']}|{L['market']}"; fd=LG.get((L['player'],L['market']),{}).get('fd')
    if key in S and fd:
        o,L2=retag(L,fd['point'],fd['over'] if L['side']=='over' else fd['under'],fd['nv_over'] if L['side']=='over' else fd['nv_under'],'FanDuel two-way no-vig (r3 odds_m1638, 16:38 ET)','main')
        sp=simp(key,fd['point'],L['side'])
    else:
        o,L2=L['name'],copy.deepcopy(L); sp={mn:tplsim[mn][o] for mn in MOD.values()}; L2['no_vig_note']+=' [not on FD m1638 / no re-sim: harness consensus line+sim kept]'
    if sp is None: print('nosim',key); continue
    legs.append(L2); [sims[mn].__setitem__(L2['name'],sp[mn]) for mn in sp]
    ck+=[r.replace(f'| {o} |',f"| {L2['name']} |",1) for r in rows[o]]
    # alt-over rungs
    if L['side']=='over' and L['player'] in ALTP and fd and key in S:
        ovr=fd['overround']
        for pt,pr in sorted(LG[(L['player'],L['market'])]['alts'].items(),key=lambda x:float(x[0])):
            pt=float(pt)
            if pt==fd['point']: continue
            rung='low' if pt<fd['point'] else 'high'
            o2,L3=retag(L,pt,pr,min(imp(pr)/ovr,0.99),'PROXY: FanDuel one-sided alt, FD main-line overround removed',rung)
            sp=simp(key,pt,'over')
            if sp is None: print('no sim rung',key,pt); continue
            legs.append(L3); [sims[mn].__setitem__(L3['name'],sp[mn]) for mn in sp]; ck+=[r.replace(f'| {o} |',f"| {L3['name']} |",1) for r in rows[o]]
m['legs']=legs; m['sims']=[dict(model=mn,n=100000,seed=20261101,legs=v,script='tools/sim_v6.py',note='current sim_v6 (post-6322cc5) re-run on scratch copy of r3/src') for mn,v in sims.items()]
m['source_note']='FD m1638 replay of MNF CHI@SEA; see build_replay.py'
json.dump(m,open(f'{RUN}/run_manifest.json','w'),indent=1,default=str); open(f'{RUN}/checklist.md','w').write('\n'.join(hdr+ck)+'\n')
print('legs',len(legs))
