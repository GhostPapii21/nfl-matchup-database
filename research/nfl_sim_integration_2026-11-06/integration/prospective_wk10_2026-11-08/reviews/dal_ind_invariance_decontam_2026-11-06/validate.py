"""Decontaminated offline validator. All writes confined to this new run."""
import sys,json,hashlib,copy,runpy
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent; ENGINE=HERE.parents[1]
sys.path.insert(0,str(ENGINE))
import pandas as pd
from joint_inputs import freeze_run
from joint_producer import simulate_trial,OpportunityModel
OLD=ENGINE/'runs/dal_ind_suite_fix_2026-11-06'
PACKET=Path('/workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08')
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def protected():
 return {str(p):sha(p) for p in ENGINE.rglob('*') if p.is_file() and HERE not in p.parents and '__pycache__' not in str(p) and (any(x.startswith('sha256_') for x in p.parts) or any(x in p.parts for x in ['certified_asof','dal_ind_roles_unify','dal_ind_usage_fit','dal_ind_suite_fix_2026-11-06']))}
before=protected();write('PROTECTED_BEFORE_HASHES.json',before)
# Execute only historical selection/evaluation definitions, never its contaminated gate or writes.
source=(OLD/'validate.py').read_text();prefix=source[:source.index('dev=evaluate')]
prefix=prefix.replace("HERE=Path(__file__).resolve().parent; ENGINE=HERE.parents[1];sys.path.insert(0,str(ENGINE))", "HERE=OLD; ENGINE=OLD.parents[1];sys.path.insert(0,str(ENGINE))")
ns={'__file__':str(__file__),'OLD':OLD};exec(compile(prefix,str(OLD/'validate.py'),'exec'),ns)
dev=ns['evaluate']([1,2,3],[4,5]);selected=min(dev,key=lambda x:(max(r['kl'] for r in dev[x] if r['n']),sum(r['mae'] for r in dev[x] if r['n']),x))
assert selected=='mix_equal_0.25'
write('role_policy_metrics.json',{'selected_on_dev':selected,'dev':dev,'W6_SECONDARY_AUDIT_NOT_PROMOTION':ns['evaluate']([1,2,3,4,5],[6]),'INSPECTED_DEV_REPORTING_ONLY':ns['evaluate']([1,2,3,4,5,6],[7,8]),'promotion_gate':None,'accepted_policy':None,'status':'RESEARCH_PROVISIONAL_NOT_PROMOTED','flags':['EMPIRICAL_IND_CARRY_REGRESSION']})
entries=json.loads((ENGINE/'runs/dal_ind_usage_fit/inputs_manifest_entries.json').read_text())
spec=json.loads((OLD/'inputs/selected_robust/run_spec.json').read_text())
models={}; roots={}
for policy in ['equal_eligible','mix_equal_0.25','empirical_mle','legacy_depth']:
 root=HERE/'inputs'/policy;root.mkdir(parents=True,exist_ok=True)
 for name in ['registry.json','splits.json','run_spec.json']:(root/name).write_bytes((OLD/'inputs/selected_robust'/name).read_bytes())
 m=copy.deepcopy(ns['model']);m['role_efficiency_coupling']=False
 for cell in ns['cells']:
  team,role,*_=cell
  for row in m['role_states'][team]:
   row['value'].pop('rotation_by_half',None);row['value']['rotation_weights'][role]=ns['predict'](cell,list(range(1,9)),policy)
 (root/'model.json').write_text(json.dumps(m,sort_keys=True));models[policy]=m;roots[policy]=root
# Same outcome and usage cells; only role attribution differs.
assert all(m['usage_cells']==models['equal_eligible']['usage_cells'] and m['outcome_cells']==models['equal_eligible']['outcome_cells'] for m in models.values())
seeds=[11,97,2026,20261108,987654];n=20;coverage=Counter();ot=[];different=0
for seed in seeds:
 baseline=None
 for policy,root in roots.items():
  f=freeze_run(spec,root,entries,n=n,seed=seed);paths=[];players=[]
  for i in range(n):
   t=simulate_trial(f,i);assert t['validation']['status']=='PASS'
   path={'team_periods':[(r['team_id'],r['period_id'],r['stats']) for r in t['team_periods']], 'terminal_state':t['status']['terminal_state'],'possessions':[sum(e['possession_id']==p['possession_id'] for e in t['events']) for p in t['possessions']], 'events':[(e['type'],e['terminal_category'],e['pre_state'],e['post_state'],e['team_credits'],e['boundary']) for e in t['events']]}
   paths.append(path);players.append([e['player_credits'] for e in t['events']])
   if policy=='equal_eligible':
    for e in t['events']:
     coverage[e['period_id']]+=1
     margin=e['pre_state']['score']['DAL']-e['pre_state']['score']['IND'];coverage['lead' if margin>0 else 'trail' if margin<0 else 'tied']+=1
     if e['boundary'] and e['boundary']['from_period_id'] is not None:coverage['period_transition']+=1
     if e['boundary'] and e['boundary']['cause']=='halftime':coverage['halftime_transition']+=1
    if t['status']['went_ot']:ot.append({'seed':seed,'trial':i})
  if baseline is None:baseline=(paths,players)
  else:assert paths==baseline[0],(seed,policy);different+=int(players!=baseline[1])
