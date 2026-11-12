# SCRATCH COPY for confidence_check_2026-11-03 (originals untouched). Patches: CC_OPP oppadj strength
"""sim_v6 — calibrated successor to runs/2026-11-01_shared_src/sim_v5.py (BUG-2026-11-01-BIAS fix).
v5 is untouched. Simulation core (volume, catch rate, yards resampling, opponent/league regression, GR beta-share x
lognormal pace x script slope) is identical to v5; differences:
  * Engine(cutoff=...) only sees pbp before a date, so backtests are leak-free.
  * the flat bias haircut (vol .92 / catch .97 / yds .95) is gone. Every model (mc, bias, gr) gets per-market
    multipliers fitted from real out-of-sample residuals (actual / model median, wk4-7 player-games of today's leg
    players, actuals = nflverse pbp aggregates = nflverse weekly player stats definition), shrunk toward 1.0
    (M = 1 + n/(n+K)*(raw-1), K=SHRINK_K) and forced to 1.0 when n < MIN_N.
  * 'bias' model = MC volume structure + its own fitted multipliers from MC's raw residuals with a heavier
    shrink (K_BIAS) so it stays a distinct, more conservative-to-the-mean correction.
  * GR lean (receiving ~10% low, rush ~10% high) is corrected by the same fitted per-market multipliers.
Calibration file: tools/sim_v6_calib.json (written by `python3 sim_v6.py fit`).
Usage: python3 sim_v6.py run <legs.json> <out.json>  |  python3 sim_v6.py fit  |  python3 sim_v6.py report"""
import warnings; warnings.filterwarnings('ignore',category=RuntimeWarning)
import pandas as pd, numpy as np, json, hashlib, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.environ.get('SIMV6_SRC', os.path.join(HERE,'..','runs','2026-11-01_shared_src'))+'/'
CALIB_F=os.path.join(HERE,'__no_calib__.json')
BOOST_F=os.path.join(HERE,'rb_script_boost.json')   # BUG-2026-11-01-RBSCRIPT fitted carry boosts
N=100_000; SEED=20261101; SD_MARGIN=13.5; SHRINK_K=30; K_BIAS=30; MIN_N=20
MODES=('mc','bias','gr'); NV={'LAR':'LA','WSH':'WAS'}
_P=pd.read_parquet(SRC+'play_by_play_2026.parquet'); _P=_P[(_P.season_type=='REG')&(_P.two_point_attempt!=1)]
_PL=pd.read_parquet(SRC+'players.parquet')
def load_calib():
    return json.load(open(CALIB_F))['multipliers'] if os.path.exists(CALIB_F) else None
def nb(rng,mean,var,n):
    var=max(var if var==var else mean*1.5,mean*1.05); pr=mean/var; k=mean*pr/(1-pr); return rng.negative_binomial(k,pr,n)
def scale_count(rng,C,m):
    if m<1: return rng.binomial(C,m)
    return C+rng.binomial(C,min(m-1,1.0))
