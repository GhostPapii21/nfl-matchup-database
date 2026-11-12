"""Overlay fixes for nfl_matchups.sqlite. Reads the copy fixes.sqlite; writes fix_* tables only.
Sources: nflverse-data releases (public), fetched to src/ (time in src/fetched_at.txt)."""
import sqlite3,json,re,pandas as pd,numpy as np,datetime as dt
DB='fixes.sqlite'; S='src/'
NOW=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
FETCH=open(S+'fetched_at.txt').read().strip()
REL='https://github.com/nflverse/nflverse-data/releases/download/'
ADMIN={'Official Timeout','Timeout','Two-minute warning','End Period','End of Half','End of Game','End of Regulation'}
ABBR={'LAR':'LA','WSH':'WAS'}
db=sqlite3.connect(DB)
pbp=pd.read_parquet(S+'play_by_play_2026.parquet')
snaps=pd.read_parquet(S+'snap_counts_2026.parquet')
inj=pd.read_parquet(S+'injuries_2026.parquet')
ros=pd.read_parquet(S+'roster_weekly_2026.parquet')
# ---- game map ESPN -> nflverse
gm=[]
for (gid,data) in db.execute("select game_id,data from games"):
    d=json.loads(data);c=d['competitions'][0]['competitors']
    h=[ABBR.get(x['team']['abbreviation'],x['team']['abbreviation']) for x in c if x['homeAway']=='home'][0]
    a=[ABBR.get(x['team']['abbreviation'],x['team']['abbreviation']) for x in c if x['homeAway']=='away'][0]
    gm.append(dict(espn_game_id=gid,week=d['week']['number'],home=h,away=a))
gm=pd.DataFrame(gm)
ng=pbp[['game_id','week','home_team','away_team']].drop_duplicates().rename(columns={'game_id':'nflverse_game_id','home_team':'home','away_team':'away'})
gm=gm.merge(ng,on=['week','home','away'],how='left')
assert gm.nflverse_game_id.notna().all(), gm[gm.nflverse_game_id.isna()]
gm.to_sql('fix_game_map',db,if_exists='replace',index=False)
# ---- FIX 1: play credits
pl=pd.read_sql("select game_id,play_id,offense_id,play_type,yards,data from plays",db)
pl['nfl_play_id']=[float(p[len(g):]) for g,p in zip(pl.game_id,pl.play_id)]
pl['text']=[json.loads(x).get('text') for x in pl.data]
pl=pl.drop(columns='data').merge(gm[['espn_game_id','nflverse_game_id']],left_on='game_id',right_on='espn_game_id')
cols=['game_id','play_id','play_type','desc','yards_gained','rushing_yards','receiving_yards','passing_yards','lateral_rushing_yards','lateral_receiving_yards','rusher_player_id','receiver_player_id','passer_player_id','rush_attempt','pass_attempt','complete_pass','sack','qb_scramble','qb_kneel','qb_spike','penalty','penalty_type','penalty_yards','fumble','fumble_lost','lateral_reception','lateral_rush','posteam','two_point_attempt']
v=pbp[cols].rename(columns={'game_id':'nflverse_game_id','play_id':'nfl_play_id','play_type':'nfl_play_type'})
f=pl.merge(v,on=['nflverse_game_id','nfl_play_id'],how='left')
def credit(r):
    if pd.isna(r.nfl_play_type):
        if r.play_type in ADMIN: return (None,None,None,'not_a_scrimmage_play','administrative ESPN event: '+str(r.play_type))
        return (None,None,None,'unresolved','no nflverse play with matching id')
    if r.two_point_attempt==1: return (None,None,None,'not_a_scrimmage_gain','two-point attempt (not credited as rush/rec yards)')
    if r.nfl_play_type=='no_play': return (None,None,None,'nullified','play nullified by penalty: no credited gain')
    if r.qb_kneel==1: return ('kneel',r.rushing_yards,r.rusher_player_id,'credited','QB kneel; kept separate from rushing')
    if r.rush_attempt==1 and not pd.isna(r.rushing_yards): return ('rush',r.rushing_yards,r.rusher_player_id,'credited','rushing_yards (pre-lateral carrier)')
    if r.complete_pass==1 and not pd.isna(r.receiving_yards): return ('reception',r.receiving_yards,r.receiver_player_id,'credited','receiving_yards (pre-lateral receiver); penalty yards excluded')
    if r.sack==1: return ('sack',r.yards_gained,None,'credited','sack: yards_gained (negative) to team, not a player rush')
    if r.pass_attempt==1: return ('incomplete_or_int',0.0 if r.complete_pass==0 else None,r.receiver_player_id,'credited','incomplete/intercepted: 0 credited gain')
    return (None,None,None,'not_a_scrimmage_play',str(r.nfl_play_type))
