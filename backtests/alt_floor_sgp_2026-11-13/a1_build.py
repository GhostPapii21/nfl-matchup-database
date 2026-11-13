"""a1: real alt Over prices (FanDuel + median-of-books) joined to nflverse outcomes and PRE-GAME usage features.
Usage features use only weeks < game week. Outcomes attached for scoring only."""
import re, numpy as np, pandas as pd
INV='/workspace/research/historical_nfl_odds_inventory_2026-11-07/sportsbook_latest_verified_pregame.csv'
NV='/workspace/nfl56_pr28/data/historical/nflverse/'
PBP=NV+'pbp_2026_w1_9_pulled_20261112T1116ET.parquet'
MK={'player_reception_yds_alternate':'recyds','player_rush_yds_alternate':'rushyds','player_receptions_alternate':'rec','player_rush_reception_yds_alternate':'rushrec'}
def dec(a): a=float(a); return 1+a/100 if a>0 else 1+100/-a
def norm(n): n=re.sub(r'\b(jr|sr|ii|iii|iv|v)\b','',str(n).lower().replace('.','').replace("'",'')); return re.sub(r'[^a-z]','',n)
d=pd.read_csv(INV,dtype=str)
d=d[(d.pregame_status=='verified_capture_before_start')&(d.period.fillna('FT').isin(['FT','FULL_GAME']))]
d['week']=d.week.astype(float).astype(int); d=d[d.week.between(4,9)]
d['line']=d.line.astype(float); d['dec']=d.price.map(dec)
d['snap']=pd.to_datetime(d.snapshot_timestamp,utc=True); d['ko']=pd.to_datetime(d.event_start_timestamp,utc=True)
assert (d.snap<d.ko).all()
# ---- player alt overs
p=d[d.market.isin(MK)&(d.selection=='Over')].copy(); p['market']=p.market.map(MK)
g=p.groupby(['week','game_id','player','market','line'])
R=g.agg(med_dec=('dec','median'),n_books=('bookmaker','nunique'),snap_min=('snap','min'),snap_max=('snap','max'),ko=('ko','first')).reset_index()
fd=p[p.bookmaker=='fanduel'].groupby(['week','game_id','player','market','line']).dec.last().rename('fd_dec')
R=R.merge(fd.reset_index(),how='left',on=['week','game_id','player','market','line'])
R['hours_pre']=(R.ko-R.snap_max).dt.total_seconds()/3600
# ---- main-line props for reference (main line per player-market = most common line among books, Over/Under)
MM={'player_reception_yds':'recyds','player_rush_yds':'rushyds','player_receptions':'rec','player_rush_reception_yds':'rushrec'}
m=d[d.market.isin(MM)&(d.selection=='Over')].copy(); m['market']=m.market.map(MM)
main=m.groupby(['game_id','player','market']).line.agg(lambda s:s.mode().iloc[0]).rename('main_line').reset_index()
R=R.merge(main,how='left',on=['game_id','player','market'])
# ---- names -> gsis via season roster + team in game
ros=pd.read_parquet(NV+'ros_2026.parquet',columns=['team','full_name','gsis_id','position'])
ros['k']=ros.full_name.map(norm)
R['home']=R.game_id.str.split('_').str[3]; R['away']=R.game_id.str.split('_').str[2]; R['k']=R.player.map(norm)
P=pd.read_parquet(PBP)
P=P[(P.season_type=='REG')|(P.season_type.isna())] if 'season_type' in P else P
# player-game outcomes
pl=P[(P.two_point_attempt!=1)]
ru=pl[(pl.rush_attempt==1)&pl.rusher_player_id.notna()]
re_=pl[(pl.pass_attempt==1)&(pl.sack!=1)&pl.receiver_player_id.notna()]
O1=ru.groupby(['week','game_id','posteam','rusher_player_id']).agg(car=('rush_attempt','size'),rushyds=('rushing_yards','sum')).reset_index().rename(columns={'rusher_player_id':'gsis'})
O2=re_.groupby(['week','game_id','posteam','receiver_player_id']).agg(tgt=('pass_attempt','size'),rec=('complete_pass','sum'),recyds=('receiving_yards','sum')).reset_index().rename(columns={'receiver_player_id':'gsis'})
O=O1.merge(O2,how='outer',on=['week','game_id','posteam','gsis']).fillna({'car':0,'rushyds':0,'tgt':0,'rec':0,'recyds':0})
O['rushrec']=O.rushyds+O.recyds
tc=ru[ru.qb_kneel!=1].groupby(['game_id','posteam']).size().rename('team_car'); tt=re_.groupby(['game_id','posteam']).size().rename('team_tgt')
O=O.merge(tc.reset_index(),how='left',on=['game_id','posteam']).merge(tt.reset_index(),how='left',on=['game_id','posteam'])
O['car_sh']=O.car/O.team_car; O['tgt_sh']=O.tgt/O.team_tgt
O.to_csv('player_game_outcomes_pbp.csv',index=False)
# map names: candidate gsis among roster rows with that key on either team; tie-break by who appears in game outcomes
cand=R[['game_id','player','k','home','away']].drop_duplicates().merge(ros[['k','gsis_id','team','position']],on='k',how='left')
inG=O[['game_id','gsis']].drop_duplicates().assign(ing=1)
cand=cand.merge(inG,how='left',left_on=['game_id','gsis_id'],right_on=['game_id','gsis']).drop(columns='gsis')
cand['score']=cand.ing.fillna(0)*2+((cand.team==cand.home)|(cand.team==cand.away)).astype(int)
cand=cand.sort_values('score').groupby(['game_id','player']).tail(1)
cand=cand[cand.score>=1]
R=R.merge(cand[['game_id','player','gsis_id','position']].rename(columns={'gsis_id':'gsis'}),how='left',on=['game_id','player'])
print('unmapped player-games',R[R.gsis.isna()][['game_id','player']].drop_duplicates().shape[0],'of',R[['game_id','player']].drop_duplicates().shape[0])
R=R[R.gsis.notna()]
# actual outcome; if player not in pbp outcomes for that game -> did not record a touch: actual=0 if he played? unknown -> mark
R=R.merge(O[['game_id','gsis','posteam','car','tgt','rushyds','recyds','rec','rushrec']].rename(columns={'posteam':'team'}),how='left',on=['game_id','gsis'])
R['actual']=[r[m] if pd.notna(r['team']) else np.nan for _,r in R[['market','team','rushyds','recyds','rec','rushrec']].iterrows() for m in [r['market']]]
# ---- pre-game usage (weeks < W, last 6 games with >=1 touch/target)
feat={}
for (gs,w) in R[['gsis','week']].drop_duplicates().itertuples(index=False):
    h=O[(O.gsis==gs)&(O.week<w)].sort_values('week').tail(6)
    feat[(gs,w)]=h
