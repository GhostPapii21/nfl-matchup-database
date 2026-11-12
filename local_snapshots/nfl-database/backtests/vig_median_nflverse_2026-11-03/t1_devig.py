from common import *; import json
d=legs().dropna(subset=['over_price','under_price','hit_over']).reset_index(drop=True)
do,du=dec(d.over_price),dec(d.under_price); d['p_mult']=mult(do,du); d['p_pow']=power(do,du); y=d.hit_over.values.astype(float)
print('check nv_over==mult max abs diff', float(np.abs(d.p_mult-d.nv_over).max()))
d['set']=np.where(d.week<=6,'fit','holdout'); rows=[]; res={}
for s in ['fit','holdout','all']:
    x=d if s=='all' else d[d.set==s]
    for mk in ['ALL']+sorted(x.market.unique()):
        z=(x if mk=='ALL' else x[x.market==mk]).reset_index(drop=True); yy=z.hit_over.values.astype(float)
        bm,bp=brier(z.p_mult.values,yy),brier(z.p_pow.values,yy); lm,lp=ll(z.p_mult.values,yy),ll(z.p_pow.values,yy)
        f=lambda q:((q.p_pow-q.hit_over)**2).mean()-((q.p_mult-q.hit_over)**2).mean()
        g=lambda q:(-(q.hit_over*np.log(q.p_pow)+(1-q.hit_over)*np.log(1-q.p_pow))).mean()-(-(q.hit_over*np.log(q.p_mult)+(1-q.hit_over)*np.log(1-q.p_mult))).mean()
        ci=cluster_boot(f,z,'game_id',B=10000 if mk=='ALL' else 2000); cil=cluster_boot(g,z,'game_id',B=10000 if mk=='ALL' else 2000)
        rows.append(dict(set=s,market=mk,n=len(z),hold_mean=float(((1/dec(z.over_price)+1/dec(z.under_price))-1).mean()),brier_mult=bm,brier_pow=bp,d_brier=bp-bm,d_brier_lo=ci[0],d_brier_hi=ci[1],ll_mult=lm,ll_pow=lp,d_ll=lp-lm,d_ll_lo=cil[0],d_ll_hi=cil[1],mean_shift=float((z.p_pow-z.p_mult).mean())))
t=pd.DataFrame(rows); t.to_csv('t1_devig.csv',index=False); print(t.round(5).to_string())
