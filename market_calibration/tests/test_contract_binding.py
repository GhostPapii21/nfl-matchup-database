"""Authorized binding and immutable producer example; no overrides or remapping."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from research.market_calibration import joint_trial_adapter as adapter
from research.market_calibration.manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZED_SHA256 = '6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367'
HISTORICAL_SHA256 = 'd6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9'
EXAMPLE = Path(__file__).resolve().parents[2] / (
    "research/nfl_sim_integration_2026-11-06/integration/wire/producer_joint_trial_example_v1.jsonl")
EXAMPLE_SHA256 = '50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd'
EXPECTED_IDS = ['sha256:d89f251bd9c3994e66f7d24a0731abbcfb2b3e25bf5302e936eb29fd338653c0/trial/0']


def example_rows():
    content = EXAMPLE.read_bytes()
    assert sha256(content).hexdigest() == EXAMPLE_SHA256
    return [json.loads(line) for line in content.splitlines()]


def test_authorized_binding_matches_current_contract_and_manifest():
    assert adapter.CONTRACT_SHA256 == AUTHORIZED_SHA256
    info = adapter.contract_info()
    assert info['sha256'] == AUTHORIZED_SHA256
    assert info['status'] == 'CONTRACT_SCORE_TRANSPORT_ONLY'
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    assert manifest['adapter']['contract_sha256'] == AUTHORIZED_SHA256
    assert manifest['adapter']['wire_agreement_id'] == 'market-producer-wire-v1.0.1'
    assert validate_manifest(manifest, ROOT)


def test_immutable_producer_example_transport_without_remap():
    rows = example_rows()
    original = deepcopy(rows)
    transported = adapter.adapt_joint_trials(rows, expected_trial_ids=EXPECTED_IDS)
    assert [trial.trial_id for trial in transported] == EXPECTED_IDS
    assert rows == original
    for source, trial in zip(rows, transported, strict=True):
        assert trial.source == source
        assert trial.source is not source
        assert trial.source['status'] is not source['status']
        assert trial.source['team_periods'] is not source['team_periods']
        assert trial.source['status']['adapter_projection_allowed'] is False
        assert 'SCENARIO_ONLY' in trial.source['status']['projection_blockers']
        assert trial.interface_status == 'CONTRACT_SCORE_TRANSPORT_ONLY'
        assert trial.actionable_status == 'NOLINE'
        assert trial.reasons == ('FULL_CORE_ACCEPTANCE_NOT_RUN',
                                 'QUOTE_RULE_COMPATIBILITY_NOT_VERIFIED')
        teams = (source['game']['home_team_id'], source['game']['away_team_id'])
        expected = tuple(sum(period['stats']['points'] for period in source['team_periods']
                             if period['team_id'] == team) for team in teams)
        assert trial.scorecard.points('FG') == expected
    assert sha256(EXAMPLE.read_bytes()).hexdigest() == EXAMPLE_SHA256


@pytest.mark.parametrize('wrong_sha', [HISTORICAL_SHA256, '0' * 64])
def test_contract_guard_still_rejects_wrong_binding(monkeypatch, wrong_sha):
    rows = example_rows()
    original = deepcopy(rows)
    # Negative guard probe only: the actual CORE_CONTRACT path stays untouched.
    monkeypatch.setattr(adapter, 'CONTRACT_SHA256', wrong_sha)
    assert adapter.contract_info()['status'] == 'CORE_CONTRACT_REQUIRES_ALIGNMENT'
    with pytest.raises(ValueError, match='bound core contract absent or changed'):
        adapter.adapt_joint_trials(rows, expected_trial_ids=EXPECTED_IDS)
    assert rows == original


@pytest.mark.parametrize('wrong_sha', [HISTORICAL_SHA256, '0' * 64])
def test_manifest_still_rejects_wrong_contract_sha(wrong_sha):
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    manifest['adapter']['contract_sha256'] = wrong_sha
    with pytest.raises(ValueError, match='adapter contract digest mismatch'):
        validate_manifest(manifest, ROOT)
