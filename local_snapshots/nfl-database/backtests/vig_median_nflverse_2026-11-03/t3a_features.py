"""T3a: nflverse (CC-BY-4.0) snap counts + FTN Data via nflverse (CC-BY-SA 4.0) charting -> features from PRIOR weeks only."""
from common import *
P=pd.read_parquet('/workspace/nfl-database/runs/2026-11-02_shared_src/play_by_play_2026.parquet',columns=['game_id','play_id','posteam','defteam','week','pass','rush'])
F=pd.read_parquet('data/ftn_charting_2026.parquet'); F=F.drop(columns=['week']).merge(P,left_on=['nflverse_game_id','nflverse_play_id'],right_on=['game_id','play_id'],how='inner')
F=F[(F['pass']==1)|(F['rush']==1)]
S=pd.read_parquet('data/snap_counts_2026.parquet')
def opp_feats(team,W):
    x=F[(F.defteam==team)&(F.week<W)]; dp=x[x['pass']==1]
    return dict(opp_blitz=(dp.n_blitzers.fillna(0)>0).mean(),opp_rushers=dp.n_pass_rushers.mean(),opp_box=x.n_defense_box.mean(),
                opp_pa_faced=dp.is_play_action.astype(float).mean(),opp_motion_faced=x.is_motion.astype(float).mean())
def snap(player,team,W):
    x=S[(S.player==player)&(S.team==team)&(S.week<W)].sort_values('week')
    return dict(snap_l2=x.offense_pct.tail(2).mean() if len(x) else np.nan, snap_trend=(x.offense_pct.tail(2).mean()-x.offense_pct.mean()) if len(x)>=2 else 0.0)
d=legs().dropna(subset=['hit_over']).reset_index(drop=True)
cache={}
for i,r in d.iterrows():
    k=(r.opp,r.week); cache.setdefault(k,opp_feats(r.opp,r.week))
    for a,b in {**cache[k],**snap(r.player,r.team,r.week)}.items(): d.loc[i,a]=b
FE=['opp_blitz','opp_rushers','opp_box','opp_pa_faced','opp_motion_faced','snap_l2','snap_trend']
d['grp']=d.market.map({'rushyds':'rush','rushrec':'rush','recyds':'rec','rec':'rec','passyds':'pass'})
print('feature coverage', d[FE].notna().mean().round(3).to_dict())
d[FE]=d[FE].fillna(d[d.week<=6][FE].mean())
fit,ho=d[d.week<=6],d[d.week>=7].copy(); ho['p_model']=np.nan
for gname in d.grp.unique():
    tr=fit[fit.grp==gname]; mu,sd=tr[FE].mean(),tr[FE].std().replace(0,1)
    w=fit_logit(((tr[FE]-mu)/sd).values,tr.hit_over.values.astype(float),off=logit(tr.nv_over.values),l2=1.0)
    m=ho.grp==gname; ho.loc[m,'p_model']=pred_logit(w,((ho.loc[m,FE]-mu)/sd).values,off=logit(ho.loc[m,'nv_over'].values))
    print(gname,'n_fit',len(tr),'w',dict(zip(['a']+FE,np.round(w,3))))
ho=ho.reset_index(drop=True); y=ho.hit_over.values.astype(float)
f=lambda q:((q.p_model-q.hit_over)**2).mean()-((q.nv_over-q.hit_over)**2).mean()
rows=[]
for mk in ['ALL']+sorted(ho.market.unique()):
    z=(ho if mk=='ALL' else ho[ho.market==mk]).reset_index(drop=True); ci=cluster_boot(f,z,'game_id',B=10000 if mk=='ALL' else 2000)
    rows.append(dict(market=mk,n=len(z),brier_mkt=brier(z.nv_over.values,z.hit_over.values),brier_model=brier(z.p_model.values,z.hit_over.values),d=float(f(z)),lo=ci[0],hi=ci[1],ll_mkt=ll(z.nv_over.values,z.hit_over.values),ll_model=ll(z.p_model.values,z.hit_over.values)))
r=pd.DataFrame(rows); r.to_csv('t3a_features.csv',index=False); print(r.round(5).to_string()); d.to_csv('t3a_leg_features.csv',index=False)
