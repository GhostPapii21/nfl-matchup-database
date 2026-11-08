"""Offline same-clock n=5 fit + shared accounting/reproducibility audit."""
import json,sys
from pathlib import Path
from collections import Counter
ENGINE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ENGINE))
from joint_producer import simulate_joint_games
from shared_accounting import shared_projection
from joint_inputs import canonical
out=Path(__file__).resolve().parent
old=ENGINE/'runs/dal_ind_usage_fit'
entries=json.loads((old/'inputs_manifest_entries.json').read_text())
spec=json.loads((out/'inputs/run_spec.json').read_text())
results=[]
for label,root in [('equal_depth_before',old/'inputs'),('empirical_after',out/'inputs'),('repeat',out/'inputs')]:
    result=simulate_joint_games(spec,input_root=root,inputs=entries,n=5,seed=20261108,output_root=out/('before_n5' if label=='equal_depth_before' else 'joint_shared_n5'))
    projections=[shared_projection(t) for t in result['trials']]
    means=Counter()
    for p in projections:
        for row in p['opportunity_ledger']:
            for stat in ('targets','carries','pass_attempts'):
                means[row['record_id']+'/'+stat]+=row['stats'][stat]/5
    summary={'label':label,'forecast_id':result['forecast_id'],'artifact_directory':result['artifact_directory'],'score_means':{team:sum(t['status']['terminal_state']['score'][team] for t in result['trials'])/5 for team in ('DAL','IND')},'player_opportunity_means':dict(means),'conservation_fail_count':sum(t['validation']['status']!='PASS' for t in result['trials']),'shared_bridge_fail_count':sum(p['team_periods']!=t['team_periods'] or p['player_periods']!=t['player_periods'] for p,t in zip(projections,result['trials'])),'n_completed':result['n_completed']}
    results.append(summary)
    if label=='empirical_after':
        (out/'shared_projections.jsonl').write_bytes(b'\n'.join(canonical(p) for p in projections)+b'\n')
    print(label,summary['forecast_id'],summary['score_means'],flush=True)
assert all(results[1][k]==results[2][k] for k in ('forecast_id','score_means','player_opportunity_means'))
roles=json.loads((out/'role_training_evidence.json').read_text())
metrics={'NFL-16':{'status':'RESEARCH_ONLY','runs':results,'roles':roles,'seeded_repeat_identical':True},'phase15':'NOT_YET','quotes':'NOLINE','100k':'DEFERRED_100K_UNFINISHED_SEMANTICS'}
(out/'completion_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
