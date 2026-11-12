"""Shared walk-forward universe for the Rico 2026-11-01 backtests (analysis only, nothing live).
Universe: tools/sim_v6_backtest.csv = leak-free sim_v6 RAW medians (Engine cutoff before week W, calib not applied), Wk4-7.
Lines: stand-in floor(prior median)+0.5 (harness.proxy_line, >=2 prior games). p_over = mean over mc/bias/gr of Normal(median, SD),
SD = per-market residual SD of (actual - stand-in line) from weeks < W only. Bet = over when p > .5238 (-110 break-even)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0,'/workspace/nfl-database/backtests/wk8_proposals'); sys.path.insert(0,'/workspace/nfl-database/tools')
from harness import load, proxy_line, prior_vals, wilson, roi
from scipy.stats import norm, binomtest
COL={'rushyds':'ryds','rec':'rec','recyds':'recyds'}
def universe():
    d,g,pg=load(); s=pd.read_csv('/workspace/nfl-database/tools/sim_v6_backtest.csv'); rows=[]
    pgi=pg.set_index(['pid','week'])
    for _,r in s[s.market.isin(COL)].iterrows():
        line=proxy_line(prior_vals(pg,r.gsis,r.week,COL[r.market]))
        if line is None or (r.gsis,r.week) not in pgi.index: continue
        x=pgi.loc[(r.gsis,r.week)]; x=x.iloc[0] if isinstance(x,pd.DataFrame) else x
        rows.append(dict(week=int(r.week),pid=r.gsis,market=r.market,pos=x.pos,team=x.team,opp=x.opp,game_id=x.game_id,dog=bool(x.dog),
            tsp=float(x.team_spread),wx=bool(x.wx),line=line,actual=float(r.actual),hit=int(r.actual>line),meds=[r.pred_mc,r.pred_bias,r.pred_gr]))
    u=pd.DataFrame(rows); u['p']=np.nan
    for mk in COL:
        for W in sorted(u.week.unique()):
            pr=pg[(pg.week<W)]; c=COL[mk]
            # SD: dispersion of player-game actuals around their own prior median (weeks < W only)
            res=[]; 
            for pid,gp in pr.groupby('pid'):
                v=gp.sort_values('week')[c].tolist()
                if len(v)>=3 and gp[c].sum()>0: res+= [v[-1]-np.median(v[:-1])]
            sd=float(np.std(res)) if len(res)>30 else None
            i=(u.market==mk)&(u.week==W)
            u.loc[i,'p']=[float(np.mean([1-norm.cdf((l-m)/sd) for m in ms])) for ms,l in zip(u[i].meds,u[i].line)]
    u['bet']=u.p>0.5238
    return d,g,pg,u
def stats(h, be=0.5238, odds=-110):
    h=list(map(int,h)); n=len(h); k=sum(h)
    if n==0: return dict(n=0,k=0,hit=float('nan'),roi=float('nan'),lo=float('nan'),hi=float('nan'),p_be=float('nan'))
    lo,hi=wilson(k,n); return dict(n=n,k=k,hit=k/n,roi=roi(k/n,odds),lo=lo,hi=hi,p_be=binomtest(k,n,be).pvalue)
def fmt(name,s): return f"| {name} | {s['n']} | {s['k']}/{s['n']} | {s['hit']:.1%} | {s['lo']:.0%}-{s['hi']:.0%} | {s['roi']:+.1%} | {s['p_be']:.2f} |"
HDR="| Bucket | n | W/L | Hit | 90% CI | ROI −110 | p vs BE |\n|---|---|---|---|---|---|---|"
def diff_p(a,b):
    """two-proportion z-test p-value (hit rate of a vs b)"""
    import math; a=list(a);b=list(b)
    if not a or not b: return float('nan')
    p1,p2=sum(a)/len(a),sum(b)/len(b); p=(sum(a)+sum(b))/(len(a)+len(b)); se=math.sqrt(p*(1-p)*(1/len(a)+1/len(b))) or 1e-9
    return float(2*(1-norm.cdf(abs(p1-p2)/se)))
def passyds_rows(d,pg):
    s=pd.read_csv('/workspace/nfl-database/tools/sim_v6_backtest.csv'); s=s[s.market=='passyds']
    pp=d[(d.pass_attempt==1)&d.passer_player_id.notna()].groupby(['game_id','week','posteam','defteam','passer_player_id']).passing_yards.sum().reset_index()
    rows=[]
    for _,r in s.iterrows():
        pr=pp[(pp.passer_player_id==r.gsis)&(pp.week<r.week)].sort_values('week').passing_yards.tolist(); line=proxy_line(pr)
        cur=pp[(pp.passer_player_id==r.gsis)&(pp.week==r.week)]
        if line is None or cur.empty: continue
        c=cur.iloc[0]; rows.append(dict(week=int(r.week),pid=r.gsis,market='passyds',pos='QB',team=c.posteam,opp=c.defteam,game_id=c.game_id,line=line,actual=float(r.actual),hit=int(r.actual>line),meds=[r.pred_mc,r.pred_bias,r.pred_gr]))
    u=pd.DataFrame(rows)
    for W in sorted(u.week.unique()):
        pr=pp[pp.week<W]; res=[]
        for pid,gp in pr.groupby('passer_player_id'):
            v=gp.sort_values('week').passing_yards.tolist()
            if len(v)>=3: res.append(v[-1]-np.median(v[:-1]))
        sd=float(np.std(res)); i=u.week==W
        u.loc[i,'p']=[float(np.mean([1-norm.cdf((l-m)/sd) for m in ms])) for ms,l in zip(u[i].meds,u[i].line)]
    u['bet']=u.p>0.5238; return u
