import json
from pathlib import Path
import pandas as pd
from fit_prospective_roles import fit_roles
from simulate import source_composition

BASE=Path(__file__).resolve().parents[1]
def test_source_identity():
    cfg=json.loads((BASE/'config/dal_ind_2026-11-08_data_only.json').read_text())
    assert 'DAL_IND' in source_composition(cfg)
    assert 'JAX_BAL' not in source_composition(cfg)
    cfg['game'].update(away='JAX',home='BAL')
    assert 'JAX_BAL' in source_composition(cfg)

def test_empirical_roles():
    players=[dict(record_id=x,player_id=x,team_id='DAL',position='RB',status=s,availability=a) for x,s,a in [('a','ACT','AVAILABLE'),('b','ACT','AVAILABLE_WITH_UNCERTAINTY'),('ir','RES','UNAVAILABLE')]]
    raw=pd.DataFrame([dict(posteam='DAL',rusher_player_id=x,receiver_player_id=None,passer_player_id=None,qtr=1,week=1) for x in ['a']*9+['b','ir']])
    model={'role_states':{'DAL':[{'value':{'available':['a','b','ir'],'rotation_weights':{}}}]}}
    evidence=fit_roles(raw,model,{'players':players})
    state=model['role_states']['DAL'][0]['value']
    assert state['rotation_weights']['carry']['a']>state['rotation_weights']['carry']['b']
    assert 'ir' not in state['available']
    assert 'b' in state['available']
    assert evidence['protocol']=='train W1-6; hold W7-8'

def test_shared_projection_conserves_and_rejects_drift(tmp_path):
    import copy
    import pytest
    from test_joint_producer import fixture_inputs
    from joint_producer import simulate_joint_games
    from shared_accounting import shared_projection
    spec,root,inputs,_,_=fixture_inputs(tmp_path)
    result=simulate_joint_games(spec,input_root=root,inputs=inputs,n=1,seed=123,output_root=tmp_path/'run')
    trial=result['trials'][0]
    projection=shared_projection(trial)
    assert projection['team_periods']==trial['team_periods']
    assert projection['player_periods']==trial['player_periods']
    assert projection['forecast_id']==trial['forecast_id']
    broken=copy.deepcopy(trial)
    broken['team_periods'][0]['stats']['points']+=1
    with pytest.raises(ValueError,match='mismatch'):
        shared_projection(broken)

def test_shared_dispatch_and_seed_repeat(tmp_path):
    from test_joint_producer import fixture_inputs
    from simulate import simulate_games
    spec,root,inputs,_,_=fixture_inputs(tmp_path)
    cfg={'mode':spec['mode'],'config_id':spec['config_id'],'joint_producer':{'spec':spec,'input_root':root,'inputs':inputs,'output_root':tmp_path/'shared','shared_accounting':True}}
    a=simulate_games(cfg,pbp_path='NEVER_READ',n=1,seed=123)
    b=simulate_games(cfg,pbp_path='NEVER_READ',n=1,seed=123)
    assert a['path_semantics']=='SHARED_ACCOUNTING_V1'
    assert a['forecast_id']==b['forecast_id']
    assert a['shared_projections']==b['shared_projections']
