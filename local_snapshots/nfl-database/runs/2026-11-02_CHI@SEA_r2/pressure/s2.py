import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V,pandas as pd
e=V.Engine()
s,i=e.sim(dict(player='AJ Barner',team='SEA',opp='CHI',market='rec',spread=-3.0,rungs=[2.5,3.5,4.5],current_qb='Sam Darnold'))
print('Barner n',i['n_games'],{m:(s[m]['cmedian'],{k:round(v,3) for k,v in s[m]['rungs'].items()}) for m in('mc','bias','gr')})
json.dump(dict(s=s,i=i),open('raw_barner.json','w'),default=float)
p=pd.read_parquet('../src/play_by_play_2026.parquet')
a=p[(p.posteam=='SEA')&(p.passer_player_name=='S.Darnold')&(p.pass_attempt==1)]
print(a.groupby('week').agg(pyds=('passing_yards','sum'),barner_rec=('complete_pass',lambda x:int(((a.loc[x.index,'receiver_player_name']=='A.Barner')&(x==1)).sum())),barner_tgt=('receiver_player_name',lambda x:int((x=='A.Barner').sum()))))
c=p[(p.defteam=='CHI')&(p.pass_attempt==1)]
