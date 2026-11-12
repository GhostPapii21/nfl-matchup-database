"""CHI@SEA Nov 2 2026 r3 (16:38 ET reprice): price candidate legs with tools/sim_v6.py (3 models x 100k, seed 20261101). Reads odds_m0505.csv (FanDuel main+alts).
Run with SIMV6_SRC=<this folder>. Writes legs.json + sims.json. Does not modify any pipeline/sim code."""
import os,sys,json,pandas as pd,numpy as np
SH=os.path.dirname(os.path.abspath(__file__))+'/'; sys.path.insert(0,'/workspace/nfl-database/tools')
assert os.environ.get('SIMV6_SRC','').rstrip('/')==SH.rstrip('/'), 'set SIMV6_SRC to this folder'
import sim_v6 as V
TAG=sys.argv[1] if len(sys.argv)>1 else 'm0505'
O=pd.read_csv(SH+f'odds_{TAG}.csv'); O=O[O.inplay==False]
MK={'passyds':'player_pass_yds','recyds':'player_reception_yds','rec':'player_receptions','rushyds':'player_rush_yds','rushrec':'player_rush_reception_yds','comp':'player_pass_completions'}
SPREAD={'CHI':3.5,'SEA':-3.5}  # FD 16:38 ET: SEA -3.5 (-102), total 46.5
C=[('Caleb Williams','CHI','QB','passyds'),('Luther Burden III','CHI','WR','recyds'),('Luther Burden III','CHI','WR','rec'),
   ('Rome Odunze','CHI','WR','recyds'),('Rome Odunze','CHI','WR','rec'),('Colston Loveland','CHI','TE','recyds'),('Colston Loveland','CHI','TE','rec'),
   ("D'Andre Swift",'CHI','RB','rushyds'),("D'Andre Swift",'CHI','RB','rushrec'),("D'Andre Swift",'CHI','RB','recyds'),("D'Andre Swift",'CHI','RB','rec'),
   ('Roschon Johnson','CHI','RB','rushyds'),
   ('Sam Darnold','SEA','QB','passyds'),('Jaxon Smith-Njigba','SEA','WR','recyds'),('Jaxon Smith-Njigba','SEA','WR','rec'),
   ('Cooper Kupp','SEA','WR','recyds'),('Cooper Kupp','SEA','WR','rec'),('AJ Barner','SEA','TE','recyds'),('AJ Barner','SEA','TE','rec'),
   ('Emanuel Wilson','SEA','RB','rushyds')]
imp=lambda a:(100/(a+100)) if a>0 else (-a/(-a+100))
def book(b,pl,mk):
    x=O[(O.book==b)&(O.player==pl)&(O.market==MK[mk])]
    if not len(x): return None
    o=x[x.side=='Over'].set_index('point').price; u=x[x.side=='Under'].set_index('point').price; both=sorted(set(o.index)&set(u.index))
    if not both: return None
    pt=min(both,key=lambda q:abs(imp(o[q])-imp(u[q]))); ov=imp(o[pt])+imp(u[pt])
    return dict(point=float(pt),over=int(o[pt]),under=int(u[pt]),overround=ov,nv_over=imp(o[pt])/ov,nv_under=imp(u[pt])/ov,last_update_utc=str(x.last_update_utc.max()))
legs=[];E=V.Engine(); out={}
for pl,tm,pos,mk in C:
    fd=book('fanduel',pl,mk); 
    if not fd: print('NOLINE',pl,mk); continue
    al=O[(O.book=='fanduel')&(O.player==pl)&(O.market==MK[mk]+'_alternate')&(O.side=='Over')]
    alts={str(float(r.point)):int(r.price) for r in al.itertuples()}
    L=dict(player=pl,team=tm,opp='SEA' if tm=='CHI' else 'CHI',pos=pos,market=mk,spread=SPREAD[tm],fd=fd,alts=alts,
           dk=book('draftkings',pl,mk),pin=book('pinnacle',pl,mk))
    rungs=sorted(set([fd['point']]+[float(a) for a in alts]+[x['point'] for x in (L['dk'],L['pin']) if x]))
    leg=dict(player=pl,team=tm,opp=L['opp'],market=mk,spread=SPREAD[tm],rungs=rungs)
    try: o,info=E.sim(leg)
    except Exception as e: print('SIMFAIL',pl,mk,e); L['simfail']=str(e); legs.append(L); continue
    out[f'{pl}|{mk}']=dict(sims=o,info=info,rungs=rungs); legs.append(L)
    print(f"{pl:20s} {mk:8s} FD {fd['point']} {fd['over']}/{fd['under']} nvO {fd['nv_over']:.3f} | med mc/bias/gr {o['mc']['median']:.1f}/{o['bias']['median']:.1f}/{o['gr']['median']:.1f} | pO {o['mc']['rungs'][str(fd['point'])]:.3f}/{o['bias']['rungs'][str(fd['point'])]:.3f}/{o['gr']['rungs'][str(fd['point'])]:.3f} n{info['n_games']}")
# RB fix A (Monangai OUT -> Roschon Johnson) and fix F/trigger inputs
ypc={t:V.opp_rb_ypc(E,t) for t in ('CHI','SEA')}
rj=[l for l in legs if l['player']=='Roschon Johnson']
fixA=None
if rj:
    L=rj[0]; fixA=V.promote_rb(E,dict(team='CHI',opp='SEA',spread=3.5,injured='Kyle Monangai',rb2='Roschon Johnson',market='rushyds',line=L['fd']['point'],no_vig=L['fd']['nv_over'],opp_ypc=ypc['SEA']))
    print('fixA',{k:fixA[k] for k in ('p','median','carry_boost','share_new','soft_run_d')})
trig={t:V.rb_script_trigger(SPREAD[t] if SPREAD[t]<0 else None,ypc['SEA' if t=='CHI' else 'CHI'],False) for t in SPREAD}
# fix E: SEA backfield split (Charbonnet back from injury, no 2026 games -> only Wilson/Holani priceable)
ew=[l for l in legs if l['player']=='Emanuel Wilson']
fixE=V.split_reprice(E,dict(team='SEA',opp='CHI',spread=-3.5,opp_ypc=ypc['CHI'],backs=[dict(player='Emanuel Wilson',line=ew[0]['fd']['point'],no_vig=ew[0]['fd']['nv_over'])])) if ew else None
if fixE: print('fixE',json.dumps(fixE['backs'][0])[:600])
meta=dict(script='tools/sim_v6.py',seed=V.SEED,n=V.N,src=SH,odds_tag=TAG,opp_rb_ypc=ypc,rb_script_trigger=trig,fixA=fixA,fixE=fixE,soft_run_d={t:V.soft_run_d_boost(ypc[t]) for t in ypc})
json.dump(dict(meta=meta,sims=out),open(SH+f'sims_{TAG}.json','w'),indent=0,default=float)
json.dump(legs,open(SH+f'legs_{TAG}.json','w'),indent=0)
print('trig',trig,'ypc',ypc)
