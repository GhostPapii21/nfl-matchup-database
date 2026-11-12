"""Grade Rico's placed slips through the same 15-phase evaluate() at each slip line. Usage: python3 dfs.py <tag> [--suffix X] [--dry]"""
import sys, copy, os, json, numpy as np
import assemble as A
from dfs_legs import SL
LEGS={(l['player'],l['market']):l for l in A.D['legs']}
E=[]; rows=[]
for slip,pl,mk,ln,disp,note in SL:
    tag=slip.split(' (')[0]
    if mk and (pl,mk) in LEGS:
        L=copy.deepcopy(LEGS[(pl,mk)]); L['force']=ln; L['bar']=None; L['explicit']=None
        L['stack']=f"placed: {slip} {disp}"
        r=A.evaluate(L); r['name']=f"[{tag}] {pl} {L['label']} Over {ln:g}"
        if note: r['R'][14]=(r['R'][14][0],r['R'][14][1]+f' | slip note: {note}',r['R'][14][2],r['R'][14][3])
        E.append(r); rows.append((slip,pl,disp,r))
    else:
        nm=f"[{tag}] {pl} {disp}"; why=note or 'no market/sim for this leg'
        R={ph:('N/A',f'not evaluated: {why}','n/a','') for ph in range(1,16)}
        R[14]=('MISSING',f'no sim model: {why}; leg left ungraded (not invented)','sim_v5.py (no model for this market)',A.T['odds'])
        Lm=dict(player=pl,team='',opp='',pos='',market=disp,label=disp,pp=[],ud=[],bar=None,stack=f'placed: {slip}',explicit=None)
        r=dict(name=nm,L=Lm,side='Over',line=ln,price=0,nv=float('nan'),ps=None,meds=None,avg=float('nan'),shr=float('nan'),R=R,bad=[(14,'MISSING',R[14][1])],status='CUT',cov=None,sims=None,info=None,rung_note='n/a',pin=None,dk=None,inj='')
        E.append(r); rows.append((slip,pl,disp,r))
# slip summary section
ex=['','## 5b. Slip grades (placed tickets; joint p assumes independence, which overstates SGP joint p for positively correlated legs and understates nothing else)','']
by={}
for slip,pl,disp,r in rows: by.setdefault(slip,[]).append((pl,disp,r))
for slip,lst in by.items():
    ex.append(f"### {slip}"); ex.append('| Leg | Status | avg p (MC/Bias/GR) | no-vig at rung | phases not PASS |'); ex.append('|---|---|---|---|---|')
    jp=1; unk=0
    for pl,disp,r in lst:
        if r['ps']: jp*=r['avg']; pp=f"{r['avg']:.3f} ({r['ps'][0]:.3f}/{r['ps'][1]:.3f}/{r['ps'][2]:.3f})"
        else: unk+=1; pp='ungraded (no model)'
        nvs='MISSING' if r['nv']!=r['nv'] else f"{r['nv']:.3f}"
        bad='; '.join(f"P{k} {s}" for k,s,m in r['bad']) or 'none'
        ex.append(f"| {pl} {A.clean(disp)} | {'supported' if r['status']=='PASS' else 'not supported (CUT)'} | {pp} | {nvs} | {bad} |")
    ex.append(f"- Joint p of the graded legs (independence): {jp:.3f}" + (f"; {unk} leg(s) ungraded, so the true ticket p is lower" if unk else ''))
    if 'Ticket 2' in slip: ex.append('- Correlation: Pickens 4+ rec and Lamb 60+ yds both need DAL passing; a DAL blowout (DAL -7) hurts both.')
    if '51.50' in slip: ex.append('- Golden leg already HIT (TNF). 3 legs UNKNOWN (no file lists them). Godwin 3+ and Flowers 50+ are brief-only.')
    if '7-leg' in slip: ex.append('- Placed status UNCONFIRMED; Washington 40+ graded anyway. JAX wind 16 mph at kickoff.')
    ex.append('')
teams=sorted({r['L']['team'] for r in E if r['L']['team']}|{r['L']['opp'] for r in E if r['L']['opp']})
g=dict(away='DFS',home='SLIPS',id='multi-game (placed slips)',ko='01:00 PM',venue=None,teams=teams,title='# Rico placed slips — Week 8 grading through the game-script run (Sunday Nov 1, 2026)',extra=ex)
out=('/tmp/dry/' if '--dry' in sys.argv else A.DB+'runs/')+'2026-11-01_DFS_SLIPS'+A.SUF
if os.path.exists(out): print('EXISTS, not overwriting:',out); sys.exit(1)
gt=A.write_game(g,E,out); print(gt)
json.dump([dict(slip=s,player=p,disp=d,status=r['status'],avg=r['avg'],nv=r['nv'],ps=r['ps'],bad=r['bad']) for s,p,d,r in rows],open(A.SH+f'dfs_eval_{A.TAG}{A.SUF}.json','w'),indent=0,default=str)
