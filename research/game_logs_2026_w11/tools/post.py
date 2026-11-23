"""Post-processing: NGS snapshot, slip-leg results, DEFENSE_PROFILES.md, INDEX.md, defense_db rows. refs NFL-56, NFL-49."""
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import json, glob, os, re, csv, collections, datetime, urllib.request
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RAW = f'{OUT}/raw'
NOWS = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p AST')
G = {r['game']: r for r in json.load(open(f'{OUT}/data/_all_games.json'))}
# ---------- NGS
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://nextgenstats.nfl.com/'}
L = [f'# Next Gen Stats, Week 11 statboard snapshot (pulled {NOWS})', '',
     'Source: nextgenstats.nfl.com public statboard API (receiving/rushing/passing, season 2026 REG week 11). **This is a live, partial snapshot**: NGS applies a minimum-volume threshold and games in progress are included mid-game. Re-pull Monday for final values.',
     'Not available publicly: per-player route trees / routes run by route type, alignment (slot/outside), coverage faced. NGS route charts exist as images on nextgenstats.nfl.com/charts but no public data endpoint; TODO Monday: re-pull statboard and check charts pages for W11.', '']
name2team = {}
for g, r in G.items():
    for t, pl in r.get('players', {}).items():
        for n in pl: name2team[n] = t
for kind, cols in (('receiving', ['targets', 'receptions', 'yards', 'recTouchdowns', 'catchPercentage', 'avgSeparation', 'avgCushion', 'avgIntendedAirYards', 'percentShareOfIntendedAirYards', 'avgYAC', 'avgYACAboveExpectation']),
                   ('rushing', ['rushAttempts', 'rushYards', 'expectedRushYards', 'rushYardsOverExpected', 'rushYardsOverExpectedPerAtt', 'rushPctOverExpected', 'percentAttemptsGteEightDefenders', 'avgTimeToLos', 'efficiency']),
                   ('passing', ['attempts', 'completions', 'passYards', 'avgTimeToThrow', 'avgCompletedAirYards', 'avgIntendedAirYards', 'aggressiveness', 'completionPercentageAboveExpectation', 'maxCompletedAirDistance'])):
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://nextgenstats.nfl.com/api/statboard/{kind}?season=2026&seasonType=REG&week=11', headers=UA), timeout=30).read())
        json.dump(d, open(f'{RAW}/ngs_{kind}.json', 'w'))
    except Exception as e:
        L.append(f'## {kind}: unknown (pull failed: {e})'); continue
    L += [f'## {kind} ({len(d["stats"])} players over NGS threshold)', '', '| Player | Team (from ESPN box) | ' + ' | '.join(cols) + ' |', '|' + '---|' * (len(cols) + 2)]
    for s in d['stats']:
        def fmt(v): return f'{v:.2f}' if isinstance(v, float) else ('unknown' if v is None else str(v))
        L.append(f"| {s['playerName']} | {name2team.get(s['playerName'], 'unknown')} | " + ' | '.join(fmt(s.get(c)) for c in cols) + ' |')
    L.append('')
open(f'{OUT}/NGS_W11_SNAPSHOT.md', 'w').write('\n'.join(L) + '\n')
# ---------- slip legs
def per(g, lab):
    r = G.get(g); return (r or {}).get('periods', {}).get(lab), r
def total_leg(g, lab, line, side='U'):
    p, r = per(g, lab)
    if not r: return 'pending (game not started)', None
    if not p or p.get('in_progress') or 'FINAL' not in r['status'] and lab in ('FULL', '2H', 'Q4'): pass
    if lab == 'FULL':
        if 'FINAL' not in r['status']: return 'pending (in progress)', None
        a, h = r['periods']['1H']['away'] + r['periods']['2H']['away'], r['periods']['1H']['home'] + r['periods']['2H']['home']
    else:
        if not p: return 'pending', None
        if p.get('in_progress'): return 'pending (period in progress)', None
        a, h = p['away'], p['home']
    t = a + h; res = 'PUSH' if t == line else ('WIN' if (t < line) == (side == 'U') else 'LOSS')
    return res, f'{t} pts'
