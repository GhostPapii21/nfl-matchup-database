# WAS scheme and opportunity profile, 2026

Washington Commanders. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_10_WAS_NYG on 2026-11-12. Last fully completed week is 9. Bye weeks inside weeks 1-9: [7].

Game ids: 2026_01_WAS_PHI, 2026_02_WAS_DAL, 2026_03_SEA_WAS, 2026_04_IND_WAS, 2026_05_NYG_WAS, 2026_06_WAS_SF, 2026_08_PHI_WAS, 2026_09_LA_WAS, 2026_10_WAS_NYG.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 543. Early-down pass rate: 51.3% (211/411). Early-down run rate: 48.7% (200/411).
Neutral pass rate (margin -7 to +7): 56.2% (223/397). Leading by 8+: 0.0% (0/3). Trailing by 8+: 60.8% (87/143). Tied: 51.6% (49/95).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 45.9% (28/61). Long-yardage pass rate (7+ yards to go): 57.5% (222/386).
Third down: 33.6% (40/119). Unknown third-down results: 0.
Red-zone plays: 65. Red-zone pass rate: 50.8% (33/65). Derived red-zone drive touchdown rate: 59.1% (13/22). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 9.4% (29/310); rush 10+ 9.0% (21/233); rush 15+ 4.7% (11/233). Official explosive label: unknown.
Sacks taken: 20. Scrambles: 33 (9.6% (33/343) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 72.7% (395/543). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 68, middle 58, right 106, unknown 1.

## Defense, regulation

Scrimmage plays faced: 564. Early-down pass rate allowed: 56.6% (246/435).
Third down allowed: 38.1% (45/118). Sacks recorded: 18. Scrambles allowed: 23.
Explosive passes allowed (20+): 8.3% (28/339). Explosive rushes allowed (10+): 8.0% (18/225).

## Overtime

Offensive scrimmage plays: 10. Early-down pass rate: 66.7% (6/9). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 53.0% (115/217) across 5 games (COMPLETE). Earlier games: 49.5% (96/194). Difference: +0.035.
Last 8 early-down pass rate: 51.8% (187/361) across 8 games. Difference versus earlier: +0.038.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| S.Diggs | 59 | 0.210 | 8 |
| A.Williams | 41 | 0.146 | 9 |
| C.Okonkwo | 39 | 0.139 | 7 |
| T.McLaurin | 27 | 0.096 | 5 |
| T.Burks | 25 | 0.089 | 7 |
| R.White | 23 | 0.082 | 8 |
| D.Brown | 16 | 0.057 | 6 |
| A.Ekeler | 12 | 0.043 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Croskey-Merritt | 67 | 0.284 | 5 |
| R.White | 65 | 0.275 | 8 |
| J.Daniels | 37 | 0.157 | 7 |
| A.Ekeler | 33 | 0.140 | 6 |
| K.Allen | 12 | 0.051 | 3 |

## Gamebook checks

- 2026_09_LA_WAS: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224919/gamecenter/ab382331-4feb-11f1-abca-2c54536568a9.pdf
- 2026_10_WAS_NYG: VERIFIED_NOT_PERSISTED. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794570519/gamecenter/ab5828d9-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
