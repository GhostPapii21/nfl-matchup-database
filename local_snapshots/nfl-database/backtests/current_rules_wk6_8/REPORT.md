# Weeks 6-8 (2026) replay through the current rulebook on real prices
Test only. Nothing went live and no bets were placed. Run on Nov 3, 2026, ET.

- **Prices:** Odds API historical, one snapshot 30 minutes before each kickoff. That's 41 games and 1,428 player lines on 4 markets (rec yds, receptions, rush yds, pass yds), US books. The price used is FanDuel when it has the line (70%), otherwise the first book with it. No-vig is the two-way devig averaged across books at the main line. About 1,770 credits used.
- **Models:** sim_v6 MC, Bias and GR at 100k runs each, leak-free (the Engine only sees games before week W). Raw with no calibration, because the calibration was fit on Weeks 4-7 and would leak. Opponent adjustment is at full strength, as in the current sim_v6.
- **Rules (thresholds read from rules/rulebook.py, depth rule from tools/depth_rule.evaluate):** NOSHRINK (+3, model p .45), FORM_3OF4, SCHEME_EDGE (flag/override), N1, RB_TRAIL, DEPTH_RECEIVER, WEATHER (wind), SHORT_PRICE flag, and mirror overs (both sides graded).
- **OFF / not replayable:**
  - TEAM_FILES is off (team files are not built yet).
  - N2: no historical verified-defender source.
  - COVERAGE_AGE, FORECAST and COVPROF: no historical snapshots.
  - INJURY: only players who played are graded.
  - N3: there are no half or quarter lines in this pull.
- **Proxies:**
  - SCHEME_EDGE = matchup (the opponent allows more than average to the position group) + script (spread/total) + form (last-4 average with the current QB on the bet side). There is no sourced scheme-fit check for past weeks, so the position-group matchup stands in for it.
  - Depth inputs: WR rank and TE rank by targets over the last 4 games, team target share, and the position-group yards per target allowed.
- **Not included:** MNF CHI@SEA (Nov 2) is not in the play-by-play feed yet.
- **Counting:** the best leg per player per week is counted (the §11 one-slip-per-player rule).

| bucket | legs | W-L | hit | $10 flat |
|---|---|---|---|---|
| PASSED (best leg per player) | 293 | 142-151 | 48.5% | $-272 |
|   Week 6 | 98 | 54-44 | 55.1% | $+36 |
|   Week 7 | 88 | 40-48 | 45.5% | $-141 |
|   Week 8 | 107 | 48-59 | 44.9% | $-167 |
|   recyds | 112 | 52-60 | 46.4% | $-136 |
|   rec | 101 | 48-53 | 47.5% | $-126 |
|   rushyds | 58 | 33-25 | 56.9% | $+41 |
|   passyds | 22 | 9-13 | 40.9% | $-51 |
|   overs | 102 | 43-59 | 42.2% | $-185 |
|   unders | 191 | 99-92 | 51.8% | $-87 |
|   SCHEME_EDGE overriding 3-of-4 | 54 | 20-34 | 37.0% | $-159 |
|   depth receivers (WR3/4, TE2) | 42 | 20-22 | 47.6% | $-57 |
|   -250 or shorter (flag) | 0 | | | |
|   alive only because the shrink is gone | 20 | 11-9 | 55.0% | $-4 |
| BLOCKED by a rule (had +3 edge) | 431 | 218-213 | 50.6% | $-184 |
|   FORM_3OF4 | 401 | 203-198 | 50.6% | $-178 |
|   N1 | 37 | 19-18 | 51.4% | $-11 |
|   RB_TRAIL | 10 | 5-5 | 50.0% | $-6 |
|   DEPTH_RECEIVER | 64 | 36-28 | 56.2% | $+71 |
|   WEATHER | 0 | | | |
| SCHEME_EDGE FLAGS (+0 to +3, for Ghost6 at real price) | 25 | 16-9 | 64.0% | $+37 |
| Positive edge under +3 (cut) | 149 | 72-77 | 48.3% | $-109 |
| No model edge (all sides) | 1327 | 653-674 | 49.2% | $-1,023 |
Model Brier (overs, all 1,323 lines) 0.267 vs market no-vig 0.247 (lower is better). Passed legs: model said 67.3% avg, no-vig 50.4%, actual 48.5%. By edge size: +3 to +6 went 17-15 (53%), +6 to +10 went 49% and +10 or more went 47.6% (-$232). The bigger the claimed edge, the worse it hit.
