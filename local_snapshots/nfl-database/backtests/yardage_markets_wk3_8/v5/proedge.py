"""PRO_EDGE offline reimplementation of /workspace/pro-edge/edge_scan.py logic (that script is live-API only; never called).
Saved pregame quotes only. Anchor no-vig: pinnacle>circa>betonlineag>consensus (multiplicative devig on same book/line).
Checks per leg: (1) script: implied team total ((T+-S)/2) direction supports side; (2) best price: best saved book price on the side beats anchor fair;
(3) lag: spread/total moved >=1 pt across saved snapshots while this prop line did not move, and move direction supports side; (4) sleepers: no structured injury/out data in packs -> NOT AVAILABLE."""
import pandas as pd,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PK=ROOT.parent/'v4'/'packs'
def imp(a):return 100/(a+100) if a>0 else -a/(-a+100)
def run(picks):
    rows=[]
    for w,P in picks.groupby('week'):
        pr=pd.read_csv(PK/f'w{w}/props_main.csv');gl=pd.read_csv(PK/f'w{w}/game_lines.csv')
        for r in P.itertuples():
            g=gl[gl.game==r.game];away,home=r.game.split('@');note=[];script=lag=None
            sp=g[(g.market=='spreads')&(g.name==home)].sort_values('timestamp');to=g[g.market=='totals'].sort_values('timestamp')
            if len(sp) and len(to):
                S=sp.groupby('timestamp').point.median();T=to.groupby('timestamp').point.median();s,t=S.iloc[-1],T.iloc[-1]
                tt=(t-s)/2 if r.team==home else (t+s)/2
                script=int((tt>=23.5)==(r.side=='over'));note.append(f'implied TT {tt:.1f}')
                if len(S)>1:
                    ds=S.iloc[-1]-S.iloc[0];dt=T.iloc[-1]-T.iloc[0]
                    q=pr[(pr.player==r.player)&(pr.market==r.market)]
                    moved=q.line.nunique()>1
                    if (abs(ds)>=1 or abs(dt)>=1) and not moved:
                        tdelta=(-ds if r.team==home else ds)/2+dt/2
                        lag=int((tdelta>0)==(r.side=='over'));note.append(f'lag: game moved {ds:+g}/{dt:+g}, prop static')
            q=pr[(pr.player==r.player)&(pr.market==r.market)&(pr.line==r.line)]
            fair=None
            for b in ['pinnacle','circa','betonlineag','consensus']:
                qb=q[q.book==b].sort_values('snap')
                o=qb[qb.side=='over'];u=qb[qb.side=='under']
                if len(o) and len(u):
                    po,pu=imp(o.price.iloc[-1]),imp(u.price.iloc[-1]);fair=(po if r.side=='over' else pu)/(po+pu);anchor=b;break
            best=q[q.side==r.side].price.max() if len(q[q.side==r.side]) else np.nan
            bp=int(fair is not None and np.isfinite(best) and imp(best)<fair)
            if fair is not None:note.append(f'anchor {anchor} fair {fair:.3f}, best {best:+g}')
            passed=int(bool(bp) or script==1 or lag==1)
            rows.append(dict(pe_script=script,pe_bestprice=bp,pe_lag=lag,pe_sleeper='NA',pe_fair=fair,pe_pass=passed,pe_note='; '.join(note)))
    return pd.DataFrame(rows,index=picks.sort_values('week').index)
