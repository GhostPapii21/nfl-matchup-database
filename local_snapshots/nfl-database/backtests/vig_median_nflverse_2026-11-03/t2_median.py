from common import *; import glob
S=[]
for e in ['sim_v5','sim_v6','sim_v6_fix']:
    x=pd.concat([pd.read_csv(f) for f in glob.glob(f'sims/{e}_w*.csv')]); x=x[x.get('err').isna()] if 'err' in x else x
    S.append(x.assign(**{f'{e}_mean':x[['mean_mc','mean_bias','mean_gr']].mean(1),f'{e}_med':x[['med_mc','med_bias','med_gr']].mean(1),f'{e}_p':x[['p_mc','p_bias','p_gr']].mean(1)})[['week','gsis','market',f'{e}_mean',f'{e}_med',f'{e}_p']])
s=S[0].merge(S[1],on=['week','gsis','market']).merge(S[2],on=['week','gsis','market']).drop_duplicates(['week','gsis','market'])
d=legs().merge(s,on=['week','gsis','market'],how='left')
print('repro check: |rerun p_v6 - saved sim_v6|0.5| median', float((d.sim_v6_p-d['sim_v6|0.5']).abs().median()), 'legs w/ sims', d.sim_v6_mean.notna().sum(), '/', len(d))
d['mean']=d[[f'{e}_mean' for e in ['sim_v5','sim_v6','sim_v6_fix']]].mean(1); d['med']=d[[f'{e}_med' for e in ['sim_v5','sim_v6','sim_v6_fix']]].mean(1)
d=d.dropna(subset=['mean','med','hit_over']).reset_index(drop=True)
fit=d.week<=6; bias=(d[fit].actual-d[fit].med).groupby(d[fit].market).median(); d['skadj']=d.med+d.market.map(bias)
d['pl_over']=np.where(d.hit_over==1,dec(d.over_price)-1,-1.0); d['pl_under']=np.where(d.hit_over==0,dec(d.under_price)-1,-1.0)
d['skew']=(d['mean']-d.med)/d.line
def bets(proj,m):
    gap=(d[proj]-d.line)/d.line; side=np.where(gap>m,'over',np.where(gap<-m,'under',None)); pl=np.where(side=='over',d.pl_over,np.where(side=='under',d.pl_under,np.nan))
    return pd.Series(pl,index=d.index)
def roi(pl,mask): x=pl[mask].dropna(); return (float(x.mean()) if len(x) else np.nan), len(x)
ho=d.week>=7; base_pl=d.pl_under.where(d.market=='rushyds')
res=[]; MARG=[0,.025,.05,.10]
for proj in ['mean','med','skadj']:
    best=max(MARG,key=lambda m:(roi(bets(proj,m),fit)[0] if roi(bets(proj,m),fit)[1]>=50 else -9))
    for m in sorted(set([0,best])):
        pl=bets(proj,m); r_ho,n_ho=roi(pl,ho); r_fit,n_fit=roi(pl,fit); r_all,n_all=roi(pl,d.week>0)
        z=d[ho].assign(pl=pl[ho],bp=base_pl[ho]).reset_index(drop=True)
        f=lambda q:q.pl.dropna().mean()-q.bp.dropna().mean(); ci=cluster_boot(f,z,'game_id',B=5000)
        xa=pl.dropna(); res.append(dict(rule=proj,margin=m,chosen_on_fit=(m==best),n_fit=n_fit,roi_fit=r_fit,n_ho=n_ho,roi_ho=r_ho,W_ho=int((pl[ho]>0).sum()),L_ho=int((pl[ho]<0).sum()),base_roi_ho=float(base_pl[ho].dropna().mean()),d_vs_base_ho=r_ho-float(base_pl[ho].dropna().mean()),lo=ci[0],hi=ci[1],n_all=n_all,W_all=int((xa>0).sum()),L_all=int((xa<0).sum()),roi_all=r_all,pl_all=float(xa.sum())))
        for mk in sorted(d.market.unique()):
            q=pl[(d.market==mk)].dropna(); res.append(dict(rule=f'{proj}|{mk}',margin=m,n_all=len(q),W_all=int((q>0).sum()),L_all=int((q<0).sum()),roi_all=float(q.mean()) if len(q) else np.nan))
R=pd.DataFrame(res); R.to_csv('t2_rules.csv',index=False); print(R.round(4).to_string())
b=base_pl.dropna(); print('baseline check', len(b), int((b>0).sum()), int((b<0).sum()), round(b.mean(),4))
# skew hypothesis on rushyds
r=d[d.market=='rushyds'].reset_index(drop=True); r['uh']=(r.hit_over==0).astype(float)
w=fit_logit(r[['skew']].values,r.uh.values,l2=0.0)
rng=np.random.default_rng(0); G=[g.index.values for _,g in r.groupby('game_id')]; bs=[]
for _ in range(2000):
    idx=np.concatenate([G[i] for i in rng.integers(0,len(G),len(G))]); bs.append(fit_logit(r.loc[idx,['skew']].values,r.loc[idx,'uh'].values,l2=0.0)[1])
r['tercile']=pd.qcut(r['skew'],3,labels=['low','mid','high'])
T=r.groupby('tercile').agg(n=('uh','size'),under_hit=('uh','mean'),skew_mean=('skew','mean'),under_roi=('pl_under','mean'),med_minus_line=('med',lambda s:0)).drop(columns='med_minus_line')
print('skew slope',w[1],'CI',np.percentile(bs,[2.5,97.5])); print(T)
print('rush: mean skew',r['skew'].mean(),'share med<line',(r.med<r.line).mean(),'share mean<line',(r['mean']<r.line).mean(), 'actual median-line',(r.actual-r.line).median(),'actual mean-line',(r.actual-r.line).mean())
for mk in sorted(d.market.unique()):
    q=d[d.market==mk]; print(mk,'skew',round(q['skew'].mean(),4),'under hit',round((q.hit_over==0).mean(),4),'under roi',round(q.pl_under.mean(),4),'actual mean-med gap/line',round(((q.actual-q.line).mean()-(q.actual-q.line).median())/q.line.mean(),4))
pd.DataFrame(dict(slope=[w[1]],lo=[np.percentile(bs,2.5)],hi=[np.percentile(bs,97.5)])).to_csv('t2_skew_slope.csv',index=False); T.to_csv('t2_skew_terciles.csv')
d.to_csv('t2_legs_meanmed.csv',index=False)
