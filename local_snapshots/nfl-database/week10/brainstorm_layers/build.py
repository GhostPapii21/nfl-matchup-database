import pandas as pd, numpy as np
O='week10/brainstorm_layers/'
p=pd.read_csv('sources/nflverse/pbp_2026.csv.gz',low_memory=False)
f=pd.read_csv('sources/nflverse/ftn_charting_2026.csv')
p=p.merge(f[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers','is_qb_out_of_pocket','is_throw_away','is_screen_pass']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
p=p[p.week<=8]
# L1 drives
d=p[p.drive.notna()&p.posteam.notna()].groupby(['game_id','posteam','drive']).agg(week=('week','first'),plays=('play_id','size'),
  first_downs=('first_down','sum'),top=('drive_time_of_possession','first'),res=('fixed_drive_result','first'),passer=('passer_player_name',lambda s:s.dropna().mode().iloc[0] if s.dropna().size else None)).reset_index()
def sec(t):
  try: m,s=str(t).split(':');return int(m)*60+int(s)
  except: return np.nan
d['top_s']=d.top.map(sec); d['three_out']=((d.first_downs==0)&(d.res=='Punt')).astype(int)
rows=[]
for lab,m in [('BAL all',d.posteam=='BAL'),('BAL wk7-8',(d.posteam=='BAL')&(d.week>=7)),('BAL Fagnano drives',(d.posteam=='BAL')&(d.passer=='J.Fagnano')),('JAX all',d.posteam=='JAX'),('LEAGUE',d.posteam.notna())]:
  x=d[m]; rows.append(dict(split=lab,drives=len(x),games=x.game_id.nunique(),plays_per_drive=round(x.plays.mean(),2),top_per_drive_s=round(x.top_s.mean(),1),three_out_rate=round(x.three_out.mean(),3),score_rate=round(x.res.isin(['Touchdown','Field goal']).mean(),3)))
L1=pd.DataFrame(rows)
g=p[p.posteam.isin(['JAX','BAL'])&(p.play_type.isin(['pass','run']))].groupby(['posteam','game_id']).agg(plays=('play_id','size')).reset_index()
gt=d[d.posteam.isin(['JAX','BAL'])].groupby(['posteam','game_id']).top_s.sum().reset_index()
L1b=g.merge(gt).groupby('posteam').agg(games=('game_id','size'),off_plays_pg=('plays','mean'),top_min_pg=('top_s',lambda s:s.mean()/60)).round(2).reset_index()
# BAL qb by game
bq=p[(p.posteam=='BAL')&(p.pass_attempt==1)|(p.posteam=='BAL')&(p.sack==1)].groupby(['week','passer_player_name']).agg(dropbacks=('play_id','size'),yds=('passing_yards','sum'),sacks=('sack','sum'),epa=('epa','mean')).round(3).reset_index()
L1.to_csv(O+'L1_drives.csv',index=False);L1b.to_csv(O+'L1_pace.csv',index=False);bq.to_csv(O+'L1_bal_qbs.csv',index=False)
print(L1.to_string());print(L1b.to_string());print(bq.to_string())
# L2
db=p[(p.qb_dropback==1)&(p.two_point_attempt!=1)]
bal=db[db.defteam=='BAL']; lg=db
def rates(x):return dict(dropbacks=len(x),ftn_charted=int(x.n_pass_rushers.notna().sum()),blitz_rate=round((x.n_blitzers>0).mean(),3) if x.n_blitzers.notna().any() else None,
  rush5plus=round((x.n_pass_rushers>=5).mean(),3),sack_rate=round(x.sack.mean(),3),qbhit_or_sack=round(((x.qb_hit==1)|(x.sack==1)).mean(),3))
L2a=pd.DataFrame([dict(team='BAL def',**rates(bal[bal.n_blitzers.notna()])),dict(team='LEAGUE',**rates(lg[lg.n_blitzers.notna()]))])
t=db[(db.posteam=='JAX')&(db.passer_player_name=='T.Lawrence')|(db.posteam=='JAX')&(db.sack==1)].copy()
t['blitz']=np.where(t.n_blitzers.isna(),'uncharted',np.where(t.n_blitzers>0,'blitz','no blitz'))
t['pressure_proxy']=np.where((t.qb_hit==1)|(t.sack==1)|(t.is_qb_out_of_pocket==1)|(t.qb_scramble==1),'pressured(proxy)','clean(proxy)')
def qs(x):
  a=x[(x.pass_attempt==1)&(x.sack!=1)]
  return pd.Series(dict(dropbacks=len(x),att=len(a),cmp_pct=round(a.complete_pass.mean(),3),ypa=round(a.passing_yards.fillna(0).mean(),2),sack_rate=round(x.sack.mean(),3),
   epa_db=round(x.epa.mean(),3),ball_out_rate=round(len(a)/len(x),3),throwaway=int(x.is_throw_away.fillna(0).sum()),int_=int(x.interception.sum()),
   third_down_db=int((x.down==3).sum()),third_conv=round(x[x.down==3].first_down.mean(),3) if (x.down==3).any() else None))
L2b=pd.concat([t.groupby('blitz').apply(qs),t.groupby('pressure_proxy').apply(qs),pd.DataFrame([qs(t)],index=['ALL'])])
L2a.to_csv(O+'L2_bal_pressure.csv',index=False);L2b.to_csv(O+'L2_lawrence_splits.csv')
print(L2a.to_string());print(L2b.to_string())
tp=t[t.receiver_player_name.notna()]
L2c=pd.crosstab(tp.receiver_player_name,[tp.pressure_proxy]).join(pd.crosstab(tp.receiver_player_name,tp.blitz),rsuffix='_b')
L2c=L2c.sort_values('pressured(proxy)',ascending=False);L2c.to_csv(O+'L2_targets_under_pressure.csv');print(L2c.head(10).to_string())
# L4 route proxy
j=p[(p.posteam=='JAX')&(p.pass_attempt==1)&p.receiver_player_name.notna()].copy()
j['depth']=pd.cut(j.air_yards,[-99,0,4.99,14.99,99],labels=['behind_los','short1-4','int5-14','deep15+'])
L4=j.groupby(['receiver_player_name','pass_location','depth'],observed=True).agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum')).reset_index()
L4=L4[L4.receiver_player_name.isin(['P.Washington','B.Strange','J.Meyers','Bri.Thomas','B.Tuten','C.Rodriguez','L.Allen'])]
L4.to_csv(O+'L4_route_proxy.csv',index=False)
piv=j[j.receiver_player_name.isin(L4.receiver_player_name.unique())].assign(area=lambda x:x.pass_location.fillna('na')+'/'+x.depth.astype(str))
pv=pd.crosstab(piv.receiver_player_name,piv.area);print(pv.to_string())
s=j.groupby('receiver_player_name').agg(scr=('is_screen_pass',lambda s:int(s.fillna(0).sum())),tgt=('play_id','size'));print(s.sort_values('tgt').tail(8))
# L6 BAL by area to TEs vs WR
r=pd.read_csv('sources/nflverse/roster_2026.csv')[['gsis_id','position']].drop_duplicates('gsis_id')
b=p[(p.defteam=='BAL')&(p.pass_attempt==1)&p.receiver_player_id.notna()].merge(r,left_on='receiver_player_id',right_on='gsis_id',how='left')
b['depth']=pd.cut(b.air_yards,[-99,4.99,14.99,99],labels=['short<5','int5-14','deep15+'])
L6=b.groupby(['position','pass_location','depth'],observed=True).agg(tgt=('play_id','size'),yds=('receiving_yards','sum'),epa=('epa','mean')).reset_index()
L6['ypt']=(L6.yds/L6.tgt).round(2);L6.to_csv(O+'L6_bal_allowed_by_pos_area.csv',index=False);print(L6.to_string())
