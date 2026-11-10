# 2026 Week 9 — Buffalo Bills at Minnesota Vikings

Official NFL Game Summary, used here as a postgame research input.

| Field | Value |
| --- | --- |
| Source | Official NFL Game Summary PDF supplied by the owner |
| nflverse `game_id` | `2026_09_BUF_MIN` (supplied at ingest; not printed on the PDF) |
| Week | 9 (supplied at ingest; not printed on the PDF) |
| Date printed | Monday, 11/9/2026, kickoff 7:16 PM CST |
| Venue | U.S. Bank Stadium, Minneapolis, MN |
| Roof / surface line | Indoors. Closed Stadium on Field Turf |
| Final | Buffalo Bills 23, Minnesota Vikings 6 |
| Ingested | 2026-11-10 |
| PDF | `2026_09_BUF_MIN_gamebook.pdf` |
| PDF SHA-256 | `056ac51502fffbff963f8c7ab1b425a6965e3631cc77b9d84890c3beb502f7a2` |
| Source URL | `https://static.www.nfl.com/image/upload/v1794285215/gamecenter/ab5825a7-4feb-11f1-abca-2c54536568a9.pdf` |
| Text | `2026_09_BUF_MIN_gamebook.txt` |
| Text extract | `pdftotext -layout` (a fresh run matches the committed text byte for byte) |
| Text SHA-256 | `189329381c78d5a032ba7e58627caad7e6dcb5b43504eef0fc2eda0a64a598d3` |

## Copyright and media-use restriction

NFL Copyright © 2026 by The National Football League. All rights reserved. This summary and play-by-play is for the express purpose of assisting media in their coverage of the game; any other use of this material is prohibited without the written permission of the National Football League.

The same paragraph is stored in `provenance.json`.

## What this ingest does not do

It does not change model weights, formulas, simulator code, configs, or `projection_ready`. It does not run a batch simulation. The sqlite snapshot in the repo-root `manifest.json` was not rebuilt. The 2026-11-06 source registry and source-run-gate manifests were left as they were.

## Files

- `2026_09_BUF_MIN_gamebook.pdf` — the PDF, unchanged.
- `2026_09_BUF_MIN_gamebook.txt` — `pdftotext -layout` text.
- `provenance.json` — source label, hashes, ingest date, copyright notice, CSV row counts.
- `parsed/*.csv` — tidy tables. Every printed number is text. The only flags added by the parser are labels of something already printed: `is_total`, `bracket_row` (`[DOWNED]` / `[TOUCHBACK]`), `contains_reversed_text` (the word REVERSED), `result` on field goals (parentheses mean made, from the heading "made ( ) & missed"), and `date_iso` (the printed `11/9/2026` written as `2026-11-09`).
- `scope` is `final` or `first_half`. First-half rows are the printed first-half summary, not a split computed from the final line.

Rebuild the CSVs from the committed text with `data/gamebooks/parse_nfl_game_summary.py`. The command is in `docs/DATA_UPDATE.md`. Check the extract with:

```sh
python3 -m unittest data/gamebooks/tests/test_2026_09_buf_min.py
```

## CSV row counts

Counts are data rows, not including the header. `provenance.json` is the same list.

| CSV | Rows |
| --- | ---: |
| game_meta | 1 |
| officials | 8 |
| quarter_scores | 12 |
| scoring_plays | 7 |
| field_goals | 5 |
| lineups | 44 |
| participation | 64 |
| rushing | 19 |
| passing | 9 |
| receiving | 38 |
| interceptions | 5 |
| punting | 4 |
| returns | 13 |
| fumbles | 7 |
| defense | 58 |
| team_stats | 55 |
| drives | 25 |
| drive_notes | 5 |
| time_of_possession | 2 |
| quarter_summaries | 8 |
| play_by_play | 223 |
| touchdown_units | 2 |
| player_scoring | 4 |
| possession_detail | 8 |
| parse_gaps | 13 |

`participation` is 52 substitutions plus 12 not-active players. `lineups` is 11 offensive and 11 defensive starters for each club. Rushing, passing, receiving, and defense include both `final` and `first_half` rows. `play_by_play` includes scrimmage plays, kickoffs, timeouts, drive headers, score lines, and notes. The unit test locks 151 scrimmage rows to the down-and-distance lines in the text.

## Parse gaps and printed quirks

These are also rows in `parsed/parse_gaps.csv`.

- **Longest plays were not emitted.** `pdftotext` wrapped the tail of an injury update on an 8-yard Minnesota play into the next 8-yard row, so that pair of yard and quarter cells is not trustworthy. Those plays remain in `play_by_play`.
- **Did Not Play is blank** for both clubs. No players were invented.
- **Week and the nflverse id are not on the PDF.** They were supplied at ingest.
- **First-half defense is a short printed list** (8 players plus totals) and was not filled from the play-by-play. A first-half sack can be missing from that list.
- **Reversed plays keep both wordings.** Four descriptions contain the original call and the REVERSED call. No yardage was read out of those sentences.
- **One lateral** (K.Coleman to K.Shakir) stays in the play text. Receiving credit is only the printed receiving line.
- **Pass attempts and targets differ as printed** (BUF 31 attempts / 29 targets, MIN 32 / 30). Both are stored. Completions match receptions (21 and 14) and passing yards match receiving yards (234 and 139).
- **`[DOWNED]` and `[TOUCHBACK]`** are kept. The printed return Total does not include them.
- **First-half scoring plays and the "3 7 = 10" line** repeat the final scoreboard. They are not a second score table. The raw reprint is in `parse_gaps`.
- **Player scoring `td` is printed 0** for J.Cook and K.Latu even though `rush_td` / `rec_td` is 1 and points are 6. The zero was not replaced with a sum. T.Bass is fg 3, xp 2, points 11.
- **Overtime points are the printed 0.** Time of possession leaves the OT cell blank because the PDF left it blank.
- Wrapped play lines are joined with a single space. The words and numbers are the printed ones. A clock such as `(:57)` stays `:57`.