def spread_leg(g, lab, team, line):
    p, r = per(g, lab)
    if not r: return 'pending', None
    if lab == 'FULL':
        if 'FINAL' not in r['status']: return 'pending (in progress)', None
        a, h = r['periods']['1H']['away'] + r['periods']['2H']['away'], r['periods']['1H']['home'] + r['periods']['2H']['home']
    else:
        if not p or p.get('in_progress'): return 'pending', None
        a, h = p['away'], p['home']
    away, home = g.split('@'); m = (h - a if team == home else a - h) + line
    return ('PUSH' if m == 0 else 'WIN' if m > 0 else 'LOSS'), f'{away} {a} - {home} {h}'
def rush_leg(g, team, player, line, side):
    r = G.get(g)
    if not r: return 'pending', None
    if 'FINAL' not in r['status']: return 'pending (in progress)', None
    v = r['players'].get(team, {}).get(player, {})
    if 'rush_yds' not in v: return 'unknown (player not in rushing box)', None
    y = int(v['rush_yds']); res = 'PUSH' if y == line else ('WIN' if (y < line) == (side == 'U') else 'LOSS')
    return res, f'{y} yds on {v.get("car")} car'
LEGS = {'S1': [('NO@CHI U47.5', lambda: total_leg('NO@CHI', 'FULL', 47.5)), ('TB@DET U48.5', lambda: total_leg('TB@DET', 'FULL', 48.5)), ('Henry rush U67.5 (DK)', lambda: rush_leg('BAL@CAR', 'BAL', 'Derrick Henry', 67.5, 'U'))],
        'S2': [('Swift rush O64.5', lambda: rush_leg('NO@CHI', 'CHI', "D'Andre Swift", 64.5, 'O')), ('DET 1H -2.5', lambda: spread_leg('TB@DET', '1H', 'DET', -2.5)), ('CIN@WAS U54.5 (MNF)', lambda: total_leg('CIN@WSH', 'FULL', 54.5))],
        'S3': [('NO@CHI Q2 U14.5 (stale FD)', lambda: total_leg('NO@CHI', 'Q2', 14.5)), ('TB@DET 1H U24.5', lambda: total_leg('TB@DET', '1H', 24.5)), ('CIN@WAS Q2 U16.5 (MNF, stale FD)', lambda: total_leg('CIN@WSH', 'Q2', 16.5))],
        'S4': [('NO@CHI alt U49.5', lambda: total_leg('NO@CHI', 'FULL', 49.5)), ('TB@DET alt U50.5', lambda: total_leg('TB@DET', 'FULL', 50.5)), ('CIN@WAS alt U56.5 (MNF)', lambda: total_leg('CIN@WSH', 'FULL', 56.5)),
               ('DET -3.5', lambda: spread_leg('TB@DET', 'FULL', 'DET', -3.5)), ('NO@CHI 1H U25.5', lambda: total_leg('NO@CHI', '1H', 25.5)), ('TB@DET Q2 U13.5 (stale FD)', lambda: total_leg('TB@DET', 'Q2', 13.5))],
        'S5': [('NO@CHI alt U48.5', lambda: total_leg('NO@CHI', 'FULL', 48.5)), ('TB@DET alt U49.5', lambda: total_leg('TB@DET', 'FULL', 49.5)), ('CIN@WAS alt U55.5 (MNF)', lambda: total_leg('CIN@WSH', 'FULL', 55.5)),
               ('CIN@WAS Q2 U16.5 (MNF)', lambda: total_leg('CIN@WSH', 'Q2', 16.5)), ('NO@CHI 1H U24.5', lambda: total_leg('NO@CHI', '1H', 24.5)), ('TB@DET 1H U25.5', lambda: total_leg('TB@DET', '1H', 25.5)), ('DET 1H -2.5', lambda: spread_leg('TB@DET', '1H', 'DET', -2.5))],
        'FOCUS9 Saved Slip 4 (uncleared, paper only; runs/2026-11-22_W11_FOCUS9/SAVED_UNCLEARED_SLIPS.md)': [('MIN@SF 1H U23.5 (DK -112, VegasInsider Sat 5:00 PM AST)', lambda: total_leg('MIN@SF', '1H', 23.5))],
        'MIN@SF excluded read (not on a slip; PAPER_SLIPS SLIPS.md Excluded)': [('MIN@SF U46.5 (excluded: model 48% vs 53.5% no-vig)', lambda: total_leg('MIN@SF', 'FULL', 46.5))],
        'FLAG (not on a slip)': [('JAX@NYG U45.5', lambda: total_leg('JAX@NYG', 'FULL', 45.5)), ('JAX@NYG U47.5 (flag only)', lambda: total_leg('JAX@NYG', 'FULL', 47.5))]}
