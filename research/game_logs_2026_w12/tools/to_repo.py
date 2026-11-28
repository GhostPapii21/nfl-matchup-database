"""Copy the W12 GB@LAR log into the repo worktree; append GB@LAR rows to defense_db.csv (dedupe by row key, no other game touched);
add a W12 game-log section to GB.md and LAR.md only. refs NFL-56, NFL-49."""
import os, shutil, glob, csv, re, datetime, subprocess, io, time
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); WT = os.environ.get('WT', '/tmp/nfl56-w12-gblar')
DST = f'{WT}/research/game_logs_2026_w12'
if os.path.exists(DST): shutil.rmtree(DST)
os.makedirs(DST)
for f in glob.glob(f'{OUT}/*.md'): shutil.copy(f, DST)
for sub in ('pbp', 'data', 'tools', 'sources'):
    shutil.copytree(f'{OUT}/{sub}', f'{DST}/{sub}', ignore=shutil.ignore_patterns('__pycache__', '_grade_*.md'))
TZ = time.strftime('%Z')
open(f'{DST}/RAW_SOURCES.md', 'w').write('# Raw pulls (kept on the box, not committed)\n\n' + '\n'.join(
    f'- {os.path.relpath(f, OUT + "/raw")} ({os.path.getsize(f)//1024} KB, mtime {datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %I:%M %p " + TZ)})'
    for f in sorted(glob.glob(f'{OUT}/raw/*.json') + glob.glob(f'{OUT}/raw/nflverse/*'))) + '\n\nBox path: /workspace/runs/2026-11-26_W12_GBLAR/raw/\n')
dbp = f'{WT}/data/redistributable/teams/defense/defense_db.csv'
base = subprocess.run(['git', '-C', WT, 'merge-base', 'HEAD', 'origin/main'], capture_output=True, text=True).stdout.strip()
orig = subprocess.run(['git', '-C', WT, 'show', f'{base}:data/redistributable/teams/defense/defense_db.csv'], capture_output=True).stdout.decode('utf-8')
assert orig
fields = next(csv.reader(io.StringIO(orig.splitlines()[0])))
KEY = lambda r: (r.get('team', ''), r.get('short', ''), r.get('defender', ''), r.get('scope', ''), str(r.get('week', '')), r.get('game', ''))
base_rows = list(csv.DictReader(io.StringIO(orig))); have = {KEY(r) for r in base_rows}
base_games = {r.get('game') for r in base_rows if str(r.get('week')) == '12'}
cand = list(csv.DictReader(open(f'{OUT}/data/defense_db_w12_rows.csv')))
new = [r for r in cand if r.get('game') not in base_games and KEY(r) not in have]
dup = len(base_rows) + len(new) - len({KEY(r) for r in base_rows} | {KEY(r) for r in new})
print(f'defense_db.csv base rows {len(base_rows)}; W12 games already on base: {sorted(base_games)}; candidate {len(cand)}; appended {len(new)}; after {len(base_rows)+len(new)}; duplicate keys after merge: {dup}')
assert dup == 0
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n'); w.writerows({k: r.get(k, '') for k in fields} for r in new)
open(dbp, 'wb').write((orig if orig.endswith('\n') else orig + '\n').encode('utf-8')); open(dbp, 'a', newline='').write(buf.getvalue())
prof = open(f'{OUT}/DEFENSE_PROFILES.md').read(); secs = re.split(r'\n(?=## )', prof)
MS, ME = '<!-- W12-GAMELOG-START refs NFL-56 -->', '<!-- W12-GAMELOG-END -->'
by = {}
for s in secs[1:]:
    m = re.match(r'## (\w+) defense vs (\w+) \((\S+), (FINAL|IN PROGRESS[^)]*)\)', s)
    if m and m.group(4) == 'FINAL': by.setdefault(m.group(1), []).append(s.replace('## ', '### ', 1).replace('\n#### ', '\n#### ', 1))
for t, ss in by.items():
    p = f'{WT}/data/redistributable/teams/defense/{t}.md'
    if not os.path.exists(p): print('no team file', t); continue
    txt = re.sub(re.escape(MS) + r'.*?' + re.escape(ME) + r'\n?', '', open(p).read(), flags=re.S)
    txt = txt.rstrip('\n') + f'\n\n{MS}\n## Week 12 game log (GB@LAR, 2026-11-25, ESPN play text + nflverse; tackler/PBU tag, not true coverage)\n\nFull game file: research/game_logs_2026_w12/GB_at_LAR.md. Evidence levels: VERIFIED = PBU/INT/DPI-named; tackler = named tackler on a completion (inferred). Man/zone, blitz and MOF shell for this game are unknown (FTN charting not posted for week 12 at pull time). Snap shares: unknown until nflverse snap counts post.\n\n' + '\n'.join(ss) + f'\n{ME}\n'
    open(p, 'w').write(txt)
print('teams updated', sorted(by), 'db rows added', len(new))
