import pandas as pd, sqlite3, json, os, numpy as np
B='/workspace/nfl-database'
p=pd.read_parquet(f'{B}/fixes/src/play_by_play_2026.parquet')
p=p[(p.season_type=='REG')&(p.week<=7)]
slate=json.load(open(f'{B}/week8/slate.json'))['games']
M={'LAR':'LA','WSH':'WAS'}; norm=lambda t:M.get(t,t)
games=[(norm(g['matchup'].split(' @ ')[0]),norm(g['matchup'].split(' @ ')[1])) for g in slate]+[('CAR','GB')]
teams=sorted({t for g in games for t in g})
fx=sqlite3.connect(f'{B}/fixes/fixes.sqlite')
role=pd.read_sql('select * from fix_player_role',fx)
qbr=pd.read_sql('select * from fix_qb_rushing',fx)
ngr=pd.read_parquet('src/ngs_receiving.parquet');ngr=ngr[(ngr.season==2026)&(ngr.week==0)].set_index('player_gsis_id')
ngu=pd.read_parquet('src/ngs_rushing.parquet');ngu=ngu[(ngu.season==2026)&(ngu.week==0)].set_index('player_gsis_id')
inj=json.load(open(f'{B}/week8/injuries.json'))['teams']
injmap={}
for t,L in inj.items():
  for x in L: injmap[(norm(t),x['name'])]=x['designation']
D=json.load(open(f'{B}/week8/defense/defense_profiles.json'))['teams']
ros={}
for t in teams:
  f=f'{B}/week8/rosters/{ {"LA":"LAR","WAS":"WSH"}.get(t,t)}.json'
  if not os.path.exists(f): f=f'{B}/week8/rosters/{t}.json'
  ros[t]={x['name']:x for x in json.load(open(f))['players']} if os.path.exists(f) else None
pa=p[p.pass_attempt==1&p.receiver_player_id.notna()] if False else p[(p.pass_attempt==1)&p.receiver_player_id.notna()&(p.two_point_attempt!=1)]
ru=p[(p.rush_attempt==1)&p.rusher_player_id.notna()&(p.qb_kneel!=1)&(p.two_point_attempt!=1)]
pa=pa.assign(rz=pa.yardline_100<=20,third=pa.down==3,deep=pa.air_yards>=20,scr=pa.air_yards<=0,mid=pa.pass_location=='middle',big=(pa.complete_pass==1)&(pa.yards_gained>=20))
ru=ru.assign(rz=ru.yardline_100<=20,i10=ru.yardline_100<=10,mid=ru.run_location=='middle')
tm={}
for t in teams:
  a=pa[pa.posteam==t];r=ru[ru.posteam==t]
  tm[t]=dict(rz_t=a.rz.sum(),third_t=a.third.sum(),rz_c=r.rz.sum(),i10_c=r.i10.sum())
