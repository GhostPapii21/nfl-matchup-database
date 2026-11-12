"""Frozen selection; outcomes never used for ordering."""
import json
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent
# Fixed before fitting: two tail conditions per numeric feature, no middle bins.
NUMERIC_FEATURES = {
 'prior_carry_share': 'prior team carry share',
 'prior_snap_share': 'prior offensive snap share',
 'second_back_share': 'second RB share of team carries',
 'opp_rush_yds_game': 'opponent rushing yards allowed per game',
 'opp_rush_yds_carry': 'opponent rushing yards allowed per carry',
 'opp_rec_yds_position_game': 'opponent receiving yards allowed per game to this position',
 'prior_target_share': 'prior team target share',
 'spread': 'team spread',
 'implied_team_total': 'implied team total',
 'model_edge': 'directional prior-average yardage gap',
 'weather_temp': 'pre-kickoff weather temperature',
 'weather_wind': 'pre-kickoff weather wind',
}

def condition_mask(x, c):
 v=x[c['feature']]
 if c['op']=='le': return v.notna() & v.le(c['value'])
 if c['op']=='ge': return v.notna() & v.ge(c['value'])
 if c['op']=='eq': return v.notna() & v.eq(c['value'])
 raise ValueError(c)

def mask(x,r):
 q=(x.market==r['market'])&(x.side==r['side'])&x.price.notna()&(x.price!=0)
 q &= (x.side!='over') | (x.position.notna() & ((x.position!='RB') | (x.prior_carry_share>=.6)))
 for c in r['conditions']: q &= condition_mask(x,c)
 return q

