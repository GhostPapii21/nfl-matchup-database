# Scenario-first chain; every rate below is an ESTIMATE (see report.md)
import numpy as np; rng=np.random.default_rng(5); N=100000
cases={'base':(54,.58),'flip':(56,.65)}
out={}
for k,(plays,pr) in cases.items():
  pl=rng.normal(plays,5,N); db=rng.binomial(np.maximum(pl,30).astype(int),pr)
  sk=rng.binomial(db,.085); sc=rng.binomial(db-sk,.03); att=db-sk-sc
  cp=np.clip(rng.normal(.585,.06,N),.35,.8); cmp_=rng.binomial(att,cp)
  ypc=np.clip(rng.normal(10.6,1.8,N),5,18); yds=cmp_*ypc - 0  # sack yds not in pass yds
  ints=rng.poisson(att*.027); tds=rng.poisson(np.maximum(att*.032,0))
  ry=sc*6+rng.binomial(2,.5,N)*2
  out[k]=dict(att=att,cmp=cmp_,yds=yds,ints=ints,tds=tds,sk=sk,ru=sc+rng.binomial(2,.5,N),ry=ry)
for k,o in out.items():
  print(k,{m:round(float(np.mean(v)),1) for m,v in o.items()})
  y=o['yds'];print('  P yds>149.5 %.2f 160.5 %.2f 162.5 %.2f 175.5 %.2f 199.5 %.2f'%tuple((y>t).mean() for t in [149.5,160.5,162.5,175.5,199.5]))
  print('  cmp>15.5 %.2f  INT>=1 %.2f  TD>=1 %.2f sacks>=3 %.2f sacks>2.5 rush yds>9.5 %.2f'%((o['cmp']>15.5).mean(),(o['ints']>=1).mean(),(o['tds']>=1).mean(),(o['sk']>=3).mean(),(o['ry']>9.5).mean()))
