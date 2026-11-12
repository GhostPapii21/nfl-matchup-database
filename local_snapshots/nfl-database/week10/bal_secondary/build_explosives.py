import pandas as pd, numpy as np
p=pd.read_parquet('raw/play_by_play_2026.parquet')
f=pd.read_parquet('raw/ftn_charting_2026.parquet')
r=pd.read_parquet('raw/roster_weekly_2026.parquet')[['gsis_id','position','week','team']].drop_duplicates(['gsis_id'])
p=p.merge(f[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers','is_play_action','is_screen_pass','n_defense_box']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
p=p[(p.season_type=='REG')&p.play_type.isin(['pass','run'])&(p.two_point_attempt!=1)]
p['xp']=((p.pass_attempt==1)&(p.complete_pass==1)&(p.yards_gained>=20))|((p.rush_attempt==1)&(p.yards_gained>=10)&(p.qb_scramble!=1))
p['xpass']=(p.pass_attempt==1)&(p.complete_pass==1)&(p.yards_gained>=20)
p['xrush']=(p.rush_attempt==1)&(p.yards_gained>=10)&(p.qb_scramble!=1)
pos=r.set_index('gsis_id').position
p['rec_pos']=p.receiver_player_id.map(pos); p['rush_pos']=p.rusher_player_id.map(pos)
p['depth']=np.where(p.air_yards>=15,'deep15+',np.where(p.air_yards>=5,'int5-14','short<5'))
b=p[(p.defteam=='BAL')&p.xp].copy()
b['shell']='UNAVAILABLE (participation file not published)'
b['blitz']=np.where(b.n_blitzers.isna(),'not charted',np.where(b.n_blitzers>0,'blitz','no blitz'))
b['margin_off']=b.score_differential
b['player']=b.receiver_player_name.fillna(b.rusher_player_name); b['pos']=b.rec_pos.fillna(b.rush_pos)
b['kind']=np.where(b.xpass,'pass20+','rush10+')
b['named_defender_in_desc']=b.pass_defense_1_player_name.fillna('')
b['tackler']=b.solo_tackle_1_player_name.fillna(b.assist_tackle_1_player_name).fillna(b.tackle_with_assist_1_player_name).fillna('')
cols=['week','posteam','qtr','down','ydstogo','margin_off','kind','blitz','n_pass_rushers','is_play_action','shell','player','pos','depth','pass_location','air_yards','yards_after_catch','yards_gained','run_location','run_gap','tackler','touchdown','desc']
b[cols].sort_values(['week','qtr']).to_csv('explosives_bal_wk1_9.csv',index=False)
# league per game
g=p.groupby(['defteam','game_id']).agg(xpass=('xpass','sum'),xrush=('xrush','sum'),xpy=('yards_gained',lambda s:s[p.loc[s.index,'xpass']].sum())).reset_index()
t=g.groupby('defteam').agg(games=('game_id','size'),xpass_pg=('xpass','mean'),xrush_pg=('xrush','mean'),xpass_yds_pg=('xpy','mean')).round(2)
t['xpass_rank']=t.xpass_pg.rank(ascending=False,method='min'); t['xrush_rank']=t.xrush_pg.rank(ascending=False,method='min')
lg=t[['xpass_pg','xrush_pg','xpass_yds_pg']].mean().round(2)
t.to_csv('explosives_by_defense.csv')
print('BAL',t.loc['BAL'].to_dict(),'\nLEAGUE',lg.to_dict(),'\nweeks',sorted(b.week.unique()))
# summaries: by pos x location x depth (passes) and per-game league compare
lp=p[p.xpass]; bp=b[b.kind=='pass20+']
def summ(d,games): return d.groupby(['rec_pos']).agg(n=('play_id','size'),yds=('yards_gained','sum')).assign(per_g=lambda x:(x.n/games).round(2))
bg=t.loc['BAL','games']; lgg=t.games.sum()
s=summ(bp,bg).join(summ(lp,lgg)[['per_g']].rename(columns={'per_g':'lg_per_def_g'}))
s.to_csv('summary_by_pos.csv'); print(s)
a=bp.groupby(['pass_location','depth']).agg(n=('play_id','size'),yds=('yards_gained','sum'))
la=(lp.groupby(['pass_location','depth']).size()/lgg).round(2).rename('lg_per_g')
a=a.join(la); a['bal_per_g']=(a.n/bg).round(2); a.to_csv('summary_by_area.csv'); print(a)
pa=bp.groupby(['rec_pos','pass_location','depth']).agg(n=('play_id','size'),yds=('yards_gained','sum')); pa.to_csv('summary_pos_area.csv'); print(pa)
print(bp.blitz.value_counts(), bp.qtr.value_counts().sort_index().to_dict())
br=b[b.kind=='rush10+']; print(br.groupby(['run_location','run_gap']).agg(n=('play_id','size'),yds=('yards_gained','sum')))
print(bp[['week','posteam','qtr','player','pos','pass_location','air_yards','yards_gained','named_defender_in_desc','tackler','blitz']].to_string())
