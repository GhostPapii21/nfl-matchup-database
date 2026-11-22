# MIA scheme and opportunity profile, 2026

Miami Dolphins. Research only. projection_ready is false. This file does not change model weights or formulas.

Overall status: PARTIAL. Opportunity evidence: COMPLETE. Gamebooks: PARTIAL. Scheme charting: BLOCKED.

## Window

8 completed games, last game 2026_09_DET_MIA on 2026-11-08. Last fully completed week is 9. Bye weeks inside weeks 1-9: [6].

Game ids: 2026_01_MIA_LV, 2026_02_MIA_SF, 2026_03_KC_MIA, 2026_04_MIA_MIN, 2026_05_CIN_MIA, 2026_07_MIA_NYJ, 2026_08_NE_MIA, 2026_09_DET_MIA.

## Blocked fields

Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. A shotgun flag is a formation label and is reported below. It is not a personnel package. Tacklers in the play-by-play are not coverage assignments.

## Offense, regulation

Scrimmage plays: 444. Early-down pass rate: 47.1% (156/331). Early-down run rate: 52.9% (175/331).
Neutral pass rate (margin -7 to +7): 48.4% (132/273). Leading by 8+: 50.0% (3/6). Trailing by 8+: 58.2% (96/165). Tied: 47.7% (31/65).
Short-yardage pass rate (1st-and-2 or fewer yards, any down): 28.6% (10/35). Long-yardage pass rate (7+ yards to go): 53.9% (181/336).
Third down: 41.6% (42/101). Unknown third-down results: 0.
Red-zone plays: 68. Red-zone pass rate: 32.4% (22/68). Derived red-zone drive touchdown rate: 52.6% (10/19). Official red-zone trip efficiency: unknown.
Derived explosives: pass 20+ 7.8% (18/231); rush 10+ 13.1% (28/213); rush 15+ 4.7% (10/213). Official explosive label: unknown.
Sacks taken: 24. Scrambles: 24 (9.4% (24/255) of dropbacks). Kneels, excluded from carries: 2.
Shotgun rate, where the flag is present: 58.1% (258/444). Plays with no shotgun flag: 0.
Rush direction counts (unknown is not folded into left, right, or middle): left 74, middle 80, right 57, unknown 2.

## Defense, regulation

Scrimmage plays faced: 453. Early-down pass rate allowed: 45.7% (159/348).
Third down allowed: 47.4% (46/97). Sacks recorded: 12. Scrambles allowed: 13.
Explosive passes allowed (20+): 9.4% (22/233). Explosive rushes allowed (10+): 10.5% (23/220).

## Overtime

Offensive scrimmage plays: 0. Early-down pass rate: unknown. A rate with no overtime plays is unknown, not zero.

## Recent games

Last 5 early-down pass rate: 45.4% (93/205) across 5 games (COMPLETE). Earlier games: 50.0% (63/126). Difference: -0.046.
Last 8 early-down pass rate: 47.1% (156/331) across 8 games. Difference versus earlier: unknown.

## Player opportunity

Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.

| Player | Targets | Target share | Games |
| --- | ---: | ---: | ---: |
| M.Washington | 48 | 0.240 | 8 |
| G.Dulcich | 32 | 0.160 | 7 |
| C.Douglas | 27 | 0.135 | 5 |
| C.Bell | 25 | 0.125 | 8 |
| K.Coleman | 21 | 0.105 | 6 |
| D.Achane | 12 | 0.060 | 3 |
| O.Gordon | 10 | 0.050 | 5 |
| W.Kacmarek | 9 | 0.045 | 6 |

| Player | Carries | Carry share | Games |
| --- | ---: | ---: | ---: |
| O.Gordon | 107 | 0.502 | 7 |
| M.Willis | 36 | 0.169 | 8 |
| D.Achane | 34 | 0.160 | 3 |
| J.Wright | 22 | 0.103 | 6 |
| M.Washington | 9 | 0.042 | 6 |

## Gamebook checks

- 2026_09_DET_MIA: MATCH. score, third down, sacks, plays, rushes including kneels, and targets matched Source: https://static.www.nfl.com/image/upload/v1794224917/gamecenter/ab381a59-4feb-11f1-abca-2c54536568a9.pdf

Weeks without a persisted or opened gamebook are not given book-derived counts.

## Sources

Play-by-play: https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`.
Evidence rows: `data/scheme_profiles/2026/evidence_plays.csv.gz`. Every count above is the numerator of those rows.
