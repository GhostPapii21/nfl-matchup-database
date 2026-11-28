#!/usr/bin/env python3
"""W12 game-log builder (copied from W11 builder, GB@LAR run 2026-11-26) (refs NFL-56). Sources: ESPN summary JSON (site.api.espn.com), Action Network public
scoreboard (pre-game, is_live=false lines). No Odds API. Never invents numbers: missing -> 'MISSING (reason)'."""
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import json, re, os, datetime, collections, urllib.request
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(OUT, 'raw'); os.makedirs(RAW, exist_ok=True)
STADIUM = {'ARI': (33.5276, -112.2626), 'ATL': (33.7554, -84.4009), 'BAL': (39.278, -76.6227), 'BUF': (42.7738, -78.787), 'CAR': (35.2258, -80.8528), 'CHI': (41.8623, -87.6167), 'CIN': (39.0955, -84.5161), 'CLE': (41.5061, -81.6995), 'DAL': (32.7473, -97.0945), 'DEN': (39.7439, -105.0201), 'DET': (42.34, -83.0456), 'GB': (44.5013, -88.0622), 'HOU': (29.6847, -95.4107), 'IND': (39.7601, -86.1639), 'JAX': (30.3239, -81.6373), 'KC': (39.0489, -94.4839), 'LV': (36.0909, -115.1833), 'LAC': (33.9535, -118.3392), 'MIA': (25.958, -80.2389), 'MIN': (44.9737, -93.2575), 'NE': (42.0909, -71.2643), 'NO': (29.9511, -90.0812), 'NYG': (40.8135, -74.0745), 'NYJ': (40.8135, -74.0745), 'PHI': (39.9008, -75.1675), 'PIT': (40.4468, -80.0158), 'SF': (37.4033, -121.9694), 'SEA': (47.5952, -122.3316), 'TB': (27.9759, -82.5033), 'TEN': (36.1665, -86.7713), 'WSH': (38.9076, -76.8645)}
NEUTRAL = {'Estadio Banorte': (19.3029, -99.1505), 'Estadio Azteca': (19.3029, -99.1505)}  # neutral-site venue coords (Mexico City)
AN_BOOKS = {15: 'consensus', 30: 'open', 68: 'DraftKings', 69: 'FanDuel', 75: 'BetMGM', 71: 'BetRivers', 79: 'bet365'}
UA = {'User-Agent': 'Mozilla/5.0'}
def get(url, path):
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=30).read()
    open(path, 'wb').write(data); return json.loads(data)
now = datetime.datetime.now()
NOWS = now.strftime('%Y-%m-%d %I:%M %p ' + __import__('time').strftime('%Z'))
sb = get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=12&dates=2026', f'{RAW}/scoreboard.json')
an = get('https://api.actionnetwork.com/web/v2/scoreboard/nfl?bookIds=15,30,68,69,71,75,79&date=20261125&periods=event', f'{RAW}/an_v2.json')
an2 = get('https://api.actionnetwork.com/web/v2/scoreboard/nfl?bookIds=15,30,68,69,71,75,79&date=20261126&periods=event', f'{RAW}/an_v2_1126.json')
ABBR_FIX = {'JAC': 'JAX', 'WSH': 'WSH', 'WAS': 'WSH', 'LA': 'LAR'}  # AN uses WAS, ESPN uses WSH (fixed 2026-11-24 MNF run)
an_games = {}
for g in an['games'] + an2['games']:
    t = {x['id']: ABBR_FIX.get(x['abbr'], x['abbr']) for x in g['teams']}
    an_games[(t[g['away_team_id']], t[g['home_team_id']])] = (g, t)

def an_lines(away, home):
    k = an_games.get((away, home))
    if not k: return None
    g, t = k; res = {}
    for bid, m in g['markets'].items():
        ev = m.get('event', {}); bk = AN_BOOKS.get(int(bid), bid); r = {}
        for o in ev.get('spread', []):
            if o.get('is_live'): continue
            if t.get(o.get('team_id')) == home: r['home_spread'] = o['value']; r['home_spread_odds'] = o['odds']
        for o in ev.get('total', []):
            if o.get('is_live'): continue
            if o['side'] == 'over': r['total'] = o['value']; r['over_odds'] = o['odds']
            if o['side'] == 'under': r['under_odds'] = o['odds']
        if r: res[bk] = r
    return res

OFFTYPES = {'Rush', 'Pass Reception', 'Pass Incompletion', 'Sack', 'Passing Touchdown', 'Rushing Touchdown', 'Pass Interception Return', 'Interception Return Touchdown', 'Fumble Recovery (Own)', 'Fumble Recovery (Opponent)', 'Fumble Return Touchdown'}
NAME = r"[A-Z][A-Za-z'\.\-]+(?: [A-Z][A-Za-z'\.\-]+)?"
def tacklers(text):
    # group right after the yardage only (trailing injury/replay/penalty/timeout notes are not tacklers)
    m = re.search(r'for (?:-?\d+ yards?|no gain)\s*(?:,\s*TOUCHDOWN\.?\s*)?\(([^()]*)\)', text)
    if not m: return []
    return [x.strip() for x in re.split(r'[;,]', m.group(1)) if x.strip() and 'Shotgun' not in x and 'Huddle' not in x and not re.match(r'Timeout #', x.strip())]

