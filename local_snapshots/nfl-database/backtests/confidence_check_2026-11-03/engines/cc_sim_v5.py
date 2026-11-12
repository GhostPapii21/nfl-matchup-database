# SCRATCH COPY for confidence_check_2026-11-03 (originals untouched). Patches: CC_OPP oppadj strength, CC_CUTOFF leak-free cutoff, gsis lookup
"""Nov 1 2026 game-day sim engine v5 (derived from week8/.../bg_sim_v4.py).
Changes vs v4: SRC = shared_src fresh pbp (07:09 ET); QB markets passyds/comp (attempts NB volume,
completions binomial, yards/completion resampled); per-catch / per-completion yards regressed toward
league (k=30 catches receivers, k=100 completions QB) before the 50%-shrunk opponent factor; YPC regressed
k=100 then full opponent YPC factor (v4 BG_YPCREG=100 behaviour). Seed 20261101, N=100,000 per model.
Models: mc (negative-binomial volume), bias (vol .92, catch .97, yds .95), gr (beta share x lognormal team
pace x script slope on margin~N(-spread,13.5))."""
import pandas as pd, numpy as np, json, hashlib, os, sys
SRC=os.environ['CC_SRC']+'/'; N=100_000; SEED=20261101; SD_MARGIN=13.5
p=pd.read_parquet(SRC+'play_by_play_2026.parquet'); p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]; p=p[p.game_date<os.environ['CC_CUTOFF']]
pl=pd.read_parquet(SRC+'players.parquet')
off=p[p.play_type.isin(['pass','run'])|(p.sack==1)]
tg=off.groupby(['game_id','posteam']).agg(pa=('pass_attempt','sum'),ra=('rush_attempt','sum'),date=('game_date','first')).reset_index()
fin=p.groupby('game_id').agg(h=('home_team','first'),hs=('home_score','max'),as_=('away_score','max')).reset_index()
tg=tg.merge(fin,on='game_id'); tg['margin']=np.where(tg.posteam==tg.h,tg.hs-tg.as_,tg.as_-tg.hs)
bP=np.polyfit(tg.margin,np.log(tg.pa),1)[0]; bR=np.polyfit(tg.margin,np.log(tg.ra),1)[0]
pos=pl.set_index('gsis_id').position_group.to_dict()
pp=p[(p.pass_attempt==1)&(p.sack!=1)].assign(pg=lambda x:x.receiver_player_id.map(pos))
ru=p[(p.rush_attempt==1)].assign(pg=lambda x:x.rusher_player_id.map(pos))
NV={'LAR':'LA','WSH':'WAS'}
def oppadj(opp,pg,kind,shrink=float(os.environ['CC_OPP'])):
    if kind=='ypt': d=pp[pp.pg==pg] if pg else pp; f=lambda x:x.receiving_yards.fillna(0).sum()/len(x)
    elif kind=='cr': d=pp[pp.pg==pg] if pg else pp; f=lambda x:x.complete_pass.mean()
    r=f(d[d.defteam==opp])/f(d); return float(1+shrink*(r-1)), float(r)
def pid(name,team):
    c=pl[pl.display_name==name]
    if len(c)>1: c=c[c.latest_team==team] if (c.latest_team==team).any() else c
    return c.gsis_id.iloc[0]
def player(name,team,qb=False,gsis=None):
    g=gsis or pid(name,team); t=tg[tg.posteam==team].sort_values('date')
    if qb: r=p[(p.passer_player_id==g)&(p.pass_attempt==1)&(p.sack!=1)]
    else: r=p[(p.receiver_player_id==g)&(p.pass_attempt==1)&(p.sack!=1)]
    u=p[(p.rusher_player_id==g)&(p.rush_attempt==1)]
    rows=[]
    for gid in t.game_id:
        rr=r[r.game_id==gid]; uu=u[u.game_id==gid]; tt=t[t.game_id==gid].iloc[0]
        yd=rr.passing_yards if qb else rr.receiving_yards
        rows.append(dict(game_id=gid,date=tt.date,tgt=len(rr),rec=int(rr.complete_pass.sum()),ry=float(yd.fillna(0).sum()),car=len(uu),rush=float(uu.rushing_yards.fillna(0).sum()),pa=tt.pa,ra=tt.ra))
    d=pd.DataFrame(rows); act=d[(d.tgt+d.car)>0]
    yc=(r[r.complete_pass==1].passing_yards if qb else r[r.complete_pass==1].receiving_yards).dropna().values
    return d,act,yc,u.rushing_yards.dropna().values,g
def nb(rng,mean,var,n):
    var=max(var if var==var else mean*1.5,mean*1.05); pr=mean/var; k=mean*pr/(1-pr); return rng.negative_binomial(k,pr,n)
