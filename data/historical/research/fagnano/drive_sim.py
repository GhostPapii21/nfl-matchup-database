# ESTIMATES throughout. Drive-level BAL sim + Henry + Hill/Bateman/Lane
import numpy as np,pandas as pd; rng=np.random.default_rng(9); N=100000
p=pd.read_parquet('../bal_secondary/raw/play_by_play_2026.parquet');p=p[p.season_type=='REG']
hc=p[(p.rusher_player_name=='D.Henry')&(p.rush_attempt==1)].yards_gained.dropna().values
cases={'base':dict(drv=10.5,tao=.42,to=.14,pts_td=.17,pts_fg=.16,hc=14,ys=.90,pr=.58),
       'rico':dict(drv=11,tao=.50,to=.17,pts_td=.13,pts_fg=.14,hc=12,ys=.90,pr=.62),
       'flip':dict(drv=10.5,tao=.33,to=.11,pts_td=.22,pts_fg=.18,hc=18,ys=.92,pr=.65)}
for k,c in cases.items():
  dr=rng.poisson(c['drv'],N); tao=rng.binomial(dr,c['tao']); rest=dr-tao
  to=rng.binomial(dr,c['to']); td=rng.binomial(rest,c['pts_td']/(1-c['tao'])); fg=rng.binomial(rest-td,c['pts_fg']/(1-c['tao']))
  plays=tao*3.2+rest*6.9; pts=td*7+fg*3
  car=rng.poisson(c['hc'],N); ys=np.array([ (rng.choice(hc,n)*c['ys']).sum() if n else 0 for n in car[:20000]])
  lng=np.array([ (rng.choice(hc,n)*c['ys']).max() if n else 0 for n in car[:20000]])
  att=plays*c['pr']*0.885; # minus sacks/scrambles
  print(f"{k}: drives {dr.mean():.1f} 3&out {tao.mean():.1f} TO {to.mean():.2f} BAL plays {plays.mean():.1f} pts {pts.mean():.1f} P(pts<13.5) {(pts<13.5).mean():.2f} | Henry car {car.mean():.1f} yds {ys.mean():.0f} P>49.5 {(ys>49.5).mean():.2f} >59.5 {(ys>59.5).mean():.2f} >69.5 {(ys>69.5).mean():.2f} long med {np.median(lng):.0f} P(long>=15) {(lng>=15).mean():.2f} | att {att.mean():.1f}")
  # receivers: share, catch rate, yds/rec (estimates)
  for n,sh,cr,ypr,lines in [('Hill',.16,.68,5.5,[(1.5,'rec'),(2.5,'rec'),(14.5,'yds')]),('Bateman',.12,.58,13,[(1.5,'rec'),(14.5,'yds'),(16.5,'yds')]),('Lane',.09,.65,9.5,[(1.5,'rec'),(14.5,'yds')]),('Flowers',.24,.58,11,[(4.5,'rec'),(44.5,'yds')]),('Andrews',.14,.65,7,[(2.5,'rec'),(18.5,'yds')])]:
    a=rng.poisson(att.mean(),N); t=rng.binomial(a,sh); r=rng.binomial(t,cr); y=r*rng.gamma(2,ypr/2,N)
    print(f"   {n}: tgt {t.mean():.1f} rec {r.mean():.1f} yds {y.mean():.0f} "+' '.join(f"{l[1]}>{l[0]} {((r if l[1]=='rec' else y)>l[0]).mean():.2f}" for l in lines))
