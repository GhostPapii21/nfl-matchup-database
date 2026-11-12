"""r6 wrapper only. sim_v6 engine unchanged; Fagnano scenario inputs remain ESTIMATES.
Player markets use sim_v6.Engine.sim. 1H spread is an uncalibrated wrapper extension
because sim_v6 does not implement spread_h1; never represent that extension as native pricing.
"""
import ast, os, sys, json, hashlib, datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
ROOT=Path(__file__).resolve().parents[3]; RUN=Path(__file__).resolve().parents[1]; OUT=RUN/'codex'
N=100000; SEED=20261104
os.environ['SIMV6_SRC']=str(OUT/'sim_src'); src=OUT/'sim_src'; src.mkdir(exist_ok=True)
for name,path in [('play_by_play_2026.parquet',ROOT/'runs/2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet'),('players.parquet',ROOT/'runs/2026-11-01_shared_src/players.parquet')]:
 dest=src/name
 if not dest.exists(): dest.symlink_to(path)
sys.path.insert(0,str(ROOT/'tools')); import sim_v6 as S
# AST-read literal scenario dictionaries: no source scripts are changed or executed.
def literal(path,name):
 tree=ast.parse(path.read_text())
 for node in tree.body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
   return eval(compile(ast.Expression(node.value),str(path),'eval'),{'dict':dict})
 raise ValueError(name)
profile=ROOT/'week10/fagnano/profile_v2/rico_sim.py'; drive=ROOT/'week10/fagnano/drive_sim.py'
cases=literal(profile,'cases'); dcases=literal(drive,'cases')
base=S.Engine(cutoff='2026-11-05',n=N,seed=SEED)
# Preserve model definitions, calibration, RNG and yard resampling in sim_v6;
# scale historical target/complete counts together to set the scenario volume anchor.
class ContextEngine(S.Engine):
 def player(self,name,team,qb=False,gsis=None):
  d,a,yc,yr,g=super().player(name,team,qb,gsis)
  if team=='JAX' and not qb:
   factor=self.jax_att/base.tg[base.tg.posteam=='JAX'].pa.mean()
   d=d.copy(); a=a.copy()
   for frame in (d,a):
    for col in ('tgt','rec'): frame[col]=frame[col]*factor
  return d,a,yc,yr,g
legs=[('Strange 4+ rec (o3.5)','Brenton Strange','JAX','BAL','rec',4),('Strange 40+ rec yds (o39.5)','Brenton Strange','JAX','BAL','recyds',39.5),('Washington rec yds o63.5','Parker Washington','JAX','BAL','recyds',63.5),('Henry 40+ rush (o39.5)','Derrick Henry','BAL','JAX','rushyds',39.5)]
models={'mc':'monte_carlo','bias':'bias','gr':'game_randomness'}
result={m:dict(model=v,n=N,seed=SEED,script='tools/sim_v6.py',wrapper=str(Path(__file__).relative_to(ROOT)),legs={}) for m,v in models.items()}
audit={'n':N,'seed':SEED,'script':'tools/sim_v6.py','script_sha256':hashlib.sha256((ROOT/'tools/sim_v6.py').read_bytes()).hexdigest(),'pbp_sha256':hashlib.sha256((src/'play_by_play_2026.parquet').read_bytes()).hexdigest(),'calibration_sha256':hashlib.sha256((ROOT/'tools/sim_v6_calib.json').read_bytes()).hexdigest(),'inputs':[str(profile),str(drive),str(ROOT/'week10/fagnano/report.md'),str(ROOT/'week10/fagnano/profile_v2/summary.md')],'assumptions':['All Fagnano scenario rates are sourced ESTIMATES, not observations. Base used for manifest; rico/flip are sensitivity cases, not model aliases.','JAX pass-volume anchor follows profile_v2 clock/lead model, applied equally to Strange and Washington; catch rates and yards remain sim_v6 history/opponent/calibration.','Henry carry target is drive_sim scenario hc via carry_boost; JAX run defense adjustment is native sim_v6. The separate drive_sim ys=.90 haircut is not double-applied.','1H spread has no native sim_v6 implementation. Wrapper uses profile_v2 full-game JAX points and BAL TD/FG, allocates to first half using observed team first-half scoring fractions from pbp, and uses sim_v6.nb for drive-count volume (mc/bias). GR uses empirical team pace variation. No half-spread calibration exists; UNVERIFIED extension.','Fagnano has no regular-season starts and one relief sample; no causal QB effect is claimed.'],'scenarios':{}}
# Empirical scoring timing; zero-score games give no timing information.
p=base.p
fractions={}
for team in ('JAX','BAL'):
 q=p[(p.home_team==team)|(p.away_team==team)]
 vals=[]
 for gid,g in q.groupby('game_id'):
  home=g.home_team.iloc[0]==team; col='total_home_score' if home else 'total_away_score'
  first=g[g.qtr.le(2)][col].max(); total=g[col].max()
  if total>0 and np.isfinite(first): vals.append(float(first/total))
 fractions[team]=np.array(vals)
