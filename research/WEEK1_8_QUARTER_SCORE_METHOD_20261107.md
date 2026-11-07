# NFL 2026 Weeks 1–8 quarter scoring reference (research only)

Generated from the public nflverse 2026 play-by-play release, downloaded 2026-11-07 17:10 UTC:
https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.csv.gz

The nflverse play-by-play dictionary defines `qtr` (1–4 regulation; 5 overtime) and includes game, team, time and score fields:
https://nflreadr.nflverse.com/articles/dictionary_pbp.html

## Files
- `WEEK1_8_QUARTER_SCORE_2026.csv`: one row per game, separate home/away points scored in Q1–Q4, overtime points, final scores, and source snapshot.
- `WEEK1_8_TEAM_QUARTER_SUMMARY_2026.csv`: one row per team and quarter; descriptive W1–8 points for/against, margin mean/median and win/tie/loss counts.

## Method
Filter to regular-season 2026 Weeks 1–8. For each game, take the cumulative home/away score from the last play row in each regulation quarter; quarter points are the difference from the prior quarter's cumulative score. Keep overtime outside Q1–Q4. Overtime points are final score minus cumulative score at the end of Q4. No quarter-market lines, prices, probabilities, or betting results are included.

## Audit notes
- 121 games across Weeks 1–8; all have a score row for each of Q1–Q4.
- 11 games have overtime rows; OT points are kept separate.
- The quarter summaries are descriptive, small-sample context (most teams have 7 or 8 games), **not** quarter-spread cover rates or forecasts.
- Before backtesting sportsbook quarter spreads, join exact book/event/period/line/price/time quotes and confirm settlement terms. Do not conflate standalone Q2 with first-half markets.
- No changes to model parameters, production data, or betting eligibility.