class Engine:
    def __init__(self,cutoff=None,calib='default',n=N,seed=SEED):
        p=_P if cutoff is None else _P[_P.game_date<cutoff]
        self.p=p; self.n=n; self.seed=seed; self.calib=load_calib() if calib=='default' else calib
        pl=_PL; off=p[p.play_type.isin(['pass','run'])|(p.sack==1)]
        tg=off.groupby(['game_id','posteam']).agg(pa=('pass_attempt','sum'),ra=('rush_attempt','sum'),date=('game_date','first')).reset_index()
        fin=p.groupby('game_id').agg(h=('home_team','first'),hs=('home_score','max'),as_=('away_score','max')).reset_index()
        tg=tg.merge(fin,on='game_id'); tg['margin']=np.where(tg.posteam==tg.h,tg.hs-tg.as_,tg.as_-tg.hs); self.tg=tg
        self.bP=np.polyfit(tg.margin,np.log(tg.pa),1)[0]; self.bR=np.polyfit(tg.margin,np.log(tg.ra),1)[0]
        self.pos=pl.set_index('gsis_id').position_group.to_dict()
        self.pp=p[(p.pass_attempt==1)&(p.sack!=1)].assign(pg=lambda x:x.receiver_player_id.map(self.pos))
        self.ru=p[(p.rush_attempt==1)].assign(pg=lambda x:x.rusher_player_id.map(self.pos))
    def oppadj(self,opp,pg,kind,shrink=float(os.environ['CC_OPP'])):
        # NOSHRINK (rules/rulebook.py, Rico 2026-11-02 21:13 ET): opponent adjustment at full strength (was shrink=0.5).
        pp=self.pp; d=pp[pp.pg==pg] if pg else pp; o=d[d.defteam==opp]
        if len(d)==0 or len(o)==0: return 1.0, 1.0      # no sample -> neutral (fixes divide-by-zero warning)
        f=(lambda x:x.receiving_yards.fillna(0).sum()/len(x)) if kind=='ypt' else (lambda x:x.complete_pass.mean())
        a,b=f(o),f(d)
        if not b or b!=b or a!=a: return 1.0, 1.0
        r=a/b; return float(1+shrink*(r-1)), float(r)
    def pid(self,name,team):
        c=_PL[_PL.display_name==name]
        if len(c)>1: c=c[c.latest_team==team] if (c.latest_team==team).any() else c
        return c.gsis_id.iloc[0]
    def player(self,name,team,qb=False,gsis=None):
        p=self.p; g=gsis or self.pid(name,team); t=self.tg[self.tg.posteam==team].sort_values('date')
        r=p[(p.passer_player_id==g)&(p.pass_attempt==1)&(p.sack!=1)] if qb else p[(p.receiver_player_id==g)&(p.pass_attempt==1)&(p.sack!=1)]
        u=p[(p.rusher_player_id==g)&(p.rush_attempt==1)]; rows=[]
        for gid in t.game_id:
            rr=r[r.game_id==gid]; uu=u[u.game_id==gid]; tt=t[t.game_id==gid].iloc[0]
            yd=rr.passing_yards if qb else rr.receiving_yards
            rows.append(dict(game_id=gid,date=tt.date,tgt=len(rr),rec=int(rr.complete_pass.sum()),ry=float(yd.fillna(0).sum()),car=len(uu),rush=float(uu.rushing_yards.fillna(0).sum()),pa=tt.pa,ra=tt.ra))
        d=pd.DataFrame(rows); act=d[(d.tgt+d.car)>0]
        yc=(r[r.complete_pass==1].passing_yards if qb else r[r.complete_pass==1].receiving_yards).dropna().values
        return d,act,yc,u.rushing_yards.dropna().values,g
    def mult(self,mode,mkt):
        if not self.calib: return 1.0
        return float(self.calib.get(mode,{}).get(mkt,{}).get('M',1.0))
    def sim(self,leg,raw=False):
        N=self.n; tg=self.tg; pp=self.pp; ru=self.ru
        name,mkt,spread=leg['player'],leg['market'],float(leg['spread']); team=NV.get(leg['team'],leg['team']); opp=NV.get(leg['opp'],leg['opp'])
        qb=mkt in('passyds','comp'); d,a,yc,ypc_rush,g=self.player(name,team,qb,leg.get('gsis')); PG=self.pos.get(g,'WR')
        if len(a)==0: raise ValueError('no active games before cutoff')
        l3=a.tail(3); w=lambda col:0.6*a[col].mean()+0.4*l3[col].mean()
        cr=(a.rec.sum()+1)/(a.tgt.sum()+2); pgk=None if qb else PG
        A_ypt,r_ypt=self.oppadj(opp,pgk,'ypt'); A_cr,r_cr=self.oppadj(opp,pgk,'cr')
        cr=min(cr*A_cr,0.95); A_rec_y=A_ypt/A_cr; info={}
        if len(yc):
            lg=(pp[pp.complete_pass==1].receiving_yards.mean() if qb else pp[(pp.pg==PG)&(pp.complete_pass==1)].receiving_yards.mean())
            K=100 if qb else 30; wv=len(yc)/(len(yc)+K); A_rec_y*=(wv*yc.mean()+(1-wv)*lg)/yc.mean()
        A_ypc=1.0
        if len(ypc_rush):
            lgA=ru.rushing_yards.mean(); pm=ypc_rush.mean(); wv=len(ypc_rush)/(len(ypc_rush)+100); oppY=ru[ru.defteam==opp].rushing_yards.mean()
            A_ypc=((wv*pm+(1-wv)*lgA)/pm)*(oppY/lgA) if pm and lgA and oppY==oppY else 1.0   # guard divide-by-zero
        out={}
        for mode in MODES:
            rng=np.random.default_rng(self.seed+int(hashlib.md5(f'{name}|{mkt}|{mode}'.encode()).hexdigest()[:6],16))
            M=1.0 if raw else self.mult(mode,mkt)
            def vol(col,teamcol,b):
                mean=w(col)
                if mode!='gr': return nb(rng,mean,a[col].var(ddof=1),N)
                share=(a[col]/a[teamcol]).clip(0,0.999); m_s,v_s=share.mean(),max(share.var(ddof=1) if len(share)>1 else 1e-3,1e-4)
                if len(l3): m_s=min(0.6*m_s+0.4*(l3[col]/l3[teamcol]).clip(0,0.999).mean(),0.995)
                kk=max(m_s*(1-m_s)/v_s-1,2); sh=rng.beta(m_s*kk,(1-m_s)*kk,N)
                tm=tg[tg.posteam==team][teamcol]; sig=np.std(np.log(tm),ddof=1)
                Mg=rng.normal(-spread,SD_MARGIN,N); pace=rng.lognormal(0,sig,N)
                TV=tm.mean()*pace*np.exp(b*(Mg-(-spread)))*np.exp(b*(-spread)); TV=TV*(mean/(m_s*TV.mean()))
                return rng.binomial(np.maximum(np.round(TV).astype(int),0),np.clip(sh,0,1))
            x=0
            if mkt in ('rec','recyds','rushrec','passyds','comp'):
                T=vol('tgt','pa',self.bP); C=rng.binomial(T,np.clip(cr,0,1))
                if mkt in('rec','comp'): x=C
                else:
                    tot=np.zeros(N)
                    if len(yc):
                        for i in range(int(C.max())): tot+=np.where(C>i,rng.choice(yc,N),0)
                    x=tot*A_rec_y
            if mkt in ('rushyds','rushrec'):
                Cr=vol('car','ra',self.bR); tot=np.zeros(N)
                cb=float(leg.get('carry_boost',1.0))
                if cb!=1.0: Cr=scale_count(rng,Cr,cb)   # game-script RB boost / promotion / split share (all three models)
                if len(ypc_rush):
                    for i in range(int(Cr.max())): tot+=np.where(Cr>i,rng.choice(ypc_rush,N),0)
                x=x+tot*A_ypc*float(leg.get('ypc_boost',1.0))   # BUG-2026-11-01-RBMISS F (all three models)
            if isinstance(x,int): x=np.zeros(N)
            x=np.asarray(x)
            x=scale_count(rng,x.astype(int),M).astype(float) if mkt in('rec','comp') else x.astype(float)*M
            out[mode]=dict(mean=float(x.mean()),median=float(np.median(x)),cmedian=float(np.median(x+rng.uniform(-.5,.5,N))) if mkt in('rec','comp') else float(np.median(x)),
                           p10=float(np.percentile(x,10)),p90=float(np.percentile(x,90)),M=M,rungs={str(k):float((x>=k).mean()) for k in leg.get('rungs',[])})
        info.update(n_games=len(a),w_tgt=float(w('tgt')),w_car=float(w('car')),cr=float(cr),A_ypc=float(A_ypc),A_rec_y=float(A_rec_y),pos=PG)
        return out,info
