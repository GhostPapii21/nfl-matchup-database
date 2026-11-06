"""Team-only empirical roles; no market or target-game inputs."""
from collections import Counter
import math

ROLES={'passer':('passer_player_id',{'QB'}),'target':('receiver_player_id',{'WR','TE','RB'}),'carry':('rusher_player_id',{'RB','QB'})}

def fit_roles(raw, model, registry):
    report={'protocol':'train W1-6; hold W7-8','prior':'team empirical -> half-state Dirichlet, strength 20; zero-count players retain zero mass','cells':[],'exclusions':[]}
    for team, rows in model['role_states'].items():
        active={p['record_id']:p for p in registry['players'] if p['team_id']==team and p['status']=='ACT' and p['availability'] in ('AVAILABLE','AVAILABLE_WITH_UNCERTAINTY')}
        for row in rows:
            state=row['value']; state['available']=sorted(active)
            legacy=state.get('rotation_weights',{})
            state['rotation_weights']={}; state['rotation_by_half']={str(h):{} for h in (1,2)}
            state['role_evidence']={}
            for role,(column,positions) in ROLES.items():
                eligible={p['player_id']:ref for ref,p in active.items() if p['position'] in positions}
                s=raw[raw.posteam==team]
                excluded=s[column].dropna(); excluded=excluded[~excluded.isin(eligible)]
                report['exclusions'].append({'team':team,'role':role,'count':len(excluded),'reason':'not ACT/available or position-ineligible; missing IDs excluded'})
                def counts(frame):
                    return Counter(eligible[x] for x in frame[column].dropna() if x in eligible)
                allc=counts(s); n=sum(allc.values())
                prior={ref:allc.get(ref,0)/n for ref in eligible.values()} if n else {'UNASSIGNED':1.0}
                state['rotation_weights'][role]=prior
                halves={}
                for half in (1,2):
                    c=counts(s[(s.qtr<=2) if half==1 else (s.qtr>2)]); size=sum(c.values())
                    weights={ref:(c.get(ref,0)+20*p)/(size+20) for ref,p in prior.items()}
                    state['rotation_by_half'][str(half)][role]=weights
                    halves[str(half)]={'sample_size':size,'posterior_alpha':{ref:c.get(ref,0)+20*p for ref,p in prior.items()},'flags':['SPARSE_STATE','LOW-SAMPLE'] if size<30 else []}
                metrics={}
                for label,train,test in [('same_set',s,s),('heldout',s[s.week<=6],s[s.week>=7])]:
                    a,b=counts(train),counts(test); na,nb=sum(a.values()),sum(b.values()); refs=list(prior)
                    if not na or not nb: metrics[label]={'status':'LOW-SAMPLE','train_n':na,'test_n':nb}; continue
                    # Evaluation floor only, explicitly avoids infinite KL for unseen heldout players.
                    predictions={'equal':{r:1/len(refs) for r in refs},'empirical':{r:(a.get(r,0)+1e-6)/(na+1e-6*len(refs)) for r in refs}}
                    old=legacy.get(role,{})
                    normalizer=sum(old.get(r,0)+1e-6 for r in refs)
                    predictions['legacy_depth']={r:(old.get(r,0)+1e-6)/normalizer for r in refs}
                    metrics[label]={'train_n':na,'test_n':nb,'evaluation_floor':1e-6}
                    for name,pred in predictions.items():
                        truth={r:b.get(r,0)/nb for r in refs}
                        metrics[label][name]={'kl':sum(v*math.log(v/pred[r]) for r,v in truth.items() if v),'mae':sum(abs(truth[r]-pred[r]) for r in refs)/len(refs)}
                ev={'team':team,'role':role,'sample_size':n,'shrinkage_strength':20,'uncertainty':'Dirichlet posterior conditional on team empirical prior; zero prior mass fixed; within-game correlation unadjusted','halves':halves,'metrics':metrics}
                state['role_evidence'][role]=ev; report['cells'].append(ev)
    model['flags']=[x for x in model['flags'] if x!='ROLES_DEPTH_ONLY'] if 'flags' in model else []
    model['flags']+=['EMPIRICAL_ROLES','TEAM_PRIOR_DIRICHLET_HALF_SHRINKAGE_20']
    model['provenance_refs']=['model','registry']
    return report
