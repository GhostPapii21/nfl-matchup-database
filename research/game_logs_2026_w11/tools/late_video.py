"""MIN@SF (late SNF) video-attributed coverage rows (source=video). Hand-checked from official captions. refs NFL-56, NFL-49."""
import os, json, re, datetime
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOWS = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p ' + __import__('time').strftime('%Z'))
V1 = 'NFL YouTube ceMTl2eqYDA "Minnesota Vikings vs San Francisco 49ers Game Highlights | 2026 NFL Season Week 11 Mexico City Game", CC1 captions'
V2 = '49ers YouTube jsOA0SpFHM4 "San Francisco 49ers vs. Minnesota Vikings Highlights | Week 11", CC1 captions'
ROWS = [  # (game, play, defender, role, evidence)
 ('MIN@SF', 'Q2 14:13 Purdy 8-yd TD pass to G.Kittle (pbp names no defender)', 'Harrison Smith (MIN S)', 'Coverage defender on the TD (broadcast: "Purdy, slings it in. Kittle hangs on for the touchdown. Took it away from Harrison Smith.")', f'{V2}; same call in {V1}'),
 ('MIN@SF', 'Q2 2:09 Purdy 4-yd TD pass to M.Evans (pbp names no defender)', 'Harrison Smith (MIN S)', 'Coverage defender on the TD (broadcast: "From the 5, to the corner. For Evans... In the back corner working one-on-one against Harrison Smith.")', f'{V1}; same call in {V2}'),
]
NOTES = [
 ('MIN@SF', 'Q2 1:59 Ji\'Ayir Brown 18-yd INT return TD (pbp already names Brown: VERIFIED INT)', 'Ji\'Ayir Brown (SF S)', 'Broadcast: "Ji\'Ayir Brown in the middle... this slant coming right that way, and he had it read all the way." Adds the route (slant), no new credit.', V1),
 ('MIN@SF', 'Not tied to one pbp play (MIN 3rd-and-3 sequence)', 'Deommodore Lenoir (SF CB)', 'General note, no row: "Lenoir in that one-on-one responsibility has played really well... He\'s got Jefferson his side this time." Lenoir is also VERIFIED with 2 PBUs in pbp.', V1),
 ('MIN@SF', 'Q1 1:13 A.Jones 11-yd rush TD', 'Deommodore Lenoir (SF CB)', 'Run defense, not coverage: "He drove Lenoir into the end zone."', V1),
]
# assignments.md (keep earlier games' rows, replace MIN@SF rows on re-run)
p = f'{OUT}/video/assignments.md'; t = open(p).read()
t = '\n'.join(l for l in t.splitlines() if not l.startswith('| MIN@SF') and not l.startswith('Count:')).rstrip('\n')
t += '\n' + '\n'.join(f'| {g} | {pl} | {d} | {r} | {e}, retrieved {NOWS} |' for g, pl, d, r, e in ROWS + NOTES)
t += '\n\nCount: 1 coverage assignment verified by video (TB@DET), 1 run-defense note (PIT@PHI); MIN@SF: 2 coverage rows by video (source=video), 3 notes (1 adds route to a pbp-verified INT, 1 general CB note, 1 run-defense note).\n'
open(p, 'w').write(t)
# game file section + record counts
gp = f'{OUT}/MIN_at_SF.md'; g = open(gp).read()
S, E_ = '<!-- VIDEO-ROWS-START -->', '<!-- VIDEO-ROWS-END -->'
g = re.sub(re.escape(S) + r'.*?' + re.escape(E_) + r'\n?', '', g, flags=re.S)
sec = [S, '## Coverage defender from official video (source=video)', '',
       'The pbp text names no defender on either of these TD passes (no tackler on a TD), so the defender comes from official highlight captions. Label: **video (highlight transcript)**. ASR captions; the defender is named by the broadcast, not charted.', '',
       '| Play | Defender | Source | Caption |', '|---|---|---|---|']
sec += [f'| {pl} | {d} | video | {r} |' for _, pl, d, r, _e in ROWS]
sec += ['', 'Other caption notes (no new coverage row): ' + ' | '.join(f'{d}: {r}' for _, pl, d, r, _e in NOTES), '',
        f'Evidence count after video: 6 VERIFIED (PBU/INT/DPI-named), 47 tackler-not-coverage (inferred), 2 video, 13 unattributed. Sources: {V1}; {V2}; retrieved {NOWS}.',
        'Broadcast (NBC) also notes the altitude ("a mile and a third high... Estadio Banorte, the highest stadium to host an NFL game"); captions do not mention rain.',
        'Weather effect: Open-Meteo model (raw/wx_401873077.json, venue coords 19.3029,-99.1505) shows light rain 0.012 in/hr at 01Z and 02Z, 0.0 by 03Z, 60-61 F, wind 2 mph (gusts 8-14). ESPN gameInfo has no weather block and no stadium observation exists in free data; no pbp or caption reference to rain or a wet ball, so any effect on the game is unknown (not evidenced).', E_, '']
g = g.replace('## Not available from free sources', '\n'.join(sec) + '\n## Not available from free sources')
open(gp, 'w').write(g)
for fn in (f'{OUT}/data/MIN_at_SF.json',):
    r = json.load(open(fn)); r.setdefault('assign_counts', {})['video'] = 2; r['assign_counts']['unattributed_after_video'] = r['assign_counts'].get('unattributed', 0) - 2
    r['video_rows'] = [dict(zip(('game', 'play', 'defender', 'role', 'source'), x)) for x in ROWS]; json.dump(r, open(fn, 'w'), indent=1, default=str)
G = json.load(open(f'{OUT}/data/_all_games.json'))
for r in G:
    if r['game'] == 'MIN@SF': r.setdefault('assign_counts', {})['video'] = 2; r['assign_counts']['unattributed_after_video'] = r['assign_counts'].get('unattributed', 0) - 2
json.dump(G, open(f'{OUT}/data/_all_games.json', 'w'), indent=1, default=str)
print('ok')