assert all(coverage[q]>0 for q in ['Q1','Q2','Q3','Q4','OT1','lead','trail','period_transition']),coverage
root=roots['equal_eligible'];m=copy.deepcopy(models['equal_eligible']);m['role_efficiency_coupling']=True
(root/'model.json').write_text(json.dumps(m,sort_keys=True))
try:simulate_trial(freeze_run(spec,root,entries,n=1,seed=11),0);raise AssertionError('coupling accepted')
except ValueError as e:assert 'UNSUPPORTED' in str(e)
(root/'model.json').write_text(json.dumps(models['equal_eligible'],sort_keys=True))
write('invariance_metrics.json',{'status':'PASS','seed_bases':seeds,'n_trials_per_seed_per_policy':n,'total_trials':len(seeds)*n*4,'policies':list(roots),'coverage_events':dict(coverage),'ot_trials':ot,'player_attribution_changed_comparisons':different,'negative_control':'UNSUPPORTED','assertions':['exact team period stats including scores/counts/yards','exact terminal states','exact event team paths and counts','possession sequence lengths'],'coupling':False})
# Descriptive materiality, no causal counterfactual claimed.
raw=pd.read_parquet(PACKET/'raw/play_by_play_2026.parquet');raw=raw[raw.week.between(1,8)]
mat={}
for label in ['league','DAL','IND']:
 d=raw if label=='league' else raw[(raw.home_team==label)|(raw.away_team==label)]
 pen=d.penalty.fillna(0).eq(1);otmask=d.qtr.gt(4);kick={}
 for name,col in [('punt','punt_attempt'),('kickoff','kickoff_attempt')]:
  k=d[d[col].fillna(0).eq(1)];v=k.return_yards
  kick[name]={'plays':len(k),'return_yards_known':int(v.notna().sum()),'return_yards_sum':float(v.sum()),'positive_return_plays':int(v.gt(0).sum()),'mean_return_yards_known':float(v.mean()) if v.notna().any() else None}
 mat[label]={'rows':len(d),'games':int(d.game_id.nunique()),'penalty_plays':int(pen.sum()),'penalty_rate_all_rows':float(pen.mean()),'penalty_yards_sum':float(d.loc[pen,'penalty_yards'].sum()),'penalty_no_play_rows':int((pen & d.play_type.eq('no_play')).sum()),'penalty_rows_touchdown_flag':int(d.loc[pen,'touchdown'].fillna(0).sum()),'ot_games':int(d.loc[otmask,'game_id'].nunique()),'ot_game_rate':float(d.loc[otmask,'game_id'].nunique()/d.game_id.nunique()),'ot_total_points':float(d.loc[otmask,'total_home_score'].max()) if False else None,'ot_touchdown_rows':int(d.loc[otmask,'touchdown'].fillna(0).sum()),'kicks':kick}
write('materiality_metrics.json',{'source':str(PACKET/'raw/play_by_play_2026.parquet'),'sha256':sha(PACKET/'raw/play_by_play_2026.parquet'),'filter':'week 1..8; team scopes include both sides of team games; league rows counted once','scopes':mat,'causal_score_impact':'NOT_IDENTIFIED_FROM_DESCRIPTIVE_PBP'})
# Reproduce the latest protected selected tree using its own frozen source in a separate process.
import subprocess,shutil
summary=json.loads((OLD/'paired_runs.json').read_text())['selected_robust'];tree=OLD/'forecasts/selected_robust'/summary['forecast_id'].replace(':','_')
staged=HERE/'activation/selected_robust'/tree.name
if not staged.exists():shutil.copytree(tree,staged)
consumer=HERE/'activation_consumer.py'
consumer.write_text('''import sys,json\nfrom pathlib import Path\ntree=Path(sys.argv[1]);sys.path.insert(0,str(tree/'engine_source'))\nfrom joint_inputs import freeze_run,digest,verify_frozen\nfrom joint_producer import simulate_trial\nr=json.loads((tree/'run_spec.json').read_text());e=json.loads((tree/'input_manifest.json').read_text())['entries']\nfirst=json.loads((tree/'trials.jsonl').read_text().splitlines()[0]);spec={**r['spec'],**{k:first['freeze'][k] for k in ['frozen_at_utc','generated_at_utc']}}\nf=freeze_run(spec,tree/'inputs',e,n=len(r['trial_indices']),seed=int(r['rng']['seed']))\nassert f['run_spec']['engine']['source_content_hash']==r['engine']['source_content_hash']\nassert f['run_spec']['engine']['dependencies']==r['engine']['dependencies']\n# Relocation changes local git patch discovery, not frozen source bytes. Restore recorded packaging identity only.\nf['run_spec']['engine']=r['engine'];f['forecast_id']=digest(f['run_spec']);verify_frozen(f)\nassert f['forecast_id']==tree.name.replace('sha256_','sha256:')\nts=[simulate_trial(f,i) for i in r['trial_indices']]\noriginal=[json.loads(x) for x in (tree/'trials.jsonl').read_text().splitlines()]\nassert json.loads(json.dumps(ts))==original\nprint(json.dumps({'forecast_id':f['forecast_id'],'trials_exact':True,'team_means':{k:sum(t['status']['terminal_state']['score'][k] for t in ts)/len(ts) for k in ['DAL','IND']}}))\n''')
p=subprocess.run([sys.executable,str(consumer),str(staged)],capture_output=True,text=True);write('activation_result.json',{'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stderr
external=json.loads((PACKET/'reviews/INVARIANCE_PASS_BEFORE_HASHES.json').read_text());write('EXTERNAL_BEFORE_HASH_CHECK.json',{p:sha(Path(p))==v['sha256'] for p,v in external['files'].items()})
after=protected();assert before==after;write('PROTECTED_HASH_CHECK.json',{'files':len(before),'all_unchanged':True})
print('PASS: invariance, decontamination, materiality, activation, protected hashes')
