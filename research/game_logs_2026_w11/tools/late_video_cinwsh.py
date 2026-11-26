"""CIN@WSH (MNF) video-attributed coverage rows (source=video), hand-checked from official captions, plus line-time,
red-zone and weather notes. Same pattern as late_video.py (MIN@SF). refs NFL-56, NFL-49."""
import os, json, re, datetime, time
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOWS = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p ') + time.strftime('%Z')
V1 = 'NFL YouTube C3ZJX7on7OE "Cincinnati Bengals vs Washington Commanders Game Highlights | 2026 NFL Season Week 11", CC1 captions'
V2 = 'NFL YouTube uLyhvnGoWNA "Jayden Daniels Every Throw & Run | Week 11", CC1 captions'
G_ = 'CIN@WSH'
ROWS = [  # (game, play, defender, role, evidence)
 (G_, 'Q2 1:55 Burrow 31-yd TD pass deep left to T.Higgins (pbp names no defender)', 'Trey Amos (WSH CB)', 'Coverage defender on the TD (broadcast: "Burrow, going for it all. Higgins -- caught it! Touchdown! ... Trey Amos in coverage ... ends up catching it with one hand")', V1),
 (G_, 'Q3 2:45 3rd-and-4 Daniels pass incomplete deep left to T.Burks (pbp names no defender)', 'Dax Hill (CIN CB)', 'Coverage defender on the incompletion (broadcast: "Third down and four. Contact, no flags. Burks, covered by Dax Hill.")', f'{V1}; same call in {V2}'),
]
NOTES = [
 (G_, 'Q3 Trey Amos DPI on Ja\'Marr Chase (pbp already names Amos: VERIFIED DPI)', 'Trey Amos (WSH CB)', 'Broadcast: "Burrow, Chase, a lot of hand checking -- and a flag. A lot of contact with Trey Amos." Confirms the pbp DPI; no new credit.', V1),
 (G_, 'Q2 4:47 3rd-and-9 Daniels incomplete to S.Diggs (pbp already names J.Newton: VERIFIED PBU)', 'Josh Newton (CIN CB)', 'Broadcast: "Broken up! And good defensive play by Josh Newton. Got his hand in front of Stefon Diggs." Confirms the pbp PBU; no new credit.', f'{V1}; same call in {V2}'),
 (G_, 'Q1 9:01 3rd-and-11 Burrow incomplete to C.Young (pbp already names R.Douglas: VERIFIED PBU)', 'Rasul Douglas (WSH CB)', 'Broadcast: "This one is broken up, and there\'s Douglas again. That was Colbie Young." Confirms the pbp PBU; no new credit.', V1),
 (G_, 'Q4 6:48 Daniels 29-yd pass to S.Diggs (pbp tackler J.Newton)', 'Josh Newton (CIN CB)', 'Broadcast: "He\'s got Diggs! Good move as he runs around Newton." Adds that Diggs beat Newton after the catch; stays a tackler tag (inferred), no new credit.', V1),
 (G_, 'Q4 9:13 3rd-and-10 Burrow 3-yd pass to J.Chase (pbp tackler R.Douglas)', 'Rasul Douglas (WSH CB)', 'Broadcast: "Commanders showing blitz, here they come. Quick throw, Chase, long way to go, he will not get there, Rasul Douglas made the play." Tackle short of the sticks; stays a tackler tag.', V1),
 (G_, 'Q3 7:04 Burrow 4-yd TD pass to C.Young', 'Frankie Luvu (WSH LB)', 'Pass rush, not coverage: "Burrow out to his right, chased from behind -- Luvu didn\'t get there! Touchdown, Colbie Young!" No coverage defender named.', V1),
 (G_, 'Q4 0:23 Daniels 42-yd pass to A.Williams', 'none named', 'Broadcast: "The middle of the field open for that throw to take place." Shell/defender not named; no row.', V1),
]
BLITZ_NOTES = ['Q1 3:52 3rd-and-9 (Perine 17-yd catch, fumble out of bounds): "Nick Cross coming on the blitz."', 'Q4 9:13 3rd-and-10: "Commanders showing blitz, here they come."',
               'Q4 2:20 CIN drive: "Bringing pressure. They\'ve been most successful tonight when they\'ve blitzed Burrow."']
p = f'{OUT}/video/assignments.md'; t = open(p).read()
t = '\n'.join(l for l in t.splitlines() if not l.startswith(f'| {G_}') and not l.startswith('Count:')).rstrip('\n')
t += '\n' + '\n'.join(f'| {g} | {pl} | {d} | {r} | {e}, retrieved {NOWS} |' for g, pl, d, r, e in ROWS + NOTES)
t += '\n\nCount: 1 coverage assignment verified by video (TB@DET), 1 run-defense note (PIT@PHI); MIN@SF: 2 coverage rows by video (source=video), 3 notes (1 adds route to a pbp-verified INT, 1 general CB note, 1 run-defense note); CIN@WSH: 2 coverage rows by video (source=video), 7 notes (3 confirm pbp-verified PBU/DPI, 2 add context to tackler tags, 1 pass-rush note, 1 shell note with no defender).\n'
open(p, 'w').write(t)
gp = f'{OUT}/CIN_at_WSH.md'; g = open(gp).read()
r = json.load(open(f'{OUT}/data/CIN_at_WSH.json')); ac = r['assign_counts']
S, E_ = '<!-- VIDEO-ROWS-START -->', '<!-- VIDEO-ROWS-END -->'
g = re.sub(re.escape(S) + r'.*?' + re.escape(E_) + r'\n?', '', g, flags=re.S)
sec = [S, '## Coverage defender from official video (source=video)', '',
       'The pbp text names no defender on either of these plays (TD pass with no tackler; incompletion with no PBU), so the defender comes from official highlight captions. Label: **video (highlight transcript)**. Broadcast captions (CC1); the defender is named by the ESPN/ABC broadcast, not charted.', '',
       '| Play | Defender | Source | Caption |', '|---|---|---|---|']
