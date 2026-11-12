"""Per-leg features from pbp, weeks < W only (except the week-W actual and starting QB, which is announced pregame)."""
import numpy as np,pandas as pd
P=pd.read_parquet('/workspace/nfl-database/runs/2026-11-02_shared_src/play_by_play_2026.parquet')
P=P[(P.season_type=='REG')&(P.two_point_attempt!=1)]
PL=pd.read_parquet('/workspace/nfl-database/runs/2026-11-02_shared_src/players.parquet').set_index('gsis_id').position_group.to_dict()
pa=P[(P.pass_attempt==1)&(P.sack!=1)].copy(); pa['pg']=pa.receiver_player_id.map(PL); ru=P[P.rush_attempt==1].copy(); ru['pg']=ru.rusher_player_id.map(PL)
wk=P.drop_duplicates('game_id').set_index('game_id').week; GI=P.drop_duplicates('game_id').set_index('game_id')
qbg=pa.groupby(['game_id','posteam','passer_player_id']).size().reset_index(name='n').sort_values('n').drop_duplicates(['game_id','posteam'],keep='last').set_index(['game_id','posteam']).passer_player_id
ST={'passyds':pa.groupby(['passer_player_id','game_id']).passing_yards.sum(),'rec':pa.groupby(['receiver_player_id','game_id']).complete_pass.sum(),
    'recyds':pa.groupby(['receiver_player_id','game_id']).receiving_yards.sum(),'rushyds':ru.groupby(['rusher_player_id','game_id']).rushing_yards.sum()}
def stat(g,gid,m): return float(ST[m].get((g,gid),0) or 0)
TGT=pa.groupby(['receiver_player_id','game_id']).size(); TT=pa.groupby(['game_id','posteam']).size()
CAR=ru.groupby(['rusher_player_id','game_id']).size(); RBC=ru[ru.pg=='RB'].groupby(['game_id','posteam']).size()
def team_games(t,W): return sorted([g for g in set(P[P.posteam==t].game_id) if wk[g]<W],key=lambda g:wk[g])
def allow(opp,W,m,pg):
    if m=='rushyds': d=ru[ru.game_id.map(wk)<W]; return d[d.defteam==opp].rushing_yards.mean()/d.rushing_yards.mean()
    if m=='passyds': d=pa[pa.game_id.map(wk)<W]; return d[d.defteam==opp].passing_yards.fillna(0).mean()/d.passing_yards.fillna(0).mean()
    d=pa[(pa.game_id.map(wk)<W)&(pa.pg==pg)]; o=d[d.defteam==opp]; return (o.receiving_yards.fillna(0).sum()/max(len(o),1))/(d.receiving_yards.fillna(0).sum()/max(len(d),1))
def feats(r):
    W,g,t,gid=r.week,r.gsis,r.team,r.game_id; qb=qbg.get((gid,t)); pr=team_games(t,W); l4=pr[-4:]
    same=[x for x in pr if qbg.get((x,t))==qb][-4:]
    f=dict(actual=stat(g,gid,r.market),vals=[stat(g,x,r.market) for x in same])
    f['tsh']=sum(TGT.get((g,x),0) for x in l4)/max(sum(TT.get((x,t),0) for x in l4),1)
    f['rb_sh']=[CAR.get((g,x),0)/max(RBC.get((x,t),1),1) for x in l4]
    f['tgt_pg']=np.mean([TGT.get((g,x),0) for x in l4]) if l4 else 0
    rk=None
    if r.pos in('WR','TE'):
        q=pa[(pa.game_id.isin(l4))&(pa.posteam==t)&(pa.pg==r.pos)].receiver_player_id.value_counts()
        rk=list(q.index).index(g)+1 if g in q.index else 9
    f['rank']=rk; f['allow']=allow(r.opp,W,r.market,r.pos)
    gi=GI.loc[gid]; f['outdoor']=gi.roof in('outdoors','open'); f['wind']=float(gi.wind) if gi.wind==gi.wind else 0.0
    return f
