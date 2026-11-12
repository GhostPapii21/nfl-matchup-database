import gzip
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from export_snapshot import build, digest

class ExportTests(unittest.TestCase):
    def test_redaction_consistency_and_change_detection(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'private.sqlite';out=root/'public'
            with sqlite3.connect(source) as db:
                db.execute('CREATE TABLE games(game_id,date,status,data)')
                db.execute('INSERT INTO games VALUES (?,?,?,?)',('1','2026-10-25','final',json.dumps({'path':'/Users/example/private/raw.json','stat':42})))
            before=digest(source)
            result=build(source,out)
            self.assertEqual(result['status'],'READY_TO_PUBLISH')
            self.assertEqual(before,digest(source))
            with gzip.open(out/'nfl_matchups.sqlite.gz','rb') as f:
                restored=root/'restored.sqlite';restored.write_bytes(f.read())
            with sqlite3.connect(restored) as db:
                payload=json.loads(db.execute('SELECT data FROM games').fetchone()[0])
                self.assertEqual(payload,{'path':'[local-path-removed]','stat':42})
            self.assertEqual(build(source,out)['status'],'UNCHANGED')
            (out/'nfl_matchups.sqlite.gz').write_bytes(b'corrupt')
            self.assertEqual(build(source,out)['status'],'READY_TO_PUBLISH')
            with sqlite3.connect(source) as db:db.execute("UPDATE games SET status='corrected'")
            self.assertEqual(build(source,out)['status'],'READY_TO_PUBLISH')

    def test_block_unknown_tables_and_credentials(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'private.sqlite';out=root/'public'
            with sqlite3.connect(source) as db:db.execute('CREATE TABLE secrets(value)')
            with self.assertRaisesRegex(ValueError,'Unexpected'):build(source,out)
            self.assertFalse((out/'manifest.json').exists())
            with sqlite3.connect(source) as db:
                db.execute('DROP TABLE secrets');db.execute('CREATE TABLE games(game_id,date,status,data)')
                db.execute('INSERT INTO games VALUES (?,?,?,?)',('1','2026-10-25','final','ghp_'+'a'*30))
            with self.assertRaisesRegex(ValueError,'Credential'):build(source,out)
            self.assertFalse((out/'nfl_matchups.sqlite.gz').exists())

if __name__=='__main__':unittest.main()
