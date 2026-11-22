# ATL scheme and opportunity profile, 2026

Atlanta Falcons. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_CIN_ATL on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_ATL_PIT, 2026_02_CAR_ATL, 2026_03_ATL_GB, 2026_04_ATL_NO, 2026_05_BAL_ATL, 2026_06_CHI_ATL, 2026_07_SF_ATL, 2026_08_ATL_TB, 2026_09_CIN_ATL.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 520. Early-down pass rate: 45.7% (184/403). Early-down run rate: 54.3% (219/403).
Neutral pass rate (margin -7 to +7): 51.4% (142/276). Leading by 8+: 33.3% (19/57). Trailing by 8+: 57.8% (108/187). Tied: 55.0% (33/60).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 37.3% (22/59). Long-yardage pass rate (7+ yards to go): 54.1% (197/364).
Third down: 34.9% (37/106). Unknown third-down results: 0.
Red-zone plays: 73. Red-zone pass rate: 46.6% (34/73). Derived red-zone drive touchdown rate: 61.5% (16/26). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 8.2% (22/269); rush 10+ 10.8% (27/251); rush 15+ 5.6% (14/251). Official explosive label: unknown.
Sacks taken: 16. Scrambles: 12 (4.3% (12/281) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 53.3% (277/520). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 123, middle 58, right 68, unknown 2.

## Defense, regulation

Scrimmage plays faced: 557. Early-down pass rate allowed: 55.2% (234/424).
Third down allowed: 41.7% (50/120). Sacks recorded: 20. Scrambles allowed: 6.
Explosive passes allowed (20+): 7.8% (26/332). Explosive rushes allowed (10+): 12.4% (28/225).

## Overtime

Offensive scrimmage plays: 2. Early-down pass rate: 100.0% (2/2). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 52.4% (108/206) across 5 games (COMPLETE). Earlier games: 38.6% (76/197). Difference: +0.138.
Last 8 early-down pass rate: 46.4% (166/358) across 8 games. Difference versus earlier: +0.064.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| D.London | 67 | 0.277 | 9 |
| B.Robinson | Bi.Robinson | 40 | 0.165 | 9 |
| K.Pitts | 37 | 0.153 | 9 |
| J.Dotson | 32 | 0.132 | 9 |
| O.Zaccheaus | 16 | 0.066 | 7 |
| Z.Branch | 12 | 0.050 | 6 |
| A.Hooper | 11 | 0.045 | 6 |
| C.Woerner | 8 | 0.033 | 6 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| B.Robinson | Bi.Robinson | 169 | 0.673 | 9 |
| Br.Robinson | 53 | 0.211 | 6 |
| M.Penix | 13 | 0.052 | 5 |
| K.Herbert | 7 | 0.028 | 3 |
| C.Rush | 2 | 0.008 | 1 |

## Gamebook checks

- 2026_09_CIN_ATL: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224918/gamecenter/ab380bc7-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
