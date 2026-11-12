"""Stage A structural and train-only checks. Never settles holdout."""
import json
from pathlib import Path
import pandas as pd
import rules
HERE=Path(__file__).resolve().parent

def main():
 c=pd.read_csv(HERE/'candidates.csv');x=pd.read_csv(HERE/'legs.csv')
 assert c.tier.eq('main').all()
 assert not x.duplicated(['week','player','market','side']).any()
 assert x.candidate_id.is_unique
 h=x[x.week>=7]
 assert h.result.eq('withheld').all()
 assert h[['result_stat','pl','stake']].isna().all().all()
 assert not any((HERE/f).exists() for f in ['grading_holdout.csv','results.md','selected_singles.csv','selected_slips.csv'])
 for _,z in c.groupby(['week','player','market','side']):
  leg=x[(x.week==z.week.iloc[0])&(x.player==z.player.iloc[0])&(x.market==z.market.iloc[0])&(x.side==z.side.iloc[0])].iloc[0]
  assert leg.line==z.line.median()
  price=z[z.line==leg.line].price.median()
  assert (pd.isna(price) and pd.isna(leg.price)) or abs(price-leg.price)<1e-9
 train=x[x.week<=6]
 for r in json.loads((HERE/'locked_rules.json').read_text())['rules']:
  z=train[(train.market==r['market'])&(train.side==r['side'])&(train.model_edge>=r['min_model_edge'])&train.result.isin(['win','loss','push'])]
  assert len(z)==r['train_n']>=30
  assert z.pl.sum()>0
  assert abs(100*z.pl.sum()/z.stake.sum()-r['train_roi'])<1e-7
 for variant in ['baseline','edgecap']:
  for sharp in [False,True]:
   z=rules.passing(x,sharp,variant)
   assert not z.duplicated(['week','player']).any()
   if variant=='edgecap':assert (z.model_edge<=15).all()
   used=set()
   for week,_,legs in rules.slips(z):
    assert 3<=len(legs)<=4
    assert pd.Series([r['game_id'] for r in legs]).value_counts().max()<=2
    for r in legs:
     key=(week,r['player']);assert key not in used;used.add(key)
 print('Stage A validation passed: main-only, consensus, train lock, player/game caps, holdout withheld.')
if __name__=='__main__':main()
