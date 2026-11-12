import pandas as pd, numpy as np, math
from scipy import stats
d=pd.read_csv('ol_dl_gap_legs.csv'); O=[]
def roi(h,o): return h*100/abs(o)-(1-h)
def wil(k,n,z=1.645):
    if n==0: return (np.nan,np.nan)
    p=k/n;dd=1+z*z/n;c=p+z*z/(2*n);r=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n));return (c-r)/dd,(c+r)/dd
def tbl(groups,title):
    O.append(f"\n### {title}\n| Bucket | n | Over W | Over hit | 90% CI | ROI −110 | −130 | −160 | Under hit | U ROI −110 | −130 | −160 |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for lab,x in groups:
        x=x[x.push==0]; n=len(x); k=int(x.over_hit.sum()); h=k/n if n else np.nan; u=1-h; lo,hi=wil(k,n)
        O.append(f"| {lab} | {n} | {k} | {h:.1%} | {lo:.0%}-{hi:.0%} | {roi(h,-110):+.1%} | {roi(h,-130):+.1%} | {roi(h,-160):+.1%} | {u:.1%} | {roi(u,-110):+.1%} | {roi(u,-130):+.1%} | {roi(u,-160):+.1%} |")
d['ter']=pd.qcut(d.gap.rank(method='first'),3,labels=['T1 (OL worst vs DL)','T2','T3 (OL best vs DL)'])
d['quin']=pd.qcut(d.gap.rank(method='first'),5,labels=['Q1','Q2','Q3','Q4','Q5'])
tbl([('ALL',d)],'All lead-RB legs')
tbl([(str(k),x) for k,x in d.groupby('ter',observed=True)],'Gap terciles')
tbl([(str(k),x) for k,x in d.groupby('quin',observed=True)],'Gap quintiles')
O.append("\nQuintile gap ranges: "+", ".join(f"{k} [{x.gap.min():.0f},{x.gap.max():.0f}]" for k,x in d.groupby('quin',observed=True)))
d['pb']=pd.cut(d.p_over,[0,.45,.55,1.01],right=False,labels=['p<.45','p .45-.55','p>=.55'])
g=[]
for pb,x in d.groupby('pb',observed=True):
    for t,y in x.groupby(x.gap>0): g.append((f"{pb} & gap {'>0' if t else '<=0'}",y))
tbl(g,'Within sim_v6 p buckets, gap split at 0')
tbl([('real lines',d[d.line_src=='real']),('stand-ins',d[d.line_src=='standin'])],'By line source')
O.append("\n### n per week × tercile\n"+pd.crosstab(d.week,d.ter,margins=True).to_markdown())
# correlations
rs=lambda a,b: stats.spearmanr(a,b)
O.append("\n### What the gap predicts (Spearman, all legs)")
d['ypc_resid']=d.ypc-d.prior_ypc; d['car_resid']=d.carries-d.prior_car; d['yds_resid']=d.actual-d.line
for c in ['actual','yds_resid','ypc','ypc_resid','carries','car_resid','over_hit']:
    r=rs(d.gap,d[c]); O.append(f"- gap vs {c}: rho {r.statistic:+.3f} (p={r.pvalue:.3f})")
r=rs(d.p_over,d.over_hit); O.append(f"- (reference) sim p vs over_hit: rho {r.statistic:+.3f} (p={r.pvalue:.3f})")
r=rs(d.gap,d.p_over); O.append(f"- gap vs sim p (overlap): rho {r.statistic:+.3f}")
# walk-forward logistic
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, brier_score_loss
x=d[d.push==0].copy(); x['lp']=np.log(x.p_over.clip(.01,.99)/(1-x.p_over.clip(.01,.99))); x['gz']=x.gap/50
P1=[];P2=[];Y=[];RAW=[];CO=[]
for W in range(4,9):
    tr=x[x.week<W]; te=x[x.week==W]
    m1=LogisticRegression(C=1.0).fit(tr[['lp']],tr.over_hit); m2=LogisticRegression(C=1.0).fit(tr[['lp','gz']],tr.over_hit)
    P1+=list(m1.predict_proba(te[['lp']])[:,1]); P2+=list(m2.predict_proba(te[['lp','gz']])[:,1]); Y+=list(te.over_hit); RAW+=list(te.p_over); CO.append((W,len(tr),m2.coef_[0].round(3).tolist()))
O.append(f"\n### Walk-forward logistic (train weeks < W, test W=4..8; n test={len(Y)})\n| Model | log loss | Brier |\n|---|---|---|")
for lab,P in (('raw sim p',RAW),('logit(p) refit',P1),('logit(p) + gap',P2)):
    O.append(f"| {lab} | {log_loss(Y,np.clip(P,.01,.99)):.4f} | {brier_score_loss(Y,P):.4f} |")
O.append("Coefficients [logit p, gap/50] per test week: "+"; ".join(f"W{w} (train n {n}): {c}" for w,n,c in CO))
full=LogisticRegression(C=1e6).fit(x[['lp','gz']],x.over_hit); O.append(f"In-sample full fit coef [logit p, gap/50]: {full.coef_[0].round(3).tolist()}")
# wk8 examples
O.append("\n### Week 8 examples\n"+d[d.week==8][['player','team','opp','off_pct','def_pct','gap','line','line_src','p_over','carries','actual','over_hit']].round(3).to_markdown(index=False))
open('tables.md','w').write('\n'.join(O)); print('\n'.join(O))
