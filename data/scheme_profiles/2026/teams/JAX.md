# JAX scheme and opportunity profile, 2026

Jacksonville Jaguars. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_JAX_BAL on 2026-11-05. Last fully completed week is 9. Bye weeks inside weeks 1-9: [7].

Game ids: 2026_01_CLE_JAX, 2026_02_JAX_DEN, 2026_03_NE_JAX, 2026_04_JAX_CIN, 2026_05_PHI_JAX, 2026_06_HOU_JAX, 2026_08_IND_JAX, 2026_09_JAX_BAL.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 462. Early-down pass rate: 48.5% (175/361). Early-down run rate: 51.5% (186/361).
Neutral pass rate (margin -7 to +7): 56.0% (178/318). Leading by 8+: 39.7% (50/126). Trailing by 8+: 61.1% (11/18). Tied: 53.9% (62/115).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 31.2% (15/48). Long-yardage pass rate (7+ yards to go): 55.2% (186/337).
Third down: 46.4% (45/97). Unknown third-down results: 0.
Red-zone plays: 78. Red-zone pass rate: 52.6% (41/78). Derived red-zone drive touchdown rate: 65.2% (15/23). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 11.3% (27/239); rush 10+ 9.0% (20/223); rush 15+ 3.6% (8/223). Official explosive label: unknown.
Sacks taken: 13. Scrambles: 9 (3.6% (9/248) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 54.3% (251/462). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 88, middle 51, right 84, unknown 0.

## Defense, regulation

Scrimmage plays faced: 466. Early-down pass rate allowed: 56.0% (202/361).
Third down allowed: 34.0% (32/94). Sacks recorded: 16. Scrambles allowed: 14.
Explosive passes allowed (20+): 7.6% (21/277). Explosive rushes allowed (10+): 6.3% (12/189).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 47.6% (108/227) across 5 games (COMPLETE). Earlier games: 50.0% (67/134). Difference: -0.024.
Last 8 early-down pass rate: 48.5% (175/361) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| P.Washington | 55 | 0.249 | 8 |
| B.Strange | 37 | 0.167 | 8 |
| J.Meyers | 37 | 0.167 | 8 |
| Bri.Thomas | 21 | 0.095 | 7 |
| B.Tuten | 16 | 0.072 | 7 |
| J.Cameron | 14 | 0.063 | 6 |
| N.Boerkircher | 12 | 0.054 | 7 |
| L.Allen | 8 | 0.036 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| B.Tuten | 122 | 0.547 | 8 |
| C.Rodriguez | 55 | 0.247 | 8 |
| A.Abdullah | 23 | 0.103 | 5 |
| T.Lawrence | 17 | 0.076 | 7 |
| P.Washington | 2 | 0.009 | 2 |

## Gamebook checks

- 2026_09_JAX_BAL: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1793965716/gamecenter/ab380826-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
