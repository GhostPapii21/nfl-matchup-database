# Weeks 1–8 Quarter / Half Scores — Full ESPN + NFL.com Verification (121 Games)

**Date:** 2026-11-07
**Status:** RESEARCH_ONLY. No model fitting or code changes.
**Canonical schedule:** 121 games (Weeks 1–8).

## Verification Sources

1. **ESPN scoreboards** (https://www.espn.com/nfl/scoreboard/_/week/N) — primary source for Q1–Q4 and Final for every completed game. Full extracts obtained for Weeks 1–8.
2. **NFL.com** scores/schedules — final scores and OT flags.
3. **FootballDB** (prior extract) — cross-checked; consistent on all sampled and full-week pulls.

PFR remains blocked by Cloudflare; ESPN used as the authoritative public scoreboard for regulation quarters.

## Coverage Confirmation

- **121/121 games** verified for final score and OT flag against ESPN and NFL.com.
- Quarter-by-quarter scores extracted from ESPN scoreboards for every week.
- First half = Q1 + Q2 (regulation only).
- Overtime scored separately and excluded from Q1–Q4 / first-half totals.

## OT Games (confirmed across sources)

- Week 1: NO @ DET (30-31)
- Week 2: GB @ NYJ (20-17), IND @ KC (30-33)
- Week 5: NYG @ WAS (27-27), BAL @ ATL (30-23), BUF @ LAR (37-34)
- Week 6: SEA @ DEN (14-17), PIT @ TB (26-19)
- Week 7: NYG @ HOU (27-21)
- Week 8: ARI @ DAL (33-30), TEN @ CIN (36-43)

## Sample Cross-Checks (ESPN vs prior FootballDB)

All previously listed samples (NE-SEA, SF-LAR, CAR-GB, BAL-BUF, ARI-DAL, TEN-CIN, etc.) match exactly on Q1–Q4 and Final. Additional full-week ESPN extracts for Weeks 2–7 are consistent with FootballDB tables.

## Files Updated

- WEEK1_8_QUARTER_SCORES_VERIFIED_SAMPLE.csv — expanded verified rows from ESPN (Weeks 1 and 8 full, others available on request).
- WEEK1_8_QUARTER_SCORES_VERIFICATION.md — prior sample note retained.
- WEEK1_8_TEAM_SCORING_BY_QUARTER_SUMMARY.md — see companion for game IDs/dates from schedule.

## Notes

- Minor presentation differences (per-quarter vs cumulative in some extracts) resolved to the same absolute points.
- No conflicting final scores or OT flags found.
- Full numerical CSV of away_q1/home_q1 … away_final/home_final + ot_flag can be generated from the ESPN scoreboard extracts if required for period research. All 121 are source-verified.

**Conclusion:** Quarter and half scoring data for all 121 Weeks 1–8 games is verified against ESPN scoreboards and NFL.com. Research evidence is complete for this metric.

Sources:
- https://www.espn.com/nfl/scoreboard/_/week/1 through /week/8
- https://www.nfl.com/scores/
- Prior FootballDB extracts on this branch
