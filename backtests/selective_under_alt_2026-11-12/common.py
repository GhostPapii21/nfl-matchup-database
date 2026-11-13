import os, numpy as np, pandas as pd
from scipy.stats import norm
OUT=os.environ.get('OUT','/workspace/research/selective_under_alt_2026-11-12')
CC='/workspace/nfl-database/backtests/confidence_check_2026-11-03'
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(HERE+'/../..')
XGRID=[0.03,0.05,0.08]
def dec(a): a=np.asarray(a,float); return np.where(a>0,1+a/100,1+100/-a)
def nv_mult(do,du): i1,i2=1/np.asarray(do),1/np.asarray(du); return i1/(i1+i2)
def settle(df):
    """df needs win (1/0/nan for push) and dec. returns profit per $1."""
    return np.where(df.push==1,0.0,np.where(df.win==1,df.dec-1,-1.0))
def summarize(df,B=10000,seed=0):
    n=len(df)
    if n==0: return dict(n=0)
    pr=settle(df); dec_=df.dec.values; be=1/dec_; nonpush=(df.push!=1).values
    w=int(((df.win==1)&nonpush).sum()); l=int(((df.win==0)&nonpush).sum()); p=int((~nonpush).sum())
    hit=w/max(w+l,1); beb=float(be[nonpush].mean()) if nonpush.any() else np.nan
    out=dict(n=n,W=w,L=l,P=p,hit=hit,be=beb,margin=hit-beb,roi=float(pr.mean()),
             nv=float(df.p_nv.mean()) if 'p_nv' in df and df.p_nv.notna().any() else np.nan, small=n<30)
    # game-cluster bootstrap for margin and ROI
    df=df.assign(_pr=pr,_be=be,_np=nonpush.astype(int),_w=((df.win==1)&nonpush).astype(int))
    df=df.assign(_beN=df._be*df._np,_one=1)
    S=df.groupby('game_id')[['_pr','_beN','_np','_w','_one']].sum().values
    rng=np.random.default_rng(seed); k=len(S); m=[];r=[]
    for _ in range(B):
        s=S[rng.integers(0,k,k)].sum(0)
        if s[2]==0: continue
        m.append(s[3]/s[2]-s[1]/s[2]); r.append(s[0]/s[4])
    out.update(margin_lo=float(np.percentile(m,2.5)),margin_hi=float(np.percentile(m,97.5)),
               roi_lo=float(np.percentile(r,2.5)),roi_hi=float(np.percentile(r,97.5)))
    return out
def table(df,by,**kw):
    rows=[]
    for k,g in df.groupby(by):
        k=k if isinstance(k,tuple) else (k,)
        rows.append(dict(zip(by,k),**summarize(g,**kw)))
    rows.append(dict({b:'ALL' for b in by},**summarize(df,**kw)))
    return pd.DataFrame(rows)

def load_cands():
    C=pd.read_csv(OUT+'/candidates.csv',low_memory=False)
    C['gate_rb']=C.gate_rb.astype(str).str.lower().isin(['true','1','1.0'])
    C['pm_key']=np.where(C.kind=='alt',C.game_id+'|'+C.gsis.fillna('')+'|'+C.market+'|'+C.side.astype(str),'')
    return C
def control_flags(C,X):
    """Pre-registered control rule. Under/spread: edge vs no-vig >= X. Alt: best-EV rung with EV > EV_main and edge vs BE >= X."""
    C=C[C.gate_rb]
    u=C[(C.kind.isin(['under','spread']))&(C.edge>=X-1e-12)]
    a=C[(C.kind=='alt')&(C.ev_better==1)&(C.edge>=X-1e-12)]
    a=a.sort_values('ev').groupby('pm_key').tail(1)
    return pd.concat([u,a])
MKTS=['rushyds','recyds','rec','rushrec','total','spread']
FEATS=['edge','rung_off','skew','skew_missing','carry_share','is_rb','team_spread','spread_missing','be','is_alt']+['m_'+m for m in MKTS]
def featurize(C):
    F=pd.DataFrame(index=C.index)
    F['edge']=C.edge; F['rung_off']=C.rung_off.fillna(0); F['skew']=C['skew'].fillna(0); F['skew_missing']=C['skew'].isna().astype(int)
    F['carry_share']=C.carry_share.fillna(0); F['is_rb']=C.is_rb.fillna(0); F['team_spread']=C.team_spread.fillna(0)
    F['spread_missing']=C.team_spread.isna().astype(int); F['be']=C.be; F['is_alt']=(C.kind=='alt').astype(int)
    for m in MKTS: F['m_'+m]=(C.market==m).astype(int)
    return F[FEATS].astype(float)
def selector_pool(C):
    C=C[C.gate_rb]
    return C[(C.kind.isin(['under','spread']))|((C.kind=='alt')&(C.ev_better==1))]
def apply_selector(C,S):
    P=selector_pool(C).copy(); F=featurize(P)
    z=(F.values-np.array(S['mu']))/np.array(S['sd']); P['p_hat']=1/(1+np.exp(-(S['intercept']+z@np.array(S['coef']))))
    P['sel_margin']=P.p_hat-P.be
    s=P[P.sel_margin>=S['min_margin']]
    a=s[s.kind=='alt'].sort_values('sel_margin').groupby('pm_key').tail(1)
    return pd.concat([s[s.kind!='alt'],a])
