"""Offline Stage B reference: all holdout consensus legs, no selection rules."""
import hashlib
import json
from pathlib import Path
import pandas as pd
from build import ROOT, profit, summary

HERE = Path(__file__).resolve().parent


def verify_frozen():
    expected = json.loads((HERE / 'frozen_sha256.json').read_text())
    for name, digest in expected.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
    return expected


def main():
    expected = verify_frozen()
    x = pd.read_csv(HERE / 'legs.csv')
    x = x[x.week.isin([7, 8])].copy().reset_index(drop=True)
    p = pd.read_parquet(ROOT / 'runs/2026-11-02_shared_src/play_by_play_2026.parquet')
    p = p[(p.season_type == 'REG') & (p.two_point_attempt != 1)]
    ru = p[(p.rush_attempt == 1) & p.rusher_player_id.notna()].groupby(['game_id', 'rusher_player_id']).rushing_yards.sum()
    re = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()].groupby(['game_id', 'receiver_player_id']).receiving_yards.sum()
    outcomes = []
    for r in x.itertuples():
        actual = (float(ru.get((r.game_id, r.gsis), 0)) * (r.market != 'recyds') + float(re.get((r.game_id, r.gsis), 0)) * (r.market != 'rushyds')) if pd.notna(r.gsis) and pd.notna(r.team) else float('nan')
        result = 'ungraded' if pd.isna(actual) or pd.isna(r.price) else 'push' if actual == r.line else 'win' if ((actual > r.line) == (r.side == 'over')) else 'loss'
        outcomes.append((actual, result, profit(r.price) if result == 'win' else -10 if result == 'loss' else 0, 0 if result == 'ungraded' else 10))
    x[['result_stat', 'result', 'pl', 'stake']] = pd.DataFrame(outcomes, index=x.index)
    x.to_csv(HERE / 'all_legs_holdout.csv', index=False)
    reports = []
    for keys in [['market', 'side'], ['week', 'market', 'side']]:
        a = summary(x, keys)
        a.to_csv(HERE / ('all_legs_holdout_' + '_'.join(keys) + '.csv'), index=False)
        reports.extend(['All holdout legs: ' + ', '.join(keys), a.to_string(index=False)])
    reference = '\n\n'.join([
        '## All-legs holdout reference (no rules)',
        'Weeks 7–8; every consensus leg from frozen legs.csv. No rule, edgecap, Sharp, or one-per-player filter. Opposing sides and multiple markets for a player remain included; this is a descriptive reference, not an independent-bet portfolio. Settlement matches grade.py: $10 per graded leg, pushes return stake, ungraded legs have zero stake; hit% excludes pushes/ungraded, ROI uses graded stake. Missing player/team or price remains ungraded. Matched players with no recorded yards settle at zero; participation voids cannot be reconstructed.',
        *reports,
    ]) + '\n'
    (HERE / 'all_legs_holdout_results.md').write_text(reference)
    results = HERE / 'results.md'
    base = results.read_text().split('\n## All-legs holdout reference (no rules)')[0].rstrip()
    results.write_text(base + '\n\n' + reference)
    assert expected == verify_frozen()
    (HERE / 'stage_b_frozen_verification.json').write_text(json.dumps({'all_match': True, 'sha256': expected}, indent=2) + '\n')
    print(reference)


if __name__ == '__main__':
    main()
