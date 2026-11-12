import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V
V.SEED=20261101
E=V.Engine()
o,info=E.sim(dict(player='Rome Odunze',team='CHI',opp='SEA',market='rec',spread=3.0,rungs=[1.5,2.5,3.5]))
for m in ('mc','bias','gr'): print(m,round(o[m]['median'],2),{k:round(v,4) for k,v in o[m]['rungs'].items()})
print('info',{k:v for k,v in info.items() if not isinstance(v,(list,dict))})
json.dump(dict(tag="fixed-model, copies only",src=V.SRC,seed=V.SEED,n=V.N,out=o,info=info),open('raw_odunze.json','w'),indent=1,default=float)