cr=f.apply(credit,axis=1,result_type='expand');cr.columns=['credit_kind','credited_yards','credited_player_gsis','credit_status','credit_rule']
f=pd.concat([f,cr],axis=1)
f['lateral_yards']=f.lateral_rushing_yards.fillna(0)+f.lateral_receiving_yards.fillna(0)
f.loc[(f.lateral_rush!=1)&(f.lateral_reception!=1),'lateral_yards']=np.nan
f['stored_yards']=f.yards
f['differs']=(f.credit_status=='credited')&(f.credited_yards.notna())&((f.stored_yards-f.credited_yards).abs()>0.5)
f['source']=REL+'pbp/play_by_play_2026.parquet (yards_gained/rushing_yards/receiving_yards)'
f['source_fetched_at']=FETCH; f['built_at']=NOW
out=f[['game_id','play_id','nflverse_game_id','nfl_play_id','play_type','nfl_play_type','text','stored_yards','yards_gained','credit_kind','credited_yards','credited_player_gsis','lateral_yards','penalty','penalty_type','penalty_yards','fumble','fumble_lost','qb_scramble','qb_kneel','credit_status','credit_rule','differs','source','source_fetched_at','built_at']]
out.to_sql('fix_play_credits',db,if_exists='replace',index=False)
# box-score reconciliation: sum credited per player-game vs nflverse weekly player stats (official)
ps=pd.read_parquet(S+'stats_player_week_2026.parquet')
o2=out.copy();o2.loc[o2.credit_kind=='kneel','credit_kind']='rush'  # official rushing includes kneels
cg=o2[o2.credit_kind.isin(['rush','reception'])].groupby(['nflverse_game_id','credited_player_gsis','credit_kind']).credited_yards.sum().unstack(fill_value=0).reset_index()
wk=pbp[['game_id','week']].drop_duplicates()
cg=cg.merge(wk,left_on='nflverse_game_id',right_on='game_id')
m=cg.merge(ps[['player_id','week','rushing_yards','receiving_yards']],left_on=['credited_player_gsis','week'],right_on=['player_id','week'],how='left')
m['rush_ok']=(m.get('rush',0)-m.rushing_yards.fillna(0)).abs()<0.5
m['rec_ok']=(m.get('reception',0)-m.receiving_yards.fillna(0)).abs()<0.5
m[['nflverse_game_id','credited_player_gsis','week','rush','reception','rushing_yards','receiving_yards','rush_ok','rec_ok']].to_sql('fix_credit_reconcile',db,if_exists='replace',index=False)
# derived counts before/after
def counts(df,yc,kindcol):
    rush=df[kindcol=='rush'];rec=df[kindcol=='reception']
    return dict(rush_explosive_10=int((rush[yc]>=10).sum()),rush_explosive_15=int((rush[yc]>=15).sum()),rec_explosive_20=int((rec[yc]>=20).sum()),run_stuff_le0=int((rush[yc]<=0).sum()))
