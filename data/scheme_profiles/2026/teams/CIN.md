# CIN scheme and opportunity profile, 2026

Cincinnati Bengals. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_CIN_ATL on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [6].

Game ids: 2026_01_TB_CIN, 2026_02_CIN_HOU, 2026_03_CIN_PIT, 2026_04_JAX_CIN, 2026_05_CIN_MIA, 2026_07_CIN_BAL, 2026_08_TEN_CIN, 2026_09_CIN_ATL.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 478. Early-down pass rate: 60.6% (228/376). Early-down run rate: 39.4% (148/376).
Neutral pass rate (margin -7 to +7): 66.7% (206/309). Leading by 8+: 52.3% (58/111). Trailing by 8+: 74.1% (43/58). Tied: 64.0% (48/75).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 42.1% (24/57). Long-yardage pass rate (7+ yards to go): 67.3% (226/336).
Third down: 53.6% (52/97). Unknown third-down results: 0.
Red-zone plays: 79. Red-zone pass rate: 55.7% (44/79). Derived red-zone drive touchdown rate: 70.0% (21/30). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 8.5% (26/307); rush 10+ 10.5% (18/171); rush 15+ 2.3% (4/171). Official explosive label: unknown.
Sacks taken: 15. Scrambles: 9 (2.8% (9/316) of dropbacks). Kneels, excluded from carries: 5.
Shotgun rate, where the flag is present: 75.9% (363/478). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 64, middle 64, right 43, unknown 0.

## Defense, regulation

Scrimmage plays faced: 484. Early-down pass rate allowed: 54.8% (206/376).
Third down allowed: 48.0% (48/100). Sacks recorded: 23. Scrambles allowed: 20.
Explosive passes allowed (20+): 9.0% (26/289). Explosive rushes allowed (10+): 14.9% (29/195).

## Overtime

Offensive scrimmage plays: 5. Early-down pass rate: 80.0% (4/5). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 62.6% (152/243) across 5 games (COMPLETE). Earlier games: 57.1% (76/133). Difference: +0.054.
Last 8 early-down pass rate: 60.6% (228/376) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| J.Chase | 73 | 0.253 | 8 |
| T.Higgins | 67 | 0.232 | 8 |
| C.Brown | 45 | 0.156 | 8 |
| D.Meyers | 26 | 0.090 | 8 |
| M.Gesicki | 26 | 0.090 | 7 |
| S.Perine | 11 | 0.038 | 6 |
| E.All | 9 | 0.031 | 3 |
| M.Tinsley | 9 | 0.031 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| C.Brown | 103 | 0.599 | 8 |
| S.Perine | 46 | 0.267 | 8 |
| J.Burrow | 18 | 0.105 | 7 |
| T.Brooks | 3 | 0.017 | 1 |
| D.Meyers | 2 | 0.012 | 2 |

## Gamebook checks

- 2026_09_CIN_ATL: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224918/gamecenter/ab380bc7-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
