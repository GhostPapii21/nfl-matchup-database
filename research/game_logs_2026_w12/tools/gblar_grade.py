"""GB@LAR (W12, ESPN 401873079) extra sections: pregame-lock grading vs the 23:31Z freeze, every pregame read graded,
QB production (nflverse splits; pressure = sacks+QB hits ESTIMATE), inactives from the ESPN game roster, who got burned.
Research only. projection_ready stays false. No Odds API. Never invents numbers: missing -> UNKNOWN. refs NFL-49, refs NFL-56."""
import json, os, re, datetime, time, collections
import pandas as pd
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RAW = f'{OUT}/raw'
NOWS = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p ') + time.strftime('%Z')
FZ_PATH = 'pregame/price_freezes/2026-11-25_GB@LA/freeze_20261125T233144Z.json'
fz = json.load(open(f'{RAW}/freeze_20261125T233144Z.json')); M = fz['markets']; meta = fz['meta']
rec = json.load(open(f'{OUT}/data/GB_at_LAR.json')); P = rec['players']
d = json.load(open(f'{RAW}/401873079.json'))
reads = json.load(open(f'{RAW}/reads.json'))['games']['2026_12_GB_LA']
dash = json.load(open(f'{RAW}/2026_12_GB_LA.json'))
nv = pd.read_csv(f'{RAW}/nflverse/pbp_2026.csv.gz', low_memory=False); g = nv[nv.game_id == '2026_12_GB_LA'].copy()
GB, LA = 13, 26; KO = '2026-11-26T01:00Z'
def et(z):
    z = z.replace('+00:00', 'Z')
    for f in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%MZ'):
        try: return datetime.datetime.strptime(z, f).replace(tzinfo=datetime.timezone.utc).astimezone().strftime('%Y-%m-%d %I:%M %p %Z')
        except ValueError: pass
    return z
def pl(name):
    for t in ('GB', 'LAR'):
        if name in P.get(t, {}): return P[t][name]
    return None
def stat(name, kind):
    v = pl(name)
    if v is None: return 0  # absent from ESPN box = no target/carry logged; played-status checked against the ESPN game roster below
    return {'rec': int(v.get('rec', 0) or 0), 'rec_yds': int(v.get('rec_yds', 0) or 0), 'rush_yds': int(v.get('rush_yds', 0) or 0), 'car': int(v.get('car', 0) or 0), 'tgt': int(v.get('tgt', 0) or 0)}[kind]
def res(actual, line, side):
    if actual == line: return 'PUSH'
    return 'W' if (actual > line) == (side == 'O') else 'L'
# ---------------- inactives from ESPN game roster (core API)
ros = {}
for tid, ab in ((9, 'GB'), (14, 'LAR')):
    team = json.load(open(f'{RAW}/roster_{tid}.json')); byj = {}
    for grp in team.get('athletes', []):
        for a in grp['items']: byj[str(a.get('jersey'))] = (a['displayName'], a.get('position', {}).get('abbreviation', '?'))
    gr = json.load(open(f'{RAW}/gameroster_{tid}.json'))
    ros[ab] = {'dnp': [byj.get(str(e.get('jersey')), (e['displayName'], '?')) for e in gr['entries'] if e.get('didNotPlay')],
               'dressed': {byj.get(str(e.get('jersey')), (e['displayName'], '?'))[0] for e in gr['entries'] if not e.get('didNotPlay')}, 'n': len(gr['entries'])}
def played(name):
    return pl(name) is not None or any(name in r['dressed'] for r in ros.values())  # a box-score stat proves he played
L = ['<!-- GBLAR-GRADE-START -->', f'## Pregame lock grading (freeze `{FZ_PATH}`)', '',
     f"Lock: prices pulled {et(meta['pulled_utc'])} ({meta['pulled_utc']}), freeze written {et(meta['written_utc'])}; kickoff {et(KO)} ({KO}). Freeze written 88 min before kickoff (prices pulled 93 min before), so it is a valid pristine pregame lock. Source: {meta['source']}. Final: LAR {LA}, GB {GB} (ESPN FINAL).", '',
     '| Market | Consensus line at lock | Pinnacle ref | Best retail price at lock | Actual | Result |', '|---|---|---|---|---|---|']