def sim(leg):
    name,mkt,spread=leg['player'],leg['market'],float(leg['spread']); team=NV.get(leg['team'],leg['team']); opp=NV.get(leg['opp'],leg['opp'])
    qb=mkt in('passyds','comp')
    d,a,yc,ypc_rush,g=player(name,team,qb,leg.get('gsis')); PG=pos.get(g,'WR')
    l3=a.tail(3); w=lambda col:0.6*a[col].mean()+0.4*l3[col].mean()
    cr=(a.rec.sum()+1)/(a.tgt.sum()+2)
    pgk=None if qb else PG
    A_ypt,r_ypt=oppadj(opp,pgk,'ypt'); A_cr,r_cr=oppadj(opp,pgk,'cr')
    cr=min(cr*A_cr,0.95); A_rec_y=A_ypt/A_cr
    info={}
    if len(yc):
        lg=(pp[pp.complete_pass==1].receiving_yards.mean() if qb else pp[(pp.pg==PG)&(pp.complete_pass==1)].receiving_yards.mean())
        K=100 if qb else 30; wv=len(yc)/(len(yc)+K); A_rec_y*=(wv*yc.mean()+(1-wv)*lg)/yc.mean()
        info['ycreg']=dict(player=float(yc.mean()),n=int(len(yc)),w=float(wv),league=float(lg))
    A_ypc=1.0
    if len(ypc_rush):
        lgA=ru.rushing_yards.mean(); pm=ypc_rush.mean(); wv=len(ypc_rush)/(len(ypc_rush)+100); oppY=ru[ru.defteam==opp].rushing_yards.mean()
        A_ypc=((wv*pm+(1-wv)*lgA)/pm)*(oppY/lgA); info['ypcreg']=dict(player=float(pm),n=int(len(ypc_rush)),w=float(wv),league=float(lgA),opp=float(oppY))
    out={}
    for mode in ['mc','bias','gr']:
        rng=np.random.default_rng(SEED+int(hashlib.md5(f'{name}|{mkt}|{mode}'.encode()).hexdigest()[:6],16))
        vf,cf,yf=(0.92,0.97,0.95) if mode=='bias' else (1,1,1)
        def vol(col,teamcol,b):
            mean=w(col)*vf
            if mode!='gr': return nb(rng,mean,a[col].var(ddof=1),N)
            share=(a[col]/a[teamcol]).clip(0,0.999); m_s,v_s=share.mean(),max(share.var(ddof=1) if len(share)>1 else 1e-3,1e-4)
            if len(l3): m_s=min(0.6*m_s+0.4*(l3[col]/l3[teamcol]).clip(0,0.999).mean(),0.995)
            kk=max(m_s*(1-m_s)/v_s-1,2); sh=rng.beta(m_s*kk,(1-m_s)*kk,N)
            tm=tg[tg.posteam==team][teamcol]; sig=np.std(np.log(tm),ddof=1)
            M=rng.normal(-spread,SD_MARGIN,N); pace=rng.lognormal(0,sig,N)
            TV=tm.mean()*pace*np.exp(b*(M-(-spread)))*np.exp(b*(-spread)); TV=TV*(mean/(m_s*TV.mean()))
            return rng.binomial(np.maximum(np.round(TV).astype(int),0),np.clip(sh,0,1))
        x=0
        if mkt in ('rec','recyds','rushrec','passyds','comp'):
            T=vol('tgt','pa',bP); C=rng.binomial(T,np.clip(cr*cf,0,1))
            if mkt in('rec','comp'): x=C
            else:
                tot=np.zeros(N)
                for i in range(int(C.max())): tot+=np.where(C>i,rng.choice(yc,N),0)
                x=tot*yf*A_rec_y
        if mkt in ('rushyds','rushrec'):
            Cr=vol('car','ra',bR); tot=np.zeros(N)
            for i in range(int(Cr.max())): tot+=np.where(Cr>i,rng.choice(ypc_rush,N),0)
            x=x+tot*yf*A_ypc
        x=np.asarray(x,dtype=float)
        out[mode]=dict(mean=float(x.mean()),median=float(np.median(x)),p10=float(np.percentile(x,10)),p90=float(np.percentile(x,90)),
                       rungs={str(k):float((x>=k).mean()) for k in leg['rungs']})
    info.update(n_games=len(a),log=a[['date','tgt','rec','ry','car','rush','pa','ra']].assign(date=a.date.astype(str)).to_dict('records'),
        w_tgt=float(w('tgt')),w_car=float(w('car')),cr=float(cr),A_ypt=A_ypt,A_cr=A_cr,A_ypc=float(A_ypc),A_rec_y=float(A_rec_y),pos=PG,raw_opp_ypt=r_ypt,raw_opp_cr=r_cr)
    return out,info
if __name__=='__main__':
    legs=json.load(open(sys.argv[1])); outp=sys.argv[2]
    R=json.load(open(outp)) if os.path.exists(outp) else {}
    for L in legs:
        k=f"{L['player']}|{L['market']}|{L['spread']}|{','.join(map(str,L['rungs']))}"
        if k in R: continue
        try: o,i=sim(L); R[k]=dict(leg=L,sims=o,info=i)
        except Exception as ex: R[k]=dict(leg=L,error=repr(ex))
        print(k,'ok' if 'sims' in R[k] else R[k]['error'],flush=True)
        json.dump(R,open(outp,'w'),default=float)
    R['_meta']=dict(N=N,seed=SEED,bP=bP,bR=bR,sd_margin=SD_MARGIN,pbp_sha=hashlib.sha256(open(SRC+'play_by_play_2026.parquet','rb').read()).hexdigest(),code_sha=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
    json.dump(R,open(outp,'w'),default=float)
