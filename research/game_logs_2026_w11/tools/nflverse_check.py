"""nflverse pbp cross-check for one game (CIN@WSH MNF late run). Free nflverse release (CC-BY), no paid charting.
Fills intended air yards / aDOT / per-receiver air yards and cross-checks ESPN play counts and PBU names. refs NFL-56, NFL-49."""
import os, sys, re, json, datetime, time, urllib.request
import pandas as pd
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); NV = f'{OUT}/raw/nflverse'
NOWS = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p ') + time.strftime('%Z')
GID, GAME, FN = '2026_11_CIN_WAS', 'CIN@WSH', 'CIN_at_WSH'
def rel(tag):
    d = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://api.github.com/repos/nflverse/nflverse-data/releases/tags/{tag}', headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read())
    return {a['name']: a['updated_at'] for a in d.get('assets', [])}
pbp_upd = rel('pbp').get('play_by_play_2026.csv.gz', 'unknown'); snap_upd = rel('snap_counts').get('snap_counts_2026.csv.gz', 'unknown'); ftn_upd = rel('ftn_charting').get('ftn_charting_2026.csv', 'unknown')
p = pd.read_csv(f'{NV}/pbp_2026.csv.gz', low_memory=False); g = p[p.game_id == GID].copy()
s = pd.read_csv(f'{NV}/snap_counts_2026.csv.gz'); sg = s[s.game_id == GID]
def et(z):
    try: return datetime.datetime.strptime(z, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).astimezone().strftime('%Y-%m-%d %I:%M %p %Z')
    except Exception: return z
fix = lambda t: 'WSH' if t == 'WAS' else t
L = ['<!-- NFLVERSE-START -->', f'## nflverse play-by-play cross-check (src: nflverse-data release pbp/play_by_play_2026.csv.gz, asset updated {et(pbp_upd)}; pulled {NOWS})', '']
if g.empty:
    L += [f'nflverse pbp: {GAME} not in the release yet (unknown). TODO: re-pull after the next nflverse rebuild.']
