# CAR scheme and opportunity profile, 2026

Carolina Panthers. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_DEN_CAR on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [5].

Game ids: 2026_01_CHI_CAR, 2026_02_CAR_ATL, 2026_03_CAR_CLE, 2026_04_DET_CAR, 2026_06_CAR_PHI, 2026_07_TB_CAR, 2026_08_CAR_GB, 2026_09_DEN_CAR.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 521. Early-down pass rate: 62.0% (246/397). Early-down run rate: 38.0% (151/397).
Neutral pass rate (margin -7 to +7): 64.1% (193/301). Leading by 8+: 54.7% (35/64). Trailing by 8+: 69.9% (109/156). Tied: 66.7% (42/63).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 46.6% (27/58). Long-yardage pass rate (7+ yards to go): 67.3% (265/394).
Third down: 37.7% (40/106). Unknown third-down results: 0.
Red-zone plays: 79. Red-zone pass rate: 60.8% (48/79). Derived red-zone drive touchdown rate: 67.9% (19/28). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 8.3% (28/337); rush 10+ 12.0% (22/184); rush 15+ 4.9% (9/184). Official explosive label: unknown.
Sacks taken: 26. Scrambles: 9 (2.6% (9/346) of dropbacks). Kneels, excluded from carries: 5.
Shotgun rate, where the flag is present: 65.6% (342/521). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 83, middle 46, right 55, unknown 0.

## Defense, regulation

Scrimmage plays faced: 516. Early-down pass rate allowed: 51.8% (206/398).
Third down allowed: 47.7% (51/107). Sacks recorded: 12. Scrambles allowed: 16.
Explosive passes allowed (20+): 4.8% (14/290). Explosive rushes allowed (10+): 10.6% (24/226).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 62.3% (154/247) across 5 games (COMPLETE). Earlier games: 61.3% (92/150). Difference: +0.010.
Last 8 early-down pass rate: 62.0% (246/397) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| T.McMillan | 71 | 0.251 | 8 |
| J.Coker | 49 | 0.173 | 7 |
| D.Waller | 35 | 0.124 | 8 |
| C.Hubbard | 31 | 0.110 | 8 |
| T.Tremble | 30 | 0.106 | 8 |
| J.Metchie | 22 | 0.078 | 6 |
| M.Evans | 14 | 0.049 | 8 |
| B.Tremayne | 12 | 0.042 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| C.Hubbard | 134 | 0.728 | 8 |
| A.Dillon | 17 | 0.092 | 4 |
| T.Etienne | 10 | 0.054 | 4 |
| J.Brooks | 9 | 0.049 | 2 |
| B.Young | 7 | 0.038 | 6 |

## Gamebook checks

- 2026_09_DEN_CAR: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224920/gamecenter/ab380efd-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
