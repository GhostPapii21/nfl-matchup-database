"""STAGE 0 only. Offline pack builder; never load target-week statistics.

Run explicitly with python3 backtests/yardage_markets_wk3_8/v4/build_packs.py.
Only prints pack counts. Existing packs are refused to prevent stale-file leakage.
"""
from pathlib import Path
import json
import re
import shutil
import pandas as pd
import pyarrow.parquet as pq

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PBP = ROOT / 'runs/2026-11-02_shared_src/play_by_play_2026.parquet'
COLS = ['week', 'game_id', 'game', 'player', 'market', 'side', 'tier',
        'line', 'price', 'book', 'snap', 'kickoff', 'source', 'gsis', 'team', 'opp',
        'candidate_id']
BAD_PATH = re.compile(r'grades?|results?|postmortem|box|graded|ledger', re.I)
READ_NAME = re.compile(r'report|checklist|game[ _-]?script|pregame|pre[ _-]?game|preview', re.I)
READ_ROOTS = ('runs', 'week8', 'week9', 'docs', 'cards', 'slips', 'outlier')
RAW_ROOTS = ('backtests/rulebook_replay_wk6_8/raw', 'backtests/current_rules_wk6_8/raw')
ODDS_COLS = ['game_id', 'game', 'kickoff', 'market', 'book', 'timestamp',
             'name', 'point', 'price', 'source']
WEATHER_COLS = ['game_id', 'game', 'kickoff', 'issued', 'valid_time', 'temp', 'wind', 'source']


def utc(value, naive='UTC'):
    try:
        t = pd.Timestamp(value)
        if pd.isna(t):
            return None
        return t.tz_localize(naive).tz_convert('UTC') if t.tzinfo is None else t.tz_convert('UTC')
    except (ValueError, TypeError):
        return None


def json_file(path):
    try:
        return json.loads(path.read_text())
    except (ValueError, UnicodeError, OSError):
        return None


def safe_files(roots, pattern):
    return sorted({p for root in roots for p in (ROOT / root).rglob(pattern)
                   if p.is_file() and not p.is_symlink()
                   and not BAD_PATH.search(str(p.relative_to(ROOT)))})


def prior(path, week, game_ids=None):
    """Push down temporal filters; never materialize target-week rows."""
    names = pq.read_schema(path).names
    if 'week' not in names:
        raise ValueError(f'{path.name}: no week field; cannot safely filter')
    filters = [('week', '<', week)]
    if 'season' in names:
        filters.append(('season', '==', 2026))
    for key in ('season_type', 'game_type'):
        if key in names:
            filters.append((key, '==', 'REG'))
    frame = pd.read_parquet(path, filters=filters)
    if game_ids is not None:
        key = next((c for c in ('game_id', 'nflverse_game_id') if c in names), None)
        if key is None:
            raise ValueError(f'{path.name}: no game identity for REG verification')
        frame = frame[frame[key].isin(game_ids)]
    assert frame.empty or (frame.week < week).all()
    return frame


def event_rows(document):
    if not isinstance(document, dict):
        return []
    data = document.get('data', document)
    return [e for e in (data if isinstance(data, list) else [data])
            if isinstance(e, dict) and 'commence_time' in e]


def saved_reads(pack, games, cutoff):
    rows = []
    for path in safe_files(READ_ROOTS, '*'):
        if path.suffix.lower() not in ('.md', '.txt', '.html') or not READ_NAME.search(path.name):
            continue
        # Later mtime cannot prove the present contents existed before cutoff.
        mtime = pd.Timestamp(path.stat().st_mtime, unit='s', tz='UTC')
        try:
            text = path.read_text()
        except (UnicodeError, OSError):
            continue
        # Accept explicit document-level timestamps, never dates quoted in prose.
        declared = []
        for match in re.finditer(
                r'(?im)^\s*(?:[-*]\s*)?(?:as.of|generated(?:_at)?|created(?:_at)?|'
                r'updated(?:_at)?|timestamp|pulled_et|_pulled_et)\s*[:=]\s*'
                r'["\x27]?([^\n"\x27]+)', text):
            t = utc(match.group(1).strip(), 'America/New_York')
            if t is not None:
                declared.append(t)
        # A later declared update disqualifies even a backdated filesystem mtime.
        if any(t >= cutoff for t in declared):
            continue
        if declared:
            timestamp, source = max(declared), 'content: document timestamp (America/New_York if naive)'
        else:
            timestamp, source = mtime, 'filesystem mtime'
        if timestamp >= cutoff:
            continue
        searchable = str(path.relative_to(ROOT)) + '\n' + text
        matches = []
        for g in games.itertuples():
            away, home = g.game.split('@')
            variants = [g.game_id, g.game, f'{away} @ {home}', f'{away} vs {home}',
                        f'{away} at {home}']
            if any(re.search(re.escape(v), searchable, re.I) for v in variants):
                matches.append(g.game)
        if not matches:
            continue
        # Do not copy documents containing explicit grading or retrospective sections.
        if re.search(r'(?im)^#{1,6}\s+.*(?:postmortem|results?|grades?|box score|recap)', text):
            continue
        relative = path.relative_to(ROOT)
        dest = pack / 'saved_reads' / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        rows.append(dict(path=str(Path('saved_reads') / relative), source_path=str(relative),
                         timestamp=timestamp.isoformat(), timestamp_source=source,
                         games=';'.join(matches)))
    pd.DataFrame(rows, columns=['path', 'source_path', 'timestamp', 'timestamp_source', 'games']).to_csv(
        pack / 'saved_reads/INDEX.csv', index=False)
    return len(rows)


