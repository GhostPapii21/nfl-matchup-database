import os,sys,json,re,numpy as np,pandas as pd
os.environ['BG_YPCREG']='100'; sys.argv=['x']
sys.path.insert(0,'.'); import bg_sim_v4 as B
fd=pd.read_csv('/workspace/nfl-database/week8/betguru_2026-11-01_raw/fd_now.csv')
P0=[('Jahmyr Gibbs','DET','MIN',-3.5),('James Cook','BUF','BAL',-3),('Kenneth Walker III','KC','DEN',-1.5),('Puka Nacua','LA','LAC',-6.5),
('Brock Bowers','LV','NYJ',1.5),('Trey McBride','ARI','DAL',7),('CeeDee Lamb','DAL','ARI',-7),('Ryan Flournoy','DAL','ARI',-7),('Bhayshul Tuten','JAX','IND',-10.5),
('DK Metcalf','PIT','CLE',-3.5),('Antonio Williams','WAS','PHI',-5.5),('Amon-Ra St. Brown','DET','MIN',-3.5),('Drake London','ATL','TB',2.5),('Justin Jefferson','MIN','DET',3.5),
('Garrett Wilson','NYJ','LV',-1.5),('Parker Washington','JAX','IND',-10.5),('Zay Flowers','BAL','BUF',3),('Aaron Jones','MIN','DET',3.5),('Bijan Robinson','ATL','TB',2.5),
('Braelon Allen','NYJ','LV',-1.5),('Javonte Williams','DAL','ARI',-7),('Jonathan Taylor','IND','JAX',10.5),('Dallas Goedert','PHI','WAS',5.5),('Jaylen Warren','PIT','CLE',-3.5),('Kyren Williams','LA','LAC',-6.5)]
P=[x for x in P0 if x[0] in ('Jahmyr Gibbs','Kenneth Walker III','Puka Nacua','Bhayshul Tuten','Jaylen Warren','Kyren Williams')]
MK={'Alt Rushing Yds':'rushyds','Alt Receptions':'rec','Alt Receiving Yds':'recyds'}
MAIN={'rushyds':'Rushing Yds','rec':'Total Receptions','recyds':'Receiving Yds','rushrec':'Rushing + Receiving Yds'}
def am(o):return 100/(o+100) if o>0 else -o/(-o+100)

