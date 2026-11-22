# DEN scheme and opportunity profile, 2026

Denver Broncos. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_DEN_CAR on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_DEN_KC, 2026_02_JAX_DEN, 2026_03_LA_DEN, 2026_04_DEN_SF, 2026_05_DEN_LAC, 2026_06_SEA_DEN, 2026_07_DEN_ARI, 2026_08_KC_DEN, 2026_09_DEN_CAR.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 509. Early-down pass rate: 52.8% (208/394). Early-down run rate: 47.2% (186/394).
Neutral pass rate (margin -7 to +7): 57.8% (211/365). Leading by 8+: 60.0% (27/45). Trailing by 8+: 60.6% (60/99). Tied: 61.9% (70/113).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 23.8% (10/42). Long-yardage pass rate (7+ yards to go): 59.8% (222/371).
Third down: 32.7% (36/110). Unknown third-down results: 0.
Red-zone plays: 77. Red-zone pass rate: 54.5% (42/77). Derived red-zone drive touchdown rate: 65.4% (17/26). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.0% (21/298); rush 10+ 7.1% (15/211); rush 15+ 2.8% (6/211). Official explosive label: unknown.
Sacks taken: 11. Scrambles: 7 (2.3% (7/305) of dropbacks). Kneels, excluded from carries: 9.
Shotgun rate, where the flag is present: 65.8% (335/509). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 69, middle 66, right 73, unknown 3.

## Defense, regulation

Scrimmage plays faced: 601. Early-down pass rate allowed: 56.7% (259/457).
Third down allowed: 41.1% (53/129). Sacks recorded: 26. Scrambles allowed: 18.
Explosive passes allowed (20+): 7.2% (26/361). Explosive rushes allowed (10+): 13.3% (32/240).

## Overtime

Offensive scrimmage plays: 3. Early-down pass rate: 0.0% (0/2). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 49.5% (110/222) across 5 games (COMPLETE). Earlier games: 57.0% (98/172). Difference: -0.074.
Last 8 early-down pass rate: 51.8% (187/361) across 8 games. Difference versus earlier: -0.118.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| J.Waddle | 52 | 0.201 | 9 |
| C.Sutton | 46 | 0.178 | 9 |
| E.Engram | 30 | 0.116 | 9 |
| R.Harvey | 28 | 0.108 | 6 |
| P.Bryant | 17 | 0.066 | 5 |
| M.Mims | 16 | 0.062 | 6 |
| T.Franklin | 15 | 0.058 | 8 |
| J.Coleman | 14 | 0.054 | 4 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Dobbins | 98 | 0.458 | 9 |
| J.Coleman | 47 | 0.220 | 4 |
| B.Nix | 28 | 0.131 | 9 |
| R.Harvey | 24 | 0.112 | 6 |
| T.Badie | 6 | 0.028 | 5 |

## Gamebook checks

- 2026_09_DEN_CAR: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224920/gamecenter/ab380efd-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
