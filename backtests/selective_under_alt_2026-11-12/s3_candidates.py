"""Step 3: build every candidate (main unders, spread sides, alt rungs) for Weeks 4-9 with model p, real price, no-vig,
gates and selector features. Flags depend only on pre-kick info; outcome columns (win/push) are attached for later scoring."""
import glob, numpy as np, pandas as pd
from scipy.stats import norm
from common import *
NAMES={'Arizona Cardinals':'ARI','Atlanta Falcons':'ATL','Baltimore Ravens':'BAL','Buffalo Bills':'BUF','Carolina Panthers':'CAR',
'Chicago Bears':'CHI','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE','Dallas Cowboys':'DAL','Denver Broncos':'DEN','Detroit Lions':'DET',
'Green Bay Packers':'GB','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC',
'Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Los Angeles Rams':'LA','Miami Dolphins':'MIA','Minnesota Vikings':'MIN',
'New England Patriots':'NE','New Orleans Saints':'NO','New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI',
'Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF','Seattle Seahawks':'SEA','Tampa Bay Buccaneers':'TB','Tennessee Titans':'TEN',
'Washington Commanders':'WAS'}
ENS=['sim_v5|0.5','sim_v6|0.5','sim_v6_fix|0.5']
# ---------- props ----------
L=pd.read_csv(CC+'/legs_with_probs.csv'); L=L[L.week.between(4,9)&(L.market!='passyds')].copy()
L['p_over']=L[ENS].mean(axis=1)
T2='/workspace/nfl-database/backtests/vig_median_nflverse_2026-11-03/t2_legs_meanmed.csv'
t2=pd.read_csv(T2,usecols=['week','gsis','market','line','mean','med'])
L=L.merge(t2.drop_duplicates(['week','gsis','market','line']),on=['week','gsis','market','line'],how='left')
L['skew']=(L['mean']-L['med'])/L.line.clip(lower=1)
pos=pd.read_parquet('/workspace/nfl-database/runs/2026-11-02_shared_src/players.parquet',columns=['gsis_id','position']).rename(columns={'gsis_id':'gsis'})
L=L.merge(pos.drop_duplicates('gsis'),on='gsis',how='left')
# carry shares (prior weeks only)
P=pd.read_parquet(REPO+'/data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet',
                  columns=['week','game_id','posteam','rush_attempt','rusher_player_id','receiver_player_id','qb_kneel','pass_attempt'])
ru=P[(P.rush_attempt==1)&(P.qb_kneel!=1)]
tc=ru.groupby(['game_id','posteam']).size().rename('team_car')
pc=ru.groupby(['week','game_id','posteam','rusher_player_id']).size().rename('car').reset_index().rename(columns={'rusher_player_id':'gsis'})
tg=P[P.pass_attempt==1].groupby(['week','game_id','posteam','receiver_player_id']).size().rename('tgt').reset_index().rename(columns={'receiver_player_id':'gsis'})
app=pd.concat([pc[['week','game_id','posteam','gsis']],tg[['week','game_id','posteam','gsis']]]).drop_duplicates()
app=app.merge(pc,how='left',on=['week','game_id','posteam','gsis']).merge(tc.reset_index(),on=['game_id','posteam'],how='left')
app['share']=app.car.fillna(0)/app.team_car
def carry(g,W):
    h=app[(app.gsis==g)&(app.week<W)].sort_values('week').tail(4)
    return (len(h), int((h.share>=0.6).sum()), float(h.share.mean()) if len(h) else np.nan)
cs={(g,w):carry(g,w) for g,w in L[['gsis','week']].drop_duplicates().itertuples(index=False)}
L['n_prior'],L['n60'],L['carry_share']=zip(*[cs[(g,w)] for g,w in zip(L.gsis,L.week)])
L['is_rb']=L.position.isin(['RB','FB']).astype(int)
rbmk=L.market.isin(['rushyds','rushrec'])&(L.is_rb==1)
L['gate_rb']=np.where(rbmk,(L.n_prior>=3)&(L.n60>=3),True)
L['rec_ungated']=L.market.isin(['recyds','rec','rushrec']).astype(int)
L['do']=dec(L.over_price); L['du']=dec(L.under_price); L['nv_over']=nv_mult(L.do,L.du)
L['ev_main']=np.maximum(L.p_over*L.do-1,(1-L.p_over)*L.du-1)
L['push']=(L.actual==L.line).astype(int)
base=dict(kind='under',side='Under')
U=L.assign(kind='under',side='Under',p_model=1-L.p_over,p_nv=1-L.nv_over,dec=L.du,rung=L.line,main_line=L.line,
           win=np.where(L.push==1,np.nan,(L.actual<L.line).astype(float)),rung_off=0.0)
