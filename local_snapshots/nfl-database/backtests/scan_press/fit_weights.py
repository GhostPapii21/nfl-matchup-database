"""Walk-forward fit of slate_scan component weights. Train on weeks 3-7 (wk1-2 data feed features/lines only;
stand-in lines need >=2 prior games), test on week 8. No week-8 outcomes are used in the fit."""
import json, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
S=["s_allow","s_explosive","s_qb","s_script","s_weather","s_promo","s_rb2","s_deep","s_repeat"]
u=pd.read_csv("universe.csv"); u=u[u.market!="pyds"].dropna(subset=["hit"])
def X(d):
    x=d[S].fillna(0).copy()
    for m in ("ryds","rec","recyds"): x["m_"+m]=(d.market==m).astype(float)
    return x
def fit(train,C=0.5):
    x=X(train); mu,sd=x.mean(),x.std().replace(0,1)
    lr=LogisticRegression(C=C,max_iter=2000).fit((x-mu)/sd,train.hit.astype(int))
    w=pd.Series(lr.coef_[0],x.columns)/sd; return w, float(lr.intercept_[0]-(w*mu).sum())
def roi(h,price):
    pay=100/abs(price); return float((h*pay-(1-h)).mean()) if len(h) else float("nan")
res={}
# walk-forward per week for stability, then the wk8 test
for wk in (5,6,7,8):
    tr=u[(u.week<wk)&(u.week>=3)]; te=u[u.week==wk].copy(); w,b=fit(tr)
    te["new"]=X(te)@w+b; te["old"]=te["score"]
    for col in ("old","new"):
        t=te.sort_values(col,ascending=False); top=t.head(50)
        res.setdefault(col,{})[wk]=dict(n=len(top),hit=round(top.hit.mean(),3),roi110=round(roi(top.hit,-110),3),roi130=round(roi(top.hit,-130),3),roi160=round(roi(top.hit,-160),3))
    if wk==8: W8,te8=(w,b),te
json.dump({"weights_fit_wk3_7":W8[0].round(4).to_dict(),"intercept":W8[1]},open("scan_weights_wk8.json","w"),indent=1)
te8["rank_old"]=te8.old.rank(ascending=False,method="first").astype(int); te8["rank_new"]=te8.new.rank(ascending=False,method="first").astype(int)
tgt={"Braelon Allen":"ryds","Kenny Gainwell":"ryds","Adonai Mitchell":"recyds","Emmett Johnson":"recyds","Chase Brown":"rec"}
print("of",len(te8),"wk8 candidates")
for n,m in tgt.items():
    r=te8[(te8.name==n)&(te8.market==m)]
    if len(r): r=r.iloc[0]; print(f"{n:16s} {m:7s} line {r.line} act {r.actual}  old {r.rank_old} -> new {r.rank_new}")
for col in ("old","new"):
    a=pd.DataFrame(res[col]).T; print(col,"top-50/wk\n",a.to_string())
    h=np.concatenate([u[u.week==wk].assign(s=lambda d:(X(d)@fit(u[(u.week<wk)&(u.week>=3)])[0]) if col=="new" else d.score).sort_values("s",ascending=False).head(50).hit.values for wk in (5,6,7,8)])
    print(col,"pooled wk5-8 top50: n",len(h),"hit",round(h.mean(),3),"roi",[round(roi(h,p),3) for p in (-110,-130,-160)])
print(W8[0].round(3).to_string())
