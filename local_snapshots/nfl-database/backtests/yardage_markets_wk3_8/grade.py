"""Offline post-lock grading. Run with python3 grade.py; never fits rules."""
import hashlib
import json
from pathlib import Path

import pandas as pd
import rules

HERE = Path(__file__).resolve().parent
FROZEN = ('rules.py', 'locked_rules.json', 'slip_method.md')


def decimal(price):
    return 1 + (price / 100 if price > 0 else 100 / -price)


def settle(outcomes, odds):
    # An ungraded leg leaves the entire slip pending, as specified in slip_method.md.
    if 'ungraded' in outcomes:
        return 'ungraded', 0.0, 0.0
    if 'loss' in outcomes:
        return 'loss', -10.0, 10.0
    payout = 1.0
    for outcome, odd in zip(outcomes, odds):
        if outcome == 'win':
            payout *= odd
    return ('push' if all(o == 'push' for o in outcomes) else 'win'), 10 * (payout - 1), 10.0


def eligible(x, locked, sharp):
    mask = pd.Series(False, index=x.index)
    for r in locked:
        mask |= ((x.market == r['market']) & (x.side == r['side']) &
                 (x.tier == r['tier']) & (x.form_edge >= r['min_form_edge']))
    if sharp:
        mask &= (((x.side == 'over') & (x.HINDSIGHT_sharp_man >= 30)) |
                 ((x.side == 'under') & (x.HINDSIGHT_sharp_man < 30)))
    return x.loc[mask].copy()


def summary(z):
    wins = int((z.result == 'win').sum())
    losses = int((z.result == 'loss').sum())
    pushes = int((z.result == 'push').sum())
    pending = int((z.result == 'ungraded').sum())
    stake = z.stake.sum()
    hit = f'{100*wins/(wins+losses):.2f}%' if wins+losses else '—'
    roi = f'{100*z.pl.sum()/stake:.2f}%' if stake else '—'
    return f'{len(z)} | {wins} | {losses} | {pushes} | {pending} | {hit} | ${z.pl.sum():.2f} | {roi}'


