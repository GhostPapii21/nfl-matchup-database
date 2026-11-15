# GB scheme and opportunity profile, 2026

Green Bay Packers. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_GB_NE on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_GB_MIN, 2026_02_GB_NYJ, 2026_03_ATL_GB, 2026_04_GB_TB, 2026_05_CHI_GB, 2026_06_DAL_GB, 2026_07_GB_DET, 2026_08_CAR_GB, 2026_09_GB_NE.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 549. Early-down pass rate: 58.6% (243/415). Early-down run rate: 41.4% (172/415).
Neutral pass rate (margin -7 to +7): 63.1% (193/306). Leading by 8+: 58.6% (106/181). Trailing by 8+: 91.9% (57/62). Tied: 60.8% (73/120).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 51.1% (24/47). Long-yardage pass rate (7+ yards to go): 66.2% (262/396).
Third down: 37.8% (45/119). Unknown third-down results: 0.
Red-zone plays: 101. Red-zone pass rate: 51.5% (52/101). Derived red-zone drive touchdown rate: 55.9% (19/34). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 11.2% (40/356); rush 10+ 7.3% (14/193); rush 15+ 2.6% (5/193). Official explosive label: unknown.
Sacks taken: 17. Scrambles: 2 (0.6% (2/358) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 68.5% (376/549). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 80, middle 50, right 62, unknown 1.

## Defense, regulation

Scrimmage plays faced: 584. Early-down pass rate allowed: 54.4% (243/447).
Third down allowed: 42.0% (50/119). Sacks recorded: 24. Scrambles allowed: 18.
Explosive passes allowed (20+): 6.4% (22/346). Explosive rushes allowed (10+): 9.2% (22/238).

## Overtime

Offensive scrimmage plays: 4. Early-down pass rate: 50.0% (2/4). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 54.8% (132/241) across 5 games (COMPLETE). Earlier games: 63.8% (111/174). Difference: -0.090.
Last 8 early-down pass rate: 57.7% (209/362) across 8 games. Difference versus earlier: -0.064.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| M.Golden | 92 | 0.280 | 9 |
| C.Watson | 74 | 0.225 | 9 |
| T.Kraft | 52 | 0.158 | 9 |
| M.Lloyd | 17 | 0.052 | 8 |
| S.Moore | 14 | 0.043 | 5 |
| J.Jacobs | 13 | 0.040 | 2 |
| S.Williams | 13 | 0.040 | 4 |
| P.Strong | 12 | 0.036 | 3 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| M.Lloyd | 57 | 0.292 | 8 |
| K.Johnson | 42 | 0.215 | 6 |
| J.Jacobs | 36 | 0.185 | 3 |
| P.Strong | 25 | 0.128 | 4 |
| C.Brooks | 15 | 0.077 | 3 |

## Gamebook checks

- 2026_09_GB_NE: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224923/gamecenter/ab581b93-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
