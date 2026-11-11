"""Verify and decompress the public snapshot using only Python's standard library."""
import gzip, hashlib, json, os, pathlib, shutil, sys

root = pathlib.Path(__file__).resolve().parent
data = root / 'data'
src_path = root / 'nfl_matchups.sqlite.gz'
out_path = data / 'nfl_matchups.sqlite'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def fail(msg):
    # Explicit exit, not assert: assert statements are removed under `python -O`.
    sys.exit('prepare.py: ' + msg)


def main():
    m = json.loads((root / 'manifest.json').read_text())
    if not src_path.is_file():
        fail(f'{src_path.name} not found next to manifest.json')
    if sha256_file(src_path) != m['gzip_sha256']:
        fail('compressed checksum mismatch; re-download nfl_matchups.sqlite.gz')
    data.mkdir(exist_ok=True)
    tmp = out_path.with_suffix('.sqlite.tmp')
    try:
        with gzip.open(src_path, 'rb') as src, tmp.open('wb') as dst:
            shutil.copyfileobj(src, dst)
        if sha256_file(tmp) != m['sqlite_sha256']:
            fail('SQLite checksum mismatch after decompression')
        os.replace(tmp, out_path)  # only a verified file ever lands at the final path
    finally:
        tmp.unlink(missing_ok=True)
    print(f'Verified database: data/{out_path.name}')


if __name__ == '__main__':
    main()
