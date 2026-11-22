# CHI scheme and opportunity profile, 2026

Chicago Bears. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_TB_CHI on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_CHI_CAR, 2026_02_MIN_CHI, 2026_03_PHI_CHI, 2026_04_NYJ_CHI, 2026_05_CHI_GB, 2026_06_CHI_ATL, 2026_07_NE_CHI, 2026_08_CHI_SEA, 2026_09_TB_CHI.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 624. Early-down pass rate: 49.0% (234/478). Early-down run rate: 51.0% (244/478).
Neutral pass rate (margin -7 to +7): 55.2% (229/415). Leading by 8+: 43.7% (66/151). Trailing by 8+: 62.1% (36/58). Tied: 53.9% (69/128).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 39.4% (28/71). Long-yardage pass rate (7+ yards to go): 56.5% (238/421).
Third down: 45.0% (58/129). Unknown third-down results: 1.
Red-zone plays: 133. Red-zone pass rate: 41.4% (55/133). Derived red-zone drive touchdown rate: 56.8% (21/37). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 10.6% (35/331); rush 10+ 8.9% (26/293); rush 15+ 3.4% (10/293). Official explosive label: unknown.
Sacks taken: 20. Scrambles: 23 (6.5% (23/354) of dropbacks). Kneels, excluded from carries: 10.
Shotgun rate, where the flag is present: 54.2% (338/624). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 110, middle 28, right 153, unknown 2.

## Defense, regulation

Scrimmage plays faced: 468. Early-down pass rate allowed: 55.1% (200/363).
Third down allowed: 22.8% (21/92). Sacks recorded: 26. Scrambles allowed: 14.
Explosive passes allowed (20+): 9.1% (26/285). Explosive rushes allowed (10+): 11.5% (21/183).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 54.0% (136/252) across 5 games (COMPLETE). Earlier games: 43.4% (98/226). Difference: +0.106.
Last 8 early-down pass rate: 50.1% (212/423) across 8 games. Difference versus earlier: +0.101.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| L.Burden | 65 | 0.223 | 9 |
| C.Loveland | 57 | 0.195 | 9 |
| R.Odunze | 51 | 0.175 | 9 |
| K.Raymond | 41 | 0.140 | 9 |
| D.Swift | 29 | 0.099 | 9 |
| C.Kmet | 14 | 0.048 | 7 |
| R.Johnson | 11 | 0.038 | 4 |
| Z.Thomas | 10 | 0.034 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| D.Swift | 155 | 0.529 | 9 |
| K.Monangai | 60 | 0.205 | 4 |
| R.Johnson | 29 | 0.099 | 5 |
| C.Williams | 26 | 0.089 | 6 |
| L.Burden | 8 | 0.027 | 5 |

## Gamebook checks

- 2026_09_TB_CHI: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224924/gamecenter/ab582247-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
