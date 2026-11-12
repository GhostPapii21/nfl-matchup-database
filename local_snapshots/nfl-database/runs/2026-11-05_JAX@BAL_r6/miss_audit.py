import pandas as pd
p=pd.read_parquet('../2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet')
j=p[(p.home_team=='JAX')|(p.away_team=='JAX')]
for gid,x in j.groupby('game_id'):
    h=x[x.qtr<=2]; f=h.iloc[-1]; m=(f.total_home_score-f.total_away_score)*(1 if f.home_team=='JAX' else -1)
    qbs=x[x.pass_attempt==1].groupby('posteam').passer_player_name.agg(lambda s:s.value_counts().index[0]).to_dict()
    print(gid,'1H margin',int(m),qbs)
for gid in ['2026_05_PHI_JAX','2026_06_HOU_JAX']:
    x=j[(j.game_id==gid)&(j.qtr<=2)]; print('=====',gid)
    d=x.groupby(['drive','posteam']).agg(start=('time','first'),qtr=('qtr','first'),plays=('play_id','count'),yds=('yards_gained','sum'),res=('fixed_drive_result','last'),to=('turnover' if 'turnover' in x else 'interception','max'),fum=('fumble_lost','max'),intc=('interception','max'),rz=('yardline_100',lambda s:(s<=20).any()),sacks=('sack','sum')).reset_index()
    print(d.to_string())
    s=x[(x.touchdown==1)|(x.field_goal_result.notna())|(x.safety==1)][['qtr','time','posteam','desc','total_home_score','total_away_score']]
    for r in s.itertuples(): print(r.qtr,r.time,r.posteam,f"{r.total_home_score}-{r.total_away_score}",r.desc[:140])
    print(x[x.desc.str.contains('injur',case=False,na=False)][['qtr','posteam','desc']].to_string()[:1500])
