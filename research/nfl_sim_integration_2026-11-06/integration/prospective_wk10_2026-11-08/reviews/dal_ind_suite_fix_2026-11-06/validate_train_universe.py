"""Additional W6 validation: universe frozen from W1-5 observed role IDs only.
No target-date availability, W6 identities or W7-8 records define eligibility.
Never selects or tunes candidates; tests the locked selection.
"""
import json,math
from collections import Counter
from pathlib import Path
import pandas as pd
H=Path(__file__).resolve().parent;E=H.parents[1]
raw=pd.read_parquet('/workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08/raw/play_by_play_2026.parquet')
registry=json.loads((E/'runs/dal_ind_usage_fit/inputs/registry.json').read_text());legacy=json.loads((E/'runs/dal_ind_usage_fit/inputs/model.json').read_text())
refs={p['record_id']:p['player_id'] for p in registry['players']}
selected=json.loads((H/'SELECTION_LOCK.json').read_text())['selected'];out=[]
for team in ['DAL','IND']:
 for role,column in [('passer','passer_player_id'),('target','receiver_player_id'),('carry','rusher_player_id')]:
  s=raw[(raw.season==2026)&(raw.posteam==team)]
  train=Counter(s[s.week.between(1,5)][column].dropna());universe=sorted(train)+['UNSEEN_IN_TRAIN'];k=len(universe);n=sum(train.values())
  truth=Counter(x if x in train else 'UNSEEN_IN_TRAIN' for x in s[s.week==6][column].dropna());nt=sum(truth.values())
  old={refs.get(r,r):w for r,w in legacy['role_states'][team][0]['value']['rotation_weights'][role].items()}
  metrics={}
  for name in ['equal_eligible','legacy_depth',selected]:
   if name=='equal_eligible':p={r:1/k for r in universe}
   elif name=='legacy_depth':
    p={r:old.get(r,0)+1e-6 for r in universe};z=sum(p.values());p={r:v/z for r,v in p.items()}
   else:
    lam=0.25;p={r:(1-lam)*(train[r]+1e-6)/(n+1e-6*k)+lam/k for r in universe}
   metrics[name]=dict(kl=sum(v/nt*math.log((v/nt)/p[r]) for r,v in truth.items()),mae=sum(abs(truth[r]/nt-p[r]) for r in universe)/k)
  out.append(dict(team=team,role=role,train_n=n,hold_n=nt,unseen_hold_count=truth['UNSEEN_IN_TRAIN'],metrics=metrics))
result=dict(protocol='train W1-5; hold W6; TRAIN_ONLY_IDENTITY_UNIVERSE; unseen heldout IDs pooled into predefined UNSEEN_IN_TRAIN bucket; no target-date availability filter',selected_previously=selected,used_for_selection=False,cells=out)
(H/'train_only_universe_validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(next(r for r in out if r['team']=='IND' and r['role']=='carry'),indent=2))
