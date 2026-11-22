# KC scheme and opportunity profile, 2026

Kansas City Chiefs. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_NYJ_KC on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [5].

Game ids: 2026_01_DEN_KC, 2026_02_IND_KC, 2026_03_KC_MIA, 2026_04_KC_LV, 2026_06_LAC_KC, 2026_07_KC_SEA, 2026_08_KC_DEN, 2026_09_NYJ_KC.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 468. Early-down pass rate: 53.7% (195/363). Early-down run rate: 46.3% (168/363).
Neutral pass rate (margin -7 to +7): 59.4% (208/350). Leading by 8+: 42.0% (37/88). Trailing by 8+: 73.3% (22/30). Tied: 54.5% (55/101).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 40.0% (24/60). Long-yardage pass rate (7+ yards to go): 58.2% (184/316).
Third down: 40.9% (38/93). Unknown third-down results: 0.
Red-zone plays: 85. Red-zone pass rate: 51.8% (44/85). Derived red-zone drive touchdown rate: 65.5% (19/29). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.5% (20/267); rush 10+ 14.9% (30/201); rush 15+ 6.0% (12/201). Official explosive label: unknown.
Sacks taken: 10. Scrambles: 13 (4.6% (13/280) of dropbacks). Kneels, excluded from carries: 7.
Shotgun rate, where the flag is present: 60.3% (282/468). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 63, middle 81, right 56, unknown 1.

## Defense, regulation

Scrimmage plays faced: 496. Early-down pass rate allowed: 51.2% (190/371).
Third down allowed: 37.0% (40/108). Sacks recorded: 14. Scrambles allowed: 15.
Explosive passes allowed (20+): 6.6% (19/286). Explosive rushes allowed (10+): 8.6% (18/210).

## Overtime

Offensive scrimmage plays: 16. Early-down pass rate: 30.8% (4/13). A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 54.4% (123/226) across 5 games (COMPLETE). Earlier games: 52.6% (72/137). Difference: +0.019.
Last 8 early-down pass rate: 53.7% (195/363) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| T.Kelce | 48 | 0.195 | 8 |
| X.Worthy | 47 | 0.191 | 8 |
| K.Walker | 36 | 0.146 | 8 |
| R.Rice | 32 | 0.130 | 5 |
| N.Gray | 17 | 0.069 | 8 |
| E.Johnson | 16 | 0.065 | 6 |
| T.Thornton | 15 | 0.061 | 4 |
| J.Royals | 14 | 0.057 | 7 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| K.Walker | 159 | 0.757 | 8 |
| E.Johnson | 26 | 0.124 | 6 |
| P.Mahomes | 17 | 0.081 | 8 |
| J.Ott | 3 | 0.014 | 1 |
| K.Tonga | 2 | 0.010 | 2 |

## Gamebook checks

- 2026_09_NYJ_KC: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224919/gamecenter/ab381724-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
