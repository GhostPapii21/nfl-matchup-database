# Blitz README.md (full text)

**Delivered:** 2026-11-08 ~06:45 ET

```markdown
# NFL 2026 historical odds export v2 (built 2026-11-07 19:14 ET). Evidence only
Local files only. No API calls, browser, or repo changes. Secret scan of copied raw files: 0 hits.

## Count reconciliation
- 145,909 = rows matching the 2026 schedule, including 420 Week 10 rows. Requested scope W1-9 = 145,489.
- My earlier "2,338 post-kick" figure was an arithmetic error. The old metric was 1,918.

## Timing rules (pregame)
- quote_update_before_kick = market (else book) last_update < kickoff. Kept as a field only; it is NOT proof the quote was observed pregame.
- observation_pregame_status uses the historical wrapper timestamp (snapshot): PREGAME_SNAPSHOT if snapshot < kickoff; SNAPSHOT_AT_OR_AFTER_KICK excluded from strict; UNKNOWN_NO_SNAPSHOT for live-list files without a snapshot/retrieval time.

## Files
- SCOPED_2026_W1_9_ALL.csv (145489)
- SCOPED_2026_W1_9_STRICT_PREGAME.csv (100996)
- SCOPED_2026_W1_9_UNKNOWN_OR_POSTKICK.csv (44493)
- LEGACY_ALL_ROWS_FLAGGED.csv (181362)
- COVERAGE_BY_WEEK_BOOK_MARKET_PERIOD.csv
- NFLDATA_CONSENSUS_LINES_W1_9.csv (136 games, bookless, timing UNKNOWN)
- supplemental_raw/ + SUPPLEMENTAL_RAW_MANIFEST.csv
- OTHER_SOURCES_NOT_NORMALIZED.csv
- SOURCE_FILE_MANIFEST.csv, raw_oddsapi/ (760 unique raw Odds API JSON), MANIFEST.json, build.py

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

Gaps: no named-book quotes for Weeks 1-2. Quarter/half quotes effectively absent. Week 6 has 40k rows with no snapshot. Only opening/close series is JAX@BAL (supplemental, unnormalized).
```
