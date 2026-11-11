"""Read-only SQL access to the public NFL snapshot.

  python3 query.py --tables
  python3 query.py --schema games
  python3 query.py --sql 'SELECT game_id,date,status FROM games ORDER BY date DESC LIMIT 12'
  python3 query.py --sql 'SELECT * FROM games WHERE season = ?' --param 2026 --format csv
"""
import argparse, csv, json, pathlib, sqlite3, sys

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
g = p.add_mutually_exclusive_group()
g.add_argument('--tables', action='store_true', help='list tables and views')
g.add_argument('--schema', metavar='TABLE', help='show the columns of one table or view')
g.add_argument('--sql', help='a read-only SQL statement')
p.add_argument('--param', action='append', default=[], help='bind a value to the next ? placeholder (repeatable)')
p.add_argument('--format', choices=('json', 'csv'), default='json', help='output format (default json)')
p.add_argument('--db', default=str(pathlib.Path(__file__).resolve().parent / 'data/nfl_matchups.sqlite'), help=argparse.SUPPRESS)
a = p.parse_args()

dbpath = pathlib.Path(a.db)
if not dbpath.is_file():
    sys.exit(f'query.py: {dbpath} not found. Run `python3 prepare.py` first.')
db = sqlite3.connect(dbpath.resolve().as_uri() + '?mode=ro', uri=True)
db.row_factory = sqlite3.Row
db.execute('PRAGMA query_only=ON')

params = list(a.param)
if a.tables:
    sql = "SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY name"
elif a.schema:
    sql, params = "SELECT name, type, \"notnull\", pk FROM pragma_table_info(?)", [a.schema]
elif a.sql:
    sql = a.sql
else:
    p.error('Use --tables, --schema TABLE or --sql SELECT...')

try:
    cur = db.execute(sql, params)
except sqlite3.Error as e:
    sys.exit(f'query.py: {e}')
cols = [d[0] for d in cur.description or []]
rows = [dict(r) for r in cur]
if a.schema and not rows:
    sys.exit(f'query.py: no table or view named {a.schema!r}')


def plain(v):
    return v.hex() if isinstance(v, (bytes, bytearray, memoryview)) else v


if a.format == 'csv':
    w = csv.writer(sys.stdout)
    w.writerow(cols)
    w.writerows([plain(r[c]) for c in cols] for r in rows)
else:
    print(json.dumps([{k: plain(v) for k, v in r.items()} for r in rows], indent=2, default=str))
