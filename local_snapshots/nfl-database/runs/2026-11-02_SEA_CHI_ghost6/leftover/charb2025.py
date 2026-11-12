# Charbonnet 2025-proxy sims (§7 EXCEPTION: 2025 sample, Rico decides). nflverse stats_player_week_2025 + pbp 2025 + snap_counts_2025. 3x100k, seed 20261101.
import pandas as pd, numpy as np, json
S=pd.read_parquet('/tmp/stats_player_week_2025.parquet'); P=pd.read_parquet('/tmp/play_by_play_2025.parquet'); SN=pd.read_parquet('/tmp/snap_counts_2025.parquet')
c=S[(S.player_display_name=='Zach Charbonnet')][['week','season_type','opponent_team','carries','rushing_yards','targets','receptions','receiving_yards']].copy()
c['snap']=c.week.map(SN[SN.player=='Zach Charbonnet'].set_index('week').offense_pct)
c['rr']=c.rushing_yards+c.receiving_yards
o=P[(P.posteam=='SEA')&P.play_type.isin(['run','pass'])]
c['lead_share']=c.week.map(o.groupby('week').apply(lambda d:(d.score_differential>0).mean()).round(2))
g=P[(P.home_team=='SEA')|(P.away_team=='SEA')].groupby('week').apply(lambda d:(d.home_score.max()-d.away_score.max())*(1 if d.home_team.iloc[0]=='SEA' else -1))
c['margin']=c.week.map(g); r=c[c.season_type=='REG']
print(c.to_string(index=False))
hr=lambda d:dict(n=len(d),rr30=int((d.rr>=30).sum()),rec2=int((d.receptions>=2).sum()))
print('season',hr(r),'last4',hr(r.tail(4)),'lead>=50%',hr(r[r.lead_share>=.5]),'lead<50%',hr(r[r.lead_share<.5]),'snap<45%',hr(r[r.snap<.45]))
print('per-snap: car',(r.carries/r.snap).median().round(1),'tgt',(r.targets.sum()/r.snap.sum()).round(2))
# run & catch pools (2025 REG, SEA, Charbonnet)
runs=P[(P.rusher_player_name=='Z.Charbonnet')&(P.rush_attempt==1)&(P.season_type=='REG')].rushing_yards.fillna(0).values
recs=P[(P.receiver_player_name=='Z.Charbonnet')&(P.complete_pass==1)&(P.season_type=='REG')].receiving_yards.fillna(0).values
catch=r.receptions.sum()/r.targets.sum(); ypc=runs.mean(); adj=0.5*(4.19/4.2)+0.5  # CHI 4.19 YPC allowed vs lg 4.2, half-strength, regressed
rng=np.random.default_rng(20261101); N=100000; out={}
def run(name,car_lo,car_hi,tgt_lam,shock):
    z=rng.standard_normal(N)*shock
    car=np.clip(np.round(rng.uniform(car_lo,car_hi+1,N)*np.exp(z)),0,None).astype(int)
    ry=np.array([rng.choice(runs,k).sum() if k else 0 for k in car])*adj*(4.2*0.3+ypc*0.7)/ypc
    t=rng.poisson(tgt_lam*np.exp(z*0.5)); rc=rng.binomial(t,catch)
    yy=np.array([rng.choice(recs,k).sum() if k else 0 for k in rc])
    rr=ry+yy; out[name]=dict(p_rr30=float((rr>=30).mean()),p_rr245=float((rr>24.5).mean()),p_rr395=float((rr>39.5).mean()),med_rr=float(np.median(rr)),p_rec2=float((rc>=2).mean()),med_rec=float(np.median(rc)),med_car=float(np.median(car)))
# tgt rate 2025: ~3.1 tgt per 100% snaps; pitch count snaps ~30-40% -> ~1.0-1.2 tgt
for tag,lo,hi in (('PriceIR',9,12),('PriceActive',8,11)):
    run(f'mc_{tag}',lo,hi,1.1,0.0)
    run(f'bias_{tag}',lo-1,hi-1,0.9,0.0)   # first game back off ACL: -1 carry, fewer pass-down snaps
    run(f'gr_{tag}',lo,hi,1.1,0.25)        # shared game shock (script), SEA -3
json.dump(dict(out=out,ypc_2025=float(ypc),catch=float(catch)),open('charb2025_sims.json','w'),indent=1)
for k,v in out.items(): print(k,{a:round(b,3) for a,b in v.items()})
