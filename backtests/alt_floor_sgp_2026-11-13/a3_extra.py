"""a3: (i) all k-combination same-game slips from cushion-rule legs (game-weighted), (ii) breakdowns by position and price band,
(iii) wide-under hit rate vs main total (no alt price: break-even UNKNOWN)."""
import itertools, json, numpy as np, pandas as pd
LC=pd.read_csv('LEGLEVEL_floor_cushion_legs.csv'); LC=LC[~LC.void]
L0=pd.read_csv('LEGLEVEL_floor_p40_legs.csv'); L0=L0[~L0.void]
def settle(df): return np.where(df.push==1,0.0,np.where(df.win==1,df.dec-1,-1.0))
rows=[]
for name,D in (('cushion',LC),('no_cushion_p40',L0)):
    D=D.sort_values('cushion_pct').groupby(['game_id','gsis']).tail(1)
    for k in [6,7,8]:
        per=[]
        for gid,g in D.groupby('game_id'):
            if len(g)<k: continue
            dd=g.dec.values; ww=g.win.fillna(1).values; pp=g.push.values
            dd=np.where((pp==1),1.0,dd)
            cs=list(itertools.combinations(range(len(g)),k))
            if len(cs)>20000: cs=[tuple(sorted(np.random.default_rng(0).choice(len(g),k,replace=False))) for _ in range(20000)]
            pr=np.array([np.prod(dd[list(c)]) for c in cs]); wn=np.array([ww[list(c)].all() for c in cs])
            per.append(dict(game_id=gid,split=g.split.iloc[0],n_combos=len(cs),hit=wn.mean(),roi=np.mean(np.where(wn,pr-1,-1)),med_dec=np.median(pr)))
        P=pd.DataFrame(per)
        if P.empty: continue
        for sp,g in P.groupby('split'):
            rows.append(dict(pool=name,k=k,split=sp,games=len(g),combos=int(g.n_combos.sum()),game_wtd_hit=round(g.hit.mean(),4),
                game_wtd_roi_indep=round(g.roi.mean(),4),med_indep_dec=round(g.med_dec.median(),3),games_with_any_win=int((g.hit>0).sum()),label='SMALL_games<30'))
pd.DataFrame(rows).to_csv('results_sgp_all_combos.csv',index=False)
# breakdowns
def s(g):
    pr=settle(g); return pd.Series(dict(n=len(g),hit=round((g.win==1).mean(),4),be=round((1/g.dec).mean(),4),margin_pts=round(100*((g.win==1).mean()-(1/g.dec).mean()),2),roi=round(pr.mean(),4)))
LC['pos']=LC.position.fillna('UNK'); LC['band']=pd.cut(1/LC.dec,[0,0.7,0.8,0.9,1.0],labels=['BE<70%','70-80%','80-90%','90%+'])
b1=LC.groupby(['split','pos']).apply(s).reset_index(); b2=LC.groupby(['split','band'],observed=True).apply(s).reset_index()
b1.to_csv('results_cushion_by_position.csv',index=False); b2.to_csv('results_cushion_by_price_band.csv',index=False)
# wide under descriptive (main totals, weeks 6-9, inventory)
T=pd.read_csv('alt_totals_quotes.csv'); g=T[['week','game_id','main_total','act_total']].drop_duplicates('game_id').dropna()
w=[]
for W in [7,10,14]:
    for sp,gg in g.assign(split=np.where(g.week<=7,'train_wk6_7','oos_wk8_9')).groupby('split'):
        w.append(dict(rule=f'total < main+{W}',split=sp,n_games=len(gg),hit=round((gg.act_total<gg.main_total+W).mean(),4),be='UNKNOWN (no alt price)'))
pd.DataFrame(w).to_csv('results_wide_under_no_price.csv',index=False)
print(pd.DataFrame(rows).to_string()); print(b1.to_string()); print(b2.to_string()); print(pd.DataFrame(w).to_string())
