# NYG scheme and opportunity profile, 2026

New York Giants. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_10_WAS_NYG on 2026-11-12. Last fully completed week is 9. Bye weeks inside weeks 1-9: [8].

Game ids: 2026_01_DAL_NYG, 2026_02_NYG_LA, 2026_03_TEN_NYG, 2026_04_ARI_NYG, 2026_05_NYG_WAS, 2026_06_NO_NYG, 2026_07_NYG_HOU, 2026_09_NYG_PHI, 2026_10_WAS_NYG.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 560. Early-down pass rate: 51.4% (222/432). Early-down run rate: 48.6% (210/432).
Neutral pass rate (margin -7 to +7): 54.9% (225/410). Leading by 8+: 29.0% (9/31). Trailing by 8+: 68.9% (82/119). Tied: 58.8% (70/119).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 18.2% (8/44). Long-yardage pass rate (7+ yards to go): 61.0% (263/431).
Third down: 38.5% (47/122). Unknown third-down results: 0.
Red-zone plays: 67. Red-zone pass rate: 46.3% (31/67). Derived red-zone drive touchdown rate: 63.0% (17/27). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 9.2% (29/316); rush 10+ 8.2% (20/244); rush 15+ 2.9% (7/244). Official explosive label: unknown.
Sacks taken: 28. Scrambles: 13 (4.0% (13/329) of dropbacks). Kneels, excluded from carries: 8.
Shotgun rate, where the flag is present: 63.8% (357/560). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 100, middle 73, right 71, unknown 0.

## Defense, regulation

Scrimmage plays faced: 524. Early-down pass rate allowed: 50.1% (202/403).
Third down allowed: 39.5% (45/114). Sacks recorded: 16. Scrambles allowed: 25.
Explosive passes allowed (20+): 6.8% (20/292). Explosive rushes allowed (10+): 12.1% (28/232).

## Overtime

Offensive scrimmage plays: 18. Early-down pass rate: 71.4% (10/14). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 57.3% (142/248) across 5 games (COMPLETE). Earlier games: 43.5% (80/184). Difference: +0.138.
Last 8 early-down pass rate: 52.5% (198/377) across 8 games. Difference versus earlier: +0.089.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| M.Nabers | 85 | 0.289 | 9 |
| I.Likely | 80 | 0.272 | 9 |
| M.Fields | 39 | 0.133 | 9 |
| D.Mooney | 31 | 0.105 | 9 |
| C.Skattebo | 17 | 0.058 | 6 |
| D.Singletary | 12 | 0.041 | 5 |
| T.Johnson | 12 | 0.041 | 5 |
| T.Tracy | 7 | 0.024 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| C.Skattebo | 116 | 0.462 | 7 |
| D.Singletary | 40 | 0.159 | 6 |
| N.Harris | 31 | 0.124 | 5 |
| T.Tracy | 19 | 0.076 | 6 |
| J.Winston | 17 | 0.068 | 7 |

## Gamebook checks

- 2026_09_NYG_PHI: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224920/gamecenter/ab38203e-4feb-11f1-abca-2c54536568a9.pdf
- 2026_10_WAS_NYG: VERIFIED_NOT_PERSISTED. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794570519/gamecenter/ab5828d9-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
