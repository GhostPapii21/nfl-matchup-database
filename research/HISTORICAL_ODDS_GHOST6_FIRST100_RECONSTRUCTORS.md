# Ghost6 First-100 Row Reconstructors

**Delivered:** 2026-11-08 ~06:45 ET

## sportsbook_latest_verified_pregame.csv
- Full file: **104,742** rows
- Header (29 columns):
```csv
observation_id,season,week,game_id,event_id,game_date_et,away_team,home_team,bookmaker,platform_type,market,period,player,selection,line,price,odds_format,snapshot_timestamp,book_update_timestamp,market_update_timestamp,event_start_timestamp,snapshot_et,event_start_et,pregame_status,flags,upstream_source,source_filepath,source_row_id,source_occurrences
```
- Lossless Python reconstructor for first 100 rows provided in bot transcript (shared metadata + variable patches).

## week9_verified_pregame.csv
- Full file: **9,120** rows
- Same header
- Lossless Python reconstructor for first 100 rows provided in bot transcript.

## Coverage Notes (Ghost6)
- Named-book data covers Weeks 3–9. Weeks 1–2 retrospective only (unknown book/capture time).
- Verified pregame quarter/half limited to Week 9 JAX–BAL. Week 6 period rows lack capture timestamps and are excluded.
- “Verified pregame” = saved capture timestamp precedes kickoff (not independently authenticated closing line).
- Preserve all flags.

Research-only. Full CSVs remain in bot package.
