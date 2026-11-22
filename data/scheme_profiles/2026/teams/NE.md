# NE scheme and opportunity profile, 2026

New England Patriots. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_GB_NE on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_NE_SEA, 2026_02_PIT_NE, 2026_03_NE_JAX, 2026_04_NE_BUF, 2026_05_LV_NE, 2026_06_NYJ_NE, 2026_07_NE_CHI, 2026_08_NE_MIA, 2026_09_GB_NE.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 545. Early-down pass rate: 50.5% (215/426). Early-down run rate: 49.5% (211/426).
Neutral pass rate (margin -7 to +7): 52.4% (183/349). Leading by 8+: 47.8% (32/67). Trailing by 8+: 65.9% (85/129). Tied: 48.7% (56/115).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 32.1% (18/56). Long-yardage pass rate (7+ yards to go): 58.2% (230/395).
Third down: 40.4% (44/109). Unknown third-down results: 0.
Red-zone plays: 67. Red-zone pass rate: 59.7% (40/67). Derived red-zone drive touchdown rate: 56.0% (14/25). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 11.0% (33/300); rush 10+ 12.2% (30/245); rush 15+ 4.9% (12/245). Official explosive label: unknown.
Sacks taken: 20. Scrambles: 28 (8.5% (28/328) of dropbacks). Kneels, excluded from carries: 11.
Shotgun rate, where the flag is present: 59.8% (326/545). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 78, middle 96, right 69, unknown 2.

## Defense, regulation

Scrimmage plays faced: 532. Early-down pass rate allowed: 54.2% (224/413).
Third down allowed: 37.6% (41/109). Sacks recorded: 25. Scrambles allowed: 11.
Explosive passes allowed (20+): 10.3% (32/310). Explosive rushes allowed (10+): 9.9% (22/222).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 52.6% (123/234) across 5 games (COMPLETE). Earlier games: 47.9% (92/192). Difference: +0.046.
Last 8 early-down pass rate: 50.9% (192/377) across 8 games. Difference versus earlier: +0.040.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| D.Douglas | 46 | 0.174 | 9 |
| H.Henry | 37 | 0.140 | 9 |
| R.Stevenson | 31 | 0.117 | 8 |
| E.Raridon | 26 | 0.098 | 8 |
| M.Hollins | 26 | 0.098 | 5 |
| E.Chism | 25 | 0.095 | 8 |
| R.Doubs | 24 | 0.091 | 6 |
| A.Brown | 20 | 0.076 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| R.Stevenson | 102 | 0.416 | 9 |
| T.Henderson | 52 | 0.212 | 6 |
| C.Kiner | 50 | 0.204 | 8 |
| D.Maye | 36 | 0.147 | 9 |
| L.Larison | 3 | 0.012 | 2 |

## Gamebook checks

- 2026_09_GB_NE: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224923/gamecenter/ab581b93-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
