import pandas as pd
p=pd.read_parquet('/workspace/nfl-database/tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet')
pl=pd.read_parquet('src/players.parquet')[['gsis_id','position']].drop_duplicates('gsis_id').set_index('gsis_id').position
pas=p[(p.pass_attempt==1)&(p.sack!=1)].copy();pas['rpos']=pas.receiver_player_id.map(pl)
s=pas[pas.posteam=='SEA'];tot=s.groupby('week').size();qb=s.groupby('week').passer_player_name.agg(lambda x:x.mode().iat[0])
for n in['C.Kupp','A.Barner']:
  o=s[s.receiver_player_name==n];g=o.groupby('week').agg(opp=('defteam','first'),tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum'),adot=('air_yards','mean'),rz=('yardline_100',lambda y:(y<=20).sum()),lng=('receiving_yards','max'),mid=('pass_location',lambda x:(x=='middle').mean()))
  g['sh']=(g.tgt/tot.reindex(g.index)).round(2);g['qb']=qb.reindex(g.index);print(n);print(g.round(1).to_markdown())
  d=g[g.qb=='S.Darnold'];print('Darnold avg',d[['tgt','rec','yds','sh']].mean().round(2).to_dict(),'last3',g.tail(3)[['tgt','rec','yds']].mean().round(1).to_dict())
c=pas[pas.defteam=='CHI']
t=c[c.rpos=='TE'].groupby(['week','posteam','receiver_player_name']).agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum')).reset_index();print(t.to_markdown(index=False))
lg=pas[pas.rpos=='TE'].groupby(['defteam','week']).agg(rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum')).groupby('defteam').mean()
print('CHI vs TE pg',lg.loc['CHI'].round(2).to_dict(),'lg',lg.mean().round(2).to_dict(),'rank rec',int(lg.rec.rank(ascending=False)['CHI']),'yds',int(lg.yds.rank(ascending=False)['CHI']))
w=c[c.rpos=='WR'];w['zone']=w.pass_location.map(lambda x:'mid' if x=='middle' else 'out')
lw=pas[pas.rpos=='WR'].assign(zone=lambda d:d.pass_location.map(lambda x:'mid' if x=='middle' else 'out')).groupby(['defteam','zone']).receiving_yards.sum().unstack()/7
print('CHI WR ypg mid/out',lw.loc['CHI'].round(1).to_dict(),'lg',lw.mean().round(1).to_dict())
print(w.groupby(['week','posteam','receiver_player_name']).agg(rec=('complete_pass','sum'),yds=('receiving_yards','sum'),mid=('zone',lambda z:(z=='mid').sum())).query('yds>=50').to_markdown())
