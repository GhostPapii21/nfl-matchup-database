from common import *
g=pd.read_csv('data/games.csv'); g=g[(g.season<=2025)&g.result.notna()].reset_index(drop=True)
rows=[]
def run(name,df,po,pu,y):
    df=df.assign(do=dec(df[po]),du=dec(df[pu])); df['p']=mult(df.do,df.du); df['y']=y(df)
    df=df[df.y.notna()].reset_index(drop=True); tr,te=df[df.season<=2017],df[df.season>=2018].reset_index(drop=True)
    w=fit_logit(logit(tr.p.values).reshape(-1,1),tr.y.values.astype(float),l2=0.0); te['pc']=pred_logit(w,logit(te.p.values).reshape(-1,1))
    f=lambda q:((q.pc-q.y)**2).mean()-((q.p-q.y)**2).mean()
    ci=cluster_boot(f,te,'game_id',B=10000)
    rows.append(dict(market=name,train_seasons=f'{int(tr.season.min())}-2017',n_train=len(tr),n_test=len(te),a=w[0],b=w[1],brier_raw=brier(te.p.values,te.y.values),brier_platt=brier(te.pc.values,te.y.values),d=float(f(te)),lo=ci[0],hi=ci[1],ll_raw=ll(te.p.values,te.y.values),ll_platt=ll(te.pc.values,te.y.values)))
m=g.dropna(subset=['home_moneyline','away_moneyline']); m=m[m.result!=0]
run('home_moneyline_win',m,'home_moneyline','away_moneyline',lambda q:(q.result>0).astype(float))
s=g.dropna(subset=['home_spread_odds','away_spread_odds','spread_line']); cov=s.result-s.spread_line
run('home_spread_cover',s,'home_spread_odds','away_spread_odds',lambda q:np.where(q.result==q.spread_line,np.nan,(q.result>q.spread_line).astype(float)))
t=g.dropna(subset=['over_odds','under_odds','total_line'])
run('total_over',t,'over_odds','under_odds',lambda q:np.where(q.total==q.total_line,np.nan,(q.total>q.total_line).astype(float)))
r=pd.DataFrame(rows); r.to_csv('t3b_closing_platt.csv',index=False); print(r.round(5).to_string())
