import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('research/possession_engine_v0').resolve()))
from joint_producer import simulate_joint_games
from joint_inputs import freeze_run
p=Path('/workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08'); out=Path('research/possession_engine_v0/runs/dal_ind_usage_fit').resolve()
entries=json.loads((out/'inputs_manifest_entries.json').read_text())
spec=json.loads((out/'inputs/run_spec.json').read_text()); seed=20261108
results=[]
for label,root in [('before',out/'baseline_inputs'),('after',out/'inputs'),('repeat',out/'inputs')]:
    result=simulate_joint_games(spec,input_root=root,inputs=entries,n=5,seed=seed,output_root=out/('baseline_n5' if label=='before' else 'joint_producer_n5'))
    trials=result.pop('trials'); scores=[]
    for t in trials:
        scores.append(t['status']['terminal_state']['score'])
    means={team:sum(s[team] for s in scores)/5 for team in ('DAL','IND')}
    result.update(label=label,seed=str(seed),score_means=means,scores=scores,trial_seeds=[t['rng']['trial_seed'] for t in trials],validations=[t['validation']['status'] for t in trials])
    results.append(result)
    print(label,result['forecast_id'],means,flush=True)
assert results[1]['forecast_id']==results[2]['forecast_id'] and results[1]['score_means']==results[2]['score_means']
(out/'reproducibility.json').write_text(json.dumps({'runs':results,'identical_forecast_id_and_score_means':True},indent=2)+'\n')
(out/'inputs_manifest_entries.json').write_text(json.dumps(entries,indent=2)+'\n')
