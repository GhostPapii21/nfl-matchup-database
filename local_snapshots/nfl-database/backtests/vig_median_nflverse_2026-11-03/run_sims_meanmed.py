"""Rerun confidence_check sim engines (read-only import, opp 0.5) to save mean AND median per leg. Same leak-free cutoff logic as
backtests/confidence_check_2026-11-03/run_sims.py; output only to this dir."""
import os,sys,importlib,numpy as np,pandas as pd,warnings; warnings.filterwarnings('ignore')
eng,W=sys.argv[1],int(sys.argv[2]); opp='0.5'; N=int(os.environ.get('CC_N','20000'))
CC='/workspace/nfl-database/backtests/confidence_check_2026-11-03'; SRC='/workspace/nfl-database/runs/2026-11-02_shared_src'
HERE=os.path.dirname(os.path.abspath(__file__)); os.makedirs(HERE+'/sims',exist_ok=True)
P=pd.read_parquet(SRC+'/play_by_play_2026.parquet',columns=['week','game_date','season_type'])
cut=P[(P.week==W)&(P.season_type=='REG')].game_date.min()
os.environ.update(CC_OPP=opp,CC_SRC=SRC,CC_CUTOFF=cut,SIMV6_SRC=SRC); sys.path.insert(0,CC+'/engines'); os.chdir(CC)
L=pd.read_csv(CC+'/legs.csv'); L=L[L.week==W]
if eng=='sim_v5':
    M=importlib.import_module('cc_sim_v5'); M.N=N; run=lambda leg: M.sim(leg)[0]
else:
    M=importlib.import_module('cc_sim_'+eng.split('sim_')[1]); bt=pd.read_csv(CC+f'/engines/{eng}_backtest.csv'); tr=bt[bt.week<min(W,8)]
    E=M.Engine(cutoff=cut,calib=M.fit(tr) if len(tr) else None,n=N); run=lambda leg: E.sim(leg)[0]
out=[]
for _,r in L.iterrows():
    leg=dict(player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,market=r.market,spread=r.team_spread,rungs=[r.line])
    try: o=run(leg)
    except Exception as ex: out.append(dict(week=W,gsis=r.gsis,market=r.market,err=repr(ex)[:120])); continue
    row=dict(week=W,gsis=r.gsis,market=r.market)
    for m in ('mc','bias','gr'): row.update({f'p_{m}':o[m]['rungs'][str(r.line)],f'med_{m}':o[m]['median'],f'mean_{m}':o[m]['mean']})
    out.append(row)
pd.DataFrame(out).to_csv(HERE+f'/sims/{eng}_w{W}.csv',index=False); print(eng,W,cut,len(out),flush=True)
