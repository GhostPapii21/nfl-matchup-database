# Ghost6 Historical Odds — Header, Counts, and Coverage Notes

**Delivered:** 2026-11-07
**Source package:** historical_nfl_odds_2026_weeks1_9.zip

## Row Counts
- `sportsbook_latest_verified_pregame.csv`: **104,742** data rows
- `week9_verified_pregame.csv`: **9,120** data rows

## Exact Header (both files)
```csv
observation_id,season,week,game_id,event_id,game_date_et,away_team,home_team,bookmaker,platform_type,market,period,player,selection,line,price,odds_format,snapshot_timestamp,book_update_timestamp,market_update_timestamp,event_start_timestamp,snapshot_et,event_start_et,pregame_status,flags,upstream_source,source_filepath,source_row_id,source_occurrences
```

## Coverage Notes (from Ghost6)
- Priced sportsbook observations cover Weeks 3–9.
- Weeks 1–2 have only retrospective full-game lines with unknown book and capture time.
- Quarter/half coverage is sparse; explicitly captured pregame period odds are limited to Week 9 JAX@BAL.
- Week 6 period odds have unknown capture times and are excluded from these pregame subsets.
- “Verified pregame” means the cache records capture before kickoff—not independent verification of the quote or a closing-line claim.

## Status
Full CSVs remain in the bot package (priority_data.zip). Header + counts + notes staged here for research review. No new API pulls. Research-only. Model remains NOT READY.
