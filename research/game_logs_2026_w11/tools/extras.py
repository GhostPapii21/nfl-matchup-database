"""Extra sections for the W11 game logs (Rico/Ghost6 spec additions, 4:53 PM AST). refs NFL-56, NFL-49."""
import json, re, csv, collections, urllib.request, os
UA = {'User-Agent': 'Mozilla/5.0'}
PERIODS = ['firstquarter', 'secondquarter', 'thirdquarter', 'fourthquarter', 'firsthalf', 'secondhalf']
PLAB = {'firstquarter': 'Q1', 'secondquarter': 'Q2', 'thirdquarter': 'Q3', 'fourthquarter': 'Q4', 'firsthalf': '1H', 'secondhalf': '2H'}
OFFT = {'Rush', 'Pass Reception', 'Pass Incompletion', 'Sack', 'Passing Touchdown', 'Rushing Touchdown', 'Pass Interception Return', 'Interception Return Touchdown',
        'Fumble Recovery (Own)', 'Fumble Recovery (Opponent)', 'Fumble Return Touchdown', 'Safety'}
_cache = {}
def _get(url, path):
    if path in _cache: return _cache[path]
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    open(path, 'wb').write(data); _cache[path] = json.loads(data); return _cache[path]

def period_lines(raw, away, home, fix):
    out = {}
    for per in PERIODS:
        for date in ('20261122', '20261123'):
            d = _get(f'https://api.actionnetwork.com/web/v2/scoreboard/nfl?bookIds=15,68,69&date={date}&periods={per}', f'{raw}/an_{per}_{date}.json')
            for g in d['games']:
                t = {x['id']: fix.get(x['abbr'], x['abbr']) for x in g['teams']}
                if (t[g['away_team_id']], t[g['home_team_id']]) != (away, home): continue
                for bid, bk in (('15', 'AN consensus'), ('68', 'DraftKings'), ('69', 'FanDuel')):
                    m = g['markets'].get(bid, {}).get(per, {})
                    sp = [o for o in m.get('spread', []) if not o.get('is_live') and t.get(o.get('team_id')) == home]
                    to = [o for o in m.get('total', []) if not o.get('is_live') and o['side'] == 'over']
                    if sp or to:
                        out[PLAB[per]] = {'book': bk, 'home_spread': sp[0]['value'] if sp else None, 'spread_odds': sp[0]['odds'] if sp else None,
                                          'total': to[0]['value'] if to else None, 'over_odds': to[0]['odds'] if to else None}
                        break
    return out

