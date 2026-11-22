# DAL scheme and opportunity profile, 2026

Dallas Cowboys. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_DAL_IND on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_DAL_NYG, 2026_02_WAS_DAL, 2026_03_BAL_DAL, 2026_04_DAL_HOU, 2026_05_TB_DAL, 2026_06_DAL_GB, 2026_07_DAL_PHI, 2026_08_ARI_DAL, 2026_09_DAL_IND.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 578. Early-down pass rate: 56.0% (252/450). Early-down run rate: 44.0% (198/450).
Neutral pass rate (margin -7 to +7): 58.8% (243/413). Leading by 8+: 36.0% (18/50). Trailing by 8+: 75.7% (87/115). Tied: 58.2% (53/91).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 39.4% (28/71). Long-yardage pass rate (7+ yards to go): 62.8% (246/392).
Third down: 45.7% (53/116). Unknown third-down results: 0.
Red-zone plays: 114. Red-zone pass rate: 49.1% (56/114). Derived red-zone drive touchdown rate: 67.6% (25/37). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 8.0% (28/348); rush 10+ 8.7% (20/230); rush 15+ 3.0% (7/230). Official explosive label: unknown.
Sacks taken: 13. Scrambles: 18 (4.9% (18/366) of dropbacks). Kneels, excluded from carries: 2.
Shotgun rate, where the flag is present: 63.8% (369/578). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 82, middle 87, right 60, unknown 1.

## Defense, regulation

Scrimmage plays faced: 557. Early-down pass rate allowed: 49.0% (213/435).
Third down allowed: 48.7% (56/115). Sacks recorded: 16. Scrambles allowed: 23.
Explosive passes allowed (20+): 9.2% (28/304). Explosive rushes allowed (10+): 10.7% (27/253).

## Overtime

Offensive scrimmage plays: 3. Early-down pass rate: 50.0% (1/2). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 55.6% (140/252) across 5 games (COMPLETE). Earlier games: 56.6% (112/198). Difference: -0.010.
Last 8 early-down pass rate: 55.5% (227/409) across 8 games. Difference versus earlier: -0.055.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| C.Lamb | 108 | 0.329 | 9 |
| G.Pickens | 62 | 0.189 | 8 |
| R.Flournoy | 47 | 0.143 | 9 |
| J.Williams | 29 | 0.088 | 8 |
| J.Ferguson | 27 | 0.082 | 8 |
| B.Spann-Ford | 21 | 0.064 | 8 |
| J.Mingo | 11 | 0.034 | 5 |
| T.Goodson | 8 | 0.024 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Williams | 154 | 0.667 | 9 |
| T.Goodson | 40 | 0.173 | 6 |
| D.Prescott | 23 | 0.100 | 8 |
| E.Demercado | 5 | 0.022 | 2 |
| H.Luepke | 4 | 0.017 | 4 |

## Gamebook checks

- 2026_09_DAL_IND: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224921/gamecenter/ab38123a-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
