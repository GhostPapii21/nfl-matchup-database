# NYJ scheme and opportunity profile, 2026

New York Jets. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_NYJ_KC on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_NYJ_TEN, 2026_02_GB_NYJ, 2026_03_NYJ_DET, 2026_04_NYJ_CHI, 2026_05_CLE_NYJ, 2026_06_NYJ_NE, 2026_07_MIA_NYJ, 2026_08_LV_NYJ, 2026_09_NYJ_KC.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 519. Early-down pass rate: 51.1% (203/397). Early-down run rate: 48.9% (194/397).
Neutral pass rate (margin -7 to +7): 54.4% (216/397). Leading by 8+: 33.3% (6/18). Trailing by 8+: 70.2% (73/104). Tied: 56.6% (64/113).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 26.4% (14/53). Long-yardage pass rate (7+ yards to go): 64.8% (236/364).
Third down: 35.7% (40/112). Unknown third-down results: 0.
Red-zone plays: 75. Red-zone pass rate: 53.3% (40/75). Derived red-zone drive touchdown rate: 42.3% (11/26). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 8.1% (24/295); rush 10+ 12.5% (28/224); rush 15+ 5.4% (12/224). Official explosive label: unknown.
Sacks taken: 26. Scrambles: 12 (3.9% (12/307) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 57.8% (300/519). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 81, middle 60, right 81, unknown 2.

## Defense, regulation

Scrimmage plays faced: 559. Early-down pass rate allowed: 47.5% (206/434).
Third down allowed: 42.3% (47/111). Sacks recorded: 22. Scrambles allowed: 20.
Explosive passes allowed (20+): 7.9% (23/290). Explosive rushes allowed (10+): 10.4% (28/269).

## Overtime

Offensive scrimmage plays: 3. Early-down pass rate: 100.0% (2/2). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 50.9% (116/228) across 5 games (COMPLETE). Earlier games: 51.5% (87/169). Difference: -0.006.
Last 8 early-down pass rate: 52.9% (185/350) across 8 games. Difference versus earlier: +0.146.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| G.Wilson | 63 | 0.244 | 8 |
| A.Mitchell | 34 | 0.132 | 5 |
| K.Sadiq | 31 | 0.120 | 9 |
| M.Taylor | 25 | 0.097 | 6 |
| B.Allen | 24 | 0.093 | 9 |
| O.Cooper | 24 | 0.093 | 4 |
| I.Williams | 15 | 0.058 | 6 |
| B.Hall | 14 | 0.054 | 4 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| B.Allen | 120 | 0.536 | 9 |
| B.Hall | 66 | 0.295 | 4 |
| G.Smith | 17 | 0.076 | 8 |
| I.Davis | 15 | 0.067 | 4 |
| I.Williams | 4 | 0.018 | 4 |

## Gamebook checks

- 2026_09_NYJ_KC: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224919/gamecenter/ab381724-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
