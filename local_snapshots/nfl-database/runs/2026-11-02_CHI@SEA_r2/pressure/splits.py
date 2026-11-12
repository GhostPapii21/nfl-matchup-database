import pandas as pd
p=pd.read_parquet('../src/play_by_play_2026.parquet')
d=p[(p.posteam=='SEA')&(p.qb_dropback==1)&(p.passer_player_name.fillna(p.name if 'name' in p else '').str.contains('Darnold',na=False)|((p.posteam=='SEA')&(p.qb_dropback==1)&p.name.fillna('').str.contains('Darnold')))].copy()
d=d[d.season_type=='REG'] if 'season_type' in d else d
d['press']=((d.sack==1)|(d.qb_hit==1)|(d.qb_scramble==1)).astype(int)
d['att']=((d.pass_attempt==1)&(d.sack==0)&(d.qb_scramble==0)).astype(int)
def summ(g):
    a=g[g.att==1]
    return pd.Series(dict(dropbacks=len(g),att=len(a),cmp_pct=round(a.complete_pass.mean()*100,1),ypa=round(a.passing_yards.fillna(0).sum()/max(len(a),1),2),
      adot=round(a.air_yards.mean(),1),short_le5=round((a.air_yards<=5).mean()*100,1),sacks=int(g.sack.sum()),sack_rate=round(g.sack.mean()*100,1),int_=int(g.interception.sum()),epa_db=round(g.epa.mean(),3)))
print('weeks',sorted(d.week.unique()))
print(d.groupby('press').apply(summ).to_string())
a=d[d.att==1]
t=a.groupby(['press','receiver_player_name']).agg(tgt=('att','size'),rec=('complete_pass','sum'),yds=('passing_yards','sum'),adot=('air_yards','mean')).reset_index()
t['share']=t.groupby('press').tgt.transform(lambda x:(x/x.sum()*100).round(1))
print(t.sort_values(['press','tgt'],ascending=[True,False]).round(1).to_string())
# hit-only (excluding sacks/scrambles = actual throws under hit)
h=a[a.qb_hit==1]; print('throws with qb_hit:',len(h)); print(h.receiver_player_name.value_counts().to_string())
g=d.groupby(['week','defteam']).agg(pyds=('passing_yards','sum'),sacks=('sack','sum'),hits=('qb_hit','sum'),scr=('qb_scramble','sum'),db=('qb_dropback','sum')).reset_index()
g['sk_plus_hit']=g.sacks+g.hits; g['press_rate']=(d.groupby('week').press.mean().values*100).round(1)
print(g.to_string())
print('corr pyds~sk+hit',round(g.pyds.corr(g.sk_plus_hit),2))
