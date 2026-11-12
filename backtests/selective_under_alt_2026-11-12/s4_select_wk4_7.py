"""Step 4: score control flags on Weeks 4-7 ONLY; choose strong markets; train + freeze selector. Weeks 8-9 outcomes not read."""
import json, hashlib, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from common import *
C=load_cands(); T=C[C.week.between(4,7)].copy()
assert T.week.max()<=7
res=[]
for X in XGRID:
    f=control_flags(T,X)
    t=table(f,['kind','market']); t.insert(0,'X',X); res.append(t)
R=pd.concat(res); R.to_csv(HERE+'/results_control_wk4_7.csv',index=False)
r5=R[(R.X==0.05)&(R.kind!='ALL')]
strong=r5[(r5.n>=30)&(r5.roi>0)&(r5.margin>0)][['kind','market','n','hit','be','margin','roi']]
json.dump(dict(frozen_et=pd.Timestamp.now(tz='America/New_York').isoformat(),rule='control X=+5 gated, Weeks 4-7: n>=30, ROI>0, margin>0',
               strong=strong.to_dict('records')),open(HERE+'/strong_markets_wk4_7.json','w'),indent=1,default=float)
# selector
P=selector_pool(T); P=P[P.push!=1]; F=featurize(P); y=P.win.values.astype(int)
mu=F.mean().values; sd=F.std().replace(0,1).values
m=LogisticRegression(C=0.5,max_iter=2000).fit((F.values-mu)/sd,y)
S=dict(frozen_et=pd.Timestamp.now(tz='America/New_York').isoformat(),trained_on='Weeks 4-7',n_train=int(len(y)),
       train_by_kind_market=P.groupby(['kind','market']).size().rename('n').reset_index().to_dict('records'),
       features=FEATS,mu=mu.tolist(),sd=sd.tolist(),coef=m.coef_[0].tolist(),intercept=float(m.intercept_[0]),C=0.5,min_margin=0.03,
       dedup='one alt rung per player-market (highest p_hat-BE)')
json.dump(S,open(HERE+'/selector_frozen.json','w'),indent=1)
s=apply_selector(T,S); ts=table(s,['kind','market']); ts.to_csv(HERE+'/results_selector_wk4_7.csv',index=False)
pd.set_option('display.width',250)
cols=['X','kind','market','n','W','L','P','hit','be','margin','margin_lo','margin_hi','roi','roi_lo','roi_hi','small']
print(R[cols].round(3).to_string(index=False)); print('STRONG:',strong.to_string(index=False))
print(dict(zip(FEATS,np.round(m.coef_[0],3))))
print(ts[cols[1:]].round(3).to_string(index=False))
