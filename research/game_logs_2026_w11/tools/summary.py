"""INDEX.md (headlines) + COVERAGE_MATRIX.md. refs NFL-56, NFL-49."""
import json, os, datetime, glob
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOWS = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p AST')
G = json.load(open(f'{OUT}/data/_all_games.json'))
sb = json.load(open(f'{OUT}/raw/scoreboard.json'))
started = {r['game'] for r in G}
I = [f'# Week 11 game logs - index (built {NOWS}, Blitz, refs NFL-56, refs NFL-49)', '', 'Research only. projection_ready stays false. No picks. Sources and pull times are inside each game file.', '',
     '| Game | Status | Quarter winners (Q1-Q4) | 1H | Close (AN consensus) | ATS | Total | RZ trips (TD) | Game target leader | Most yds on a named defender (tackler tag, inferred) | Most VERIFIED-PBU/INT/DPI credits | Verified / tackler / unattributed pass plays |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in G:
    q = ', '.join(f'{l} {w}' for l, w, a, h in r['quarters'][:5]); a1, h1 = r['first_half']; away, home = r['game'].split('@')
    ats = r.get('ats', {})
    rz = '; '.join(f"{t} {len(v['trips'])} ({sum(1 for x in v['trips'] if x == 'Touchdown')})" for t, v in r.get('red_zone', {}).items())
    tl = r.get('game_target_leader'); mb = r.get('most_beaten', {})
    ac = r.get('assign_counts', {})
    I.append(f"| {r['game']} | {r['status'].split(' - partial')[0]} | {q} | {away if a1>h1 else home if h1>a1 else 'TIE'} {a1}-{h1} | {home} {ats.get('home_spread','unknown')}, {ats.get('total_line','unknown')} | {ats.get('cover','unknown') if 'FINAL' in r['status'] else 'n/a (in progress)'} | {ats.get('total','?')} {ats.get('total_res','unknown') if 'FINAL' in r['status'] else '(in progress)'} | {rz} | {f'{tl[1]} ({tl[0]}) {tl[2]}' if tl else 'unknown'} | {'; '.join(f'{t}: {v[0]} {v[1]}-{v[2]}' for t, v in mb.items())} | {'; '.join((f'{t}: {v[0]} PBU {v[1]}/INT {v[2]}/DPI {v[3]}' if v else f'{t}: none named') for t, v in r.get('most_verified', {}).items())} | {ac.get('verified')}/{ac.get('tackler_inferred')}/{ac.get('unattributed')} |")
ns = [e['shortName'] + ' (' + e['status']['type']['shortDetail'] + ')' for e in sb['events'] if e['status']['type']['name'] != 'STATUS_FINAL']
I += ['', 'Not logged in this run (not final at pull time; a later run logs them): ' + ', '.join(ns), '',
      'Files: one `<AWAY>_at_<HOME>.md` per game, `pbp/` full play-by-play CSVs, `data/` JSON (pass-play defender log per game), DEFENSE_PROFILES.md, NGS_W11_SNAPSHOT.md, VIDEO_EVIDENCE.md, SLIP_LEG_RESULTS.md, COVERAGE_MATRIX.md, EXTRAS_TO_CAPTURE.md.']
open(f'{OUT}/INDEX.md', 'w').write('\n'.join(I) + '\n')
FIELDS = [('Quarter scores, quarter/1H/2H winners', lambda r: 'filled'), ('Q2 leader track', lambda r: 'filled' if r.get('q2_leaders') else 'unknown'),
          ('Full-game close spread/total + ATS/total result', lambda r: 'filled' if r.get('ats') else 'unknown'),
          ('Per-period (Q1-Q4/1H/2H) lines + results', lambda r: 'filled' if all((r.get('periods', {}).get(p, {}).get('line') or {}).get('home_spread') is not None for p in ('Q1', 'Q2', 'Q3', 'Q4', '1H', '2H') if p in r.get('periods', {})) and r.get('periods') else 'partial'),
          ('Scoring plays + breakdown (rush/rec/QB rush/DST/FG)', lambda r: 'filled'), ('Full pbp, play count reconciles to ESPN', lambda r: 'filled' if all(v[2] for v in r.get('play_recon', {}).values()) else 'MISMATCH'),
          ('3rd/4th down, RZ trips + usage, TOP, drives', lambda r: 'filled'), ('Turnovers + rate', lambda r: 'filled'),
          ('Targets/rec/catch%/yds/target share for every WR/TE/RB with a target', lambda r: 'filled'), ('Carries/rush yds/carry share', lambda r: 'filled'),
          ('Defender on pass plays', lambda r: f"partial: {r['assign_counts']['verified']} verified (PBU/INT/DPI), {r['assign_counts']['tackler_inferred']} tackler-only, {r['assign_counts']['unattributed']} unattributed"),
          ('Defense leaks by position (TE/WR/RB)', lambda r: 'filled; WR slot vs outside unknown'), ('QB vs man/zone, blitz, MOF shell, pressure', lambda r: 'unknown (no free charting)'),
          ('Weather (ESPN + Open-Meteo kickoff hour)', lambda r: 'filled' if r.get('weather') or r.get('weather_openmeteo') else 'unknown (indoor/neutral)'),
          ('Explosives, sack rate, QB-hit proxy, early-down pass rate, completed air/YAC, penalties, injuries, garbage-time flag', lambda r: 'filled (pressure rate = QB-hit proxy only)'),
          ('Intended air yards (incl. incompletions)', lambda r: 'unknown until nflverse overnight rebuild'), ('Snap shares', lambda r: 'unknown until snap counts post (Mon-Tue)'),
          ('NGS separation/cushion/RYOE', lambda r: 'partial live snapshot (threshold players only); route trees unknown'),
          ('Video defender evidence', lambda r: 'checked' if r['game'] in json.load(open(f'{OUT}/video/evidence.json')) else 'not available yet (official highlights not posted at pull time)')]
C = [f'# Field coverage per game (built {NOWS})', '', '| Field | ' + ' | '.join(r['game'] + (' (IN PROGRESS)' if 'FINAL' not in r['status'] else '') for r in G) + ' |', '|' + '---|' * (len(G) + 1)]
for name, f in FIELDS:
    C.append(f'| {name} | ' + ' | '.join(f(r) for r in G) + ' |')
open(f'{OUT}/COVERAGE_MATRIX.md', 'w').write('\n'.join(C) + '\n')
print('\n'.join(I))
