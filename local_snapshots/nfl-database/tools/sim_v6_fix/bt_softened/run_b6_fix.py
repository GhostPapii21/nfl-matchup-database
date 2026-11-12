"""B6 softened edges, Wk8 (2026-11-01 runs), real lines. Analysis only.
Aligned = over leg, context checks not failed (no P3/P5/P6/P7/P11/P13/§7/injury FAIL in cut_reasons), §7 3 of last 4 > line, avg p(mc,gr) >= .55.
Softened = aligned and then (a) CUT only for softening/administrative reasons (edge/shrink, MODEL-SUSPECT, cushion, missing price/defender/caption),
or (b) played at an alt rung below main, or (c) shrunk edge <= 0 while the raw edge is >= +3."""
import json, glob, re, numpy as np, pandas as pd, sys
sys.path.insert(0,'/workspace/nfl-database/backtests/rico_common'); import common as C
import importlib.util as _iu
_sp=_iu.spec_from_file_location('sv6fix','/workspace/nfl-database/tools/sim_v6_fix/sim_v6.py'); SV=_iu.module_from_spec(_sp); sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix'); _sp.loader.exec_module(SV)
EFX=SV.Engine(cutoff='2026-11-01',n=20000); _MD={}
def fixmeds(l):
    k=(l['player'],l['market'])
    if k not in _MD:
        try: o,_=EFX.sim(dict(player=l['player'],team=l['team'],opp=l['opp'],market=l['market'],spread=l.get('spread',0))); _MD[k]=[o[m]['median'] for m in ('mc','bias','gr')]
        except Exception as e: _MD[k]=None; print('FIXSIM ERR',k,repr(e)[:100])
    return _MD[k]
sys.path.insert(0,'/workspace/nfl-database/tools'); import press_tier as PT
R='/workspace/nfl-database'; MK={'recyds':'recyds','rec':'rec','rushyds':'ryds','rushrec':'rr','passyds':'pyds'}
act={}
for f in glob.glob(f'{R}/playlogs/2026_wk8/*_box.json'):
    b=json.load(open(f))
    for t,x in b['teams'].items():
        for r in x.get('rushing',[]): a=act.setdefault(r['player'],dict(ryds=0,rec=0,recyds=0,pyds=0)); a['ryds']=float(r['YDS'])
        for r in x.get('receiving',[]): a=act.setdefault(r['player'],dict(ryds=0,rec=0,recyds=0,pyds=0)); a['rec']=float(r['REC']); a['recyds']=float(r['YDS'])
        for r in x.get('passing',[]): a=act.setdefault(r['player'],dict(ryds=0,rec=0,recyds=0,pyds=0)); a['pyds']=float(r['YDS'])
for a in act.values(): a['rr']=a['ryds']+a['recyds']
HARD=re.compile(r'^(P3|P5|P6|P7|P11|P13|§7|P1 |P2 |injury)|FAIL: (under|underdog)|inactive|weather',re.I)
rows=[]; seen=set()
for f in glob.glob(f'{R}/runs/2026-11-01_*/run_manifest.json'):
    m=json.load(open(f)); meds={}
    for s in m['sims']:
        for k,v in s['legs'].items(): meds.setdefault(k,{})[s['model']]=v.get('median')
    for l in m['legs']:
        if l['side']!='over' or l.get('market') not in MK or l['player'] not in act: continue
        key=(l['player'],l['market'],l['line'])
        if key in seen: continue
        seen.add(key)
        cr=l.get('cut_reasons') or []; hard=[c for c in cr if HARD.search(c) and 'FAIL' in c]
        rf=(l.get('recent_form') or {}).get('values') or []; form=len(rf)>=3 and sum(v>l['line'] for v in rf[-4:])>=3
        p=l.get('avg_p_mc_gr'); aligned=(not hard) and form and p is not None and p>=0.55
        if not aligned: continue
        rung=str(l.get('rung')); alt='alt' in rung.lower() and 'below' in rung.lower()
        soft_cut=l['status']=='CUT'
        shr=(l.get('shrunk_mc_gr') or 0)<=0 and (l.get('edge_mc_gr') or 0)>=3
        main=next((b.get('point') for b in (l.get('pinnacle'),l.get('draftkings')) if isinstance(b,dict) and isinstance(b.get('point'),(int,float))),None) if alt else l['line']
        main=main if isinstance(main,(int,float)) else l['line']
        a=act[l['player']][MK[l['market']]]
        md=meds.get(l['name'],{}); ml=[md.get(k) for k in ('monte_carlo','bias','game_randomness')]; ml_old=ml; ml=fixmeds(l) or ml
        ev=PT.evaluate(dict(weather_stop=False,injury_status=l.get('injury_status','Active'),on_inactives=False,sec11_conflict=False,wr_rank=None,
            matchup=True,coverage=bool(l.get('coverage')),script=True,qb=True,form7=form,medians=ml,line=main,side='over'))
        rows.append(dict(run=f.split('/')[-2],leg=l['name'],status=l['status'],kind='alt-rung' if alt else ('cut' if soft_cut else ('shrunk' if shr else 'played-full')),
            p=p,edge=l.get('edge_mc_gr'),shrunk=l.get('shrunk_mc_gr'),line_played=l['line'],line_full=main,actual=a,hit_played=int(a>l['line']),hit_full=int(a>main),
            press=ev['tier'],old_meds=ml_old,new_meds=[round(x,1) for x in ml],press_why=ev['reason'],cut='; '.join(cr)[:160]))
D=pd.DataFrame(rows); D.to_csv('b6_legs.csv',index=False)
S=D[D.kind!='played-full']
lines=["| Leg | Status/kind | p | edge→shrunk | full line | actual | full hit | PRESS? | cut reason |","|---|---|---|---|---|---|---|---|---|"]
for _,r in S.iterrows(): lines.append(f"| {r.leg} | {r.status}/{r.kind} | {r.p:.2f} | {100*r.edge:+.1f}→{100*r.shrunk:+.1f} | {r.line_full} | {r.actual:g} | {'✔' if r.hit_full else '✘'} | {r.press} ({r.press_why}) | {r.cut} |")
st=C.stats(S.hit_full); pr=S[S.press=='PRESS']; sp=C.stats(pr.hit_full); pf=D[D.kind=='played-full']
summ=f"\nSoftened/cut aligned overs graded at full strength: {st['k']}/{st['n']} = {st['hit']:.1%}, ROI −110 {st['roi']:+.1%}, p vs BE {st['p_be']:.2f}.\nOf those, the ones PRESS (k=2) would have tagged went {sp['k']}/{sp['n']}" + (f" = {sp['hit']:.1%}" if sp['n'] else "") + f".\nAligned overs that were played at full strength: {pf.hit_full.sum()}/{len(pf)}."
open('b6_fix.md','w').write("\n".join(lines)+"\n"+summ); print(open('b6_fix.md').read())
