# Weeks 1–8 Quarter / Half Scores — ESPN & NFL.com Verification

**Date:** 2026-11-07
**Status:** RESEARCH_ONLY. No model changes.

## Verification Method

- Primary extract: FootballDB public quarter tables (footballdb.com/scores).
- Cross-check: ESPN scoreboard pages (espn.com/nfl/scoreboard/_/week/N) which display Q1–Q4 and Final for completed games.
- Secondary: NFL.com scores/schedules for final scores and OT flags.

## Sample Matches Confirmed (ESPN vs FootballDB)

| Game | ESPN Q1-Q4 Final | FootballDB | Match |
|------|------------------|------------|-------|
| NE @ SEA (Wk1) | 0-7-3-0 / 0-0-3-10 = 10-13 | Same | Yes |
| SF @ LAR (Wk1) | 3-7-7-10 / 0-7-0-0 = 27-7 | Same | Yes |
| CAR @ GB (Wk8) | 3-7-3-6 / 6-14-7-0 = 19-27 | Same | Yes |
| BAL @ BUF (Wk8) | 7-0-3-0 / 10-6-7-13 = 10-36 | Same | Yes |

Additional OT flags on ESPN/NFL.com match the earlier list (e.g., ARI-DAL, TEN-CIN, SEA-DEN, etc.).

## Conclusion

Quarter scoring tables from FootballDB are consistent with ESPN scoreboards and NFL.com final/OT results on all sampled games. Full 121-game numerical extract remains available from these public sources. First-half = Q1+Q2. Overtime scored separately and excluded from regulation quarters/halves.

Sources:
- https://www.espn.com/nfl/scoreboard/_/week/1
- https://www.espn.com/nfl/scoreboard/_/week/8
- https://www.nfl.com/scores/2026/week-8
- FootballDB week pages (previously extracted)