# ---------- BUG-2026-11-01-RBSCRIPT: game-script RB rule ----------
FAV_SPREAD, FAV_YPC = -7.0, 4.4
RUSH_ORDER = {'rushyds':0,'rushrec':1}
def rb_script_trigger(fav_spread, opp_ypc, wx_flag):
    """favored by 7+ AND opp allows 4.4+ RB YPC season-to-date, OR weather-flagged (Phase 11)."""
    return bool(wx_flag) or (fav_spread is not None and opp_ypc is not None and float(fav_spread)<=FAV_SPREAD and float(opp_ypc)>=FAV_YPC)
def rb_script_boosts(fav_spread, opp_ypc, wx_flag):
    g=json.load(open(BOOST_F))['groups']; fav=bool(fav_spread is not None and opp_ypc is not None and float(fav_spread)<=FAV_SPREAD and float(opp_ypc)>=FAV_YPC); wx=bool(wx_flag)
    lead=rb2=1.0
    if fav: lead*=g['lead_fav']['boost']; rb2*=g['rb2_fav']['boost']
    if wx: lead*=g['lead_wx']['boost']; rb2*=g['rb2_wx']['boost']
    return dict(triggered=fav or wx, components=dict(fav=fav,wx=wx), lead=lead, rb2=rb2, source=os.path.relpath(BOOST_F,os.path.join(HERE,'..')))