S = [f'# Paper slip legs vs results (unofficial check, pulled {NOWS})', '', 'Paper only; the official grade is the 11:45 PM ET grading routine. Legs from runs/2026-11-22_W11_PAPER_SLIPS/SLIPS.md (Ghost6-vetted version). Results from ESPN summary JSON.', '']
for s, legs in LEGS.items():
    S += [f'## {s}', '| Leg | Result | Actual |', '|---|---|---|']
    out = []
    for n, f in legs:
        res, act = f(); out.append(res); S.append(f'| {n} | {res} | {act or ""} |')
    st = 'LOSS' if 'LOSS' in out else ('WIN' if all(x in ('WIN', 'PUSH') for x in out) else 'pending')
    S += [f'Slip status: **{st}**', '']
open(f'{OUT}/SLIP_LEG_RESULTS.md', 'w').write('\n'.join(S) + '\n')
print('\n'.join(S))
# ---------- defense profiles
sb = json.load(open(f'{RAW}/scoreboard.json'))
ab2id = {}
for e in sb['events']:
    for c in e['competitions'][0]['competitors']: ab2id[c['team']['abbreviation']] = c['team']['id']
def rmap(team):
    fn = f"{RAW}/roster_{ab2id.get(team)}.json"
    m = {}
    if not os.path.exists(fn): return m
    for g in json.load(open(fn)).get('athletes', []):
        for a in g['items']:
            f_, l_ = a.get('firstName', ''), a.get('lastName', '')
            for k in {f'{f_[:1]}.{l_}', f'{f_[:2]}.{l_}'}: m.setdefault(k, []).append((a['displayName'], a.get('position', {}).get('abbreviation', 'unknown')))
            m.setdefault('LAST:' + l_, []).append((a['displayName'], a.get('position', {}).get('abbreviation', 'unknown')))
    return m
def who(m, short):
    c = m.get(short)
    if c and len(c) == 1: return c[0]
    if not c and '.' in short:
        c2 = m.get('LAST:' + short.split('.', 1)[1])
        if c2 and len(c2) == 1: return (c2[0][0] + ' (last-name match)', c2[0][1])
    return (short + ' (name unresolved)', 'unknown')
VID = {}
if os.path.exists(f'{OUT}/video/evidence.json'): VID = json.load(open(f'{OUT}/video/evidence.json'))
P = [f'# Defensive coverage profiles from Week 11 games (built {NOWS} by Blitz, refs NFL-56)', '',
     'Sources: ESPN summary JSON play text (per game, pull time in each game file), ESPN team rosters for names/positions, official NFL YouTube highlight auto-captions where noted (labeled video). No PFF/FTN paid content.',
     '**Evidence levels:** VERIFIED = play text names the defender who broke up/intercepted the pass or was flagged for DPI. tackler = defender named as tackler on a completion (not proof of coverage). video = a highlight-commentary mention (auto-captions; names can be misspelled). Man/zone, blitz and MOF shell per play are **unknown** in free data.', '']
import cov_rates as CR
CD = CR.load()
P += ['## Season coverage rates, all 32 teams (public; StatRankings primary, Sharp cross-check; never mixed)', '',
      f'StatRankings = {CR.SR_TAG}. Sharp = {CR.SH_TAG}. Copies of the source CSV and source log: sources/team_coverage_rates.csv, sources/COVERAGE_SOURCES.md.', '',
      '| Team | Man SR / Sharp | Zone SR / Sharp | MOF closed SR / Sharp | MOF open SR / Sharp | Blitz SR / Sharp | Flags |', '|---|---|---|---|---|---|---|']
for ab in sorted(CD):
    sr, sh = CD[ab].get('SR'), CD[ab].get('SH')
    fl = CR.flags(ab, CD); ol = CR.outliers(ab, CD)
    P.append(f'| {ab} | ' + ' | '.join(f'{CR.v(sr, k)} / {CR.v(sh, k)}' for k, _ in CR.CORE) + ' | ' + (('7+ pts: ' + ', '.join(f'{x[0]} {x[3]:+}' for x in fl)) if fl else '') + ((' ; OUTLIER: ' + ', '.join(x[0] for x in ol)) if ol else '') + ' |')
