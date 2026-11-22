# BUF scheme and opportunity profile, 2026

Buffalo Bills. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_BUF_MIN on 2026-11-09. Last fully completed week is 9. Bye weeks inside weeks 1-9: [7].

Game ids: 2026_01_BUF_HOU, 2026_02_DET_BUF, 2026_03_LAC_BUF, 2026_04_NE_BUF, 2026_05_BUF_LA, 2026_06_BUF_LV, 2026_08_BAL_BUF, 2026_09_BUF_MIN.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 492. Early-down pass rate: 46.2% (180/390). Early-down run rate: 53.8% (210/390).
Neutral pass rate (margin -7 to +7): 51.5% (207/402). Leading by 8+: 48.1% (38/79). Trailing by 8+: 54.5% (6/11). Tied: 46.7% (49/105).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 24.5% (12/49). Long-yardage pass rate (7+ yards to go): 52.6% (183/348).
Third down: 43.2% (41/95). Unknown third-down results: 0.
Red-zone plays: 91. Red-zone pass rate: 39.6% (36/91). Derived red-zone drive touchdown rate: 68.8% (22/32). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 12.4% (31/251); rush 10+ 14.1% (34/241); rush 15+ 6.6% (16/241). Official explosive label: unknown.
Sacks taken: 17. Scrambles: 19 (7.0% (19/270) of dropbacks). Kneels, excluded from carries: 14.
Shotgun rate, where the flag is present: 44.7% (220/492). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 85, middle 77, right 77, unknown 2.

## Defense, regulation

Scrimmage plays faced: 495. Early-down pass rate allowed: 57.6% (221/384).
Third down allowed: 39.0% (39/100). Sacks recorded: 17. Scrambles allowed: 10.
Explosive passes allowed (20+): 8.4% (26/311). Explosive rushes allowed (10+): 10.9% (20/184).

## Overtime

Offensive scrimmage plays: 8. Early-down pass rate: 25.0% (2/8). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 45.1% (111/246) across 5 games (COMPLETE). Earlier games: 47.9% (69/144). Difference: -0.028.
Last 8 early-down pass rate: 46.2% (180/390) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| K.Shakir | 42 | 0.189 | 8 |
| D.Kincaid | 38 | 0.171 | 8 |
| K.Coleman | 33 | 0.149 | 8 |
| D.Moore | 32 | 0.144 | 5 |
| J.Cook | 18 | 0.081 | 8 |
| D.Knox | 17 | 0.077 | 8 |
| T.Johnson | 17 | 0.077 | 6 |
| J.Palmer | 12 | 0.054 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| J.Cook | 169 | 0.684 | 8 |
| J.Allen | 52 | 0.211 | 8 |
| R.Davis | 13 | 0.053 | 6 |
| T.Johnson | 7 | 0.028 | 4 |
| D.Moore | 4 | 0.016 | 4 |

## Gamebook checks

- 2026_09_BUF_MIN: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794285215/gamecenter/ab5825a7-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
