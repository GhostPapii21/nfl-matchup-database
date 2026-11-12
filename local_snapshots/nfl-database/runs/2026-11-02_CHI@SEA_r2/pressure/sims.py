# Tag: fixed-model, copies only. sim_v6_fix unedited, 3x100k, seed 20261101.
import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V, pandas as pd
e=V.Engine();out={}
def run(L,tag):
    s,i=e.sim(L);out[tag]=dict(s=s,i=i)
    print(tag,'n',i['n_games'],{m:(round(s[m]['median'],1),{k:round(v,3) for k,v in s[m]['rungs'].items()}) for m in('mc','bias','gr')})
    return i
W=dict(player='Emanuel Wilson',team='SEA',opp='CHI',market='rushyds',spread=-3.0,rungs=[14.5,19.5])
b=run(W,'Wilson_base')['w_car']
for t,sh in (('cap_W.45',.45),('cap_W.40',.40),('Charb_full_W.35',.35)): run(dict(W,carry_boost=sh*27/b),'Wilson_'+t)
D=dict(player='Sam Darnold',team='SEA',opp='CHI',market='passyds',spread=-3.0,rungs=[199.5,224.5,238.5,249.5])
run(D,'Darnold_base')
# pressure adj: proxy pressure rate vs CHI expected; Y/DB pressured 3.24*... use scale via ypt? apply via M is internal; approximate post-hoc
json.dump(out,open('raw_sims.json','w'),default=float,indent=1)
p=pd.read_parquet('../src/play_by_play_2026.parquet')
r=p[(p.defteam=='CHI')&(p.rush==1)&(p.qb_scramble==0)]
import numpy as np
pl=pd.read_parquet('../src/players.parquet') if False else None
print('CHI rush allowed (non-scramble, all rushers) YPC',round(r.rushing_yards.mean(),2),'n',len(r))
rb=r[~r.rusher_player_id.isin(p[p.passer_player_id.notna()].passer_player_id.unique())]
print('CHI non-QB rushes YPC',round(rb.rushing_yards.mean(),2),'n',len(rb),'weeks',sorted(r.week.unique()))
