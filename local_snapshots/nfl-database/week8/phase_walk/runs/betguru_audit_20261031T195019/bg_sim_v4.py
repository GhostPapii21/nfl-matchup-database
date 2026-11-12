# BetGuru requested sims (NOT outputs/nfl.py engine). 100k trials x 3 models per leg.
import pandas as pd, numpy as np, json, hashlib, sys
import os
SRC='../../src/'; N=int(os.environ.get('BG_N',100_000)); SEED=20261101; SHR=float(os.environ.get('BG_SHRINK',0)); OUT=os.environ.get('BG_OUT','bg_sims.json'); LEGS=os.environ.get('BG_LEGS','legs_in.json')
p=pd.read_parquet(SRC+'play_by_play_2026.parquet')
p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
pl=pd.read_parquet(SRC+'players.parquet')
# team-game volume
off=p[p.play_type.isin(['pass','run'])|(p.sack==1)]
tg=off.groupby(['game_id','posteam']).agg(pa=('pass_attempt','sum'),ra=('rush_attempt','sum'),date=('game_date','first')).reset_index()
fin=p.groupby('game_id').agg(h=('home_team','first'),a=('away_team','first'),hs=('home_score','max'),as_=('away_score','max')).reset_index()
tg=tg.merge(fin,on='game_id'); tg['margin']=np.where(tg.posteam==tg.h,tg.hs-tg.as_,tg.as_-tg.hs)
# script slope: log(team att) on margin (league, 2026 pbp)
bP=np.polyfit(tg.margin,np.log(tg.pa),1)[0]; bR=np.polyfit(tg.margin,np.log(tg.ra),1)[0]
SD_MARGIN=13.5
pos=pl.set_index('gsis_id').position_group.to_dict()
pp=p[(p.pass_attempt==1)&(p.sack!=1)].assign(pg=lambda x:x.receiver_player_id.map(pos))
ru=p[(p.rush_attempt==1)].assign(pg=lambda x:x.rusher_player_id.map(pos))
def oppadj(opp,pg,kind,shrink=0.5):
    # v3: opponent adjustment (2026 pbp, allowed to position group vs league), shrunk 50% toward 1.0
    if kind=='ypt': d=pp[pp.pg==pg]; f=lambda x:x.receiving_yards.fillna(0).sum()/len(x)
    elif kind=='cr': d=pp[pp.pg==pg]; f=lambda x:x.complete_pass.mean()
    else: d=ru[ru.pg=='RB']; f=lambda x:x.rushing_yards.fillna(0).mean()
    r=f(d[d.defteam==opp])/f(d); return float(1+shrink*(r-1)), float(r)  # assumption: commonly used NFL margin SD vs spread; not fit here
def pid(name,team):
    c=pl[(pl.display_name==name)]
    if len(c)>1: c=c[c.latest_team==team] if (c.latest_team==team).any() else c
    return c.gsis_id.iloc[0]
def player(name,team):
    g=pid(name,team); t=tg[tg.posteam==team].sort_values('date')
    r=p[(p.receiver_player_id==g)&(p.pass_attempt==1)&(p.sack!=1)]
    u=p[(p.rusher_player_id==g)&(p.rush_attempt==1)]
    games=t.game_id.tolist()
    rows=[]
    for gid in games:
        rr=r[r.game_id==gid]; uu=u[u.game_id==gid]; tt=t[t.game_id==gid].iloc[0]
        rows.append(dict(game_id=gid,date=tt.date,tgt=len(rr),rec=int(rr.complete_pass.sum()),ry=float(rr.receiving_yards.fillna(0).sum()),
          car=len(uu),rush=float(uu.rushing_yards.fillna(0).sum()),pa=tt.pa,ra=tt.ra))
    d=pd.DataFrame(rows); act=d[(d.tgt+d.car)>0]
    return d,act,r[r.complete_pass==1].receiving_yards.dropna().values,u.rushing_yards.dropna().values,r
def nb(rng,mean,var,n):
    var=max(var,mean*1.05)
    pr=mean/var; k=mean*pr/(1-pr); return rng.negative_binomial(k,pr,n)
