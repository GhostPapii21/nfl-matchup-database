# Codex — 2026 Weeks 1–8 period/half coverage ledger (NO CORE edits)

## Hard rules
- Work ONLY under `/workspace/research/nfl_period_w1_8_2026/`
- Do NOT modify CORE / market_calibration / nfl-database production tools
- No paid Odds API / no PFF premium login / no access bypass
- Free data: `nflreadpy` schedules + pbp (nflverse). Official ESPN/gamebook only if publicly fetchable without auth; label source.
- Spread/total grading: **ONLY** if schedule row has moneyline/spread/total fields usable as retained historic quotes with documented limitation that nflverse lines are NOT verified closers/timestamps → otherwise mark **NOLINE** for market grade. **Scores are not spread covers.**
- AI/PFF "Key Takeaways" are out of scope here (browser-generated; do not invent).

## Deliverables
1. `data/games_w1_8.csv` — one row per completed 2026 W1–8 game: game_id, season, week, gameday, kickoff, home, away, home_score, away_score, overtime, q1-q4 scores if reconstructable from pbp, h1/h2, winner, tie flag, source=`nflverse_pbp+schedules`, pull_utc
2. `data/period_scores_w1_8.csv` — long or wide period table: game_id, period in {Q1,Q2,Q3,Q4,H1,H2,REG,OT}, home_pts, away_pts, cumulative_home, cumulative_away, period_winner, source
3. `data/coverage_ledger_w1_8.csv` — every game × required fields: scoreboard periods, OT, tie, source identity, missingness flags (PFF overview MISSING unless local public scrape exists for that game), market_spread_grade=NOLINE|GRADED with quote fields if present
4. `data/DEFINITIONS.md` — how quarters are computed from pbp (qtr), OT handling, cumulative, half = Q1+Q2 / Q3+Q4(+OT rule explicit)
5. `reviews/COUNTS.md` — N games expected vs built, missing panels, OT count, teams covered (all 32?)
6. `scripts/` reproducible builders + `pytest` for: 121 games (or exact schedule count), no future weeks, OT games flagged, period pts sum to final (with OT rule)
7. Optional: attempt public PFF recap URL pattern scrape for W1-8 ONLY if free and no login; record success/fail per game — do not claim PFF if failed

## JAX@BAL W9 note (context only, not in W1-8)
Local PFF public scrape exists under live notes; W9 is OUT of W1-8 ledger. Do not mix.

## Success
- All completed W1-8 games present
- Coverage ledger honest about MISSING PFF panels
- Market grades NOLINE when quote provenance insufficient
