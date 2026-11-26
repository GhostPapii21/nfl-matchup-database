# NFL 2026 historical odds export v2 (built 2026-11-07 19:14 ET). Evidence only
Local files only. No API calls, browser, or repo changes. Secret scan of copied raw files: 0 hits.

## Count reconciliation
- 145,909 = rows matching the 2026 schedule, including 420 Week 10 rows (['2026_10_WAS_NYG', '2026_10_NE_DET', '2026_10_KC_ATL', '2026_10_BUF_NYJ', '2026_10_CAR_NO', '2026_10_HOU_CLE', '2026_10_MIN_GB', '2026_10_MIA_IND', '2026_10_JAX_TEN', '2026_10_LA_ARI', '2026_10_SF_DAL', '2026_10_PIT_CIN', '2026_10_LAC_BAL', '2026_10_SEA_LV']). Requested scope W1-9 = 145,489.
- My earlier "2,338 post-kick" figure was an arithmetic error (145,909 - 143,571). The old metric, quote update at/after kick within W1-9, was 1,918. That metric is replaced below.

## Timing rules (pregame)
- quote_update_before_kick = market (else book) last_update < kickoff. Kept as a field only; it is NOT proof the quote was observed pregame (stale quotes possible).
- observation_pregame_status uses the historical wrapper `timestamp` (snapshot): PREGAME_SNAPSHOT if snapshot < kickoff; SNAPSHOT_AT_OR_AFTER_KICK is excluded from strict even with old updates; UNKNOWN_NO_SNAPSHOT for live-list files without a snapshot/retrieval time (never certified).

## Files
- SCOPED_2026_W1_9_ALL.csv (145489): W1-8 142285, W9 3204.
- SCOPED_2026_W1_9_STRICT_PREGAME.csv (100996).
- SCOPED_2026_W1_9_UNKNOWN_OR_POSTKICK.csv (44493).
- LEGACY_ALL_ROWS_FLAGGED.csv (181362): all deduped rows. scope = 2026_W1_8 / 2026_W9 / 2026_W10PLUS_OUTSIDE / NON_2026_OUTSIDE (2024-25 prop samples).
- COVERAGE_BY_WEEK_BOOK_MARKET_PERIOD.csv (scoped, split by observation status).
- NFLDATA_CONSENSUS_LINES_W1_9.csv (136 games): bookless consensus; no book, no snapshot time; timing UNKNOWN.
- supplemental_raw/ + SUPPLEMENTAL_RAW_MANIFEST.csv (45 files): genuine quote files, not normalized. JAX@BAL open/T120/T60/T30/close CSV + meta (meta labels data_week 10, but the nflverse schedule has 2026_09_JAX_BAL = Week 9, Thu 2026-11-05; trust the schedule), the Nov 5 JAX@BAL run odds, FanDuel-native prop JSON (nfl-sim/live, balatl), CHI@SEA odds_m0505.csv/lines_m0505.json, fd_oct18_lines.txt.
- OTHER_SOURCES_NOT_NORMALIZED.csv: every candidate path, with included flag and exclusion reason. Excluded: model-mixed files (week6_props with projections/sims, lines_snapshot with projection, live_lines with live/pre_med), backtest derivatives (no-vig, devig, graded, real_lines with nv_over), quota logs.
- SOURCE_FILE_MANIFEST.csv, raw_oddsapi/ (760 unique raw Odds API JSON), MANIFEST.json, build.py.

## Format assumptions
Odds API v4 JSON. Prices are American when |price| >= 100 or an integer. Period comes from the market key suffix (_q1.._h1). Dedup key: event_id, book, market, outcome, player, line, price, market_last_update, book_last_update (earliest snapshot kept).

## Coverage (scoped, by observation status)
|   week |   PREGAME_SNAPSHOT |   SNAPSHOT_AT_OR_AFTER_KICK |   UNKNOWN_NO_SNAPSHOT |
|-------:|-------------------:|----------------------------:|----------------------:|
|      3 |               4602 |                           0 |                     0 |
|      4 |               4436 |                           0 |                     0 |
|      5 |               3994 |                           0 |                     0 |
|      6 |              31585 |                         644 |                 40151 |
|      7 |              35130 |                         608 |                   730 |
|      8 |              18919 |                         658 |                   828 |
|      9 |               2330 |                           0 |                   874 |

Gaps: no named-book quotes for Weeks 1-2. Quarter/half quotes are about 280 in total, in a few events, so effectively absent. Week 6 has 40k rows with no snapshot (live-list files), timing UNKNOWN. The only opening/close series is JAX@BAL (supplemental, unnormalized).