def build():
    if (OUT / 'packs').exists():
        raise FileExistsError('v4/packs already exists; refusing to mix old and new packs')
    # CSV usecols prevents loading any result, feature, or hindsight fields.
    legs = pd.read_csv(OUT.parent / 'v2/legs.csv', usecols=COLS)
    legs = legs[legs.week.between(3, 8) & legs.tier.eq('main') &
                legs.market.isin(['rushyds', 'recyds', 'rushrecyds', 'receptions'])].copy()
    legs.kickoff = legs.kickoff.map(utc)
    if legs.kickoff.isna().any():
        raise ValueError('Missing kickoff in v2 identity data')
    ab = json_file(ROOT / 'backtests/rulebook_replay_wk6_8/abbr.json')
    if not isinstance(ab, dict):
        raise ValueError('Missing team abbreviation map')
    ab.update({'LAR': 'LA', 'WSH': 'WAS'})
    schedule = legs[['week', 'game_id', 'game', 'kickoff']].drop_duplicates()
    if schedule.duplicated(['game_id']).any():
        raise ValueError('Conflicting saved kickoff identity')
    # Schedule completeness verified using identity fields only, never current-week stats.
    identity = pd.read_parquet(PBP, columns=['week', 'game_id', 'season_type'],
                               filters=[('week', '>=', 3), ('week', '<=', 8), ('season_type', '==', 'REG')])
    missing = set(identity.game_id) - set(schedule.game_id)
    if missing:
        raise ValueError('v2 schedule missing game identities: ' + ', '.join(sorted(missing)))
    lookup = {(r.game, r.kickoff): r for r in schedule.itertuples()}
    quotes, odds, weather = [], [], []
    roots = (*READ_ROOTS, *RAW_ROOTS, 'backtests/yardage_markets_wk3_8/raw')
    raw_paths = set(safe_files(RAW_ROOTS, '*.json'))
    for path in safe_files(roots, '*.json'):
        doc = json_file(path)
        if not isinstance(doc, dict):
            continue
        source = str(path.relative_to(ROOT))
        for e in event_rows(doc):
            ko = utc(e['commence_time'])
            game = f"{ab.get(e.get('away_team'), e.get('away_team'))}@{ab.get(e.get('home_team'), e.get('home_team'))}"
            g = lookup.get((game, ko))
            if g is None:
                continue
            for book in e.get('bookmakers', []):
                for market in book.get('markets', []):
                    key = market.get('key')
                    if key not in ('spreads', 'totals', 'player_receptions'):
                        continue
                    stamp = utc(doc.get('timestamp') or doc.get('snapshot_time') or
                                market.get('last_update') or book.get('last_update'))
                    updates = [utc(x) for x in (market.get('last_update'), book.get('last_update')) if x]
                    if stamp is None or stamp > ko or any(t is None or t > ko for t in updates):
                        continue
                    for o in market.get('outcomes', []):  # bookmaker quote outcomes, not game results
                        if o.get('point') is None:
                            continue
                        if key == 'player_receptions' and path in raw_paths:
                            if o.get('name', '').lower() not in ('over', 'under') or not o.get('price') or not o.get('description'):
                                continue
                            quotes.append(dict(week=g.week, game_id=g.game_id, game=game,
                                player=o['description'], market='receptions', side=o['name'].lower(),
                                tier='main', line=o['point'], price=o['price'], book=book['key'],
                                snap=stamp.isoformat(), kickoff=ko, source=source))
                        elif key in ('spreads', 'totals'):
                            odds.append(dict(game_id=g.game_id, game=game, kickoff=ko,
                                market=key, book=book['key'], timestamp=stamp, name=ab.get(o.get('name'), o.get('name')),
                                point=o['point'], price=o.get('price'), source=source))
        if 'weather' not in source.lower() and 'forecast' not in source.lower():
            continue
        issued = utc(doc.get('pulled_et') or doc.get('_pulled_et'), 'America/New_York')
        if issued is None:
            continue
        for home, value in doc.items():
            if not isinstance(value, dict) or value.get('roof') != 'open':
                continue
            for forecast in value.get('om', []):
                valid = utc(forecast.get('t'))
                if valid is None:
                    continue
                for g in schedule.itertuples():
                    if (g.game.split('@')[1] == ab.get(home, home) and issued <= g.kickoff
                            and abs((valid - g.kickoff).total_seconds()) <= 3600):
                        weather.append(dict(game_id=g.game_id, game=g.game, kickoff=g.kickoff,
                            issued=issued, valid_time=valid, temp=forecast.get('temp'),
                            wind=forecast.get('wind'), source=source))
    receptions = pd.DataFrame(quotes)
    if not receptions.empty:
        receptions = receptions.sort_values(['snap', 'source']).drop_duplicates(
            ['game_id', 'player', 'market', 'side', 'book'], keep='last')
    odds = pd.DataFrame(odds, columns=ODDS_COLS)
    weather = pd.DataFrame(weather, columns=WEATHER_COLS)
    for week in range(3, 9):
        pack = OUT / 'packs' / f'w{week}'
        (pack / 'saved_reads').mkdir(parents=True)
        notes = []
        games = schedule[schedule.week.eq(week)]
        cutoff = games.kickoff.min()
        history = prior(PBP, week)
        history.to_parquet(pack / 'pbp_prior.parquet', index=False)
        snap = Path('/tmp/snap_counts_2026.parquet')
        if not snap.is_file():
            raise FileNotFoundError('Required /tmp/snap_counts_2026.parquet missing')
        snaps = prior(snap, week, set(history.game_id))
        snaps.to_parquet(pack / 'snap_counts_prior.parquet', index=False)
        ftn_frames = []
        for path in sorted(Path('/tmp').glob('*ftn*.parquet')):
            ftn_frames.append(prior(path, week, set(history.game_id)))
        if ftn_frames:
            ftn = pd.concat(ftn_frames, ignore_index=True).drop_duplicates()
            ftn.to_parquet(pack / 'ftn_prior.parquet', index=False)
            if not any(re.search('mofo|mofc|coverage|shell', c, re.I) for c in ftn.columns):
                notes.append('Saved FTN lacks MOFO/MOFC coverage fields; no coverage inferred.')
        else:
            notes.append('No saved /tmp/*ftn*.parquet charting available.')
        props = legs[legs.week.eq(week)].copy()
        if not receptions.empty:
            props = pd.concat([props, receptions[receptions.week.eq(week)]], ignore_index=True)
        props.reindex(columns=COLS).drop_duplicates().to_csv(pack / 'props_main.csv', index=False)
        gl = odds[odds.game_id.isin(games.game_id)].sort_values(['timestamp', 'source']).drop_duplicates(
            ['game_id', 'book', 'market', 'name'], keep='last')
        gl.to_csv(pack / 'game_lines.csv', index=False)
        wx = weather[weather.game_id.isin(games.game_id)].drop_duplicates()
        wx.to_csv(pack / 'weather.csv', index=False)
        covered = set(gl.groupby('game_id').market.agg(set).loc[lambda x: x.map(lambda v: {'spreads', 'totals'} <= v)].index)
        no_lines = sorted(set(games.game_id) - covered)
        no_weather = sorted(set(games.game_id) - set(wx.game_id))
        notes.append('Missing saved pre-kick spread/total games: ' + (', '.join(no_lines) or 'none'))
        notes.append('Missing eligible saved weather games: ' + (', '.join(no_weather) or 'none'))
        count = saved_reads(pack, games, cutoff)
        files = sorted(str(p.relative_to(pack)) for p in pack.rglob('*') if p.is_file())
        files.append('MANIFEST.md')
        manifest = [f'# Week {week} pack', f'First kickoff cutoff: {cutoff.isoformat()}',
            f'All statistics: 2026 REG weeks < {week}. No target-week statistics loaded.',
            'Props: v2 identity/quote allowlist plus saved main receptions quotes; no passing yards or TDs.',
            'Game lines: latest eligible quote per book/market/outcome (v3 approach); no fabricated consensus.',
            'Weather: saved Open-Meteo open-roof forecasts, issuance <= kickoff, valid hour within one hour.',
            'Saved reads: explicit document timestamp or filesystem mtime before first kickoff; '
            'timestamps are local provenance, not independently audited. Postmortems excluded entirely.',
            'Historical source revisions can introduce revision bias.', *notes, '', 'Files:',
            *[f'- {name}' for name in sorted(files)]]
        (pack / 'MANIFEST.md').write_text('\n\n'.join(manifest) + '\n')
        print(f'w{week}: {len(files)} files; {len(history)} prior plays; {len(snaps)} prior snaps; '
              f'{len(props)} props; {len(gl)} game lines; {len(wx)} forecasts; {count} saved reads')


if __name__ == '__main__':
    build()
