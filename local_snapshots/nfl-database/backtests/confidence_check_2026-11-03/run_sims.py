"""One job = (engine, opp strength, week). Leak-free: engine sees pbp with game_date < first game date of week W
(MNF: < 2026-11-02). sim_v6 / sim_v6_fix per-market multipliers are refit walk-forward from each engine's own saved
backtest residual file using only weeks < W (originals were fit on wk4-7 incl. outcomes later in the test window)."""
import os,sys,json,importlib,numpy as np,pandas as pd,warnings; warnings.filterwarnings('ignore')
eng,opp,W=sys.argv[1],sys.argv[2],int(sys.argv[3]); N=int(os.environ.get('CC_N','20000'))
SRC='/workspace/nfl-database/runs/2026-11-02_shared_src'; HERE=os.path.dirname(os.path.abspath(__file__))
P=pd.read_parquet(SRC+'/play_by_play_2026.parquet',columns=['week','game_date','season_type'])
cut='2026-11-02' if W==9 else P[(P.week==W)&(P.season_type=='REG')].game_date.min()
os.environ.update(CC_OPP=opp,CC_SRC=SRC,CC_CUTOFF=cut,SIMV6_SRC=SRC); sys.path.insert(0,HERE+'/engines')
L=pd.read_csv(HERE+'/legs.csv'); L=L[L.week==W]
out=[]; calib_used=None
if eng=='sim_v5':
    M=importlib.import_module('cc_sim_v5'); M.N=N
    def run(leg): return M.sim(leg)[0]
else:
    M=importlib.import_module('cc_sim_'+eng.split('sim_')[1])
    bt=pd.read_csv(HERE+f'/engines/{eng}_backtest.csv'); tr=bt[bt.week<min(W,8)]
    calib_used=M.fit(tr) if len(tr) else None
    E=M.Engine(cutoff=cut,calib=calib_used,n=N)
    def run(leg): return E.sim(leg)[0]
for _,r in L.iterrows():
    leg=dict(player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,market=r.market,spread=r.team_spread,rungs=[r.line])
    try: o=run(leg)
    except Exception as ex: out.append(dict(week=W,gsis=r.gsis,market=r.market,err=repr(ex)[:120])); continue
    out.append(dict(week=W,gsis=r.gsis,market=r.market,**{f'p_{m}':o[m]['rungs'][str(r.line)] for m in ('mc','bias','gr')},**{f'med_{m}':o[m]['median'] for m in ('mc','bias','gr')}))
os.makedirs(HERE+'/sims',exist_ok=True)
pd.DataFrame(out).to_csv(HERE+f'/sims/{eng}_opp{opp}_w{W}.csv',index=False)
json.dump(dict(engine=eng,opp=opp,week=W,cutoff=cut,n=N,calib_weeks=sorted(set(tr.week)) if eng!='sim_v5' and len(tr) else [],calib=calib_used),open(HERE+f'/sims/{eng}_opp{opp}_w{W}.json','w'),indent=1,default=str)
print(eng,opp,W,cut,len(out),sum('err' in x for x in out))
