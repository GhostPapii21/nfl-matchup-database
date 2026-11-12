import pandas as pd
p=pd.read_parquet('tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet'); p=p[p.season_type=='REG']
qbm=p[p.pass_attempt==1].groupby(['game_id','posteam']).passer_player_name.agg(lambda s:s.mode().iat[0])
p['gqb']=[qbm.get((g,t)) for g,t in zip(p.game_id,p.posteam)]
# TD and FG counts per team game (offense only; non-offensive TDs separate)
off=p[(p.touchdown==1)&(p.td_team==p.posteam)&((p.rush==1)|(p.pass_attempt==1))]
fg=p[(p.field_goal_attempt==1)&(p.field_goal_result=='made')]
ng=p.groupby('posteam').game_id.nunique()
print('lg offTD/g',round(len(off)/ng.sum(),2),'FG/g',round(len(fg)/ng.sum(),2))
for t,qb in (('CHI','C.Williams'),('SEA','S.Darnold')):
    g=p[(p.posteam==t)]; gq=g[g.gqb==qb]; ng_=gq.game_id.nunique()
    o=off[(off.posteam==t)&(off.gqb==qb)]; f=fg[(fg.posteam==t)&(fg.gqb==qb)]
    print(f'\n### {t} with {qb}: games {ng_}, offTD {len(o)} ({len(o)/ng_:.2f}/g), FG {len(f)} ({len(f)/ng_:.2f}/g)')
    da=off[off.defteam==t]; fa=fg[fg.defteam==t]; print(f'{t} D allowed offTD {len(da)/7:.2f}/g FG {len(fa)/7:.2f}/g')
    s=gq[(gq.rush==1)|(gq.pass_attempt==1)].copy()
    s['who']=s.rusher_player_name.where(s.rush==1,s.receiver_player_name)
    s['rz']=s.yardline_100<=20; s['i10']=s.yardline_100<=10; s['i5']=s.yardline_100<=5
    s['tdp']=((s.touchdown==1)&(s.td_team==t))
    s['kind']=s.rush.map({1:'car',0:'tgt'})
    a=s.groupby('who').agg(car=('rush','sum'),tgt=('pass_attempt','sum'),rz_car=('rz',lambda x:(x&(s.loc[x.index,'rush']==1)).sum()),rz_tgt=('rz',lambda x:(x&(s.loc[x.index,'pass_attempt']==1)).sum()),
        i10_car=('i10',lambda x:(x&(s.loc[x.index,'rush']==1)).sum()),i10_tgt=('i10',lambda x:(x&(s.loc[x.index,'pass_attempt']==1)).sum()),td=('tdp','sum'))
    # QB passing plays shouldn't credit QB: 'who' is receiver for passes, rusher for rushes (QB scrambles count as QB rush)
    a['rz_opp']=a.rz_car+a.rz_tgt; a['i10_opp']=a.i10_car+a.i10_tgt
    a['rz_sh']=a.rz_opp/a.rz_opp.sum(); a['i10_sh']=a.i10_opp/a.i10_opp.sum(); a['td_sh']=a.td/a.td.sum()
    a=a[a.rz_opp>=2].sort_values('rz_opp',ascending=False); print(a.round(3).to_markdown())
    # last-3 with QB
    wk=sorted(gq.week.unique())[-3:]; s3=s[s.week.isin(wk)]
    b=s3[s3.rz].groupby('who').size(); print('last3 RZ opp share', (b/b.sum()).round(3).sort_values(ascending=False).head(8).to_dict(), 'weeks',wk)
