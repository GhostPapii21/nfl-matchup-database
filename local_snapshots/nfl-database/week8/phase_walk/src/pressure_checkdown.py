import pandas as pd,numpy as np
p=pd.read_parquet('play_by_play_2026.parquet');f=pd.read_parquet('ftn.parquet')
ro=pd.read_parquet('roster.parquet')[['gsis_id','position']].drop_duplicates('gsis_id')
p=p[p.season_type=='REG'] if 'season_type' in p else p
d=p[(p.qb_dropback==1)&p.play_type.isin(['pass','run','no_play'])].merge(f[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers','is_screen_pass']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
d['blitz']=(d.n_blitzers>0).astype(float).where(d.n_blitzers.notna());d['five']=(d.n_pass_rushers>=5).astype(float).where(d.n_pass_rushers.notna())
d['press']=((d.sack==1)|(d.qb_hit==1)|(d.qb_scramble==1)).astype(float)
print('FTN merge cov',d.n_blitzers.notna().mean().round(3),'wkmax',d.week.max())
def L4(x,t,col):
  w=sorted(x[x[col]==t].week.unique())[-4:];return x[(x[col]==t)&x.week.isin(w)]
print('\n## DEF blitz/pressure (season | last4)  league:',d.blitz.mean().round(3),d.five.mean().round(3),d.press.mean().round(3))
for t in ['MIN','CLE','IND','LAC','DEN']:
  s=d[d.defteam==t];l=L4(d,t,'defteam');print(t,*(round(v,3) for v in [s.blitz.mean(),s.five.mean(),s.press.mean(),l.blitz.mean(),l.five.mean(),l.press.mean()]),'dropbacks',len(s))
pa=d[(d.pass_attempt==1)&d.receiver_player_id.notna()].merge(ro,left_on='receiver_player_id',right_on='gsis_id',how='left')
pa['ry']=pa.receiving_yards.fillna(0)
rb=pa[pa.position=='RB'];lg=rb.ry.sum()/len(rb)
print('\n## QBs: blitz faced, press rate, RB tgt share all/blitz/press/clean, aDOT, short(<=0 air) rate, top receivers when blitzed')
for t in ['DET','LA','PIT','JAX','KC']:
  q=pa[pa.posteam==t];qb=q.passer_player_name.value_counts().index[0];q=q[q.passer_player_name==qb];db=d[(d.posteam==t)&(d.passer_player_name==qb)]
  sh=lambda x:round((x.position=='RB').mean(),3)
  print(t,qb,'blitzfaced',round(db.blitz.mean(),3),'press',round(db.press.mean(),3),'RBsh',sh(q),'blitz',sh(q[q.blitz==1]),'press',sh(q[q.press==1]),'clean',sh(q[q.press==0]),'aDOT',round(q.air_yards.mean(),1),'aDOTblitz',round(q[q.blitz==1].air_yards.mean(),1),'behindLOS',round((q.air_yards<=0).mean(),3))
  for nm,sub in [('blitz',q[q.blitz==1]),('noblitz',q[q.blitz==0])]:
    v=sub.receiver_player_name.value_counts(normalize=True).head(5).round(3);print('  ',nm,len(sub),dict(v))
print('\n## RB YPT allowed, QB/offense-adjusted (league RB YPT',round(lg,2),')')
for t in ['MIN','CLE','IND','LAC','DEN']:
  s=rb[rb.defteam==t];rows=[]
  for g,gg in s.groupby('game_id'):
    o=gg.posteam.iloc[0];base=rb[(rb.posteam==o)&(rb.defteam!=t)];rows.append((o,len(gg),gg.ry.sum(),base.ry.sum()/len(base)))
  r=pd.DataFrame(rows,columns=['off','t','y','base']);act=r.y.sum()/r.t.sum();exp=(r.base*r.t).sum()/r.t.sum()
  print(t,'allowed',round(act,2),'expected from offenses faced',round(exp,2),'ratio',round(act/exp,2),'adj YPT',round(lg*act/exp,2),r.round(2).values.tolist())
print('\n## receiving player YPT by blitz')
for n,t in [('J.Gibbs','DET'),('J.Warren','PIT'),('B.Tuten','JAX'),('K.Williams','LA'),('P.Nacua','LA')]:
  x=pa[(pa.receiver_player_name==n)&(pa.posteam==t)];print(n,'YPT',round(x.ry.mean(),2),'blitz',round(x[x.blitz==1].ry.mean(),2),len(x[x.blitz==1]),'noblitz',round(x[x.blitz==0].ry.mean(),2))