rec=pa.groupby(['posteam','receiver_player_id']).agg(tg=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),adot=('air_yards','mean'),deep=('deep','mean'),scr=('scr','mean'),mid=('mid','mean'),loc_n=('pass_location','count'),yac=('yards_after_catch','mean'),rz=('rz','sum'),third=('third','sum'),big=('big','sum')).reset_index()
rus=ru.groupby(['posteam','rusher_player_id']).agg(car=('play_id','size'),ryds=('rushing_yards','sum'),rz_c=('rz','sum'),i10=('i10','sum'),mid=('mid','mean'),locn=('run_location','count')).reset_index()
def r1(x,n=1): return None if x is None or (isinstance(x,float) and np.isnan(x)) else round(float(x),n)
out={}
for t in teams:
  rl=role[role.team==t]
  pl=[]
  for _,R in rl.iterrows():
    pos=R.position; g=R.gsis_id
    if pos not in('WR','TE','RB','FB','QB'): continue
    meaningful = max(R.season_target_share or 0,R.current_target_share_l3 or 0)>=0.08 or max(R.season_carry_share or 0,R.current_carry_share_l3 or 0)>=0.15 or (R.current_snap_pct_l3 or 0)>=0.40
    if pos=='QB': meaningful=False
    if not meaningful: continue
    e=dict(player=R.player,gsis=g,team=t,pos=pos,gp=int(R.games_played),last_wk=int(R.last_played_week) if pd.notna(R.last_played_week) else None,
      tgt_share_season=r1(R.season_target_share*100),tgt_share_l3=r1((R.current_target_share_l3 or 0)*100),car_share_season=r1(R.season_carry_share*100),car_share_l3=r1((R.current_carry_share_l3 or 0)*100),snap_l3=r1((R.current_snap_pct_l3 or 0)*100),tgt_pg=r1(R.targets_per_game),car_pg=r1(R.carries_per_game))
    x=rec[rec.receiver_player_id==g]; x=x[x.posteam==t] if len(x[x.posteam==t]) else x
    if len(x):
      x=x.iloc[0]; e.update(tg=int(x.tg),rec=int(x.rec),rec_yds=int(x.yds),catch_pct=r1(100*x.rec/x.tg),adot=r1(x.adot),deep20_rate=r1(100*x.deep),screen_rate=r1(100*x.scr),middle_share=r1(100*x.mid) if x.loc_n else None,yac_per_rec=r1(x.yac),rz_tgts=int(x.rz),rz_tgt_share=r1(100*x.rz/max(tm[t]['rz_t'],1)),third_tgts=int(x.third),third_tgt_share=r1(100*x.third/max(tm[t]['third_t'],1)),rec20=int(x.big),big_play_share=r1(100*x.big/max(x.rec,1)))
    y=rus[rus.rusher_player_id==g]; y=y[y.posteam==t] if len(y[y.posteam==t]) else y
    if len(y):
      y=y.iloc[0]; e.update(car=int(y.car),rush_yds=int(y.ryds),ypc=r1(y.ryds/y.car),rz_car=int(y.rz_c),i10_car=int(y.i10),i10_share=r1(100*y.i10/max(tm[t]['i10_c'],1)),inside_run_share=r1(100*y.mid) if y.locn else None)
    if g in ngr.index:
      n=ngr.loc[g]; n=n.iloc[0] if isinstance(n,pd.DataFrame) else n
      e.update(ngs_adot=r1(n.avg_intended_air_yards),ngs_sep=r1(n.avg_separation),ngs_cushion=r1(n.avg_cushion),ngs_yacoe=r1(n.avg_yac_above_expectation),ngs_catch=r1(n.catch_percentage))
    if g in ngu.index:
      n=ngu.loc[g]; n=n.iloc[0] if isinstance(n,pd.DataFrame) else n
      e.update(ngs_ryoe_att=r1(n.rush_yards_over_expected_per_att,2),ngs_8box=r1(n.percent_attempts_gte_eight_defenders))
    e['injury']=injmap.get((t,R.player),'none listed')
    e['on_current_roster']= (None if ros[t] is None else (R.player in ros[t]))
    pl.append(e)
  # team ranks
  wr=sorted([q for q in pl if q['pos']=='WR'],key=lambda q:-(q['tgt_share_l3'] or 0))
  te=sorted([q for q in pl if q['pos']=='TE'],key=lambda q:-(q['tgt_share_l3'] or 0))
  allr=sorted([q for q in pl if q['pos']!='QB'],key=lambda q:-max(q['tgt_share_l3'] or 0,q['tgt_share_season'] or 0))
  top2={q['gsis'] for q in allr[:2]}
  for q in pl:
    T=[];g=lambda k,d=0:(q.get(k) if q.get(k) is not None else d)
    ts=max(g('tgt_share_l3'),g('tgt_share_season')); cs=max(g('car_share_l3'),g('car_share_season'))
    tgn=g('tg'); small=tgn<15
    if q['pos']=='WR':
      if ts>=20 and (g('adot',99)<=10.5 or g('catch_pct')>=66): T.append('Volume/possession')
      elif ts>=20: T.append('Volume (target-share) receiver')
      if tgn>=12 and (g('adot')>=13 or g('deep20_rate')>=25 or (g('big_play_share')>=25 and g('rec')>=6)): T.append('Explosive/deep')
      if tgn>=12 and q.get('middle_share') is not None:
        if q['middle_share']>=35: T.append('Slot (middle-target proxy)')
        elif q['middle_share']<=20: T.append('Boundary (L/R-target proxy)')
      if tgn>=12 and g('adot',99)<=6.5 and (g('yac_per_rec')>=6 or g('ngs_yacoe')>=1): T.append('Screen/YAC')
      if g('rz_tgts')>=4 and g('rz_tgt_share')>=20: T.append('Red-zone target')
      if g('third_tgts')>=6 and g('third_tgt_share')>=22: T.append('3rd-down chain mover')
      if ts<20: T.append('WR2/WR3 depth' if ts>=10 else 'Rotational WR (<10% tgt)')
    if q['pos']=='TE':
      if q['gsis'] in top2 and ts>=15: T.append('TE-as-primary')
      if tgn>=12 and g('adot')>=8 and g('middle_share')>=40: T.append('Move/seam TE')
      if g('snap_l3')>=70 and g('tgt_share_l3')<12: T.append('Blocking/inline TE')
      if g('rz_tgts')>=3 and g('rz_tgt_share')>=15: T.append('Red-zone TE')
      if tgn>=12 and g('adot',99)<=6: T.append('Check-down/blitz-beater TE')
      if not T: T.append('Secondary TE (low volume)')
    if q['pos'] in('RB','FB'):
      tpg=g('tg')/max(q['gp'],1)
      if cs>=40 and q.get('inside_run_share') is not None and q['inside_run_share']>=45: T.append('Early-down/between-tackles')
      elif cs>=40: T.append('Early-down lead back')
      if cs>=35 and (tpg>=3 or ts>=10): T.append('Rush-receive')
      if cs<35 and (ts>=8 or tpg>=2.5): T.append('Receiving/3rd-down back')
      if g('i10_car')>=3 and g('i10_share')>=40: T.append('Goal-line/RZ back')
      if g('ngs_ryoe_att',-9)>=0.5 and g('car_pg')>=12: T.append('Elite rusher (RYOE)')
      if 15<=cs<50: T.append('Committee member')
      ir=q.get('inside_run_share')
      if ir is not None and g('car')>=20: q['run_tendency']='inside' if ir>=55 else ('outside' if ir<=35 else 'balanced')
    q['types']=T; q['primary']=T[0] if T else None; q['secondary']=T[1:]
    if small: q['sample_note']=f'small sample ({tgn} tgts)'
  qs=[]
  for _,Q in qbr[qbr.qb_gsis.isin(p[p.posteam==t].passer_player_id.dropna().unique())].iterrows():
    a=p[(p.passer_player_id==Q.qb_gsis)&(p.pass_attempt==1)&(p.posteam==t)]
    if len(a)<30: continue
    gms=a.game_id.nunique()
    qs.append(dict(player=Q.qb,gsis=Q.qb_gsis,team=t,pos='QB',starts=int(Q.starts_ge10_dropbacks),att_pg=r1(len(a)/gms),adot=r1(a.air_yards.mean()),deep20_rate=r1(100*(a.air_yards>=20).mean()),scramble_rate=r1(100*Q.scr_rate_per_dropback),scr_att_pg=r1(Q.scr_att_pg),designed_runs_pg=r1(Q.des_att_pg),rush_yds_pg=r1(Q.rush_yds_ex_kneel_pg),injury=injmap.get((t,Q.qb),'none listed')))
  for q in qs:
    T=[]
    T.append('High-volume passer' if q['att_pg']>=36 else ('Low-volume passer' if q['att_pg']<=28 else 'Mid-volume passer'))
    if q['adot']>=8.5: T.append('Aggressive/deep (aDOT)')
    elif q['adot']<=6.5: T.append('Short-area/checkdown (aDOT)')
    if q['designed_runs_pg']>=3: T.append('Designed-run QB')
    if q['scramble_rate']>=6: T.append('Scrambler')
    q['types']=T; q['primary']=T[0]; q['secondary']=T[1:]
  out[t]=pl+qs
json.dump(dict(built='2026-10-29',data_through_week=7,teams=out),open('player_types.json','w'),indent=1,default=str)
print(sum(len(v) for v in out.values()))