sp = M['spread']; tot = M['total']; ml = M['moneyline']
def best(m, s): b = m['best_retail_price'][s]; return f"{b['book']} {b['line'] if b['line'] is not None else ''} {int(b['price']):+d}".replace('  ', ' ')
L.append(f"| Spread | LAR {sp['consensus']['line']} ({sp['consensus']['n_books_at_line']} books) | LAR {sp['reference']['line']} (no-vig LAR {sp['reference']['no_vig']['LA']:.1%}) | LAR: {best(sp,'LA')}; GB: GB +2.5 {sp['best_retail_price']['GB']['book']} {int(sp['best_retail_price']['GB']['price']):+d} | LAR by {LA-GB} | **LAR -2.5 covers by {LA-GB-2.5}**; GB +2.5 loses |")
L.append(f"| Total | {tot['consensus']['line']} | {tot['reference']['line']} (no-vig over {tot['reference']['no_vig']['Over']:.1%}) | Over: {best(tot,'Over')}; Under: {best(tot,'Under')} | {LA+GB} | **UNDER by {tot['consensus']['line']-(LA+GB)}** |")
L.append(f"| Moneyline | LAR -144 / GB +120 (consensus) | LAR -140 / GB +126 (no-vig LAR {ml['reference']['no_vig']['LA']:.1%}) | LAR: {best(ml,'LA')}; GB: {best(ml,'GB')} | LAR won | **LAR ML wins**; GB ML loses |")
L.append(f"| Implied team totals (derived from 43.5 and -2.5; not a posted market) | LAR 23.0 / GB 20.5 | | | LAR {LA} / GB {GB} | LAR over (+3.0); GB under (-7.5) |")
L += ['', 'Team-total and period (quarter/half) prices are not in the freeze file (it holds full-game spread/total/ML and player props only). Period results (section below) use the Action Network public scoreboard pre-game lines (is_live=false), pulled after the game; they are labeled as such and are not the lock.', '']
# ---- every prop in the freeze
L += ['### Every player prop in the lock, graded at the consensus line', '', '| Player | Market | Consensus line | Pinnacle line (no-vig over) | Actual | Over/Under result | Played (ESPN game roster) |', '|---|---|---|---|---|---|---|']
props = []
for k, m in M.items():
    if '|' not in k: continue
    mk, name = k.split('|'); line = m['consensus']['line']; ref = m['reference']
    kind = {'receiving_yards': 'rec_yds', 'receptions': 'rec', 'rushing_yards': 'rush_yds'}[mk]
    a = stat(name, kind); r = res(a, line, 'O'); props.append((name, mk, line, a, r))
    L.append(f"| {name} | {mk.replace('_',' ')} | {line} | {ref.get('line')} ({(ref.get('no_vig') or {}).get('Over', float('nan')):.1%}) | {a} | {'OVER' if r=='W' else 'UNDER' if r=='L' else 'PUSH'} | {'yes' if played(name) else 'NO / not on game roster'} |")
ov = sum(1 for p in props if p[4] == 'W'); un = sum(1 for p in props if p[4] == 'L')
L += ['', f'Prop tally at consensus lines: {ov} over, {un} under, {len(props)-ov-un} push, of {len(props)}.', '']
# ---------------- reads graded
def G(play, actual, line, side, why_res, src, kind='lean'):
    r = res(actual, line, side); return {'play': play, 'src': src, 'kind': kind, 'line': line, 'side': side, 'actual': actual, 'result': r, 'note': why_res}
