"""Engineering regressions only: no forecasts, network or paid requests."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('provenance', Path(__file__).parents[1] / 'provenance.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def test_athlete_parser_excludes_nested_entity_ids():
    document = {'athletes': [{'items': [{'id': '123', 'fullName': 'A',
        'college': {'id': '158', 'name': 'Nebraska'},
        'position': {'id': '9', 'name': 'Running Back'}}]}]}
    assert p.espn_athletes(document) == [{'espn_id': '123', 'name': 'A'}]
    assert p.espn_athletes({'entries': [{'playerId': 123, 'position': {'id': 9}}]}) == [
        {'espn_id': '123', 'name': None}]


@pytest.mark.parametrize('team,count,expected', [('JAX', 1, True), ('BAL', 1, False), ('JAX', 2, False)])
def test_exact_join_rejects_wrong_team_and_ambiguous_alias(team, count, expected):
    player = {'team': 'JAX', 'canonical_id': '00-1', 'canonical_namespace': 'gsis',
              'aliases': [{'namespace': 'espn', 'id': '123'}]}
    joined, unmatched = p.join_players([{'team': team, 'espn_id': '123', 'name': 'A'}], [player] * count)
    assert bool(joined) is expected
    assert bool(unmatched) is not expected


def test_hash_and_snapshot_conflicts_fail_closed(tmp_path):
    source, target = tmp_path / 'source', tmp_path / 'target'
    source.write_bytes(b'original')
    with pytest.raises(ValueError, match='hash'):
        p.verified_copy(source, target, '0' * 64)
    assert not target.exists()
    assert p.verified_copy(source, target)['sha256'] == p.digest(b'original')
    source.write_bytes(b'changed')
    with pytest.raises(ValueError, match='snapshot conflict'):
        p.verified_copy(source, target)
    assert target.read_bytes() == b'original'


@pytest.mark.parametrize('value', [None, '2026-11-05T18:55', 'bad'])
def test_unknown_or_naive_timestamp_rejected(value):
    with pytest.raises(ValueError):
        p.utc(value)


def quote():
    return {'book': 'fanduel', 'market': 'spreads', 'side': 'JAX', 'point': '-9.5',
            'price': '-110', 'event_id': 'provider-alias', 'inplay': 'False',
            'last_update_utc': '2026-11-06T01:12:25Z',
            'pulled_utc': '2026-11-06T01:12:42Z', 'commence_utc': '2026-11-06T01:20:00Z'}


def test_pre_cutoff_does_not_override_identity_conflicts():
    result = p.inspect_quotes([quote()], {'season': 2026, 'data_week': 10,
        'pulled_utc': '2026-11-06T01:12:42Z', 'max_quote_age_min': 30}, '2026-11-06T01:15:00Z', 9)
    assert result['timestamp_checks_pass']
    assert result['issues'] == ['KICKOFF_CONFLICT', 'WEEK_LABEL_CONFLICT']
    assert result['status'] == 'SAVED_ONLY'
    assert not result['usable_for_run']
    assert result['actionable_status'] == 'NOLINE'


@pytest.mark.parametrize('change,issue', [
    ({'last_update_utc': '2026-11-06T01:16:00Z'}, 'QUOTE_PULL_ASOF_CONFLICT'),
    ({'pulled_utc': '2026-11-06T01:16:00Z'}, 'QUOTE_PULL_ASOF_CONFLICT'),
    ({'last_update_utc': ''}, 'QUOTE_TIME_UNKNOWN'),
    ({'inplay': ''}, 'INPLAY_OR_UNKNOWN'), ({'point': ''}, 'LINE_MISSING')])
def test_bad_saved_quote_never_promoted(change, issue):
    row = {**quote(), **change}
    result = p.inspect_quotes([row], {'season': 2026, 'data_week': 9,
        'pulled_utc': '2026-11-06T01:12:42Z', 'max_quote_age_min': 30}, '2026-11-06T01:15:00Z', 9)
    assert issue in result['issues']
    assert not result['usable_for_frozen_pregame']


def test_header_only_quote_file_is_missing_data():
    result = p.inspect_quotes([], {}, '2026-11-06T01:15:00Z', 9)
    assert 'EMPTY_QUOTES' in result['issues']
    assert not result['usable_for_run']


@pytest.mark.parametrize('price', ['nan', 'inf', '0', 'not-a-price'])
def test_corrupt_quote_price_is_reported(price):
    result = p.inspect_quotes([{**quote(), 'price':price}], {}, '2026-11-06T01:15:00Z', 9)
    assert any('INVALID' in reason for reason in result['issues'])
