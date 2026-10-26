"""Verify and decompress the public snapshot using only Python's standard library."""
import gzip,hashlib,json,pathlib,shutil
root=pathlib.Path(__file__).resolve().parent
(root/'data').mkdir(exist_ok=True)
m=json.loads((root/'manifest.json').read_text())
p=root/'nfl_matchups.sqlite.gz'
assert hashlib.sha256(p.read_bytes()).hexdigest()==m['gzip_sha256'],'Compressed checksum mismatch'
with gzip.open(p,'rb') as src,(root/'data/nfl_matchups.sqlite').open('wb') as dst: shutil.copyfileobj(src,dst)
assert hashlib.sha256((root/'data/nfl_matchups.sqlite').read_bytes()).hexdigest()==m['sqlite_sha256'],'SQLite checksum mismatch'
print('Verified database: data/nfl_matchups.sqlite')
