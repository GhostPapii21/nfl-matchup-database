"""SYNTHETIC regression fixtures only; no live retrieval or projection execution."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('source_readiness', PACKAGE / 'readiness.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


@pytest.fixture
def full(tmp_path):
    """Full real-shaped file contract, with every observation explicitly synthetic."""
    stamp = '2026-11-06T10:00:00Z'
    records = [{'game_id': 'synthetic-game', 'team_id': 'SYN', 'targets': 4, 'synthetic': True}]
    data = (json.dumps(records) + '\n').encode()
    (tmp_path / 'source.json').write_bytes(data)
    text = 'SYNTHETIC fixture; no live retrieval. betting-game-brainstorm\n'
    (tmp_path / 'brainstorm.md').write_text(text)
    (tmp_path / 'report.md').write_text(text)
    (tmp_path / 'checklist.md').write_text(text + ''.join(
        f'| [x] | {n:02} | Synthetic phase {n} | report.md | |\n' for n in range(1, 16)))
    row = dict(document_type='ledger_row', source_id='synthetic-source', source_tool='nflverse',
               status='SUCCESS', assessment='retrieved', status_reason='SYNTHETIC fixture only',
               fields_retrieved=['game_id', 'team_id', 'targets'], season=2026, week=10,
               data_through_timestamp=stamp, pull_timestamp=stamp, source_available_timestamp=stamp,
               cutoff_utc=stamp, attempt_timestamp=stamp, artifact_path='source.json',
               artifact_sha256=hashlib.sha256(data).hexdigest(), unknown_reasons={},
               scope='Synthetic game only', usable_for_run=True, asof_status='verified',
               freshness_status='current', fallback={'kind':'none','detail':'Synthetic full fixture','source_refs':[]})
    rows = [row]
    for i, source in enumerate(sorted(gate.REQUIRED_SOURCES - {'nflverse'})):
        na = copy.deepcopy(row)
        na.update(source_id=f'synthetic-na-{i}', source_tool=source, status='NOT_APPLICABLE',
                  reason='SYNTHETIC fixture scope has no dependency on this provider', usable_for_run=False)
        rows.append(na)
    manifest = dict(document_type='run_manifest', schema_version='1.0.0', run_id='synthetic-full',
        run_kind='projection', season=2026, week=10, game_id='synthetic-game', game_id_namespace='synthetic',
        cutoff_utc=stamp, frozen_at_utc=stamp, generated_at_utc=stamp, engine_version='synthetic-engine',
        config_id='synthetic-config', input_content_hash='sha256:'+'0'*64,
        workflow_versions={n:'synthetic-v1' for n in ['betting-game-brainstorm','nfl-game-script-run','nfl-betting-script','football-period-game-flow']},
        checklist_path='checklist.md', report_path='report.md', brainstorm_path='brainstorm.md',
        source_ledger=rows, source_gate={'status':'APPROVED','evidence':'report.md','permitted_scope':'Synthetic fixture only','blockers':[]},
        scenario_first={'status':'COMPLETE','evidence':'brainstorm.md'},
        phases=[{'number':n,'authoritative_name':f'Synthetic phase {n}, not an authoritative workflow definition',
                 'status':'COMPLETE','evidence':'report.md','reason':None} for n in range(1,16)],
        supplemental_workflows={n:{'status':'NOT_APPLICABLE','reason':'Synthetic fixture only','evidence':None} for n in ['nfl-betting-script','football-period-game-flow']},
        projection_execution_status='NOT_RUN', engineering_checks=[], blockers=[], projection_ready=True,
        synthetic=True, validation_basis='full_source_run',
        automatic_cuts=copy.deepcopy(json.loads((PACKAGE / 'MANIFEST.json').read_text())['automatic_cuts']))
    return manifest, tmp_path


def result(full):
    return gate.assess(*full, allow_synthetic=True)


def test_schema_is_valid():
    Draft202012Validator.check_schema(gate.SCHEMA)


def test_diagnostic_run_is_schema_valid_but_never_ready(full):
    manifest, directory = full
    manifest.update(run_kind='diagnostic_evaluation', projection_ready=False)
    assert not list(gate.VALIDATOR.iter_errors(manifest))
    checked = gate.assess(manifest, directory, allow_synthetic=True)
    assert not checked['projection_ready']
    assert not checked['synthetic_fixture_ready']
    manifest['projection_ready'] = True
    assert list(gate.VALIDATOR.iter_errors(manifest))


def test_saved_bytes_may_have_unknown_pull_without_invented_time(full):
    manifest, directory = full
    row = manifest['source_ledger'][0]
    row.update(status='SAVED_ONLY', usable_for_run=False, pull_timestamp=None)
    row['unknown_reasons']['pull_timestamp'] = 'Original provider retrieval instant unavailable'
    assert not list(gate.VALIDATOR.iter_errors(row))
    assert not gate.assess(manifest, directory, allow_synthetic=True)['synthetic_fixture_ready']
    row['status'] = 'SUCCESS'
    row['usable_for_run'] = True
    assert list(gate.VALIDATOR.iter_errors(row))


def test_green_full_fixture_never_claims_live_readiness(full):
    assert not list(gate.VALIDATOR.iter_errors(full[0]))
    assert result(full) == {'projection_ready':False,'synthetic_fixture_ready':True,'errors':[]}
    assert gate.assess(*full)['errors']


@pytest.mark.parametrize('filename', ['brainstorm.md','checklist.md','report.md','source.json'])
def test_red_missing_required_artifact(full, filename):
    (full[1] / filename).unlink()
    assert result(full)['errors']
    assert not result(full)['synthetic_fixture_ready']


@pytest.mark.parametrize('bad_records', [[], {}, [{'game_id':'synthetic-game'}], [{'game_id':None,'team_id':'SYN','targets':4}]])
def test_red_empty_template_or_incomplete_records(full, bad_records):
    data = json.dumps(bad_records).encode()
    (full[1] / 'source.json').write_bytes(data)
    full[0]['source_ledger'][0]['artifact_sha256'] = hashlib.sha256(data).hexdigest()
    assert result(full)['errors']


def test_red_empty_ledger(full):
    full[0]['source_ledger'] = []
    assert result(full)['errors']


@pytest.mark.parametrize('status', ['SAVED_ONLY','STALE','MISSING','LOGIN_REQUIRED','ERROR'])
@pytest.mark.parametrize('usable', [True, False])
def test_red_nonlive_status_cannot_be_promoted(full, status, usable):
    full[0]['source_ledger'][0].update(status=status, usable_for_run=usable)
    assert result(full)['errors']


def test_red_success_unusable(full):
    full[0]['source_ledger'][0]['usable_for_run'] = False
    assert result(full)['errors']


@pytest.mark.parametrize('field', ['fields_retrieved','season','week','data_through_timestamp',
    'pull_timestamp','cutoff_utc','artifact_path','artifact_sha256','fallback'])
def test_red_missing_provenance(full, field):
    del full[0]['source_ledger'][0][field]
    assert result(full)['errors']


@pytest.mark.parametrize('reason', [None, '', '   '])
def test_red_na_requires_nonempty_reason(full, reason):
    row = full[0]['source_ledger'][1]
    if reason is None:
        del row['reason']
    else:
        row['reason'] = reason
    assert result(full)['errors']


@pytest.mark.parametrize('basis', ['infrastructure_only','schema_only'])
def test_red_infrastructure_is_not_readiness(full, basis):
    full[0]['validation_basis'] = basis
    assert result(full)['errors']


def test_engineering_pass_does_not_set_projection_ready(full):
    full[0].update(projection_ready=False, run_kind='engineering_test',
                   engineering_checks=[{'name':'unit tests','status':'COMPLETE','evidence':'report.md'}])
    assert not result(full)['projection_ready']
    assert not result(full)['synthetic_fixture_ready']
    assert full[0]['projection_ready'] is False


@pytest.mark.parametrize('change', ['unmarked','duplicate','missing_marker','hash','cutoff','scope','inventory','escape','unlabeled'])
def test_red_semantic_artifact_checks(full, change):
    manifest, root = full
    if change == 'unmarked':
        p=root/'checklist.md'; p.write_text(p.read_text().replace('[x]', '[ ]', 1))
    elif change == 'duplicate':
        p=root/'checklist.md'; p.write_text(p.read_text().replace('| 15 |', '| 14 |'))
    elif change == 'missing_marker':
        (root/'brainstorm.md').write_text('SYNTHETIC blank brainstorm')
    elif change == 'hash':
        (root/'source.json').write_text('[{"tampered":true}]')
    elif change == 'cutoff':
        manifest['source_ledger'][0]['source_available_timestamp']='2026-11-07T10:00:00Z'
    elif change == 'scope':
        manifest['source_ledger'][0]['week']=9
    elif change == 'inventory':
        manifest['source_ledger'].pop()
    elif change == 'escape':
        manifest['brainstorm_path']='../brainstorm.md'
    elif change == 'unlabeled':
        (root/'report.md').write_text('Looks like a live report')
    assert result(full)['errors']


def test_exact_status_enum_and_reject_legacy(full):
    assert gate.SCHEMA['$defs']['ledger_row']['properties']['status']['enum'] == [
        'SUCCESS','SAVED_ONLY','MISSING','LOGIN_REQUIRED','STALE','ERROR','NOT_APPLICABLE']
    full[0]['source_ledger'][0]['status']='success'
    assert result(full)['errors']


def test_entry_point_red_and_synthetic_green(full):
    manifest, root = full
    path=root/'manifest.json'; path.write_text(json.dumps(manifest))
    cmd=[sys.executable,str(PACKAGE/'readiness.py'),str(path)]
    red=subprocess.run(cmd,capture_output=True,text=True)
    green=subprocess.run(cmd+['--synthetic-fixture'],capture_output=True,text=True)
    assert red.returncode == 1
    assert green.returncode == 0
    assert json.loads(green.stdout)['projection_ready'] is False
    (root/'report.md').unlink()
    assert subprocess.run(cmd+['--synthetic-fixture'],capture_output=True).returncode == 1


def test_red_synthetic_evidence_cannot_be_relabelled_live(full):
    full[0]['synthetic'] = False
    outcome = gate.assess(*full)
    assert outcome['errors']
    assert outcome['projection_ready'] is False


def test_all_na_inventory_is_not_source_evidence(full):
    full[0]['source_ledger'][0].update(status='NOT_APPLICABLE', usable_for_run=False,
        reason='Synthetic fixture exclusion')
    assert result(full)['errors']


def test_package_inventory_is_schema_valid_but_not_ready():
    package = json.loads((PACKAGE / 'MANIFEST.json').read_text())
    assert package['projection_ready'] is False
    assert package['execution_status']['live_retrieval'] == 'NOT_RUN'
    for row in package['source_inventory']:
        assert not list(gate.VALIDATOR.iter_errors(row))
        assert row['status'] == 'MISSING' and row['usable_for_run'] is False


@pytest.mark.parametrize('cut', ['weather', 'WR', 'edge'])
def test_red_automatic_cuts_enabled_without_dated_approval(full, cut):
    full[0]['automatic_cuts'][cut]['enabled'] = True
    outcome = result(full)
    assert outcome['projection_ready'] is False
    assert outcome['synthetic_fixture_ready'] is False
    assert any(f'automatic cuts: {cut} must remain DISABLED' in e for e in outcome['errors'])


@pytest.mark.parametrize('cut', ['weather', 'WR', 'edge'])
def test_red_automatic_cuts_cannot_omit_disablement(full, cut):
    del full[0]['automatic_cuts'][cut]
    assert result(full)['errors']
    assert not result(full)['synthetic_fixture_ready']


def test_red_automatic_cuts_declaration_required(full):
    del full[0]['automatic_cuts']
    assert result(full)['errors']
    assert not result(full)['synthetic_fixture_ready']


def test_green_automatic_cuts_explicitly_disabled(full):
    for settings in full[0]['automatic_cuts'].values():
        assert settings['enabled'] is False
        assert settings['approval_status'] == 'MISSING'
    assert result(full)['synthetic_fixture_ready'] is True
    assert result(full)['projection_ready'] is False


@pytest.mark.parametrize('reason', [None, '', '   ', '\t\n'])
def test_red_na_reason_is_enforced_by_runtime_schema(full, reason):
    row = full[0]['source_ledger'][1]
    row['reason'] = reason
    assert list(gate.VALIDATOR.iter_errors(row))
    outcome = result(full)
    assert any(e.startswith('schema:') for e in outcome['errors'])
    assert outcome['projection_ready'] is False
    assert outcome['synthetic_fixture_ready'] is False


@pytest.mark.parametrize('cut', ['weather', 'WR', 'edge'])
def test_red_automatic_cuts_approval_claim_does_not_unlock(full, cut):
    full[0]['automatic_cuts'][cut].update(
        enabled=True, approval_status='APPROVED',
        reason='SYNTHETIC claimed approval dated 2026-11-06; no authorization artifact')
    outcome = result(full)
    assert outcome['projection_ready'] is False
    assert outcome['synthetic_fixture_ready'] is False
    assert any(f'automatic cuts: {cut} must remain DISABLED' in e for e in outcome['errors'])