RD = []
RD.append(G('Tutu Atwell over 1.5 catches (model 66% vs market 57%)', stat('Tutu Atwell', 'rec'), 1.5, 'O', 'Dressed (ESPN game roster, didNotPlay=false) but 0 targets; LAR threw only 23 times and ran 47 times. The read assumed WR targets with Nacua/Adams out; Mumpfield (5) and the backs took them.', 'reads.json final (pick)', 'pick'))
RD.append(G('Blake Corum over 1.5 catches (model 63% vs market 56%)', stat('Blake Corum', 'rec'), 1.5, 'O', '2 catches on 3 targets (21 yds); backs got 8 of 21 targets.', 'reads.json final (pick)', 'pick'))
RD.append(G('Tyler Higbee under 31.5 receiving yards', stat('Tyler Higbee', 'rec_yds'), 31.5, 'U', '1 catch for 14 on 3 targets; GB held LAR TEs to 5/7 for 27 yds.', 'reads.json final (lean)'))
RD.append(G('Matthew Golden 4+ catches (over 3.5)', stat('Matthew Golden', 'rec'), 3.5, 'O', '1 catch on 5 targets (39 yds, tackled by S K.Curl). VERIFIED defenders on Golden targets: T.McDuffie PBU (Q2 8:54 short right), Q.Lake PBU (Q2 3:17 deep middle), J.McCollough INT (Q3 3:59 deep middle); a T.McDuffie INT on him (Q4 11:57) was REVERSED to an incompletion. aDOT 23.0: he was used deep, not on slot volume.', 'reads.json final (lean; commit 5d31b010)'))
RD.append(G('Christian Watson over 4.5 catches', stat('Christian Watson', 'rec'), 4.5, 'O', '4 catches on 4 targets for 65 yds and the TD, then injured on a Q2 2:00 4th-and-1 throw that was wiped out by offsetting fouls (No Play), and had no target after. Pace was there; injury killed it.', 'reads.json final (lean; commit fbe94cfa)'))
RD.append(G('Tucker Kraft over 3.5 catches', stat('Tucker Kraft', 'rec'), 3.5, 'O', '3 catches on 5 targets (24 yds), plus a 10-yd catch that he fumbled (forced by N.Landman, recovered by Q.Lake). K.Kinchens PBU on one Kraft target. GB ran only 44 plays (19:20 TOP).', 'reads.json final (lean)'))
RD.append(G('Blake Corum over 57.5 rushing yards', stat('Blake Corum', 'rush_yds'), 57.5, 'O', f"32 carries for 184 (68% of LAR carries), long 35. The no-Nacua run lean was right.", 'reads.json final (lean)'))
RD.append(G('Savion Williams over 18.5 receiving yards', stat('Savion Williams', 'rec_yds'), 18.5, 'O', '1 catch for 3 on 3 targets (Q.Lake PBU on one). He did run 2 times for 18.', 'reads.json final (lean)'))
RD.append(G('MarShawn Lloyd over 8.5 receiving yards', stat('MarShawn Lloyd', 'rec_yds'), 8.5, 'O', '1 target, 1 catch for 6. Chris Brooks (5 tgt) was the receiving back.', 'reads.json final (lean)'))
RD.append(G('MarShawn Lloyd over 1.5 catches', stat('MarShawn Lloyd', 'rec'), 1.5, 'O', 'Same play: 1 catch.', 'reads.json final (lean)'))
RD.append(G('Kyren Williams under 54.5 rushing yards', stat('Kyren Williams', 'rush_yds'), 54.5, 'U', '12 carries for 46 (26% of LAR carries). Note: under the 50% carry rule he was do-not-play (well under 50%), so this win does not count as a playable leg.', 'reads.json final (lean)'))
RD.append(G('Tyler Higbee under 3.5 catches', stat('Tyler Higbee', 'rec'), 3.5, 'U', '1 catch.', 'reads.json final (lean)'))
RD.append(G('Colby Parkinson under 20.5 receiving yards', stat('Colby Parkinson', 'rec_yds'), 20.5, 'U', '2 catches for -1.', 'reads.json final (lean)'))
RD.append(G('Matthew Golden under 75.5 receiving yards (superseded)', stat('Matthew Golden', 'rec_yds'), 75.5, 'U', '39 yds. Added in fbe94cfa, then moved to "avoid / pass" in 5d31b010. Would have won.', 'commit fbe94cfa (removed in 5d31b010)'))
RD.append(G('Matthew Golden over 5.5 catches (superseded)', stat('Matthew Golden', 'rec'), 5.5, 'O', '1 catch. In the reads before fbe94cfa; moved to avoid in fbe94cfa. Avoiding it was right.', 'reads before fbe94cfa (removed)'))
AV = [('Watson 73.5 receiving yards (avoid)', f"{stat('Christian Watson','rec_yds')} yds (under 73.5); left injured in Q2. Avoid was neutral-to-right."),
      ('Love passing yards under (avoid)', '198 passing yds on 17/29 (no Love passing line in the freeze; passing-yards legs are off Rico\'s slips anyway).'),
      ('Mumpfield under (avoid)', f"{stat('Konata Mumpfield','rec_yds')} yds on 4/5 vs 34.5 consensus: over. Avoiding the under was right."),
      ('Kaleb Johnson rushing (avoid)', f"8 carries for 13 vs 31.5: under would have won. 8 of 14 GB carries = 57% share, but GB ran only 14 times."),
      ('Golden yards (avoid)', '39 yds vs 74.5 consensus: under would have won.')]
