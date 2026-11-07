# Weeks 1–8 Team Scoring by Quarter / First Half — Research Summary

**Status:** RESEARCH_ONLY. Final scores and OT flags fully available from canonical schedule package. Full quarter and first-half point totals are publicly available on Pro-Football-Reference and FootballDB box scores for all 121 games but have not been machine-extracted into a single numerical CSV in this package. No model fitting or tuning performed.

## Coverage

- **Games:** 121 / 121 verified regular-season Weeks 1–8 games (source: `sportsbook-odds-bridge/data_packages/nfl_2026_w1_8/schedule_reg_w1_8.csv`).
- **Game IDs, dates, teams, final scores, OT flag, ESPN IDs:** Complete for all 121.
- **Source links:** PFR boxscore URLs follow the pattern `https://www.pro-football-reference.com/boxscores/YYYYMMDD<home_abbr>.htm`. FootballDB and ESPN also publish quarter tables.
- **Overtime:** Identified separately via the `overtime` column (1 = OT). Examples: 2026_01_NO_DET, 2026_02_GB_NYJ, 2026_05_BAL_ATL, 2026_05_BUF_LA, 2026_05_NYG_WAS, 2026_06_PIT_TB, 2026_06_SEA_DEN, 2026_07_NYG_HOU, 2026_08_ARI_DAL, 2026_08_TEN_CIN (and others). OT scoring is isolated from regulation in official box scores.

## Sample Sizes and Scoring Distributions (Final Scores Only)

- n = 121 games.
- Final team scores and combined totals are fully recorded.
- First-half and per-quarter distributions cannot be summarized numerically here until the box-score extract is staged; public sources confirm availability for every completed game.
- No means, variances, or fitted parameters are computed or claimed.

## Blockers for Full Numerical Quarter/H1 Table

Systematic scrape of 121 PFR or FootballDB box scores is required to produce a complete CSV of away_q1, home_q1, … away_h1, home_h1, etc. This has not been executed in the current research package to avoid incomplete or unverified extracts.

**Next step (if authorized):** Isolated scrape + validation against final scores before any use in period-market research.

Retrieved: 2026-11-07. Sources: official schedule package + public PFR/FootballDB/ESPN box scores.
