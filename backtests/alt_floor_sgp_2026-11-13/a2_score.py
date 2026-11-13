"""a2: floor-leg selection, cushion grid (train Wk6-7 only), OOS scoring Wk8-9, alt-total wide unders, 6-8 leg SGP sims.
Prices: FanDuel when quoted, else median-of-books (flagged). Never invents prices: rungs with no quote are absent."""
import re, json, numpy as np, pandas as pd
rng0=0
def norm(n): n=re.sub(r'\b(jr|sr|ii|iii|iv|v)\b','',str(n).lower().replace('.','').replace("'",'')); return re.sub(r'[^a-z]','',n)
R=pd.read_csv('alt_over_rungs_with_features.csv')
# resolve no-touch players: snaps>0 (wk<=7) -> actual 0 ; else void (unknown)
S=pd.read_parquet('/workspace/nfl56_pr28/data/historical/nflverse/snaps_2026.parquet',columns=['game_id','player','offense_snaps'])
S['k']=S.player.map(norm); S=S.groupby(['game_id','k']).offense_snaps.max()
R['k']=R.player.map(norm)
miss=R.actual.isna()
sn=[S.get((g,k),np.nan) for g,k in zip(R.game_id,R.k)]
R['snaps']=sn
R.loc[miss&(R.snaps>0),'actual']=0.0
R['void']=R.actual.isna()
R['dec']=R.fd_dec.fillna(R.med_dec); R['price_src']=np.where(R.fd_dec.notna(),'fanduel','median_books')
R['be']=1/R.dec
R['push']=(R.actual==R.line).astype(int)
R['win']=np.where(R.void|(R.push==1),np.nan,(R.actual>R.line).astype(float))
R['split']=np.where(R.week<=7,'train_wk6_7','oos_wk8_9')
R['cushion']=R.med-R.line; R['cushion_pct']=R.cushion/R.line.clip(lower=0.5)
# volume gates
rec_m=R.market.isin(['recyds','rec']); rush_m=R.market.isin(['rushyds','rushrec'])
R['gate_vol']=np.where(rec_m,(R.tgt_sh>=0.15)&(R.med_tgt>=4),np.where(rush_m,(R.position=='RB')&(R.n60>=3),False))
R['gate_vol']&=(R.n_prior>=3)
R['defender_gate']=np.where(rec_m|(R.market=='rushrec'),'UNVERIFIABLE_historical','n/a')
def settle(df): return np.where(df.push==1,0.0,np.where(df.win==1,df.dec-1,-1.0))
def summ(df,B=10000,seed=0):
    df=df[~df.void] if 'void' in df else df
    n=len(df)
    if n==0: return dict(n=0)
    pr=settle(df); nonp=(df.push!=1).values; w=int(((df.win==1)&nonp).sum()); l=int(((df.win==0)&nonp).sum())
    hit=w/max(w+l,1); be=float((1/df.dec.values)[nonp].mean())
    o=dict(n=n,W=w,L=l,P=n-w-l,hit=round(hit,4),be=round(be,4),margin_pts=round(100*(hit-be),2),roi=round(float(pr.mean()),4),
           med_price_dec=round(float(df.dec.median()),3),fd_share=round(float((df.price_src=='fanduel').mean()),3) if 'price_src' in df else np.nan)
    d=df.assign(_pr=pr,_beN=(1/df.dec)*nonp,_np=nonp.astype(int),_w=((df.win==1)&nonp).astype(int),_one=1)
    A=d.groupby('game_id')[['_pr','_beN','_np','_w','_one']].sum().values
    r=np.random.default_rng(seed); k=len(A); M=[];Q=[]
    for _ in range(B):
        s=A[r.integers(0,k,k)].sum(0)
        if s[2]==0: continue
        M.append(s[3]/s[2]-s[1]/s[2]); Q.append(s[0]/s[4])
    o.update(margin_ci=[round(100*np.percentile(M,2.5),2),round(100*np.percentile(M,97.5),2)],roi_ci=[round(np.percentile(Q,2.5),4),round(np.percentile(Q,97.5),4)],games=k)
    o['ready_NFL75']=bool(n>=30 and o['margin_pts']>=3 and o['margin_ci'][0]>0)
    o['label']='ok' if n>=30 else 'SMALL_n<30'
    return o
