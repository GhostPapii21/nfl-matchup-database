# W12 Thanksgiving pristine lock — status

- Checked: `2026-11-26T17:26:33+00:00` (12:26 PM EST)
- Branch: `cursor/w12-thanksgiving-locks-9aff`
- CHI@DET: still PRE at last check; **NO_LOCK** (protocol)
- Worker [Week 12 pristine holdout eval](bc-621b3725-f09e-5863-b942-60ca89b823b6) produced 15 `snapshots.lock` artifacts on `cursor/w12-pristine-holdout-23b6` — **non-qualifying** (see `NON_QUALIFYING_PARALLEL_LOCKS.md`). `sim100k` still REFUSED.

## Live refusals (~17:20Z)

- FTN/PFR GAP for `2026_12_GB_LA`
- CHI official inactives MISSING (DET OK)
- Odds/four_book STALE inside T-2h — refreshed again (`freeze_20261126T172633Z.json`, pulled `17:21:44Z`)

## Protocol correction

Parallel branch artifacts are research/`NOT_FINAL` only. Do not merge as holdout completion.
Scored remains **14** (weeks 10–11) until finals + SCORE under the frozen protocol after a
**sim100k-gated** lock.

## Holdout

- Scored: **14** (W10–11)
- Qualifying W12 LOCKs on this branch: **0**
- `projection_ready`: **false**
