import pandas as pd, numpy as np, json
C='/workspace/nfl-sim/data/derived/source_cache/'
p=pd.read_parquet(C+'pbp_2026.parquet')
r=pd.read_parquet(C+'rosters_2026.parquet')[['gsis_id','position']].drop_duplicates('gsis_id')
pos=dict(zip(r.gsis_id,r.position))
p=p[(p.play_type.isin(['pass','run']))&(p.two_point_attempt!=1)]
p['rpos']=p.receiver_player_id.map(pos)
p['rbpos']=p.rusher_player_id.map(pos)
ftn=pd.read_parquet(C+'ftn_charting_2026.parquet')
out={}
for d in ['LA','ARI']:
    q=p[p.defteam==d]; ps=q[(q.pass_attempt==1)&(q.sack!=1)&q.receiver_player_id.notna()]
    o={'games':int(q.game_id.nunique())}
    for P in ['WR','TE','RB']:
        x=ps[ps.rpos==P]; o[f'{P}_targets']=len(x); o[f'{P}_YPT']=round(x.yards_gained.sum()/len(x),2); o[f'{P}_rec_pg']=round(x.complete_pass.sum()/o['games'],2); o[f'{P}_yds_pg']=round(x.yards_gained.sum()/o['games'],1)
    x=ps[ps.pass_location.isin(['left','right'])]; o['Outside_YPT_all']=round(x.yards_gained.sum()/len(x),2)
    x=ps[ps.pass_location.isin(['left','right'])&(ps.rpos=='WR')]; o['Outside_YPT_WR']=round(x.yards_gained.sum()/len(x),2)
    x=ps[ps.pass_location=='middle']; o['Middle_YPT']=round(x.yards_gained.sum()/len(x),2)
    x=ps[ps.air_yards>=20]; o['Deep20_YPT']=round(x.yards_gained.sum()/max(len(x),1),2)
    ru=q[(q.rush_attempt==1)&(q.qb_scramble!=1)]; o['run_YPC_all']=round(ru.yards_gained.mean(),2); o['rush_yds_pg']=round(ru.yards_gained.sum()/o['games'],1)
    rb=ru[ru.rbpos=='RB']; o['RB_YPC']=round(rb.yards_gained.mean(),2); o['RB_rush_yds_pg']=round(rb.yards_gained.sum()/o['games'],1)
    o['explosive_pass20']=int(((q.pass_attempt==1)&(q.yards_gained>=20)).sum()); o['explosive_rush15']=int(((q.rush_attempt==1)&(q.yards_gained>=15)).sum())
    dr=q.groupby(['game_id','drive']).agg(rz=('yardline_100',lambda s:(s<=20).any()),td=('touchdown',lambda s:0)).reset_index()
    rzd=q[q.yardline_100<=20].groupby(['game_id','drive']).apply(lambda g:((g.touchdown==1)&(g.td_team==g.posteam)).any())
    o['RZ_TD_pct']=round(rzd.mean()*100,1); o['RZ_trips']=len(rzd)
    t=q[q.down==3]; o['third_down_conv_pct']=round(t.first_down.fillna(0).mean()*100+0,1)
    f=ftn.merge(q[['game_id','play_id']].assign(nflverse_game_id=q.game_id), left_on=['nflverse_game_id','nflverse_play_id'] if 'nflverse_play_id' in ftn.columns else ['nflverse_game_id','play_id'], right_on=['nflverse_game_id','play_id'])
    db=f[f.is_qb_kneel!=True] if 'is_qb_kneel' in f else f
    db=f[f.n_pass_rushers.notna()&(f.n_pass_rushers>0)]
    o['blitz_pct_5plus']=round((db.n_pass_rushers>=5).mean()*100,1); o['blitz_n']=len(db)
    out[d]=o
json.dump(out,open('defense_profile.json','w'),indent=1)
print(pd.DataFrame(out))
