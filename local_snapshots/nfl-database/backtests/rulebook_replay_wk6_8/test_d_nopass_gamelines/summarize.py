import pandas as pd,re,os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L=pd.read_csv('graded_legs.csv'); P=L[L.pool]
def sg(d): 
    w=(d.result=='win').sum(); l=(d.result=='loss').sum(); return f"{len(d)} legs, {w}-{l}, {w/(w+l):.1%}, ${d.profit_single.sum():.2f}"
print('(a) singles before:',sg(P)); print('removed:',sg(P[P.market=='passyds'])); print('after:',sg(P[P.market!='passyds']))
O=pd.concat([pd.read_csv('slips.csv'),pd.read_csv('test_c_4to5/slips.csv')]); O['pool']='original'
S=pd.read_csv('test_d_nopass_gamelines/slips_graded.csv'); S['won']=S.outcome=='win'
A=pd.concat([O,S]); A['won']=A.outcome=='win'
def agg(d): return pd.Series(dict(slips=len(d),won=int(d.won.sum()),hit=round(100*d.won.mean(),1),pl=round(d.profit.sum(),2),roi=round(100*d.profit.sum()/(10*len(d)),1)))
t=A.groupby(['test','pool']).apply(agg); print(t.to_string()); t.to_csv('test_d_nopass_gamelines/comparison.csv')
w=S.groupby(['pool','test','week']).apply(agg); print(w.to_string()); w.to_csv('test_d_nopass_gamelines/by_week.csv')
rows=[]
for s in S.itertuples():
    legs=s.legs.split(' | '); res=s.results.split(); nl=res.count('loss')
    for l,r in zip(legs,res):
        m=re.search(r' (passyds|rushyds|recyds|rec) (over|under) ',l); mk=f"{m[1]} {m[2]}" if m else 'game_total over'
        rows.append(dict(pool=s.pool,test=s.test,slip=s.slip_id,mkt=mk,res=r,only=(r=='loss' and nl==1)))
R=pd.DataFrame(rows); out=[]
for (p,tt),x in R.groupby(['pool','test']):
    g=x.groupby('mkt').agg(legs=('res','size'),W=('res',lambda v:(v=='win').sum()),L=('res',lambda v:(v=='loss').sum()))
    g['hit']=(100*g.W/(g.W+g.L)).round(1); g['slips_killed']=x[x.res=='loss'].groupby('mkt').slip.nunique(); g['only_loser']=x[x.only].groupby('mkt').slip.nunique()
    g=g.fillna(0); g['pool']=p; g['test']=tt; out.append(g.reset_index())
M=pd.concat(out); M.to_csv('test_d_nopass_gamelines/by_market.csv',index=False)
print(M[M.pool=='combined'].sort_values(['test','slips_killed'],ascending=[True,False]).to_string(index=False))
print(S.groupby(['pool','test','door_leglevel']).size().to_string())