bk=np.where(out.play_type.isin(['Rush','Rushing Touchdown']),'rush',np.where(out.play_type.isin(['Pass Reception','Passing Touchdown']),'reception','other'))
before=counts(out,'stored_yards',bk)
cc=out[out.credit_status=='credited'];after=counts(cc,'credited_yards',cc.credit_kind)
# per team-game derived table (after)
cc2=cc.merge(pbp[['game_id','play_id','posteam']].rename(columns={'game_id':'nflverse_game_id','play_id':'nfl_play_id'}),on=['nflverse_game_id','nfl_play_id'])
pos=ros.drop_duplicates('gsis_id').set_index('gsis_id').position
cc2['pos']=cc2.credited_player_gsis.map(pos)
dg=cc2.groupby(['game_id','posteam']).apply(lambda d:pd.Series(dict(
  wr_explosive_rec20=int(((d.credit_kind=='reception')&(d.pos=='WR')&(d.credited_yards>=20)).sum()),
  te_explosive_rec20=int(((d.credit_kind=='reception')&(d.pos=='TE')&(d.credited_yards>=20)).sum()),
  rb_explosive_rush10=int(((d.credit_kind=='rush')&(d.pos=='RB')&(d.credited_yards>=10)).sum()),
  rb_explosive_rec20=int(((d.credit_kind=='reception')&(d.pos=='RB')&(d.credited_yards>=20)).sum()),
  run_stuffs_le0=int(((d.credit_kind=='rush')&(d.credited_yards<=0)).sum()),
  designed_rushes=int(((d.credit_kind=='rush')&(d.qb_scramble!=1)).sum())))).reset_index()
dg['definition']='explosive: reception credited >=20, rush credited >=10 (non-kneel, scrambles included); stuff: credited rush <=0; kneels excluded'
dg['source']='fix_play_credits';dg['built_at']=NOW
dg.to_sql('fix_team_explosives',db,if_exists='replace',index=False)
# ---- FIX 2/3: participation
ros['week']=ros.week.astype(int)
sn=snaps.merge(ros[['pfr_id','gsis_id','espn_id','week']].dropna(subset=['pfr_id']).drop_duplicates(['pfr_id','week']),left_on=['pfr_player_id','week'],right_on=['pfr_id','week'],how='left')
games=pbp[['game_id','week','home_team','away_team']].drop_duplicates()
tg=pd.concat([games.rename(columns={'home_team':'team'})[['game_id','week','team']],games.rename(columns={'away_team':'team'})[['game_id','week','team']]])
R=ros[ros.game_type=='REG'][['gsis_id','espn_id','full_name','team','position','week','status']].dropna(subset=['gsis_id'])
R=R.merge(tg,on=['team','week'],how='inner')  # only weeks the team played
S2=sn[['game_id','gsis_id','pfr_player_id','offense_snaps','offense_pct','defense_snaps','st_snaps']].dropna(subset=['gsis_id'])
P=R.merge(S2,on=['game_id','gsis_id'],how='outer')
ij=inj[['gsis_id','week','report_status','practice_status']]
P=P.merge(ij,on=['gsis_id','week'],how='left')
def st(r):
    tot=sum(x for x in [r.offense_snaps,r.defense_snaps,r.st_snaps] if pd.notna(x))
    if pd.notna(r.offense_snaps) or pd.notna(r.st_snaps):
        if tot>0: return ('played','snap_counts>0')
    if r.status=='INA': return ('inactive','roster_weekly status INA')
    if r.status in('RES','EXE','RET','CUT','DEV','TRD','TRT'): return ('not_on_active_roster','roster_weekly status '+str(r.status))
    if r.report_status=='Out': return ('inactive','injury report Out')
    if r.status=='ACT': return ('active_no_snaps_recorded','ACT on roster, no snap row: DNP or unrecorded (not a verified zero)')
    return ('unresolved','no roster/snap evidence')
