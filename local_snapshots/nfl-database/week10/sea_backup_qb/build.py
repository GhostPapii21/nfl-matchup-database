import pandas as pd, numpy as np
d=pd.read_parquet('../bal_secondary/raw/play_by_play_2026.parquet')
s=d[(d.posteam=='SEA')&d.play_type.isin(['pass','run'])].copy()
out=[]
P=lambda *a:out.append(' '.join(str(x) for x in a))
# throw log for Lock
L=d[(d.posteam=='SEA')&(d.passer_player_name=='D.Lock')|((d.posteam=='SEA')&(d.rusher_player_name=='D.Lock'))]
cols=['week','qtr','time','down','ydstogo','yardline_100','score_differential','play_type','pass_length','pass_location','air_yards','yards_gained','complete_pass','sack','qb_hit','interception','pass_touchdown','receiver_player_name','first_down','desc']
cols=[c for c in cols if c in d.columns]
L[cols].to_csv('throw_log.csv',index=False)
for w in [1,2]:
  x=d[(d.posteam=='SEA')&(d.week==w)&(d.passer_player_name=='D.Lock')]
  att=x.pass_attempt.sum()-x.sack.sum(); cmp_=x.complete_pass.sum(); yds=x[x.sack==0].yards_gained.sum() if False else x.passing_yards.fillna(0).sum()
  P(f'## Week {w} Lock: dropbacks {len(x)}, att {int(att)}, cmp {int(cmp_)} ({cmp_/att:.1%}), pass yds {int(yds)}, YPA {yds/att:.2f}, sacks {int(x.sack.sum())}, qb_hit {int(x.qb_hit.sum())}, INT {int(x.interception.sum())}, TD {int(x.pass_touchdown.sum())}')
  a=x[x.sack==0]
  P(' aDOT',round(a.air_yards.mean(),1),'| deep(15+ air) att',int((a.air_yards>=15).sum()),'cmp',int(((a.air_yards>=15)&(a.complete_pass==1)).sum()),'| behind LOS',int((a.air_yards<0).sum()))
  P(' targets:',a.receiver_player_name.value_counts().to_dict())
  P(' catches/yds:',a[a.complete_pass==1].groupby('receiver_player_name').yards_gained.agg(['count','sum']).to_dict('index'))
  t=x[x.down==3]; P(' 3rd down dropbacks',len(t),'conversions',int(t.first_down.sum()))
  P(' Q split att by qtr:',a.groupby('qtr').size().to_dict())
# team splits
P('\n## SEA team by week (pass/run plays excl. kneels; pass rate incl sacks/scrambles via play_type)')
g=s.groupby('week')
tab=pd.DataFrame({'plays':g.size(),'pass_rate':g.apply(lambda x:(x.play_type=='pass').mean()).round(3),
 'neutral_pass_rate':g.apply(lambda x:(x[(x.score_differential.abs()<=7)&(x.qtr<=3)].play_type=='pass').mean()).round(3),
 'sec_per_play':(g.apply(lambda x: (x.game_seconds_remaining.max()-x.game_seconds_remaining.min())/len(x))).round(1)})
P(tab.to_string())
r=s[s.play_type=='run']
sh=r.groupby(['week','rusher_player_name']).size().unstack(1).fillna(0)
sh=sh.loc[:,sh.sum()>=3]; P('\nRB/rush attempts by week:\n'+sh.astype(int).to_string())
p=s[(s.play_type=='pass')&s.receiver_player_name.notna()]
ts=p.groupby(['week','receiver_player_name']).size().unstack(1).fillna(0)
ts=ts.loc[:,ts.sum()>=6]; P('\nTargets by week:\n'+ts.astype(int).to_string())
P('\nTarget share Lock wks1-2 (Lock only) vs Darnold wks3-8:')
lk=p[p.passer_player_name=='D.Lock'].receiver_player_name.value_counts(normalize=True)
dk=p[(p.passer_player_name=='S.Darnold')&(p.week>=3)].receiver_player_name.value_counts(normalize=True)
P(pd.DataFrame({'Lock':lk,'Darnold':dk}).fillna(0).round(3).sort_values('Darnold',ascending=False).head(10).to_string())
# drives wk2
x=d[(d.posteam=='SEA')&(d.week==2)]
dr=x.groupby('drive').agg(plays=('play_id','size'),result=('fixed_drive_result','first'),start=('drive_start_yard_line','first'))
P('\n## Week 2 SEA drives\n'+dr.to_string()); P('Drive results:',dr.result.value_counts().to_dict())
x1=d[(d.posteam=='SEA')&(d.week==1)&(d.passer_player_name=='D.Lock')]
P('Wk1 Lock drives:',x1.groupby('drive').fixed_drive_result.first().value_counts().to_dict())
# ARI defense
a=d[(d.defteam=='ARI')&d.play_type.isin(['pass','run'])]
g=a.groupby('week')
P('\n## ARI defense by week'); P(pd.DataFrame({'opp':g.posteam.first(),'pts_allowed':g.apply(lambda x: x.posteam_score_post.max()),'pass_yds':g.apply(lambda x:x.passing_yards.fillna(0).sum()),'rush_yds':g.apply(lambda x:x[x.play_type=='run'].yards_gained.sum()),'sacks':g.sack.sum(),'ypc':g.apply(lambda x:round(x[x.play_type=='run'].yards_gained.mean(),2))}).to_string())
db=a[a.play_type=='pass']; P('ARI dropbacks faced',len(db),'sack%',round(db.sack.mean()*100,1),'qb_hit%',round(db.qb_hit.mean()*100,1),'EPA/play allowed',round(a.epa.mean(),3),'rush EPA',round(a[a.play_type=="run"].epa.mean(),3))
open('pbp_summary.txt','w').write('\n'.join(out)); print('\n'.join(out))
