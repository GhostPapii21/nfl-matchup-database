"""SHARED_ACCOUNTING_V1: empirical-model joint events are the sole credit authority.

Adapter does not reconcile or relabel legacy independent yard-row simulations.
"""
from copy import deepcopy
from joint_accounting import derive_tables, validate_trial

def shared_projection(trial):
    periods=list(dict.fromkeys(e['period_id'] for e in trial['events']))
    team,player,aggregates=derive_tables(trial['events'],trial['game'],trial['provenance']['roster'],periods,complete=trial['status']['state']=='COMPLETE')
    if (team,player,aggregates)!=(trial['team_periods'],trial['player_periods'],trial['aggregates']):
        raise ValueError('shared derive_tables mismatch')
    validation=validate_trial(trial)
    if validation['status']!='PASS':
        raise ValueError('shared accounting validation failed')
    validation={k:v for k,v in validation.items() if k!='checks'}
    ledger=[]
    by_id={(p['team_id'],p['player_id_namespace'],p['player_id']):p['record_id'] for p in trial['provenance']['roster']}
    for event in trial['events']:
        for p in event['player_credits']:
            ledger.append({'event_id':event['event_id'],'period_id':event['period_id'],'record_id':by_id[(p['team_id'],p['player_id_namespace'],p['player_id'])], 'team_id':p['team_id'],'stats':deepcopy(p['stats'])})
    return {'path_semantics':'SHARED_ACCOUNTING_V1','forecast_id':trial['forecast_id'],'trial_id':trial['trial_id'],'rng':deepcopy(trial['rng']), 'opportunity_ledger':ledger,'team_periods':team,'player_periods':player,'aggregates':aggregates,'validation':validation,'provenance_refs':['model','registry']}