def pick(df,floor_q='p40',X=0,Y=0.0):
    """per player-game-market: highest rung with line<=floor (pre-game percentile) and cushion>=max(X,Y*line). best price."""
    e=df[df.gate_vol&(df.line<=df[floor_q])&(df.cushion>=X)&(df.cushion>=Y*df.line)&(df.dec>1.0)]
    return e.sort_values('line').groupby(['game_id','gsis','market']).tail(1)
out={'pulled_inputs':{'odds':'sportsbook_latest_verified_pregame.csv (inventory built 2026-11-07, files dated 2026-11-12 6:58 PM ET)','pbp':'nflverse pbp_2026_w1_9 pulled 2026-11-12 11:16 AM ET sha256 1028614b...'}}
# ---- 1. no-cushion floor rule, by market and split, p25 and p40
rows=[]
for fq in ['p25','p40']:
    L=pick(R,fq)
    for (sp,mk),g in L.groupby(['split','market']): rows.append(dict(rule=f'floor<={fq}',split=sp,market=mk,**summ(g)))
    for sp,g in L.groupby('split'): rows.append(dict(rule=f'floor<={fq}',split=sp,market='ALL',**summ(g)))
base=pd.DataFrame(rows)
# ---- 2. cushion grid on TRAIN only
grid=[]
TR=R[R.split=='train_wk6_7']
for fam,mks,Xs in (('yards',['recyds','rushyds','rushrec'],[0,5,10,15,20,25]),('receptions',['rec'],[0,1,2])):
    for X in Xs:
        for Y in [0,0.25,0.5,1.0]:
            L=pick(TR[TR.market.isin(mks)],'p40',X,Y); s=summ(L,B=2000)
            grid.append(dict(family=fam,X=X,Y=Y,**s))
G=pd.DataFrame(grid)
chosen={}
for fam,g in G.groupby('family'):
    g=g[g.n>=30]
    best=g.sort_values(['margin_pts','n'],ascending=[False,False]).iloc[0]
    chosen[fam]=dict(X=float(best.X),Y=float(best.Y),train_n=int(best.n),train_margin=float(best.margin_pts))
json.dump(chosen,open('cushion_rule_frozen_train_wk6_7.json','w'),indent=1)
# ---- 3. apply chosen rule to all splits
def pick_rule(df):
    a=pick(df[df.market.isin(['recyds','rushyds','rushrec'])],'p40',chosen['yards']['X'],chosen['yards']['Y'])
    b=pick(df[df.market=='rec'],'p40',chosen['receptions']['X'],chosen['receptions']['Y'])
    return pd.concat([a,b])
LC=pick_rule(R); rows=[]
for (sp,mk),g in LC.groupby(['split','market']): rows.append(dict(rule='floor<=p40 + cushion',split=sp,market=mk,**summ(g)))
for sp,g in LC.groupby('split'): rows.append(dict(rule='floor<=p40 + cushion',split=sp,market='ALL',**summ(g)))
# FD-only robustness
for sp,g in LC[LC.price_src=='fanduel'].groupby('split'): rows.append(dict(rule='floor<=p40 + cushion (FanDuel-priced only)',split=sp,market='ALL',**summ(g)))
L0=pick(R,'p40')
for sp,g in L0[L0.price_src=='fanduel'].groupby('split'): rows.append(dict(rule='floor<=p40 (FanDuel-priced only)',split=sp,market='ALL',**summ(g)))
cush=pd.DataFrame(rows)
# thin-clear diagnostic: how often legs hit by <= 5 yds / lose
L0=L0.assign(margin_yds=L0.actual-L0.line)
# ---- 4. alt total wide unders (weeks 8-9 only have alt totals)
T=pd.read_csv('alt_totals_quotes.csv'); T=T[(T.selection=='Under')&(T.market=='alternate_totals')]
T['dec']=T.fd_dec.fillna(T.med_dec); T['price_src']=np.where(T.fd_dec.notna(),'fanduel','median_books')
T['push']=(T.act_total==T.line).astype(int); T['win']=np.where(T.push==1,np.nan,(T.act_total<T.line).astype(float)); T['void']=T.act_total.isna()
trows=[]; TT={}
for W in [7,10,14]:
    t=T[T.line>=T.main_total+W].sort_values('line').groupby('game_id').head(1); TT[W]=t
    for wk,g in t.groupby('week'): trows.append(dict(rule=f'alt U >= main+{W}',week=wk,**summ(g)))
    trows.append(dict(rule=f'alt U >= main+{W}',week='8-9',**summ(t)))