sec += [f'| {pl} | {d} | video | {rr} |' for _, pl, d, rr, _e in ROWS]
sec += ['', 'Other caption notes (no new coverage row): ' + ' | '.join(f'{d}: {rr}' for _, pl, d, rr, _e in NOTES), '',
        'Blitz mentions in the broadcast (commentary, not charting; the game-level blitz rate stays unknown): ' + ' | '.join(BLITZ_NOTES), '',
        f"Evidence count after video: {ac['verified']} VERIFIED (PBU/INT/DPI-named), {ac['tackler_inferred']} tackler-not-coverage (inferred), {len(ROWS)} video, {ac['unattributed'] - len(ROWS)} unattributed. Sources: {V1}; {V2}; retrieved {NOWS}.",
        '',
        '## Late-run notes (CIN@WSH, MNF)', '',
        f'- Line time: Action Network rows are the last pre-game (is_live=false) line per book as served at the pull ({r["pulled"]}); AN does not stamp the line time, so the line time is "last pre-kick", kickoff 2026-11-23 8:15 PM EST (2026-11-24 01:15Z). ESPN pickcenter (DraftKings) CIN -6 (-116) / WSH +6 (-103), O/U 54.5 (o-107/u-112), ML CIN -290 / WSH +237; open (AN) WSH +1.5, 52.5. No Odds API call was made.',
        '- Red zone: ESPN box counts CIN 1-1 and WSH 1-4. The pbp snap list (any snap starting at or inside the opp 20) counts CIN 2 trips: drive 7 (15 plays, FG 38) had a snap at the WAS 20, which ESPN does not count as a red-zone trip. WSH 4 trips match ESPN (1 TD, 3 FG).',
        '- Red-zone TDs: CIN 1 (Q3 7:04, Joe Burrow 4-yd pass to Colbie Young, rec TD; drive 13); WSH 1 (Q2 0:12, Jacory Croskey-Merritt 1-yd rush, non-QB rush TD; drive 10). Tee Higgins 31-yd TD (Q2 1:55) started outside the red zone.',
        '- Third downs: pbp count reconciles to the ESPN box (CIN 4-12, WSH 2-10) after the MNF-run fix (skip non-snap rows such as Official Timeout; judge the conversion on the snap gain in the play text when a post-play penalty or a fumble out of bounds changes statYardage). Earlier W11 game files keep their committed counts.',
        '- Weather effect: Open-Meteo model (raw/wx_401873078.json, Northwest Stadium coords) shows 0.016 in rain at 00Z, then 0.0 from 01Z-04Z, 55.9 F at kickoff falling to 50.6 F, wind 7.6-11.3 mph with gusts 17.0-21.9 mph during the game. ESPN gameInfo has no weather block. Broadcast (pre-game): "There\'s been a light rain falling on and off." The pre-game paper-slip forecast of 30.9 mph gusts did not verify (model gusts peaked 21.9 mph in-game). No pbp or caption ties a play to rain or wind (two "high snap" calls are not attributed to weather; all 7 FGs were good in pbp, incl. Evan McPherson 56; the caption line "Drew Stevens misses from beyond 50" matches no pbp attempt and is treated as a stat graphic, not a play), so any effect on play is unknown (not evidenced).',
        E_, '']
g = g.replace('## Not available from free sources', '\n'.join(sec) + '\n## Not available from free sources')
open(gp, 'w').write(g)
r.setdefault('assign_counts', {})['video'] = len(ROWS); r['assign_counts']['unattributed_after_video'] = r['assign_counts'].get('unattributed', 0) - len(ROWS)
r['video_rows'] = [dict(zip(('game', 'play', 'defender', 'role', 'source'), x)) for x in ROWS]; json.dump(r, open(f'{OUT}/data/CIN_at_WSH.json', 'w'), indent=1, default=str)
G = json.load(open(f'{OUT}/data/_all_games.json'))
for x in G:
    if x['game'] == G_: x.setdefault('assign_counts', {})['video'] = len(ROWS); x['assign_counts']['unattributed_after_video'] = x['assign_counts'].get('unattributed', 0) - len(ROWS); x['video_rows'] = r['video_rows']
json.dump(G, open(f'{OUT}/data/_all_games.json', 'w'), indent=1, default=str)
print('ok')
