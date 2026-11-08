"""Offline evidence checks. These do not certify forecast readiness or access."""
import hashlib
import math
from datetime import datetime, timezone
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verified_copy(source, target, expected_hash=None):
    """Keep source bytes immutable and reject an existing conflicting snapshot."""
    data = Path(source).read_bytes()
    if expected_hash is not None and digest(data) != expected_hash:
        raise ValueError('source hash mismatch')
    target = Path(target)
    if target.exists() and target.read_bytes() != data:
        raise ValueError('snapshot conflict')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'sha256': digest(data), 'bytes': len(data)}


def utc(value):
    """Require an explicit offset; never substitute a local read or mtime."""
    if not isinstance(value, str):
        raise ValueError('missing timestamp')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('ambiguous timestamp')
    return parsed.astimezone(timezone.utc)


def espn_athletes(document):
    """Read only athlete containers, never nested colleges/positions/injuries."""
    result = []
    for group in document.get('athletes', []):
        for item in group.get('items', []):
            if item.get('id') is not None:
                result.append({'espn_id': str(item['id']),
                               'name': item.get('fullName') or item.get('displayName')})
    for entry in document.get('entries', []):
        if entry.get('playerId') is not None:
            result.append({'espn_id': str(entry['playerId']), 'name': None})
    return result


def join_players(observations, players):
    """Exact ESPN ID plus team only. Ambiguous IDs stay unresolved."""
    index = {}
    for player in players:
        for alias in player['aliases']:
            if alias['namespace'] == 'espn':
                index.setdefault((player['team'], str(alias['id'])), []).append(player)
    joined, unmatched = [], []
    for observation in observations:
        matches = index.get((observation['team'], observation['espn_id']), [])
        if len(matches) == 1 and matches[0].get('canonical_id'):
            joined.append({**observation, 'canonical_id': matches[0]['canonical_id'],
                           'canonical_namespace': matches[0]['canonical_namespace'],
                           'join_method': 'EXACT_ESPN_ID_AND_TEAM'})
        else:
            unmatched.append({**observation, 'canonical_id': None,
                              'reason': 'AMBIGUOUS_ID' if matches else 'ID_NOT_IN_TEAM_ROSTER'})
    return joined, unmatched


def inspect_quotes(rows, meta, cutoff, expected_week):
    """Evaluate raw saved quotes without guessing event aliases or book rules."""
    issues = set()
    if not rows:
        issues.add('EMPTY_QUOTES')
    if meta.get('season') is None:
        issues.add('SEASON_UNKNOWN')
    elif meta.get('season') != 2026:
        issues.add('SEASON_CONFLICT')
    if meta.get('data_week') is None:
        issues.add('WEEK_UNKNOWN')
    elif meta.get('data_week') != expected_week:
        issues.add('WEEK_LABEL_CONFLICT')
    try:
        if utc(meta.get('pulled_utc')) > utc(cutoff):
            issues.add('PULL_AFTER_CUTOFF')
    except ValueError:
        issues.add('PULL_TIME_UNKNOWN')
    for row in rows:
        for field in ('book', 'market', 'side', 'price', 'event_id'):
            if not row.get(field):
                issues.add('QUOTE_FIELD_MISSING:' + field)
        if not str(row.get('market', '')).startswith('h2h') and not row.get('point'):
            issues.add('LINE_MISSING')
        try:
            if not math.isfinite(float(row.get('price', ''))) or float(row['price']) == 0:
                issues.add('PRICE_INVALID')
            if row.get('point') and not math.isfinite(float(row['point'])):
                issues.add('LINE_INVALID')
        except (ValueError, TypeError):
            issues.add('NUMERIC_QUOTE_INVALID')
        if str(row.get('inplay')).lower() != 'false':
            issues.add('INPLAY_OR_UNKNOWN')
        try:
            quote, pull, start = [utc(row.get(k)) for k in
                                  ('last_update_utc', 'pulled_utc', 'commence_utc')]
            if not quote <= pull <= utc(cutoff):
                issues.add('QUOTE_PULL_ASOF_CONFLICT')
            if pull != utc(meta.get('pulled_utc')):
                issues.add('PULL_META_CONFLICT')
            if start != utc(cutoff):
                issues.add('KICKOFF_CONFLICT')
            age = (pull - quote).total_seconds() / 60
            limit = meta.get('max_quote_age_min')
            if limit is None or age > limit or age < 0:
                issues.add('FRESHNESS_UNVERIFIED_OR_STALE')
        except ValueError:
            issues.add('QUOTE_TIME_UNKNOWN')
    return {'row_count': len(rows), 'issues': sorted(issues),
            'timestamp_checks_pass': not any(x in issues for x in
                ('PULL_AFTER_CUTOFF', 'PULL_TIME_UNKNOWN', 'QUOTE_PULL_ASOF_CONFLICT',
                 'PULL_META_CONFLICT', 'QUOTE_TIME_UNKNOWN')),
            'status': 'SAVED_ONLY', 'usable_for_run': False,
            'usable_for_frozen_pregame': False,
            'canonical_event_join': 'UNVERIFIED', 'settlement_compatibility': 'UNVERIFIED',
            'actionable_status': 'NOLINE'}
