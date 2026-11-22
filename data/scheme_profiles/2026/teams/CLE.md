# CLE scheme and opportunity profile, 2026

Cleveland Browns. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_CLE_NO on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_CLE_JAX, 2026_02_CLE_TB, 2026_03_CAR_CLE, 2026_04_PIT_CLE, 2026_05_CLE_NYJ, 2026_06_BAL_CLE, 2026_07_CLE_TEN, 2026_08_CLE_PIT, 2026_09_CLE_NO.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 537. Early-down pass rate: 55.0% (224/407). Early-down run rate: 45.0% (183/407).
Neutral pass rate (margin -7 to +7): 56.5% (213/377). Leading by 8+: 40.9% (9/22). Trailing by 8+: 65.2% (90/138). Tied: 55.4% (77/139).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 28.6% (14/49). Long-yardage pass rate (7+ yards to go): 62.0% (238/384).
Third down: 33.1% (39/118). Unknown third-down results: 0.
Red-zone plays: 65. Red-zone pass rate: 47.7% (31/65). Derived red-zone drive touchdown rate: 42.9% (9/21). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 8.7% (27/312); rush 10+ 8.0% (18/225); rush 15+ 4.0% (9/225). Official explosive label: unknown.
Sacks taken: 38. Scrambles: 31 (9.0% (31/343) of dropbacks). Kneels, excluded from carries: 8.
Shotgun rate, where the flag is present: 76.9% (413/537). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 93, middle 56, right 74, unknown 2.

## Defense, regulation

Scrimmage plays faced: 553. Early-down pass rate allowed: 52.5% (222/423).
Third down allowed: 37.9% (47/124). Sacks recorded: 26. Scrambles allowed: 13.
Explosive passes allowed (20+): 8.3% (26/315). Explosive rushes allowed (10+): 15.5% (37/238).

## Overtime

Offensive scrimmage plays: 8. Early-down pass rate: 100.0% (6/6). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 54.2% (128/236) across 5 games (COMPLETE). Earlier games: 56.1% (96/171). Difference: -0.019.
Last 8 early-down pass rate: 55.2% (203/368) across 8 games. Difference versus earlier: +0.013.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| D.Boston | 60 | 0.217 | 9 |
| K.Concepcion | 55 | 0.199 | 9 |
| H.Fannin | 53 | 0.192 | 9 |
| J.Jeudy | 28 | 0.101 | 8 |
| Q.Judkins | 24 | 0.087 | 8 |
| D.Sampson | 17 | 0.062 | 3 |
| R.Sanders | 12 | 0.043 | 5 |
| I.Bond | 9 | 0.033 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| Q.Judkins | 116 | 0.516 | 8 |
| D.Watson | 44 | 0.196 | 8 |
| D.Sampson | 15 | 0.067 | 3 |
| J.McLaughlin | 11 | 0.049 | 3 |
| K.Concepcion | 10 | 0.044 | 5 |

## Gamebook checks

- 2026_09_CLE_NO: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794257318/gamecenter/ab381d58-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
