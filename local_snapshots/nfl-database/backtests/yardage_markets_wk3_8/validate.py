from pathlib import Path
import json
import pandas as pd
P=Path(__file__).resolve().parent
x=pd.read_csv(P/'candidates.csv')
assert x.candidate_id.is_unique
assert x.week.between(3,8).all()
assert set(x.market)<= {'rushyds','recyds','rushrecyds'}
assert (pd.to_datetime(x.snap,format='mixed',utc=True)<=pd.to_datetime(x.kickoff,format='mixed',utc=True)).all()
assert (x.feature_cutoff=='weeks<'+x.week.astype(str)).all()
assert ((x.result_stat[x.result=='win']>x.line[x.result=='win'])==(x.side[x.result=='win']=='over')).all()
assert (x.pl[x.result=='loss']==-10).all()
for r in json.loads((P/'locked_rules.json').read_text()):
 z=x[(x.week<=6)&(x.market==r['market'])&(x.side==r['side'])&(x.tier==r['tier'])&(x.form_edge>=r['min_form_edge'])&(x.result!='ungraded')]
 assert len(z)==r['train_n']>=15
 assert abs(100*z.pl.sum()/z.stake.sum()-r['train_roi'])<1e-8
print('Candidate, timestamp, grading, and training-rule checks passed:',len(x))
