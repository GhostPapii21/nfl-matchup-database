import os, json, numpy as np, pandas as pd, common as C, features as Fx
d,g,pg,u=C.universe(); pu=C.passyds_rows(d,pg)
FE={W:Fx.week_feats(d,W) for W in range(4,8)}
B='/workspace/nfl-database/backtests/'
def tab(rows): return C.HDR+"\n"+"\n".join(C.fmt(n,C.stats(h)) for n,h in rows)
def write(name,title,body):
    os.makedirs(B+name,exist_ok=True); open(B+name+'/RESULTS.md','w').write(f"# {title}\nGenerated 2026-11-01 (ET), analysis only, nothing live. Scripts: `backtests/rico_common/` (`common.py`, `features.py`, `run_b1_b4.py`).\n\n**Method (shared):** this uses the leak-free sim_v6 RAW medians in `tools/sim_v6_backtest.csv`, Wk4–7. Each week's Engine cutoff falls before that week and no calibration is applied. Lines are **stand-ins**, floor(prior median)+0.5. p = mean over mc/bias/gr of a Normal(median, walk-forward SD). A bet is an over with p > .5238, the −110 break-even. Every feature uses only weeks < W. Wk3 is out because there are under 2 prior games, and Wk8 Sunday is out because no RAW medians exist for it. The p-values are two-sided binomials vs the 52.4% break-even. Small samples and stand-in lines both apply, so treat every result as directional.\n\n"+body+"\n")
    return name
out={}
# ---------- B1 RB YPC floor ----------
r=u[(u.market=='rushyds')&(u.pos=='RB')&u.bet].copy()
r['sim_ypc']=[np.mean([0])+0 for _ in range(len(r))]
sy=[];da=[]
for _,x in r.iterrows():
    F=FE[x.week]; cpg=F['car_pg'].get(x.pid,np.nan); med=np.mean(C.universe.__defaults__ or [0]) if False else None
    sy.append(np.nan); da.append(F['def_adj_ypc'].get(x.opp,np.nan))
s=pd.read_csv('/workspace/nfl-database/tools/sim_v6_backtest.csv').set_index(['gsis','week','market'])
r['sim_med']=[float(np.mean(s.loc[(p,w,'rushyds')][['pred_mc','pred_bias','pred_gr']].values)) for p,w in zip(r.pid,r.week)]
r['cpg']=[FE[w]['car_pg'].get(p,np.nan) for p,w in zip(r.pid,r.week)]
r['sim_ypc']=r.sim_med/r.cpg; r['def_ypc']=da
r['floor_ok']=r.sim_ypc<=r.def_ypc; r['floor_ok_tol']=r.sim_ypc<=r.def_ypc+0.3
k=r.dropna(subset=['sim_ypc','def_ypc'])
b1=tab([('All RB rush-yds overs the model would bet',k.hit),('Pass floor (sim YPC ≤ def adj YPC allowed)',k[k.floor_ok].hit),('FAIL floor → would be cut',k[~k.floor_ok].hit),('Variant: tolerance +0.3',k[k.floor_ok_tol].hit),('Variant tol fails',k[~k.floor_ok_tol].hit)])
pd1=C.diff_p(k[k.floor_ok].hit,k[~k.floor_ok].hit)
k.drop(columns=[]).to_csv(B+'rico_common/b1_legs.csv',index=False)
out['B1']=dict(all=C.stats(k.hit),ok=C.stats(k[k.floor_ok].hit),fail=C.stats(k[~k.floor_ok].hit),p_diff=pd1)
# ---------- B2 QB return ----------
w=u[u.pos.isin(['WR','TE'])&u.bet].copy(); fl=[];why=[]
for _,x in w.iterrows():
    st=Fx.starter(d,x.team,x.week); F=FE[x.week]['starters']; tp=F[F.posteam==x.team].sort_values('week')
    missed=int((tp.passer_player_id!=st).sum()); last=tp.passer_player_id.iloc[-1] if len(tp) else None
    ret = missed>=2 and len(tp) and (tp.passer_player_id.iloc[-2:]!=st).any()
    backup = last is not None and last!=st
    fl.append(bool(ret or backup)); why.append('return' if ret else ('built-on-backup' if backup else ''))
w['flag']=fl; w['why']=why
# one-rung drop: recyds line -10 / rec line -1 at an assumed −150 rung price (BE .600)
w['drop_line']=np.where(w.market=='recyds',w.line-10,w.line-1); w['drop_hit']=(w.actual>w.drop_line).astype(int)
f=w[w.flag]; nf=w[~w.flag]
sd=C.stats(f.drop_hit,be=0.6,odds=-150)
b2=tab([('All WR/TE overs bet',w.hit),('No QB-change flag',nf.hit),('Flagged (QB return or model built on backup)',f.hit),('  flagged: return',f[f.why=='return'].hit),('  flagged: built-on-backup',f[f.why=='built-on-backup'].hit)])
b2+=f"\n\nOne-rung drop on the flagged legs (line −10 yds / −1 rec, priced −150, BE 60.0%): {sd['k']}/{sd['n']} = {sd['hit']:.1%}, ROI {sd['roi']:+.1%}, p vs BE {sd['p_be']:.2f}."
w.to_csv(B+'rico_common/b2_legs.csv',index=False)
out['B2']=dict(flag=C.stats(f.hit),noflag=C.stats(nf.hit),drop=sd,p_diff=C.diff_p(f.hit,nf.hit))
# ---------- B3 QB under pressure / weather ----------
def qbfe(x):
    F=FE[x.week]; st=x.pid if x.pos=='QB' else Fx.starter(d,x.team,x.week)
    q=F['qbp']; comp=q.comp.get(st,np.nan); dp=F['def_press'].get(x.opp,np.nan)
    hi=dp>=F['def_press'].quantile(2/3); wx=F['qb_wx_epa']
    return comp,hi
