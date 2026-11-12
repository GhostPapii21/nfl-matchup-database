import pandas as pd, numpy as np, json
C='/workspace/nfl-sim/data/derived/source_cache/'
rng=np.random.default_rng(20261115)
s26=pd.read_parquet(C+'stats_player_week_2026.parquet'); s25=pd.read_parquet(C+'stats_player_week_2025.parquet')
sn=pd.read_parquet(C+'snap_counts_2026.parquet')
P={'Puka Nacua':('LA','Volume'),'Davante Adams':('LA','Explosive/RZ'),'Kyren Williams':('LA','Rush-Receive'),'Blake Corum':('LA','RB2'),
   'Trey McBride':('ARI','TE-Primary'),'Michael Wilson':('ARI','Explosive'),'Jeremiyah Love':('ARI','RB (committee)'),'Tyler Allgeier':('ARI','RB (committee)')}
# multipliers from defensive-profile triggers (documented in sheet)
M={'Puka Nacua':{'rec_yds':1.03,'rec':1.02},           # ARI WR YPT 9.71>=9.0 slight positive, capped +3%
   'Davante Adams':{'rec_yds':1.0,'rec':1.0},          # ARI Outside WR YPT 9.77 <10.5 -> neutral
   'Kyren Williams':{'rush_yds':1.0,'rec':1.0,'rec_yds':1.0},  # ARI RB YPC 4.29 neutral band
   'Blake Corum':{'rush_yds':1.0},
   'Trey McBride':{'rec_yds':0.88,'rec':1.0},          # LA TE YPT 5.03 <=5.5 hard TE -> cut yards, volume holds
   'Michael Wilson':{'rec_yds':0.92,'rec':0.97},       # LA Outside WR YPT 6.04 hard + blitz 29% minor volume cut
   'Jeremiyah Love':{'rush_yds':0.90},'Tyler Allgeier':{'rush_yds':0.90}}  # LA RB YPC 3.77 <=3.8 run suppression
stats={'rec':'receptions','rec_yds':'receiving_yards','rush_yds':'rushing_yards'}
rows=[];logs={}
for n,(t,role) in P.items():
    g=s26[(s26.player_display_name==n)&(s26.team==t)].sort_values('week')
    g25=s25[(s25.player_display_name==n)&(s25.season_type=='REG')]
    tt=s26[s26.team==t].groupby('week').targets.sum()
    sp=sn[(sn.player==n)&(sn.team==t)].set_index('week').offense_pct
    lg=g[['week','opponent_team','targets','receptions','receiving_yards','carries','rushing_yards']].copy()
    lg['tgt_share']=(lg.targets/lg.week.map(tt)).round(3); lg['snap_pct']=lg.week.map(sp)
    logs[n]=lg.to_dict('records')
    for k,c in stats.items():
        if k=='rush_yds' and g.carries.sum()<20: continue
        if k!='rush_yds' and g.targets.sum()<10: continue
        x=g[c].values.astype(float); prior=g25[c].values.astype(float) if len(g25) else x
        m=M[n].get(k,1.0)
        # Model 1: Monte Carlo 10k — bootstrap game from 2026 logs (70%) / 2025 (30%) with multiplicative noise
        pool=np.where(rng.random(10000)<0.7, rng.choice(x,10000), rng.choice(prior,10000))
        mc=np.clip(pool*rng.lognormal(0,0.25,10000)*m,0,None)
        # Model 2: Bayesian normal-normal: prior 2025 per-game mean (8 game weight), likelihood 2026 games
        pm,pv=prior.mean(),max(prior.var(),1e-6); n26=len(x); w=n26/(n26+8)
        post=(w*x.mean()+(1-w)*pm)*m; sd=np.sqrt(pv)
        bay=np.clip(rng.normal(post,sd,10000),0,None)
        # Model 3: game randomness — script factor (ARI ~ trailing more), pace, plus Poisson-ish volume
        script=rng.normal(1.0,0.15,10000)
        gr=np.clip(rng.choice(x,10000)*script*m,0,None)
        allm=np.concatenate([mc,bay,gr])
        if k=='rec': allm=np.round(allm)
        q=np.percentile(allm,[5,10,15,20,25]); med=np.median([np.median(mc),np.median(bay),np.median(gr)])
        rows.append(dict(player=n,team=t,role=role,stat=k,games26=n26,avg26=round(x.mean(),1),avg25=round(pm,1),mult=m,
          p5=round(q[0],1),p10=round(q[1],1),p15_MAIN=round(q[2],1),p20=round(q[3],1),p25=round(q[4],1),
          med_MC=round(np.median(mc),1),med_Bayes=round(np.median(bay),1),med_GR=round(np.median(gr),1),median=round(med,1)))
df=pd.DataFrame(rows); df.to_csv('projections.csv',index=False); json.dump(logs,open('player_logs.json','w'),indent=1,default=str)
pd.set_option('display.width',250); print(df.drop(columns=['team']).to_string())
for n,l in logs.items(): print(n); print(pd.DataFrame(l).to_string(index=False))
