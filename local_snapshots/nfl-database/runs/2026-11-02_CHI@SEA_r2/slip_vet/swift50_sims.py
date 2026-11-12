# Swift 50+ rush+rec. Tag: fixed-model, copies only. sim_v6_fix 3x100k seed 20261101.
import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V
e=V.Engine()
L=dict(player="D'Andre Swift",team='CHI',opp='SEA',market='rushrec',spread=3.0,rungs=[49.5,59.5,81.5],current_qb='Caleb Williams')
s,info=e.sim(L)
print('seed',V.SEED,'n',V.N,'games',info.get('n_games'))
for m in ('mc','bias','gr'): print(m,round(s[m]['median'],1),{k:round(v,3) for k,v in s[m]['rungs'].items()})
json.dump(dict(tag='fixed-model, copies only',src=V.SRC,seed=V.SEED,n=V.N,sims=s,info=info),open('raw_swift50.json','w'),indent=1,default=float)
