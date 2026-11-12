"""Receiving candidates + re-grade of 3 gated legs. sim_v6 100k x3, seed 20261101."""
import sys,json; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
E=V.Engine(); R=json.load(open('bonus_sims.json'))
C=[('Tre Tucker','LV','NYJ','rec',1.5,[2.5,3.5]),('Puka Nacua','LAR','LAC','rec',-6.5,[6.5,7.5]),('Stefon Diggs','WSH','PHI','rec',-5.5,[2.5,3.5]),
 ('Dalton Kincaid','BUF','BAL','rec',-3,[2.5,3.5]),('Brenton Strange','JAX','IND','rec',-10.5,[2.5,3.5]),('Sam LaPorta','DET','MIN','rec',-3.5,[3.5,4.5]),
 ('Travis Kelce','KC','DEN','rec',-1.5,[3.5,4.5]),('Rashee Rice','KC','DEN','rec',-1.5,[3.5]),('Cade Otton','TB','ATL','rec',-1.5,[2.5,3.5])]
for n,t,o,m,sp,r in C:
    d=dict(player=n,team=t,opp=o,market=m,rungs=r)
    if sp is not None: d['spread']=sp
    out,info=E.sim(d); R[f'{n}|{m}']=dict(sims=out,info=info,spread=sp,team=t,opp=o)
    print(n,m,sp,{k:(round(v['median'],1),{a:round(b,3) for a,b in v['rungs'].items()}) for k,v in out.items()},flush=True)
json.dump(R,open('bonus_sims.json','w'),default=float)
