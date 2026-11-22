# SEA scheme and opportunity profile, 2026

Seattle Seahawks. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

9 completed games, last game 2026_09_ARI_SEA on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: none.

Game ids: 2026_01_NE_SEA, 2026_02_SEA_ARI, 2026_03_SEA_WAS, 2026_04_LAC_SEA, 2026_05_SF_SEA, 2026_06_SEA_DEN, 2026_07_KC_SEA, 2026_08_CHI_SEA, 2026_09_ARI_SEA.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 551. Early-down pass rate: 49.2% (211/429). Early-down run rate: 50.8% (218/429).
Neutral pass rate (margin -7 to +7): 57.5% (188/327). Leading by 8+: 33.0% (37/112). Trailing by 8+: 68.8% (77/112). Tied: 54.8% (63/115).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 29.5% (13/44). Long-yardage pass rate (7+ yards to go): 56.9% (232/408).
Third down: 37.2% (42/113). Unknown third-down results: 0.
Red-zone plays: 81. Red-zone pass rate: 48.1% (39/81). Derived red-zone drive touchdown rate: 53.6% (15/28). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.9% (24/302); rush 10+ 9.2% (23/249); rush 15+ 3.6% (9/249). Official explosive label: unknown.
Sacks taken: 19. Scrambles: 11 (3.5% (11/313) of dropbacks). Kneels, excluded from carries: 6.
Shotgun rate, where the flag is present: 50.8% (280/551). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 76, middle 76, right 97, unknown 0.

## Defense, regulation

Scrimmage plays faced: 522. Early-down pass rate allowed: 50.1% (195/389).
Third down allowed: 30.8% (37/120). Sacks recorded: 21. Scrambles allowed: 19.
Explosive passes allowed (20+): 4.7% (14/298). Explosive rushes allowed (10+): 6.7% (15/224).

## Overtime

Offensive scrimmage plays: 6. Early-down pass rate: 25.0% (1/4). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 50.6% (124/245) across 5 games (COMPLETE). Earlier games: 47.3% (87/184). Difference: +0.033.
Last 8 early-down pass rate: 49.2% (194/394) across 8 games. Difference versus earlier: +0.007.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| J.Smith-Njigba | 99 | 0.357 | 9 |
| A.Barner | 38 | 0.137 | 9 |
| C.Kupp | 34 | 0.123 | 9 |
| R.Shaheed | 30 | 0.108 | 7 |
| T.Horton | 19 | 0.069 | 6 |
| G.Holani | 15 | 0.054 | 7 |
| J.Price | 15 | 0.054 | 5 |
| E.Wilson | 9 | 0.032 | 5 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| E.Wilson | 111 | 0.440 | 7 |
| J.Price | 47 | 0.187 | 5 |
| G.Holani | 37 | 0.147 | 8 |
| Z.Charbonnet | 22 | 0.087 | 2 |
| S.Darnold | 9 | 0.036 | 6 |

## Gamebook checks

- 2026_09_ARI_SEA: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224924/gamecenter/ab581f17-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
