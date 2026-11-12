import numpy as np, pandas as pd
from scipy.optimize import brentq, minimize
CC='/workspace/nfl-database/backtests/confidence_check_2026-11-03'
EPS=1e-4
def dec(a): a=np.asarray(a,float); return np.where(a>0,1+a/100,1+100/-a)
def mult(do,du): i1,i2=1/do,1/du; return i1/(i1+i2)
def power1(do,du):
    i1,i2=1/do,1/du
    if i1+i2<=1: return i1/(i1+i2)
    k=brentq(lambda k:i1**k+i2**k-1,1,50); return i1**k
def power(do,du): return np.array([power1(a,b) for a,b in zip(do,du)])
def logit(p): p=np.clip(np.asarray(p,float),EPS,1-EPS); return np.log(p/(1-p))
def sig(x): return 1/(1+np.exp(-x))
def brier(p,y): return float(np.mean((p-y)**2))
def ll(p,y): p=np.clip(p,EPS,1-EPS); return float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p)))
def cluster_boot(stat_fn, df, cl, B=10000, seed=0):
    """stat_fn(sub_df)->float; resample clusters with replacement."""
    rng=np.random.default_rng(seed); groups=[g.index.values for _,g in df.groupby(cl)]; G=len(groups); out=np.empty(B)
    for b in range(B):
        idx=np.concatenate([groups[i] for i in rng.integers(0,G,G)]); out[b]=stat_fn(df.loc[idx])
    return float(np.percentile(out,2.5)), float(np.percentile(out,97.5))
def fit_logit(X,y,off=None,l2=1.0):
    X=np.column_stack([np.ones(len(X)),X]); off=np.zeros(len(y)) if off is None else off
    def nll(w): z=off+X@w; return np.sum(np.logaddexp(0,z)-y*z)+l2*(w[1:]**2).sum()/2
    return minimize(nll,np.zeros(X.shape[1]),method='BFGS').x
def pred_logit(w,X,off=None):
    X=np.column_stack([np.ones(len(X)),X]); off=np.zeros(len(X)) if off is None else off; return sig(off+X@w)
def legs():
    d=pd.read_csv(CC+'/legs_with_probs.csv'); return d[d.week.between(3,8)].reset_index(drop=True)
