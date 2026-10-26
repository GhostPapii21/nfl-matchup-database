"""Build an audited public SQLite snapshot without modifying the source.

Usage: python3 export_snapshot.py --source /path/nfl_matchups.sqlite --output .
Requires only Python's standard library. Publishing is a separate authenticated step.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile

TABLES = {'games', 'plays', 'player_stats', 'profiles', 'external_fetches',
          'external_observations', 'external_profile_links', 'external_gaps',
          'external_rosters', 'espn_boxscores', 'historical_game_audits',
          'supplemental_records', 'supplemental_play_links', 'ngs_route_charts',
          'ngs_carry_charts', 'ngs_carry_visual_notes'}
LOCAL_PATH = re.compile(r'(?:/Users/|/private/var/folders/|/var/folders/|/tmp/)[^\s"\u0027<>]*')
SECRET = re.compile(r'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def clean(value):
    if SECRET.search(value):
        raise ValueError('Credential-like content found; publication blocked')
    return LOCAL_PATH.sub('[local-path-removed]', value)

def build(source, output, gaps=None, force=False):
    source, output = Path(source).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if source == output / 'nfl_matchups.sqlite':
        raise ValueError('Source must be separate from export destination')
    # A read transaction and SQLite backup include WAL data consistently.
    with tempfile.TemporaryDirectory(prefix='nfl-export-') as scratch:
        scratch = Path(scratch)
        backup = scratch / 'nfl_matchups.sqlite'
        with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src:
            with sqlite3.connect(backup) as dst:
                src.backup(dst)
        fingerprint = digest(backup)
        gap_text = clean(Path(gaps).read_text()) if gaps else None
        gap_hash = hashlib.sha256((gap_text or '').encode()).hexdigest()
        old_path = output / 'manifest.json'
        old = json.loads(old_path.read_text()) if old_path.exists() else {}
        archive = output / 'nfl_matchups.sqlite.gz'
        if (not force and old.get('source_fingerprint') == fingerprint
                and old.get('gap_sha256') == gap_hash and archive.exists()
                and digest(archive) == old.get('gzip_sha256')):
            return {'status': 'UNCHANGED', 'sqlite_sha256': old['sqlite_sha256']}
        db = sqlite3.connect(backup)
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
        if tables - TABLES:
            raise ValueError('Unexpected database tables; review before publication')
        counts = {}
        for table in sorted(tables):
            cols = [c[1] for c in db.execute(f'PRAGMA table_info("{table}")')]
            for row in db.execute(f'SELECT rowid,* FROM "{table}"').fetchall():
                updates = {}
                for name, value in zip(cols, row[1:]):
                    if isinstance(value, str):
                        new = clean(value)
                        if name in ('raw_path', 'image_path'):
                            new = ''
                        if new != value:
                            updates[name] = new
                if updates:
                    sql = f'UPDATE "{table}" SET ' + ','.join(f'"{k}"=?' for k in updates) + ' WHERE rowid=?'
                    db.execute(sql, list(updates.values()) + [row[0]])
            counts[table] = db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]
        db.commit()
        db.execute('VACUUM')
        if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('SQLite integrity check failed')
        if db.execute('PRAGMA foreign_key_check').fetchone():
            raise ValueError('SQLite foreign key check failed')
        for table in tables:
            for row in db.execute(f'SELECT * FROM "{table}"'):
                for value in row:
                    if isinstance(value, str) and (LOCAL_PATH.search(value) or SECRET.search(value)):
                        raise ValueError('Public-copy audit failed')
        dates = db.execute('SELECT min(date),max(date) FROM games').fetchone()
        schema = '\n\n'.join(r[0] + ';' for r in db.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY type,name"))
        db.close()
        compressed = scratch / 'nfl_matchups.sqlite.gz'
        with backup.open('rb') as f, compressed.open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', compresslevel=9, mtime=0) as g:
                shutil.copyfileobj(f, g)
        manifest = {
            'created_at': dt.datetime.now(dt.timezone.utc).isoformat(),
            'source_fingerprint': fingerprint, 'gap_sha256': gap_hash,
            'coverage': {'games': counts.get('games', 0), 'first_date': dates[0], 'last_date': dates[1]},
            'tables': counts, 'sqlite_bytes': backup.stat().st_size,
            'gzip_bytes': compressed.stat().st_size,
            'gzip_sha256': digest(compressed), 'sqlite_sha256': digest(backup),
            'privacy': 'Local paths removed; original media and raw webpage archives omitted.',
        }
        # Install only a fully validated package; manifest is installed last.
        os.replace(compressed, archive)
        (output / 'schema.sql').write_text(schema + '\n')
        if gap_text is not None:
            (output / 'DATA_GAPS.md').write_text(gap_text)
        temp_manifest = output / 'manifest.json.tmp'
        temp_manifest.write_text(json.dumps(manifest, indent=2) + '\n')
        os.replace(temp_manifest, old_path)
        return {'status': 'READY_TO_PUBLISH', 'manifest': manifest}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--gaps')
    p.add_argument('--force', action='store_true')
    a = p.parse_args()
    print(json.dumps(build(a.source, a.output, a.gaps, a.force), indent=2))
