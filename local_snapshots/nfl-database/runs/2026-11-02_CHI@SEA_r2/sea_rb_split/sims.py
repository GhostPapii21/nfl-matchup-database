# SEA RB split. Tag: fixed-model, copies only. sim_v6_fix unedited, 3x100k, seed 20261101, SEA -3.
# Scenarios scale Wilson/Holani carries via the engine's own carry_boost (target share / base weighted share).
import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V
e=V.Engine();out={}
def run(pl,mk,r,cb=1.0,tag='base'):
    L=dict(player=pl,team='SEA',opp='CHI',market=mk,spread=-3.0,rungs=r,carry_boost=cb)
    if mk in('rec','recyds'): L['current_qb']='Sam Darnold'
    s,info=e.sim(L);k=f'{pl}|{mk}|{tag}';out[k]=dict(sims=s,info=info,cb=cb)
    print(k,'cb',round(cb,2),'n',info['n_games'],'w_car',round(info['w_car'],1),{m:(round(s[m]['median'],1),{kk:round(v,3) for kk,v in s[m]['rungs'].items()}) for m in('mc','bias','gr')})
    return info
i=run('Emanuel Wilson','rushyds',[9.5,14.5,19.5,24.5])
base=i['w_car']; TEAM_RB=27.0  # SEA RB carries/g wk1-7 approx (from usage.md team_car incl. QB ~ RB-only est)
for tag,sh in (('PriceIR_Charb_capped_W.45',.45),('PriceIR_Charb_full_W.35',.35),('PriceActive_W.28',.28)):
    run('Emanuel Wilson','rushyds',[9.5,14.5,19.5,24.5],cb=sh*TEAM_RB/base,tag=tag)
run('George Holani','rec',[0.5,1.5,2.5]); run('George Holani','recyds',[4.5,9.5])
for pl in ('Zach Charbonnet','Jadarian Price'):
    try: run(pl,'rushyds',[24.5,29.5,32.5])
    except Exception as ex: print(pl,'SIMULATION NOT RUN:',type(ex).__name__,str(ex)[:120]); out[pl]='SIMULATION NOT RUN: '+str(ex)[:200]
json.dump(dict(tag='fixed-model, copies only',src=V.SRC,seed=V.SEED,n=V.N,out=out),open('raw_sims.json','w'),indent=1,default=float)