def parse_pass(text):
    if 'REVERSED.' in text: text = text.split('REVERSED.', 1)[1]  # 2026-11-23 fix: replay reversal -> grade the final ruling only
    t = re.sub(r'^\s*\([^)]*\)\s*', '', text)
    m = re.search(r'(\S+) pass (incomplete )?(short|deep)? ?(left|middle|right)? ?(?:to|intended for) ([A-Z][\w\.\'\-]+(?: [A-Z][\w\.\'\-]+)?)', t)
    if not m:  # 2026-11-23 fix: interceptions with no intended receiver ("pass deep middle INTERCEPTED by X")
        m2 = re.search(r'(\S+) pass (short|deep)? ?(left|middle|right)? ?INTERCEPTED by ([A-Z][\w\.\'\-]+)', t)
        if not m2: return None
        rest = t[m2.end():]
        cm = re.match(r'\s*\(([^)]*)\)', rest)
        return {'qb': m2.group(1), 'inc': False, 'depth': m2.group(2) or '?', 'dir': m2.group(3) or '?', 'target': 'no intended receiver', 'yds': None, 'td': False,
                'int_by': m2.group(4).rstrip('.,'), 'int_assist': [x.strip() for x in re.split(r'[;,]', cm.group(1)) if x.strip()] if cm else [], 'pbu': None, 'tack': [], 'qb_hit': re.findall(r'\[([^\]]+)\]', rest)}
    tgt = re.split(r'\.(?=[A-Z]{2,})', m.group(5))[0]
    tgt = ' '.join(w for w in tgt.split() if not re.fullmatch(r'[A-Z]{2,}\.?', w))
    d = {'qb': m.group(1), 'inc': bool(m.group(2)), 'depth': m.group(3) or '?', 'dir': m.group(4) or '?', 'target': tgt.rstrip('.,')}
    rest = t[m.end():]
    ym = re.search(r'for (-?\d+) yards?', rest); d['yds'] = int(ym.group(1)) if ym else (0 if 'no gain' in rest else None)
    d['td'] = 'TOUCHDOWN' in rest
    im = re.search(r'INTERCEPTED by ([A-Z][\w\.\'\-]+?)\.?(?=[\s\[(]|$)\s*(?:\(([^)]*)\))?', t); d['int_by'] = im.group(1) if im else None
    d['int_assist'] = [x.strip() for x in re.split(r'[;,]', im.group(2)) if x.strip()] if im and im.group(2) else []
    if im: d['yds'] = None  # 'for N yards' after an INT is the return, not a reception
    d['pbu'] = None; d['tack'] = []
    if d['inc']:
        pm = re.match(r'\s*\(([^)]*)\)', rest)
        if pm: d['pbu'] = [x.strip() for x in re.split(r'[;,]', pm.group(1)) if x.strip()]
    elif not d['int_by']:
        d['tack'] = tacklers(rest)
    d['qb_hit'] = re.findall(r'\[([^\]]+)\]', rest)
    return d

def parse_rush(text):
    t = re.sub(r'^\s*\([^)]*\)\s*', '', text)
    m = re.match(r'([A-Z][\w\.\'\-]+(?: [A-Z][\w\.\'\-]+)?) (?:up the middle|left|right|scrambles|kneels|to )', t)
    if not m: return None
    ym = re.search(r'for (-?\d+) yards?', t)
    return {'runner': m.group(1), 'yds': int(ym.group(1)) if ym else (0 if 'no gain' in t else None), 'td': 'TOUCHDOWN' in t,
            'dir': (re.search(r'(up the middle|left end|left tackle|left guard|right end|right tackle|right guard|scrambles)', t) or [None, '?'])[1] if re.search(r'(up the middle|left end|left tackle|left guard|right end|right tackle|right guard|scrambles)', t) else '?',
            'tack': tacklers(t)}

def stat(team_stats, name):
    for s in team_stats:
        if s['name'] == name: return s['displayValue']
    return 'unknown (not in ESPN boxscore)'