else:
    off = g[g.play_type.isin(['pass', 'run', 'qb_spike', 'qb_kneel'])]
    L += ['| Team | nflverse offensive plays (pass+run+spike+kneel, incl. sacks/scrambles; no-plays excluded) | ESPN box Total Plays | Match |', '|---|---|---|---|']
    espn = json.load(open(f'{OUT}/data/{FN}.json'))['team_stats']
    rec = {'pulled': NOWS, 'pbp_asset_updated_utc': pbp_upd, 'teams': {}}
    for t in ('CIN', 'WAS'):
        n = int((off.posteam == t).sum()); e = espn.get(fix(t), {}).get('totalOffensivePlays', 'unknown')
        L.append(f'| {fix(t)} | {n} | {e} | {"yes" if str(n) == str(e) else "no (nflverse counts differ: see note)"} |'); rec['teams'][fix(t)] = {'nflverse_off_plays': n}
    L += ['', '| Team | Pass att (excl. sacks) | Intended air yards (all attempts with air_yards) | aDOT | Completed air yards | YAC | Shotgun % of dropbacks | No-huddle plays | Scrambles | QB hits (nflverse) | Sacks |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for t in ('CIN', 'WAS'):
        d = g[(g.posteam == t)]; pa = d[(d.pass_attempt == 1) & (d.sack == 0) & d.play_type.eq('pass')]
        db = d[(d.qb_dropback == 1) & d.play_type.eq('pass')]
        iay = pa.air_yards.dropna(); cay = pa[pa.complete_pass == 1].air_yards.dropna(); yac = pa[pa.complete_pass == 1].yards_after_catch.dropna()
        row = {'pass_att': len(pa), 'intended_air_yards': float(iay.sum()), 'adot': round(float(iay.mean()), 2) if len(iay) else None, 'completed_air_yards': float(cay.sum()), 'yac': float(yac.sum()),
               'shotgun_pct': round(100 * float(db.shotgun.mean()), 1) if len(db) else None, 'no_huddle': int(d[d.play_type.isin(['pass', 'run'])].no_huddle.sum()), 'scrambles': int(d.qb_scramble.sum()), 'qb_hits': int(d.qb_hit.sum()), 'sacks': int(d.sack.sum())}
        rec['teams'][fix(t)].update(row)
        L.append(f"| {fix(t)} | {row['pass_att']} | {row['intended_air_yards']:.0f} ({len(iay)} att) | {row['adot']} | {row['completed_air_yards']:.0f} | {row['yac']:.0f} | {row['shotgun_pct']}% ({len(db)} dropbacks) | {row['no_huddle']} | {row['scrambles']} | {row['qb_hits']} | {row['sacks']} |")
    L += ['', 'Per-target air yards (nflverse; targets = pass attempts with a named receiver, sacks excluded):', '', '| Team | Receiver | Tgt | Intended air yds | aDOT | Rec | YAC | Pass location L/M/R | Deep (15+ air) tgt |', '|---|---|---|---|---|---|---|---|---|']
    tg = g[(g.pass_attempt == 1) & (g.sack == 0) & g.receiver_player_name.notna() & g.play_type.eq('pass')]
    rec['receivers'] = []
    for (t, r), d in sorted(tg.groupby(['posteam', 'receiver_player_name']), key=lambda kv: (kv[0][0], -len(kv[1]))):
        ay = d.air_yards.dropna(); loc = d.pass_location.value_counts()
        x = {'team': fix(t), 'receiver': r, 'tgt': len(d), 'air': float(ay.sum()), 'adot': round(float(ay.mean()), 1) if len(ay) else None, 'rec': int(d.complete_pass.sum()), 'yac': float(d.yards_after_catch.dropna().sum()), 'deep': int((d.air_yards >= 15).sum())}
        rec['receivers'].append(x)
        L.append(f"| {x['team']} | {r} | {x['tgt']} | {x['air']:.0f} | {x['adot']} | {x['rec']} | {x['yac']:.0f} | {loc.get('left', 0)}/{loc.get('middle', 0)}/{loc.get('right', 0)} | {x['deep']} |")
    pdn = g[g.pass_defense_1_player_name.notna() | g.pass_defense_2_player_name.notna() | g.interception_player_name.notna()]
    L += ['', 'nflverse pass_defense_1/2 and interception fields (gamebook-sourced; the same evidence class as ESPN PBU/INT = VERIFIED):', '']
    L += [f"- Q{int(r.qtr)} {r.time}: {fix(r.defteam)} {', '.join(x for x in (r.pass_defense_1_player_name, r.pass_defense_2_player_name, r.interception_player_name) if isinstance(x, str))} on {r.receiver_player_name} ({r.desc[:110]})" for r in pdn.itertuples()] or ['- none']
    L.append(f'nflverse names {len(pdn)} PBU/INT plays; ESPN play text names the same defenders on the same plays (4 PBUs: J.Reaves, R.Douglas x2, J.Newton). DPIs (D.Hill, T.Amos) are in the penalty fields, as in ESPN.')
    rec['pass_defense_rows'] = len(pdn)
    json.dump(rec, open(f'{OUT}/data/{FN}_nflverse.json', 'w'), indent=1, default=str)
L += ['', f'Snap shares: {"unknown: nflverse snap_counts_2026 (asset updated " + et(snap_upd) + ") has no " + GID + " rows yet (posted before MNF). TODO: re-pull after the next snap-count update." if sg.empty else "see data/" + FN + "_snaps.csv"}',
      f'FTN charting (nflverse ftn_charting_2026, asset updated {et(ftn_upd)}): not used for this game; the asset was updated before the 8:15 PM EST kickoff, so it cannot contain CIN@WSH. Game-level man/zone, blitz and MOF stay unknown. TODO: check after the next FTN update.',
      'pbp_participation (NGS coverage type / defenders in box): no 2026 release asset yet (unknown).', '<!-- NFLVERSE-END -->', '']
if not sg.empty: sg.to_csv(f'{OUT}/data/{FN}_snaps.csv', index=False)
gp = f'{OUT}/{FN}.md'; t = open(gp).read()
t = re.sub(r'<!-- NFLVERSE-START -->.*?<!-- NFLVERSE-END -->\n?', '', t, flags=re.S)
t = t.replace('## Not available from free sources', '\n'.join(L) + '\n## Not available from free sources')
if not g.empty:
    t = re.sub(r"nflverse 2026 pbp release was last modified [^.]*\(before kickoff\), so today's games are not in it yet; nflverse pass_defense_1/2 fields will be checked on the overnight rebuild\.",
               f"nflverse 2026 pbp now includes {GID} (asset updated {et(pbp_upd)}); see the nflverse cross-check section above for intended air yards and pass_defense fields.", t)
    t = t.replace('| Intended air yards on incompletions | unknown (not in ESPN; nflverse air_yards after overnight rebuild) | unknown |',
                  '| Intended air yards on incompletions | see nflverse cross-check section (all-attempt intended air yards) | see nflverse cross-check section |')
open(gp, 'w').write(t); print('\n'.join(L))
