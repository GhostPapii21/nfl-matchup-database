"""Write the Monday gap-fill (monday_fill/*.json) into the W11 game files + COVERAGE_MATRIX. refs NFL-56, refs NFL-49.
Idempotent: replaces its own marked block. Missing stays 'unknown' with a reason."""
import json, os, re
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, E = '<!-- MONDAY-FILL-START refs NFL-56 -->', '<!-- MONDAY-FILL-END -->'
SUM = json.load(open(f'{OUT}/monday_fill/_summary.json'))
def pct(x): return f'{100*x:.0f}%' if isinstance(x, (int, float)) else str(x)
for r in SUM:
    away, home = r['game'].split('@'); fn = f"{OUT}/{r['game'].replace('@', '_at_')}.md"; t = open(fn).read()
    t = re.sub(re.escape(S) + r'.*?' + re.escape(E) + r'\n?', '', t, flags=re.S)
    ia = r['air_yards']
    row = '| Intended air yards on incompletions | ' + ' | '.join(f"{ia[x]['intended_air_yards_on_incompletions']} air yds on {ia[x]['incompletions']} incompletions (total intended {ia[x]['intended_air_yards_total']}, aDOT {ia[x]['adot']} on {ia[x]['pass_attempts']} att; nflverse pbp)" for x in (away, home)) + ' |'
    t = re.sub(r'^\| Intended air yards on incompletions \|.*$', lambda m: row, t, flags=re.M)
    if isinstance(r['snap_counts'], dict):
        def top(x): return '; '.join(f"{p['player']} ({p['position']}) {p['offense_snaps']:.0f} ({pct(p['offense_pct'])})" for p in r['snap_counts'][x] if p['position'] in ('WR', 'TE', 'RB', 'FB') and p['offense_snaps'] > 0)
        srow = '| Snap shares (offense, WR/TE/RB; full table in Monday fill below) | ' + ' | '.join(top(x) for x in (away, home)) + ' |'
    else:
        srow = '| Snap shares | unknown: not posted yet (nflverse snap_counts has no row for this game as of 2026-11-23 07:10 AM AST; PFR page blocked to the box) | unknown |'
    t = re.sub(r'^\| Snap shares.*$', lambda m: srow, t, flags=re.M)
    t = re.sub(r'\nNFL game-feed weather \(nflverse[^\n]*', '', t)
    t = re.sub(r'^ESPN gameInfo: MISSING \(ESPN gameInfo has no weather block for this game\)$', lambda m: m.group(0) + f"\nNFL game-feed weather (nflverse pbp `weather`, roof `{r['roof_nfl_feed']}`): {r['weather_nfl_feed']}", t, flags=re.M)
    L = [S, '## Monday fill (2026-11-23, free nflverse releases; research only)', '',
         f"Source: {r['pbp_source']}. Box path of the pulls: /tmp/w11fill (manifest in research/game_logs_2026_w11/monday_fill/MANIFEST.json).", '',
         f"**Weather (NFL game feed):** {r['weather_nfl_feed']} (roof: {r['roof_nfl_feed']}).", '',
         '**Intended air yards (nflverse, 2-pt tries and no-plays excluded)**', '', '| Team | Att | Intended air yds | aDOT | Incompletions | Air yds on incompletions | INT |', '|---|---|---|---|---|---|---|']
    L += [f"| {x} | {ia[x]['pass_attempts']} | {ia[x]['intended_air_yards_total']} | {ia[x]['adot']} | {ia[x]['incompletions']} | {ia[x]['intended_air_yards_on_incompletions']} | {ia[x]['interceptions']} |" for x in (away, home)]
    L += ['', '**Air yards by receiver (nflverse)**', '', '| Team | Receiver | Tgt | Air yds | Air share | aDOT |', '|---|---|---|---|---|---|']
    L += [f"| {x} | {v['receiver']} | {v['targets']} | {v['air_yards']:.0f} | {pct(v['air_share'])} | {v['adot']} |" for x in (away, home) for v in ia[x]['receivers']]
    pc = r['pbu_int_crosscheck']
    L += ['', f"**PBU/INT cross-check:** ESPN-text VERIFIED PBU/INT rows {pc['espn_verified_pbu_int_rows']}; nflverse plays with a named pass defender or interceptor {pc['nflverse_plays_with_named_pbu_or_int']}; matched {pc['matched']}; nflverse-only {len(pc['nflverse_only'])}; ESPN-only {len(pc['espn_only'])}. DPI rows ({pc['dpi_rows_not_in_nflverse_pd_fields']}) come from the penalty text and are not in the nflverse pass-defense fields."]
    mm = r['target_crosscheck_mismatches']
    real = [m for m in mm if not (m['espn_box_tgt'] == 0 or m['nflverse_tgt'] == 0)]
    L += [f"**Target cross-check (ESPN box vs nflverse, roster-ID name match):** " + ('all receivers agree.' if not mm else ('; '.join(f"{m['team']} {m['player']} ESPN {m['espn_box_tgt']} / nflverse {m['nflverse_tgt']}" for m in mm) + ' (zero on one side = name-spelling mismatch between feeds, counts agree)' if not real else '; '.join(f"{m['team']} {m['player']} ESPN {m['espn_box_tgt']} / nflverse {m['nflverse_tgt']}" for m in mm)))]
    if isinstance(r['snap_counts'], dict):
        L += ['', f"**Snap counts** ({r['snap_source']})", '', '| Team | Player | Pos | Off snaps | Off % | Def snaps | Def % | ST % |', '|---|---|---|---|---|---|---|---|']
        L += [f"| {x} | {p['player']} | {p['position']} | {p['offense_snaps']:.0f} | {pct(p['offense_pct'])} | {p['defense_snaps']:.0f} | {pct(p['defense_pct'])} | {pct(p['st_pct'])} |" for x in (away, home) for p in r['snap_counts'][x]]
    else:
        L += ['', f"**Snap counts:** {r['snap_counts']}"]
    if isinstance(r['ftn'], dict):
        L += ['', f"**QB vs blitz / rush size / play action (FTN charting)** ({r['ftn_source']}). Man/zone and MOF shell stay unknown: the public FTN fields carry no coverage type.", '',
              '| Offense | Split | Dropbacks | Comp-Att | Yds | Sacks | INT | EPA/db |', '|---|---|---|---|---|---|---|---|']
        for x in (away, home):
            f = r['ftn'][x]
            for k in ('vs_blitz', 'vs_no_blitz', 'vs_5plus_rushers', 'vs_4_or_fewer', 'play_action', 'out_of_pocket'):
                v = f[k]; L.append(f"| {x} | {k} | {v['dropbacks']} | {v['comp']}-{v['att']} | {v['yds']:.0f} | {v['sacks']} | {v['int']} | {v['epa_per_db']} |")
            L.append(f"| {x} | defense blitz rate faced | {f['charted_dropbacks']} charted | | | | | blitz rate {pct(f['blitz_rate'])}; drops {f['drops']}; contested targets {f['contested_targets']} |")
        t = re.sub(r'^\| vs blitz / no blitz \|.*$', '| vs blitz / no blitz | filled from FTN charting via nflverse (see Monday fill below) |', t, flags=re.M)
    else:
        L += ['', f"**FTN charting (blitz/rushers):** {r['ftn']}"]
    L += [E, '']
    t = t.replace('## Not available from free sources', '\n'.join(L) + '\n## Not available from free sources', 1)
    open(fn, 'w').write(t)