def model_order(legs, wx_flag):
    """weather-flagged games: rushing overs are modeled before passing/receiving overs (stable)."""
    if not wx_flag: return legs
    return sorted(legs, key=lambda l: RUSH_ORDER.get(l['market'], 2))
def opp_rb_ypc(E, opp):
    r=E.ru[(E.ru.defteam==NV.get(opp,opp))&(E.ru.pg=='RB')]
    if 'qb_kneel' in r: r=r[r.qb_kneel!=1]
    return float(r.rushing_yards.fillna(0).sum()/len(r))
def price_game_script(E, fx):
    """fx: {team,opp,fav_spread,opp_ypc,wx_flag,lead:{player,market,line,no_vig},rb2:{player,market},other_legs:[...]}.
    Re-prices the lead back on the boosted script and models the RB2's rushing too (all three models)."""
    b=rb_script_boosts(fx['fav_spread'],fx['opp_ypc'],fx['wx_flag']); out=dict(b)
    legs=[dict(fx['lead'],role='lead'),dict(fx['rb2'],role='rb2')]+[dict(x,role='other') for x in fx.get('other_legs',[])]
    order=model_order(legs,fx['wx_flag']); out['model_order']=[l['market'] for l in order]
    for L in order:
        if L['role']=='other': continue
        cb=b[L['role']] if b['triggered'] else 1.0; line=L.get('line')
        leg=dict(player=L['player'],team=fx['team'],opp=fx['opp'],market=L['market'],spread=fx['fav_spread'],rungs=[line] if line is not None else [],carry_boost=cb)
        o,info=E.sim(leg); r=dict(player=L['player'],market=L['market'],boost=cb,script='boosted' if cb!=1.0 else 'base',
            median={m:o[m]['median'] for m in MODES},mean={m:o[m]['mean'] for m in MODES},w_car=info['w_car']*cb,A_ypc=info['A_ypc'])
        if line is not None:
            r['p']={m:o[m]['rungs'][str(line)] for m in MODES}; r['line']=line
            if L.get('no_vig') is not None:
                av=sum(r['p'].values())/3; r['edge']=av-L['no_vig']
        out[L['role']]=r
    return out
# ---------- BUG-2026-11-01-RBMISS (A promotion, E split re-price, F soft run D) ----------
MISS_F=os.path.join(HERE,'rb_miss_fit.json'); SOFT_YPC=4.4
def _miss(): 
    with open(MISS_F) as f: return json.load(f)
def soft_run_d_boost(opp_ypc):
    """F: opponent allows >=4.4 RB YPC season-to-date -> YPC boost fitted from backtest residuals (independent of spread).
    The fit is a residual on top of the model's existing opp-YPC multiplier; a fit <1 means no extra boost (applied=1.0)."""
    f=_miss()['soft_run_d']; soft=opp_ypc is not None and float(opp_ypc)>=SOFT_YPC
    return dict(soft=soft,opp_ypc=opp_ypc,fitted=f['boost'],applied=max(1.0,f['boost']) if soft else 1.0,source=os.path.relpath(MISS_F,os.path.join(HERE,'..')))
def _rb_games(E,team):
    r=E.ru[(E.ru.posteam==NV.get(team,team))&(E.ru.pg=='RB')]
    c=r.groupby(['game_id','rusher_player_id']).size().unstack(fill_value=0)
    d=r.drop_duplicates('game_id').set_index('game_id').game_date.sort_values(); return c.loc[d.index]
