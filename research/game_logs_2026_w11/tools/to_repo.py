"""Copy logs into the repo worktree and add W11 rows/sections to the defense DB. refs NFL-56, NFL-49."""
import os, shutil, glob, csv, json, re, datetime
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); WT = '/tmp/nfl56-w11-logs'
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
orig = subprocess.run(['git', '-C', WT, 'show', 'HEAD:data/redistributable/teams/defense/defense_db.csv'], capture_output=True).stdout.decode('utf-8')
fields = next(csv.reader(io.StringIO(orig.splitlines()[0])))
new = list(csv.DictReader(open(f'{OUT}/data/defense_db_w11_rows.csv'))) if os.path.exists(f'{OUT}/data/defense_db_w11_rows.csv') else []
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
