import pandas as pd, numpy as np
S='/workspace/nfl-database/sources/nflverse/'
p=pd.read_csv(S+'pbp_2026.csv.gz',low_memory=False)
p=p[(p.season_type=='REG')&(p.week<=8)&p.receiver_player_id.notna()&(p.pass_attempt==1)]
r=pd.read_csv(S+'roster_2026.csv',low_memory=False)
pos=r.drop_duplicates('gsis_id').set_index('gsis_id')['position']
p['pos']=p.receiver_player_id.map(pos)
p['opp']=p.defteam
g=p.groupby(['receiver_player_id','receiver_player_name','pos','posteam','week','opp']).agg(tgt=('pass_attempt','size'),rec=('complete_pass','sum'),yds=('yards_gained',lambda s:0),mid=('pass_location',lambda s:(s=='middle').mean()),adot=('air_yards','mean')).reset_index()
yd=p[p.complete_pass==1].groupby(['receiver_player_id','week']).receiving_yards.sum() if 'receiving_yards' in p else p[p.complete_pass==1].groupby(['receiver_player_id','week']).yards_gained.sum()
g['yds']=g.set_index(['receiver_player_id','week']).index.map(yd).fillna(0).values
# pre-season cols
SLOT={'J.Downs','C.Lamb','K.Concepcion','K.Shakir','C.Tate','A.Iosivas','R.Shaheed','D.Mooney'}
vb=g[g.opp=='BAL']
rows=[]
for _,x in vb.iterrows():
    te=x.pos=='TE'
    slot=x.receiver_player_name in SLOT
    if not(te or slot): continue
    oth=g[(g.receiver_player_id==x.receiver_player_id)&(g.opp!='BAL')]
    n=len(oth)
    d=dict(week=x.week,team=x.posteam,player=x.receiver_player_name,role='TE' if te else 'slot WR',
      vb_tgt=x.tgt,vb_rec=x.rec,vb_yds=x.yds,n_base=n,
      b_tgt=oth.tgt.mean(),b_rec=oth.rec.mean(),b_yds=oth.yds.mean(),med_rec=oth.rec.median(),med_yds=oth.yds.median())
    d['d_yds_avg']=x.yds-d['b_yds'];d['d_yds_med']=x.yds-d['med_yds'];d['d_rec']=x.rec-d['b_rec']
    d['held_under']='UNDER' if x.yds<d['med_yds'] and x.yds<d['b_yds'] else ('OVER' if x.yds>d['med_yds'] and x.yds>d['b_yds'] else 'MIXED')
    rows.append(d)
o=pd.DataFrame(rows).sort_values(['week','role']).round(1)
o=o[(o.vb_tgt>=2)|(o.b_tgt>=3)]
o.to_csv('hamilton_test.csv',index=False);print(o.to_string())
for k,s in [('ALL',o),('TE',o[o.role=='TE']),('SLOT',o[o.role!='TE'])]:
    print(k,len(s),s.held_under.value_counts().to_dict(),'avg dYds vs mean',round(s.d_yds_avg.mean(),1),'vs med',round(s.d_yds_med.mean(),1),'dRec',round(s.d_rec.mean(),2))
