"""Verify the public GitHub download against this local snapshot manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

BASE='https://raw.githubusercontent.com/GhostPapii21/nfl-matchup-database/main/'
def verify(root):
    local=json.loads((Path(root)/'manifest.json').read_text())
    req=urllib.request.Request(BASE+'manifest.json',headers={'Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=30) as f:remote=json.load(f)
    for key in ('gzip_sha256','sqlite_sha256','tables'):
        if remote.get(key)!=local.get(key):raise ValueError('Remote snapshot differs: '+key)
    h=hashlib.sha256();size=0
    with urllib.request.urlopen(BASE+'nfl_matchups.sqlite.gz',timeout=60) as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk);size+=len(chunk)
    if h.hexdigest()!=local['gzip_sha256'] or size!=local['gzip_bytes']:
        raise ValueError('Public download checksum/size mismatch')
    return {'status':'PUBLICATION_VERIFIED','gzip_sha256':h.hexdigest(),'games':local['tables']['games'],'bytes':size}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',default=str(Path(__file__).resolve().parent));a=p.parse_args()
    print(json.dumps(verify(a.root),indent=2))