import pandas as _pd
_p=_pd.read_parquet('/tmp/play_by_play_2026.parquet');_f=_pd.read_parquet('/tmp/ftn.parquet')
_d=_p[_p.qb_dropback==1].merge(_f[['nflverse_game_id','nflverse_play_id','n_blitzers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'])
_d['bl']=_d.n_blitzers>0
def _l4(t):
  w=sorted(_d[_d.defteam==t].week.unique())[-4:];return _d[(_d.defteam==t)&_d.week.isin(w)].bl.mean()
LGB=_d.bl.mean();TM={}
SN={'Jahmyr Gibbs':'J.Gibbs','Kenneth Walker III':'K.Walker','Puka Nacua':'P.Nacua','Bhayshul Tuten':'B.Tuten','Jaylen Warren':'J.Warren','Kyren Williams':'K.Williams'}
for nm,tm,op,_ in P0:
  if nm not in SN:continue
  q=_d[(_d.posteam==tm)&(_d.pass_attempt==1)&_d.receiver_player_id.notna()]
  r=q.receiver_player_name==SN[nm];sb=r[q.bl].mean();sn=r[~q.bl].mean();ss=r.mean();b=_l4(op)
  m=(b*sb+(1-b)*sn)/ss;TM[nm]=1+0.5*(m-1)
  print('PRESS',nm,op,'blitzL4',round(b,3),'shareBlitz',round(sb,3),'noBlitz',round(sn,3),'season',round(ss,3),'tgtmult(50%shrunk)',round(TM[nm],3))
QADJ={'MIN':4.72/4.04,'CLE':3.63/3.89,'IND':8.12/7.74,'LAC':3.81/4.53,'DEN':5.23/5.06}
_op=B.oppadj
def _oa(opp,PG,k,*a,**kw):
  f,x=_op(opp,PG,k,*a,**kw)
  return (f*(1+0.5*(QADJ.get(opp,1)-1)),x) if (k=='ypt' and PG=='RB') else (f,x)
B.oppadj=_oa
_pl=B.player
def _player(name,team,*a,**kw):
  d,aa,yrec,yrush,r=_pl(name,team,*a,**kw)
  if name in TM: aa=aa.copy(); aa['tgt']=aa['tgt']*TM[name]
  return d,aa,yrec,yrush,r
B.player=_player

lgY=B.ru.rushing_yards.mean()
def mine(name,team,opp,spread,mkt,rungs):
  d,a,yrec,yrush,r=B.player(name,team); g=B.pid(name,team); PG=B.pos.get(g,'WR')
  T=a.tgt.mean(); C=a.car.mean(); cr=(a.rec.sum()+1)/(a.tgt.sum()+2)
  Ay,_=B.oppadj(opp,PG,'ypt'); Ac,_=B.oppadj(opp,PG,'cr')
  oppY=B.ru[B.ru.defteam==opp].rushing_yards.mean()
  ry=yrush*(((yrush.mean()+lgY)/2)/yrush.mean())*(1+0.5*(oppY/lgY-1)) if len(yrush) else yrush
  sg=1 if mkt=='rushyds' else (-1 if PG in('WR','TE') else 0); out={}
  for j,m in enumerate(['mc','bias','gr']):
    rng=np.random.default_rng(abs(hash((name,mkt,m)))%2**32 if False else 4242+j+sum(map(ord,name+mkt)))
    vf,cf,yf=(.92,.97,.95) if m=='bias' else (1,1,1); N=100000
    sh=rng.lognormal(0,.22,N)*np.exp(.08*rng.normal(0,1,N)*(np.sign(-spread) if True else 0)) if m=='gr' else np.ones(N)
    x=np.zeros(N)
    if mkt in('rec','recyds','rushrec'):
      n=rng.poisson(rng.gamma(8,T*vf*sh/8)); c=rng.binomial(n,min(cr*Ac*cf,.95))
      if mkt=='rec': x=c.astype(float)
      elif len(yrec):
        mx=c.max(); x=x+(rng.choice(yrec,(N,mx))*(np.arange(mx)[None]<c[:,None])).sum(1)*Ay/Ac*yf
    if mkt in('rushyds','rushrec') and len(ry):
      n=rng.poisson(rng.gamma(8,C*vf*sh/8)); mx=n.max()
      x=x+(rng.choice(ry,(N,mx))*(np.arange(mx)[None]<n[:,None])).sum(1)*yf
    out[m]={str(k):float((x>=k).mean()) for k in rungs}; out[m]['med']=float(np.median(x))
  return out
rows=[]
for name,team,opp,sp in P:
  f=fd[fd.market.str.startswith(name+' - ')]
  for alt,mkt in list(MK.items())+[(None,'rushrec')]:
    mm=f[f.market==f'{name} - {MAIN[mkt]}']
    o=mm[mm.runner.str.contains('Over')]; u=mm[mm.runner.str.contains('Under')]
    if not len(o):continue
    io,iu=am(o.odds.iloc[0]),am(u.odds.iloc[0]); V=io+iu; line=o.hcp.iloc[0]
    if alt:
      a=f[f.market==f'{name} - {alt}']
      lad=[(int(re.search(r'(\d+)\+',x).group(1)),int(od)) for x,od in zip(a.runner,a.odds) if re.search(r'(\d+)\+',x)]
    else: lad=[(int(np.ceil(line)),int(o.odds.iloc[0]))]
    lad=sorted(set(lad))
    if not lad:continue
    rungs=[k for k,_ in lad]
    try:
      mi=mine(name,team,opp,sp,mkt,rungs)
      bo,_=B.sim(dict(player=name,team=team,market=mkt,spread=sp,rungs=rungs,opp=opp))
    except Exception as e: print('ERR',name,mkt,e);continue
    for k,od in lad:
      fair=min(am(od)/V,.99)
      if alt is None: fair=io/V
      g=np.mean([mi[m][str(k)] for m in mi]); b=np.mean([bo[m]['rungs'][str(k)] for m in bo])
      rows.append(dict(player=name,team=team,opp=opp,spread=sp,mkt=mkt,rung=k,odds=od,main=line,V=round(V,3),nv=round(fair,3),
        g_mc=mi['mc'][str(k)],g_b=mi['bias'][str(k)],g_gr=mi['gr'][str(k)],g=g,g_med=mi['mc']['med'],
        b_mc=bo['mc']['rungs'][str(k)],b_b=bo['bias']['rungs'][str(k)],b_gr=bo['gr']['rungs'][str(k)],b=b,b_med=bo['mc']['median']))
  print(name,'done',flush=True)
df=pd.DataFrame(rows)
for s in 'gb':
  df[s+'_e']=(df[s]-df.nv)*100; df[s+'_se']=((0.5+0.7*(df[s]-0.5))-df.nv)*100
df.to_csv('/workspace/nfl-database/week8/phase_walk/pressure_scan.csv',index=False)
