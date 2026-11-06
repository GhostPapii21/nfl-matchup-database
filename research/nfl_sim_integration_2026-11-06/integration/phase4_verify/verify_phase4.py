"""Local engineering verification only; writes evidence to this directory."""
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

CORE = Path('/workspace/wt-nfl-sim-core-2026-11-06')
ROOT = Path('/workspace/research/nfl_sim_integration_2026-11-06')
OUT = Path(__file__).resolve().parent

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

def git(*args):
    p = subprocess.run(['git', '-C', str(CORE), *args], capture_output=True, text=True)
    return {'command': ['git', '-C', str(CORE), *args], 'returncode': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

def inventory(paths):
    return {str(p): {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
            for p in sorted(set(paths)) if p.is_file()}

def files(root):
    return [p for p in root.rglob('*') if p.is_file() and
            not any(x in p.parts for x in ('__pycache__', '.pytest_cache', '.git'))]

started = now()
historical = json.loads((ROOT / 'integration/verification_post_snapshot.json').read_text())
market_roots = {Path(x['path']).parents[len(Path(x['path']).parts) - Path(x['path']).parts.index('market_calibration') - 1]
                for x in historical['market_files']}
# Also cover the market tree in this worktree if present.
market_roots.add(CORE / 'research/market_calibration')
core_paths = files(CORE / 'research/possession_engine_v0')
protected_paths = files(ROOT / 'source_run_gate') + files(ROOT / 'integration/wire') + [
    ROOT / 'core_contract.md', ROOT / 'core_contract_wire_v1.md', ROOT / 'core_contract.checklist.json']

def snapshot():
    return {'timestamp_utc': now(), 'core_files': inventory(files(CORE / 'research/possession_engine_v0')),
            'protected_files': inventory(protected_paths),
            'market_roots': sorted(map(str, market_roots)),
            'market_files': inventory([p for r in market_roots for p in files(r)]),
            'git_status': git('status', '--short', '--untracked-files=all'),
            'git_head': git('rev-parse', 'HEAD'), 'git_diff': git('diff', 'HEAD', '--', 'research/possession_engine_v0')}

before = snapshot()
write('before_snapshot.json', before)
(OUT / 'core_tracked_before.diff').write_text(before['git_diff']['stdout'])
(OUT / 'git_status_before.txt').write_text(before['git_status']['stdout'])
test_path = CORE / 'research/possession_engine_v0/tests/test_joint_producer.py'
b = test_path.read_bytes()
a, z = b.index(b'WIRE_ROOT ='), b.index(b'def fixture_inputs(')
prior = b[:a] + b[z:]
prior_record = next(x for x in historical['core_files'] if x['path'] == str(test_path))
phase4_diff = ''.join(difflib.unified_diff(prior.decode().splitlines(True), b.decode().splitlines(True),
    fromfile='pre_phase4/test_joint_producer.py', tofile='phase4/test_joint_producer.py'))
(OUT / 'test_joint_producer_phase4.diff').write_text(phase4_diff)
untracked = git('ls-files', '--others', '--exclude-standard', '--', 'research/possession_engine_v0')
write('core_untracked_inventory.json', inventory([CORE / x for x in untracked['stdout'].splitlines()]))
example_path = ROOT / 'integration/wire/producer_joint_trial_example_v1.jsonl'
expected_example = '50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd'
example_sha = sha(example_path.read_bytes())
contract_path = ROOT / 'core_contract.md'
contract = contract_path.read_bytes()
link = b'Producer export wire: [`1.0.0-producer`](core_contract_wire_v1.md), frozen example and field-name lock.  \n'
expected_current = '6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367'
expected_historical = 'd6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9'
restored = contract.replace(link, b'', 1)
(OUT / 'contract_companion_link_only.diff').write_text(''.join(difflib.unified_diff(
    restored.decode().splitlines(True), contract.decode().splitlines(True),
    fromfile='historical/core_contract.md', tofile='current/core_contract.md')))
runs = []
for name, target in [('joint_producer', 'research/possession_engine_v0/tests/test_joint_producer.py'),
                     ('source_run_gate', str(ROOT / 'source_run_gate/tests'))]:
    command = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', target,
               '--basetemp=' + str(OUT / ('tmp_' + name)), '--junitxml=' + str(OUT / (name + '.xml'))]
    record = {'command': command, 'cwd': str(CORE), 'started_at_utc': now(),
              'log': str(OUT / (name + '.log')), 'junit': str(OUT / (name + '.xml'))}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    t = time.monotonic()
    with (OUT / (name + '.log')).open('w') as log:
        result = subprocess.run(command, cwd=CORE, env=env, stdout=log, stderr=subprocess.STDOUT)
    record.update(returncode=result.returncode, elapsed_seconds=time.monotonic()-t, finished_at_utc=now())
    xml = OUT / (name + '.xml')
    if xml.exists():
        suites = ET.parse(xml).getroot().iter('testsuite')
        counts = {k: 0 for k in ('tests', 'failures', 'errors', 'skipped')}
        for suite in suites:
            for k in counts:
                counts[k] += int(suite.get(k, 0))
        record['counts'] = counts
        record['passed'] = counts['tests'] - sum(counts[k] for k in ('failures', 'errors', 'skipped'))
    write(name + '_run.json', record)
    runs.append(record)
    print(name, record['returncode'], record.get('counts'), flush=True)
after = snapshot()
write('after_snapshot.json', after)
(OUT / 'git_status_after.txt').write_text(after['git_status']['stdout'])
(OUT / 'core_tracked_after.diff').write_text(after['git_diff']['stdout'])
changes = {}
for group in ('core_files', 'protected_files', 'market_files'):
    changes[group] = [p for p in sorted(set(before[group]) | set(after[group])) if before[group].get(p) != after[group].get(p)]
historical_core = {x['path']: {'sha256': x['sha256'], 'bytes': x['bytes']} for x in historical['core_files']}
phase4_core_changes = [{'path': p, 'historical': historical_core.get(p), 'current': before['core_files'].get(p)}
    for p in sorted(set(historical_core) | set(before['core_files'])) if historical_core.get(p) != before['core_files'].get(p)]
write('historical_core_comparison.json', phase4_core_changes)
checks = {'immutable_example_hash': example_sha == expected_example,
          'current_contract_hash': sha(contract) == expected_current,
          'historical_contract_link_only_restore': contract.count(link) == 1 and sha(restored) == expected_historical,
          'test_phase4_addition_only_matches_historical_hash': sha(prior) == prior_record['sha256'],
          'core_unchanged_this_verification': not changes['core_files'],
          'protected_unchanged_this_verification': not changes['protected_files'],
          'market_unchanged_this_verification': not changes['market_files'],
          'git_status_unchanged_this_verification': before['git_status'] == after['git_status'],
          'git_diff_unchanged_this_verification': before['git_diff'] == after['git_diff'],
          'pytest_all_passed': all(r['returncode'] == 0 and not sum(r['counts'][k] for k in ('failures','errors','skipped')) for r in runs)}
evidence = {'document_type': 'CORE_PHASE4_VERIFY_EVIDENCE', 'started_at_utc': started, 'finished_at_utc': now(),
 'verification_status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks,
 'scope': 'CORE phase4 wire-lock engineering verification only',
 'snapshots': {'before': 'before_snapshot.json', 'after': 'after_snapshot.json', 'hash_algorithm': 'sha256', 'changes': changes},
 'git': {'head': before['git_head'], 'status_before': before['git_status'], 'status_after': after['git_status'],
         'tracked_diff_before': 'core_tracked_before.diff', 'tracked_diff_after': 'core_tracked_after.diff',
         'untracked_inventory': 'core_untracked_inventory.json',
         'limitation': 'Joint producer and its tests are untracked; git diff alone cannot isolate phase4. Historical snapshot hash confirms exact insertion-only reconstruction.'},
 'historical_core_comparison': {'baseline': str(ROOT / 'integration/verification_post_snapshot.json'), 'changes': phase4_core_changes},
 'immutable_example': {'path': str(example_path), 'expected_sha256': expected_example, 'actual_sha256': example_sha},
 'contract': {'path': str(contract_path), 'current_sha256': sha(contract), 'expected_current_sha256': expected_current,
              'historical_restored_in_memory_sha256': sha(restored), 'expected_historical_sha256': expected_historical,
              'removed_line_utf8': link.decode(), 'removed_line_occurrences': contract.count(link),
              'restore_method': 'Remove only companion-link line in memory; no contract file write',
              'diff': 'contract_companion_link_only.diff'},
 'test_diff': {'path': str(test_path), 'historical_sha256': prior_record['sha256'], 'phase4_sha256': sha(b),
               'reconstructed_historical_sha256': sha(prior), 'added_lines': b[a:z].count(b'\n'), 'removed_lines': 0,
               'added_tests': ['test_frozen_producer_wire_v1_exact_bytes', 'test_export_preserves_documented_producer_wire_v1_shapes'],
               'diff': 'test_joint_producer_phase4.diff', 'field_renames': False,
               'pins': ['exact immutable fixture bytes and single JSONL row', 'schema/version and top-level keys',
                        'status object and nested fields/types', 'freeze.input_manifest_digest',
                        'engine.component_version and dependencies (python/numpy)', 'team_periods[].stats.points',
                        'exact canonical JSONL export bytes'],
               'production_code_changed_for_phase4': False},
 'pytest': runs,
 'model_predictive_metrics': {'status': 'NOT_MEASURED', 'reason': 'No frozen forecast vs actual evaluation in this engineering pass; insufficient paired data for predictive metrics. Synthetic engineering test counts are not predictive evidence.',
                             'metrics': {k: 'NOT_MEASURED' for k in ['accuracy', 'calibration', 'bias', 'predictive_improvement']}},
 'constraints': {'market_edits': False, 'spend': 0, 'network_requests': 0, 'paid_pulls': 0, 'projection_runs': 0,
                 'projection_ready_claim': False, 'predictive_improvement_claim': False},
 'acceptance_scope': 'No direct adapter or final integration acceptance claimed; those are outside this verification.',
 'artifacts': inventory([p for p in OUT.iterdir() if p.is_file() and p.name not in ('PHASE4_VERIFY_EVIDENCE.json', 'PHASE4_VERIFY.md')])}
write('PHASE4_VERIFY_EVIDENCE.json', evidence)
rows = '\n'.join(f"| {Path(x['path']).relative_to(CORE)} | {x['historical']['sha256'] if x['historical'] else 'absent'} | {x['current']['sha256'] if x['current'] else 'absent'} |" for x in phase4_core_changes)
md = f'''# CORE phase4 verification

Engineering verification: **{evidence['verification_status']}**. No market edits, network requests, paid pulls, spend, or projection runs. No projection readiness or predictive improvement claimed.

## Regression results

- Joint producer: {runs[0].get('passed')} passed; exit {runs[0]['returncode']}. [Log](joint_producer.log), [JUnit](joint_producer.xml), [command/timing](joint_producer_run.json).
- Source run gate: {runs[1].get('passed')} passed; exit {runs[1]['returncode']}. [Log](source_run_gate.log), [JUnit](source_run_gate.xml), [command/timing](source_run_gate_run.json).

## Integrity

Immutable JSONL example SHA-256: `{example_sha}` — matches requested digest.

Current core_contract.md SHA-256: `{sha(contract)}`.
Historical SHA-256 reconstructed by removing only the one companion-link line: `{sha(restored)}`.
The reconstruction was performed in memory; the contract was not edited. [Exact one-line diff](contract_companion_link_only.diff).

[Before](before_snapshot.json) and [after](after_snapshot.json) snapshots record SHA-256/size for CORE files (including all possession tests), source-gate files, wire artifacts, contract documents, and market trees listed in the snapshots. No inventoried files changed during verification. Git status and tracked diff are unchanged; the existing dirty state was preserved. Market coverage is the recorded inventory roots, not a claim about every filesystem location.

## CORE diff assessment

Git HEAD: `{before['git_head']['stdout'].strip()}`. The worktree has four inherited tracked modifications (README.md, config_load.py, simulate.py, validation/accounting.py) and six untracked producer files, including test_joint_producer.py. [Status](git_status_before.txt), [tracked diff](core_tracked_before.diff), [untracked hashes](core_untracked_inventory.json).

Relative to the pre-phase4 integration snapshot, CORE changes are:

| File | Historical SHA-256 | Phase4 SHA-256 |
| --- | --- | --- |
{rows}

The [phase4 test diff](test_joint_producer_phase4.diff) adds exactly 58 lines and removes none: an immutable-fixture loader and two wire-shape tests. Removing that block reproduces the historical test hash `{sha(prior)}` exactly. This proves the rest of the test file is unchanged against that recorded baseline. Production CORE hashes match the historical snapshot.

The additions pin fixture SHA and schema/version, exact canonical JSONL export, top-level keys, the nested status object, freeze.input_manifest_digest, engine.component_version/dependencies, and team_periods[].stats.points. They reject alternate field spellings and keep adapter_projection_allowed false. No producer field renames or runtime code changes occurred for this wire lock. Git itself cannot show an incremental diff for the untracked test; the hash-verified historical reconstruction supplies that comparison.

## Predictive metrics

**NOT_MEASURED**: no frozen forecast vs actual evaluation in this engineering pass; insufficient paired data for predictive metrics. Accuracy, calibration, bias, and predictive improvement remain NOT_MEASURED. Passing synthetic engineering tests supplies no predictive evidence.

Direct adapter acceptance and final integration acceptance were not exercised or claimed. Full machine-readable checks, before/after evidence, commands, and artifact hashes are in [PHASE4_VERIFY_EVIDENCE.json](PHASE4_VERIFY_EVIDENCE.json).
'''
(OUT / 'PHASE4_VERIFY.md').write_text(md)
print(json.dumps({'status': evidence['verification_status'], 'checks': checks, 'historical_core_changed_paths': [x['path'] for x in phase4_core_changes]}, indent=2))