# WR1 shutdown + headline claims
CL = [('Rams corners McDuffie/Forbes shut down WR1s (WR1 3.3 catches/43 yds a game; under in 6 of 9)', 'W', 'GB target leader Golden: 1 catch, 39 yds (catch tackled by S K.Curl, not a corner). McDuffie: PBU on Golden; Forbes: INT on B.Melton. VERIFIED corner credits on GB WRs: McDuffie 1 PBU, Forbes 1 INT. But Watson (the other starter) caught 4/4 for 65 before his injury.'),
      ('Since Week 6 every TE1 caught 5+ vs the Rams', 'L', 'Kraft 3 catches on 5 targets.'),
      ('Without Nacua the Rams lean on the backs; Corum out-gains Kyren', 'W', 'LAR ran 47 times (30% early-down pass rate). Corum 184 vs Kyren 46.'),
      ('Rams 4-man rush heating up (42% sack-or-hit last game)', 'L', 'LAR: 1 sack (B.Young) and 3 nflverse QB hits (the sack is one of them) = 3 of 31 GB dropbacks hit or sacked, about 10% (estimate). Love got the ball out; the damage came from coverage (2 INTs + 3 PBUs on deep/middle throws).'),
      ('Rams allow few explosive catches (2.3 a game)', 'W', 'GB had 3 completions of 20+ (Watson 32 and 21, Golden 39).'),
      ('Soft spots: safeties Curl and Kinchens', 'Split', 'Curl was the tackler on 2 catches for 71 yds (Watson 32, Golden 39; inferred, tackler tag). Kinchens: 2 VERIFIED PBUs and 0 catches tagged; he was disqualified at Q2 2:00 (offsetting fouls).'),
      ('Love produces with a thin line (288/372 in Weeks 8-9)', 'L', '198 yds, 1 TD, 2 INT, QBR 39.7.')]
# dashboard game_bets
TB = []
for p in dash['game_bets']['picks']:
    b = p['best']; per = p['period']; side = b['side']; line = b['line']
    if p['market'] == 'moneyline': r = 'W' if side == 'LA' else 'L'; act = f'LAR won {LA}-{GB}'
    elif p['market'] == 'total': r = res(LA+GB, line, 'O' if side == 'Over' else 'U'); act = f'{LA+GB}'
    else:
        seg = {'Game': (GB, LA), '2nd quarter': (10, 7), '1st half': (13, 13), '2nd half': (0, 13)}[per]
        m = (seg[1] - seg[0]) if side == 'LA' else (seg[0] - seg[1]); r = 'PUSH' if m + line == 0 else ('W' if m + line > 0 else 'L'); act = f'GB {seg[0]} - LAR {seg[1]}'
    TB.append((p['market'], per, f"{side} {line if line is not None else ''} {b['american']:+d} ({b['book']}{', alt' if b['alt'] else ''})", f"model {b['p_model']:.1%} / market {b['p_market']:.1%}", act, r))
