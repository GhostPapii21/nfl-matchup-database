# PHI scheme and opportunity profile, 2026

Philadelphia Eagles. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_NYG_PHI on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_WAS_PHI, 2026_02_PHI_TEN, 2026_03_PHI_CHI, 2026_04_LA_PHI, 2026_05_PHI_JAX, 2026_06_CAR_PHI, 2026_07_DAL_PHI, 2026_08_PHI_WAS, 2026_09_NYG_PHI.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 543. Early-down pass rate: 54.8% (218/398). Early-down run rate: 45.2% (180/398).
Neutral pass rate (margin -7 to +7): 58.7% (249/424). Leading by 8+: 23.8% (5/21). Trailing by 8+: 79.6% (78/98). Tied: 55.4% (51/92).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 39.1% (18/46). Long-yardage pass rate (7+ yards to go): 63.2% (249/394).
Third down: 35.9% (46/128). Unknown third-down results: 0.
Red-zone plays: 63. Red-zone pass rate: 33.3% (21/63). Derived red-zone drive touchdown rate: 72.7% (16/22). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 4.2% (14/332); rush 10+ 7.6% (16/211); rush 15+ 4.3% (9/211). Official explosive label: unknown.
Sacks taken: 30. Scrambles: 23 (6.5% (23/355) of dropbacks). Kneels, excluded from carries: 2.
Shotgun rate, where the flag is present: 72.7% (395/543). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 76, middle 52, right 81, unknown 2.

## Defense, regulation

Scrimmage plays faced: 586. Early-down pass rate allowed: 50.5% (221/438).
Third down allowed: 40.6% (54/133). Sacks recorded: 16. Scrambles allowed: 18.
Explosive passes allowed (20+): 9.8% (31/316). Explosive rushes allowed (10+): 10.0% (27/270).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 60.0% (138/230) across 5 games (COMPLETE). Earlier games: 47.6% (80/168). Difference: +0.124.
Last 8 early-down pass rate: 55.7% (201/361) across 8 games. Difference versus earlier: +0.097.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| M.Lemon | 54 | 0.189 | 9 |
| D.Goedert | 41 | 0.144 | 7 |
| D.Smith | 41 | 0.144 | 4 |
| D.Cooper | 32 | 0.112 | 7 |
| D.Wicks | 32 | 0.112 | 6 |
| E.Mitchell | 14 | 0.049 | 3 |
| D.Pierce | 11 | 0.039 | 3 |
| S.Barkley | 11 | 0.039 | 7 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| S.Barkley | 69 | 0.327 | 7 |
| D.Pierce | 37 | 0.175 | 3 |
| T.Bigsby | 28 | 0.133 | 3 |
| J.Hurts | 21 | 0.100 | 5 |
| W.Shipley | 20 | 0.095 | 4 |

## Gamebook checks

- 2026_09_NYG_PHI: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224920/gamecenter/ab38203e-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