P += ['', '**Systematic gap between the sources** (definitions differ; this is why they are never averaged):', '', CR.offsets_md(CD), '',
      'Because StatRankings man is higher than Sharp for all 32 teams, a raw 7+ point man gap is common. The OUTLIER flag marks gaps 2+ SD from the league-median gap, or ranks 10+ apart, which is the disagreement worth checking.', '']
rows_csv = []
for g, r in sorted(G.items()):
    away, home = g.split('@'); st = r['status']
    for de, off in ((away, home), (home, away)):
        m = rmap(de)
        P.append(f'## {de} defense vs {off} ({g}, {st.split(" -")[0]})\n')
        ds = [(k.split('|', 1)[1], v) for k, v in r.get('defenders', {}).items() if k.startswith(de + '|')]
        P.append('| Defender | Pos | Tags | Rec allowed | Yds | TD | PBU | INT | DPI | Evidence | Receivers | 20+ allowed |'); P.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for short, v in sorted(ds, key=lambda x: -x[1]['yds']):
            full, pos = who(m, short); ev = 'VERIFIED x%d' % (v['pbu'] + v['int'] + v['dpi']) if (v['pbu'] + v['int'] + v['dpi']) else ''
            ev = ', '.join(x for x in (ev, 'tackler x%d' % v['rec'] if v['rec'] else '') if x)
            rc = ', '.join(f'{k} {n}' for k, n in v['vs'].items())
            P.append(f"| {full} | {pos} | {v['tags']} | {v['rec']} | {v['yds']} | {v['td']} | {v['pbu']} | {v['int']} | {v['dpi']} | {ev} | {rc} | {'; '.join(v['big'])} |")
            if 'FINAL' in st:
                rows_csv.append({'team': de, 'defender': full.replace(' (last-name match)', '').replace(' (name unresolved)', ''), 'short': short, 'gsis_id': '', 'pos': pos, 'scope': 'game', 'week': '11', 'game': g, 'games': '1',
                                 'tags': v['tags'], 'rec': float(v['rec']), 'yds': float(v['yds']), 'ypt': round(v['yds'] / v['tags'], 2) if v['tags'] else '', 'td': v['td'], 'exp20': len(v['big']), 'pbu': v['pbu'], 'ints': v['int'], 'dpi': v['dpi'],
                                 'tags_pg': float(v['tags']), 'yds_pg': float(v['yds']), 'def_snap_pct': '', 'receivers': ', '.join(f'{k}x{n}' for k, n in v['vs'].items()), 'explosives': '; '.join(v['big']),
                                 'method': 'tackler/PBU tag, not true coverage (W11 ESPN play text, refs NFL-56); only pbu/ints/dpi are VERIFIED coverage, rec/yds are inferred tackler tags'})
        lk = r.get('leaks', {}).get(de, {})
        P.append('\nYards allowed by target position (WR slot/outside unknown): ' + ('; '.join(f'{k} {v[1]}/{v[0]} for {v[2]} yds, {v[3]} TD' for k, v in sorted(lk.items(), key=lambda kv: -kv[1][2])) or 'none'))
        ex = r.get('extras', {}).get('explosives_allowed', {}).get(de)
        P.append(f'Explosives allowed (pass 20+/rush 15+): {ex["pass20"]}/{ex["rush15"]}' if ex else 'Explosives allowed: unknown')
        sk = {k.split('|')[1]: v for k, v in r.get('sacks', {}).items() if k.startswith(de + '|')}; hh = {k.split('|')[1]: v for k, v in r.get('qb_hits', {}).items() if k.startswith(de + '|')}
        P.append('Pass rush: sacks ' + (', '.join(f'{k} {v}' for k, v in sk.items()) or 'none') + '; QB hits ' + (', '.join(f'{k} {v}' for k, v in hh.items()) or 'none'))
        vv = VID.get(g, {}).get(de, [])
        P.append('Video (highlight transcript) mentions: ' + ('; '.join(vv) if vv else 'none found / not checked'))
        P.append('Man/zone, blitz rate, MOF shell this game: unknown (no free play-level charting).\n')
        P.append(CR.block(de, CD, '####') + '\n')
open(f'{OUT}/DEFENSE_PROFILES.md', 'w').write('\n'.join(P) + '\n')
with open(f'{OUT}/data/defense_db_w11_rows.csv', 'w', newline='') as f:
    if rows_csv:
        w = csv.DictWriter(f, fieldnames=list(rows_csv[0].keys())); w.writeheader(); w.writerows(rows_csv)
print('defense rows', len(rows_csv))
