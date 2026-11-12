"""Read-only SQL access to the public NFL snapshot."""
import argparse,json,pathlib,sqlite3
p=argparse.ArgumentParser();p.add_argument('--tables',action='store_true');p.add_argument('--sql');a=p.parse_args()
dbpath=pathlib.Path(__file__).resolve().parent/'data/nfl_matchups.sqlite'
db=sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row;db.execute('PRAGMA query_only=ON')
sql="SELECT name FROM sqlite_master WHERE type IN ('table','view') ORDER BY name" if a.tables else a.sql
if not sql:p.error('Use --tables or --sql SELECT...')
print(json.dumps([dict(r) for r in db.execute(sql)],indent=2))
