"""Fit game-script RB carry boosts from real nflverse pbp (2025 REG + 2026 REG thru 2026-10-29; all pre-today).
Per team-game: lead RB / RB2 = top-2 RBs by season-to-date carries BEFORE that game (>=2 prior games played).
expected = player's pre-game avg carries (games with >=1 carry); ratio = sum(actual)/sum(expected) per group.
Boost = ratio(trigger)/ratio(baseline), shrunk toward 1: 1+n/(n+K)*(raw-1), K=30. 1000x game-level bootstrap CI.
Groups: FAV = team favored by >=7 (closing spread_line) AND opp pre-game season YPC allowed to RBs >=4.4 (no kneels; same definition as the IND 4.49 RB YPC);
WX = outdoor game with 'rain'/'shower'/'storm'/'snow' in nflverse weather string OR wind >=15 (pbp has no gusts/PoP);
baseline = neither. Output: rb_boost_fit.json"""
import pandas as pd, numpy as np, json, re
K=30
pl=pd.read_parquet('/workspace/nfl-database/runs/2026-11-01_shared_src/players.parquet').set_index('gsis_id').position_group.to_dict()
rows=[]
for f in ['/tmp/play_by_play_2025.parquet','/workspace/nfl-database/runs/2026-11-01_shared_src/play_by_play_2026.parquet']:
    p=pd.read_parquet(f); p=p[(p.season_type=='REG')]
    ru=p[(p.rush_attempt==1)&(p.qb_kneel!=1)&(p.two_point_attempt!=1)]
    G=p.drop_duplicates('game_id')[['game_id','game_date','home_team','away_team','spread_line','roof','weather','wind']].sort_values('game_date')
    # opp YPC allowed season-to-date (pre-game)
    ruR=ru[ru.rusher_player_id.map(pl)=='RB']; dg=ruR.groupby(['game_id','defteam']).agg(y=('rushing_yards','sum'),n=('rush_attempt','size')).reset_index().merge(G[['game_id','game_date']])
    car=ru[ru.rusher_player_id.map(pl)=='RB'].groupby(['game_id','posteam','rusher_player_id']).size().rename('c').reset_index().merge(G[['game_id','game_date']])
    for _,g in G.iterrows():
        for team,opp,sp in ((g.home_team,g.away_team,-g.spread_line),(g.away_team,g.home_team,g.spread_line)):
            prev=car[(car.posteam==team)&(car.game_date<g.game_date)]
            if prev.game_id.nunique()<2: continue
            od=dg[(dg.defteam==opp)&(dg.game_date<g.game_date)]
            if od.n.sum()<50: continue
            ypc=od.y.sum()/od.n.sum()
            st=prev.groupby('rusher_player_id').agg(tot=('c','sum'),gp=('c','size'))
            st=st[st.gp>=2].sort_values('tot',ascending=False)
            if len(st)<2: continue
            cur=car[(car.game_id==g.game_id)&(car.posteam==team)].set_index('rusher_player_id').c
            outdoor=str(g.roof) in ('outdoors','open')
            wx=outdoor and (bool(re.search(r'rain|shower|storm|snow|drizzle',str(g.weather),re.I)) or (g.wind==g.wind and g.wind>=15))
            fav=(sp<=-7) and ypc>=4.4
            tc=car[(car.game_id==g.game_id)&(car.posteam==team)].c.sum()
            for role,pid in (('lead',st.index[0]),('rb2',st.index[1])):
                rows.append(dict(game_id=g.game_id,team=team,role=role,pid=pid,exp=st.loc[pid,'tot']/st.loc[pid,'gp'],act=int(cur.get(pid,0)),fav=fav,wx=wx,spread=sp,opp_ypc=ypc))
D=pd.DataFrame(rows); D.to_csv('rb_boost_rows.csv',index=False)
rng=np.random.default_rng(20261101); out=dict(doc=__doc__,K=K,groups={})
def rat(d): return d.act.sum()/d.exp.sum()
for role in ('lead','rb2'):
    B=D[(D.role==role)&~D.fav&~D.wx]; base=rat(B)
    for grp,mask in (('fav',D.fav),('wx',D.wx)):
        T=D[(D.role==role)&mask]; raw=rat(T)/base; n=len(T)
        gids=T.game_id.unique(); bs=[]
        for _ in range(1000):
            s=T.set_index('game_id').loc[rng.choice(gids,len(gids))]; bb=B.sample(len(B),replace=True,random_state=int(rng.integers(1e9)))
            bs.append(rat(s)/rat(bb))
        M=1+n/(n+K)*(raw-1)
        out['groups'][f'{role}_{grp}']=dict(n=n,raw=round(raw,4),boost=round(M,4),ci90=[round(float(np.percentile(bs,5)),3),round(float(np.percentile(bs,95)),3)],base_ratio=round(base,4),trig_ratio=round(rat(T),4),n_base=len(B))
json.dump(out,open('rb_boost_fit.json','w'),indent=1); print(json.dumps(out['groups'],indent=1))