rows=pd.concat([pu[pu.bet],w.drop(columns=['flag','why','drop_line','drop_hit'])],ignore_index=True)
cc=[qbfe(x) for _,x in rows.iterrows()]; rows['qb_comp']=[c[0] for c in cc]; rows['hi_press']=[bool(c[1]) for c in cc]
rows=rows.dropna(subset=['qb_comp']); weak=rows.qb_comp<rows.qb_comp.median()
rows['risk']=rows.hi_press&weak
qb=rows[rows.pos=='QB']; rc=rows[rows.pos!='QB']
b3=tab([('QB pass-yds overs, all',qb.hit),('QB: high-pressure D & weak-under-pressure QB',qb[qb.risk].hit),('QB: other',qb[~qb.risk].hit),
        ('WR/TE overs, all',rc.hit),('WR/TE: high-pressure D & weak-under-pressure QB',rc[rc.risk].hit),('WR/TE: other',rc[~rc.risk].hit),
        ('WR/TE: high-pressure D & STRONG-under-pressure QB',rc[rc.hi_press&~weak.loc[rc.index]].hit)])
wxr=rows[rows.game_id.isin(g[g.wx].index)]
b3+=f"\n\nWeather slice: {len(wxr)} bet legs in rain or wind ≥15 games, hit {wxr.hit.mean() if len(wxr) else float('nan'):.1%}. That n is too small to test, and the Phase 11 and forecast gates already cut these."
rows.to_csv(B+'rico_common/b3_legs.csv',index=False)
out['B3']=dict(qb_risk=C.stats(qb[qb.risk].hit),qb_other=C.stats(qb[~qb.risk].hit),rc_risk=C.stats(rc[rc.risk].hit),rc_other=C.stats(rc[~rc.risk].hit),p_rc=C.diff_p(rc[rc.risk].hit,rc[~rc.risk].hit),p_qb=C.diff_p(qb[qb.risk].hit,qb[~qb.risk].hit),wx_n=len(wxr))
# ---------- B4 OL pass-block vs DL pass-rush ----------
z=rows.copy(); z['gap']=[FE[x.week]['def_press'].get(x.opp,np.nan)+FE[x.week]['off_press'].get(x.team,np.nan)-2*FE[x.week]['lg_press'] for _,x in z.iterrows()]
z=z.dropna(subset=['gap']); t=z.gap.quantile(2/3); bad=z.gap>=t
qq=z[z.pos=='QB']; rr=z[z.pos!='QB']
b4=tab([('QB pass-yds overs: OL-DL mismatch (top third: leaky OL + strong rush)',qq[bad.loc[qq.index]].hit),('QB: rest',qq[~bad.loc[qq.index]].hit),
        ('WR/TE overs: mismatch top third',rr[bad.loc[rr.index]].hit),('WR/TE: rest',rr[~bad.loc[rr.index]].hit)])
b4+=f"\n\nGap = (opp D pressure rate − lg) + (team OL pressure allowed − lg), using sack-or-hit per dropback from our pbp, weeks < W. Top-third cut = {t:+.3f}. ESPN PBWR/PRWR is published only as season-to-date with no weekly snapshots on hand, so it can't be used walk-forward for Wk4–7 without leaking. It's left out of the test, and an ESPN-only slice would be look-ahead."
z.to_csv(B+'rico_common/b4_legs.csv',index=False)
out['B4']=dict(qq_bad=C.stats(qq[bad.loc[qq.index]].hit),qq_rest=C.stats(qq[~bad.loc[qq.index]].hit),rr_bad=C.stats(rr[bad.loc[rr.index]].hit),rr_rest=C.stats(rr[~bad.loc[rr.index]].hit),p_rr=C.diff_p(rr[bad.loc[rr.index]].hit,rr[~bad.loc[rr.index]].hit),p_qq=C.diff_p(qq[bad.loc[qq.index]].hit,qq[~bad.loc[qq.index]].hit))
json.dump(out,open(B+'rico_common/b1_b4_summary.json','w'),indent=1,default=float)
open('/tmp/tabs.md','w').write("\n\n".join(["## B1\n"+b1+f"\n\nfloor ok vs fail p={pd1:.2f}","## B2\n"+b2,"## B3\n"+b3,"## B4\n"+b4]))
print(open('/tmp/tabs.md').read())