def _price(E,leg,line,no_vig):
    o,info=E.sim(leg); r=dict(median={m:o[m]['median'] for m in MODES},mean={m:o[m]['mean'] for m in MODES})
    if line is not None:
        r['p']={m:o[m]['rungs'][str(line)] for m in MODES}
        if no_vig is not None: av=sum(r['p'].values())/3; r['edge']=av-no_vig
    return r,info
def promote_rb(E,fx):
    """A: RB1 OUT/IR/inactive -> build and price RB2 automatically. New share = own share + tau x injured back's share,
    shares from games both backs were active; tau fitted from pbp (rb_miss_fit.json). fx: team,opp,spread,injured,rb2,market,line,no_vig[,opp_ypc]."""
    tau=float(fx.get('tau_override') or _miss()['promotion']['tau']); c=_rb_games(E,fx['team']); i1=E.pid(fx['injured'],fx['team']); i2=E.pid(fx['rb2'],fx['team'])
    both=c[(c.get(i1,0)>0)&(c.get(i2,0)>0)] if i1 in c and i2 in c else c.iloc[0:0]
    tot=both.sum(axis=1).sum() if len(both) else 0
    s1=float(both[i1].sum()/tot) if tot else 0.0; s2=float(both[i2].sum()/tot) if tot else float(c[i2].sum()/c.values.sum()) if i2 in c else 0.0
    new=s2+tau*s1
    # carry target = new share x team RB carries (games both active); boost is vs the RB2's own weighted carries (w_car),
    # so games the injured back already missed are not double-counted.
    _,a,_,_,_=E.player(fx['rb2'],NV.get(fx['team'],fx['team'])); wc=0.6*a.car.mean()+0.4*a.tail(3).car.mean()
    tm=float(both.sum(axis=1).mean()) if len(both) else float(c.sum(axis=1).mean()); target=new*tm; cb=max(target/wc,1.0) if wc>0 else 1.0
    yb=soft_run_d_boost(fx.get('opp_ypc'))
    leg=dict(player=fx['rb2'],team=fx['team'],opp=fx['opp'],market=fx.get('market','rushyds'),spread=fx['spread'],rungs=[fx['line']] if fx.get('line') is not None else [],carry_boost=cb,ypc_boost=yb['applied'])
    r,info=_price(E,leg,fx.get('line'),fx.get('no_vig'))
    r.update(rb2=fx['rb2'],injured=fx['injured'],tau=tau,team_rb_carries=tm,target_carries=target,share_own=s2,share_injured=s1,share_new=new,carry_boost=cb,w_car=info['w_car'],boosted_carries=info['w_car']*cb,soft_run_d=yb,games_both=len(both),line=fx.get('line'))
    return r
def split_reprice(E,fx):
    """E: backfield-split flag -> price both backs over a carry-share range from the last 4 team games
    (lo=min, hi=max, mid=mean over each back's last 4 ACTIVE games of his share of team RB carries; base = 0.6 season + 0.4 last-3 active share).
    nflverse Week-8 snap counts are not published, so the range is carries-based. fx: team,opp,spread,backs:[{player,line,no_vig}]."""
    c=_rb_games(E,fx['team']); out=dict(team=fx['team'],backs=[])
    sh=c.div(c.sum(axis=1),axis=0)
    for b in fx['backs']:
        g=E.pid(b['player'],fx['team']); s=sh[g] if g in sh else pd.Series([0.0])
        act=s[c[g]>0] if g in c else s; base=0.6*act.mean()+0.4*act.tail(3).mean()
        l4=act.tail(4); lo,hi,mid=float(l4.min()),float(l4.max()),float(l4.mean())
        if hi-lo<0.05: lo,hi=max(mid-0.05,0.01),min(mid+0.05,0.99)
        yb=soft_run_d_boost(fx.get('opp_ypc')); rec=dict(player=b['player'],share_range=[lo,hi],share_mid=mid,share_base=float(base),p={},median={},edge={})
        for k,v in (('lo',lo),('mid',mid),('hi',hi)):
            leg=dict(player=b['player'],team=fx['team'],opp=fx['opp'],market=b.get('market','rushyds'),spread=fx['spread'],rungs=[b['line']],carry_boost=v/base if base>0 else 1.0,ypc_boost=yb['applied'])
            r,_=_price(E,leg,b['line'],b.get('no_vig')); rec['p'][k]=r['p']; rec['median'][k]=r['median']; rec['edge'][k]=r.get('edge')
        out['backs'].append(rec)
    return out
