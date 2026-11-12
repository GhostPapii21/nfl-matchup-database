import pandas as pd
p=pd.read_csv('sources/nflverse/pbp_2026.csv.gz',low_memory=False)
d=p[(p.defteam=='BAL')&(p.season_type=='REG')]
O='week10/bal_def_snapshot/'
r=d[(d.play_type=='run')&(d.qb_kneel!=1)]
rows=[]
for (w,t),g in d.groupby(['week','posteam']):
    rr=r[r.week==w]; rb=rr.groupby('rusher_player_name').agg(c=('play_id','size'),y=('rushing_yards','sum')).sort_values('c',ascending=False)
    sc=g.iloc[-1]; pts=int(sc.posteam_score_post if sc.posteam==t else sc.defteam_score_post)
    rows.append(dict(week=w,opp=t,opp_pts_pbp=int(g.total_away_score.max() if g.away_team.iloc[0]==t else g.total_home_score.max()),team_rush=len(rr),team_rush_yds=int(rr.rushing_yards.sum()),ypc=round(rr.rushing_yards.sum()/len(rr),2),rb1=rb.index[0],rb1_line=f"{int(rb.c.iloc[0])}-{int(rb.y.iloc[0])}",rb1_ypc=round(rb.y.iloc[0]/rb.c.iloc[0],2),
     qb_line=f"{int(g.complete_pass.sum())}/{int(g.pass_attempt[g.sack!=1].sum())} {int(g.passing_yards.sum())}"))
pd.DataFrame(rows).to_csv(O+'rush_allowed.csv',index=False)
pa=d[(d.pass_attempt==1)&d.receiver_player_name.notna()].copy()
pa['deep']=pa.air_yards>=15
rec=pa.groupby(['week','posteam','receiver_player_name']).agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum'),adot=('air_yards','mean'),yac=('yards_after_catch','sum'),
 L=('pass_location',lambda s:(s=='left').sum()),M=('pass_location',lambda s:(s=='middle').sum()),R=('pass_location',lambda s:(s=='right').sum()),deep_tgt=('deep','sum')).reset_index()
rec['rank']=rec.groupby('week').yds.rank(ascending=False,method='first')
top=rec[rec['rank']<=3].sort_values(['week','rank']);top.round(1).to_csv(O+'top_receivers.csv',index=False)
rec.round(1).to_csv(O+'all_receivers.csv',index=False)
# zone breakdown
pa['loc']=pa.pass_location; pa['depth']=pa.air_yards.apply(lambda a:'deep15+' if a>=15 else ('int5-14' if a>=5 else 'short<5'))
z=pa.groupby(['loc','depth']).agg(tgt=('play_id','size'),comp=('complete_pass','sum'),yds=('receiving_yards','sum'),epa=('epa','mean')).reset_index();z['ypt']=z.yds/z.tgt
z.round(2).to_csv(O+'zone_allowed.csv',index=False)
print(pd.DataFrame(rows).to_string());print(top.round(1).to_string());print(z.round(2).to_string())
