"""2025 packs wk2-18. Lines: nflverse games.csv spread/total; props STAND-IN = 2025 season-to-date median (weeks<w). Week 1 skipped (no 2024 pbp on box)."""
import pandas as pd,numpy as np
from common import *
g=pd.read_csv(GAMES);pl=pd.read_parquet(PLAYERS);pos=dict(zip(pl.gsis_id,pl.position));name=dict(zip(pl.gsis_id,pl.display_name))
inj=pd.read_parquet(ROOT/'packs/injuries_2025.parquet');PB=clean(pd.read_parquet(PB25))
for w in range(2,19):
    d=ROOT/f'packs25/w{w}';d.mkdir(parents=True,exist_ok=True)
    gw=g[(g.season==2025)&(g.week==w)&(g.game_type=='REG')].copy();gw['game']=gw.away_team+'@'+gw.home_team
    gw[['game_id','game','gameday','gametime','home_team','away_team','spread_line','total_line','roof']].to_csv(d/'game_lines.csv',index=False)
    pb=PB[PB.week<w];L=logs(pb);L['team']=L.posteam;rows=[]
    last=L.sort_values('week').groupby('gsis').team.last()
    for gr in gw.itertuples():
        for team,opp in [(gr.away_team,gr.home_team),(gr.home_team,gr.away_team)]:
            cur=set(last[last==team].index);T=L[L.gsis.isin(cur)]
            agg=T.groupby('gsis').agg(car=('car','sum'),tgt=('tgt','sum'))
            out=set(inj[(inj.week==w)&(inj.team==team)&inj.report_status.isin(['Out','Doubtful'])].gsis_id)
            agg=agg[~agg.index.isin(out)&agg.index.map(lambda x:pos.get(x) in('RB','WR','TE','FB'))]
            rb=agg[agg.index.map(lambda x:pos.get(x) in('RB','FB'))].sort_values('car',ascending=False).head(2).index;rc=agg.sort_values('tgt',ascending=False).head(4).index
            for p in set(rb)|set(rc):
                for m in (['rushyds','rushrecyds'] if p in rb else [])+(['recyds'] if p in rc or pos.get(p)=='RB' else []):
                    v=T[T.gsis==p][m];line=np.floor(float(np.median(v)))+0.5
                    for s in('over','under'):rows.append(dict(week=w,game_id=gr.game_id,game=gr.game,player=nm(name.get(p,p)),gsis=p,team=team,opp=opp,market=m,side=s,tier='main',line=line,price=np.nan,book='STAND-IN',line_src=f'STAND-IN 2025 season-to-date median of {len(v)} games'))
    pd.DataFrame(rows).to_csv(d/'props_standin.csv',index=False)
print('ok')
