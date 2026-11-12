import sys; sys.path.insert(0,'/workspace/nfl-database/backtests/wk8_proposals')
import numpy as np, pandas as pd
from harness import roi, wilson
from scipy.optimize import minimize
d=pd.read_csv('rb_rec_legs_raw.csv')
# triggers (pregame only). (c)/(d) thresholds: worst-8 pass D by prior EPA/dropback; QB checkdown composite top third
d['trig_a']=d.pa_hat>=40; d['trig_a35']=d.pa_hat>=35
d['trig_b']=d.team_spread>=3
d['trig_c']=(d.team_spread<0)&(d.own_passD_rank<=8)
d['trig_d']=d.qb_checkdown_pct>=2/3
d['trig_any']=d[['trig_a','trig_b','trig_c','trig_d']].any(axis=1)
d['script_uncertain']=(d.team_spread.abs()<=7)|(d.total>=47)
d.to_csv('rb_rec_legs.csv',index=False)
T=[('a: proj PA>=40','trig_a'),('a2: proj PA>=35 (looser)','trig_a35'),('b: dog >=3','trig_b'),('c: fav w/ bottom-8 own pass D','trig_c'),('d: QB checkdown top 1/3','trig_d'),('any trigger','trig_any')]
def row(lbl,x):
    n=len(x);k=int(x.hit.sum())
    if n==0: return f'| {lbl} | 0 | | | | | | | |'
    h=k/n;lo,hi=wilson(k,n); res=(x.hit-x.p).mean()
    return f'| {lbl} | {n} | {k} | {h:.1%} | {lo:.0%}-{hi:.0%} | {roi(h,-110):+.1%} | {roi(h,-130):+.1%} | {roi(h,-160):+.1%} | {x.p.mean():.2f} | {res:+.3f} |'
H='| Bucket | n | W | Hit | 90% CI | ROI −110 | ROI −130 | ROI −160 | mean sim p | hit − p |\n|---|---|---|---|---|---|---|---|---|---|'
def logit_add(x,c):
    y=x.hit.values; lp=np.log(np.clip(x.p,1e-3,1-1e-3)/(1-np.clip(x.p,1e-3,1-1e-3))).values; t=x[c].astype(float).values
    def nll(b,useT=True):
        z=b[0]+b[1]*lp+(b[2]*t if useT else 0); return np.sum(np.logaddexp(0,z)-y*z)
    r1=minimize(nll,[0,1,0]); r0=minimize(lambda b:nll(np.r_[b,0],False),[0,1])
    # SE via numerical hessian inverse
    se=np.sqrt(np.diag(r1.hess_inv))[2] if hasattr(r1,'hess_inv') else np.nan
    return r1.x[2],se,2*(r0.fun-r1.fun)
out=['# RB receiving game-script backtest (2026 Wk3–8). Analysis only, no rules changed','',open('notes.md').read() if False else '']
for m,lab in (('rec','Receptions'),('recyds','Receiving yards'),('rushrec','Rush+Rec yards')):
    x=d[d.market==m]; out+=[f'## {lab} OVER (lead RB)','',H,row('ALL lead RBs',x)]
    for l,c in T: out+=[row(l,x[x[c]]),row(f'  not {c[5:]}',x[~x[c]])]
    out+=[row('real lines only',x[x.line_src=="real"]),row('stand-ins only',x[x.line_src=="standin"]),'']
    out+=['Signal on top of sim_v6 p (logistic hit ~ logit(p) + trigger; LR χ² 1df, ≥2.71 ≈ p<.10, ≥3.84 ≈ p<.05):','','| Trigger | coef | SE | LR χ² |','|---|---|---|---|']
    for l,c in T:
        if x[c].sum()<3: out.append(f'| {l} | n<3 | | |'); continue
        b,se,lr=logit_add(x,c); out.append(f'| {l} | {b:+.2f} | {se:.2f} | {lr:.2f} |')
    out+=['','n per week (trigger legs / all):','','| week | '+' | '.join(c for _,c in T)+' | all |','|'+'---|'*(len(T)+2)]
    for w,g in x.groupby('week'): out.append(f'| {w} | '+' | '.join(f'{int(g[c].sum())} ({int(g[g[c]].hit.sum())}W)' for _,c in T)+f' | {len(g)} ({int(g.hit.sum())}W) |')
    out.append('')
# rush+rec vs rush-only
out+=['## Claim: rush+rec beats rush-only for lead backs when script is uncertain','',
 'Same player-games, both markets present. "Uncertain" = |spread| ≤ 7 or total ≥ 47. Compared (1) blind over hit rate, (2) over hit rate when sim p ≥ .55, (3) how often the over lands on one market but not the other.','']
pv=d[d.market.isin(['rushyds','rushrec'])].pivot_table(index=['week','gsis','team'],columns='market',values=['hit','p','script_uncertain','line_src'],aggfunc='first').dropna()
pv.columns=[f'{a}_{b}' for a,b in pv.columns]
out+=['| Group | n games | rush-only over hit | rush+rec over hit | rush hit when p≥.55 (n) | rush+rec hit when p≥.55 (n) | rush+rec hit when rush missed |','|---|---|---|---|---|---|---|']
for lbl,mask in (('script uncertain',pv.script_uncertain_rushrec.astype(bool)),('script clear',~pv.script_uncertain_rushrec.astype(bool)),('all',pv.index==pv.index)):
    g=pv[mask]; ra=g.hit_rushyds.astype(float); rr=g.hit_rushrec.astype(float)
    s1=g[g.p_rushyds.astype(float)>=.55]; s2=g[g.p_rushrec.astype(float)>=.55]; miss=g[ra==0]
    out.append(f'| {lbl} | {len(g)} | {ra.mean():.1%} | {rr.mean():.1%} | {s1.hit_rushyds.astype(float).mean():.1%} ({len(s1)}) | {s2.hit_rushrec.astype(float).mean():.1%} ({len(s2)}) | {miss.hit_rushrec.astype(float).mean():.1%} ({len(miss)}) |')
out.append('')
open('tables.md','w').write('\n'.join(out)); print('\n'.join(out))
print(d.groupby(['market','line_src']).size())
