import pandas as pd,re
p=pd.read_parquet('/workspace/nfl-database/tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet')
pl=pd.read_parquet('src/players.parquet')[['gsis_id','position']].drop_duplicates('gsis_id').set_index('gsis_id').position
pas=p[(p.pass_attempt==1)&(p.sack!=1)].copy();pas['rpos']=pas.receiver_player_id.map(pl)
c=pas[pas.posteam=='CHI'];tot=c.groupby('week').size();qb=c.groupby('week').passer_player_name.agg(lambda s:s.mode().iat[0])
o=c[c.receiver_player_name=='R.Odunze']
g=o.groupby('week').agg(opp=('defteam','first'),tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum'),adot=('air_yards','mean'),air=('air_yards','sum'),rz=('yardline_100',lambda y:(y<=20).sum()),lng=('receiving_yards','max'),mid=('pass_location',lambda s:(s=='middle').mean()))
g['share']=(g.tgt/tot.reindex(g.index)).round(3);g['qb']=qb.reindex(g.index);print(g.round(2).to_markdown())
cg=c[c.week.isin([1,2,6,7])];print('Caleb-game WR/TE targets',cg[cg.rpos.isin(['WR','TE'])].receiver_player_name.value_counts().head(6).to_dict())
print('location all',o.pass_location.value_counts().to_dict())
w=pas[(pas.defteam=='SEA')&(pas.rpos=='WR')]
s=w.groupby(['week','posteam','receiver_player_name']).agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum')).reset_index()
print(s[s.yds>=30].to_markdown(index=False));print('SEA WR ypg',w.groupby('week').receiving_yards.sum().mean().round(1),'outside(L/R) ypg',w[w.pass_location!='middle'].groupby('week').receiving_yards.sum().mean().round(1),'middle ypg',w[w.pass_location=='middle'].groupby('week').receiving_yards.sum().mean().round(1))
