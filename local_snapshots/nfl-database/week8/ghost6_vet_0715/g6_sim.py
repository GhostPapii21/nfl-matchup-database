# Ghost6 independent sim, Nov 1 2026. 3 models x 100k, seed 20261101+hash. Regressed YPC/YPR toward league; opp factor shrunk 50%.
import pandas as pd, numpy as np, json, hashlib, csv
SRC='/workspace/nfl-database/week8/phase_walk/src/'; N=100_000; SEED=20261101
p=pd.read_parquet(SRC+'play_by_play_2026.parquet'); p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
pl=pd.read_parquet(SRC+'players.parquet'); pos=pl.set_index('gsis_id').position_group.to_dict()
pas=p[(p.pass_attempt==1)&(p.sack!=1)].copy(); pas['pg']=pas.receiver_player_id.map(pos)
ru=p[p.rush_attempt==1].copy(); ru['pg']=ru.rusher_player_id.map(pos)
LG_YPC=ru[ru.pg=='RB'].rushing_yards.mean()
def pid(name,team):
    c=pl[pl.display_name==name]
    if len(c)>1 and (c.latest_team==team).any(): c=c[c.latest_team==team]
    return c.gsis_id.iloc[0]
def oppf(opp,pg,kind):
    if kind=='rush': d=ru[ru.pg=='RB']; f=lambda x:x.rushing_yards.mean()
    elif kind=='cr': d=pas[pas.pg==pg]; f=lambda x:x.complete_pass.mean()
    else: d=pas[(pas.pg==pg)&(pas.complete_pass==1)]; f=lambda x:x.receiving_yards.mean()
    return 1+0.5*(f(d[d.defteam==opp])/f(d)-1)
def log(name,team):
    g=pid(name,team); gm=p[p.posteam==team].groupby('game_id').game_date.first().sort_values()
    rows=[]
    for gid,dt in gm.items():
        r=pas[(pas.game_id==gid)&(pas.receiver_player_id==g)]; u=ru[(ru.game_id==gid)&(ru.rusher_player_id==g)]
        tp=pas[(pas.game_id==gid)&(pas.posteam==team)]; tr=ru[(ru.game_id==gid)&(ru.posteam==team)]
        rows.append(dict(gid=gid,date=dt,tgt=len(r),rec=int(r.complete_pass.sum()),ry=r.receiving_yards.fillna(0).sum(),car=len(u),rush=u.rushing_yards.fillna(0).sum(),tpa=len(tp),tra=len(tr)))
    d=pd.DataFrame(rows); return g,d[(d.tgt+d.car)>0]
def nb(rng,m,v,n):
    v=max(v,m*1.1); pr=m/v; k=m*pr/(1-pr); return rng.negative_binomial(k,pr,n)
def run(leg):
    name,team,opp,mkt,rung,spread=leg['player'],leg['team'],leg['opp'],leg['mkt'],leg['rung'],leg['spread']
    g,a=log(name,team); PG=pos.get(g,'WR'); l4=a.tail(4)
    out={'n_games':len(a),'L4':l4[['date','tgt','rec','ry','car','rush']].astype(str).values.tolist()}
    res={}
    for mode in ['mc','bias','gr']:
        rng=np.random.default_rng(SEED+int(hashlib.md5(f'{name}|{mkt}|{mode}'.encode()).hexdigest()[:6],16))
        vf,cf,yf=(0.92,0.97,0.95) if mode=='bias' else (1,1,1)
        if mode=='gr':
            M=rng.normal(-spread,13.5,N); shock=rng.lognormal(0,0.12,N)
            pas_m=np.exp(-0.008*(M+spread))*shock; run_m=np.exp(0.012*(M+spread))*shock; yshock=rng.lognormal(0,0.06,N)
        else: pas_m=run_m=yshock=np.ones(N)
        if mkt in ('rec','recyds'):
            mt=0.5*a.tgt.mean()+0.5*l4.tgt.mean()
            T=nb(rng,mt*vf,a.tgt.var(ddof=1),N); T=np.round(T*pas_m).astype(int)
            lgcr=pas[pas.pg==PG].complete_pass.mean(); cr=(a.rec.sum()+30*lgcr)/(a.tgt.sum()+30)*oppf(opp,PG,'cr')*cf
            C=rng.binomial(T,np.clip(cr,0,.95))
            if mkt=='rec': X=C
            else:
                yc=pas[(pas.receiver_player_id==g)&(pas.complete_pass==1)].receiving_yards.dropna().values
                lg=pas[(pas.pg==PG)&(pas.complete_pass==1)].receiving_yards.mean(); n=len(yc)
                tgtm=(n*yc.mean()+40*lg)/(n+40); sc=tgtm/yc.mean()*oppf(opp,PG,'ypr')*yf
                X=np.zeros(N)
                for i in range(C.max()): X+=np.where(C>i,rng.choice(yc,N)*sc,0)
                X=X*yshock
        else:
            mc=0.5*a.car.mean()+0.5*l4.car.mean()
            Cn=nb(rng,mc*vf,a.car.var(ddof=1),N); Cn=np.round(Cn*run_m).astype(int)
            yr=ru[ru.rusher_player_id==g].rushing_yards.dropna().values; n=len(yr)
            tgtm=(n*yr.mean()+100*LG_YPC)/(n+100); sc=tgtm/yr.mean()*oppf(opp,PG,'rush')*yf
            X=np.zeros(N)
            for i in range(Cn.max()): X+=np.where(Cn>i,rng.choice(yr,N)*sc,0)
            X=X*yshock
        res[mode]=(round(float((X>=rung).mean()),4),round(float(np.median(X)),1))
    out['sims']=res; return out
legs=json.load(open('legs.json')); R={}
for L in legs:
    try: R[L['id']]=run(L); print(L['id'],R[L['id']]['sims'])
    except Exception as e: print('ERR',L['id'],e); R[L['id']]={'err':str(e)}
json.dump(R,open('g6_sims.json','w'),indent=1,default=str)
