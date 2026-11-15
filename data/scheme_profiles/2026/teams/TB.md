# TB scheme and opportunity profile, 2026

Tampa Bay Buccaneers. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_TB_CHI on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_TB_CIN, 2026_02_CLE_TB, 2026_03_MIN_TB, 2026_04_GB_TB, 2026_05_TB_DAL, 2026_06_PIT_TB, 2026_07_TB_CAR, 2026_08_ATL_TB, 2026_09_TB_CHI.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 545. Early-down pass rate: 41.4% (171/413). Early-down run rate: 58.6% (242/413).
Neutral pass rate (margin -7 to +7): 52.9% (165/312). Leading by 8+: 27.2% (34/125). Trailing by 8+: 55.6% (60/108). Tied: 50.9% (55/108).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 34.5% (19/55). Long-yardage pass rate (7+ yards to go): 50.4% (200/397).
Third down: 36.9% (45/122). Unknown third-down results: 0.
Red-zone plays: 93. Red-zone pass rate: 41.9% (39/93). Derived red-zone drive touchdown rate: 50.0% (15/30). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 6.2% (16/259); rush 10+ 12.9% (37/286); rush 15+ 4.9% (14/286). Official explosive label: unknown.
Sacks taken: 26. Scrambles: 25 (8.8% (25/284) of dropbacks). Kneels, excluded from carries: 6.
Shotgun rate, where the flag is present: 63.1% (344/545). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 120, middle 52, right 110, unknown 4.

## Defense, regulation

Scrimmage plays faced: 502. Early-down pass rate allowed: 59.5% (223/375).
Third down allowed: 33.6% (38/113). Sacks recorded: 17. Scrambles allowed: 12.
Explosive passes allowed (20+): 6.7% (21/315). Explosive rushes allowed (10+): 8.6% (16/187).

## Overtime

Offensive scrimmage plays: 10. Early-down pass rate: 83.3% (5/6). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 32.2% (76/236) across 5 games (COMPLETE). Earlier games: 53.7% (95/177). Difference: -0.215.
Last 8 early-down pass rate: 39.8% (148/372) across 8 games. Difference versus earlier: -0.163.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| E.Egbuka | 54 | 0.234 | 7 |
| C.Godwin | 38 | 0.165 | 9 |
| C.Otton | 38 | 0.165 | 8 |
| B.Irving | 28 | 0.121 | 7 |
| T.Hurst | 25 | 0.108 | 8 |
| K.Gainwell | 21 | 0.091 | 8 |
| T.Johnson | 20 | 0.087 | 8 |
| K.Johnson | 2 | 0.009 | 1 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| B.Irving | 167 | 0.580 | 9 |
| K.Gainwell | 63 | 0.219 | 9 |
| J.Daniels | 18 | 0.062 | 4 |
| B.Mayfield | 15 | 0.052 | 6 |
| S.Tucker | 15 | 0.052 | 3 |

## Gamebook checks

- 2026_09_TB_CHI: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224924/gamecenter/ab582247-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
