# LA scheme and opportunity profile, 2026

Los Angeles Rams. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_LA_WAS on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_SF_LA, 2026_02_NYG_LA, 2026_03_LA_DEN, 2026_04_LA_PHI, 2026_05_BUF_LA, 2026_06_ARI_LA, 2026_07_LA_LV, 2026_08_LAC_LA, 2026_09_LA_WAS.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 585. Early-down pass rate: 56.9% (264/464). Early-down run rate: 43.1% (200/464).
Neutral pass rate (margin -7 to +7): 64.3% (241/375). Leading by 8+: 46.7% (63/135). Trailing by 8+: 65.3% (49/75). Tied: 63.2% (60/95).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 39.7% (27/68). Long-yardage pass rate (7+ yards to go): 62.4% (251/402).
Third down: 40.4% (44/109). Unknown third-down results: 0.
Red-zone plays: 98. Red-zone pass rate: 56.1% (55/98). Derived red-zone drive touchdown rate: 66.7% (24/36). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 6.2% (22/353); rush 10+ 10.3% (24/232); rush 15+ 5.2% (12/232). Official explosive label: unknown.
Sacks taken: 13. Scrambles: 6 (1.7% (6/359) of dropbacks). Kneels, excluded from carries: 8.
Shotgun rate, where the flag is present: 51.6% (302/585). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 65, middle 103, right 64, unknown 0.

## Defense, regulation

Scrimmage plays faced: 535. Early-down pass rate allowed: 50.2% (205/408).
Third down allowed: 31.6% (36/114). Sacks recorded: 16. Scrambles allowed: 18.
Explosive passes allowed (20+): 6.6% (20/305). Explosive rushes allowed (10+): 8.7% (20/230).

## Overtime

Offensive scrimmage plays: 7. Early-down pass rate: 83.3% (5/6). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 55.2% (139/252) across 5 games (COMPLETE). Earlier games: 59.0% (125/212). Difference: -0.038.
Last 8 early-down pass rate: 58.1% (244/420) across 8 games. Difference versus earlier: +0.126.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| P.Nacua | 93 | 0.276 | 7 |
| D.Adams | 49 | 0.145 | 6 |
| K.Williams | 46 | 0.136 | 9 |
| T.Higbee | 39 | 0.116 | 8 |
| C.Parkinson | 23 | 0.068 | 7 |
| K.Mumpfield | 23 | 0.068 | 8 |
| B.Corum | 17 | 0.050 | 8 |
| D.Allen | 16 | 0.047 | 7 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| K.Williams | 127 | 0.543 | 9 |
| B.Corum | 86 | 0.368 | 9 |
| M.Stafford | 7 | 0.030 | 5 |
| P.Nacua | 7 | 0.030 | 4 |
| R.Rivers | 5 | 0.021 | 1 |

## Gamebook checks

- 2026_09_LA_WAS: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224919/gamecenter/ab382331-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
