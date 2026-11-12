"""14:35 inactives re-score of PLACED 4 PM ticket legs on sim_v6 (100k x3, seed 20261101), current FD spreads from lines_i1435.json."""
import sys,json; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
E=V.Engine()
LEGS=[('Kenneth Walker III','KC','DEN','rushyds',-1.5,[69.5,97.5]),('Kenneth Walker III','KC','DEN','rushrec',-1.5,[79.5]),
 ('Puka Nacua','LAR','LAC','recyds',-6.5,[59.5,69.5]),('Puka Nacua','LAR','LAC','rec',-6.5,[7.5]),
 ('Kyren Williams','LAR','LAC','rushyds',-6.5,[58.5]),('Patrick Mahomes','KC','DEN','passyds',-1.5,[0.5,220.5])]
R={}
for n,t,o,m,sp,r in LEGS:
    try: out,info=E.sim(dict(player=n,team=t,opp=o,market=m,spread=sp,rungs=r))
    except Exception as ex: R[f'{n}|{m}']=dict(err=str(ex)); print(n,m,'ERR',ex,flush=True); continue
    R[f'{n}|{m}']=dict(sims=out,info=info,spread=sp)
    print(n,m,sp,{k:(round(v['median'],1),v['rungs']) for k,v in out.items()},flush=True)
R['_meta']=dict(N=V.N,seed=V.SEED,engine='tools/sim_v6.py',calib=V.CALIB_F)
json.dump(R,open('rescore_v6_i1435.json','w'),default=float)