U['edge']=U.p_model-U.p_nv
# alt rungs
A=pd.read_csv(OUT+'/alt_rungs_props.csv')
S=pd.concat([pd.read_csv(f) for f in glob.glob(OUT+'/altsims/*.csv')])
S=S.groupby(['week','gsis','market','rung']).p_over.mean().reset_index()   # ensemble of 3 engines
A=A.merge(S,on=['week','gsis','market','rung'],how='inner')
keep=['week','game_id','player','gsis','team','market','line','team_spread','is_rb','carry_share','n_prior','n60','gate_rb','rec_ungated','skew','ev_main','actual','position']
A=A.merge(L[keep],on=['week','game_id','gsis','market'],how='inner',suffixes=('','_l'))
A=A.assign(kind='alt',side='Over',p_model=A.p_over,p_nv=np.nan,main_line=A.line,
           push=(A.actual==A.rung).astype(int))
A['win']=np.where(A.push==1,np.nan,(A.actual>=A.rung).astype(float))
A['edge']=A.p_model-1/A.dec; A['rung_off']=(A.rung-A.main_line)/A.main_line.clip(lower=1)
A['ev']=A.p_model*A.dec-1; A['ev_better']=(A.ev>A.ev_main).astype(int)
# ---------- games ----------
G=pd.read_csv(REPO+'/calibration/outputs/backtest_wk04_09_n2000_per_game.csv'); G=G[G.arm=='new_off']
Q=pd.read_csv(OUT+'/game_quotes.csv')
def pnorm_win(mu,sd,L,side):
    """P(win), P(push) for 'Under' total L / 'cover' with margin threshold"""
    if float(L).is_integer():
        pp=norm.cdf(L+0.5,mu,sd)-norm.cdf(L-0.5,mu,sd); pu=norm.cdf(L-0.5,mu,sd)
    else: pp=0.0; pu=norm.cdf(L,mu,sd)
    return (pu if side=='Under' else 1-pu-pp), pp