tot=pd.DataFrame(trows)
# ---- 5. SGP slips (same game), one leg per player (largest cushion_pct), + alt total U (main+10) when available
LP=LC.sort_values('cushion_pct').groupby(['game_id','gsis']).tail(1)
LP=LP[~LP.void]
srows=[];slips=[]
for k in [6,7,8]:
    for gid,g in LP.groupby('game_id'):
        t=TT[10][TT[10].game_id==gid]
        legs=g.sort_values('cushion_pct',ascending=False)
        use_t=len(t)==1 and not t.void.iloc[0]
        need=k-1 if use_t else k
        if len(legs)<need: continue
        legs=legs.head(need)
        decs=list(legs.dec)+([t.dec.iloc[0]] if use_t else []); wins=list(legs.win.fillna(1))+([t.win.iloc[0] if pd.notna(t.win.iloc[0]) else 1] if use_t else [])
        # push -> leg drops (treated as 1.0); count
        decs=[1.0 if (wn==1 and p==1) else dc for dc,wn,p in zip(decs,wins,list(legs.push)+([t.push.iloc[0]] if use_t else []))]
        price=float(np.prod(decs)); win=int(all(w==1 for w in wins))
        slips.append(dict(k=k,game_id=gid,week=int(g.week.iloc[0]),split=g.split.iloc[0],with_total=use_t,legs_hit=int(sum(wins)),
            indep_dec=round(price,3),indep_american=round((price-1)*100) if price>=2 else round(-100/(price-1)),win=win,profit_indep=price-1 if win else -1.0))
SL=pd.DataFrame(slips)
for (k,sp),g in SL.groupby(['k','split']):
    h=g.win.mean()
    srows.append(dict(k=k,split=sp,n_slips=len(g),wins=int(g.win.sum()),hit=round(h,4),med_indep_dec=round(g.indep_dec.median(),3),
        avg_be_indep=round(float((1/g.indep_dec).mean()),4),roi_at_indep_price=round(g.profit_indep.mean(),4),
        breakeven_dec_from_hit=round(1/h,3) if h>0 else None,share_with_alt_total=round(g.with_total.mean(),3),
        avg_legs_hit=round(g.legs_hit.mean(),2),label='SMALL_n<30' if len(g)<30 else 'ok'))
slip=pd.DataFrame(srows)
# ---- save aggregates
base.to_csv('results_floor_no_cushion.csv',index=False); G.to_csv('results_cushion_grid_train.csv',index=False)
cush.to_csv('results_floor_with_cushion.csv',index=False); tot.to_csv('results_alt_total_unders.csv',index=False)
slip.to_csv('results_sgp_slips_summary.csv',index=False)
SL.to_csv('LEGLEVEL_sgp_slips.csv',index=False); LC.to_csv('LEGLEVEL_floor_cushion_legs.csv',index=False); L0.to_csv('LEGLEVEL_floor_p40_legs.csv',index=False)
thin=L0[~L0.void].groupby('split').apply(lambda g:pd.Series(dict(n=len(g),lost=int((g.win==0).sum()),hit_by_le5=int(((g.win==1)&(g.margin_yds<=5)&(g.market!='rec')).sum()),
     lost_cush_lt10=int(((g.win==0)&(g.cushion<10)&(g.market!='rec')).sum()),lost_cush_ge10=int(((g.win==0)&(g.cushion>=10)&(g.market!='rec')).sum()))))
thin.to_csv('results_thin_clear_diag.csv')
void=dict(rungs_void=int(R.void.sum()),floor_legs_void=int(L0.void.sum()),cushion_legs_void=int(LC.void.sum()))
json.dump(dict(chosen=chosen,void=void),open('meta.json','w'),indent=1,default=str)
pd.set_option('display.width',250)
print(base.drop(columns=['roi_ci']).to_string()); print(chosen); print(cush.drop(columns=['roi_ci']).to_string()); print(tot.to_string()); print(slip.to_string()); print(thin); print(void)
