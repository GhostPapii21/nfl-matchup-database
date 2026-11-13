"""Step 2: re-run the three walk-forward prop engines (read-only copies in confidence_check_2026-11-03/engines, NOT this repo's
engine) with rungs = [main line + every real alt rung]. Same leak-free cutoffs and walk-forward calibration as
confidence_check run_sims.py. No outcomes used. Usage: python3 s2_run_alt_sims.py ENGINE WEEK"""
import os,sys,json,importlib,pandas as pd,warnings; warnings.filterwarnings('ignore')
CC='/workspace/nfl-database/backtests/confidence_check_2026-11-03'; OUT=os.environ.get('OUT','/workspace/research/selective_under_alt_2026-11-12')
eng,W=sys.argv[1],int(sys.argv[2]); N=int(os.environ.get('CC_N','20000')); opp='0.5'
SRC='/workspace/nfl-database/runs/2026-11-02_shared_src'
P=pd.read_parquet(SRC+'/play_by_play_2026.parquet',columns=['week','game_date','season_type'])
cut='2026-11-02' if W==9 else P[(P.week==W)&(P.season_type=='REG')].game_date.min()
os.environ.update(CC_OPP=opp,CC_SRC=SRC,CC_CUTOFF=cut,SIMV6_SRC=SRC); sys.path.insert(0,CC+'/engines')
L=pd.read_csv(CC+'/legs.csv'); L=L[(L.week==W)&(L.market!='passyds')]
A=pd.read_csv(OUT+'/alt_rungs_props.csv'); A=A[A.week==W]
R=A.groupby(['gsis','market']).rung.apply(lambda s:sorted(set(s))).to_dict()
L=L[[ (g,m) in R for g,m in zip(L.gsis,L.market)]]
if eng=='sim_v5':
    M=importlib.import_module('cc_sim_v5'); M.N=N; run=lambda leg:M.sim(leg)[0]
else:
    M=importlib.import_module('cc_sim_'+eng.split('sim_')[1]); bt=pd.read_csv(CC+f'/engines/{eng}_backtest.csv'); tr=bt[bt.week<min(W,8)]
    E=M.Engine(cutoff=cut,calib=M.fit(tr) if len(tr) else None,n=N); run=lambda leg:E.sim(leg)[0]
out=[]
for _,r in L.iterrows():
    rungs=[r.line]+[x for x in R[(r.gsis,r.market)] if x!=r.line]
    leg=dict(player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,market=r.market,spread=r.team_spread,rungs=rungs)
    try: o=run(leg)
    except Exception as ex: out.append(dict(week=W,gsis=r.gsis,market=r.market,err=repr(ex)[:120])); continue
    for k in rungs:
        out.append(dict(week=W,gsis=r.gsis,market=r.market,rung=k,is_main=int(k==r.line),
                        p_over=sum(o[m]['rungs'][str(k)] for m in ('mc','bias','gr'))/3))
os.makedirs(OUT+'/altsims',exist_ok=True)
pd.DataFrame(out).to_csv(OUT+f'/altsims/{eng}_w{W}.csv',index=False); print(eng,W,cut,len(L),len(out))
