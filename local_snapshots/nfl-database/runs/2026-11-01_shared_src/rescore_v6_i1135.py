"""11:35 inactives re-score of PLACED 1 PM ticket legs on sim_v6 (100k x3, seed 20261101), current FD spreads from lines_i1135.json."""
import sys,json; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
E=V.Engine()
LEGS=[('Tee Higgins','CIN','TEN','rec',-13.5,[3.5]),('Tee Higgins','CIN','TEN','recyds',-13.5,[49.5,68.5]),
 ('CeeDee Lamb','DAL','ARI','rec',-7,[4.5,6.5]),('CeeDee Lamb','DAL','ARI','recyds',-7,[49.5,59.5]),
 ('Brock Bowers','LV','NYJ','recyds',1.5,[49.5]),('Amon-Ra St. Brown','DET','MIN','rec',-3.5,[5.5,6.5]),
 ('Amon-Ra St. Brown','DET','MIN','recyds',-3.5,[49.5,59.5]),('Zay Flowers','BAL','BUF','recyds',3,[49.5,59.5]),
 ('Zay Flowers','BAL','BUF','rec',3,[4.5,5.5]),('Drake London','ATL','TB','rec',1.5,[4.5,5.5]),
 ('Bijan Robinson','ATL','TB','rec',1.5,[3.5]),('Jaylen Warren','PIT','CLE','rushrec',-3.5,[69.5]),
 ('Denzel Boston','CLE','PIT','recyds',3.5,[29.5]),('Parker Washington','JAX','IND','recyds',-10.5,[39.5]),
 ('George Pickens','DAL','ARI','rec',-7,[3.5,4.5]),('Jahmyr Gibbs','DET','MIN','rec',-3.5,[4.5]),
 ('Chris Godwin','TB','ATL','rec',-1.5,[2.5,3.5]),('James Cook','BUF','BAL','rushrec',-3,[69.5])]
R={}
for n,t,o,m,sp,r in LEGS:
    try:
        out,info=E.sim(dict(player=n,team=t,opp=o,market=m,spread=sp,rungs=r))
    except Exception as ex:
        R[f'{n}|{m}']=dict(err=str(ex)); print(n,m,'ERR',ex,flush=True); continue
    R[f'{n}|{m}']=dict(sims=out,info=info,spread=sp)
    print(n,m,sp,{k:(round(v['median'],1),v['rungs']) for k,v in out.items()},flush=True)
R['_meta']=dict(N=V.N,seed=V.SEED,engine='tools/sim_v6.py',calib=V.CALIB_F)
json.dump(R,open('rescore_v6_i1135.json','w'),default=float)
