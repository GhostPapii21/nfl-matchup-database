# Existing historical NFL odds inventory — November 7, 2026 (ET)

Local-only research export. No network/API requests, credits, repository writes, PR updates, model changes, or messages. Originals preserved. This is source recovery, not independent verification that cached vendor responses were accurate or executable.

## Recommended staging files
- `sportsbook_latest_verified_pregame.csv`: 104,742 outcome quotes; latest explicitly captured pre-start observation for each game/book/market/period/player/selection/line. Different lines remain separate. Not a closing-line claim.
- `week9_verified_pregame.csv`: 9,120 explicitly captured pre-start Week 9 observations, retaining historical snapshots.
- `sportsbook_observations.csv`: 264,785 normalized historical sportsbook observations across 104 games, 12 named books, actual schedule Weeks 3–9. Includes unknown-capture and after-start rows: FILTER `pregame_status` before using for pregame research.
- `retrospective_game_lines_book_unknown.csv`: 816 full-game outcome rows from saved nflverse schedule, Weeks 1–9, book and quote timestamp unknown. Not point-in-time observations and not verified closing prices. No prices filled in.
- `non_sportsbook_platform_observations.csv`: 71,188 pick'em/exchange observations kept separate, not counted as sportsbook coverage.
- `coverage_by_week_book_market.csv`, `summary.json`, `source_manifest.csv`, `provenance.csv`: counts and complete per-observation source-file/row mapping.
- `source_artifacts/`: content-deduplicated source copies keyed by SHA256. Manifest maps each original path to packaged copy and records original and packaged hashes. JSON canonicalized and credential keys/query parameters redacted; schedule copy filtered to 2026 REG Weeks 1–9. No credential files opened or packaged.

## Coverage / limits
Books: betmgm, betonlineag, betrivers, betus, bovada, draftkings, fanatics, fanduel, lowvig, mybookieag, pinnacle, williamhill_us.

| Actual week | Sportsbook observations | Games | Explicitly captured pre-start |
|---|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 4,602 | 16 | 4,602 |
| 4 | 4,436 | 16 | 4,436 |
| 5 | 3,994 | 15 | 3,994 |
| 6 | 54,335 | 14 | 31,585 |
| 7 | 37,018 | 14 | 35,130 |
| 8 | 150,406 | 14 | 135,002 |
| 9 | 9,994 | 15 | 9,120 |

- Weeks 1–2: only retrospective full-game lines in saved schedule found; no priced, named-book point-in-time sportsbook props recovered. Stand-in/simulated prop lines in the v6 hit-rate backtest are excluded.
- Weeks 3–5: recovered full-game player rushing, receiving, and rush+receiving yardage markets. No quarter/half game markets recovered there.
- Week 6: full game plus selected H1/Q1 markets, sparse Q2–Q4 spreads/totals. Player Q1 receiving/rushing yards and H1 rushing yards exist, not a comprehensive slate. IMPORTANT: all recovered Week 6 quarter/half observations lack explicit capture timestamps; none qualify for the verified-pregame subset (book updates alone are insufficient).
- Weeks 7–8: full-game game lines and props; no quarter/half coverage in recovered sources.
- Week 9: full-game game lines and selected props across 15 games; quarter/half markets limited to JAX@BAL. Sunday line-watch covers 13 games; DraftKings game lines and FanDuel game/prop lines have differing availability. Preserve native market names (`spread` vs `spreads`, `receiving_yards` vs `player_reception_yds`); not economically deduplicated across vendor taxonomies.
- Missing Q/H/prop books/markets are gaps, not evidence no markets existed. No wholesale historic slate, no executable SGP quotes, no guaranteed opener/closing observations.
- `hist_props_oddsapi/lines.parquet` was checked via its README: intentionally EMPTY, exhausted quota, zero historical games. It is NOT included as odds evidence. Historical raw files under `hist_props` also contain January 2026 games from a prior season; these are excluded by game schedule matching.
- A saved source folder may be mislabeled: Nov 1/Nov 2 = actual Week 8; JAX@BAL Nov 5 = Week 9, although `line_movement_wk10` calls it Week 10. Use the saved 2026 NFL regular-season schedule `game_id`/week, not directory names. All datetime matching uses America/New_York calendar date, so UTC next-day kickoffs map correctly.
- `pregame_status=verified_capture_before_start` means source explicitly records snapshot/pull/fetch time before event start (not external authentication of the quote). Source update alone cannot prove capture before start; these are `update_before_start_capture_unknown`. At/after-start rows are never in recommended pregame files. Historical snapshot timestamp may differ from pull time; historical API snapshot is used when present. File mtime is NEVER quote/capture time.
- Preserve source timestamp offsets; normalized timestamps are ISO8601 with offsets and supplementary `snapshot_et`/`event_start_et` fields. ET is America/New_York (-04:00 or -05:00 as appropriate). Source originals remain in packaged copies. Naive explicitly-labeled `pulled_et` metadata localized to America/New_York.
- `odds_format` inferred from numeric scale (absolute value >=100 American, positive >1 and <100 decimal) where absent; flagged as inferred. No conversion or implied/no-vig probability calculation. NULL CSV values are empty cells. nflverse handicap signs translated from home-favored spread_line into selection handicap; source feed retains original sign in schedule copy.
- Exact normalized rows deduplicated with all timestamp/flag fields retained. Different snapshots, source feeds, update timestamps, and quote lines remain distinct; counts are correlated outcome observations, NOT independent bets. `source_occurrences` and `provenance.csv` preserve duplicates. Latest quote file is a compact per-line view, not a single final market.
- Discovery was bounded to canonical local NFL repositories/caches and existing NFL line-watch ledger. Worktree/review clone copies were not re-read; no claim all data anywhere on disk was found. Oversized/nonmatching JSON and non-supported formats were not mined. Raw sources with out-of-scope dates can remain in source copies; only normalized requested-week data should be staged as usable evidence.
