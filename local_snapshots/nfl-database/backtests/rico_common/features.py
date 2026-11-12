"""Walk-forward (weeks < W) team/QB features from nflverse pbp. No blitz column exists in pbp: pressure proxy = sack OR qb_hit per dropback."""
import numpy as np, pandas as pd
def week_feats(d,W):
    p=d[d.week<W]; F={}
    ru=p[(p.rush_attempt==1)&(p.qb_kneel!=1)&p.rusher_player_id.notna()&(p.qb_scramble!=1)]
    pav=ru.groupby('rusher_player_id').rushing_yards.mean(); ru=ru.assign(res=ru.rushing_yards-ru.rusher_player_id.map(pav))
    F['lg_ypc']=ru.rushing_yards.mean(); F['def_adj_ypc']=F['lg_ypc']+ru.groupby('defteam').res.mean()
    F['car_pg']=ru.groupby(['rusher_player_id','game_id']).size().groupby(level=0).mean()
    F['ypc']=pav
    db=p[p.qb_dropback==1].copy(); db['press']=((db.sack==1)|(db.qb_hit==1)).astype(int)
    F['def_press']=db.groupby('defteam').press.mean(); F['off_press']=db.groupby('posteam').press.mean(); F['lg_press']=db.press.mean()
    pr=db[db.press==1]; q=pr.groupby('passer_player_id').agg(n=('epa','size'),epa=('epa','mean'),cmp=('complete_pass','mean'),
        ypa=('yards_gained','mean'),sk=('sack','mean'),to=('interception', 'mean'))
    q['to']=q.to+pr.groupby('passer_player_id').fumble_lost.mean().reindex(q.index).fillna(0)
    q=q[q.n>=15]; z=lambda s:(s-s.mean())/s.std()
    q['comp']=z(q.epa)+z(q.cmp)+z(q.ypa)-z(q.sk)-z(q.to)
    F['qbp']=q
    wxp=db[db.game_id.isin(p[(p.roof.isin(['outdoors','open']))&((p.wind.fillna(0)>=15)|p.weather.fillna('').str.lower().str.contains('rain|snow|shower'))].game_id)]
    F['qb_wx_epa']=wxp.groupby('passer_player_id').epa.agg(['mean','size'])
    # starters: top passer by attempts per team-game
    st=p[p.pass_attempt==1].groupby(['posteam','week','passer_player_id']).size().reset_index(name='n').sort_values('n').groupby(['posteam','week']).tail(1)
    F['starters']=st
    return F
def starter(d,team,W):
    x=d[(d.week==W)&(d.posteam==team)&(d.pass_attempt==1)].passer_player_id.value_counts()
    return x.index[0] if len(x) else None
