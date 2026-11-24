import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from data_ingest.import_sharp_advanced_boxscores import run

class SharpAdvancedImportTests(unittest.TestCase):
    def test_dry_run_then_idempotent_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); data=root/"data"; data.mkdir()
            (data/"team_games.jsonl").write_text(json.dumps({
                "source_game_id":"2026_01_NE_SEA","season":2026,"week":1,"date":"2026-09-09",
                "team":"NE","opponent":"SEA","venue_role":"away","quarterback":"QB","metrics":{"epa":1.2},
                "source_generated_utc":"2026-11-24 02:15:25"
            })+"\n")
            (data/"team_quarters.jsonl").write_text(json.dumps({
                "source_game_id":"2026_01_NE_SEA","season":2026,"week":1,"date":"2026-09-09",
                "team":"NE","opponent":"SEA","venue_role":"away","quarter":1,"quarter_label":"Q1",
                "metrics":{"epa":0.4},"source_generated_utc":"2026-11-23 17:01:09"
            })+"\n")
            (data/"manifest.json").write_text(json.dumps({"source_generated_utc":"2026-11-24 02:15:25","metric_catalog":[
                {"key":"epa","group":"eff","label":"EPA per play","kind":"epa","num":"epa","den":"plays","hi_good":True},
                {"key":"p11","group":"run","label":"11 personnel","kind":"pct","num":"p11","den":"pers_n","hi_good":None}
            ]}))
            dbpath=root/"nfl.sqlite"
            with sqlite3.connect(dbpath) as db:
                db.execute("CREATE TABLE games(game_id TEXT PRIMARY KEY,date TEXT,status TEXT,data TEXT)")
                db.execute("INSERT INTO games VALUES(?,?,?,?)",("espn-1","2026-09-09","final",json.dumps({"home":"SEA","away":"NE"})))
                db.execute("""CREATE TABLE supplemental_records(
                    record_id TEXT PRIMARY KEY,dataset TEXT,game_id TEXT,team_id TEXT,player_id TEXT,
                    week INTEGER,source_url TEXT,retrieved_at TEXT,asset_updated_at TEXT,data TEXT)""")
            dry=run(dbpath,data,False)
            self.assertEqual(dry["status"],"DRY_RUN")
            self.assertEqual(dry["game_id_matches"],2)
            self.assertEqual(dry["metric_catalog_rows"],2)
            self.assertEqual(dry["source_rows"],4)
            first=run(dbpath,data,True)
            second=run(dbpath,data,True)
            self.assertEqual(first["sqlite_integrity"],"ok")
            self.assertEqual(second["existing_source_rows"],4)
            with sqlite3.connect(dbpath) as db:
                self.assertEqual(db.execute("SELECT count(*) FROM supplemental_records").fetchone()[0],4)
                self.assertEqual(db.execute("SELECT count(*) FROM supplemental_records WHERE dataset = 'sharp_advanced_boxscore_metric_catalog'").fetchone()[0],2)
                self.assertEqual(db.execute("SELECT count(DISTINCT game_id) FROM supplemental_records").fetchone()[0],1)

if __name__=="__main__":
    unittest.main()
