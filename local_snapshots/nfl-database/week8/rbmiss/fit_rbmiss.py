"""BUG-2026-11-01-RBMISS fits from real nflverse pbp (2025 REG + 2026 REG thru 2026-10-29; all pre-today).
(A) promotion transfer tau: team-games where the season-to-date RB1 (most RB carries before the game, >=3 prior games with a carry)
    has 0 carries (absent) after having played the team's previous game or later; RB2 = second in pre-game carries.
    tau = (sum RB2 carries_absent - sum RB2 own_share*team_RB_carries) / sum(RB1 share * team_RB_carries); 1000x bootstrap by game; shrink to 0.75 prior? no: reported raw + CI.
(F) soft run-D YPC residual: rushyds rows of tools/sim_v6_backtest.csv (leak-free wk4-7, calibrated pred = pred_mc * fitted M),
    split by opponent pre-week RB YPC allowed >=4.4 vs <4.4; ypc_boost = median(actual/pred | soft) / median(actual/pred | not soft),
    shrunk 1 + n/(n+30)*(raw-1). Output: rbmiss_fit.json"""
import pandas as pd, numpy as np, json
PL=pd.read_parquet('/workspace/nfl-database/runs/2026-11-01_shared_src/players.parquet').set_index('gsis_id').position_group.to_dict()
rng=np.random.default_rng(20261101); rows=[]
P26=None
for f in ['/tmp/play_by_play_2025.parquet','/workspace/nfl-database/runs/2026-11-01_shared_src/play_by_play_2026.parquet']:
    p=pd.read_parquet(f); p=p[p.season_type=='REG']; ru=p[(p.rush_attempt==1)&(p.qb_kneel!=1)&(p.two_point_attempt!=1)]
    ru=ru[ru.rusher_player_id.map(PL)=='RB']
    if '2026' in f: P26=p
    G=p.drop_duplicates('game_id')[['game_id','game_date']]
    c=ru.groupby(['game_id','posteam','rusher_player_id']).size().rename('c').reset_index().merge(G)
    tc=ru.groupby(['game_id','posteam']).size().rename('tc').reset_index().merge(G)
    for team,T in tc.sort_values('game_date').groupby('posteam'):
        dates=list(T.game_date)
        for i,(gid,d,n_tc) in enumerate(zip(T.game_id,T.game_date,T.tc)):
            prev=c[(c.posteam==team)&(c.game_date<d)]
            if prev.game_id.nunique()<3: continue
            st=prev.groupby('rusher_player_id').agg(tot=('c','sum'),gp=('c','size')).sort_values('tot',ascending=False)
            st=st[st.gp>=3]
            if len(st)<2: continue
            rb1,rb2=st.index[0],st.index[1]; cur=c[(c.game_id==gid)&(c.posteam==team)].set_index('rusher_player_id').c
            if cur.get(rb1,0)>0: continue
            prev_tc=tc[(tc.posteam==team)&(tc.game_date<d)].tc.sum()
            s1=st.loc[rb1,'tot']/prev_tc; s2=st.loc[rb2,'tot']/prev_tc
            rows.append(dict(game_id=gid,team=team,tc=n_tc,s1=s1,s2=s2,rb2_act=int(cur.get(rb2,0))))
A=pd.DataFrame(rows); A.to_csv('promotion_rows.csv',index=False)
def tau(d): return (d.rb2_act.sum()-(d.s2*d.tc).sum())/(d.s1*d.tc).sum()
t=tau(A); bs=[tau(A.sample(len(A),replace=True,random_state=int(rng.integers(1e9)))) for _ in range(1000)]
out=dict(doc=__doc__,promotion=dict(tau=round(float(t),4),n=len(A),ci90=[round(float(np.percentile(bs,5)),3),round(float(np.percentile(bs,95)),3)],prior_in_request=0.75))
# F
import sys; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S
B=pd.read_csv('/workspace/nfl-database/tools/sim_v6_backtest.csv'); B=B[B.market=='rushyds'].copy()
M=S.load_calib()['mc']['rushyds']['M']; P=P26[P26.season_type=='REG']; ruA=P[(P.rush_attempt==1)&(P.qb_kneel!=1)]; ruA=ruA[ruA.rusher_player_id.map(PL)=='RB']
opp=[];soft=[]
for _,r in B.iterrows():
    q=P[(P.week==r.week)&(P.rusher_player_id==r.gsis)]
    t_=q.posteam.mode().iloc[0]; g=P[P.game_id==q.game_id.iloc[0]].iloc[0]; o=g.home_team if g.away_team==t_ else g.away_team
    cut=P[P.week==r.week].game_date.min(); d=ruA[(ruA.defteam==o)&(ruA.game_date<cut)]
    y=d.rushing_yards.fillna(0).sum()/len(d); opp.append(o); soft.append(y)
B['opp']=opp; B['opp_ypc']=soft; B['pred']=B.pred_mc*M; B=B[B.pred>0.5]; B['ratio']=B.actual/B.pred
S1=B[B.opp_ypc>=4.4]; S0=B[B.opp_ypc<4.4]; raw=S1.ratio.median()/S0.ratio.median(); n=len(S1)
bsF=[]
for _ in range(1000):
    a=S1.sample(len(S1),replace=True,random_state=int(rng.integers(1e9))); b=S0.sample(len(S0),replace=True,random_state=int(rng.integers(1e9))); bsF.append(a.ratio.median()/b.ratio.median())
out['soft_run_d']=dict(threshold=4.4,raw=round(float(raw),4),n_soft=n,n_other=len(S0),boost=round(float(1+n/(n+30)*(raw-1)),4),ci90=[round(float(np.percentile(bsF,5)),3),round(float(np.percentile(bsF,95)),3)],
                      note='residual AFTER the model\'s existing opponent YPC adjustment (A_ypc already multiplies by opp YPC / league).')
B.to_csv('soft_run_d_rows.csv',index=False); json.dump(out,open('rbmiss_fit.json','w'),indent=1); print(json.dumps({k:v for k,v in out.items() if k!='doc'},indent=1))
