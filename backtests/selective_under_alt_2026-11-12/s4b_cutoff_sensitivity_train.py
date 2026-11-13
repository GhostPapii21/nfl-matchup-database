"""TRAIN-only (Weeks 4-7) probability-cutoff sensitivity: is the edge the filter or the number?
For gated main unders (props/totals), spread sides and alt rungs with EV>main: pick if p_model >= cutoff. Descriptive only, not used to tune."""
import numpy as np, pandas as pd
from common import *
C=load_cands(); T=selector_pool(C[C.week.between(4,7)])
rows=[]
for cut in (0.0,0.50,0.55,0.58,0.60,0.62,0.65):
    for kd in ('under','alt','spread'):
        for mk,g in T[(T.kind==kd)].groupby('market'):
            f=g[g.p_model>=cut]
            if kd=='alt': f=f.sort_values('p_model').groupby('pm_key').tail(1)
            sm=summarize(f,B=2000) if len(f) else dict(n=0)
            rows.append(dict(cutoff=cut,kind=kd,market=mk,pool=len(g),**{k:sm.get(k,np.nan) for k in ('n','hit','be','margin','roi','margin_lo','margin_hi','small')}))
R=pd.DataFrame(rows); R.to_csv(HERE+'/results_cutoff_sensitivity_train.csv',index=False)
pd.set_option('display.width',220); print(R.round(3).to_string(index=False))