# ---------- backtest / calibration ----------
def actual(p,gid,g,mkt):
    q=p[p.game_id==gid]
    if mkt=='passyds': return float(q[(q.passer_player_id==g)&(q.pass_attempt==1)&(q.sack!=1)].passing_yards.fillna(0).sum())
    rr=q[(q.receiver_player_id==g)&(q.pass_attempt==1)&(q.sack!=1)]; uu=q[(q.rusher_player_id==g)&(q.rush_attempt==1)]
    if mkt=='rec': return float(rr.complete_pass.sum())
    if mkt=='recyds': return float(rr.receiving_yards.fillna(0).sum())
    if mkt=='rushyds': return float(uu.rushing_yards.fillna(0).sum())
    if mkt=='rushrec': return float(rr.receiving_yards.fillna(0).sum()+uu.rushing_yards.fillna(0).sum())
def legs_today():
    D=json.load(open(SRC+'legs_final.json'))['legs']
    return [L for L in D if L['market'] in ('passyds','rec','recyds','rushyds','rushrec')]
def universe(E):
    """Leak-free backtest universe: every player whose PRE-cutoff usage would get him a line (same thresholds for
    every week, chosen before seeing outcomes): QB avg >=20 att -> passyds; avg >=4 targets -> rec, recyds;
    avg >=8 carries -> rushyds (+rushrec if RB). Needs >=2 prior active games."""
    p=E.p; out=[]
    qa=p[(p.pass_attempt==1)&(p.sack!=1)].groupby(['passer_player_id','game_id']).size().groupby(level=0).agg(['mean','size'])
    out+=[(g,'passyds') for g,r in qa.iterrows() if r['mean']>=20 and r['size']>=2]
    ta=p[(p.pass_attempt==1)&(p.sack!=1)].groupby(['receiver_player_id','game_id']).size().groupby(level=0).agg(['mean','size'])
    out+=[(g,m) for g,r in ta.iterrows() if r['mean']>=4 and r['size']>=2 for m in ('rec','recyds')]
    ca=p[p.rush_attempt==1].groupby(['rusher_player_id','game_id']).size().groupby(level=0).agg(['mean','size'])
    out+=[(g,m) for g,r in ca.iterrows() if r['mean']>=8 and r['size']>=2 for m in (('rushyds','rushrec') if E.pos.get(g)=='RB' else ('rushyds',))]
    return out
def backtest_rows(weeks,n,seed=SEED):
    """Raw (uncalibrated) model medians vs actual week-W stat for the leak-free universe, using only pbp before week W."""
    P=_P; rows=[]
    for W in weeks:
        cut=P[P.week==W].game_date.min(); E=Engine(cutoff=cut,calib=None,n=n,seed=seed); PW=P[P.week==W]
        for g,mkt in universe(E):
            q=PW[(PW.passer_player_id==g)|(PW.receiver_player_id==g)|(PW.rusher_player_id==g)]
            if q.empty: continue   # inactive/DNP/bye: excluded (lines are only settled for active players)
            gid=q.game_id.iloc[0]; Q=PW[PW.game_id==gid]
            t=q.posteam.mode().iloc[0]; opp=Q.home_team.iloc[0] if Q.away_team.iloc[0]==t else Q.away_team.iloc[0]
            if not (E.tg.posteam==t).any(): continue
            try: o,_=E.sim(dict(player=g,gsis=g,team=t,opp=opp,market=mkt,spread=0.0),raw=True)
            except Exception: continue
            if not all(np.isfinite(o[m]['cmedian']) for m in MODES): continue   # degenerate history (0 YPC / no opp data)
            act=actual(P,gid,g,mkt)
            if mkt=='rec': act+=np.random.default_rng(int(hashlib.md5(f'{g}|{W}'.encode()).hexdigest()[:8],16)).uniform(-.5,.5)
            rows.append(dict(week=W,gsis=g,market=mkt,actual=act,**{f'pred_{m}':o[m]['cmedian'] for m in MODES}))
    return pd.DataFrame(rows)
