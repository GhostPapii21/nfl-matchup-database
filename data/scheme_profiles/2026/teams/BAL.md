# BAL scheme and opportunity profile, 2026

Baltimore Ravens. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_JAX_BAL on 2026-11-05. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_BAL_IND, 2026_02_NO_BAL, 2026_03_BAL_DAL, 2026_04_TEN_BAL, 2026_05_BAL_ATL, 2026_06_BAL_CLE, 2026_07_CIN_BAL, 2026_08_BAL_BUF, 2026_09_JAX_BAL.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 512. Early-down pass rate: 45.3% (179/395). Early-down run rate: 54.7% (216/395).
Neutral pass rate (margin -7 to +7): 51.0% (149/292). Leading by 8+: 53.2% (66/124). Trailing by 8+: 50.0% (48/96). Tied: 50.0% (34/68).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 15.7% (8/51). Long-yardage pass rate (7+ yards to go): 54.2% (189/349).
Third down: 36.7% (40/109). Unknown third-down results: 0.
Red-zone plays: 79. Red-zone pass rate: 41.8% (33/79). Derived red-zone drive touchdown rate: 57.7% (15/26). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.6% (20/263); rush 10+ 12.0% (30/249); rush 15+ 5.6% (14/249). Official explosive label: unknown.
Sacks taken: 23. Scrambles: 20 (7.1% (20/283) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 61.3% (314/512). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 103, middle 34, right 108, unknown 4.

## Defense, regulation

Scrimmage plays faced: 547. Early-down pass rate allowed: 49.9% (207/415).
Third down allowed: 39.0% (46/118). Sacks recorded: 17. Scrambles allowed: 22.
Explosive passes allowed (20+): 8.3% (25/302). Explosive rushes allowed (10+): 6.9% (17/245).

## Overtime

Offensive scrimmage plays: 14. Early-down pass rate: 25.0% (3/12). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 47.8% (97/203) across 5 games (COMPLETE). Earlier games: 42.7% (82/192). Difference: +0.051.
Last 8 early-down pass rate: 46.5% (160/344) across 8 games. Difference versus earlier: +0.093.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| Z.Flowers | 64 | 0.267 | 8 |
| M.Andrews | 43 | 0.179 | 9 |
| R.Bateman | 31 | 0.129 | 9 |
| J.Hill | 28 | 0.117 | 8 |
| D.Henry | 14 | 0.058 | 8 |
| J.Lane | 14 | 0.058 | 4 |
| J.Cuevas | 13 | 0.054 | 5 |
| D.Walker | 9 | 0.037 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| D.Henry | 175 | 0.678 | 9 |
| J.Hill | 33 | 0.128 | 8 |
| L.Jackson | 16 | 0.062 | 4 |
| T.Huntley | 15 | 0.058 | 4 |
| R.Ali | 6 | 0.023 | 2 |

## Gamebook checks

- 2026_09_JAX_BAL: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1793965716/gamecenter/ab380826-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
