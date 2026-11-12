"""P6 rush-over exception backtest (analysis only; nothing live, run_gate untouched).
P6 proxy: RB rush-yds OVER on an underdog team (team spread > 0) = 'needs a trailing script' -> cut by P6.
Walk-forward: week W uses pbp strictly before week W's first game (Engine cutoff), RAW sim_v6 (calib=None,
because calib was fitted on wk4-7 outcomes -> would leak). 100k sims per model, 3 models; p = mean of mc/bias/gr P(X>=line).
Lines: real book line from runs/2026-11-01_*/run_manifest.json if present, else stand-in floor(prior median)+0.5 (>=2 prior games)."""
import sys, json, glob, os
import numpy as np, pandas as pd
sys.path.insert(0,'/workspace/nfl-database/tools'); sys.path.insert(0,'/workspace/nfl-database/backtests/wk8_proposals')
import sim_v6 as S
from harness import load, proxy_line, prior_vals
ROOT='/workspace/nfl-database'
def real_lines():
    r={}
    for f in glob.glob(f"{ROOT}/runs/2026-11-01_*/run_manifest.json"):
        for l in json.load(open(f)).get('legs',[]):
            if l.get('market')!='rushyds': continue
            pt=next((b['point'] for b in (l.get('fanduel'),l.get('pinnacle'),l.get('draftkings')) if isinstance(b,dict) and b.get('point') is not None), l.get('line'))
            r.setdefault(l.get('player'),pt)
    return r
def main():
  d,g,pg=load(); RL=real_lines(); rows=[]
  for W in range(3,9):
      cut=d[d.week==W].game_date.min(); E=S.Engine(cutoff=cut,calib=None)
      cur=pg[(pg.week==W)&(pg.pos=='RB')&(pg.car>0)]
      for _,r in cur.iterrows():
          pr=pg[(pg.pid==r.pid)&(pg.week<W)&(pg.car>0)]
          if len(pr)<2 or pr.car.mean()<8 or not (r.team_spread>0): continue
          name=E.pos and S._PL.set_index('gsis_id').display_name.get(r.pid,r.pid)
          src='standin'; line=proxy_line(prior_vals(pg[pg.car>0],r.pid,W,'ryds'))
          if W==8 and name in RL and RL[name] is not None: line,src=float(RL[name]),'real'
          if line is None: continue
          try: o,info=E.sim(dict(player=name,gsis=r.pid,team=r.team,opp=r.opp,market='rushyds',spread=float(r.team_spread),rungs=[line]),raw=True)
          except Exception as e: print('skip',name,W,e); continue
          ps={m:o[m]['rungs'][str(line)] for m in S.MODES}
          rows.append(dict(week=W,player=name,gsis=r.pid,team=r.team,opp=r.opp,team_spread=float(r.team_spread),line=line,line_src=src,
              p_mc=ps['mc'],p_bias=ps['bias'],p_gr=ps['gr'],p=np.mean(list(ps.values())),med_mc=o['mc']['median'],actual=float(r.ryds),carries=int(r.car),hit=int(r.ryds>line)))
          print(W,name,line,src,round(rows[-1]['p'],3),r.ryds,flush=True)
  pd.DataFrame(rows).to_csv('p6_legs_pbp_wk3_8TNF.csv',index=False)

if __name__=='__main__': main()