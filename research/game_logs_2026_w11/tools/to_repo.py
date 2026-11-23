"""Copy logs into the repo worktree and add W11 rows/sections to the defense DB. refs NFL-56, NFL-49."""
import os, shutil, glob, csv, json, re, datetime
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); WT = os.environ.get('WT', '/tmp/nfl56-w11-logs')
DST = f'{WT}/research/game_logs_2026_w11'
if os.path.exists(DST): shutil.rmtree(DST)
os.makedirs(DST)
for f in glob.glob(f'{OUT}/*.md'): shutil.copy(f, DST)
os.makedirs(f'{DST}/video', exist_ok=True); shutil.copy(f'{OUT}/video/assignments.md', f'{DST}/video/')
for sub in ('pbp', 'data', 'tools'):
    shutil.copytree(f'{OUT}/{sub}', f'{DST}/{sub}', ignore=shutil.ignore_patterns('__pycache__'))
# raw ESPN JSON kept out of git (size); list what was pulled
open(f'{DST}/RAW_SOURCES.md', 'w').write('# Raw pulls (kept on the box, not committed)\n\n' + '\n'.join(f'- {os.path.basename(f)} ({os.path.getsize(f)//1024} KB, mtime {datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %I:%M %p AST")})' for f in sorted(glob.glob(f'{OUT}/raw/*.json'))) + '\n\nBox path: /workspace/runs/2026-11-22_W11_GAME_LOGS/raw/\n')
# defense_db.csv: append W11 game rows (FINAL games only), replacing any earlier W11 rows from this builder
dbp = f'{WT}/data/redistributable/teams/defense/defense_db.csv'
import subprocess, io
# base = the file as it is on the merge-base with origin/main. Re-runs and late-game runs dedupe by row key, so rows
# already on main (e.g. the 11 games merged in PR #106) are never re-appended.
base = subprocess.run(['git', '-C', WT, 'merge-base', 'HEAD', 'origin/main'], capture_output=True, text=True).stdout.strip()
orig = subprocess.run(['git', '-C', WT, 'show', f'{base}:data/redistributable/teams/defense/defense_db.csv'], capture_output=True).stdout.decode('utf-8')
assert orig, 'could not read base defense_db.csv'
fields = next(csv.reader(io.StringIO(orig.splitlines()[0])))
KEY = lambda r: (r.get('team', ''), r.get('short', ''), r.get('defender', ''), r.get('scope', ''), str(r.get('week', '')), r.get('game', ''))
def _rows_to_csv(rows, fields):
    b = io.StringIO(); w = csv.DictWriter(b, fieldnames=fields, lineterminator='\n'); w.writerows(rows); return [b.getvalue()]
base_rows = list(csv.DictReader(io.StringIO(orig))); have = {KEY(r) for r in base_rows}
base_games = {r.get('game') for r in base_rows if str(r.get('week')) == '11' and 'refs NFL-56' in r.get('method', '')}
cand = list(csv.DictReader(open(f'{OUT}/data/defense_db_w11_rows.csv'))) if os.path.exists(f'{OUT}/data/defense_db_w11_rows.csv') else []
# skip any game whose W11 builder rows are already on base (game-level dedupe), then any exact key already present
# 2026-11-23 Monday correction run (REPLACE_W11=1): the INT parser fix changes W11 builder rows already on main, so drop
# base W11 builder rows for the games being rebuilt and append the corrected rows (still deduped by key).
if os.environ.get('REPLACE_W11'):
    cand_games = {r.get('game') for r in cand}
    dropped = [r for r in base_rows if str(r.get('week')) == '11' and 'refs NFL-56' in r.get('method', '') and r.get('game') in cand_games]
    base_rows = [r for r in base_rows if r not in dropped]; have = {KEY(r) for r in base_rows}; base_games = set()
    print(f'REPLACE_W11: dropped {len(dropped)} earlier W11 builder rows for {len(cand_games)} games')
    orig = orig.splitlines()[0] + '\n' + ''.join(_rows_to_csv(base_rows, fields))
new = [r for r in cand if r.get('game') not in base_games and KEY(r) not in have]
print(f'defense_db.csv base rows {len(base_rows)} (W11 builder games on base: {len(base_games)}); candidate rows {len(cand)}; skipped as already on base {len(cand) - len(new)}; appended {len(new)}; after {len(base_rows) + len(new)}')
dup = len(base_rows) + len(new) - len({KEY(r) for r in base_rows} | {KEY(r) for r in new})
print('duplicate keys after merge:', dup)
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n'); w.writerows({k: r.get(k, '') for k in fields} for r in new)
open(dbp, 'wb').write((orig if orig.endswith('\n') else orig + '\n').encode('utf-8'))
open(dbp, 'a', newline='').write(buf.getvalue())
# team MD sections
prof = open(f'{OUT}/DEFENSE_PROFILES.md').read()
secs = re.split(r'\n(?=## )', prof)
MARK_S, MARK_E = '<!-- W11-GAMELOG-START refs NFL-56 -->', '<!-- W11-GAMELOG-END -->'
by_team = {}
for s in secs[1:]:
    m = re.match(r'## (\w+) defense vs (\w+) \((\S+), (FINAL|IN PROGRESS[^)]*)\)', s)
    if m and m.group(4) == 'FINAL': by_team.setdefault('WSH' if m.group(1) == 'WSH' else m.group(1), []).append(s.replace('## ', '### ', 1))
for t, ss in by_team.items():
    p = f'{WT}/data/redistributable/teams/defense/{t}.md'
    if not os.path.exists(p): print('no team file', t); continue
    txt = open(p).read()
    txt = re.sub(re.escape(MARK_S) + r'.*?' + re.escape(MARK_E) + r'\n?', '', txt, flags=re.S)
    txt = txt.rstrip('\n') + f'\n\n{MARK_S}\n## Week 11 game log (2026-11-22, ESPN play text; tackler/PBU tag, not true coverage)\n\nFull game file: research/game_logs_2026_w11/. Evidence levels: VERIFIED = PBU/INT/DPI-named; tackler = named tackler on a completion. Man/zone, blitz and MOF shell are unknown in free data.\n\n' + '\n'.join(ss) + f'\n{MARK_E}\n'
    open(p, 'w').write(txt)
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cov_rates as CR
CD = CR.load(); CS, CE = '<!-- W11-COVRATES-START refs NFL-56 -->', '<!-- W11-COVRATES-END -->'
cov_teams = []
for ab in sorted(CD):
    p = f'{WT}/data/redistributable/teams/defense/{ab}.md'
    if not os.path.exists(p): print('no team file for coverage', ab); continue
    txt = open(p).read(); txt = re.sub(re.escape(CS) + r'.*?' + re.escape(CE) + r'\n?', '', txt, flags=re.S)
    txt = txt.rstrip('\n') + f'\n\n{CS}\n' + CR.block(ab, CD, '##') + f'\n{CE}\n'
    open(p, 'w').write(txt); cov_teams.append(ab)
os.makedirs(f'{DST}/sources', exist_ok=True)
for f in glob.glob(f'{OUT}/sources/*'): shutil.copy(f, f'{DST}/sources/')
print('coverage-rate sections', len(cov_teams))
print('teams updated', sorted(by_team), 'db rows added', len(new))
