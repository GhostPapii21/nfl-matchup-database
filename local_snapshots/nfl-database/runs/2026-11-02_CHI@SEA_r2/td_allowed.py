import pandas as pd
p=pd.read_parquet('tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet')
pl=pd.read_parquet('runs/2026-11-02_CHI@SEA_r2/src/players.parquet')[['gsis_id','position']].drop_duplicates('gsis_id').set_index('gsis_id').position
p=p[p.season_type=='REG'] if 'season_type' in p else p
td=p[(p.touchdown==1)&(p.td_team==p.posteam)&((p.rush==1)|(p.pass_attempt==1))].copy()
td['pid']=td.td_player_id; td['pos']=td.pid.map(pl); td['kind']=td.pass_attempt.map({1:'rec',0:'rush'})
td['yds']=td.yards_gained; td['rz']=td.yardline_100<=20; td['in5']=td.yardline_100<=5
td['expl']=((td.kind=='rush')&(td.yds>=10))|((td.kind=='rec')&(td.yds>=20))
# drives: RZ trips
p['rzd']=p.yardline_100<=20
dr=p[p.posteam.notna()&p.drive.notna()].groupby(['game_id','posteam','defteam','drive']).agg(rz=('rzd','max'),td=('touchdown',lambda x:0)).reset_index()
tdd=td.groupby(['game_id','posteam','drive']).size().rename('t').reset_index()
dr=dr.merge(tdd,on=['game_id','posteam','drive'],how='left');dr['t']=dr.t.fillna(0)>0
games=p.groupby('defteam').game_id.nunique()
L=[]
for d in ['SEA','CHI']:
    x=td[td.defteam==d][['week','posteam','td_player_name','pos','kind','yds','rz','in5','expl']].sort_values('week')
    print(f'\n## TDs allowed by {d}\n'+x.to_markdown(index=False))
    g=games[d]; r=dr[(dr.defteam==d)&dr.rz]
    print(f"{d}: games {g}, TDs {len(x)}, rush {(x.kind=='rush').sum()} ({(x.kind=='rush').sum()/g:.2f}/g), rec {(x.kind=='rec').sum()} ({(x.kind=='rec').sum()/g:.2f}/g); by pos {x.pos.value_counts().to_dict()}; rec by pos {x[x.kind=='rec'].pos.value_counts().to_dict()}; RZ-origin {x.rz.sum()}, outside-RZ {(~x.rz).sum()}, explosive {x.expl.sum()}; RZ trips {len(r)} ({len(r)/g:.2f}/g), RZ TD% {r.t.mean():.1%}")
r=dr[dr.rz]; print(f"LEAGUE: TD/team-game {len(td)/games.sum():.2f}, rush {(td.kind=='rush').sum()/games.sum():.2f} rec {(td.kind=='rec').sum()/games.sum():.2f}, RZ trips/g {len(r)/games.sum():.2f}, RZ TD% {r.t.mean():.1%}, rec TD pos share {td[td.kind=='rec'].pos.value_counts(normalize=True).round(2).to_dict()}")
# TE vs SEA
pas=p[(p.pass_attempt==1)&(p.sack!=1)].copy(); pas['rpos']=pas.receiver_player_id.map(pl)
te=pas[pas.rpos=='TE']
def tes(d):
    t=te[te.defteam==d]; g=t.groupby(['week','posteam','receiver_player_name']).agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum')).reset_index()
    pg=t.groupby('week').agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum'))
    return g,pg
g,pg=tes('SEA'); print('\n## TEs vs SEA\n'+g.to_markdown(index=False)); print(pg.mean().round(1).to_dict())
lg=te.groupby(['defteam','game_id']).agg(rec=('complete_pass','sum'),yds=('receiving_yards','sum')).groupby('defteam').mean()
lg['yrk']=lg.yds.rank(ascending=False);lg['rrk']=lg.rec.rank(ascending=False); print('SEA rank (1=most allowed):',lg.loc['SEA'].round(1).to_dict(),'league avg',lg.mean().round(1).to_dict())
# Loveland
c=pas[pas.posteam=='CHI']; tot=c.groupby('week').size()
lv=c[c.receiver_player_name.str.contains('Loveland',na=False)]
lg2=lv.groupby('week').agg(tgt=('play_id','size'),rec=('complete_pass','sum'),yds=('receiving_yards','sum'),td=('pass_touchdown','sum'),rz_tgt=('yardline_100',lambda y:(y<=20).sum()))
lg2['share']=(lg2.tgt/tot.reindex(lg2.index)).round(3); lg2['qb']=c.groupby('week').passer_player_name.agg(lambda s:s.mode().iat[0]).reindex(lg2.index)
print('\n## Loveland\n'+lg2.to_markdown())
km=c[c.receiver_player_name.str.contains('Kmet',na=False)].groupby('week').size(); print('Kmet tgts by wk',km.to_dict())
