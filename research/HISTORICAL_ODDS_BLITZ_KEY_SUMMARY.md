# Blitz KEY_CSV_SUMMARY.md (full text)

**Delivered:** 2026-11-08 ~06:45 ET

```markdown
# Key CSV summary (extracted from NFL_HISTORICAL_ODDS_2026_W1_9_v2.zip, sha256 690499ae...ddb9)
Byte-exact extracts; no field transformations. Previews are the first 50 data rows + header, in archive order (PREVIEW ONLY).

| file | rows | bytes | note |
|---|---|---|---|
| SCOPED_2026_W1_9_STRICT_PREGAME.csv.gz | 100996 | 1044754 | full strict file, gzip -9; decompressed sha256 matches archive: True (58433581 bytes uncompressed) |
| STRICT_PREGAME_FIRST50.csv | 50 | 29432 | preview |
| NFLDATA_CONSENSUS_LINES_W1_9.csv | 136 | 42106 | full; bookless consensus, timing UNKNOWN |
| COVERAGE_BY_WEEK_BOOK_MARKET_PERIOD.csv | 619 | 39074 | full (scoped W1-9, includes all observation statuses) |
| COVERAGE_FIRST50.csv | 50 | 3420 | preview |
| README.md | - | 3918 | exact copy, with coverage/timing notes |

## Headers
- Strict: provider, event_id, home_team, away_team, commence_time_utc, book, book_title, market, period, outcome, player, line, price, price_format, snapshot_ts_utc, book_last_update_utc, market_last_update_utc, raw_sha256, source_path, home, away, kick_date_et, game_id, week, gameday, gametime, season_status, quote_time_basis, record_class, dup_n, quote_update_before_kick, observation_pregame_status, scope
- Consensus: game_id, week, gameday, gametime, away_team, home_team, away_moneyline, home_moneyline, spread_line, away_spread_odds, home_spread_odds, total_line, under_odds, over_odds, record_class, source
- Coverage: week, book, period, market, observation_pregame_status, quotes, events

## Strict pregame by week (snapshot < kickoff)
|   week |   quotes |   events |   books |
|-------:|---------:|---------:|--------:|
|      3 |     4602 |       16 |       7 |
|      4 |     4436 |       16 |       7 |
|      5 |     3994 |       15 |       7 |
|      6 |    31585 |       14 |      11 |
|      7 |    35130 |       14 |      11 |
|      8 |    18919 |       14 |      11 |
|      9 |     2330 |       15 |      11 |
Periods: {'FULL_GAME': 100996}. No named-book quotes for W1-2. Quarter/half quotes are effectively absent.

## Timing caveats
Strict = historical snapshot timestamp before kickoff. Excluded and not extracted here: 44,493 scoped rows (UNKNOWN_NO_SNAPSHOT 42,583; SNAPSHOT_AT_OR_AFTER_KICK 1,910). `quote_update_before_kick` is a field only, not proof. Consensus lines have no book or time.
```
