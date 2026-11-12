import pandas as pd, numpy as np, json
p=pd.read_parquet('tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet'); p=p[p.season_type=='REG']
G=p.groupby('game_id').agg(week=('week','first'),home=('home_team','first'),away=('away_team','first'),hs=('home_score','first'),as_=('away_score','first'),tl=('total_line','first'),sl=('spread_line','first')).reset_index()
rows=[]
for _,g in G.iterrows():
    for t,o,pf,pa in ((g.home,g.away,g.hs,g.as_),(g.away,g.home,g.as_,g.hs)):
        q=p[(p.game_id==g.game_id)&(p.posteam==t)]; d=p[(p.game_id==g.game_id)&(p.posteam==o)]
        qb=q[q.pass_attempt==1].passer_player_name.mode(); qb=qb.iat[0] if len(qb) else None
        sc=q[(q.rush==1)|(q.pass_attempt==1)]
        dr=q.groupby('drive').agg(rz=('yardline_100',lambda y:(y<=20).any()),td=('touchdown',lambda x:((x==1)&(q.loc[x.index,'td_team']==t)).any()))
        drd=d.groupby('drive').agg(rz=('yardline_100',lambda y:(y<=20).any()),td=('touchdown',lambda x:((x==1)&(d.loc[x.index,'td_team']==o)).any()))
        rows.append(dict(week=g.week,team=t,opp=o,qb=qb,pf=pf,pa=pa,tot=pf+pa,close_total=g.tl,plays=len(sc),
            rz_trips=int(dr.rz.sum()),rz_td=int((dr.rz&dr.td).sum()),rz_trips_a=int(drd.rz.sum()),rz_td_a=int((drd.rz&drd.td).sum()),
            expl=int(((sc.rush==1)&(sc.yards_gained>=15)).sum()+((sc.pass_attempt==1)&(sc.yards_gained>=20)).sum()),
            expl_a=int(((d.rush==1)&(d.yards_gained>=15)).sum()+((d.pass_attempt==1)&(d.yards_gained>=20)).sum()),
            to=int(q.interception.sum()+q.fumble_lost.sum()),to_a=int(d.interception.sum()+d.fumble_lost.sum()),
            epa_pl=sc.epa.mean()))
T=pd.DataFrame(rows); T['ou']=np.where(T.tot>T.close_total,'O',np.where(T.tot<T.close_total,'U','P'))
T.to_csv('runs/2026-11-02_CHI@SEA_r2/total/team_games.csv',index=False)
for t in ('CHI','SEA'):
    x=T[T.team==t].sort_values('week'); print(f'\n## {t}\n'+x.drop(columns=['team']).round(3).to_markdown(index=False))
    for lab,y in (('all',x),('curQB',x[x.qb==('C.Williams' if t=='CHI' else 'S.Darnold')])):
        print(t,lab,'n',len(y),y[['pf','pa','tot','plays','rz_trips','rz_trips_a','expl','expl_a','to','to_a']].mean().round(2).to_dict(),'RZTD%',round(y.rz_td.sum()/max(y.rz_trips.sum(),1),3),'RZTD%allowed',round(y.rz_td_a.sum()/max(y.rz_trips_a.sum(),1),3),'O/U',y.ou.value_counts().to_dict())
print('LEAGUE ppg',T.pf.mean().round(2),'plays',T.plays.mean().round(1),'tot',T.drop_duplicates(['week','tot']).tot.mean())
