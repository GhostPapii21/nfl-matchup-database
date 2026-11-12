"""OL-vs-DL run-matchup gap backtest (analysis only). Own pbp + ESPN box only; no PFF.
Factor (walk-forward, plays before week W): per team on RB carries (no kneels): success rate (nflverse 'success'), stuff rate (<=0 yds), YPC.
One-step opponent adjustment: off_adj = off_raw - (opp_def_allowed_avg - league) over games played; mirror for defense.
Composite = mean z(success_adj), -z(stuff_adj), z(ypc_adj). Off pct: high = good blocking; Def pct: high = good run D. gap = off_pct - def_pct.
Legs: lead RB per team (most RB carries in prior weeks, >=2 games, avg>=8 car) active in week W, rush-yds over AND under at the same line.
Line: real (Wk8 run manifests) else stand-in floor(prior median)+0.5. p = raw sim_v6 (calib=None) mean of mc/bias/gr P(X>=line), 100k each, game spread used."""
import sys, json, glob
import numpy as np, pandas as pd
sys.path.insert(0,'/workspace/nfl-database/tools'); sys.path.insert(0,'/workspace/nfl-database/backtests/wk8_proposals'); sys.path.insert(0,'/workspace/nfl-database/backtests/p6_rush_exception')
import sim_v6 as S
from harness import load, proxy_line
from bt_p6 import real_lines
d,g,pg=load(); RL=real_lines(); NAME=S._PL.set_index('gsis_id').display_name.to_dict()
POS=S._PL.set_index('gsis_id').position_group.to_dict()
R=d[(d.rush_attempt==1)&(d.qb_kneel!=1)&d.rusher_player_id.notna()].copy(); R=R[R.rusher_player_id.map(POS)=='RB']
R['stuff']=(R.rushing_yards.fillna(0)<=0).astype(float); R['ry']=R.rushing_yards.fillna(0)
def factor(W):
    r=R[R.week<W]; gm=r.groupby(['game_id','posteam','defteam']).agg(succ=('success','mean'),stuff=('stuff','mean'),ypc=('ry','mean'),n=('ry','size')).reset_index()
    out={}
    for side,me,them in (('off','posteam','defteam'),('def','defteam','posteam')):
        raw=gm.groupby(me)[['succ','stuff','ypc']].mean(); out[side]=raw
    lg=gm[['succ','stuff','ypc']].mean()
    adj={}
    for side,me,them,other in (('off','posteam','defteam','def'),('def','defteam','posteam','off')):
        x=gm.copy(); oth=out[other].reindex(x[them]).values
        x[['succ','stuff','ypc']]=x[['succ','stuff','ypc']].values-(oth-lg.values)
        a=x.groupby(me)[['succ','stuff','ypc']].mean(); z=(a-a.mean())/a.std()
        comp=(z.succ-z.stuff+z.ypc)/3
        adj[side]=(comp if side=='off' else -comp).rank(pct=True)*100   # def: high = strong run D
    return adj
GS=pd.read_csv('/workspace/nfl-database/playlogs/game_scripts_2026.csv'); GS=GS[GS.week==8]
box={}
for f in glob.glob('/workspace/nfl-database/playlogs/2026_wk8/*_box.json'):
    b=json.load(open(f))
    for t,v in b['teams'].items(): box[t]={x['player']:(float(x['YDS']),int(x['CAR'])) for x in v.get('rushing',[])}
rows=[]
for W in range(3,9):
    F=factor(W); cut=d[d.week==W].game_date.min() if W<8 else '2026-11-01'
    E=S.Engine(cutoff=cut,calib=None)
    games=[]  # (team,opp,spread,src)
    for _,r in pg[pg.week==W][['team','opp','team_spread']].drop_duplicates('team').iterrows(): games.append((r.team,r.opp,float(r.team_spread),'pbp'))
    if W==8:
        for _,r in GS.iterrows():
            if r.team in box: games.append((r.team,r.opp,float(r.spread),'box'))
    for team,opp,sp,src in games:
        pr=pg[(pg.team==team)&(pg.week<W)&(pg.pos=='RB')&(pg.car>0)]
        if pr.empty: continue
        s=pr.groupby('pid').agg(c=('car','sum'),n=('car','size'),m=('car','mean')).sort_values('c',ascending=False)
        pid=s.index[0]
        if s.n.iloc[0]<2 or s.m.iloc[0]<8: continue
        name=NAME.get(pid,pid)
        if src=='pbp':
            cur=pg[(pg.week==W)&(pg.pid==pid)&(pg.car>0)]
            if cur.empty: continue
            act,car=float(cur.ryds.iloc[0]),int(cur.car.iloc[0])
        else:
            if name not in box[team]: continue
            act,car=box[team][name]
        line=proxy_line(pr[pr.pid==pid].sort_values('week').ryds.tolist()); ls='standin'
        if W==8 and RL.get(name) is not None: line,ls=float(RL[name]),'real'
        try: o,info=E.sim(dict(player=name,gsis=pid,team=team,opp=opp,market='rushyds',spread=sp,rungs=[line]),raw=True)
        except Exception as e: print('skip',name,e); continue
        p=np.mean([o[m]['rungs'][str(line)] for m in S.MODES])
        op=float(F['off'].get(S.NV.get(team,team),np.nan)); dp=float(F['def'].get(S.NV.get(opp,opp),np.nan))
        prior=pr[pr.pid==pid]; pc=prior.car.mean(); py=prior.ryds.sum()/max(prior.car.sum(),1)
        rows.append(dict(week=W,player=name,team=team,opp=opp,team_spread=sp,line=line,line_src=ls,p_over=p,off_pct=op,def_pct=dp,gap=op-dp,
            actual=act,carries=car,ypc=act/car if car else np.nan,prior_car=pc,prior_ypc=py,over_hit=int(act>line),under_hit=int(act<line),push=int(act==line),grade_src=src))
    print(W,len(rows),flush=True)
pd.DataFrame(rows).to_csv('ol_dl_gap_legs.csv',index=False)
