"""Regression tests for missing inputs, paired paths, and declared rule limits."""
import copy
import numpy as np
import pytest
from empirical import lookup_plays, StateKey
from joint_inputs import freeze_run
from joint_producer import simulate_trial, missing_features, OT_PROFILE
from test_joint_producer import fixture_inputs


def test_missing_history_is_explicit_empty_evidence():
    evidence=lookup_plays(None,StateKey('IND',1,'long','own20to50'))
    assert evidence.status=='EMPTY_STATE'
    assert evidence.plays is None
    assert 'MISSING' in evidence.pool_proposal


def test_role_weights_cannot_change_team_path(tmp_path):
    spec,root,inputs,data,save=fixture_inputs(tmp_path,terminal='targeted_pass',elapsed=100)
    data['model']['role_efficiency_coupling']=False
    save()
    first=simulate_trial(freeze_run(spec,root,inputs,n=1,seed=20261108),0)
    for team,rows in data['model']['role_states'].items():
        rows[0]['value']['rotation_weights']['target']={team+'ZERO':1}
        rows[0]['value']['rotation_weights']['passer']={team+'ZERO':1}
    save()
    second=simulate_trial(freeze_run(spec,root,inputs,n=1,seed=20261108),0)
    def team_path(trial):
        return [(r['team_id'],r['period_id'],r['stats']) for r in trial['team_periods']]
    assert first['validation']['status']==second['validation']['status']=='PASS'
    assert team_path(first)==team_path(second)
    assert first['status']['terminal_state']==second['status']['terminal_state']
    assert [e['player_credits'] for e in first['events']] != [e['player_credits'] for e in second['events']]
    assert first['freeze']['input_content_hash']!=second['freeze']['input_content_hash']
    assert first['rng']['trial_seed']==second['rng']['trial_seed']


def test_semantics_are_explicitly_unsupported():
    features=missing_features()
    for name in ['penalties','returns','official_overtime']:
        assert features[name]['status']=='UNSUPPORTED'
        assert features[name]['allows_sim_effect'] is False
    assert 'NOT_VERIFIED_OFFICIAL_OT' in OT_PROFILE['limitations']


def test_return_yards_cannot_be_silently_ignored(tmp_path):
    spec,root,inputs,data,save=fixture_inputs(tmp_path)
    data['model']['outcome_cells'][0]['distribution'][0]['value']['return_yards']=20
    save()
    with pytest.raises(ValueError,match='UNSUPPORTED'):
        simulate_trial(freeze_run(spec,root,inputs,n=1,seed=1),0)


def test_unfitted_role_efficiency_coupling_rejected(tmp_path):
    spec,root,inputs,data,save=fixture_inputs(tmp_path)
    data['model']['role_efficiency_coupling']=True
    save()
    with pytest.raises(ValueError,match='UNSUPPORTED'):
        simulate_trial(freeze_run(spec,root,inputs,n=1,seed=1),0)
