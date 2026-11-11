"""Direct retained producer wire regression; no diagnostic mapping or simulation."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from market_calibration.joint_trial_adapter import adapt_joint_trials
from test_contract_manifest import trial


INTEGRATION = Path(__file__).resolve().parents[2] / "research/nfl_sim_integration_2026-11-06"
SMOKE = INTEGRATION / 'reviews/core_producer_synthetic_smoke/forecasts' / (
    'sha256_d89f251bd9c3994e66f7d24a0731abbcfb2b3e25bf5302e936eb29fd338653c0') / 'trials.jsonl'
SMOKE_SHA256 = '1f9ac51296d4d760510b46f77f56de0c4a4df437c94895e327c3b794434f5e6d'


def test_direct_retained_producer_wire_without_remap():
    # Load the independently retained population BEFORE opening consumer rows.
    evidence = json.loads((INTEGRATION / 'reviews/EVIDENCE_CODEX.json').read_text())['smoke']
    expected_ids = evidence['trial_ids']
    content = SMOKE.read_bytes()
    assert sha256(content).hexdigest() == SMOKE_SHA256
    assert evidence['artifact_hashes']['trials.jsonl'] == 'sha256:' + SMOKE_SHA256
    rows = [json.loads(line) for line in content.splitlines()]
    original = deepcopy(rows)

    transported = adapt_joint_trials(rows, expected_trial_ids=expected_ids)

    assert [trial.trial_id for trial in transported] == expected_ids
    assert rows == original

    for source, trial in zip(rows, transported, strict=True):
        assert trial.source == source
        assert trial.source is not source
        assert trial.source['status'] is not source['status']
        assert trial.source['team_periods'] is not source['team_periods']
        assert trial.actionable_status == 'NOLINE'
        assert trial.interface_status == 'CONTRACT_SCORE_TRANSPORT_ONLY'
        assert 'FULL_CORE_ACCEPTANCE_NOT_RUN' in trial.reasons
        teams = (source['game']['home_team_id'], source['game']['away_team_id'])
        windows = {'Q1': {'Q1'}, 'Q2': {'Q2'}, 'Q3': {'Q3'}, 'Q4': {'Q4'},
                   'H1': {'Q1', 'Q2'}, 'H2': {'Q3', 'Q4'},
                   'REG': {'Q1', 'Q2', 'Q3', 'Q4'},
                   'FG': {p['period_id'] for p in source['team_periods']}}
        for period, primitives in windows.items():
            expected = tuple(sum(p['stats']['points'] for p in source['team_periods']
                                 if p['team_id'] == team and p['period_id'] in primitives)
                             for team in teams)
            assert trial.scorecard.points(period) == expected
        # Mutating the retained copy cannot inject fields into caller-owned rows.
        trial.source['status']['state'] = 'COPY_ONLY'
    assert rows == original


@pytest.fixture
def producer_trial():
    """Labeled synthetic score fixture for edge cases; never a producer forecast."""
    row = trial()
    row['status'] = dict(state=row['status'], **{
        key: row.pop(key) for key in ('completion_reason', 'terminal_state', 'went_ot')})
    row['freeze']['input_manifest_digest'] = row['freeze'].pop('input_manifest_hash')
    row['engine'].pop('component_versions')
    row['engine']['component_version'] = 'synthetic-wire-fixture-v1'
    row['engine']['dependencies'] = row['engine'].pop('dependency_versions')
    for period in row['team_periods']:
        period['stats'] = {'points': period.pop('points')}
    return row


def test_object_wire_retains_nonzero_nested_scores(producer_trial):
    original = deepcopy(producer_trial)
    projected = adapt_joint_trials([producer_trial])[0]
    assert projected.scorecard.points('H1') == (3, 17)
    assert projected.scorecard.points('H2') == (17, 3)
    assert projected.scorecard.points('FG') == (20, 20)
    assert projected.source == producer_trial == original


@pytest.mark.parametrize('state', ['INCOMPLETE', 'INVALID', None, {}, 'complete'])
def test_object_status_requires_complete(producer_trial, state):
    producer_trial['status']['state'] = state
    with pytest.raises(ValueError, match='incomplete/invalid'):
        adapt_joint_trials([producer_trial])


@pytest.mark.parametrize('field', ['state', 'completion_reason', 'terminal_state', 'went_ot'])
def test_object_status_requires_nested_fields(producer_trial, field):
    del producer_trial['status'][field]
    with pytest.raises(ValueError, match='status fields'):
        adapt_joint_trials([producer_trial])


@pytest.mark.parametrize('value', [None, 0, 1, 'false'])
def test_object_went_ot_requires_boolean(producer_trial, value):
    producer_trial['status']['went_ot'] = value
    with pytest.raises(ValueError, match='OT'):
        adapt_joint_trials([producer_trial])


@pytest.mark.parametrize('field', ['completion_reason', 'terminal_state', 'went_ot'])
def test_object_sibling_fields_must_agree_when_present(producer_trial, field):
    producer_trial[field] = producer_trial['status'][field]
    assert adapt_joint_trials([producer_trial])[0].source == producer_trial
    producer_trial[field] = 'CONFLICT'
    with pytest.raises(ValueError, match='conflicting status'):
        adapt_joint_trials([producer_trial])


@pytest.mark.parametrize('mode', ['digest', 'hash', 'both', 'conflict', 'missing', 'invalid'])
def test_manifest_digest_aliases(producer_trial, mode):
    freeze = producer_trial['freeze']
    if mode in {'hash', 'both', 'conflict'}:
        freeze['input_manifest_hash'] = freeze['input_manifest_digest']
    if mode in {'hash', 'missing'}:
        del freeze['input_manifest_digest']
    if mode == 'conflict':
        freeze['input_manifest_hash'] = 'sha256:' + 'e' * 64
    if mode == 'invalid':
        freeze['input_manifest_digest'] = 'invalid'
    if mode in {'conflict', 'missing', 'invalid'}:
        with pytest.raises(ValueError, match='manifest|freeze hash'):
            adapt_joint_trials([producer_trial])
    else:
        assert adapt_joint_trials([producer_trial])[0].source == producer_trial


@pytest.mark.parametrize('components', ['singular', 'plural', 'both', 'missing'])
@pytest.mark.parametrize('dependencies', ['singular', 'plural', 'both', 'missing', 'conflict'])
def test_engine_wire_names(producer_trial, components, dependencies):
    engine = producer_trial['engine']
    if components in {'plural', 'both'}:
        engine['component_versions'] = {'joint_producer': engine['component_version']}
    if components in {'plural', 'missing'}:
        del engine['component_version']
    if dependencies in {'plural', 'both', 'conflict'}:
        engine['dependency_versions'] = deepcopy(engine['dependencies'])
    if dependencies in {'plural', 'missing'}:
        del engine['dependencies']
    if dependencies == 'conflict':
        engine['dependency_versions'] = {'python': 'CONFLICT'}
    if 'missing' in (components, dependencies) or dependencies == 'conflict':
        with pytest.raises(ValueError, match='engine'):
            adapt_joint_trials([producer_trial])
    else:
        assert adapt_joint_trials([producer_trial])[0].source == producer_trial


@pytest.mark.parametrize('profile', ['ot_rule_profile', 'stat_credit_profile'])
@pytest.mark.parametrize('value', [None, '', {}])
def test_object_wire_still_requires_profiles(producer_trial, profile, value):
    producer_trial['engine'][profile] = value
    with pytest.raises(ValueError, match='profile'):
        adapt_joint_trials([producer_trial])


@pytest.mark.parametrize('mode', ['nested', 'flat', 'both', 'conflict', 'missing', 'bool', 'float'])
def test_score_aliases(producer_trial, mode):
    period = producer_trial['team_periods'][0]
    if mode in {'flat', 'both', 'conflict', 'bool', 'float'}:
        period['points'] = period['stats']['points']
    if mode in {'flat', 'missing'}:
        del period['stats']['points']
    if mode == 'conflict':
        period['points'] += 1
    if mode == 'bool':
        period['points'] = True
        period['stats']['points'] = 1
    if mode == 'float':
        period['points'] = 3.0
    if mode in {'conflict', 'missing', 'bool', 'float'}:
        with pytest.raises(ValueError, match='points|score'):
            adapt_joint_trials([producer_trial])
    else:
        assert adapt_joint_trials([producer_trial])[0].scorecard.points('Q1') == (3, 10)


@pytest.mark.parametrize('case', ['played_zero', 'played_score', 'unplayed_zero', 'missing',
                                 'missing_team', 'gap', 'regulation_not_tied'])
def test_object_ot_policy(producer_trial, case):
    producer_trial['status']['went_ot'] = case != 'unplayed_zero'
    if case != 'missing':
        producer_trial['team_periods'].extend([
            dict(team_id='BAL', period_id='OT1', stats=dict(points=0)),
            dict(team_id='JAX', period_id='OT1', stats=dict(points=3 if case == 'played_score' else 0))])
    if case == 'missing_team':
        producer_trial['team_periods'].pop()
    if case == 'gap':
        for period in producer_trial['team_periods'][-2:]:
            period['period_id'] = 'OT2'
    if case == 'regulation_not_tied':
        producer_trial['team_periods'][0]['stats']['points'] += 1
    original = deepcopy(producer_trial)
    if case in {'played_zero', 'played_score'}:
        projected = adapt_joint_trials([producer_trial])[0]
        assert projected.scorecard.points('FG') == (20, 23 if case == 'played_score' else 20)
        assert projected.source == original
    else:
        with pytest.raises(ValueError, match='OT'):
            adapt_joint_trials([producer_trial])
    assert producer_trial == original
