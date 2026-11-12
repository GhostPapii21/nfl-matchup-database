import pandas as pd,json
p=pd.read_parquet('/workspace/nfl-database/tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet')
print('weeks',sorted(p.week.unique()))
pas=p[(p.pass_attempt==1)&(p.sack!=1)]
for tm,names in [('CHI',['R.Johnson','K.Monangai','D.Swift']),('SEA',['J.Price','K.Walker','Z.Charbonnet','G.Holani','R.Shaheed','J.Smith-Njigba','C.Kupp','A.Barner','E.Saubert'])]:
  s=pas[pas.posteam==tm];tot=s.groupby('week').size();qb=s.groupby('week').passer_player_name.agg(lambda x:x.mode().iat[0])
  r=p[(p.posteam==tm)&(p.rush_attempt==1)];rt=r.groupby('week').size()
  print('==',tm,'QB',qb.to_dict())
  for n in names:
    t=s[s.receiver_player_name==n].groupby('week').agg(tgt=('play_id','size'),rec=('complete_pass','sum'),ryd=('receiving_yards','sum'))
    c=r[r.rusher_player_name==n].groupby('week').agg(car=('play_id','size'),rush=('rushing_yards','sum'))
    g=t.join(c,how='outer').fillna(0);g['tsh']=(g.tgt/tot.reindex(g.index)).round(2);g['csh']=(g.car/rt.reindex(g.index)).round(2)
    print(n);print(g.to_string())
