# SEA RB usage 2026 (Darnold games) + Charbonnet 2025 baseline + Jacobs 2026 return. nflverse pbp/snaps.
import pandas as pd
P6=pd.read_parquet('/workspace/nfl-database/tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet')
S6=pd.read_parquet('/tmp/snap_counts_2026.parquet')
P5=pd.read_parquet('/tmp/play_by_play_2025.parquet')
def rb(P,team,names=None):
    p=P[(P.posteam==team)&(P.season_type=='REG') if 'season_type' in P else (P.posteam==team)]
    ru=p[p.rush_attempt==1].groupby(['week','rusher_player_name']).size().rename('car')
    ry=p[p.rush_attempt==1].groupby(['week','rusher_player_name']).rushing_yards.sum().rename('ryd')
    tg=p[p.pass_attempt==1].groupby(['week','receiver_player_name']).size().rename('tgt')
    rc=p[p.complete_pass==1].groupby(['week','receiver_player_name']).size().rename('rec')
    yd=p[p.complete_pass==1].groupby(['week','receiver_player_name']).receiving_yards.sum().rename('recyd')
    tc=p[p.rush_attempt==1].groupby('week').size().rename('team_car'); tt=p[p.pass_attempt==1].groupby('week').size().rename('team_tgt')
    a=pd.concat([ru,ry],axis=1).reset_index().rename(columns={'rusher_player_name':'pl'})
    b=pd.concat([tg,rc,yd],axis=1).reset_index().rename(columns={'receiver_player_name':'pl'})
    m=a.merge(b,on=['week','pl'],how='outer').fillna(0).merge(tc,on='week').merge(tt,on='week')
    m['car_sh']=(m.car/m.team_car).round(2); m['tgt_sh']=(m.tgt/m.team_tgt).round(2)
    if names: m=m[m.pl.str.contains('|'.join(names))]
    return m
print('== SEA RBs 2026 ==');print(rb(P6,'SEA',['Holani','Wilson','Price','Charbonnet','Jones','Russell']).sort_values(['week','car'],ascending=[True,False]).to_string(index=False))
s=S6[(S6.team=='SEA')&(S6.position=='RB')][['week','player','offense_snaps','offense_pct']];print(s.sort_values(['week','offense_pct'],ascending=[True,False]).to_string(index=False))
print('== Charbonnet 2025 ==');c=rb(P5,'SEA',['Charbonnet']);print(c.to_string(index=False));print(c[['car','ryd','tgt','rec','recyd','car_sh','tgt_sh']].mean().round(2))
print('== Jacobs 2026 ==');print(rb(P6,'GB',['Jacobs']).to_string(index=False))
print(S6[S6.player.str.contains('Josh Jacobs')][['week','offense_snaps','offense_pct']].to_string(index=False))
