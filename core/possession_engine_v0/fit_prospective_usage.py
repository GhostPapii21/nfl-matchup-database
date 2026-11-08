"""Offline, guarded DAL/IND W1–8 fit; writes only to explicit output directory."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import pandas as pd


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n')


def evidence(n):
    return {'sample_size': n, 'flags': ['SPARSE_STATE', 'LOW-SAMPLE'] if n < 30 else [],
            'uncertainty': {'method': 'empirical_multinomial_plugin; Wilson95 per category',
                            'independent_unit': 'play; within-game dependence not adjusted',
                            'predictive_validation': 'NOT_MEASURED'}}


def distribution(values):
    counts=Counter(json.dumps(v,sort_keys=True) for v in values); n=sum(counts.values()); rows=[]
    for v,k in sorted(counts.items()):
        p=k/n; z=1.96; den=1+z*z/n; mid=(p+z*z/(2*n))/den; rad=z*((p*(1-p)/n+z*z/(4*n*n))**.5)/den
        rows.append({'value':json.loads(v),'weight':k,'sample_size':k,'probability':p,'wilson95':[max(0,mid-rad),min(1,mid+rad)]})
    return rows


def fit(packet, out):
    out.mkdir(parents=True,exist_ok=True); inputs=out/'inputs'; inputs.mkdir(exist_ok=True)
    src=packet/'records/pbp_DAL_IND_w1_8.csv.gz'; raw=pd.read_csv(src,low_memory=False)
    assert raw.week.between(1,8).all() and (raw.season==2026).all()
    assert not raw.game_id.astype(str).str.contains('2026_09_DAL_IND|401873040').any()
    assert pd.to_datetime(raw.game_date).max() < pd.Timestamp('2026-11-06')
    assert ((raw.home_team.isin(['DAL','IND'])) | (raw.away_team.isin(['DAL','IND']))).all()
    # Adjacent PBP timestamps include inter-snap time; never cross game/quarter boundaries.
    nxt=raw.groupby(['game_id','qtr'],sort=False).game_seconds_remaining.shift(-1)
    raw['_elapsed']=raw.game_seconds_remaining-nxt
    counts={}; plays=[]
    for _,r in raw.iterrows():
        reason=None
        if r.posteam not in ('DAL','IND'): reason='opponent_offense_or_no_possession'
        elif r.down not in (1,2,3,4): reason='missing_down'
        elif any(r.get(k,0)==1 for k in ('penalty','fumble','lateral_reception','lateral_rush','return_touchdown','punt_blocked')): reason='unsupported_penalty_fumble_lateral_return_or_block'
        elif not (0 < r._elapsed <= 60): reason='missing_zero_or_over60_adjacent_clock'
        terminal=None; catch='NA'
        if reason is None:
            if r.punt_attempt==1: terminal='punt'
            elif r.field_goal_attempt==1 and r.field_goal_result in ('made','missed'): terminal='field_goal'
            elif r.qb_kneel==1: terminal='kneel'
            elif r.qb_spike==1: terminal='spike'
            elif r.sack==1: terminal='sack'
            elif r.qb_scramble==1: terminal='scramble'
            elif r.play_type=='run': terminal='designed_rush'
            elif r.play_type=='pass' and pd.notna(r.receiver_player_id):
                terminal='targeted_pass'; catch='INTERCEPTION' if r.interception==1 else 'COMPLETE' if r.complete_pass==1 else 'INCOMPLETE'
            elif r.play_type=='pass': terminal='other_untargeted_attempt'
            else: reason='unsupported_play_type'
        if reason: counts[reason]=counts.get(reason,0)+1; continue
        yards=int(r.yards_gained) if terminal in ('designed_rush','kneel','scramble','sack') or catch=='COMPLETE' else 0
        outcome={'yards':yards,'elapsed_seconds':int(r._elapsed)}
        if terminal=='punt':
            if pd.isna(r.kick_distance): counts['missing_punt_distance']=counts.get('missing_punt_distance',0)+1; continue
            outcome['punt_net_yards']=int(r.kick_distance-(r.return_yards if pd.notna(r.return_yards) else 0))
            if outcome['punt_net_yards'] < 0:
                counts['unsupported_negative_punt_net']=counts.get('unsupported_negative_punt_net',0)+1
                continue
        if terminal=='field_goal': outcome['made']=r.field_goal_result=='made'
        plays.append({'team_id':r.posteam,'down':int(r.down),'terminal':terminal,'catch':catch,'outcome':outcome,'game_id':r.game_id,'play_id':int(r.play_id)})
    d=pd.DataFrame(plays); model=json.loads((packet/'inputs/model.json').read_text()); before={'sample_size':model['sample_size'],'usage_cells':len(model['usage_cells']),'outcome_cells':len(model['outcome_cells'])}
    model.update(model_version='dal-ind-w1-8-empirical-v1',sample_size=len(d),sample_size_reason='Retained supported DAL/IND offensive plays; exclusions in training_evidence.json',provenance_refs=['model','registry'])
    model['flags']=[x for x in model['flags'] if x!='EMPIRICAL_USAGE_PENDING']+['EMPIRICAL_PARTIAL_SEMANTICS','COARSE_DOWN_STATE','CLOCK_PROXY','ROLES_DEPTH_ONLY','NO_OUT_OF_SAMPLE_VALIDATION']
    model['usage_cells']=[]
    for team in ('DAL','IND'):
        for down in range(1,5):
            s=d[(d.team_id==team)&(d.down==down)]; assert len(s)
            model['usage_cells'].append({'cell_id':f'{team}_down{down}','when':{'team_id':team,'down':down},'terminals':distribution(s.terminal),**evidence(len(s)),'pooling':'NONE across teams; distance/field/score/period deliberately unconditioned'})
    targeted=d[d.terminal=='targeted_pass']
    model['catch_distributions']={'targeted_pass':distribution(targeted['catch'])}
    model['catch_evidence']={'targeted_pass':{**evidence(len(targeted)),'pooling':'EXPLICIT DAL+IND offensive targeted attempts; API supports terminal-only catch distribution'}}
    model['outcome_cells']=[]
    for (team,term,catch),s in d.groupby(['team_id','terminal','catch'],sort=True):
        when={'team_id':team,'terminal':term}
        if term=='targeted_pass': when['catch']=catch
        model['outcome_cells'].append({'cell_id':f'{team}_{term}_{catch}','when':when,'distribution':distribution(s.outcome),**evidence(len(s)),'pooling':'NONE across teams; down/distance/field/score unconditioned'})
    # Global catch API can select a catch absent for a team; reject instead of fallback.
    for team in ('DAL','IND'):
        assert set(targeted['catch'])==set(targeted[targeted.team_id==team]['catch'])
    model['training_source']={'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'path':str(src),'weeks':[1,8],'cutoff_utc':'2026-11-06T12:40:00Z'}
    for key in ('registry','splits','run_spec'):
        (inputs/f'{key}.json').write_bytes((packet/f'inputs/{key}.json').read_bytes())
    from fit_prospective_roles import fit_roles
    role_evidence=fit_roles(raw,model,json.loads((inputs/'registry.json').read_text()))
    dump(out/'role_training_evidence.json',role_evidence)
    dump(inputs/'model.json',model)
    ev={'source':model['training_source'],'input_rows':len(raw),'retained_rows':len(d),'exclusions':counts,'training_game_ids':sorted(d.game_id.unique()),'before':before,'after':{'sample_size':len(d),'usage_cells':len(model['usage_cells']),'outcome_cells':len(model['outcome_cells'])},'cells':[{k:v for k,v in c.items() if k not in ('distribution','terminals')} for c in model['usage_cells']+model['outcome_cells']],'leakage_checks':'PASS: season2026 weeks1-8, game dates before cutoff, DAL/IND involved only; no target game or market read','limitations':['Clock proxy excludes zero/missing/>60s; selection bias','Penalties/fumbles/laterals/returns excluded; no official rules integration','Rotation fitted separately in role_training_evidence.json; target depth/try point weights remain prior model','Usage/outcome counts and Wilson intervals are descriptive; role-only W7-8 heldout evaluation is separate; game correlation and model bias not covered']}
    dump(out/'training_evidence.json',ev)
    dump(out/'training_records.json',plays)
    return ev

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();print(json.dumps(fit(a.packet,a.output)['after']))