def fit(train, write=True):
 """Fit only already settled train rows; never load or settle holdout."""
 from itertools import combinations
 from build import summary
 assert train.week.isin([3,4,5,6]).all()
 locked=[]; grids=[]
 for (market,side),z in train.groupby(['market','side'],sort=True):
  conditions=[];cuts={};excluded=[]
  for feature in NUMERIC_FEATURES:
   values=z[feature].dropna()
   if values.nunique()<3:
    excluded.append(feature);continue
   lo,hi=map(float,values.quantile([1/3,2/3]))
   cuts[feature]=[lo,hi]
   conditions.extend([dict(feature=feature,op='le',value=lo),dict(feature=feature,op='ge',value=hi)])
  for feature in ['favored','injury_status','injury_flag','weather_flag']:
   if feature not in z or z[feature].dropna().empty:
    excluded.append(feature);continue
   for value in sorted(z[feature].dropna().unique().tolist()):
    conditions.append(dict(feature=feature,op='eq',value=value))
  base=mask(z,dict(market=market,side=side,conditions=[])) & z.result.isin(['win','loss','push'])
  arrays=[condition_mask(z,c).to_numpy() for c in conditions]
  best=None;tested=0;qualifying=0
  for size in [1,2,3]:
   for ids in combinations(range(len(conditions)),size):
    cs=[conditions[i] for i in ids];fs=[c['feature'] for c in cs]
    if len(set(fs))!=size or fs==['model_edge']:continue
    tested+=1
    take=base.to_numpy().copy()
    for i in ids:take &= arrays[i]
    n=int(take.sum())
    if n<30:continue
    pl=float(z.loc[take,'pl'].sum());stake=float(z.loc[take,'stake'].sum())
    roi=100*pl/stake if stake else 0
    if roi<=0:continue
    qualifying+=1;score=roi*n/(n+50)
    key=(score,n,-size,tuple(-i for i in ids))
    if best is None or key>best[0]:best=(key,cs,take)
  grids.append(dict(market=market,side=side,tercile_cutpoints=cuts,excluded_unavailable_or_constant=excluded,candidate_cells=tested,qualifying_cells=qualifying))
  if best:
   key,cs,take=best
   stats=summary(z.loc[take],['market','side']).iloc[0].to_dict()
   locked.append(dict(market=market,side=side,conditions=cs,shrinkage_score=key[0],train=stats))
 cfg=dict(train_weeks=[3,4,5,6],holdout_weeks=[7,8],rb_over_min_carry_share=.6,
  search=dict(numeric_bins='low <= train q1/3; high >= train q2/3; linear quantiles per market-side, available train rows before guards; no holdout cutpoints',condition_counts=[1,2,3],distinct_features=True,requires_non_gap_condition=True,min_train_n=30,min_roi_exclusive=0,score='ROI*n/(n+50)',ties='larger n, fewer conditions, fixed grid order',grids=grids),rules=locked)
 if write: (HERE/'locked_rules.json').write_text(json.dumps(cfg,indent=2)+'\n')
 desc=['# Locked train matchup/script/role rules',
 'Pre-specified grid: 1–3 conditions on distinct features per market-side. Each numeric feature offers only low (<= train 1/3 quantile) and high (>= train 2/3 quantile) tails. Cutpoints use available weeks 3–6 feature values within each market-side before guards, with linear interpolation. Favored and available injury/weather flags offer equality conditions. No missing-value conditions. Numeric grid: '+', '.join(NUMERIC_FEATURES)+'.',
 'At least one condition must use a matchup/script/role feature; the prior-average gap is optional and can appear at most once. Keep only graded train cells with n>=30 and ROI>0. Pick highest ROI*n/(n+50); ties favor larger n, fewer conditions, then fixed grid order. Every tested/qualifying cell count and full-precision cutpoint is recorded in locked_rules.json.',
 'All RB overs require prior carry share >=60%, in addition to the 1–3 searched conditions. Missing position on overs, required values or valid price abstains. Statistics use $10 stakes before cross-rule player deduplication; hit rate excludes pushes. Injury/weather data are unavailable in train and yield no conditions. This expanded search remains exploratory and subject to selection overfit.',
 'Single-player and slip ordering remains directional prior-average gap, price, candidate ID, without outcomes; the gap is not an implicit eligibility filter.']
 for r in locked:
  phrases=[]
  for c in r['conditions']:
   name=NUMERIC_FEATURES.get(c['feature'],c['feature'])
   op={'le':'at most','ge':'at least','eq':'equal to'}[c['op']]
   phrases.append(f"{name} {op} {c['value']:.8g}")
  a=r['train'];desc.append(f"{r['market']} {r['side']}: "+' AND '.join(phrases)+f". Train n={a['n']}, wins/losses/pushes={a['wins']}/{a['losses']}/{a['pushes']}, hit={a['hit_pct']:.2f}%, P/L=${a['pl']:.2f}, ROI={a['roi']:.2f}%; shrinkage score={r['shrinkage_score']:.4f}.")
 for g in grids:
  if not any(r['market']==g['market'] and r['side']==g['side'] for r in locked):desc.append(f"{g['market']} {g['side']}: no qualifying cell; no bets.")
 if write: (HERE/'RULES.md').write_text('\n\n'.join(desc)+'\n')
 return cfg

def one_player(x):
 return x.sort_values(['week','model_edge','price','candidate_id'],ascending=[True,False,False,True]).drop_duplicates(['week','player']).copy()
def passing(x):
 cfg=json.loads((HERE/'locked_rules.json').read_text());q=pd.Series(False,index=x.index)
 for r in cfg['rules']:q |= mask(x,r)
 return one_player(x[q])
def slips(x):
 for week,z in one_player(x).groupby('week'):
  pool=z.to_dict('records');number=0
  while len(pool)>=3:
   selected=[];counts={}
   for r in pool:
    if counts.get(r['game_id'],0)<2:
     selected.append(r);counts[r['game_id']]=counts.get(r['game_id'],0)+1
    if len(selected)==4:break
   if len(selected)<3:break
   number+=1;yield week,number,selected
   ids={r['candidate_id'] for r in selected};pool=[r for r in pool if r['candidate_id'] not in ids]
