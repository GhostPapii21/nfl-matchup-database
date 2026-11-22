# DET scheme and opportunity profile, 2026

Detroit Lions. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_DET_MIA on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [6].

Game ids: 2026_01_NO_DET, 2026_02_DET_BUF, 2026_03_NYJ_DET, 2026_04_DET_CAR, 2026_05_DET_ARI, 2026_07_GB_DET, 2026_08_MIN_DET, 2026_09_DET_MIA.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 506. Early-down pass rate: 50.9% (201/395). Early-down run rate: 49.1% (194/395).
Neutral pass rate (margin -7 to +7): 54.9% (202/368). Leading by 8+: 41.5% (22/53). Trailing by 8+: 75.3% (64/85). Tied: 55.2% (69/125).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 30.9% (17/55). Long-yardage pass rate (7+ yards to go): 59.7% (218/365).
Third down: 37.2% (35/94). Unknown third-down results: 0.
Red-zone plays: 103. Red-zone pass rate: 54.4% (56/103). Derived red-zone drive touchdown rate: 62.5% (20/32). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.6% (22/288); rush 10+ 14.2% (31/218); rush 15+ 6.4% (14/218). Official explosive label: unknown.
Sacks taken: 19. Scrambles: 6 (2.0% (6/294) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 47.0% (238/506). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 75, middle 74, right 66, unknown 3.

## Defense, regulation

Scrimmage plays faced: 505. Early-down pass rate allowed: 59.5% (229/385).
Third down allowed: 44.9% (48/107). Sacks recorded: 26. Scrambles allowed: 14.
Explosive passes allowed (20+): 9.7% (32/330). Explosive rushes allowed (10+): 13.1% (23/175).

## Overtime

Offensive scrimmage plays: 10. Early-down pass rate: 50.0% (5/10). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 48.8% (120/246) across 5 games (COMPLETE). Earlier games: 54.4% (81/149). Difference: -0.056.
Last 8 early-down pass rate: 50.9% (201/395) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| A.St. Brown | 86 | 0.320 | 8 |
| S.LaPorta | 49 | 0.182 | 8 |
| J.Williams | 46 | 0.171 | 8 |
| J.Gibbs | 45 | 0.167 | 8 |
| I.TeSlaa | 23 | 0.086 | 7 |
| S.Vaki | 8 | 0.030 | 6 |
| B.Wright | 6 | 0.022 | 4 |
| T.Conklin | 3 | 0.011 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Gibbs | 177 | 0.794 | 8 |
| S.Vaki | 30 | 0.135 | 7 |
| J.Goff | 12 | 0.054 | 7 |
| A.St. Brown | 2 | 0.009 | 2 |
| J.Williams | 1 | 0.004 | 1 |

## Gamebook checks

- 2026_09_DET_MIA: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224917/gamecenter/ab381a59-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