def build(ev):
    eid = ev['id']; comp = ev['competitions'][0]
    status = ev['status']['type']['name']; detail = ev['status']['type'].get('shortDetail', '')
    if status == 'STATUS_SCHEDULED' or ev['status'].get('period', 0) == 0: return None
    d = get(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eid}', f'{RAW}/{eid}.json')
    hc = d['header']['competitions'][0]
    teams = {c['homeAway']: c for c in hc['competitors']}
    away, home = teams['away']['team']['abbreviation'], teams['home']['team']['abbreviation']
    tid = {teams['away']['team']['id']: away, teams['home']['team']['id']: home}
    final = status == 'STATUS_FINAL'
    tag = 'FINAL' if final else f'IN PROGRESS ({detail}) - partial, a later run must finish it'
    L = []; W = L.append
    rec = {'event_id': eid, 'game': f'{away}@{home}', 'status': tag, 'pulled': NOWS}
    W(f'# {away} @ {home} - Week 12 game log ({tag})')
    W(f'\nESPN event {eid}. Pulled {NOWS}. Sources: ESPN summary JSON (play-by-play, box, drives), Action Network public scoreboard (pre-game lines). Research only, refs NFL-56.')
    if not final: W('\n> **IN PROGRESS: every number below is partial as of the pull time. Re-run after the final whistle.**')
    # linescore
    ls = {side: [int(x['displayValue']) for x in teams[side].get('linescores', [])] for side in ('away', 'home')}
    nq = max(len(ls['away']), len(ls['home']))
    W('\n## Score by quarter\n'); W('| Team | ' + ' | '.join(f'Q{i+1}' if i < 4 else 'OT' for i in range(nq)) + ' | 1H | 2H | Final |'); W('|' + '---|' * (nq + 4))
    for side, ab in (('away', away), ('home', home)):
        q = ls[side] + [0] * (nq - len(ls[side]))
        W(f'| {ab} | ' + ' | '.join(map(str, q)) + f' | {sum(q[:2])} | {sum(q[2:4])} | {teams[side].get("score")} |')
    qw = []
    for i in range(nq):
        a = ls['away'][i] if i < len(ls['away']) else 0; h = ls['home'][i] if i < len(ls['home']) else 0
        lab = f'Q{i+1}' if i < 4 else 'OT'
        qw.append((lab, away if a > h else home if h > a else 'TIE', a, h))
    a1, h1 = sum(ls['away'][:2]), sum(ls['home'][:2])
    W('\nQuarter winners: ' + '; '.join(f'{l} {w} ({a}-{h})' for l, w, a, h in qw) + f'; 1H {away if a1>h1 else home if h1>a1 else "TIE"} ({a1}-{h1}).')
    if len(ls['away']) >= 2 and len(ls['home']) >= 2:
        a2, h2 = sum(ls['away'][:3]), sum(ls['home'][:3])
    rec['quarters'] = qw; rec['first_half'] = (a1, h1)
    # plays
    drives = d.get('drives', {}).get('previous', [])
    plays = [(dr, p) for dr in drives for p in dr.get('plays', [])]
    # leader during Q2 (score after each play in Q2)
    q2 = [(p['awayScore'], p['homeScore'], p['clock']['displayValue']) for dr, p in plays if p['period']['number'] == 2]
    if q2:
        leaders = []
        for a, h, c in q2:
            ld = away if a > h else home if h > a else 'TIED'
            if not leaders or leaders[-1][0] != ld: leaders.append((ld, c, a, h))
        W('Who led during Q2 (score changes, clock at the play): ' + ' -> '.join(f'{l} {a}-{h} @{c}' for l, c, a, h in leaders) + f'. Leader at end of Q2: {leaders[-1][0]}.')
        rec['q2_leaders'] = leaders
    # lines
    W('\n## Result vs closing line\n')
    lines = an_lines(away, home); pick = d.get('pickcenter') or []
    if lines:
        W('Action Network public scoreboard, last pre-game line per book (is_live=false), pulled ' + NOWS + '. Home spread shown.\n')
        W('| Book | Home spread (odds) | Total (O/U odds) |'); W('|---|---|---|')
        for bk, r in lines.items():
            W(f"| {bk} | {home} {r.get('home_spread','?'):+} ({r.get('home_spread_odds','?')}) | {r.get('total','?')} ({r.get('over_odds','?')}/{r.get('under_odds','?')}) |" if isinstance(r.get('home_spread'), (int, float)) else f"| {bk} | MISSING | {r.get('total','MISSING')} |")
    else: W('Action Network lines: MISSING (game not found on AN scoreboard).')
    for pc in pick:
        W(f"\nESPN pickcenter ({pc.get('provider',{}).get('name')}): {pc.get('details')}, O/U {pc.get('overUnder')} (ESPN-displayed pre-game line; pulled {NOWS}).")
    ref = (lines or {}).get('consensus') or (lines or {}).get('DraftKings')
    refname = 'AN consensus' if (lines or {}).get('consensus') else 'AN DraftKings'
    sa, sh = int(teams['away'].get('score') or 0), int(teams['home'].get('score') or 0)
    if ref and isinstance(ref.get('home_spread'), (int, float)):
        hs = ref['home_spread']; margin = sh - sa + hs
        cover = 'PUSH' if margin == 0 else (home if margin > 0 else away)
        tot = sa + sh; tl = ref.get('total')
        tres = 'PUSH' if tot == tl else ('OVER' if tot > tl else 'UNDER')
        pre = '' if final else ' (CURRENT SCORE, NOT FINAL)'
        W(f"\n**Grading{pre} vs {refname} close ({home} {hs:+}, total {tl}):** outright winner {home if sh>sa else away if sa>sh else 'TIE'} ({sa}-{sh}); ATS cover {cover}{' (push)' if cover=='PUSH' else ''}; total {tot} -> {tres}.")
        rec['ats'] = {'ref': refname, 'home_spread': hs, 'total_line': tl, 'outright': home if sh > sa else away, 'cover': cover, 'total': tot, 'total_res': tres}
    else: W('\nGrading: MISSING (no closing spread found on the free feeds).')
    # scoring plays
    W('\n## Scoring plays\n'); W('| Q | Clock | Team | Type | Play | Score |'); W('|---|---|---|---|---|---|')
    sp_count = collections.Counter()
    for s in d.get('scoringPlays', []):
        tm = s.get('team', {}).get('abbreviation', '?'); ty = s['type']['text']
        sp_count[(tm, ty)] += 1
        W(f"| {s['period']['number']} | {s['clock']['displayValue']} | {tm} | {ty} | {s['text']} | {s['awayScore']}-{s['homeScore']} |")
    W('\nScoring mix: ' + '; '.join(f'{t} {ty} x{n}' for (t, ty), n in sorted(sp_count.items())))
    rec['scoring_mix'] = {f'{t}|{ty}': n for (t, ty), n in sp_count.items()}
    # team stats
    bt = {tid.get(t['team']['id'], t['team']['abbreviation']): t['statistics'] for t in d['boxscore']['teams']}
    W('\n## Team stats (ESPN box)\n'); W(f'| Stat | {away} | {home} |'); W('|---|---|---|')
    for nm, lab in [('thirdDownEff', '3rd down (conv-att)'), ('fourthDownEff', '4th down'), ('redZoneAttempts', 'Red zone TD-trips (ESPN)'), ('possessionTime', 'Time of possession'),
                    ('totalDrives', 'Drives'), ('totalOffensivePlays', 'Plays'), ('totalYards', 'Total yards'), ('netPassingYards', 'Net pass yds'), ('rushingYards', 'Rush yds'), ('rushingAttempts', 'Rush att'),
                    ('sacksYardsLost', 'Sacks-yds lost'), ('turnovers', 'Turnovers'), ('totalPenaltiesYards', 'Penalties-yds'), ('firstDowns', 'First downs')]:
        W(f'| {lab} | {stat(bt.get(away, []), nm)} | {stat(bt.get(home, []), nm)} |')
    rec['team_stats'] = {t: {s['name']: s['displayValue'] for s in v} for t, v in bt.items()}
    # drives
    W('\n## Drives\n'); W('| # | Team | Start | Q/clock | Plays | Yds | Time | Result | Reached RZ |'); W('|---|---|---|---|---|---|---|---|---|')
    rz = collections.defaultdict(list); drive_res = collections.defaultdict(collections.Counter)
    for i, dr in enumerate(drives, 1):
        tm = tid.get(dr.get('team', {}).get('id'), '?')
        scrim = [p for p in dr.get('plays', []) if p.get('start', {}).get('team', {}).get('id') == dr.get('team', {}).get('id') and p['type']['text'] in OFFTYPES and 'No Play' not in p['text']]
        reached = any(0 < (p.get('start', {}).get('yardsToEndzone') or 99) <= 20 for p in scrim)
        res = dr.get('displayResult', dr.get('result', '?'))
        drive_res[tm][res] += 1
        if reached: rz[tm].append((i, res))
        W(f"| {i} | {tm} | {dr.get('start',{}).get('text','')} | Q{dr.get('start',{}).get('period',{}).get('number','')} {dr.get('start',{}).get('clock',{}).get('displayValue','')} | {dr.get('offensivePlays','')} | {dr.get('yards','')} | {dr.get('timeElapsed',{}).get('displayValue','')} | {res} | {'yes' if reached else ''} |")
    W('\nDrive outcomes: ' + ' | '.join(f'{t}: ' + ', '.join(f'{k} {v}' for k, v in c.items()) for t, c in drive_res.items()))
    # red zone usage
    W('\n## Red zone (snaps starting at or inside the opponent 20; derived from ESPN play-by-play)\n')
    rzu = collections.defaultdict(lambda: collections.defaultdict(lambda: {'tgt': 0, 'car': 0, 'td': 0}))
    for dr, p in plays:
        st = p.get('start', {}); ytg = st.get('yardsToEndzone')
        if not ytg or ytg > 20: continue
        if p['type']['text'] not in OFFTYPES: continue
        tm = tid.get(st.get('team', {}).get('id'), '?'); txt = p['text']
        if 'No Play' in txt or 'NO PLAY' in txt: continue
        if ' pass ' in txt:
            pp = parse_pass(txt)
            if pp: rzu[tm][pp['target']]['tgt'] += 1; rzu[tm][pp['target']]['td'] += int(pp['td'])
        elif p['type']['text'] in ('Rush', 'Rushing Touchdown') or re.search(r' (up the middle|left end|right end|left tackle|right tackle|left guard|right guard) ', txt):
            rr = parse_rush(txt)
            if rr: rzu[tm][rr['runner']]['car'] += 1; rzu[tm][rr['runner']]['td'] += int(rr['td'])
    rec['red_zone'] = {}
    for tm in (away, home):
        trips = rz.get(tm, [])
        W(f"**{tm}**: {len(trips)} trips -> " + (', '.join(f'drive {i}: {r}' for i, r in trips) or 'none'))
        u = sorted(rzu[tm].items(), key=lambda kv: -(kv[1]['tgt'] + kv[1]['car']))
        W('  Usage inside the 20: ' + ('; '.join(f"{n} {v['car']} car/{v['tgt']} tgt/{v['td']} TD" for n, v in u) or 'none'))
        rec['red_zone'][tm] = {'trips': [r for _, r in trips], 'usage': {n: v for n, v in u}}
    # third down detail
    W('\n## Third downs (play-by-play)\n')
    td3 = collections.defaultdict(lambda: [0, 0, collections.Counter()])
    for dr, p in plays:
        st = p.get('start', {})
        if st.get('down') != 3 or 'No Play' in p['text'] or p['type']['text'] in ('Timeout', 'Penalty', 'Field Goal Good', 'Punt', 'Field Goal Missed', 'Two-minute warning', 'End Period'): continue
        if THIRD_FIX and p['type']['text'] not in OFFTYPES: continue  # 2026-11-24 MNF fix: skip 'Official Timeout' and other non-snap rows
        tm = tid.get(st.get('team', {}).get('id'), '?'); dist = st.get('distance') or 0
        b = 'short (1-3)' if dist <= 3 else 'medium (4-6)' if dist <= 6 else 'long (7+)'
        conv = (p.get('statYardage') or 0) >= dist or 'TOUCHDOWN' in p['text']
        if THIRD_FIX:  # gain on the snap from play text (a post-play penalty or a fumble out of bounds changes statYardage, not the conversion)
            gm = re.search(r'for (-?\d+) yards?|for no gain', p['text']); conv = conv or (bool(gm) and gm.group(1) is not None and int(gm.group(1)) >= dist)
        td3[tm][1] += 1; td3[tm][0] += int(conv); td3[tm][2][(b, conv)] += 1
    for tm in (away, home):
        c, a, cc = td3[tm]
        W(f"{tm}: {c}/{a} from pbp (box says {stat(bt.get(tm, []), 'thirdDownEff')}). By distance: " + '; '.join(f"{b} {cc[(b,True)]}/{cc[(b,True)]+cc[(b,False)]}" for b in ('short (1-3)', 'medium (4-6)', 'long (7+)')))
    # players
    W('\n## Player lines (ESPN box)\n')
    prec = {}
    for tp in d['boxscore'].get('players', []):
        tm = tid.get(tp['team']['id'], tp['team']['abbreviation'])
        cats = {c['name']: c for c in tp['statistics']}
        rcv = cats.get('receiving'); rsh = cats.get('rushing')
        tt = None
        if rcv:
            ki = rcv['keys']; tt = int(rcv['totals'][ki.index('receivingTargets')]) if 'receivingTargets' in ki and len(rcv.get('totals') or []) > ki.index('receivingTargets') else (sum(int(dict(zip(ki, a['stats'])).get('receivingTargets', 0) or 0) for a in rcv['athletes']) or None)
        W(f'\n**{tm} receiving** (team targets {tt})\n'); W('| Player | Tgt | Rec | Yds | TD | Long | Catch% | Tgt share |'); W('|---|---|---|---|---|---|---|---|')
        rows = []
        if rcv:
            ki = rcv['keys']
            for a in rcv['athletes']:
                s = dict(zip(ki, a['stats'])); tg = int(s.get('receivingTargets', 0) or 0); r = int(s.get('receptions', 0) or 0)
                rows.append((a['athlete']['displayName'], tg, r, s.get('receivingYards'), s.get('receivingTouchdowns'), s.get('longReception')))
        rows.sort(key=lambda x: -x[1])
        for n, tg, r, y, tdv, lg in rows:
            W(f"| {n} | {tg} | {r} | {y} | {tdv} | {lg} | {f'{100*r/tg:.0f}%' if tg else 'n/a'} | {f'{100*tg/tt:.1f}%' if tt else 'MISSING'} |")
            prec.setdefault(tm, {}).setdefault(n, {}).update(tgt=tg, rec=r, rec_yds=y, rec_td=tdv)
        if rows: W(f'\nTarget-share leader ({tm}): {rows[0][0]} {rows[0][1]}/{tt} ({100*rows[0][1]/tt:.1f}%)' if tt else '')
        W(f'\n**{tm} rushing**\n'); W('| Player | Car | Yds | YPC | TD | Long | Carry share |'); W('|---|---|---|---|---|---|---|')
        if rsh:
            ki = rsh['keys']; tc = int(rsh['totals'][ki.index('rushingAttempts')]) if 'rushingAttempts' in ki and len(rsh.get('totals') or []) > ki.index('rushingAttempts') else (sum(int(dict(zip(ki, a['stats'])).get('rushingAttempts', 0) or 0) for a in rsh['athletes']) or None)
            for a in rsh['athletes']:
                s = dict(zip(ki, a['stats'])); c = int(s.get('rushingAttempts', 0) or 0)
                W(f"| {a['athlete']['displayName']} | {c} | {s.get('rushingYards')} | {s.get('yardsPerRushAttempt')} | {s.get('rushingTouchdowns')} | {s.get('longRushing')} | {f'{100*c/tc:.0f}%' if tc else ''} |")
                prec.setdefault(tm, {}).setdefault(a['athlete']['displayName'], {}).update(car=c, rush_yds=s.get('rushingYards'), rush_td=s.get('rushingTouchdowns'))
        pss = cats.get('passing')
        if pss:
            ki = pss['keys']
            for a in pss['athletes']:
                s = dict(zip(ki, a['stats'])); W(f"\n{tm} passing: {a['athlete']['displayName']} {s.get('completions/passingAttempts')}, {s.get('passingYards')} yds, {s.get('passingTouchdowns')} TD, {s.get('interceptions')} INT, sacks {s.get('sacks-sackYardsLost')}")
    rec['players'] = prec
    # game-wide target leader
    allp = [(tm, n, v.get('tgt', 0)) for tm, pl in prec.items() for n, v in pl.items()]
    if allp:
        top = max(allp, key=lambda x: x[2]); W(f'\n**Game target leader:** {top[1]} ({top[0]}) {top[2]} targets.'); rec['game_target_leader'] = top
    # defenders
    W('\n## Defenders named on pass plays (ESPN play text)\n')
    W('Evidence labels: **VERIFIED-PBU/INT/DPI** = play text names the defender who broke up or intercepted the pass, or who was flagged for DPI; these are the only coverage counts. **tackler, not coverage** = defender named as tackler on a completion (inferred; not counted as coverage). No Play rule: a snap wiped out by an accepted penalty writes no tackler/PBU/INT rows; a DPI flag on it still counts. Declined penalties keep their rows. Free sources never name the assigned coverage defender on completions.\n')
    dlog = []; dagg = collections.defaultdict(lambda: {'tags': 0, 'rec': 0, 'yds': 0, 'td': 0, 'pbu': 0, 'int': 0, 'dpi': 0, 'big': [], 'vs': collections.Counter(), 'team': ''})
    sacks = collections.Counter(); hits = collections.Counter(); explos = []; injuries = []; pens = collections.Counter()
    for dr, p in plays:
        txt = p['text']; st = p.get('start', {}); off = tid.get(st.get('team', {}).get('id'), '?'); de = home if off == away else away
        for m in re.finditer(r'([A-Z]{2,3})-([A-Z][\w\.\'\- ]+?) was injured', txt): injuries.append((p['period']['number'], p['clock']['displayValue'], ABBR_FIX.get(m.group(1), m.group(1)), m.group(2)))
        for m in re.finditer(r'PENALTY on ([A-Z]{2,3})-([A-Z][\w\.\'\-]+), ([A-Za-z \-]+?),', txt): pens[(ABBR_FIX.get(m.group(1), m.group(1)), m.group(3))] += 1
        dpi = re.search(r'PENALTY on ([A-Z]{2,3})-([A-Z][\w\.\'\-]+), Defensive Pass Interference, (\d+) yards', txt)
        if 'sacked' in txt:
            sm = re.search(r'sacked [^()]*\(([^)]*)\)', txt)
            if sm:
                for s in re.split(r'[;,]| and ', sm.group(1).replace('sack split by ', '')): sacks[(de, s.strip() + (' (half)' if 'split' in sm.group(1) else ''))] += 1
        for h in re.findall(r'\[([^\]]+)\]', txt):
            for x in re.split(r'[;,]', h): hits[(de, x.strip())] += 1
        if ' pass ' in txt and 'No Play' in txt and dpi and 'sacked' not in txt:
            # No Play rule (Ghost6, PR #107): the snap never happened -> no tackler/PBU/INT rows; the DPI flag still counts
            pp = parse_pass(txt)
            if pp:
                dt_ = ABBR_FIX.get(dpi.group(1), dpi.group(1)); a = dagg[(dt_, dpi.group(2))]; a['team'] = dt_; a['dpi'] += 1; a['vs'][pp['target']] += 1
                dlog.append({'q': p['period']['number'], 'clock': p['clock']['displayValue'], 'off': off, 'def': de, 'qb': pp['qb'], 'target': pp['target'], 'depth': pp['depth'], 'dir': pp['dir'], 'result': 'DPI', 'yds': int(dpi.group(3)), 'defender': dpi.group(2), 'evidence': 'VERIFIED-DPI (flagged defender; No Play)', 'text': txt})
        elif ' pass ' in txt and 'No Play' not in txt and 'sacked' not in txt:
            pp = parse_pass(txt)
            if not pp: continue
            if pp['yds'] is not None and pp['yds'] >= 20 and not pp['inc']: explos.append((p['period']['number'], p['clock']['displayValue'], off, 'pass', pp['target'], pp['yds'], ', '.join(pp['tack']) or '(no tackler named)'))
            ev2 = None
            if pp['int_by']: who, lab = [pp['int_by']] + [x for x in pp.get('int_assist', []) if x != pp['int_by']], 'VERIFIED-PBU/INT (INT)'  # assist = defender named in () on the INT (NFL feed PD credit)
            elif pp['inc'] and pp['pbu']: who, lab = pp['pbu'], 'VERIFIED-PBU/INT (PBU)'
            elif not pp['inc'] and pp['tack']: who, lab = pp['tack'][:1], 'tackler, not coverage'
            elif not pp['inc']: who, lab = [], 'unattributed (TD/out of bounds, no defender named)'
            else: who, lab = [], 'incomplete, no defender named'
            for w in who:
                a = dagg[(de, w)]; a['team'] = de; a['tags'] += 1; a['vs'][pp['target']] += 1
                if not pp['inc'] and not pp['int_by']:
                    a['rec'] += 1; a['yds'] += pp['yds'] or 0; a['td'] += int(pp['td'])
                    if (pp['yds'] or 0) >= 20: a['big'].append(f"{pp['target']} {pp['yds']} {pp['depth']}_{pp['dir']} Q{p['period']['number']}")
                if pp['inc']: a['pbu'] += 1
                if pp['int_by']: a['int' if w == pp['int_by'] else 'pbu'] += 1
            dlog.append({'q': p['period']['number'], 'clock': p['clock']['displayValue'], 'off': off, 'def': de, 'qb': pp['qb'], 'target': pp['target'], 'depth': pp['depth'], 'dir': pp['dir'],
                         'result': 'INT' if pp['int_by'] else 'INC' if pp['inc'] else 'TD' if pp['td'] else 'C', 'yds': pp['yds'], 'defender': '; '.join(who), 'evidence': lab, 'text': txt})
            if dpi:
                dt_ = ABBR_FIX.get(dpi.group(1), dpi.group(1)); a = dagg[(dt_, dpi.group(2))]; a['team'] = dt_; a['dpi'] += 1; a['vs'][pp['target']] += 1
                dlog.append({'q': p['period']['number'], 'clock': p['clock']['displayValue'], 'off': off, 'def': de, 'qb': pp['qb'], 'target': pp['target'], 'depth': pp['depth'], 'dir': pp['dir'], 'result': 'DPI', 'yds': int(dpi.group(3)), 'defender': dpi.group(2), 'evidence': 'VERIFIED-DPI (flagged defender)', 'text': txt})
        elif p['type']['text'] in ('Rush', 'Rushing Touchdown') and 'No Play' not in txt:
            rr = parse_rush(txt)
            if rr and rr['yds'] is not None and rr['yds'] >= 15: explos.append((p['period']['number'], p['clock']['displayValue'], off, 'rush', rr['runner'], rr['yds'], ', '.join(rr['tack']) or '(no tackler named)'))
    W('| Defense | Defender | Plays tagged | Rec | Yds | TD | PBU | INT | DPI | Receivers | 20+ allowed |'); W('|---|---|---|---|---|---|---|---|---|---|---|')
    for (de, w), a in sorted(dagg.items(), key=lambda kv: -kv[1]['yds']):
        W(f"| {de} | {w} | {a['tags']} | {a['rec']} | {a['yds']} | {a['td']} | {a['pbu']} | {a['int']} | {a['dpi']} | {', '.join(f'{k} {v}' for k, v in a['vs'].most_common())} | {'; '.join(a['big'])} |")
    ver = sum(1 for x in dlog if x['evidence'].startswith('VERIFIED')); inf = sum(1 for x in dlog if x['evidence'].startswith('tackler')); un = len(dlog) - ver - inf
    W(f'\nESPN box red zone (TD-trips): {away} {stat(bt.get(away, []), "redZoneAttempts")}, {home} {stat(bt.get(home, []), "redZoneAttempts")} (ESPN counts trips differently; pbp trip list above is snap-based).') if False else None
    W(f'\nAssignment evidence count: {ver} VERIFIED (PBU/INT/DPI-named), {inf} tackler-not-coverage (inferred), {un} unattributed.')
    rec['assign_counts'] = {'verified': ver, 'tackler_inferred': inf, 'unattributed': un}
    rec['defenders'] = {f'{de}|{w}': {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in a.items()} for (de, w), a in dagg.items()}
    for tm in (away, home):
        tg = [(w, a) for (de, w), a in dagg.items() if de == tm]
        if tg:
            w, a = max(tg, key=lambda x: x[1]['yds']); W(f'Most yards charged to a {tm} defender (tackler tag, not coverage; inferred): {w} {a["rec"]} rec / {a["yds"]} yds.')
            rec.setdefault('most_beaten', {})[tm] = (w, a['rec'], a['yds'])
        vg = [(w, a) for w, a in tg if a['pbu'] + a['int'] + a['dpi']]
        if vg:
            w, a = max(vg, key=lambda x: (x[1]['pbu'] + x[1]['int'] + x[1]['dpi'], x[1]['dpi'])); W(f'Most VERIFIED-PBU/INT/DPI credits on a {tm} defender (the only coverage counts): {w} PBU {a["pbu"]}, INT {a["int"]}, DPI {a["dpi"]}.')
            rec.setdefault('most_verified', {})[tm] = (w, a['pbu'], a['int'], a['dpi'])
        else:
            W(f'VERIFIED-PBU/INT/DPI credits on a {tm} defender: none named.'); rec.setdefault('most_verified', {})[tm] = None
    W('\n## Explosive plays (pass 20+, rush 15+)\n'); W('| Q | Clock | Off | Type | Player | Yds | Tackler (not coverage) |'); W('|---|---|---|---|---|---|---|')
    for e in explos: W('| ' + ' | '.join(map(str, e)) + ' |')
    rec['explosives'] = explos
    W('\n## Pass rush (play text)\n')
    for tm in (away, home):
        W(f"{tm} defense sacks credited: " + (', '.join(f'{n} {c}' for (t, n), c in sacks.items() if t == tm) or 'none') + f" | QB hits [bracketed]: " + (', '.join(f'{n} {c}' for (t, n), c in hits.items() if t == tm) or 'none'))
    rec['sacks'] = {f'{t}|{n}': c for (t, n), c in sacks.items()}; rec['qb_hits'] = {f'{t}|{n}': c for (t, n), c in hits.items()}
    W('\n## In-game injuries (play text "was injured during the play")\n')
    W('\n'.join(f'- Q{q} {c}: {t} {n}' for q, c, t, n in injuries) or 'None noted in play text.')
    rec['injuries'] = injuries
    W('\n## Penalties by type (play text)\n'); W(', '.join(f'{t} {k} x{v}' for (t, k), v in pens.most_common()) or 'none parsed')
    wx = d.get('gameInfo', {}).get('weather')
    W('\n## Weather\n')
    W('ESPN gameInfo: ' + (json.dumps({k: v for k, v in (wx or {}).items() if k != 'link'}) if wx else 'MISSING (ESPN gameInfo has no weather block for this game)'))
    venue = d.get('gameInfo', {}).get('venue', {})
    W(f"Venue: {venue.get('fullName')} ({venue.get('address',{}).get('city')}), indoor={venue.get('indoor')}, grass={venue.get('grass')}")
    co = STADIUM.get(home)
    if d['header']['competitions'][0].get('neutralSite'): co = NEUTRAL.get(venue.get('fullName'))
    if co:
        try:
            ko = datetime.datetime.strptime(ev['date'], '%Y-%m-%dT%H:%MZ'); hr = ko.strftime('%Y-%m-%dT%H:00')
            om = get(f'https://api.open-meteo.com/v1/forecast?latitude={co[0]}&longitude={co[1]}&hourly=temperature_2m,precipitation,rain,wind_speed_10m,wind_gusts_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=UTC&start_date={ko.date()}&end_date={ko.date()}', f'{RAW}/wx_{eid}.json')
            j = om['hourly']['time'].index(hr); hv = {k: om['hourly'][k][j] for k in om['hourly'] if k != 'time'}
            W(f'Open-Meteo at kickoff hour ({hr}Z; model value, not a stadium observation; ignore if indoor): ' + json.dumps(hv)); rec['weather_openmeteo'] = hv
        except Exception as e: W(f'Open-Meteo: MISSING ({e})')
    else: W('Open-Meteo: not pulled (neutral site or unmapped)')
    rec['weather'] = {k: v for k, v in (wx or {}).items() if k != 'link'}
    import extras; extras.run(d, ev, away, home, tid, W, rec, RAW, OUT, NOWS, final, parse_pass, parse_rush, ABBR_FIX)
    W('\n## Not available from free sources (marked unknown)\n')
    W('- Assigned coverage defender on completions, man/zone per snap, routes run, snap shares: not in ESPN or nflverse free pbp (PFF/FTN premium). nflverse 2026 pbp release (asset updated 2026-11-26 06:03 UTC) includes 2026_12_GB_LA; see the nflverse cross-check section. FTN charting (blitz/pass rushers) only runs through week 11 at pull time, so blitz is UNKNOWN for this game.')
    W('- Next Gen Stats: week-12 statboard snapshot (separation, cushion, intended air yards, RYOE) saved in NGS_W12_SNAPSHOT.md; per-route charts are not public via API.')
    open(f"{OUT}/{away}_at_{home}.md", 'w').write('\n'.join(L) + '\n')
    json.dump(dlog, open(f'{OUT}/data/{away}_at_{home}_pass_defender_log.json', 'w'), indent=1)
    json.dump(rec, open(f'{OUT}/data/{away}_at_{home}.json', 'w'), indent=1, default=str)
    return rec

os.makedirs(f'{OUT}/data', exist_ok=True)
recs = []
EXCLUDE = set()
ONLY = os.environ.get('ONLY')
THIRD_FIX = True  # keep the 2026-11-24 MNF third-down fix for all W12 runs
for ev in sb['events']:
    if ev['status']['type']['name'] != 'STATUS_FINAL' or ev['shortName'].replace(' @ ', '@') in EXCLUDE or ev['shortName'] in EXCLUDE:
        print('skip', ev['shortName'], ev['status']['type']['name']); continue
    if ONLY and ev['shortName'] != ONLY: continue
    r = build(ev)
    if r: recs.append(r); print(r['game'], r['status'])
if ONLY:
    prev = [r for r in json.load(open(f'{OUT}/data/_all_games.json')) if r['game'] not in {x['game'] for x in recs}]
    recs = prev + recs
json.dump(recs, open(f'{OUT}/data/_all_games.json', 'w'), indent=1, default=str)
