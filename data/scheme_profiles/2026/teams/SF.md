# SF scheme and opportunity profile, 2026

San Francisco 49ers. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_LV_SF on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [8].

Game ids: 2026_01_SF_LA, 2026_02_MIA_SF, 2026_03_ARI_SF, 2026_04_DEN_SF, 2026_05_SF_SEA, 2026_06_WAS_SF, 2026_07_SF_ATL, 2026_09_LV_SF.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 466. Early-down pass rate: 48.8% (179/367). Early-down run rate: 51.2% (188/367).
Neutral pass rate (margin -7 to +7): 50.7% (153/302). Leading by 8+: 48.9% (67/137). Trailing by 8+: 81.5% (22/27). Tied: 54.1% (59/109).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 28.4% (19/67). Long-yardage pass rate (7+ yards to go): 55.4% (170/307).
Third down: 51.7% (46/89). Unknown third-down results: 0.
Red-zone plays: 86. Red-zone pass rate: 46.5% (40/86). Derived red-zone drive touchdown rate: 85.2% (23/27). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 11.2% (27/242); rush 10+ 14.3% (32/224); rush 15+ 4.9% (11/224). Official explosive label: unknown.
Sacks taken: 8. Scrambles: 19 (7.3% (19/261) of dropbacks). Kneels, excluded from carries: 10.
Shotgun rate, where the flag is present: 48.5% (226/466). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 73, middle 91, right 60, unknown 0.

## Defense, regulation

Scrimmage plays faced: 480. Early-down pass rate allowed: 55.5% (202/364).
Third down allowed: 40.4% (42/104). Sacks recorded: 15. Scrambles allowed: 9.
Explosive passes allowed (20+): 6.2% (18/291). Explosive rushes allowed (10+): 2.6% (5/189).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 50.9% (119/234) across 5 games (COMPLETE). Earlier games: 45.1% (60/133). Difference: +0.057.
Last 8 early-down pass rate: 48.8% (179/367) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| G.Kittle | 53 | 0.232 | 8 |
| C.McCaffrey | 45 | 0.197 | 8 |
| M.Evans | 39 | 0.171 | 6 |
| D.Samuel | 20 | 0.088 | 4 |
| J.Watkins | 13 | 0.057 | 4 |
| J.Cowing | 11 | 0.048 | 5 |
| K.Juszczyk | 11 | 0.048 | 5 |
| B.Cooks | 10 | 0.044 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| C.McCaffrey | 102 | 0.455 | 8 |
| K.Black | 68 | 0.304 | 8 |
| B.Purdy | 34 | 0.152 | 8 |
| D.Samuel | 9 | 0.040 | 5 |
| J.James | 8 | 0.036 | 3 |

## Gamebook checks

- 2026_09_LV_SF: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224923/gamecenter/ab581766-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
