# LAC scheme and opportunity profile, 2026

Los Angeles Chargers. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_HOU_LAC on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [7].

Game ids: 2026_01_ARI_LAC, 2026_02_LV_LAC, 2026_03_LAC_BUF, 2026_04_LAC_SEA, 2026_05_DEN_LAC, 2026_06_LAC_KC, 2026_08_LAC_LA, 2026_09_HOU_LAC.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 496. Early-down pass rate: 46.4% (170/366). Early-down run rate: 53.6% (196/366).
Neutral pass rate (margin -7 to +7): 49.0% (150/306). Leading by 8+: 60.0% (6/10). Trailing by 8+: 64.4% (116/180). Tied: 52.9% (46/87).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 44.7% (17/38). Long-yardage pass rate (7+ yards to go): 54.7% (205/375).
Third down: 34.2% (39/114). Unknown third-down results: 0.
Red-zone plays: 59. Red-zone pass rate: 49.2% (29/59). Derived red-zone drive touchdown rate: 50.0% (9/18). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 6.6% (18/272); rush 10+ 9.4% (21/224); rush 15+ 3.6% (8/224). Official explosive label: unknown.
Sacks taken: 31. Scrambles: 23 (7.8% (23/295) of dropbacks). Kneels, excluded from carries: 0.
Shotgun rate, where the flag is present: 67.3% (334/496). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 79, middle 72, right 71, unknown 2.

## Defense, regulation

Scrimmage plays faced: 473. Early-down pass rate allowed: 46.3% (171/369).
Third down allowed: 34.3% (34/99). Sacks recorded: 13. Scrambles allowed: 9.
Explosive passes allowed (20+): 9.3% (23/246). Explosive rushes allowed (10+): 11.0% (25/227).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 46.5% (107/230) across 5 games (COMPLETE). Earlier games: 46.3% (63/136). Difference: +0.002.
Last 8 early-down pass rate: 46.4% (170/366) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| T.Harris | 35 | 0.150 | 7 |
| Q.Johnston | 30 | 0.128 | 7 |
| O.Gadsden | 29 | 0.124 | 8 |
| L.McConkey | 24 | 0.103 | 6 |
| K.Mitchell | 22 | 0.094 | 7 |
| C.Kolar | 20 | 0.085 | 5 |
| K.Vidal | 17 | 0.073 | 6 |
| K.Lambert-Smith | 13 | 0.056 | 2 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| O.Hampton | 102 | 0.455 | 8 |
| K.Mitchell | 46 | 0.205 | 8 |
| K.Vidal | 36 | 0.161 | 6 |
| J.Herbert | 34 | 0.152 | 8 |
| Q.Johnston | 3 | 0.013 | 3 |

## Gamebook checks

- 2026_09_HOU_LAC: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794257318/gamecenter/ab580cb7-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
