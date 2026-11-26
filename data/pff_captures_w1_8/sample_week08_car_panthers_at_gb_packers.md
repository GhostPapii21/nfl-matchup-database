# PFF sample feasibility: 2026 NFL Week 8

## Source and sample identity
- Schedule page: https://www.pff.com/nfl/scores?week=8
- Game recap page: https://www.pff.com/nfl/scores/2026/8/carolina-panthers_at_green-bay-packers_30713#recap
- Page title: Panthers vs. Packers (Oct 29, 2026) Live Score and Odds
- Identity/date: 2026 Season, Week 8; Carolina Panthers at Green Bay Packers; Thursday, October 29, 2026.
- Final: Panthers 19, Packers 27.
- This is explicitly 2026, not a default/current-year fallback: recap header visibly reads Week 8, October 29, 2026, 2026 Season.

## Access and export feasibility
- On the PFF recap page, “Generate Key Takeaways” was available and was activated; it changed to “Hide Key Takeaways” and displayed comparison/standout cards without a purchase prompt.
- The recap page also visibly offered “Start your free trial of PFF Pro,” “View in Premium Stats,” and “Jump to box score.” No CSV or Download control was exposed on the recap; browser UI search found no “CSV” or “Download” control. The sample below was transcribed from visible page content, not exported.
- Separate Premium Stats team table still showed locked detailed cells in the prior feasibility check; do not interpret this recap visibility as proof that the paid Premium Stats database is unlocked.
- PFF note shown on page: “Data: Pro Football Focus · Initial grades subject to review.”

## PFF-generated analysis (keep separate from measured box-score/stat rows)
The page-generated “Biggest Team Differences” card reported Panthers vs. Packers:
- Air yards: 83 vs. 198; Packers +115.
- Total net yards: 254 vs. 338; Packers +84.
- Gross passing yards: 210 vs. 288; Packers +78.
- Yards on deep completions: 0 vs. 77; Packers +77.
- Yards on explosive passes: 62 vs. 117; Packers +55.

The page-generated “Box Score Standouts” card reported:
- Jordan Love (Packers passing): 288 yards, 30/41 completions, 3 TD, 1 INT.
- Chuba Hubbard (Panthers rushing): 80 yards, 22 attempts, 1 TD, 3.6 yards/carry.
- Christian Watson (Packers receiving): 113 yards, 8/10 receptions, 0 TD, 14.1 yards/reception.
- Brenton Cox Jr. (Packers pass rush): 6 pressures, 1 sack, 1 hit, 4 hurries.
- Zakee Wheatley (Panthers coverage): 1 INT, 0 pass breakups, 0/0 targets.
- Bobby Okereke (Panthers run defense): 3 run stops, 3 tackles, 1 assist, 0 TFL+NG.

These are PFF's generated summary/selection, not a separately authored interpretation. Do not merge with or present them as independent measured stats without provenance.

## Visible measured/statistical sections (sample values transcribed from visible carousel cards)
- Game Overview: 12 cards; includes score timeline and team-game context. The visible headline score is CAR 19–27 GB.
- Team Rushing Reports: 4 cards. EPA per rushing play card: Panthers -0.13 (34th percentile), Packers -0.15 (28th percentile), ranked against every 2026 team game.
- Team Passing Reports: 11 cards. EPA per passing play card: Panthers -0.15 (22nd percentile), Packers +0.17 (63rd percentile), ranked against every 2026 team game.
- Quarterback Comparison: 5 cards. QB box-score card: Bryce Young—47 dropbacks, 41 attempts, 23 completions, 210 pass yards, 1 TD, 1 INT, 68.1 passer rating; Jordan Love—41 dropbacks, 41 attempts, 30 completions, 288 pass yards, 3 TD, 1 INT, 106.6 passer rating.
- Player Participation & Snap Counts: 4 cards. Panthers offense card lists 17 players; visible examples include Bryce Young 73 snaps and Chuba Hubbard 67.
- Initial PFF Grades: 12 cards. The visible offense top-five card begins Corey Bullock 87.8, Tucker Kraft 82.7, Jordan Love 79.6, Jordan Morgan 74.6, Robert Hunt 70.3. PFF labels these grades initial and subject to review.
- Box Score Breakdown: 12 cards. Visible Panthers rushing card: Chuba Hubbard—80 rush yards, 22 attempts, 3.6 YPC, 2 missed tackles forced, 1 rush TD, 12 yards before contact, 68 yards after contact; Trevor Etienne—1 rush yard, 1 attempt, 1.0 YPC, 0 missed tackles forced, 0 rush TD, 0 yards before contact, 1 after contact.

## Workflow implications
A repeatable visible-UI route exists: NFL Scores & Schedule > select 2026 Week > open a completed game > Recap > Generate Key Takeaways. For backfill, collect each game's recap page and section data with provenance; preserve PFF-generated takeaways separately from source statistics and retain the “initial grades subject to review” caveat. This was a one-game sample only; Weeks 1–8 coverage has not been performed.

## Visible schedule coverage inspection (selected 2026 weeks)
Using the on-page 2026 Week selector at https://www.pff.com/nfl/scores, the schedule list exposed completed-game links as follows:
- Week 1: 16
- Week 2: 16
- Week 3: 16
- Week 4: 16
- Week 5: 15
- Week 6: 14
- Week 7: 14
- Week 8: 14
- Total visible game links for Weeks 1–8: 121

This count is from visible schedule links only; it is a coverage estimate for backfill, not evidence that all 121 recaps have been opened or extracted. The week selector updates the page URL to `?week=N`, and each game link carries a 2026/week/game slug, so a permitted, efficient workflow would enumerate those visible links by week, then process each game's Recap/Generate Key Takeaways/section content systematically. The current run intentionally stopped after the single Week 8 sample and schedule count inspection.