x=P.apply(st,axis=1,result_type='expand');P['participation']=x[0];P['evidence']=x[1]
P['source']=REL+'snap_counts/snap_counts_2026 + weekly_rosters/roster_weekly_2026 + injuries/injuries_2026'
P['source_fetched_at']=FETCH;P['built_at']=NOW
P=P.merge(gm[['espn_game_id','nflverse_game_id']],left_on='game_id',right_on='nflverse_game_id',how='left').drop(columns='nflverse_game_id').rename(columns={'game_id':'nflverse_game_id'})
P.to_sql('fix_participation',db,if_exists='replace',index=False)
# role: targets/carries per player-game from pbp (credited, incl. incompletions), denominators = team totals in games player PLAYED
tgt=pbp[(pbp.pass_attempt==1)&(pbp.sack!=1)&pbp.receiver_player_id.notna()&(pbp.play_type!='no_play')].groupby(['game_id','receiver_player_id']).size().rename('targets')
car=pbp[(pbp.rush_attempt==1)&(pbp.qb_kneel!=1)&(pbp.play_type!='no_play')&pbp.rusher_player_id.notna()].groupby(['game_id','rusher_player_id']).size().rename('carries')
tt=pbp[(pbp.pass_attempt==1)&(pbp.sack!=1)&pbp.receiver_player_id.notna()&(pbp.play_type!='no_play')].groupby(['game_id','posteam']).size().rename('team_targets')
tc=pbp[(pbp.rush_attempt==1)&(pbp.qb_kneel!=1)&(pbp.play_type!='no_play')].groupby(['game_id','posteam']).size().rename('team_carries')
pg=P[P.participation=='played'][['nflverse_game_id','week','gsis_id','full_name','team','position','offense_pct']].dropna(subset=['team'])
pg=pg.merge(tgt,left_on=['nflverse_game_id','gsis_id'],right_index=True,how='left').merge(car,left_on=['nflverse_game_id','gsis_id'],right_index=True,how='left')
pg=pg.merge(tt,left_on=['nflverse_game_id','team'],right_index=True,how='left').merge(tc,left_on=['nflverse_game_id','team'],right_index=True,how='left')
pg[['targets','carries']]=pg[['targets','carries']].fillna(0)  # verified: player PLAYED (snaps>0) and pbp has no target/carry -> true zero
pg.to_sql('fix_player_game_usage',db,if_exists='replace',index=False)
rows=[]
for (gid,nm,tm,pos_),d in pg.sort_values('week').groupby(['gsis_id','full_name','team','position']):
    allp=P[(P.gsis_id==gid)&(P.team==tm)]
    l3=d.tail(3)
    rows.append(dict(gsis_id=gid,player=nm,team=tm,position=pos_,games_played=len(d),
      games_inactive=int((allp.participation=='inactive').sum()),games_not_on_roster=int((allp.participation=='not_on_active_roster').sum()),
      games_active_no_snaps=int((allp.participation=='active_no_snaps_recorded').sum()),
      season_target_share=d.targets.sum()/d.team_targets.sum() if d.team_targets.sum() else None,
      season_carry_share=d.carries.sum()/d.team_carries.sum() if d.team_carries.sum() else None,
      current_target_share_l3=l3.targets.sum()/l3.team_targets.sum() if l3.team_targets.sum() else None,
      current_carry_share_l3=l3.carries.sum()/l3.team_carries.sum() if l3.team_carries.sum() else None,
      current_snap_pct_l3=l3.offense_pct.mean(),last_played_week=int(d.week.max()),
      is_returning=bool(((allp.participation.isin(['inactive','not_on_active_roster']))&(allp.week<d.week.max())&(allp.week>d.week.min())).any()) or bool(((allp.participation.isin(['inactive','not_on_active_roster']))&(allp.week<d.week.max())).any()),
      targets_per_game=d.targets.mean(),carries_per_game=d.carries.mean(),
      method='denominator = team targets/carries in games the player PLAYED (snaps>0); inactive/absent games excluded; current role = last 3 played games',
      source='fix_participation + nflverse pbp',built_at=NOW))
