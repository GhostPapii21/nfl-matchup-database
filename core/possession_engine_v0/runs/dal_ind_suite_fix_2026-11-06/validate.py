"""Offline preregistered selection, immutable source copies, paired common random runs."""
import sys,json,hashlib,copy,math,shutil
from pathlib import Path
from collections import Counter
import pandas as pd
HERE=Path(__file__).resolve().parent; ENGINE=HERE.parents[1];sys.path.insert(0,str(ENGINE))
from fit_prospective_roles import ROLES
from joint_producer import simulate_joint_games
from shared_accounting import shared_projection
PACKET=Path('/workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08')
OLD=ENGINE/'runs/dal_ind_roles_unify'; LEG=ENGINE/'runs/dal_ind_usage_fit'
protocol=json.loads((HERE/'ROLE_POLICY_PREREGISTRATION.json').read_text())
raw=pd.read_parquet(PACKET/'raw/play_by_play_2026.parquet')
model=json.loads((OLD/'inputs/model.json').read_text());registry=json.loads((OLD/'inputs/registry.json').read_text());legacy=json.loads((LEG/'inputs/model.json').read_text())
# Capture counts now: closures otherwise bind the final loop variables.
cells=[]
for team,rows in model['role_states'].items():
 for role,(column,positions) in ROLES.items():
  refs={p['player_id']:p['record_id'] for p in registry['players'] if p['record_id'] in rows[0]['value']['available'] and p['position'] in positions}
  weekly={w:Counter(refs[x] for x in raw[(raw.posteam==team)&(raw.week==w)][column].dropna() if x in refs) for w in range(1,9)}
  cells.append((team,role,list(refs.values()),weekly,legacy['role_states'][team][0]['value']['rotation_weights'][role]))
def predict(cell,weeks,name):
 team,role,refs,weekly,old=cell;c=sum((weekly[w] for w in weeks),Counter());n=sum(c.values());k=len(refs)
 if name=='empirical_recent_2':c=sum((weekly[w] for w in weeks[-2:]),Counter());n=sum(c.values())
 if name=='equal_eligible':p={r:1/k for r in refs}
 elif name=='legacy_depth':p={r:old.get(r,0)+1e-6 for r in refs}
 else:
  strength=float(name.split('_')[-1]) if name.startswith('dirichlet_') else k*1e-6
  p={r:(c[r]+strength/k)/(n+strength) for r in refs}
  if name.startswith('mix_equal_'):
   lam=float(name.split('_')[-1]);p={r:(1-lam)*v+lam/k for r,v in p.items()}
 z=sum(p.values());return {r:v/z for r,v in p.items()}
def evaluate(train,hold):
 result={}
 for name in protocol['candidates']:
  result[name]=[]
  for cell in cells:
   team,role,refs,weekly,_=cell;p=predict(cell,train,name);c=sum((weekly[w] for w in hold),Counter());n=sum(c.values());truth={r:c[r]/n for r in refs} if n else {}
   result[name].append(dict(team=team,role=role,n=n,kl=sum(v*math.log(v/p[r]) for r,v in truth.items() if v) if n else None,mae=sum(abs(v-p[r]) for r,v in truth.items())/len(refs) if n else None))
 return result
dev=evaluate([1,2,3],[4,5]);selected=min(dev,key=lambda x:(max(r['kl'] for r in dev[x] if r['n']),sum(r['mae'] for r in dev[x] if r['n']),x))
(HERE/'SELECTION_LOCK.json').write_text(json.dumps({'selected':selected,'dev':dev},indent=2))
audit=evaluate([1,2,3,4,5],[6]);inspected=evaluate([1,2,3,4,5,6],[7,8])
def ind(result,name):return next(r for r in result[name] if r['team']=='IND' and r['role']=='carry')
gate=all(ind(audit,selected)[m] < min(ind(audit,b)[m] for b in ['equal_eligible','legacy_depth']) for m in ['kl','mae']) and ind(inspected,selected)['kl']<=ind(inspected,'equal_eligible')['kl']+0.5
policy=selected if gate else 'equal_eligible'
(HERE/'role_policy_metrics.json').write_text(json.dumps(dict(selected_on_dev=selected,accepted_policy=policy,gate_passed=gate,validation=audit,INSPECTED_HOLDOUT=inspected,flags=['EMPIRICAL_IND_CARRY_REGRESSION','ROLES_POLICY_ROBUST']),indent=2))
entries=json.loads((LEG/'inputs_manifest_entries.json').read_text());spec=json.loads((OLD/'inputs/run_spec.json').read_text())
runs={}
for label in ['equal_depth','empirical','selected_robust']:
 dest=HERE/'inputs'/label;dest.mkdir(parents=True,exist_ok=True)
 for filename in ['registry.json','splits.json','run_spec.json']:shutil.copyfile(OLD/'inputs'/filename,dest/filename)
 m=copy.deepcopy(model)
 m['flags']=[f for f in m.get('flags',[]) if f not in ['EMPIRICAL_ROLES','TEAM_PRIOR_DIRICHLET_HALF_SHRINKAGE_20']]+['EMPIRICAL_IND_CARRY_REGRESSION','ROLE_POLICY_SENSITIVITY_RESEARCH']
 for cell in cells:
  team,role,*_=cell
  for row in m['role_states'][team]:
   state=row['value'];state.pop('rotation_by_half',None);state.pop('role_evidence',None)
   state['role_policy_evidence']={'protocol_ref':'ROLE_POLICY_PREREGISTRATION.json','selection_lock_ref':'SELECTION_LOCK.json','candidate_selected_on_dev':'mix_equal_0.25','empirical_unshrunk_status':'EMPIRICAL_IND_CARRY_REGRESSION','same_set_validation_claim':False}
   if label!='empirical':state['rotation_weights'][role]=predict(cell,list(range(1,9)),'equal_eligible' if label=='equal_depth' else policy)
 m['role_efficiency_coupling']=False
 (dest/'model.json').write_text(json.dumps(m,sort_keys=True))
 run=simulate_joint_games(spec,input_root=dest,inputs=entries,n=5,seed=20261108,output_root=HERE/'forecasts'/label)
 repeat=simulate_joint_games(spec,input_root=dest,inputs=entries,n=5,seed=20261108,output_root=HERE/'forecasts'/label)
 assert run==repeat
 for t in run['trials']:
  p=shared_projection(t);assert p['team_periods']==t['team_periods'];assert p['player_periods']==t['player_periods'];assert t['validation']['status']=='PASS'
 runs[label]=run
base=runs['equal_depth']['trials']
for label,run in runs.items():
 assert [[(r['team_id'],r['period_id'],r['stats']) for r in t['team_periods']] for t in run['trials']]==[[(r['team_id'],r['period_id'],r['stats']) for r in t['team_periods']] for t in base],label
summary={label:dict(n_completed=r['n_completed'],forecast_id=r['forecast_id'],score_means={team:sum(t['status']['terminal_state']['score'][team] for t in r['trials'])/5 for team in ['DAL','IND']},conservation_failures=0,seeded_repeat_identical=True) for label,r in runs.items()}
(HERE/'paired_runs.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
