import pandas as pd, numpy as np, sqlite3, json, io, re
B='/workspace/nfl-database'; D=B+'/week8/defense'
sb=json.load(open(D+'/espn_scoreboard_20261101.json'))
games=[]; espn2abbr={}
for e in sb['events']:
    cs=e['competitions'][0]['competitors']
    h=[c for c in cs if c['homeAway']=='home'][0]; a=[c for c in cs if c['homeAway']=='away'][0]
    odds=e['competitions'][0].get('odds',[{}])
    games.append(dict(id=e['id'],away=a['team']['abbreviation'],home=h['team']['abbreviation'],date=e['date'],
        odds=(odds[0].get('details'),odds[0].get('overUnder')) if odds else None,
        awayrec=(a.get('records') or [{}])[0].get('summary'),homerec=(h.get('records') or [{}])[0].get('summary')))
    for c in cs: espn2abbr[c['team']['id']]=c['team']['abbreviation']; 
names={c['team']['displayName']:c['team']['abbreviation'] for e in sb['events'] for c in e['competitions'][0]['competitors']}
fix=lambda t:{'WSH':'WAS','LAR':'LA'}.get(t,t)   # ESPN->nflverse
p=pd.read_parquet(B+'/fixes/src/play_by_play_2026.parquet')
ro=pd.read_parquet(B+'/fixes/src/roster_weekly_2026.parquet')[['gsis_id','position']].drop_duplicates('gsis_id')
pos=dict(zip(ro.gsis_id,ro.position))
p['rpos']=p.receiver_player_id.map(pos); p['rupos']=p.rusher_player_id.map(pos)
ng=p.groupby('defteam').game_id.nunique()
ftn=pd.read_parquet(D+'/raw/ftn_charting_2026.parquet')
p=p.merge(ftn[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
tg=p[p.receiver_player_id.notna()&(p.play_type=='pass')]
ru=p[(p.play_type=='run')&(p.qb_kneel!=1)]
def pergame(df,key):
    return df.groupby(key)
out={}
allteams=sorted(ng.index)
for t in allteams:
    g=ng[t]; d={}
    for P in ['WR','TE','RB']:
        x=tg[(tg.defteam==t)&(tg.rpos==P)]
        d[P]=dict(tgt_pg=len(x)/g,rec_pg=x.complete_pass.sum()/g,yds_pg=x.receiving_yards.fillna(0).sum()/g,ypt=x.receiving_yards.fillna(0).sum()/max(len(x),1))
    for loc,lab in [(['left','right'],'WR_outside_proxy'),(['middle'],'WR_middle_proxy')]:
        x=tg[(tg.defteam==t)&(tg.rpos=='WR')&tg.pass_location.isin(loc)]
        d[lab]=dict(tgt_pg=len(x)/g,ypt=x.receiving_yards.fillna(0).sum()/max(len(x),1),yds_pg=x.receiving_yards.fillna(0).sum()/g)
    x=ru[(ru.defteam==t)&(ru.rupos=='RB')]
    d['RB_rush']=dict(car_pg=len(x)/g,yds_pg=x.rushing_yards.fillna(0).sum()/g,ypc=x.rushing_yards.fillna(0).sum()/max(len(x),1))
    d['RB_total_yds_pg']=d['RB_rush']['yds_pg']+d['RB']['yds_pg']
    dd=p[p.defteam==t]
    t3=dd.third_down_converted.sum()+dd.third_down_failed.sum(); d['third_down_pct_allowed']=100*dd.third_down_converted.sum()/t3
    rz=dd[dd.yardline_100<=20].drop_duplicates(['game_id','drive']); d['rz_trips']=len(rz); d['rz_td_pct_allowed']=100*(rz.fixed_drive_result=='Touchdown').mean()
    db=dd[dd.qb_dropback==1]; d['sack_rate']=100*db.sack.mean(); d['qb_hit_plus_sack_rate_proxy']=100*((db.qb_hit==1)|(db.sack==1)).mean()
    dbf=db[db.n_blitzers.notna()]; d['ftn_blitz_rate']=100*(dbf.n_blitzers>0).mean(); d['ftn_charted_db']=len(dbf)
    d['epa_play_allowed']=dd[dd.play_type.isin(['pass','run'])].epa.mean(); d['games']=int(g)
    # offense vs blitz
    o=p[(p.posteam==t)&(p.qb_dropback==1)&p.n_blitzers.notna()]
    d['off_epa_vs_blitz']=o[o.n_blitzers>0].epa.mean(); d['off_epa_no_blitz']=o[o.n_blitzers==0].epa.mean(); d['off_blitz_faced']=100*(o.n_blitzers>0).mean()
    oo=p[(p.posteam==t)&(p.qb_dropback==1)]; d['off_sack_rate_allowed']=100*oo.sack.mean(); d['off_hit_sack_rate_allowed_proxy']=100*((oo.qb_hit==1)|(oo.sack==1)).mean()
    d['off_epa_play']=p[(p.posteam==t)&p.play_type.isin(['pass','run'])].epa.mean()
    d['off_plays_pg']=len(p[(p.posteam==t)&p.play_type.isin(['pass','run'])])/p[p.posteam==t].game_id.nunique()
    out[t]=d
# explosives allowed (fix_team_explosives; posteam=offense -> defense=opponent)
c=sqlite3.connect(B+'/fixes/fixes.sqlite')
ex=pd.read_sql('select e.*,m.home,m.away from fix_team_explosives e join fix_game_map m on m.espn_game_id=e.game_id',c)
ex['def']=np.where(ex.posteam==ex.home,ex.away,ex.home)
exa=ex.groupby('def')[['wr_explosive_rec20','te_explosive_rec20','rb_explosive_rush10','rb_explosive_rec20','run_stuffs_le0','designed_rushes']].mean()
for t in out:
    if t in exa.index: out[t]['explosives_allowed_pg']=exa.loc[t].round(2).to_dict()
# Sharp tables
def sharp(f):
    t=pd.read_html(io.StringIO(open(D+f'/raw/{f}.html').read()))[0]; t['abbr']=t.Team.map(lambda n:fix(names.get(n,{'Washington Commanders':'WSH'}.get(n,n)))); return t.set_index('abbr')
allnames={}
sp,ss,st=[sharp(f) for f in ['nfl-coverage-stats-by-position','nfl-coverage-schemes','nfl-defensive-tendencies']]
# Sharp names for teams not on Sunday slate -> map via full nflverse team list
tm={'Arizona Cardinals':'ARI','Atlanta Falcons':'ATL','Baltimore Ravens':'BAL','Buffalo Bills':'BUF','Carolina Panthers':'CAR','Chicago Bears':'CHI','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Dallas Cowboys':'DAL','Denver Broncos':'DEN','Detroit Lions':'DET','Green Bay Packers':'GB','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC','Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Los Angeles Rams':'LA','Miami Dolphins':'MIA','Minnesota Vikings':'MIN','New England Patriots':'NE','New Orleans Saints':'NO','New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI','Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF','Seattle Seahawks':'SEA','Tampa Bay Buccaneers':'TB','Tennessee Titans':'TEN','Washington Commanders':'WAS'}
for f in ['nfl-coverage-stats-by-position','nfl-coverage-schemes','nfl-defensive-tendencies']:
    t=pd.read_html(io.StringIO(open(D+f'/raw/{f}.html').read()))[0]; t['abbr']=t.Team.map(tm)
    assert t.abbr.notna().all(), t.Team[t.abbr.isna()].tolist()
    for _,r in t.iterrows():
        out[r.abbr].setdefault('sharp',{}).update({k:float(v) for k,v in r.items() if k not in('Team','abbr')})
# Sharp advanced: defensive pressure rate = opponents' pressure_rate_allowed in games vs team; ESPN win rates
db=sqlite3.connect(B+'/repo/data/nfl_matchups.sqlite')
obs=pd.read_sql("select team_id,game_id,metric,value,source_updated_at,data from external_observations where source_id in('sharp_advanced','espn_win_rates')",db)
obs['team']=obs.data.map(lambda s:json.loads(s).get('team')); obs['ent']=obs.data.map(lambda s:json.loads(s).get('entity_type'))
pr=obs[obs.metric=='offense.efficiency.pressure_rate_allowed_pct'].drop_duplicates(['game_id','team'],keep='last')
gm=pr.groupby('game_id').team.apply(list).to_dict()
for t in out:
    tt={'WAS':'WSH','LA':'LAR'}.get(t,t)
    mine=pr[pr.team==tt]; out[t]['sharp_off_pressure_allowed_avg']=mine.value.mean(); out[t]['sharp_games']=len(mine)
    opp=[ (g,[x for x in gm[g] if x!=tt]) for g in mine.game_id]
    vals=[pr[(pr.game_id==g)&(pr.team==o[0])].value.iloc[0] for g,o in opp if o]
    out[t]['sharp_def_pressure_rate_proxy']=float(np.mean(vals)) if vals else None
    w=obs[(obs.team==tt)&(obs.ent=='team')]
    for m in ['defense.pass_rush_win_rate_pct','offense.pass_block_win_rate_pct']:
        v=w[w.metric==m]; out[t][m]=float(v.value.iloc[-1]) if len(v) else None
    g=obs[(obs.team==tt)&(obs.metric=='offense.efficiency.epa_per_play')].drop_duplicates('game_id',keep='last')
    out[t]['sharp_game_epa_series']=g.value.round(2).tolist()
# ranks (1 = softest i.e. most allowed)
def rank(fn,asc=False):
    s=pd.Series({t:fn(out[t]) for t in out}).dropna(); return s.rank(ascending=asc,method='min').astype(int).to_dict()
R={'WR_ypt':rank(lambda d:d['WR']['ypt']),'TE_ypt':rank(lambda d:d['TE']['ypt']),'RB_rec_ypt':rank(lambda d:d['RB']['ypt']),
 'WR_yds_pg':rank(lambda d:d['WR']['yds_pg']),'TE_yds_pg':rank(lambda d:d['TE']['yds_pg']),'TE_rec_pg':rank(lambda d:d['TE']['rec_pg']),'RB_rec_pg':rank(lambda d:d['RB']['rec_pg']),
 'RB_ypc':rank(lambda d:d['RB_rush']['ypc']),'RB_rush_yds_pg':rank(lambda d:d['RB_rush']['yds_pg']),'RB_total':rank(lambda d:d['RB_total_yds_pg']),
 'out_ypt':rank(lambda d:d['WR_outside_proxy']['ypt']),'mid_ypt':rank(lambda d:d['WR_middle_proxy']['ypt']),
 'sh_wr':rank(lambda d:d['sharp']['YPT Allowed WR']),'sh_te':rank(lambda d:d['sharp']['YPT Allowed TE']),'sh_rb':rank(lambda d:d['sharp']['YPT Allowed RB']),'sh_out':rank(lambda d:d['sharp']['YPT Allowed Outside']),'sh_slot':rank(lambda d:d['sharp']['YPT Allowed Slot']),
 'blitz':rank(lambda d:d['sharp']['Blitz Rate']),'press':rank(lambda d:d['sharp_def_pressure_rate_proxy']),'third':rank(lambda d:d['third_down_pct_allowed']),'rz':rank(lambda d:d['rz_td_pct_allowed']),'epa':rank(lambda d:d['epa_play_allowed'])}
for t in out: out[t]['ranks']={k:v.get(t) for k,v in R.items()}
json.dump(dict(games=games,teams=out),open(D+'/defense_profiles.json','w'),indent=1,default=float)
print('ok',len(out))