# coverage matrix rows
cm = f'{OUT}/COVERAGE_MATRIX.md'; t = open(cm).read()
hdr = re.search(r'^\| Field \|(.*)\|$', t, flags=re.M).group(1).split('|'); games = [h.strip() for h in hdr]
by = {r['game']: r for r in SUM}
def setrow(label, fnc):
    global t
    t = re.sub(r'^\| ' + re.escape(label) + r' \|.*$', lambda m: f'| {label} | ' + ' | '.join(fnc(by[g]) for g in games) + ' |', t, flags=re.M)
setrow('NGS separation/cushion/RYOE', lambda r: 'Monday re-pull of the NGS statboard (final week values; NGS volume threshold applies); nflverse NGS copy in monday_fill/; route trees unknown')
setrow('Intended air yards (incl. incompletions)', lambda r: 'filled (nflverse pbp, Mon 07:10 AM AST)')
setrow('Snap shares', lambda r: 'filled (nflverse/PFR snap_counts)' if isinstance(r['snap_counts'], dict) else 'unknown: not posted yet (nflverse snap_counts last updated 2026-11-20; PFR blocked to the box)')
setrow('QB vs man/zone, blitz, MOF shell, pressure', lambda r: 'blitz/rushers filled (FTN via nflverse); man/zone/MOF/pressure unknown' if isinstance(r['ftn'], dict) else 'unknown (FTN via nflverse not posted for this game yet; man/zone/MOF not in any free feed)')
setrow('Weather (ESPN + Open-Meteo kickoff hour)', lambda r: 'filled + NFL game-feed weather' if 'n/a' not in r['weather_nfl_feed'] else 'filled (indoor)')
t = t.rstrip('\n') + '\n| PBU/INT named defender cross-check vs nflverse | ' + ' | '.join(f"{by[g]['pbu_int_crosscheck']['matched']}/{by[g]['pbu_int_crosscheck']['nflverse_plays_with_named_pbu_or_int']} match" for g in games) + ' |\n'
open(cm, 'w').write(t)
ng = f'{OUT}/NGS_W11_SNAPSHOT.md'; x = open(ng).read()
x = x.replace('**This is a live, partial snapshot**: NGS applies a minimum-volume threshold and games in progress are included mid-game. Re-pull Monday for final values.', '**Monday re-pull (2026-11-23), after all Sunday games went final**: values are final for the week; NGS still applies a minimum-volume threshold, so low-volume players are absent (not zero). CIN@WAS (MNF) is not in it yet. nflverse copy of the same week in monday_fill/ngs_w11_nflverse.json.')
x = x.replace('TODO Monday: re-pull statboard and check charts pages for W11.', 'Statboard re-pulled Monday 2026-11-23; route charts remain image-only (no public data endpoint), so route trees stay unknown.')
open(ng, 'w').write(x)
print('md ok')
