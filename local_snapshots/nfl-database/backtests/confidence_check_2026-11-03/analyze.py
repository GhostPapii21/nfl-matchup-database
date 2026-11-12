import glob,json,numpy as np,pandas as pd
L=pd.read_csv('legs.csv'); K=['week','gsis','market']
ENG=['sim_v5','sim_v6','sim_v6_fix']; VER={'V1 old (30% shrink, opp 0.5)':('0.5',True),'V2 no shrink, opp 0.5':('0.5',False),'V3 no shrink, opp 1.0':('1.0',False)}
S={}
for e in ENG:
    for o in ('0.5','1.0'):
        d=pd.concat([pd.read_csv(f) for f in glob.glob(f'sims/{e}_opp{o}_w*.csv')])
        if 'err' in d: d=d[d.err.isna()]
        d['p']=d[['p_mc','p_bias','p_gr']].mean(axis=1); S[(e,o)]=d[K+['p']].rename(columns={'p':f'{e}|{o}'})
D=L.copy()
for v in S.values(): D=D.merge(v,on=K,how='inner')   # same legs for every row
y=D.hit_over.values; mkt=D.nv_over.values; EPS=1e-3
brier=lambda p:float(np.mean((p-y)**2)); ll=lambda p:float(-np.mean(y*np.log(np.clip(p,EPS,1-EPS))+(1-y)*np.log(np.clip(1-p,EPS,1-EPS))))
dec=lambda a:1+a/100 if a>0 else 1+100/(-a)
imp=lambda o:100/(o+100) if o>0 else -o/(-o+100)
rng=np.random.default_rng(1); games=D.game_id.values; ug=np.unique(games); gi={g:np.where(games==g)[0] for g in ug}
def boot(p):  # game-clustered paired bootstrap of Brier(model)-Brier(market)
    dd=(p-y)**2-(mkt-y)**2; r=[]
    for _ in range(2000):
        idx=np.concatenate([gi[g] for g in rng.choice(ug,len(ug))]); r.append(dd[idx].mean())
    return np.percentile(r,[2.5,97.5])
def probs(e,ver):
    o,sh=VER[ver]; p=D[f'{e}|{o}'].values.copy()
    return 0.5+0.7*(p-0.5) if sh else p
rows=[]; cal={}; roi=[]; bymk=[]; byweek=[]
BINS=[0,.40,.50,.55,.60,.65,.70,.80,1.0001]; LAB=['0-40','40-50','50-55','55-60','60-65','65-70','70-80','80+']
for e in ENG:
    for ver in VER:
        p=probs(e,ver); ci=boot(p)
        rows.append(dict(sim=e,version=ver,N=len(p),brier=brier(p),logloss=ll(p),mkt_brier=brier(mkt),mkt_logloss=ll(mkt),d_brier=brier(p)-brier(mkt),ci_lo=ci[0],ci_hi=ci[1],
                         mean_p_over=p.mean(),mean_abs_dev_from_mkt=np.mean(np.abs(p-mkt))))
        # over-side calibration
        b=pd.cut(p,BINS,labels=LAB,right=False); c=pd.DataFrame(dict(b=b,p=p,y=y,m=mkt)).groupby('b',observed=False).agg(n=('y','size'),pred=('p','mean'),hit=('y','mean'),mkt=('m','mean'))
        # model-favored side calibration
        fav=np.maximum(p,1-p); yf=np.where(p>=.5,y,1-y); mf=np.where(p>=.5,mkt,1-mkt)
        cf=pd.DataFrame(dict(b=pd.cut(fav,BINS[2:],labels=LAB[2:],right=False),p=fav,y=yf,m=mf)).groupby('b',observed=False).agg(n=('y','size'),pred=('p','mean'),hit=('y','mean'),mkt=('m','mean'))
        cal[(e,ver)]=(c,cf)
        # +3 vs no-vig flat $10
        eo=p-mkt; pl=[]; 
        for i,r in D.reset_index(drop=True).iterrows():
            if eo[i]>=.03: side,pr,win=('over',r.over_price,y[i]==1)
            elif -eo[i]>=.03: side,pr,win=('under',r.under_price,y[i]==0)
            else: continue
            pl.append(dict(sim=e,version=ver,week=r.week,market=r.market,side=side,edge=abs(eo[i]),p_side=p[i] if side=='over' else 1-p[i],win=win,pnl=10*(dec(pr)-1) if win else -10.0))
        pl=pd.DataFrame(pl); roi.append(pl)
        for mk,g in D.assign(p=p).groupby('market'): bymk.append(dict(sim=e,version=ver,market=mk,n=len(g),brier=float(np.mean((g.p-g.hit_over)**2)),mkt_brier=float(np.mean((g.nv_over-g.hit_over)**2))))
        for w,g in D.assign(p=p).groupby('week'): byweek.append(dict(sim=e,version=ver,week=w,n=len(g),brier=float(np.mean((g.p-g.hit_over)**2)),mkt_brier=float(np.mean((g.nv_over-g.hit_over)**2))))
T=pd.DataFrame(rows); R=pd.concat(roi); BM=pd.DataFrame(bymk); BW=pd.DataFrame(byweek)
T.to_csv('scores.csv',index=False); R.to_csv('plus3_bets.csv',index=False); BM.to_csv('brier_by_market.csv',index=False); BW.to_csv('brier_by_week.csv',index=False)
D.to_csv('legs_with_probs.csv',index=False)
with open('calibration.md','w') as f:
    for (e,ver),(c,cf) in cal.items():
        f.write(f'\n### {e} — {ver}\nOver-side probability bins:\n\n| bin | n | mean pred | actual hit | market nv |\n|---|---|---|---|---|\n')
        for b,r in c.iterrows(): f.write(f'| {b} | {int(r.n)} | {r.pred:.3f} | {r.hit:.3f} | {r.mkt:.3f} |\n' if r.n else f'| {b} | 0 | - | - | - |\n')
        f.write('\nModel-favored side (prob of the side the model leans):\n\n| bin | n | mean pred | actual hit | market nv (same side) |\n|---|---|---|---|---|\n')
        for b,r in cf.iterrows(): f.write(f'| {b} | {int(r.n)} | {r.pred:.3f} | {r.hit:.3f} | {r.mkt:.3f} |\n' if r.n else f'| {b} | 0 | - | - | - |\n')
RS=R.groupby(['sim','version'],sort=False).agg(bets=('win','size'),W=('win','sum'),pnl=('pnl','sum'),mean_p=('p_side','mean'),mean_edge=('edge','mean')).reset_index()
RS['L']=RS.bets-RS.W; RS['hit']=RS.W/RS.bets; RS['roi']=RS.pnl/(10*RS.bets); RS.to_csv('plus3_roi.csv',index=False)
pd.set_option('display.width',250); print(T.round(4).to_string()); print(RS.round(3).to_string())
print(BW.pivot_table(index=['sim','version'],columns='week',values='brier').round(4)); print(BW.groupby('week')[['n','mkt_brier']].first().round(4))
print(BM.pivot_table(index=['sim','version'],columns='market',values='brier').round(4)); print(BM.groupby('market')[['n','mkt_brier']].first().round(4))
print(R.groupby(['sim','version','side'],sort=False).agg(n=('win','size'),hit=('win','mean'),pnl=('pnl','sum')).round(3))
