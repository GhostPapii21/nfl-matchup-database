"""Weeks 1-2 packs. Lines: STAND-IN (no free historical player-prop line source found; see GAPS). Game lines: nflverse nfldata games.csv (public GitHub, closing spread/total)."""
import pandas as pd,numpy as np
from common import *
g=pd.read_csv(GAMES);pl=pd.read_parquet(PLAYERS)
pos=dict(zip(pl.gsis_id,pl.position));tm26=dict(zip(pl.gsis_id,pl.latest_team));name=dict(zip(pl.gsis_id,pl.display_name))
inj=pd.read_parquet(INJ)
for w in (1,2):
    d=ROOT/f'packs/w{w}';d.mkdir(parents=True,exist_ok=True)
    gw=g[(g.season==2026)&(g.week==w)&(g.game_type=='REG')].copy();gw['away']=gw.away_team.replace('LA','LA');gw['game']=gw.away_team+'@'+gw.home_team
    gw[['game_id','game','gameday','gametime','home_team','away_team','spread_line','total_line','home_moneyline','away_moneyline','roof','temp','wind']].to_csv(d/'game_lines.csv',index=False)
    pb,lab=prior_pbp(w);L=logs(pb)
    if w==1:L['team']=L.gsis.map(tm26)
    else:L['team']=L.posteam
    rows=[]
    for gr in gw.itertuples():
        for team,opp in [(gr.away_team,gr.home_team),(gr.home_team,gr.away_team)]:
            T=L[L.team==team]
            if w==1:T=T[T.gsis.map(lambda x:tm26.get(x)==team)]
            agg=T.groupby('gsis').agg(car=('car','sum'),tgt=('tgt','sum'),n=('game_id','nunique'))
            out=set(inj[(inj.week==w)&(inj.team==team)&inj.report_status.isin(['Out','Doubtful'])].gsis_id)
            agg=agg[~agg.index.isin(out)&agg.index.map(lambda x:pos.get(x) in ('RB','WR','TE','FB'))]
            rb=agg[agg.index.map(lambda x:pos.get(x) in('RB','FB'))].sort_values('car',ascending=False).head(2).index
            rc=agg.sort_values('tgt',ascending=False).head(4).index
            for p in set(rb)|set(rc):
                mk=(['rushyds','rushrecyds'] if p in rb else [])+(['recyds'] if p in rc or pos.get(p)=='RB' else [])
                for m in mk:
                    v=T[T.gsis==p][m];med=float(np.median(v));line=np.floor(med)+0.5
                    for s in('over','under'):rows.append(dict(week=w,game_id=gr.game_id,game=gr.game,player=nm(name.get(p,p)),gsis=p,team=team,opp=opp,market=m,side=s,tier='main',line=line,price=np.nan,book='STAND-IN',
                        line_src=f'STAND-IN median of {len(v)} prior games ({lab})'))
    pd.DataFrame(rows).to_csv(d/'props_standin.csv',index=False);print(w,len(gw),len(rows))
