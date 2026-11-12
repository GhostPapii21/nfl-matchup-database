"""Stage A audit only: no holdout outcome access."""
from pathlib import Path
import hashlib,json,ast
import pandas as pd
import rules
from build import summary
O=Path(__file__).resolve().parent
x=pd.read_csv(O/'features.csv');v=pd.read_csv(O.parent/'v2/legs.csv',usecols=['candidate_id','week','player','market','side','line','price'])
assert len(x)==len(v) and set(x.candidate_id)==set(v.candidate_id)
a=x.set_index('candidate_id');b=v.set_index('candidate_id');pd.testing.assert_frame_equal(a[b.columns].sort_index(),b.sort_index(),check_dtype=False)
assert not x.duplicated(['week','player','market','side']).any()
h=x[x.week>=7];assert h.result.eq('withheld').all() and h[['result_stat','pl','stake']].isna().all().all()
assert not any('HINDSIGHT' in c for c in x)
assert (x.feature_cutoff=='weeks<'+x.week.astype(str)).all()
cfg=json.loads((O/'locked_rules.json').read_text())
# Independently replay every pre-specified cell on train only, including winner selection.
assert rules.fit(x[x.week.between(3,6)].copy(),write=False)==cfg
for r in cfg['rules']:
 assert 1<=len(r['conditions'])<=3
 features=[c['feature'] for c in r['conditions']]
 assert len(features)==len(set(features)) and any(f!='model_edge' for f in features)
 assert features.count('model_edge')<=1
 assert abs(r['shrinkage_score']-r['train']['roi']*r['train']['n']/(r['train']['n']+50))<1e-8
for r in cfg['rules']:
 q=x[(x.week<=6)&rules.mask(x,r)&x.result.isin(['win','loss','push'])]
 s=summary(q,['market','side']).iloc[0]
 assert len(q)>=30 and s.roi>0
 for c in ['n','wins','losses','pushes','hit_pct','pl','roi']:assert abs(float(s[c])-r['train'][c])<1e-8
q=rules.passing(x)
assert not q.duplicated(['week','player']).any()
rb=q[(q.position=='RB')&(q.side=='over')];assert rb.prior_carry_share.ge(.6).all()
for _,_,legs in rules.slips(q):
 assert 3<=len(legs)<=4 and len({r['player'] for r in legs})==len(legs)
 assert max(pd.Series([r['game_id'] for r in legs]).value_counts())<=2
for f in ['build.py','rules.py','grade.py']:ast.parse((O/f).read_text())
assert not (O/'results.md').exists() and not (O/'selected_singles.csv').exists()
expected=json.loads((O/'frozen_sha256.json').read_text());assert all(hashlib.sha256((O/f).read_bytes()).hexdigest()==v for f,v in expected.items())
print(f'PASS: {len(x)} original consensus legs; {len(cfg["rules"])} qualifying train rules; holdout withheld; RB carry guard; singles/slip constraints; frozen hashes; grade.py parsed only.')
