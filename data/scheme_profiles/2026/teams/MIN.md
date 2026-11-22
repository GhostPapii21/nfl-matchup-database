# MIN scheme and opportunity profile, 2026

Minnesota Vikings. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_BUF_MIN on 2026-11-09. Last fully completed week is 9. Bye weeks inside weeks 1-9: [6].

Game ids: 2026_01_GB_MIN, 2026_02_MIN_CHI, 2026_03_MIN_TB, 2026_04_MIA_MIN, 2026_05_MIN_NO, 2026_07_IND_MIN, 2026_08_MIN_DET, 2026_09_BUF_MIN.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 445. Early-down pass rate: 47.3% (157/332). Early-down run rate: 52.7% (175/332).
Neutral pass rate (margin -7 to +7): 55.1% (212/385). Leading by 8+: 33.3% (4/12). Trailing by 8+: 62.5% (30/48). Tied: 48.6% (36/74).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 32.4% (12/37). Long-yardage pass rate (7+ yards to go): 53.9% (178/330).
Third down: 33.0% (36/109). Unknown third-down results: 1.
Red-zone plays: 46. Red-zone pass rate: 60.9% (28/46). Derived red-zone drive touchdown rate: 55.6% (10/18). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.7% (19/246); rush 10+ 10.1% (20/199); rush 15+ 5.5% (11/199). Official explosive label: unknown.
Sacks taken: 23. Scrambles: 18 (6.8% (18/264) of dropbacks). Kneels, excluded from carries: 12.
Shotgun rate, where the flag is present: 62.0% (276/445). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 63, middle 48, right 86, unknown 2.

## Defense, regulation

Scrimmage plays faced: 480. Early-down pass rate allowed: 48.3% (174/360).
Third down allowed: 31.2% (34/109). Sacks recorded: 29. Scrambles allowed: 9.
Explosive passes allowed (20+): 6.1% (16/262). Explosive rushes allowed (10+): 11.9% (26/218).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 52.1% (111/213) across 5 games (COMPLETE). Earlier games: 38.7% (46/119). Difference: +0.135.
Last 8 early-down pass rate: 47.3% (157/332) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| J.Jefferson | 51 | 0.242 | 7 |
| T.Hockenson | 44 | 0.209 | 8 |
| J.Addison | 36 | 0.171 | 7 |
| A.Jones | 22 | 0.104 | 7 |
| M.Price | 11 | 0.052 | 4 |
| J.Jennings | 10 | 0.047 | 6 |
| G.Bartholomew | 8 | 0.038 | 3 |
| T.Felton | 7 | 0.033 | 4 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| A.Jones | 115 | 0.578 | 8 |
| J.Mason | 44 | 0.221 | 4 |
| K.Murray | 20 | 0.101 | 6 |
| C.Wentz | 6 | 0.030 | 3 |
| D.Claiborne | 6 | 0.030 | 2 |

## Gamebook checks

- 2026_09_BUF_MIN: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794285215/gamecenter/ab5825a7-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
