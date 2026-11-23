"""W11 Monday gap-fill from free nflverse releases (refs NFL-56, refs NFL-49). Research only; projection_ready untouched.
Fills: NFL game-feed weather, intended air yards (incl. incompletions) + per-receiver air yards, PBU/INT cross-check vs the
ESPN-text VERIFIED rows, target cross-check, snap shares + FTN charting (blitz/rushers) where posted (IND@HOU only so far).
Missing stays 'unknown' with a reason, never zero.  Usage: python3 monday_fill.py <dir with nflverse files> <manifest.json>"""
import sys, os, json, re, collections, unicodedata
import pandas as pd
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, MAN = sys.argv[1], json.load(open(sys.argv[2]))
FILL = f'{OUT}/monday_fill'; os.makedirs(FILL, exist_ok=True)
P = pd.read_parquet(f'{SRC}/play_by_play_2026.parquet'); P = P[P.week == 11]
R = pd.read_parquet(f'{SRC}/roster_weekly_2026.parquet'); R = R[R.week == 11]
S = pd.read_parquet(f'{SRC}/snap_counts_2026.parquet'); S = S[S.week == 11]
F = pd.read_parquet(f'{SRC}/ftn_charting_2026.parquet'); F = F[F.week == 11]
def src(k): m = MAN[k]; return f"nflverse-data `{m['tag']}/{m['asset']}` (release updated {m['updated_at']}, sha256 {m['sha256'][:12]}, pulled {MAN['pulled_ast']})"
def clk(t): m, s = str(t).split(':'); return f'{int(m)}:{s}'
def norm(n): n = unicodedata.normalize('NFKD', str(n)).encode('ascii', 'ignore').decode(); n = re.sub(r'\b(Jr|Sr|II|III|IV|V)\.?$', '', n.strip()).strip(); return re.sub(r'[^a-z]', '', n.lower())
summary = []
for g in json.load(open(f'{OUT}/data/_all_games.json')):
    away, home = g['game'].split('@'); gid = f'2026_11_{away}_{home}'; fn = g['game'].replace('@', '_at_')
    w = P[P.game_id == gid]
    res = {'game': g['game'], 'nflverse_game_id': gid, 'nflverse_rows': int(len(w)), 'pbp_source': src('pbp')}
    if not len(w): res['status'] = 'unknown: nflverse pbp has no rows for this game yet'; summary.append(res); continue
    wx = w.weather.dropna().unique(); roof = w.roof.dropna().unique()
    res['roof_nfl_feed'] = roof[0] if len(roof) else 'unknown'
    res['weather_nfl_feed'] = wx[0] if len(wx) else ('n/a: indoor (%s); NFL feed has no weather string' % res['roof_nfl_feed'] if res['roof_nfl_feed'] in ('dome', 'closed') else 'unknown (NFL feed has no weather string)')
    real = w[(w.play_type == 'pass') & (w.two_point_attempt != 1)]
    pa = real[(real.pass_attempt == 1) & (real.sack == 0)]
    ia = {}
    for t in (away, home):
        x = pa[pa.posteam == t]; inc = x[x.incomplete_pass == 1]
        ia[t] = {'pass_attempts': int(len(x)), 'air_yards_charted_on': int(x.air_yards.notna().sum()),
                 'intended_air_yards_total': float(x.air_yards.sum()) if x.air_yards.notna().any() else 'unknown',
                 'adot': round(float(x.air_yards.mean()), 2) if x.air_yards.notna().any() else 'unknown',
                 'incompletions': int(len(inc)), 'intended_air_yards_on_incompletions': float(inc.air_yards.sum()) if inc.air_yards.notna().any() else 'unknown',
                 'interceptions': int(x.interception.sum())}
        tg = x[x.receiver_player_name.notna()]; tot_air = tg.air_yards.sum(); tot_t = len(tg)
        ia[t]['receivers'] = [{'receiver': n, 'targets': int(len(y)), 'air_yards': float(y.air_yards.sum()),
                               'air_share': round(float(y.air_yards.sum() / tot_air), 3) if tot_air else 'unknown',
                               'adot': round(float(y.air_yards.mean()), 1) if y.air_yards.notna().any() else 'unknown'}
                              for n, y in sorted(tg.groupby('receiver_player_name'), key=lambda kv: (-len(kv[1]), kv[0]))]
    res['air_yards'] = ia
    # target cross-check: ESPN box (log) vs nflverse, matched through the weekly roster gsis_id
    gs2full = {r.gsis_id: r.full_name for r in R.itertuples()}
    xc = []
    for t in (away, home):
        espn = {norm(k): (k, v.get('tgt', 0)) for k, v in g['players'].get(t, {}).items() if v.get('tgt')}
        nv = collections.Counter(norm(gs2full.get(i, n)) for i, n in zip(pa[(pa.posteam == t) & pa.receiver_player_id.notna()].receiver_player_id, pa[(pa.posteam == t) & pa.receiver_player_id.notna()].receiver_player_name))
        for k in sorted(set(espn) | set(nv)):
            e = espn.get(k, (k, 0)); n = nv.get(k, 0)
            if e[1] != n: xc.append({'team': t, 'player': e[0], 'espn_box_tgt': e[1], 'nflverse_tgt': n})
    res['target_crosscheck_mismatches'] = xc
    # PBU/INT cross-check vs ESPN-text VERIFIED rows
    log = json.load(open(f'{OUT}/data/{fn}_pass_defender_log.json'))
    ver = {}
    for r in log:
        if r['evidence'].startswith('VERIFIED') and 'No Play' not in r['evidence']: ver.setdefault((r['q'], r['def']), []).append(r)
    nvp = w[w.pass_defense_1_player_name.notna() | w.interception_player_name.notna()]
    matched, only_nv = 0, []
    for _, r in nvp.iterrows():
        names = sorted({x for x in (r.pass_defense_1_player_name, r.pass_defense_2_player_name, r.interception_player_name) if isinstance(x, str)})
        cands = ver.get((int(r.qtr), r.defteam), [])
        hit = next((c for c in cands if any(n.split('.', 1)[-1] in c['defender'] for n in names)), None)
        if hit: matched += 1; cands.remove(hit)
        else: only_nv.append({'q': int(r.qtr), 'clock_nflverse': clk(r.time), 'def': r.defteam, 'nflverse_named': names, 'desc': r.desc})
    only_espn = [{'q': k[0], 'clock': c['clock'], 'def': k[1], 'defender': c['defender'], 'evidence': c['evidence'], 'text': c['text'][:160]} for k, v in ver.items() for c in v]
    res['pbu_int_crosscheck'] = {'espn_verified_pbu_int_rows': sum(1 for r in log if r['evidence'].startswith('VERIFIED-PBU/INT')), 'nflverse_plays_with_named_pbu_or_int': int(len(nvp)), 'matched': matched, 'nflverse_only': only_nv, 'espn_only': only_espn,
                                 'dpi_rows_not_in_nflverse_pd_fields': sum(1 for r in log if r['evidence'].startswith('VERIFIED-DPI'))}
    sc = S[S.game_id == gid]
    if len(sc):
        res['snap_counts'] = {t: sc[sc.team == t][['player', 'position', 'offense_snaps', 'offense_pct', 'defense_snaps', 'defense_pct', 'st_snaps', 'st_pct']].sort_values(['offense_snaps', 'defense_snaps'], ascending=False).to_dict('records') for t in (away, home)}
        res['snap_source'] = src('snap_counts') + ' (PFR-sourced)'
    else:
        res['snap_counts'] = f"unknown: not posted yet ({src('snap_counts')} has no {gid} rows; PFR boxscore page returned a Cloudflare challenge to the box and was not bypassed)"
    ft = F[F.nflverse_game_id == gid]
    if len(ft):
        j = w.merge(ft, left_on='play_id', right_on='nflverse_play_id', how='inner'); dbk = j[j.qb_dropback == 1]; ftn = {}
        for t in (away, home):
            x = dbk[dbk.posteam == t]
            def split(m):
                y = x[m]; ps = y[(y.pass_attempt == 1) & (y.sack == 0)]
                return {'dropbacks': int(len(y)), 'att': int(len(ps)), 'comp': int(ps.complete_pass.sum()), 'yds': float(y.yards_gained.sum()), 'sacks': int(y.sack.sum()), 'int': int(y.interception.sum()), 'epa_per_db': round(float(y.epa.mean()), 3) if len(y) else 'unknown'}
            ftn[t] = {'charted_dropbacks': int(len(x)), 'blitz_rate': round(float((x.n_blitzers >= 1).mean()), 3) if len(x) else 'unknown',
                      'vs_blitz': split(x.n_blitzers >= 1), 'vs_no_blitz': split(x.n_blitzers == 0), 'vs_5plus_rushers': split(x.n_pass_rushers >= 5), 'vs_4_or_fewer': split(x.n_pass_rushers <= 4),
                      'play_action': split(x.is_play_action == True), 'out_of_pocket': split(x.is_qb_out_of_pocket == True), 'drops': int(x.is_drop.sum()), 'contested_targets': int(x.is_contested_ball.sum()),
                      'man_zone_MOF': 'unknown (FTN public fields carry no coverage type or shell)'}
        res['ftn'] = ftn; res['ftn_source'] = src('ftn_charting') + '; FTN Data via nflverse (CC-BY-SA 4.0)'
    else:
        res['ftn'] = f"unknown: {src('ftn_charting')} has no {gid} rows yet"
    json.dump(res, open(f'{FILL}/{fn}.json', 'w'), indent=1, default=str); summary.append(res)
ngs = {}
for n in ('passing', 'receiving', 'rushing'):
    x = pd.read_parquet(f'{SRC}/ngs_{n}.parquet'); ngs[n] = x[(x.season == 2026) & (x.week == 11)].to_dict('records')
json.dump({'source': {k: MAN['ngs_' + k] for k in ngs}, 'rows': ngs}, open(f'{FILL}/ngs_w11_nflverse.json', 'w'), indent=1, default=str)
json.dump(MAN, open(f'{FILL}/MANIFEST.json', 'w'), indent=1)
json.dump(summary, open(f'{FILL}/_summary.json', 'w'), indent=1, default=str)
print('ok', len(summary))
