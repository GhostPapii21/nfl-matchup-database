import pandas as pd
T=pd.read_csv('scores.csv'); R=pd.read_csv('plus3_roi.csv'); L=pd.read_csv('legs.csv')
t="| sim | version | N legs | Brier | log loss | market Brier | market log loss | Δ Brier vs mkt (95% CI, game-clustered) |\n|---|---|---|---|---|---|---|---|\n"
for _,r in T.iterrows(): t+=f"| {r.sim} | {r.version} | {r.N} | {r.brier:.4f} | {r.logloss:.4f} | {r.mkt_brier:.4f} | {r.mkt_logloss:.4f} | +{r.d_brier:.4f} ({r.ci_lo:+.4f} to {r.ci_hi:+.4f}) |\n"
r3="| sim | version | bets | W–L | hit | P/L ($10 flat) | ROI | mean model p (bet side) |\n|---|---|---|---|---|---|---|---|\n"
for _,r in R.iterrows(): r3+=f"| {r.sim} | {r.version} | {r.bets} | {r.W}–{r.L} | {r.hit:.1%} | {r.pnl:+,.2f} | {r.roi:+.1%} | {r.mean_p:.3f} |\n"
cov=L.groupby(['week','market']).size().unstack(fill_value=0); cov['games']=L.groupby('week').game_id.nunique()
covt="| week | "+" | ".join(cov.columns)+" |\n|"+"---|"*(len(cov.columns)+1)+"\n"+"".join(f"| {'MNF CHI@SEA' if w==9 else w} | "+" | ".join(str(v) for v in r)+" |\n" for w,r in cov.iterrows())
rep=open('report_template.md').read().replace('@@MAIN@@',t).replace('@@ROI@@',r3).replace('@@COV@@',covt).replace('@@CAL@@',open('calibration.md').read())
open('report.md','w').write(rep)