L += ['<!-- GBLAR-GRADE-END -->']
open(f'{OUT}/data/_grade_lock.md', 'w').write('\n'.join(L) + '\n')
# ---------------- READS section
R = ['<!-- GBLAR-READS-START -->', '## Pregame reads graded (reads.json, dashboard, brief, and the GB@LAR read commits)', '',
     f'Actuals: ESPN box (event 401873079, FINAL). Lines are the read\'s own line. Graded {NOWS}. Research only; none of these were vetted slips.', '',
     '| Read | Source | Line | Actual | Result | Why |', '|---|---|---|---|---|---|']
for x in RD: R.append(f"| {x['play']} | {x['src']} | {'O' if x['side']=='O' else 'U'} {x['line']} | {x['actual']} | **{x['result']}** | {x['note']} |")
live = [x for x in RD if 'superseded' not in x['play']]
w = sum(x['result'] == 'W' for x in live); l = sum(x['result'] == 'L' for x in live)
pk = [x for x in live if x['kind'] == 'pick']
R += ['', f"Final reads.json (picks + leans, excluding superseded): **{w}-{l}**. Model picks (with a model %): {sum(x['result']=='W' for x in pk)}-{sum(x['result']=='L' for x in pk)}. Every under won ({sum(1 for x in live if x['side']=='U' and x['result']=='W')}/{sum(1 for x in live if x['side']=='U')}); {sum(1 for x in live if x['side']=='O' and x['result']=='L')} of {sum(1 for x in live if x['side']=='O')} overs lost; the only overs that won were Corum's two.", '',
      '### Avoid list (reads.json final)', '', '| Avoided | What happened |', '|---|---|'] + [f'| {a} | {b} |' for a, b in AV]
R += ['', '### Headline claims (reads.json headline)', '', '| Claim | Result | Evidence |', '|---|---|---|'] + [f'| {a} | {b} | {c} |' for a, b, c in CL]
R += ['', '### Dashboard game bets (dashboard/data/2026_12_GB_LA.json game_bets; best price per the board at 23:26Z)', '', '| Market | Period | Board side | Model / market | Actual | Result |', '|---|---|---|---|---|---|'] + [f'| {a} | {b} | {c} | {d_} | {e} | **{f}** |' for a, b, c, d_, e, f in TB]
R += ['', 'Note: the three full-game board picks priced at the "open" book are stale opening numbers (GB +185, GB +4.5, Under 48.5), not prices available at the lock; their EV is not real. At the real lock numbers: LAR -2.5 covered, Under 43.5 won, LAR ML won.', '']
tp = dash['team_projection']['samplers']
R += ['### Team score projection (period_engine_v0, unvalidated)', '', '| Sampler | Projected | Actual | Side | Total vs 43.5 |', '|---|---|---|---|---|']
for k, s in tp.items():
    R.append(f"| {k} | GB {s['away_points']} - LAR {s['home_points']} (total {s['total']}, LAR covers {s['home_covers_market_spread']:.1%}, over {s['over_market_total']:.1%}) | GB 13 - LAR 26 (39) | LAR side right | over lean wrong (39 under) |")
