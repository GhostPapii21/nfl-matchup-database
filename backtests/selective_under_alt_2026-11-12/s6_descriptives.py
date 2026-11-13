"""Descriptive (not used for any selection): edge-filter vs market baseline, and alt flag shape."""
import pandas as pd, numpy as np
from common import *
C=load_cands(); rows=[]
for lab,ws in (('IS_wk4_7',(4,7)),('OOS_wk8_9',(8,9))):
    D=C[C.week.between(*ws)]
    for name,f in (('all gated rushyds unders (no edge filter)',D[(D.kind=='under')&(D.market=='rushyds')&D.gate_rb]),
                   ('rushyds unders failing RB 60% gate',D[(D.kind=='under')&(D.market=='rushyds')&~D.gate_rb]),
                   ('control X=+5 rushyds unders',control_flags(D,0.05).query("kind=='under' and market=='rushyds'"))):
        sm=summarize(f,B=10000); rows.append(dict(set=lab,slice=name,**{k:sm.get(k) for k in ('n','hit','be','margin','margin_lo','margin_hi','roi','small')}))
    a=control_flags(D,0.05); a=a[a.kind=='alt']
    for mk,g in a.groupby('market'):
        rows.append(dict(set=lab,slice=f'alt flags shape {mk}: median rung_off',n=len(g),hit=float(g.rung_off.median()),be=float(g.be.median()),margin=np.nan,roi=np.nan))
R=pd.DataFrame(rows); R.to_csv(HERE+'/results_descriptives.csv',index=False); pd.set_option('display.width',220); print(R.round(3).to_string(index=False))