_ros = {}
def roster(raw, team_id):
    if team_id in _ros: return _ros[team_id]
    d = _get(f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster', f'{raw}/roster_{team_id}.json')
    full, short = {}, collections.defaultdict(set)
    for g in d.get('athletes', []):
        for a in g['items']:
            pos = a.get('position', {}).get('abbreviation'); full[a['displayName']] = pos
            fn, ln = a.get('firstName', ''), a.get('lastName', '')
            for k in {f'{fn[:1]}.{ln}', f'{fn[:2]}.{ln}', f'{fn[:1]}.{ln.split(" ")[0]}'}: short[k].add(pos)
            short['LAST:' + ln.split(' ')[0]].add(pos)
    _ros[team_id] = (full, short); return _ros[team_id]

def pos_of(short, name):
    s = short.get(name)
    if s and len(s) == 1: return next(iter(s))
    if not s and '.' in name:
        s2 = short.get('LAST:' + name.split('.', 1)[1].split(' ')[0])
        if s2 and len(s2) == 1: return next(iter(s2)) + ' (last-name match)'
    return 'unknown' if not s else 'ambiguous:' + '/'.join(sorted(x or '?' for x in s))

def run(d, ev, away, home, tid, W, rec, raw, out, nows, final, parse_pass, parse_rush, fix):
    SRC_ESPN = f'src: ESPN summary JSON event {ev["id"]}, pulled {nows}'
    hc = d['header']['competitions'][0]; teams = {c['homeAway']: c for c in hc['competitors']}
    ls = {s: [int(x['displayValue']) for x in teams[s].get('linescores', [])] for s in ('away', 'home')}
    # ---- period ATS/total
    pl = period_lines(raw, away, home, fix); rec['period_lines'] = pl
    W(f'\n## Period spread and total results (lines: Action Network public scoreboard pre-game is_live=false, consensus unless noted, pulled {nows}; scores: {SRC_ESPN})\n')
    W('| Period | Away pts | Home pts | Total | Winner | Line (home) | ATS winner | Total line | O/U |'); W('|---|---|---|---|---|---|---|---|---|')
    def seg(idx):
        return sum(ls['away'][i] for i in idx if i < len(ls['away'])), sum(ls['home'][i] for i in idx if i < len(ls['home']))
    segs = {'Q1': [0], 'Q2': [1], 'Q3': [2], 'Q4': [3], '1H': [0, 1], '2H': [2, 3] + ([4] if len(ls['away']) > 4 else [])}
    nq = len(ls['away']); rec['periods'] = {}
    for lab, idx in segs.items():
        if max(idx[:1]) >= nq: W(f'| {lab} | unknown (not played yet) | | | | | | | |'); continue
        incomplete = (not final) and max(idx) >= nq - 1
        a, h = seg(idx); win = away if a > h else home if h > a else 'TIE'
        L = pl.get(lab, {}); hs, tl = L.get('home_spread'), L.get('total')
        if hs is not None:
            m = h - a + hs; ats = 'PUSH' if m == 0 else (home if m > 0 else away)
        else: ats = 'unknown (no pre-game line on free feed)'
        ou = ('PUSH' if a + h == tl else 'OVER' if a + h > tl else 'UNDER') if tl is not None else 'unknown (no line)'
        tag = ' (in progress)' if incomplete else ''
        W(f"| {lab}{tag} | {a} | {h} | {a+h} | {win} | {f'{home} {hs:+} ({L.get(chr(115)+chr(112)+chr(114)+chr(101)+chr(97)+chr(100)+chr(95)+chr(111)+chr(100)+chr(100)+chr(115))}) {L.get(chr(98)+chr(111)+chr(111)+chr(107))}' if hs is not None else 'unknown'} | {ats} | {tl if tl is not None else 'unknown'} | {ou} |")
        rec['periods'][lab] = {'away': a, 'home': h, 'winner': win, 'line': L, 'ats': ats, 'ou': ou, 'in_progress': incomplete}
    W('\nNote: books differ on whether OT counts in Q4/2H markets; 2H here includes OT if played, Q4 excludes it. Check the book rule before settling.')
    # ---- full pbp + reconciliation
    wp = {w['playId']: w.get('homeWinPercentage') for w in d.get('winprobability', [])}
    rows = []; cnt = collections.Counter(); qbs = set()
    for tp in d['boxscore'].get('players', []):
        for c in tp['statistics']:
            if c['name'] == 'passing':
                for a in c['athletes']:
                    n = a['athlete']; qbs.add(n['displayName']); qbs.add(f"{n.get('firstName','')[:1]}.{n.get('lastName','')}")
    for di, dr in enumerate(d.get('drives', {}).get('previous', []), 1):
        for p in dr.get('plays', []):
            st = p.get('start', {}); off = tid.get(st.get('team', {}).get('id'), '')
            ty = p['type']['text']; txt = p['text']; nop = 'No Play' in txt or 'NO PLAY' in txt
            isoff = (ty in OFFT or ('Sack' in ty) or ('Interception' in ty and 'Kick' not in ty and 'Punt' not in ty) or ('Fumble' in ty and 'Punt' not in ty and 'Kick' not in ty and 'Muff' not in ty)) and not nop
            if isoff: cnt[off] += 1
            h = wp.get(p['id']); a_s, h_s = p.get('awayScore'), p.get('homeScore')
            margin = abs((h_s or 0) - (a_s or 0)); q = p['period']['number']
            gt = (h is not None and (h < 0.05 or h > 0.95) and q >= 3) or (q == 4 and margin >= 17)
            rows.append({'drive': di, 'drive_team': tid.get(dr.get('team', {}).get('id'), ''), 'play_id': p['id'], 'q': q, 'clock': p['clock']['displayValue'], 'offense': off,
                         'down': st.get('down'), 'dist': st.get('distance'), 'yards_to_endzone': st.get('yardsToEndzone'), 'type': ty, 'offensive_play': int(isoff), 'no_play': int(nop),
                         'yards': p.get('statYardage'), 'yac': p.get('yardsAfterCatch', ''), 'scoring': int(bool(p.get('scoringPlay'))), 'away_score': a_s, 'home_score': h_s,
                         'home_wp': h if h is not None else '', 'garbage_time_flag': int(gt), 'wallclock': p.get('wallclock', ''), 'text': txt})
    os.makedirs(f'{out}/pbp', exist_ok=True)
    fn = f'{out}/pbp/{away}_at_{home}_pbp.csv'
    with open(fn, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['none']); w.writeheader(); w.writerows(rows)
    bt = {tid.get(t['team']['id']): {s['name']: s['displayValue'] for s in t['statistics']} for t in d['boxscore']['teams']}
    W(f'\n## Full play-by-play and play-count reconciliation ({SRC_ESPN})\n')
    W(f'Every ESPN play ({len(rows)} rows incl. kickoffs, penalties, timeouts) is in `pbp/{away}_at_{home}_pbp.csv` with down/distance, yards, YAC, home win prob and a garbage-time flag.\n')
    W('| Team | Offensive plays counted from pbp (rush+pass att+sacks, no-plays excluded) | ESPN box Total Plays | Match |'); W('|---|---|---|---|')
    recon = {}
    for t in (away, home):
        e = bt.get(t, {}).get('totalOffensivePlays', 'unknown'); ok = str(cnt[t]) == str(e)
        W(f'| {t} | {cnt[t]} | {e} | {"yes" if ok else "NO - see note"} |'); recon[t] = (cnt[t], e, ok)
    rec['play_recon'] = recon
    if not all(v[2] for v in recon.values()): W('\nMismatch note: ESPN sometimes counts aborted snaps/spikes differently or the feed is mid-update; flagged for Ghost6.')
    # ---- turnovers, 4th down, RZ
    W(f'\n## Turnovers, 4th down, red zone ({SRC_ESPN})\n'); W(f'| Stat | {away} | {home} |'); W('|---|---|---|')
    for k, lab in (('turnovers', 'Turnovers'), ('fumblesLost', 'Fumbles lost'), ('interceptions', 'INTs thrown'), ('fourthDownEff', '4th down conv-att'), ('redZoneAttempts', 'Red zone TD-trips (ESPN)'), ('totalDrives', 'Drives')):
        W(f"| {lab} | {bt.get(away,{}).get(k,'unknown')} | {bt.get(home,{}).get(k,'unknown')} |")
    def rate(t):
        try: return f"{100*int(bt[t]['turnovers'])/int(bt[t]['totalDrives']):.1f}% of drives; {100*int(bt[t]['turnovers'])/cnt[t]:.1f}% of plays"
        except Exception: return 'unknown'
    W(f'| Turnover rate | {rate(away)} | {rate(home)} |')
    # ---- scoring breakdown
    W(f'\n## Scoring breakdown ({SRC_ESPN} scoringPlays)\n')
    sb = {away: collections.Counter(), home: collections.Counter()}
    for s in d.get('scoringPlays', []):
        t = fix.get(s.get('team', {}).get('abbreviation', ''), s.get('team', {}).get('abbreviation', '')); ty = s['type']['text']; txt = s['text']
        if ty == 'Rushing Touchdown':
            scorer = re.match(r'(.+?) \d+ Yd', txt); scorer = scorer.group(1) if scorer else ''
            sb.setdefault(t, collections.Counter())['QB rush TD' if scorer in qbs else 'Non-QB rush TD'] += 1
        elif ty == 'Passing Touchdown': sb.setdefault(t, collections.Counter())['Receiving TD'] += 1
        elif ty in ('Field Goal Good',): sb.setdefault(t, collections.Counter())['FG'] += 1
        elif 'Return' in ty or 'Blocked' in ty or 'Defensive' in ty: sb.setdefault(t, collections.Counter())['Defense/ST TD'] += 1
        elif ty == 'Safety': sb.setdefault(t, collections.Counter())['Safety'] += 1
        else: sb.setdefault(t, collections.Counter())[ty] += 1
        if 'Two-Point' in txt or '2PT' in txt.upper() or 'two-point' in txt.lower():
            sb[t]['2-pt attempt (see text)'] += 1
    cats = ['Non-QB rush TD', 'QB rush TD', 'Receiving TD', 'Defense/ST TD', 'FG', 'Safety']
    W('| Team | ' + ' | '.join(cats) + ' | Other |'); W('|' + '---|' * (len(cats) + 2))
    for t in (away, home):
        other = {k: v for k, v in sb[t].items() if k not in cats}
        W(f'| {t} | ' + ' | '.join(str(sb[t][c]) for c in cats) + f' | {other or ""} |')
    rec['scoring_breakdown'] = {t: dict(v) for t, v in sb.items()}
    # ---- skill players with positions
    W(f'\n## WR / TE / RB usage with positions (box: {SRC_ESPN}; positions: ESPN team roster API, pulled {nows})\n')
    W('Players absent from the ESPN receiving box had no target or reception logged; whether they played is unknown until snap counts post (nflverse/PFR, usually Monday-Tuesday).\n')
    W('\\* "0 logged" = the player is absent from that ESPN box table (ESPN lists every player with a target or carry), not a missing value.\n')
    W('| Team | Player | Pos | Tgt | Rec | Catch% | Rec yds | Car | Rush yds | Tgt share |'); W('|---|---|---|---|---|---|---|---|---|---|')
    tidr = {v: k for k, v in tid.items()}; shorts = {}
    for t in (away, home):
        full, short = roster(raw, tidr[t]); shorts[t] = short
        pp = rec.get('players', {}).get(t, {}); tt = sum(v.get('tgt', 0) for v in pp.values())
        for n, v in sorted(pp.items(), key=lambda kv: -(kv[1].get('tgt', 0) * 10 + kv[1].get('car', 0))):
            pos = full.get(n, 'unknown')
            if pos == 'QB' and not v.get('tgt'): continue
            tg = v.get('tgt'); r = v.get('rec')
            W(f"| {t} | {n} | {pos} | {tg if tg is not None else '0 logged*'} | {r if r is not None else '0 logged*'} | {f'{100*r/tg:.0f}%' if tg else 'n/a'} | {v.get('rec_yds') if tg is not None else '0 logged*'} | {v.get('car') if 'car' in v else '0 logged*'} | {v.get('rush_yds') if 'car' in v else '0 logged*'} | {f'{100*tg/tt:.1f}%' if tg is not None and tt else '0%*'} |")
    # ---- per-play passing detail: leaks by position, air yards, YAC, early-down pass rate, sacks
    W(f'\n## Defensive leaks by target position (derived from ESPN play text + roster positions, {nows})\n')
    W('WR slot vs outside alignment is **unknown** in free data (ESPN/nflverse do not chart alignment; FTN/PFF are paid and are not used). Pass location (left/middle/right) is shown as a proxy only.\n')
    leak = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0, 0]))
    locs = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))
    air = collections.defaultdict(lambda: [0, 0, 0]); early = collections.defaultdict(lambda: [0, 0]); dropbacks = collections.Counter(); sk = collections.Counter(); hitc = collections.Counter()
    expl_allowed = collections.defaultdict(lambda: {'pass20': 0, 'rush15': 0})
    for r in rows:
        if not r['offensive_play']: continue
        off = r['offense']; de = home if off == away else away; txt = r['text']
        ispass = ' pass ' in txt or r['type'] == 'Sack'
        if r['down'] in (1, 2):
            early[off][1] += 1; early[off][0] += int(ispass)
        if ispass: dropbacks[off] += 1
        if r['type'] == 'Sack' or 'sacked' in txt: sk[off] += 1
        if '[' in txt: hitc[off] += 1
        if ' pass ' in txt and 'sacked' not in txt:
            pp = parse_pass(txt)
            if not pp: continue
            pos = pos_of(shorts[off], pp['target'])
            pos = pos.replace(' (last-name match)', '')
            pg = 'WR' if pos == 'WR' else 'TE' if pos == 'TE' else 'RB' if pos in ('RB', 'FB') else pos
            L = leak[de][pg]; L[0] += 1
            comp = not pp['inc'] and not pp['int_by']
            if comp: L[1] += 1; L[2] += pp['yds'] or 0; L[3] += int(pp['td'])
            lo = locs[de][f"{pp['depth']}_{pp['dir']}"]; lo[0] += 1; lo[1] += int(comp); lo[2] += (pp['yds'] or 0) if comp else 0
            if comp and r['yac'] != '' and pp['yds'] is not None:
                air[off][0] += 1; air[off][1] += pp['yds'] - int(r['yac']); air[off][2] += int(r['yac'])
            if comp and (pp['yds'] or 0) >= 20: expl_allowed[de]['pass20'] += 1
        elif r['type'] in ('Rush', 'Rushing Touchdown'):
            rr = parse_rush(txt)
            if rr and (rr['yds'] or 0) >= 15: expl_allowed[de]['rush15'] += 1
    rec['leaks'] = {}
    for de in (away, home):
        W(f'**{de} defense allowed, by target position**'); W('| Pos | Tgt | Rec | Yds | TD | Yds/tgt |'); W('|---|---|---|---|---|---|')
        for pg, (t_, c_, y_, td_) in sorted(leak[de].items(), key=lambda kv: -kv[1][2]):
            W(f'| {pg} | {t_} | {c_} | {y_} | {td_} | {y_/t_:.1f} |')
        rec['leaks'][de] = {k: v for k, v in leak[de].items()}
        W(f'\n{de} defense by depth/location (proxy, not alignment): ' + '; '.join(f'{k} {v[1]}/{v[0]} {v[2]}y' for k, v in sorted(locs[de].items(), key=lambda kv: -kv[1][2])) + '\n')
    W(f'\n## Extras ({SRC_ESPN}; derived where noted)\n'); W(f'| Metric | {away} | {home} |'); W('|---|---|---|')
    def f1(x): return x
    W(f'| Early-down pass rate (1st/2nd down, pass att+sacks / plays) | ' + ' | '.join(f'{100*early[t][0]/early[t][1]:.0f}% ({early[t][0]}/{early[t][1]})' if early[t][1] else 'unknown' for t in (away, home)) + ' |')
    W(f'| Sack rate (sacks / dropbacks) | ' + ' | '.join(f'{100*sk[t]/dropbacks[t]:.1f}% ({sk[t]}/{dropbacks[t]})' if dropbacks[t] else 'unknown' for t in (away, home)) + ' |')
    W(f'| QB-hit rate (plays with a [bracketed] hit / dropbacks) - pressure proxy; true pressure rate unknown (charting is paid) | ' + ' | '.join(f'{100*hitc[t]/dropbacks[t]:.1f}% ({hitc[t]}/{dropbacks[t]})' if dropbacks[t] else 'unknown' for t in (away, home)) + ' |')
    W(f'| Completed air yards / YAC (ESPN yardsAfterCatch; air = gain - YAC on completions) | ' + ' | '.join(f'{air[t][1]} air / {air[t][2]} YAC on {air[t][0]} comps' if air[t][0] else 'unknown' for t in (away, home)) + ' |')
    W(f'| Intended air yards on incompletions | unknown (not in ESPN; nflverse air_yards after overnight rebuild) | unknown |')
    W(f'| Explosive plays allowed by this team\'s defense (pass 20+ / rush 15+) | ' + ' | '.join(f"{expl_allowed[t]['pass20']} / {expl_allowed[t]['rush15']}" for t in (away, home)) + ' |')
    W(f"| Penalties-yds | {bt.get(away,{}).get('totalPenaltiesYards','unknown')} | {bt.get(home,{}).get('totalPenaltiesYards','unknown')} |")
    gt = [r for r in rows if r['garbage_time_flag'] and r['offensive_play']]
    W(f'| Garbage-time offensive plays (Q3+ with home WP <5% or >95%, or Q4 margin 17+) | ' + ' | '.join(str(sum(1 for r in gt if r['offense'] == t)) for t in (away, home)) + ' |')
    W('| Snap shares | unknown (nflverse/PFR snap counts post Mon-Tue) | unknown |')
    rec['extras'] = {'early_pass': {t: early[t] for t in (away, home)}, 'sacks_dropbacks': {t: (sk[t], dropbacks[t]) for t in (away, home)}, 'qb_hits': dict(hitc),
                     'air_yac': {t: air[t] for t in (away, home)}, 'explosives_allowed': {t: expl_allowed[t] for t in (away, home)}, 'garbage_plays': len(gt)}
    W('\n## QB vs coverage shell / pressure\n')
    W('| Split | Status |'); W('|---|---|')
    for s in ('vs man / vs zone', 'vs blitz / no blitz', 'vs MOF open / MOF closed', 'under pressure / clean'):
        W(f'| {s} | unknown: no free play-level source charts this (FTN/PFF are paid and are not used). Season-level Sharp shell rates stay in the defense DB profiles. |')
    return rec