R += ['', 'Both samplers leaned over (56% and 72%); the game went 4.5 under. This fits the known +0.794 total bias of period_engine_v0.', '']
# brief matchup flags
WRY = sum(stat(n, 'rec_yds') for n in ('Matthew Golden', 'Christian Watson', 'Bo Melton', 'Savion Williams', 'J. Michael Sturdivant'))
GBRB = sum(stat(n, 'rush_yds') for n in ('Kaleb Johnson', 'MarShawn Lloyd', 'Chris Brooks'))
LARB = sum(stat(n, 'rush_yds') for n in ('Blake Corum', 'Kyren Williams'))
TEY = sum(stat(n, 'rec_yds') for n in ('Tyler Higbee', 'Davis Allen', 'Colby Parkinson'))
GBRBREC = sum(stat(n, 'rec_yds') for n in ('Kaleb Johnson', 'MarShawn Lloyd', 'Chris Brooks'))
R += ['### Brief "Matchup edges" flags', '', '| Flag | Pregame numbers | Actual | Held? |', '|---|---|---|---|',
      f'| LA defence strength: WR yards | GB WRs 212.1/g; LA allows 110.9 | GB WRs {WRY} | yes |',
      f'| LA defence weak spot: RB receiving yards | LA allows 45.1 | GB RBs {GBRBREC} receiving | yes (47 = at the weak-spot rate) |',
      f'| LA defence advantage: RB rushing yards | GB RBs 57.1; LA allows 67.8 | GB RBs {GBRB} | yes |',
      '| GB offence strength: explosive passes (20+) | 4.4/g | 3 | no (below GB norm) |',
      '| LA defence strength: third downs | LA allows 27.7% | GB 2/8 (25%) | yes |',
      '| LA defence strength: red-zone TD | LA allows 47.8% | GB 1/1 TD | no (1 trip) |',
      '| LA defence weak spot: pressure (sacks+hits) | LA 11.8% | 3 of 31 GB dropbacks hit or sacked (10%, estimate) | yes (LA rush stayed light) |',
      f'| LA offence strength: RB rushing yards | LA RBs 123.1; GB allows 101.2 | LAR RBs {LARB} | yes, big |',
      f'| GB defence strength: TE yards | GB allows 41.5 | LAR TEs {TEY} | yes |', '']
R += ['### Rule checks (Rico\'s standing rules)', '',
      '- 50% carry rule: Corum 32/47 = 68% (eligible). Kyren 12/47 = 26% (do-not-play; his under won but is not a playable leg). Kaleb Johnson 8/14 = 57% of GB carries (eligible by share, but GB ran only 14 times).',
      '- Receiving legs need a verified main defender: none of the receiving reads had a VERIFIED main defender before kickoff (season tackler/PFR tags only), so under the rules none were playable as receiving legs.',
      '- No passing-yards legs: none graded as legs (Love/Stafford passing listed for context only).', '<!-- GBLAR-READS-END -->']
