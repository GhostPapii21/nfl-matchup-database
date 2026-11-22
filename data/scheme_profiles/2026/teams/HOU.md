# HOU scheme and opportunity profile, 2026

Houston Texans. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_HOU_LAC on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [8].

Game ids: 2026_01_BUF_HOU, 2026_02_CIN_HOU, 2026_03_HOU_IND, 2026_04_DAL_HOU, 2026_05_HOU_TEN, 2026_06_HOU_JAX, 2026_07_NYG_HOU, 2026_09_HOU_LAC.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 485. Early-down pass rate: 57.2% (215/376). Early-down run rate: 42.8% (161/376).
Neutral pass rate (margin -7 to +7): 59.9% (208/347). Leading by 8+: 54.7% (41/75). Trailing by 8+: 73.0% (46/63). Tied: 54.8% (51/93).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 38.6% (22/57). Long-yardage pass rate (7+ yards to go): 64.3% (225/350).
Third down: 40.2% (41/102). Unknown third-down results: 0.
Red-zone plays: 76. Red-zone pass rate: 57.9% (44/76). Derived red-zone drive touchdown rate: 58.1% (18/31). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 10.8% (32/295); rush 10+ 9.5% (18/190); rush 15+ 1.6% (3/190). Official explosive label: unknown.
Sacks taken: 16. Scrambles: 11 (3.6% (11/306) of dropbacks). Kneels, excluded from carries: 4.
Shotgun rate, where the flag is present: 68.9% (334/485). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 68, middle 44, right 78, unknown 0.

## Defense, regulation

Scrimmage plays faced: 507. Early-down pass rate allowed: 55.0% (214/389).
Third down allowed: 38.7% (41/106). Sacks recorded: 29. Scrambles allowed: 8.
Explosive passes allowed (20+): 10.2% (31/303). Explosive rushes allowed (10+): 7.8% (16/204).

## Overtime

Offensive scrimmage plays: 3. Early-down pass rate: 50.0% (1/2). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 53.7% (122/227) across 5 games (COMPLETE). Earlier games: 62.4% (93/149). Difference: -0.087.
Last 8 early-down pass rate: 57.2% (215/376) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| D.Schultz | 47 | 0.175 | 8 |
| X.Hutchinson | 45 | 0.168 | 8 |
| N.Collins | 39 | 0.146 | 6 |
| K.Boutte | 28 | 0.104 | 8 |
| J.Noel | 23 | 0.086 | 7 |
| W.Marks | 21 | 0.078 | 8 |
| F.Moreau | 14 | 0.052 | 6 |
| J.Wayne | 12 | 0.045 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| W.Marks | 95 | 0.497 | 8 |
| D.Montgomery | 52 | 0.272 | 5 |
| C.Stroud | 18 | 0.094 | 8 |
| E.Demercado | 6 | 0.031 | 1 |
| J.Jordan | 6 | 0.031 | 1 |

## Gamebook checks

- 2026_09_HOU_LAC: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794257318/gamecenter/ab580cb7-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
