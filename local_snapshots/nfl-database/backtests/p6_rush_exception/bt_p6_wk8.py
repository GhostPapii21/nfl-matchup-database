"""Week 8 Sunday extension: pbp parquet only has CAR@GB for wk8, so Sunday games are graded from playlogs/2026_wk8/*_box.json
(ESPN summary). Spreads from playlogs/game_scripts_2026.csv. Engine cutoff 2026-11-01 (all pbp before Sunday)."""
import sys, json, glob
import numpy as np, pandas as pd
sys.path.insert(0,'/workspace/nfl-database/tools'); sys.path.insert(0,'/workspace/nfl-database/backtests/wk8_proposals')
sys.path.insert(0,'.')
import sim_v6 as S
from harness import load, proxy_line, prior_vals
from bt_p6 import real_lines  # noqa (module guarded below)
d,g,pg=load(); RL=real_lines(); GS=pd.read_csv('/workspace/nfl-database/playlogs/game_scripts_2026.csv'); GS=GS[GS.week==8]
NAME=S._PL.set_index('gsis_id').display_name.to_dict()
E=S.Engine(cutoff='2026-11-01',calib=None); rows=[]
for f in sorted(glob.glob('/workspace/nfl-database/playlogs/2026_wk8/*_box.json')):
    b=json.load(open(f))
    for team,t in b['teams'].items():
        gs=GS[GS.team==team]
        if gs.empty: print('no spread',team); continue
        sp=float(gs.spread.iloc[0]); opp=gs.opp.iloc[0]
        if not sp>0: continue
        rush={x['player']:(float(x['YDS']),int(x['CAR'])) for x in t.get('rushing',[])}
        pri=pg[(pg.team==team)&(pg.week<8)&(pg.pos=='RB')&(pg.car>0)]
        for pid,pr in pri.groupby('pid'):
            if len(pr)<2 or pr.car.mean()<8: continue
            name=NAME.get(pid,pid)
            if name not in rush: print('not in box (inactive/0 car)',name,team); continue
            line=proxy_line(pr.sort_values('week').ryds.tolist()); src='standin'
            if RL.get(name) is not None: line,src=float(RL[name]),'real'
            o,_=E.sim(dict(player=name,gsis=pid,team=team,opp=opp,market='rushyds',spread=sp,rungs=[line]),raw=True)
            ps={m:o[m]['rungs'][str(line)] for m in S.MODES}; a,c=rush[name]
            rows.append(dict(week=8,player=name,gsis=pid,team=team,opp=opp,team_spread=sp,line=line,line_src=src,p_mc=ps['mc'],p_bias=ps['bias'],p_gr=ps['gr'],
                p=np.mean(list(ps.values())),med_mc=o['mc']['median'],actual=a,carries=c,hit=int(a>line)))
            print(8,name,line,src,round(rows[-1]['p'],3),a,flush=True)
pd.DataFrame(rows).to_csv('p6_legs_wk8.csv',index=False)
