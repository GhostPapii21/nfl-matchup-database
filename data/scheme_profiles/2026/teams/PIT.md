# PIT scheme and opportunity profile, 2026

Pittsburgh Steelers. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_08_CLE_PIT on 2026-11-01. Last fully completed week is 9. Bye weeks inside weeks 1-9: [9].

Game ids: 2026_01_ATL_PIT, 2026_02_PIT_NE, 2026_03_CIN_PIT, 2026_04_PIT_CLE, 2026_05_IND_PIT, 2026_06_PIT_TB, 2026_07_PIT_NO, 2026_08_CLE_PIT.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 480. Early-down pass rate: 59.2% (221/373). Early-down run rate: 40.8% (152/373).
Neutral pass rate (margin -7 to +7): 61.1% (209/342). Leading by 8+: 34.5% (10/29). Trailing by 8+: 76.1% (83/109). Tied: 62.4% (63/101).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 40.0% (18/45). Long-yardage pass rate (7+ yards to go): 64.0% (219/342).
Third down: 37.3% (38/102). Unknown third-down results: 0.
Red-zone plays: 66. Red-zone pass rate: 63.6% (42/66). Derived red-zone drive touchdown rate: 47.8% (11/23). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.9% (24/302); rush 10+ 12.9% (23/178); rush 15+ 7.9% (14/178). Official explosive label: unknown.
Sacks taken: 23. Scrambles: 5 (1.6% (5/307) of dropbacks). Kneels, excluded from carries: 10.
Shotgun rate, where the flag is present: 66.7% (320/480). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 75, middle 52, right 51, unknown 0.

## Defense, regulation

Scrimmage plays faced: 476. Early-down pass rate allowed: 58.0% (210/362).
Third down allowed: 35.0% (36/103). Sacks recorded: 25. Scrambles allowed: 11.
Explosive passes allowed (20+): 9.1% (27/298). Explosive rushes allowed (10+): 9.0% (16/178).

## Overtime

Offensive scrimmage plays: 12. Early-down pass rate: 54.5% (6/11). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 57.9% (132/228) across 5 games (COMPLETE). Earlier games: 61.4% (89/145). Difference: -0.035.
Last 8 early-down pass rate: 59.2% (221/373) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| D.Metcalf | 64 | 0.239 | 8 |
| G.Bernard | 42 | 0.157 | 7 |
| J.Warren | 36 | 0.134 | 8 |
| P.Freiermuth | 35 | 0.131 | 8 |
| D.Washington | 28 | 0.104 | 8 |
| R.Wilson | 25 | 0.093 | 5 |
| R.Dowdle | 17 | 0.063 | 4 |
| M.Pittman | 12 | 0.045 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Warren | 119 | 0.650 | 8 |
| R.Dowdle | 46 | 0.251 | 5 |
| T.Homer | 5 | 0.027 | 3 |
| A.Rodgers | 4 | 0.022 | 4 |
| P.Freiermuth | 4 | 0.022 | 4 |

## Gamebook checks


Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
