# LV scheme and opportunity profile, 2026

Las Vegas Raiders. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_LV_SF on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_MIA_LV, 2026_02_LV_LAC, 2026_03_LV_NO, 2026_04_KC_LV, 2026_05_LV_NE, 2026_06_BUF_LV, 2026_07_LA_LV, 2026_08_LV_NYJ, 2026_09_LV_SF.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 544. Early-down pass rate: 55.6% (233/419). Early-down run rate: 44.4% (186/419).
Neutral pass rate (margin -7 to +7): 58.4% (198/339). Leading by 8+: 34.3% (12/35). Trailing by 8+: 71.8% (122/170). Tied: 64.0% (71/111).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 24.1% (13/54). Long-yardage pass rate (7+ yards to go): 67.4% (261/387).
Third down: 43.8% (49/112). Unknown third-down results: 0.
Red-zone plays: 98. Red-zone pass rate: 54.1% (53/98). Derived red-zone drive touchdown rate: 54.3% (19/35). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 9.3% (31/332); rush 10+ 5.7% (12/212); rush 15+ 3.3% (7/212). Official explosive label: unknown.
Sacks taken: 11. Scrambles: 6 (1.8% (6/338) of dropbacks). Kneels, excluded from carries: 10.
Shotgun rate, where the flag is present: 56.1% (305/544). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 59, middle 89, right 64, unknown 0.

## Defense, regulation

Scrimmage plays faced: 557. Early-down pass rate allowed: 47.7% (211/442).
Third down allowed: 44.0% (48/109). Sacks recorded: 19. Scrambles allowed: 17.
Explosive passes allowed (20+): 9.1% (27/298). Explosive rushes allowed (10+): 14.7% (38/259).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 59.8% (131/219) across 5 games (COMPLETE). Earlier games: 51.0% (102/200). Difference: +0.088.
Last 8 early-down pass rate: 57.3% (211/368) across 8 games. Difference versus earlier: +0.142.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| B.Bowers | 69 | 0.222 | 7 |
| T.Tucker | 56 | 0.180 | 9 |
| A.Jeanty | 55 | 0.177 | 9 |
| M.Mayer | 46 | 0.148 | 9 |
| J.Nailor | 28 | 0.090 | 7 |
| C.White | 19 | 0.061 | 7 |
| M.Benson | 9 | 0.029 | 5 |
| J.Bech | 8 | 0.026 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| A.Jeanty | 114 | 0.538 | 9 |
| M.Washington | 71 | 0.335 | 9 |
| K.Cousins | 12 | 0.057 | 6 |
| C.Heyward | 5 | 0.024 | 4 |
| D.Laube | 5 | 0.024 | 2 |

## Gamebook checks

- 2026_09_LV_SF: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224923/gamecenter/ab581766-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
