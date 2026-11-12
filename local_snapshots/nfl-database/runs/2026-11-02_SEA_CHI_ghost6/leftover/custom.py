# Custom 3-model sims for markets sim_v6 lacks (fantasy, sacks). 100k each, seed 20261101. Self-derived, approximations flagged.
import numpy as np, json
N=100000; rng=np.random.default_rng(20261101); out={}
# JSN PrizePicks fantasy 21 (rec + 0.1*yds + 6*TD). Inputs = sim_v6 medians per model (raw_sims.json); sigma fitted to P(>59.5).
from scipy.stats import norm
S=json.load(open('raw_sims.json'))['out']
def fant(ymed,p595,rmed,ptd,shock=0.0):
    sig=np.log(ymed/59.5)/norm.ppf(p595)
    z=rng.standard_normal(N)+shock*rng.standard_normal(N)
    y=ymed*np.exp(sig*z)
    r=np.maximum(0,np.round(rmed*np.exp(0.6*sig*z+0.15*rng.standard_normal(N))))
    td=rng.random(N)<ptd*np.clip(y/ymed,0.5,1.6)/1.0
    return r+0.1*y+6*td
y=S['Jaxon Smith-Njigba|recyds|cb1.000']; r=S['Jaxon Smith-Njigba|rec|cb1.000']
for m in ('mc','bias','gr'):
    f=fant(y[m]['median'],y[m]['rungs']['59.5'],r[m]['median'],0.45,0.3 if m=='gr' else 0)
    out[f'jsn_fant_{m}']=dict(p_over21=float((f>21).mean()),median=float(np.median(f)))
# market proxy: FD yds 99.5 nv .50, FD alt 59.5 nv .817, rec 7.5 nv .415 -> median ~7.2; ATD proxy .45
f=fant(99.5,0.817,7.2,0.45); out['jsn_fant_market_proxy']=dict(p_over21=float((f>21).mean()),median=float(np.median(f)))
# Darnold sacks 2.0 (push at 2). dropbacks ~35 (Darnold Wk3-7 mean 38, team -3 fav).
dr=13/190; chi=19/216; lg=0.065
for m,rate,sh in (('mc',dr*chi/lg,0),('bias',0.5*(dr+chi)*1.05,0),('gr',dr*chi/lg,0.25)):  # bias: +5% for LT Cross OUT (Josh Jones)
    lam=35*rate*np.exp(sh*rng.standard_normal(N)-sh**2/2)
    k=rng.poisson(lam); out[f'darnold_sacks_{m}']=dict(lam=float(35*rate),p_over=float((k>=3).mean()),p_push=float((k==2).mean()),p_under=float((k<=1).mean()))
json.dump(out,open('custom_sims.json','w'),indent=1); print(json.dumps(out,indent=0))