def sim(leg):
    name,team,mkt,spread=leg['player'],leg['team'],leg['market'],leg['spread']; team={'LAR':'LA','WSH':'WAS'}.get(team,team)
    d,a,ypc_rec,ypc_rush,r=player(name,team)
    l3=a.tail(3); w=lambda col:0.6*a[col].mean()+0.4*l3[col].mean()
    cr=(a.rec.sum()+1)/(a.tgt.sum()+2)
    opp={'LAR':'LA','WSH':'WAS'}.get(leg['opp'],leg['opp']); g=pid(name,team); PG=pos.get(g,'WR')
    A_ypt,_=oppadj(opp,PG,'ypt'); A_cr,_=oppadj(opp,PG,'cr'); A_ypc,_=oppadj(opp,PG,'ypc')
    cr=min(cr*A_cr,0.95); A_rec_y=A_ypt/A_cr  # yards per catch adj
    YK=float(os.environ.get('BG_YPCREG',0))
    if YK>0 and len(ypc_rush):  # v4 FIX: regress player YPC toward league (k carries), then apply FULL opponent YPC allowed (all rushes), replacing v3 shrunk RB-only opp adj
        lgA=ru.rushing_yards.mean(); pm=ypc_rush.mean(); wv=len(ypc_rush)/(len(ypc_rush)+YK)
        oppY=ru[ru.defteam==opp].rushing_yards.mean()
        A_ypc=((wv*pm+(1-wv)*lgA)/pm)*(oppY/lgA)
        YPCINFO=dict(player_ypc=float(pm),n=int(len(ypc_rush)),w=float(wv),league=float(lgA),opp_allowed=float(oppY),target_ypc=float(pm*A_ypc))
    else: YPCINFO={}
    if SHR>0:  # sensitivity: shrink player per-play yards toward league position mean
        lr=pp[(pp.pg==PG)&(pp.complete_pass==1)].receiving_yards.mean(); lu=ru[ru.pg=='RB'].rushing_yards.mean()
        if len(ypc_rec): A_rec_y*= (1-SHR)+SHR*lr/ypc_rec.mean()
        if len(ypc_rush): A_ypc*= (1-SHR)+SHR*lu/ypc_rush.mean()
    out={}; info=dict(n_games=len(a),games=a.game_id.tolist())
    for mode in ['mc','bias','gr']:
        rng=np.random.default_rng(SEED+int(hashlib.md5(f'{name}|{mkt}|{mode}'.encode()).hexdigest()[:6],16))
        vf,cf,yf=(0.92,0.97,0.95) if mode=='bias' else (1,1,1)
        def vol(col,teamcol,b):
            mean=w(col)*vf
            if mode!='gr': return nb(rng,mean,a[col].var(ddof=1),N)
            # GR: share x team volume; team vol shared pace lognormal + script shock
            share=(a[col]/a[teamcol]); m_s,v_s=share.mean(),max(share.var(ddof=1),1e-4)
            if len(l3): m_s=0.6*m_s+0.4*(l3[col]/l3[teamcol]).mean()
            kk=m_s*(1-m_s)/v_s-1; kk=max(kk,2)
            sh=rng.beta(m_s*kk,(1-m_s)*kk,N)
            tm=tg[tg.posteam==team][teamcol]; sig=np.std(np.log(tm),ddof=1)
            M=rng.normal(-spread,SD_MARGIN,N); pace=rng.lognormal(0,sig,N)
            # center script: E[team vol | margin] relative to league mean margin 0, mean preserved at -spread
            TV=tm.mean()*pace*np.exp(b*(M-(-spread)))*np.exp(b*(-spread))  # spread-signed expected shift
            TV=TV*(mean/(m_s*TV.mean()))  # FIX v2: anchor GR mean volume to MC weighted mean (removes share x team-mean inflation); GR adds variance only
            return rng.binomial(np.maximum(np.round(TV).astype(int),0),np.clip(sh,0,1))
        res={}
        if mkt in ('rec','recyds','rushrec'):
            T=vol('tgt','pa',bP); C=rng.binomial(T,np.clip(cr*cf,0,1))
            if mkt=='rec': res['x']=C
            else:
                tot=np.zeros(N); mx=C.max()
                for i in range(mx): tot+=np.where(C>i,rng.choice(ypc_rec,N),0)
                res['x']=tot*yf*A_rec_y
        if mkt in ('rushyds','rushrec'):
            Cr=vol('car','ra',bR); tot=np.zeros(N)
            for i in range(Cr.max()): tot+=np.where(Cr>i,rng.choice(ypc_rush,N),0)
            res['x']=res.get('x',0)+tot*yf*A_ypc
        x=res['x']; out[mode]=dict(mean=float(x.mean()),median=float(np.median(x)),p10=float(np.percentile(x,10)),p90=float(np.percentile(x,90)),
              rungs={str(k):float((x>=k).mean()) for k in leg['rungs']})
    info.update(ypc=YPCINFO,log=a[['date','tgt','rec','ry','car','rush','pa','ra']].assign(date=a.date.astype(str)).to_dict('records'),
       w_tgt=float(w('tgt')),w_car=float(w('car')),cr=float(cr),n_rec_yards=len(ypc_rec),n_rush=len(ypc_rush),
       sigma_pace_pa=float(np.std(np.log(tg[tg.posteam==team].pa),ddof=1)),sigma_pace_ra=float(np.std(np.log(tg[tg.posteam==team].ra),ddof=1)),
       A_ypt=A_ypt,A_cr=A_cr,A_ypc=A_ypc,pos=PG,team_pa=float(tg[tg.posteam==team].pa.mean()),team_ra=float(tg[tg.posteam==team].ra.mean()))
    return out,info
if __name__=='__main__':
    legs=json.load(open(LEGS)); R={}
    for L in legs:
        k=f"{L['player']}|{L['market']}"; o,i=sim(L); R[k]=dict(leg=L,sims=o,info=i); print(k,{m:(round(o[m]['median'],1),{r:round(v,3) for r,v in o[m]['rungs'].items()}) for m in o},flush=True)
    R['_meta']=dict(N=N,seed=SEED,bP=bP,bR=bR,sd_margin=SD_MARGIN,pbp_sha=hashlib.sha256(open(SRC+'play_by_play_2026.parquet','rb').read()).hexdigest(),
                    code_sha=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
    json.dump(R,open(OUT,'w'),indent=1,default=float)
    print('slopes',bP,bR)
