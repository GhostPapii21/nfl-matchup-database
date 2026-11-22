# IND scheme and opportunity profile, 2026

Indianapolis Colts. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_DAL_IND on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_BAL_IND, 2026_02_IND_KC, 2026_03_HOU_IND, 2026_04_IND_WAS, 2026_05_IND_PIT, 2026_06_TEN_IND, 2026_07_IND_MIN, 2026_08_IND_JAX, 2026_09_DAL_IND.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 569. Early-down pass rate: 53.2% (230/432). Early-down run rate: 46.8% (202/432).
Neutral pass rate (margin -7 to +7): 55.6% (230/414). Leading by 8+: 50.0% (11/22). Trailing by 8+: 64.7% (86/133). Tied: 54.5% (54/99).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 28.1% (18/64). Long-yardage pass rate (7+ yards to go): 63.5% (250/394).
Third down: 37.2% (45/121). Unknown third-down results: 0.
Red-zone plays: 72. Red-zone pass rate: 40.3% (29/72). Derived red-zone drive touchdown rate: 65.2% (15/23). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 5.2% (17/327); rush 10+ 11.6% (28/242); rush 15+ 4.5% (11/242). Official explosive label: unknown.
Sacks taken: 25. Scrambles: 12 (3.5% (12/339) of dropbacks). Kneels, excluded from carries: 4.
Shotgun rate, where the flag is present: 62.9% (358/569). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 85, middle 54, right 101, unknown 2.

## Defense, regulation

Scrimmage plays faced: 507. Early-down pass rate allowed: 48.2% (188/390).
Third down allowed: 31.4% (33/105). Sacks recorded: 18. Scrambles allowed: 13.
Explosive passes allowed (20+): 10.2% (28/275). Explosive rushes allowed (10+): 11.6% (27/232).

## Overtime

Offensive scrimmage plays: 4. Early-down pass rate: 33.3% (1/3). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 52.9% (128/242) across 5 games (COMPLETE). Earlier games: 53.7% (102/190). Difference: -0.008.
Last 8 early-down pass rate: 52.6% (205/390) across 8 games. Difference versus earlier: -0.070.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| K.Allen | 58 | 0.202 | 8 |
| J.Downs | 57 | 0.199 | 9 |
| T.Warren | 53 | 0.185 | 7 |
| J.Taylor | 36 | 0.125 | 9 |
| L.Treadwell | 29 | 0.101 | 9 |
| A.Dulin | 9 | 0.031 | 3 |
| D.Burks | 9 | 0.031 | 6 |
| W.Mallory | 9 | 0.031 | 2 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Taylor | 161 | 0.657 | 9 |
| S.McGowan | 43 | 0.176 | 8 |
| D.Jones | 25 | 0.102 | 9 |
| D.Giddens | 6 | 0.024 | 1 |
| D.Burks | 3 | 0.012 | 2 |

## Gamebook checks

- 2026_09_DAL_IND: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224921/gamecenter/ab38123a-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