rows=[]
for gid,q in Q.groupby('game_id'):
    g=G[G.game_id==gid]
    if g.empty: continue
    g=g.iloc[0]; wk=int(g.week); home=g.home
    for mk,alt in (('totals','alternate_totals'),('spreads','alternate_spreads')):
        m=q[q.market==mk]
        if mk=='spreads': m=m.assign(team=m.selection.map(NAMES)); m=m[m.team==home]  # home handicap rows
        if m.empty: continue
        line_counts=m.groupby('line').bookmaker.nunique()
        med=m.line.median(); mx=line_counts.max(); cand=line_counts[line_counts==mx].index
        Lm=min(cand,key=lambda x:abs(x-med))
        if mk=='totals':
            o=q[(q.market=='totals')&(q.line==Lm)]; piv=o.pivot_table(index='bookmaker',columns='selection',values='dec',aggfunc='last').dropna()
            if piv.empty: continue
            nvU=float(nv_mult(piv['Under'],piv['Over']).mean())
            mu,sd,act=g.sim_total,g.sim_total_sd,g.act_total
            evs={}
            for side in ('Under','Over'):
                pw,pp=pnorm_win(mu,sd,Lm,side); evs[side]=pw*piv[side].max()-(1-pw-pp)
            pw,pp=pnorm_win(mu,sd,Lm,'Under')
            rows.append(dict(kind='under',market='total',side='Under',week=wk,game_id=gid,rung=Lm,main_line=Lm,
                p_model=pw/(1-pp),p_nv=nvU,dec=piv['Under'].max(),push=int(act==Lm),win=np.nan if act==Lm else float(act<Lm),
                team_spread=np.nan,rung_off=0.0,ev_main=max(evs.values())))
            for _,r in q[q.market==alt].iterrows():
                if r.line==Lm: continue
                pw,pp=pnorm_win(mu,sd,r.line,r.selection)
                rows.append(dict(kind='alt',market='total',side=r.selection,week=wk,game_id=gid,rung=r.line,main_line=Lm,
                    p_model=pw/(1-pp),p_nv=np.nan,dec=r.dec,push=int(act==r.line),
                    win=np.nan if act==r.line else float((act<r.line) if r.selection=='Under' else (act>r.line)),
                    team_spread=np.nan,rung_off=(r.line-Lm)/Lm,ev_main=max(evs.values()),ev=pw*r.dec-(1-pw-pp)))
        else:
            # home handicap Lm; away handicap -Lm
            s=q[q.market=='spreads'].assign(team=lambda x:x.selection.map(NAMES))
            s=s[((s.team==home)&(s.line==Lm))|((s.team!=home)&(s.line==-Lm))]
            piv=s.pivot_table(index='bookmaker',columns='team',values='dec',aggfunc='last').dropna()
            if piv.shape[1]<2: continue
            away=[c for c in piv.columns if c!=home][0]
            nvH=float(nv_mult(piv[home],piv[away]).mean())
            mu,sd,act=g.sim_margin,g.sim_margin_sd,g.act_margin
            # home covers if margin > -Lm
            def cover(team,h):  # h = that team's handicap
                thr=-h  # team margin must exceed thr
                mu_t=mu if team==home else -mu
                if float(thr).is_integer():
                    pp=norm.cdf(thr+0.5,mu_t,sd)-norm.cdf(thr-0.5,mu_t,sd); pw=1-norm.cdf(thr+0.5,mu_t,sd)
                else: pp=0.0; pw=1-norm.cdf(thr,mu_t,sd)
                return pw,pp
            evs={}
            for t,h in ((home,Lm),(away,-Lm)):
                pw,pp=cover(t,h); evs[t]=pw*piv[t].max()-(1-pw-pp)
            for t,h,nv in ((home,Lm,nvH),(away,-Lm,1-nvH)):
                pw,pp=cover(t,h); am=act if t==home else -act
                rows.append(dict(kind='spread',market='spread',side=t,week=wk,game_id=gid,rung=h,main_line=h,
                    p_model=pw/(1-pp),p_nv=nv,dec=piv[t].max(),push=int(am==-h),win=np.nan if am==-h else float(am>-h),
                    team_spread=h,rung_off=0.0,ev_main=max(evs.values())))
            for _,r in q[q.market==alt].iterrows():
                t=NAMES.get(r.selection); h=r.line
                if (t==home and h==Lm) or (t!=home and h==-Lm): continue
                pw,pp=cover(t,h); am=act if t==home else -act
                rows.append(dict(kind='alt',market='spread',side=t,week=wk,game_id=gid,rung=h,main_line=Lm if t==home else -Lm,
                    p_model=pw/(1-pp),p_nv=np.nan,dec=r.dec,push=int(am==-h),win=np.nan if am==-h else float(am>-h),
                    team_spread=h,rung_off=(h-(Lm if t==home else -Lm))/7.0,ev_main=max(evs.values()),ev=pw*r.dec-(1-pw-pp)))
GC=pd.DataFrame(rows)
GC['edge']=np.where(GC.kind=='alt',GC.p_model-1/GC.dec,GC.p_model-GC.p_nv)
if 'ev' in GC: GC['ev_better']=(GC.ev>GC.ev_main).astype(int)
for c in ['is_rb','carry_share','gate_rb','rec_ungated','skew']: GC[c]={'gate_rb':True}.get(c,np.nan)
GC['rec_ungated']=0; GC['is_rb']=0
C=pd.concat([U,A,GC],ignore_index=True,sort=False)
C['be']=1/C.dec
C=C[['kind','market','side','week','game_id','player','gsis','position','rung','main_line','p_model','p_nv','dec','be','edge','ev','ev_main','ev_better',
     'rung_off','skew','carry_share','is_rb','n_prior','n60','gate_rb','rec_ungated','team_spread','push','win']]
C.to_csv(OUT+'/candidates.csv',index=False)
print(C.groupby(['kind','market','week']).size().unstack().to_string())