pd.DataFrame(rows).to_sql('fix_player_role',db,if_exists='replace',index=False)
# ---- FIX 4: QB rushing
q=pbp[(pbp.rush_attempt==1)&(pbp.play_type!='no_play')&pbp.rusher_player_id.notna()]
qbs=set(ros[ros.position=='QB'].gsis_id)
q=q[q.rusher_player_id.isin(qbs)].copy()
q['kind']=np.where(q.qb_kneel==1,'kneel',np.where(q.qb_scramble==1,'scramble','designed'))
qg=q.groupby(['game_id','week','posteam','rusher_player_id','rusher_player_name','kind']).agg(att=('play_id','size'),yds=('rushing_yards','sum')).unstack('kind')
qg.columns=[f'{k}_{a}' for a,k in qg.columns];qg=qg.reset_index()
# include QB games with dropbacks but no rushes (verified zero rushes)
db_=pbp[(pbp.qb_dropback==1)&pbp.passer_player_id.notna()&(pbp.play_type!='no_play')].groupby(['game_id','week','posteam','passer_player_id','passer_player_name']).size().rename('dropbacks').reset_index().rename(columns={'passer_player_id':'rusher_player_id','passer_player_name':'rusher_player_name'})
qg=db_.merge(qg,on=['game_id','week','posteam','rusher_player_id','rusher_player_name'],how='outer')
for k in ['scramble','designed','kneel']:
    for a in ['att','yds']: qg[f'{k}_{a}']=qg.get(f'{k}_{a}',np.nan)
    qg.loc[qg.dropbacks.notna()|qg[f'{k}_att'].notna(),f'{k}_att']=qg[f'{k}_att'].fillna(0)
    qg.loc[qg[f'{k}_att']==0,f'{k}_yds']=0
qg['rush_yds_ex_kneel']=qg.scramble_yds+qg.designed_yds
qg['source']=REL+'pbp (qb_scramble, qb_kneel, rush_attempt, rushing_yards)';qg['built_at']=NOW
qg.rename(columns={'rusher_player_id':'qb_gsis','rusher_player_name':'qb'}).to_sql('fix_qb_rushing_game',db,if_exists='replace',index=False)
qs=qg[qg.dropbacks>=10].groupby(['rusher_player_id','rusher_player_name']).agg(starts_ge10_dropbacks=('game_id','size'),scr_att_pg=('scramble_att','mean'),scr_yds_pg=('scramble_yds','mean'),des_att_pg=('designed_att','mean'),des_yds_pg=('designed_yds','mean'),kneel_att_pg=('kneel_att','mean'),kneel_yds_pg=('kneel_yds','mean'),rush_yds_ex_kneel_pg=('rush_yds_ex_kneel','mean'),rush_yds_ex_kneel_median=('rush_yds_ex_kneel','median'),scr_rate_per_dropback=('scramble_att','sum')).reset_index()
tdb=qg[qg.dropbacks>=10].groupby('rusher_player_id').dropbacks.sum()
qs['scr_rate_per_dropback']=qs.scr_rate_per_dropback/qs.rusher_player_id.map(tdb)
qs['qb_full_name']=qs.rusher_player_id.map(ros.drop_duplicates('gsis_id').set_index('gsis_id').full_name)
qs['method']='per-QB baseline over games with >=10 dropbacks; kneels separated and excluded from rush_yds_ex_kneel';qs['source']='fix_qb_rushing_game';qs['built_at']=NOW
qs.rename(columns={'rusher_player_id':'qb_gsis','rusher_player_name':'qb'}).to_sql('fix_qb_rushing',db,if_exists='replace',index=False)
db.execute("create table if not exists fix_meta(k text primary key,v text)")
for k,v_ in dict(built_at=NOW,source_fetched_at=FETCH,before=json.dumps(before),after=json.dumps(after)).items(): db.execute("insert or replace into fix_meta values(?,?)",(k,v_))
db.commit()
print('before',before,'after',after)
print(out.credit_status.value_counts().to_dict(),'differs',int(out.differs.sum()))
