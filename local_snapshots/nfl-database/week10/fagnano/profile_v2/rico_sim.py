# ESTIMATES. Clock-linked drive sim: BAL 3&outs -> more JAX drives/plays; JAX pass rate falls with lead.
import numpy as np; rng=np.random.default_rng(11); N=100000
sy=np.load('strange_catch_yds_2026.npy')  # Strange 2026 catch yards (n=28, pbp)
cases={'base':dict(tao=.42,bal_td=.17,bal_fg=.16),'rico':dict(tao=.50,bal_td=.13,bal_fg=.14),'flip':dict(tao=.33,bal_td=.22,bal_fg=.18)}
import sys; SH=float(sys.argv[1]) if len(sys.argv)>1 else .209
for k,c in cases.items():
  # minutes per drive: BAL 3&out 1.7, BAL other 3.0, JAX 2.9 (incl. kick/clock), 60 min
  bal_min=c['tao']*1.7+(1-c['tao'])*3.0; pair=bal_min+3.3
  dr=rng.poisson(60/pair,N)             # drives each side
  tao=rng.binomial(dr,c['tao']); rest=dr-tao
  td=rng.binomial(rest,c['bal_td']/(1-c['tao'])); fg=rng.binomial(rest-td,c['bal_fg']/(1-c['tao']))
  balpts=7*td+3*fg
  jdr=dr+rng.integers(0,2,N)
  jplays=rng.normal(jdr*6.0,4)          # JAX 5.99 plays/drive (58.3/9.7 pbp)
  jpts=np.maximum(rng.normal(jdr*2.65*(1+0.15*(c['tao']-.42)/.08*0.5),7),0)  # JAX ~27-28 at -10
  lead=jpts-balpts
  pr=np.where(lead>=14,.45,.558)        # blend: big lead late -> 0.338 for ~half the game
  att=rng.binomial(np.maximum(jplays,30).astype(int),pr)*0.938
  att=att.astype(int)
  t=rng.binomial(att,SH); r=rng.binomial(t,.80)
  yds=np.array([rng.choice(sy,n).sum() if n else 0 for n in r[:30000]])
  # 1H: 1H target share .63 (pbp; neutral-script 1H, no lead burn)
  r1=rng.binomial(r[:30000],.58); y1=np.array([rng.choice(sy,n).sum() if n else 0 for n in r1])
  mid=np.array([ (lambda s:(s[(s>=12)&(s<=20)].sum()))(rng.choice(sy,n)) if n else 0 for n in r[:30000]])
  print(f"{k}: drives/side {dr.mean():.1f} BAL 3&out {tao.mean():.1f} BAL pts {balpts.mean():.1f} | JAX drives {jdr.mean():.1f} plays {jplays.mean():.1f} att {att.mean():.1f} P(lead14+) {(lead>=14).mean():.2f}")
  print(f"   Strange tgt {t.mean():.1f} rec {r.mean():.1f} yds {yds.mean():.0f} | P4+ {(r>=4).mean():.2f} P5+ {(r>=5).mean():.2f} P40+ {(yds>=40).mean():.2f} | 1H rec {r1.mean():.1f} yds {y1.mean():.0f} P1H25+ {(y1>=25).mean():.2f} | 12-20yd share {mid.sum()/yds.sum():.2f}")
