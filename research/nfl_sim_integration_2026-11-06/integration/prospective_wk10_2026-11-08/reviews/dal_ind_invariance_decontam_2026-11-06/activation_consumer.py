import sys,json
from pathlib import Path
tree=Path(sys.argv[1]);sys.path.insert(0,str(tree/'engine_source'))
from joint_inputs import freeze_run,digest,verify_frozen
from joint_producer import simulate_trial
r=json.loads((tree/'run_spec.json').read_text());e=json.loads((tree/'input_manifest.json').read_text())['entries']
first=json.loads((tree/'trials.jsonl').read_text().splitlines()[0]);spec={**r['spec'],**{k:first['freeze'][k] for k in ['frozen_at_utc','generated_at_utc']}}
f=freeze_run(spec,tree/'inputs',e,n=len(r['trial_indices']),seed=int(r['rng']['seed']))
assert f['run_spec']['engine']['source_content_hash']==r['engine']['source_content_hash']
assert f['run_spec']['engine']['dependencies']==r['engine']['dependencies']
# Relocation changes local git patch discovery, not frozen source bytes. Restore recorded packaging identity only.
f['run_spec']['engine']=r['engine'];f['forecast_id']=digest(f['run_spec']);verify_frozen(f)
assert f['forecast_id']==tree.name.replace('sha256_','sha256:')
ts=[simulate_trial(f,i) for i in r['trial_indices']]
original=[json.loads(x) for x in (tree/'trials.jsonl').read_text().splitlines()]
assert json.loads(json.dumps(ts))==original
print(json.dumps({'forecast_id':f['forecast_id'],'trials_exact':True,'team_means':{k:sum(t['status']['terminal_state']['score'][k] for t in ts)/len(ts) for k in ['DAL','IND']}}))