rows=[]
for i,r in R.iterrows():
    h=feat[(r.gsis,r.week)]; v=h[r.market].values if len(h) else np.array([])
    rows.append(dict(n_prior=len(h),p25=np.percentile(v,25) if len(v) else np.nan,p40=np.percentile(v,40) if len(v) else np.nan,
        med=np.median(v) if len(v) else np.nan,min_prior=v.min() if len(v) else np.nan,
        tgt_sh=h.tgt_sh.mean() if len(h) else np.nan,med_tgt=h.tgt.median() if len(h) else np.nan,
        car_sh4=h.car_sh.tail(4).mean() if len(h) else np.nan,n60=int((h.car_sh.tail(4)>=0.6).sum()) if len(h) else 0,
        med_car=h.car.median() if len(h) else np.nan))
R=pd.concat([R.reset_index(drop=True),pd.DataFrame(rows)],axis=1)
R.drop(columns=['k','home','away']).to_csv('alt_over_rungs_with_features.csv',index=False)
# ---- alt totals (game)
t=d[d.market.isin(['totals','alternate_totals'])].copy()
gt=t.groupby(['week','game_id','market','selection','line']).agg(med_dec=('dec','median'),n_books=('bookmaker','nunique')).reset_index()
gfd=t[t.bookmaker=='fanduel'].groupby(['week','game_id','market','selection','line']).dec.last().rename('fd_dec').reset_index()
gt=gt.merge(gfd,how='left',on=['week','game_id','market','selection','line'])
mainT=t[t.market=='totals'].groupby('game_id').line.agg(lambda s:s.mode().iloc[0]).rename('main_total')
gt=gt.merge(mainT.reset_index(),how='left',on='game_id')
sc=P.groupby('game_id').agg(tot=('total_home_score','max'),tot2=('total_away_score','max')); sc['act_total']=sc.tot+sc.tot2
gt=gt.merge(sc[['act_total']].reset_index(),how='left',on='game_id')
gt.to_csv('alt_totals_quotes.csv',index=False)
print(R.groupby(['week','market']).size().unstack(fill_value=0)); print('actual missing',R.actual.isna().sum())
print(gt[gt.market=='alternate_totals'].groupby(['week','selection']).size())
