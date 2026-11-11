# Fix W1–8 period ledger (research workspace only)

Path: `/workspace/research/nfl_period_w1_8_2026/`
Do NOT touch CORE / market / nfl-database production.

## Bugs to fix
1. `reconstruct()` returns `NONMONOTONIC_SCORE_OR_QUARTER` for 83/121 games because administrative plays (esp. Timeouts) carry **stale lower** `total_home_score`/`total_away_score` mid-quarter. Example: ATL_PIT play 3537 Timeout shows 13–10 after prior 19–10.
2. Market grades mark `GRADED` whenever nflverse `spread_line`/`total_line` exist. Rico rule: grade **ONLY** with exact historic quote/book/time; otherwise **NOLINE**. Current `quote_verified_closer=False` and limitation text already admit unverified — so set grades to **NOLINE** always for this dataset (do not treat schedule lines as closers). Keep quote fields for transparency but `market_spread_grade=NOLINE`, `market_total_grade=NOLINE`, clear cover/over results, set `market_missing_reason` like `NO_VERIFIED_CLOSER_QUOTE`.

## Required fix for (1)
When walking plays sorted by play_id:
- Skip score/quarter updates that would regress (keep last good cumulative), OR skip plays whose desc is Timeout / similar admin without advancing score, OR forward-fill monotonic cumulative max.
- Still require usable Q1–Q4 endpoints via quarter_end markers or END OF QUARTER/HALF/GAME desc.
- Do not invent scores; if true scoring non-monotonicity remains after skipping admin stale rows, keep MISSING with reason.
- Add unit tests covering timeout stale-score regression → still recovers quarters.
- Preserve OT/tie logic.

## Rebuild
Offline snapshots already exist under `data/raw/` with FETCHED manifest (parent-seeded). Run:
`python3 scripts/build_ledger.py --offline --as-of 2026-11-06T14:00:00+00:00`
Update COUNTS.md / VALIDATION.md / tests. Target: ~121 games with PRESENT scoreboards (or document residual MISSING with exact reasons), all 32 teams, market grades all NOLINE, PFF still NOT_ATTEMPTED/MISSING.

Return brief summary of before/after counts.