def main():
    hashes = {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in FROZEN}
    locked = json.loads((HERE/'locked_rules.json').read_text())
    x = pd.read_csv(HERE/'candidates.csv')
    assert x.candidate_id.is_unique
    assert set(x.result) <= {'win', 'loss', 'push', 'ungraded'}
    assert (x.price.ne(0) & x.price.notna()).all()
    # Recompute settlement from stats and prices, rather than trusting cached P/L.
    actual = pd.Series('ungraded', index=x.index)
    graded = x.result_stat.notna()
    actual.loc[graded] = 'loss'
    actual.loc[graded & ((x.result_stat > x.line) & (x.side == 'over') |
                       (x.result_stat < x.line) & (x.side == 'under'))] = 'win'
    actual.loc[graded & (x.result_stat == x.line)] = 'push'
    assert actual.equals(x.result)
    payouts = [settle([r.result], [decimal(r.price)]) for r in x.itertuples()]
    x['pl'] = [r[1] for r in payouts]
    x['stake'] = [r[2] for r in payouts]
    singles, parlays = [], []
    for sharp in (False, True):
        q = eligible(x, locked, sharp)
        best = q.sort_values(['price', 'candidate_id'], ascending=[False, True]).drop_duplicates(['player', 'side', 'week'])
        pools = {'qualifying_quotes': q, 'frozen_selected': rules.passing(x, sharp),
                 'dedup_best_price': best}
        for view, pool in pools.items():
            pool = pool.copy()
            pool['view'] = view
            pool['sharp'] = 'ON' if sharp else 'OFF'
            pool['split'] = pool.week.map(lambda w: 'train' if w <= 6 else 'holdout')
            singles.append(pool)
            if view == 'qualifying_quotes':
                continue
            # Retain frozen player cap, ordering and game cap on the sensitivity pool too.
            chosen = rules.passing(pool, sharp)
            for week, number, legs in rules.slips(chosen):
                assert 3 <= len(legs) <= 4
                assert len({r['player'] for r in legs}) == len(legs)
                assert max(pd.Series([r['game_id'] for r in legs]).value_counts()) <= 2
                outcomes = [r['result'] for r in legs]
                odds = [decimal(r['price']) for r in legs]
                result, pl, stake = settle(outcomes, odds)
                parlays.append(dict(view=view, sharp='ON' if sharp else 'OFF',
                    split='train' if week <= 6 else 'holdout', week=week,
                    slip_id=f'{view}_{"on" if sharp else "off"}_w{week}_{number}',
                    legs=len(legs), candidate_ids=json.dumps([r['candidate_id'] for r in legs]),
                    players=json.dumps([r['player'] for r in legs]),
                    game_ids=json.dumps([r['game_id'] for r in legs]),
                    leg_results=json.dumps(outcomes), decimal_odds=__import__('math').prod(odds),
                    result=result, pl=pl, stake=stake))
    s = pd.concat(singles, ignore_index=True)
    p = pd.DataFrame(parlays, columns=['view','sharp','split','week','slip_id','legs',
        'candidate_ids','players','game_ids','leg_results','decimal_odds','result','pl','stake'])
    for (_, _, week), z in p.groupby(['view', 'sharp', 'week']):
        players = [player for v in z.players for player in json.loads(v)]
        assert len(players) == len(set(players))
    s.to_csv(HERE/'selected_singles.csv', index=False)
    p.to_csv(HERE/'selected_slips.csv', index=False)
    lines = ['# Frozen yardage results', '',
        'Rules lock: `593ec21` (user supplied). Train: week 6 only; holdout: weeks 7–8. Weeks 3–5 and rush+receiving have no admissible quotes. No rules were retuned.', '',
        'Views: `qualifying_quotes` includes every quote passing the locked cell and Sharp filter, before the player cap; these quotes are correlated. `frozen_selected` applies rules.passing unchanged (one player/week, form edge then price then candidate ID). `dedup_best_price` keeps one qualifying quote per player-side-week, highest American price then candidate ID, across lines/markets/books. This requested sensitivity can change the chosen line/market and is not line-matched price shopping. Its slips then apply the frozen player/order/game caps unchanged.', '',
        'Sharp ON uses the Oct27 HINDSIGHT man filter; missing values abstain. It is not point-in-time evidence. Sharp OFF ignores Sharp. $10 per settled single/slip; pending stakes excluded from ROI. Hit% = wins/(wins+losses), excluding pushes/pending. n includes pending; won counts profitable slips. Push legs contribute decimal 1, all pushes refund; any ungraded leg leaves the slip pending. Slip payouts multiply quoted odds and are illustrative: correlation/SGP repricing, limits and participation void rules are unavailable. Singles and slips are separate portfolios.', '']
    periods = [('week 6', 'week', 6), ('week 7', 'week', 7), ('week 8', 'week', 8),
               ('train', 'split', 'train'), ('holdout', 'split', 'holdout')]
    for view in ('qualifying_quotes', 'frozen_selected', 'dedup_best_price'):
        lines += [f'## Singles: {view}', '', '| Sharp | Period | Rule cell | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |',
                  '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for sharp in ('OFF', 'ON'):
            for label, key, value in periods:
                z = s[(s.view == view) & (s.sharp == sharp) & (s[key] == value)]
                for r in locked:
                    cell = z[(z.market == r['market']) & (z.side == r['side']) & (z.tier == r['tier'])]
                    name = f'{r["market"]}/{r["side"]}/{r["tier"]}/edge≥{r["min_form_edge"]}'
                    lines.append(f'| {sharp} | {label} | {name} | {summary(cell)} |')
                lines.append(f'| {sharp} | {label} | ALL | {summary(z)} |')
        lines.append('')
    for view in ('frozen_selected', 'dedup_best_price'):
        lines += [f'## Slips: {view}', '', '| Sharp | Period | n | Won | Lost | Push | Pending | Hit% | $10 P/L | ROI |',
                  '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for sharp in ('OFF', 'ON'):
            for label, key, value in periods:
                z = p[(p.view == view) & (p.sharp == sharp) & (p[key] == value)]
                lines.append(f'| {sharp} | {label} | {summary(z)} |')
        lines.append('')
    lines += ['## Frozen input SHA-256', ''] + [f'- `{f}`: `{v}`' for f, v in hashes.items()]
    assert hashes == {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in FROZEN}
    report = '\n'.join(lines) + '\n'
    (HERE/'results.md').write_text(report)
    print(report, end='')


if __name__ == '__main__':
    main()
