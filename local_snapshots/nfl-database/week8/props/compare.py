"""Compare FD props to full.json projections. Method: lognormal per market, median = model median,
25th/75th pct = median x (player lo/tot, hi/tot) from his Wks1-7 rush+rec game spread; sigma floor from typical NFL prop dispersion: rec yds 0.55, rush 0.40, rush+rec 0.40, receptions 0.40.
P(over line) = 1-Phi((ln line - ln med)/sigma). Updates in proj_overrides.json are applied first."""
import json,math,csv,os
W='/workspace/nfl-database/week8/'
F=json.load(open(W+'breakdown/full/full.json')); P=json.load(open(W+'props/props.json'))
OV=json.load(open(W+'props/proj_overrides.json')) if os.path.exists(W+'props/proj_overrides.json') else {}
GID={'LAC@LAR':'LAC@LA','PHI@WSH':'PHI@WAS'}
PL={}
for g in F['games']:
    for t in g['teams']:
        for p in t['players']: PL[(g['id'],p['name'])]=(p,t)
MK={'rec_yds':'recyds','receptions':'rec','rush_yds':'rushyds','rush_rec_yds':'tot'}
Phi=lambda z:0.5*(1+math.erf(z/math.sqrt(2)))
def imp(o):
    if o in('',None): return None
    o=int(o); return 100/(o+100) if o>0 else -o/(-o+100)
def pover(med,line,rlo,rhi,mk):
    if med<=0: return 0.0
    s=max((math.log(max(rhi,1.01))-math.log(max(rlo,.05)))/1.349,{'receptions':0.40,'rec_yds':0.55,'rush_yds':0.40,'rush_rec_yds':0.40}[mk])
    return 1-Phi((math.log(max(line,.01))-math.log(med))/s)
import pandas as pd,re
SN=pd.read_parquet('/workspace/nfl-database/fixes/src/snap_counts_2026.parquet')
nrm=lambda n:re.sub(r'[^a-z]','',re.sub(r'\b(jr|sr|ii|iii|iv)\b\.?','',n.lower()))
GP={}
for k,o in zip(SN.player.map(nrm),SN.offense_snaps):
    if (o or 0)>0: GP[k]=GP.get(k,0)+1
rows=[];td=[]
for r in P['rows']:
    gid=GID.get(r['game'],r['game']); k=(gid,r['player'])
    if r['market']=='anytime_td':
        if k in PL:
            p,t=PL[k]; td.append(dict(game=r['game'],player=r['player'],team=t['team'],pos=p['pos'],fd_odds=r['over_odds'],fd_implied=round(imp(r['over_odds'])*100,1) if r['over_odds'] not in('',None) else None,rz=p['rz'],q=p['q']))
        continue
    if r['market'] not in MK or k not in PL or r['line']=='': continue
    p,t=PL[k]; pr=dict(p['proj']); pr.update(OV.get(f"{gid}|{p['name']}",{}).get('proj',{}))
    med=pr[MK[r['market']]]; tot=max(pr['tot'],1)
    rlo=pr['lo']/tot if pr['tot'] else .6; rhi=pr['hi']/tot if pr['tot'] else 1.4
    line=float(r['line']); po=pover(med,line,rlo,rhi,r['market'])
    io=imp(r['over_odds']); iu=imp(r['under_odds']); fair=io/(io+iu) if io and iu else io
    edge=round(med-line,1); ep=round(100*(med-line)/line,1) if line else None
    volatile=rhi/max(rlo,.05)>2.2
    # lean
    lean='NO BET'; why=[]
    if po>=0.60 and ep>=10: lean='LEAN OVER'
    elif po<=0.40 and ep<=-10: lean='LEAN UNDER'
    if not p['gate'] and lean=='LEAN OVER': lean='NO BET'; why.append('fails opportunity gate')
    if p.get('verdict')=='NO' and lean=='LEAN OVER' and 'A:' not in OV.get(f"{gid}|{p['name']}",{}).get('why',''): lean='NO BET'; why.append('production verdict NO')
    if t['script']=='underdog' and abs(float(F and 0) or 0)>0: pass
    gp=GP.get(nrm(p['name']))
    if gp is not None and gp<3 and lean!='NO BET': lean='NO BET'; why.append(f'sample: {gp} game(s) with snaps')
    if f"{gid}|{p['name']}" in OV: why.append('projection updated (see PROJECTION_UPDATES.md)')
    if p['q']: why.append('QUESTIONABLE: low alt rung or fade, confirm at 90-min inactives')
    if volatile: why.append('volatile yards: moderate rung')
    rung=''
    if lean=='LEAN OVER' and r['alt']:
        tgt=0.80 if (p['q'] or volatile) else 0.68
        cands=[(a,o) for a,o in r['alt'] if o is not None and pover(med,a-0.5,rlo,rhi,r['market'])>=tgt and pover(med,a-0.5,rlo,rhi,r['market'])>imp(o) and o>=-250]
        if cands:
            a,o=max(cands,key=lambda x:x[0]); rung=f"{a}+ ({'+' if o>0 else ''}{o}), model P {round(100*pover(med,a-0.5,rlo,rhi,r['market']))}%"
        else: rung='main line only (no alt rung clears model P/price)'
    elif lean=='LEAN OVER': rung='main line (no alt ladder posted)'
    elif lean=='LEAN UNDER': rung='main line under (FD posts no alt unders)'
    rows.append(dict(game=r['game'],team=t['team'],player=p['name'],pos=p['pos'],q=p['q'],gate=p['gate'],verdict=p.get('verdict'),market=r['market'],
        fd_line=line,fd_over=r['over_odds'],fd_under=r['under_odds'],dk_line='n/a',dk_odds='n/a',median=med,lo=round(med*rlo,1),hi=round(med*rhi,1),
        edge=edge,edge_pct=ep,p_over=round(po,3),fd_fair_over=round(fair,3) if fair else None,lean=lean,rung=rung,notes='; '.join(why),
        alt=' '.join(f"{a}+:{o}" for a,o in r['alt']),overridden=f"{gid}|{p['name']}" in OV))
rows.sort(key=lambda x:-abs(x['edge_pct'] or 0))
json.dump(dict(method=__doc__,rows=rows,anytime_td=td),open(W+'props/compare.json','w'),indent=1)
with open(W+'props/compare.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows),'compared;',sum(r['lean']!='NO BET' for r in rows),'leans;',len(td),'TD rows')
