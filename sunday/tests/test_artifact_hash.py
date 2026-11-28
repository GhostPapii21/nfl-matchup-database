import hashlib

from sunday.stack import _dump, _sha_file


def test_dump_hash_matches_persisted_bytes(tmp_path):
    path = tmp_path / 'nested' / 'artifact.json'
    digest = _dump(path, {'value': 42})
    assert path.read_bytes().endswith(b'\n')
    assert digest == hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == _sha_file(path)
