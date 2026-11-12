import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V
E=V.Engine();out={}
for pl,mk,r in [('Jaxon Smith-Njigba','recyds',[79.5,89.5,99.5]),('Cooper Kupp','rec',[1.5,2.5]),('AJ Barner','rec',[2.5,3.5,4.5])]+[("D'Andre Swift",'rec',[2.5,3.5])]:
    o,info=E.sim(dict(player=pl,team=('CHI' if 'Swift' in pl else 'SEA'),opp=('SEA' if 'Swift' in pl else 'CHI'),market=mk,spread=(3.0 if 'Swift' in pl else -3.0),rungs=r))
    out[pl+'|'+mk]=dict(sims=o,info=info)
    print(pl,mk,{m:(round(o[m]['median'],1),{k:round(v,3) for k,v in o[m]['rungs'].items()}) for m in ('mc','bias','gr')},'n',info.get('n_games'))
json.dump(dict(src=V.SRC,seed=V.SEED,n=V.N,out=out),open('raw_sims.json','w'),indent=1,default=float)