audit['half_scoring_fractions']={k:v.tolist() for k,v in fractions.items()}
for ci,(case,c) in enumerate(cases.items()):
 rng=np.random.default_rng(SEED+ci); dr=rng.poisson(60/(c['tao']*1.7+(1-c['tao'])*3+3.3),N)
 tao=rng.binomial(dr,c['tao']); rest=dr-tao
 td=rng.binomial(rest,c['bal_td']/(1-c['tao'])); fg=rng.binomial(rest-td,c['bal_fg']/(1-c['tao']))
 balpts=7*td+3*fg; jdr=dr+rng.integers(0,2,N); jplays=rng.normal(jdr*6,4)
 jpts=np.maximum(rng.normal(jdr*2.65*(1+.15*(c['tao']-.42)/.08*.5),7),0)
 pr=np.where(jpts-balpts>=14,.45,.558); att=(rng.binomial(np.maximum(jplays,30).astype(int),pr)*.938).astype(int)
 E=ContextEngine(cutoff='2026-11-05',n=N,seed=SEED); E.jax_att=float(att.mean()); entry={'context':dict(jax_attempts=E.jax_att,bal_pts=float(balpts.mean()),jax_pts=float(jpts.mean()),henry_carries=dcases[case]['hc']),'legs':{}}
 for name,player,team,opp,market,rung in legs:
  kw=dict(player=player,team=team,opp=opp,market=market,spread=0,rungs=[rung])
  if team=='BAL':
   _,a,_,_,_=base.player(player,team); wc=.6*a.car.mean()+.4*a.tail(3).car.mean(); kw['carry_boost']=dcases[case]['hc']/wc
  # Spread is zero: sourced clock/carry anchors already apply game script; don't double-apply a market spread.
  o,info=E.sim(kw); entry['legs'][name]={}
  for m in models:
   val=dict(p=o[m]['rungs'][str(rung)],median=o[m]['median'])
   entry['legs'][name][m]=val
   if case=='base': result[m]['legs'][name]=val
 for mi,m in enumerate(models):
  r=np.random.default_rng(SEED+500+ci*10+mi)
  mean=60/(c['tao']*1.7+(1-c['tao'])*3+3.3)
  if m=='gr':
   tm=base.tg[base.tg.posteam=='JAX'].pa; sig=float(np.std(np.log(tm),ddof=1)); drives=r.poisson(mean*r.lognormal(-sig*sig/2,sig,N))
  else: drives=S.nb(r,mean,float(dr.var(ddof=1)),N)
  three=r.binomial(drives,c['tao']); other=drives-three
  td1=r.binomial(other,c['bal_td']/(1-c['tao'])); fg1=r.binomial(other-td1,c['bal_fg']/(1-c['tao']))
  jf=r.choice(fractions['JAX'],N); bf=r.choice(fractions['BAL'],N)
  jp=np.maximum(r.normal((drives+r.integers(0,2,N))*2.65*(1+.15*(c['tao']-.42)/.08*.5),7),0)
  margin=np.rint(jp*jf)-(7*r.binomial(td1,bf)+3*r.binomial(fg1,bf))
  val=dict(p=float((margin>6.5).mean()),median=float(np.median(margin)),pricing_engine='UNVERIFIED wrapper extension; sim_v6.nb + profile_v2; not native spread_h1')
  entry['legs'].setdefault('JAX 1H -6.5',{})[m]=val
  if case=='base': result[m]['legs']['JAX 1H -6.5']=val
 audit['scenarios'][case]=entry
 print(case,json.dumps(entry['context']),flush=True)
(OUT/'sims.json').write_text(json.dumps(list(result.values()),indent=2,allow_nan=False)+'\n')
(OUT/'sims_audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
