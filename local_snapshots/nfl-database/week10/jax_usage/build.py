import pandas as pd
P='sources/nflverse/'
p=pd.read_csv(P+'pbp_2026.csv.gz',low_memory=False)
j=p[(p.posteam=='JAX')&(p.two_point_attempt!=1)]
t=j[j.receiver_player_name.notna()&(j.pass_attempt==1)]
g=t.groupby(['week','receiver_player_name']).agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),air=('air_yards','sum')).reset_index()
g['tgt_share']=(g.tgt/g.groupby('week').tgt.transform('sum')).round(3)
g['rank']=g.groupby('week').tgt.rank(method='first',ascending=False).astype(int)
g.sort_values(['week','rank']).to_csv('week10/jax_usage/targets_by_game.csv',index=False)
s=g.groupby('receiver_player_name').agg(gp=('week','nunique'),tgt=('tgt','sum'),rec=('rec','sum'),yds=('yds','sum'),air=('air','sum'),
 top1=('rank',lambda r:(r==1).sum()),top2=('rank',lambda r:(r<=2).sum()),top3=('rank',lambda r:(r<=3).sum())).reset_index()
s['share']=(s.tgt/s.tgt.sum()).round(3);s['tgt_pg']=(s.tgt/s.gp).round(1);s['adot']=(s.air/s.tgt).round(1)
s.sort_values('tgt',ascending=False).to_csv('week10/jax_usage/targets_season.csv',index=False)
r=j[(j.rush_attempt==1)&j.rusher_player_name.notna()]
rr=r.groupby(['week','rusher_player_name']).agg(car=('play_id','size'),yds=('rushing_yards','sum'),scr=('qb_scramble','sum')).reset_index()
rr['carry_share']=(rr.car/rr.groupby('week').car.transform('sum')).round(3);rr['ypc']=(rr.yds/rr.car).round(2)
sn=pd.read_csv(P+'snap_counts_2026.csv.gz');sn=sn[(sn.team=='JAX')&(sn.position.isin(['RB','QB','FB']))][['week','player','position','offense_snaps','offense_pct']]
sn.to_csv('week10/jax_usage/rb_snaps.csv',index=False)
rr.sort_values(['week','car'],ascending=[True,False]).to_csv('week10/jax_usage/rush_by_game.csv',index=False)
print(g.sort_values(['week','rank']).groupby('week').head(4).to_string())
print(s.sort_values('tgt',ascending=False).head(12).to_string())
print(rr.sort_values(['week','car'],ascending=[True,False]).to_string())
print(sn.sort_values(['week','offense_snaps'],ascending=[True,False]).to_string())
