"""08:25 routine re-score on sim_v6 (100k x3, seed 20261101). Rice/Worthy RECEPTIONS use the same Rice-active KC split as rec_r0750.py (v5)."""
import sys,json; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
E=V.Engine(); orig=E.player
KC=json.load(open('/workspace/nfl-database/runs/2026-11-01_shared_src/rec_r0750.json'))['kc_games']
def split(name,team,qb=False,gsis=None):
    d,a,yc,yr,g=orig(name,team,qb,gsis); return d,a[a.game_id.isin(KC)],yc,yr,g
LEGS=[('Jahan Dotson','ATL','TB','recyds',2.5,[25.5],False),('Xavier Worthy','KC','DEN','recyds',-1.5,[29.5],False),
 ('Puka Nacua','LAR','LAC','rec',-6.5,[7.5,8.5],False),('Tre Tucker','LV','NYJ','rec',1.5,[3.5],False),
 ('Jordan Addison','MIN','DET','rec',3.5,[3.5],False),('Stefon Diggs','WSH','PHI','recyds',-5.5,[42.5],False),
 ('Stefon Diggs','WSH','PHI','rec',-5.5,[3.5,4.5],False),('Matthew Stafford','LAR','LAC','comp',-6.5,[22.5],False),
 ('Rashee Rice','KC','DEN','rec',-1.5,[3.5,4.5,5.5],True),('Xavier Worthy','KC','DEN','rec',-1.5,[3.5],True)]
R={}
for n,t,o,m,sp,r,s in LEGS:
    E.player=split if s else orig
    out,info=E.sim(dict(player=n,team=t,opp=o,market=m,spread=sp,rungs=r))
    R[f'{n}|{m}']=dict(sims=out,info=info,split=s); print(n,m,{k:(round(v['median'],2),v['rungs']) for k,v in out.items()},flush=True)
R['_meta']=dict(N=V.N,seed=V.SEED,engine='tools/sim_v6.py',calib=V.CALIB_F)
json.dump(R,open('/workspace/nfl-database/runs/2026-11-01_shared_src/rescore_v6_r0835.json','w'),default=float)
