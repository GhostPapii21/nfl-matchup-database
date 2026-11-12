# leftover vet sims: sim_v6_fix unedited, 3x100k, seed per engine. Tag: copies only.
import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V
e=V.Engine();out={}
legs=[('Sam Darnold','SEA','CHI','passyds',-3.0,[224.5,238.5],'Sam Darnold',1.0),
('Caleb Williams','CHI','SEA','passyds',3.0,[174.5,227.5],'Caleb Williams',1.0),
('Jaxon Smith-Njigba','SEA','CHI','recyds',-3.0,[59.5,99.5],'Sam Darnold',1.0),
('Jaxon Smith-Njigba','SEA','CHI','rec',-3.0,[6.5,7.5],'Sam Darnold',1.0),
("D'Andre Swift",'CHI','SEA','recyds',3.0,[14.5,21.5],'Caleb Williams',1.0),
('Cooper Kupp','SEA','CHI','rec',-3.0,[1.5,2.5],'Sam Darnold',1.0),
('Emanuel Wilson','SEA','CHI','rushyds',-3.0,[22.5],None,1.0),
('Emanuel Wilson','SEA','CHI','rushyds',-3.0,[22.5],None,0.45*27/17.2),
('Emanuel Wilson','SEA','CHI','rushyds',-3.0,[22.5],None,0.28*27/17.2)]
for pl,t,o,mk,sp,r,cq,cb in legs:
    L=dict(player=pl,team=t,opp=o,market=mk,spread=sp,rungs=r,current_qb=cq)
    if cb!=1.0: L['carry_boost']=cb
    try: s,info=e.sim(L)
    except Exception as ex: print(pl,mk,'ERR',ex); continue
    k=f'{pl}|{mk}|cb{cb:.3f}'; out[k]=s
    print(k,{m:(round(s[m]['median'],1),{kk:round(v,3) for kk,v in s[m]['rungs'].items()}) for m in ('mc','bias','gr')})
json.dump(dict(src=V.SRC,seed=V.SEED,n=V.N,out=out),open('raw_sims.json','w'),indent=1,default=float)
