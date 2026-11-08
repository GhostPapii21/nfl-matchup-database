"""Check actual diagnostic artifact bytes; never grant source/run readiness."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root=ROOT):
    def load(name):
        return json.loads((root / name).read_text())

    manifest, rows = load('run_manifest.json'), load('source_ledger.json')
    assert manifest['source_ledger'] == rows
    assert manifest['run_kind'] == 'diagnostic_evaluation'
    assert manifest['projection_ready'] is False
    assert manifest['projection_execution_status'] == 'NOT_RUN'
    assert all(not item['enabled'] for item in manifest['automatic_cuts'].values())
    assert len(rows) == len({r['source_tool'] for r in rows}) == 34
    assert not any(r['usable_for_run'] or r['status'] == 'SUCCESS' for r in rows)
    artifact_count = 0
    for item in load('provenance.json')['artifacts']:
        path = root / item['path']
        assert sha(path) == item['sha256'], path
        assert path.stat().st_size == item['bytes'], path
        # Original explicit inputs are read-only. No timestamp claim follows.
        assert path.read_bytes() == Path(item['original_path']).read_bytes(), path
        artifact_count += 1
    for row in rows:
        if row['artifact_path']:
            path = root / row['artifact_path']
            assert sha(path) == row['artifact_sha256'], path
            records = json.loads(path.read_text())
            assert isinstance(records, list) and records
    for item in load('input_manifest.json')['inputs']:
        path = root / item['path']
        assert sha(path) == item['sha256'], path
    assert manifest['input_content_hash'] == 'sha256:' + sha(root / 'input_manifest.json')
    features = load('feature_availability.json')
    assert features['coverage']['status'] == 'UNKNOWN'
    assert all(features[k]['status'] == 'MISSING' for k in features if k != 'coverage')
    assert all(v['value'] is None and v['allows_sim_effect'] is False for v in features.values())
    assert [p['number'] for p in manifest['phases']] == list(range(1, 16))
    assert all(p['authoritative_name'] and p['status'] == 'BLOCKED' for p in manifest['phases'])
    players = load('aliases/player_aliases_certified_v2.json')
    assert len(players['matched']) == players['counts']['matched_observations']
    assert len(players['unmatched']) == players['counts']['unmatched_observations']
    assert all(x['canonical_id'] is None for x in players['unmatched'])
    assert all(x['join_method'] == 'EXACT_ESPN_ID_AND_TEAM' for x in players['matched'])
    assert load('aliases/game_aliases_certified_v2.json')['canonical_game_id'] is None
    return {'byte_verification': 'PASS', 'copied_artifacts_checked': artifact_count,
            'ledger_arrays_checked': sum(r['artifact_path'] is not None for r in rows),
            'input_hashes_checked': len(load('input_manifest.json')['inputs']),
            'source_gate': 'BLOCKED', 'projection_ready': False, 'impact': 'NOT_MEASURED'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
