# ARI scheme and opportunity profile, 2026

Arizona Cardinals. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_ARI_SEA on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_ARI_LAC, 2026_02_SEA_ARI, 2026_03_ARI_SF, 2026_04_ARI_NYG, 2026_05_DET_ARI, 2026_06_ARI_LA, 2026_07_DEN_ARI, 2026_08_ARI_DAL, 2026_09_ARI_SEA.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 590. Early-down pass rate: 57.9% (256/442). Early-down run rate: 42.1% (186/442).
Neutral pass rate (margin -7 to +7): 58.1% (205/353). Leading by 8+: 42.1% (8/19). Trailing by 8+: 73.4% (160/218). Tied: 55.0% (72/131).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 51.3% (39/76). Long-yardage pass rate (7+ yards to go): 66.8% (270/404).
Third down: 38.1% (51/134). Unknown third-down results: 0.
Red-zone plays: 121. Red-zone pass rate: 62.0% (75/121). Derived red-zone drive touchdown rate: 47.1% (16/34). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 5.1% (19/373); rush 10+ 6.5% (14/217); rush 15+ 5.1% (11/217). Official explosive label: unknown.
Sacks taken: 22. Scrambles: 9 (2.4% (9/382) of dropbacks). Kneels, excluded from carries: 3.
Shotgun rate, where the flag is present: 60.3% (356/590). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 76, middle 87, right 54, unknown 0.

## Defense, regulation

Scrimmage plays faced: 529. Early-down pass rate allowed: 47.4% (194/409).
Third down allowed: 41.1% (44/107). Sacks recorded: 18. Scrambles allowed: 13.
Explosive passes allowed (20+): 9.1% (25/275). Explosive rushes allowed (10+): 9.4% (24/254).

## Overtime

Offensive scrimmage plays: 10. Early-down pass rate: 42.9% (3/7). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 59.5% (144/242) across 5 games (COMPLETE). Earlier games: 56.0% (112/200). Difference: +0.035.
Last 8 early-down pass rate: 58.8% (227/386) across 8 games. Difference versus earlier: +0.070.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| T.McBride | 94 | 0.275 | 9 |
| Mi.Wilson | 88 | 0.257 | 9 |
| K.Bourne | 38 | 0.111 | 7 |
| T.Allgeier | 25 | 0.073 | 9 |
| E.Higgins | 20 | 0.058 | 7 |
| J.Brooks | 17 | 0.050 | 4 |
| J.Love | 14 | 0.041 | 5 |
| M.Harrison | 13 | 0.038 | 4 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| T.Allgeier | 89 | 0.399 | 9 |
| J.Love | 76 | 0.341 | 6 |
| Z.Knight | 28 | 0.126 | 5 |
| J.Brissett | 26 | 0.117 | 8 |
| Mi.Wilson | 3 | 0.013 | 2 |

## Gamebook checks

- 2026_09_ARI_SEA: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224924/gamecenter/ab581f17-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