def fit(df):
    """Per (mode, market): raw=median(actual/pred); bias model fitted on MC preds with heavier shrink."""
    res={}
    for mode in MODES:
        res[mode]={}; col='pred_mc' if mode=='bias' else f'pred_{mode}'; K=K_BIAS if mode=='bias' else SHRINK_K
        for mk,g in df.groupby('market'):
            g=g[g[col]>0.5]; n=len(g)
            raw=float(np.median(g.actual/g[col])) if n else 1.0
            M=1.0 if n<MIN_N else 1+(n/(n+K))*(raw-1)
            res[mode][mk]=dict(M=round(M,4),raw=round(raw,4),n=n,shrink_K=K,guard=n<MIN_N)
    return res
def score(df,mult):
    out={}
    for mk,g in df.groupby('market'):
        out[mk]={}
        for mode in MODES:
            col='pred_mc' if mode=='bias' else f'pred_{mode}'; gg=g[g[col]>0.5]
            pred=gg[col]*mult[mode][mk]['M']
            out[mk][mode]=dict(n=len(gg),median_signed_err_pct=float(100*np.median((pred-gg.actual)/pred)) if len(gg) else 0.0)
    return out
def cross_validate(weeks=(4,5,6,7),n=4000,df=None):
    """Leave-one-week-out: fit on the other weeks, score the held-out week; errors pooled across held-out weeks."""
    df=backtest_rows(weeks,n) if df is None else df; parts=[]
    for W in weeks:
        m=fit(df[df.week!=W]); h=df[df.week==W].copy()
        for mode in MODES:
            col='pred_mc' if mode=='bias' else f'pred_{mode}'
            h[f'cal_{mode}']=h.apply(lambda r:r[col]*m[mode][r.market]['M'] if r.market in m[mode] else r[col],axis=1)
        parts.append(h)
    H=pd.concat(parts); out={}
    for mk,g in H.groupby('market'):
        out[mk]={}
        for mode in MODES:
            gg=g[g[f'cal_{mode}']>0.5]; pr=gg[f'cal_{mode}']
            out[mk][mode]=dict(n=len(gg),median_signed_err_pct=float(100*np.median((pr-gg.actual)/pr)) if len(gg) else 0.0)
    return out
def below_line_share(n=4000,calib='default'):
    E=Engine(calib=calib,n=n); cnt={m:0 for m in MODES}; tot=0; per=[]
    for L in legs_today():
        try: o,_=E.sim(dict(player=L['player'],team=L['team'],opp=L['opp'],market=L['market'],spread=L['spread']))
        except Exception: continue
        tot+=1; line=L['fd']['point']; r=dict(player=L['player'],market=L['market'],line=line)
        for m in MODES: cnt[m]+=o[m]['median']<line; r[m]=o[m]['median']
        per.append(r)
    return dict(n_legs=tot,share={m:cnt[m]/tot for m in MODES},legs=per)
if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'run'
    if cmd=='fit':
        n=int(os.environ.get('SIMV6_FIT_N','4000')); df=backtest_rows((4,5,6,7),n); df.to_csv(os.path.join(HERE,'sim_v6_backtest.csv'),index=False)
        json.dump(dict(fitted_on='wk4-7 2026, leak-free usage-threshold universe, model fed only pbp before each week (pbp thru 2026-10-29)',n_sims=n,min_n=MIN_N,shrink_k=SHRINK_K,k_bias=K_BIAS,
                       multipliers=fit(df)),open(CALIB_F,'w'),indent=1); print(json.dumps(load_calib(),indent=1))
    elif cmd=='run':
        legs=json.load(open(sys.argv[2])); outp=sys.argv[3]; E=Engine(); R={}
        for L in legs:
            k=f"{L['player']}|{L['market']}|{L['spread']}|{','.join(map(str,L['rungs']))}"
            try: o,i=E.sim(L); R[k]=dict(leg=L,sims=o,info=i)
            except Exception as ex: R[k]=dict(leg=L,error=repr(ex))
        R['_meta']=dict(N=N,seed=SEED,calib=load_calib(),code_sha=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
        json.dump(R,open(outp,'w'),default=float)