open(f'{OUT}/data/_grade_reads.md', 'w').write('\n'.join(R) + '\n')
# ---------------- QB production
Q = ['<!-- GBLAR-QB-START -->', f'## QB production (ESPN box + nflverse pbp, asset updated 2026-11-26 01:03 AM EST)', '',
     'Roof: SoFi Stadium, fixed translucent roof (indoor; the pregame packet lists roof = dome). ESPN gameInfo has no weather block; no weather effect.', '',
     '| QB | Comp/Att | Yds | Y/A | TD | INT | Sacks-yds | QBR | Rating | Rush | Dropbacks | aDOT | Deep (15+ air) comp/att | CPOE (mean) | EPA/dropback |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
box = {}
for tp_ in d['boxscore']['players']:
    for c in tp_['statistics']:
        if c['name'] == 'passing':
            for a in c['athletes']: box[a['athlete']['displayName']] = dict(zip(c['labels'], a['stats']))
qbsplit = {}
for qb, team, nm in (('J.Love', 'GB', 'Jordan Love'), ('M.Stafford', 'LA', 'Matthew Stafford')):
    db = g[(g.posteam == team) & (g.qb_dropback == 1) & g.play_type.isin(['pass', 'run'])]
    pa = g[(g.posteam == team) & (g.pass_attempt == 1) & (g.sack == 0) & (g.play_type == 'pass')]
    deep = pa[pa.air_yards >= 15]; b = box[nm]
    hit = db[(db.qb_hit == 1) | (db.sack == 1)]; clean = db[(db.qb_hit == 0) & (db.sack == 0)]
    def line(x):
        a = x[(x.pass_attempt == 1) & (x.sack == 0)]
        return f"{int(a.complete_pass.sum())}/{len(a)}, {int(a[a.complete_pass==1].yards_gained.sum())} yds, {int(a.interception.sum())} INT, {int(x.sack.sum())} sk"
    rush = P['GB' if team == 'GB' else 'LAR'].get(nm, {})
    Q.append(f"| {nm} | {b['C/ATT']} | {b['YDS']} | {b['AVG']} | {b['TD']} | {b['INT']} | {b['SACKS']} | {b['QBR']} | {b['RTG']} | {rush.get('car',0)}-{rush.get('rush_yds',0)} | {len(db)} | {pa.air_yards.mean():.1f} | {int(deep.complete_pass.sum())}/{len(deep)} | {pa.cpoe.mean():+.1f} | {db.qb_epa.mean():+.2f} |")
    qbsplit[nm] = {'hit_or_sacked': line(hit), 'n_hit': len(hit), 'clean': line(clean), 'n_clean': len(clean), 'by_q': {q: line(db[db.qtr == q]) for q in (1, 2, 3, 4)},
                   'by_loc': {k: f"{int(v.complete_pass.sum())}/{len(v)}" for k, v in pa.groupby('pass_location')},
                   'shotgun': f"{int(db.shotgun.sum())}/{len(db)}", 'pressure_est': f"{len(hit)}/{len(db)} = {100*len(hit)/len(db):.0f}%"}
Q += ['', '| QB | Pressure ESTIMATE (dropbacks with a sack or nflverse QB hit) | When hit/sacked | Clean (no hit/sack) | Q1 | Q2 | Q3 | Q4 | Pass location comp/att (L/M/R) |', '|---|---|---|---|---|---|---|---|---|']
for nm, s in qbsplit.items():
    Q.append(f"| {nm} | {s['pressure_est']} | {s['hit_or_sacked']} | {s['clean']} | {s['by_q'][1]} | {s['by_q'][2]} | {s['by_q'][3]} | {s['by_q'][4]} | {s['by_loc'].get('left','0/0')} / {s['by_loc'].get('middle','0/0')} / {s['by_loc'].get('right','0/0')} |")
Q += ['', '- vs blitz / no blitz: **UNKNOWN**. FTN charting (n_blitzers, n_pass_rushers) in nflverse ftn_charting_2026 only runs through week 11 at pull time. TODO: re-run after the next FTN update.',
      '- vs man / zone and MOF open/closed: **UNKNOWN** (no free play-level charting). Season-level rates are in the defense profiles (StatRankings primary, Sharp cross-check, never mixed).',
      '- True pressure rate: **UNKNOWN**; the pressure figure above is an ESTIMATE from sacks + QB hits only (hurries are not in free data).',
      '- Love turnovers: INT by J.McCollough (Q3 3:59, deep middle to Golden, at LA 3), INT by E.Forbes (Q4 3:46, deep right to B.Melton); a McDuffie INT (Q4 11:57) was overturned on replay; a K.Curl INT (Q1 7:28) was wiped out by an Illegal Contact penalty on E.Forbes (No Play). Kraft lost a fumble after a 10-yd catch (Q1 7:15). Stafford INT: T.Hopper (Q3 4:43, short left to Higbee); one aborted snap at GB 26 recovered by Corum.',
      '<!-- GBLAR-QB-END -->']
open(f'{OUT}/data/_grade_qb.md', 'w').write('\n'.join(Q) + '\n')
# ---------------- inactives + burned
I = ['<!-- GBLAR-ROSTER-START -->', '## Inactives / did not play (ESPN core API game roster, pulled ' + NOWS + ')', '']
for ab in ('GB', 'LAR'):
    I.append(f"- **{ab}** ({ros[ab]['n']} on game roster): " + ', '.join(f'{n} ({p})' for n, p in ros[ab]['dnp']))
I += ['- Not on either game roster (IR/out before the game): Puka Nacua and Davante Adams (LAR) do not appear; Josh Jacobs (GB) is listed did-not-play.', '- Tutu Atwell and CJ Daniels (LAR) were on the game roster with didNotPlay=false and no target or carry logged.', '']
dl = json.load(open(f'{OUT}/data/GB_at_LAR_pass_defender_log.json'))
I += ['## Who got burned (named defenders; VERIFIED vs inferred kept apart)', '',
      'VERIFIED coverage events are only PBU / INT / DPI. Yards "allowed" below are tackler tags on completions (inferred, not proof of coverage). No Play snaps write no rows except DPI credit; the Q4 11:57 McDuffie INT reversal is graded as an incompletion with no PBU.', '',
      '**GB defense (inferred, tackler tags):** K.Nixon (CB) 6 catches / 52 yds (D.Allen 2, Mumpfield 2, K.Williams, X.Smith; long 20 to Mumpfield). E.Williams (S) 2/29, X.McKinney (S) 2/25 (Mumpfield 24). VERIFIED: B.Cisse (CB) DPI 37 yds on X.Smith (Q1 11:59); T.Hopper (LB) INT on Higbee. GB was not burned through the air (LAR 140 net passing yards); it was run over: Corum 32-184, including a 35-yd run (tackled by X.McKinney), and LAR RBs 230 rush yds.',
      '**LAR defense (inferred, tackler tags):** K.Curl (S) 2 catches / 71 yds (Watson 32, Golden 39), the biggest leak. T.McDuffie (CB) 2/31 + 1 VERIFIED PBU on Golden. E.Forbes (CB) 3/22 + VERIFIED INT on Melton. Q.Lake (S) 2/13 + 2 VERIFIED PBUs. K.Kinchens (S) 2 VERIFIED PBUs, 0 catches tagged (ejected Q2 2:00). J.McCollough (S) VERIFIED INT on Golden. A.Donald (DT) VERIFIED batted/PBU on K.Johnson.',
      '', 'Explosive plays allowed by player type: GB allowed WR 24 and 20 (Mumpfield) and RB rush 35 (Corum). LAR allowed WR 32 and 21 (Watson) and WR 39 (Golden).',
      f"Leaks by target position: GB allowed WR 5/6 for 73, RB 6/8 for 40, TE 5/7 for 27. LAR allowed WR 8/16 for 127 (1 TD), RB 6/8 for 47, TE 3/5 for 24. Slot vs outside: UNKNOWN (no free alignment data).",
      '<!-- GBLAR-ROSTER-END -->']
open(f'{OUT}/data/_grade_roster.md', 'w').write('\n'.join(I) + '\n')
# stitch into game md
gp = f'{OUT}/GB_at_LAR.md'; t = open(gp).read()
for tag in ('GRADE', 'READS', 'QB', 'ROSTER'): t = re.sub(rf'<!-- GBLAR-{tag}-START -->.*?<!-- GBLAR-{tag}-END -->\n?', '', t, flags=re.S)
t = t.replace('## Scoring plays', open(f'{OUT}/data/_grade_lock.md').read() + '\n' + open(f'{OUT}/data/_grade_reads.md').read() + '\n## Scoring plays', 1)
t = t.replace('## QB vs coverage shell / pressure', open(f'{OUT}/data/_grade_qb.md').read() + '\n' + open(f'{OUT}/data/_grade_roster.md').read() + '\n## QB vs coverage shell / pressure', 1)
t = t.replace("Players absent from the ESPN receiving box had no target or reception logged; whether they played is unknown until snap counts post (nflverse/PFR, usually Monday-Tuesday).",
              "Players absent from the ESPN receiving box had no target or reception logged. Played/inactive status is from the ESPN game roster (see Inactives); snap shares stay unknown until snap counts post.")
t = t.replace('Open-Meteo: not pulled (neutral site or unmapped)', 'Open-Meteo: not pulled (LAR is not in the stadium map). SoFi Stadium has a fixed translucent roof, so outdoor weather does not apply; the pregame packet lists roof = dome and weather INDOOR.')
open(gp, 'w').write(t)
json.dump({'lock': FZ_PATH, 'pulled_utc': meta['pulled_utc'], 'final': {'GB': GB, 'LAR': LA}, 'props': props, 'reads': RD, 'dashboard_bets': TB, 'qb': qbsplit, 'inactives': {k: v['dnp'] for k, v in ros.items()}},
          open(f'{OUT}/data/GB_at_LAR_grades.json', 'w'), indent=1, default=str)
print('\n'.join(L[:12])); print('\n'.join(R[:30])); print('\n'.join(Q))
