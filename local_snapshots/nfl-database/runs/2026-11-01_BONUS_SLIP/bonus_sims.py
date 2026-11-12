"""BONUS slip candidates: sim_v6 100k x3 models, seed 20261101; FD spreads from lines_b1149.json (11:49 ET)."""
import sys,json,time; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
E=V.Engine(); R={}
C=[('Javonte Williams','DAL','ARI','rushyds',-7,[49.5,59.5,69.5]),('Bucky Irving','TB','ATL','rushyds',-1.5,[49.5,59.5]),
 ('Chase Brown','CIN','TEN','rushyds',-13.5,[39.5,49.5]),('Jahmyr Gibbs','DET','MIN','rushyds',-3.5,[59.5,69.5,79.5]),
 ('Braelon Allen','NYJ','LV','rushyds',-1.5,[59.5,69.5]),('Kyren Williams','LAR','LAC','rushyds',-6.5,[39.5,49.5]),
 ('Bijan Robinson','ATL','TB','rushyds',1.5,[59.5,69.5]),('James Cook','BUF','BAL','rushyds',-3,[59.5,69.5]),
 ('Derrick Henry','BAL','BUF','rushyds',3,[59.5,69.5]),('Tony Pollard','TEN','CIN','rushyds',13.5,[49.5]),
 ("Ja'Marr Chase",'CIN','TEN','recyds',-13.5,[49.5,59.5]),("Ja'Marr Chase",'CIN','TEN','rec',-13.5,[4.5,5.5]),
 ('Trey McBride','ARI','DAL','rec',7,[4.5,5.5]),('Justin Jefferson','MIN','DET','rec',3.5,[4.5,5.5]),
 ('Garrett Wilson','NYJ','LV','rec',-1.5,[4.5]),('Jonathan Taylor','IND','JAX','rushyds',10.5,[39.5])]
for n,t,o,m,sp,r in C:
    t0=time.time()
    try: out,info=E.sim(dict(player=n,team=t,opp=o,market=m,spread=sp,rungs=r))
    except Exception as ex: R[f'{n}|{m}']=dict(err=str(ex)); print(n,m,'ERR',ex,flush=True); continue
    R[f'{n}|{m}']=dict(sims=out,info=info,spread=sp,team=t,opp=o)
    print(n,m,sp,{k:(round(v['median'],1),{a:round(b,3) for a,b in v['rungs'].items()}) for k,v in out.items()},round(time.time()-t0),flush=True)
R['_meta']=dict(N=V.N,seed=V.SEED,engine='tools/sim_v6.py',calib=V.CALIB_F)
json.dump(R,open('bonus_sims.json','w'),default=float)
