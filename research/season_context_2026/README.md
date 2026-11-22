# 2026 season context database (Weeks 1-10)

Rebuilt every Tuesday (retry Wednesday) by `.github/workflows/nfl-season-data.yml`: refresh nflverse, fetch any missing
NFL game books, rebuild, audit, commit. Run by hand: `python research/season_context_2026/build.py`. Definitions are in
the docstring of `build.py`.

## Is the data complete and correct? (`AUDIT.md`)
- 150 of 150 games, Weeks 1-10: final scores, full play-by-play, quarter scores that add up to every final.
- Official NFL game books for all 150 games (`data/gamebooks/2026/wk01`-`wk10`, PDF + text + parsed tables).
- Second-source check: game book quarter scores equal the play-by-play quarter scores in all 150 games (0 disagreements).
- Every team's game count matches its schedule. Flags: none.

## Files
| File | One row per | What is in it |
|---|---|---|
| `games.csv` | game | Score by quarter, who won each quarter, each half and the game; OT; rain/snow highlighted (`rain_or_snow`), bad weather, indoor, temp, wind, weather text; international site; rest days; coaches; QB changes during the game |
| `team_games.csv` | team per game | Result, quarters won/lost, halves, comeback win / blown halftime lead; opponent defense rank and tier (top 5 / bottom 5, season and as-of that week); off bye, short week, after an international trip; key offensive players out and the share of targets+carries they carried; starting QB out; QB change in game; key defenders out; injury factor in a loss; first vs second half offense EPA, success and pass rate, defense EPA allowed, and plain-words adjustment notes |
| `team_profile.csv` | team | Record vs top-5 and bottom-5 defenses, in bad weather, indoors, with key offense out, with the QB out or changed, off bye, after international, on a short week; half win rates; comebacks; average second-half change |
| `player_splits.csv` | WR/TE/RB (3+ games) | Per-game targets, catches, yards and carries overall, and split by: vs top-5 / bottom-5 pass and run defense, bad weather, indoor, off bye, after international, key teammate out, home/away (each with its game count) |
| `key_players.csv` | key player | Who counts as a key player per team (QB, top 2 WR, TE1, RB1 by usage; defenders with 70%+ snaps) |

## League-wide reads so far (small samples; treat as leads to check, not rules)
| Situation | Record | Avg margin | Games |
|---|---|---|---|
| Off a bye | 13-3 | +8.7 | 16 |
| After an international game | 8-5 | +5.5 | 14 |
| Short week | 9-9 | 0.0 | 18 |
| Starting QB out | 11-17 | -1.9 | 28 |
| QB changed during the game | 5-15 | -13.8 | 20 |
| 3+ key defenders out | 3-4 | -5.0 | 7 |
| Won the first half | won the game 108 of 139 | | |

- Rain or snow: 10 games, average total 36.6 points vs 46.2 for all games; home teams won 4 of 10.
- Losses where injuries were a likely factor: 32. Comeback wins from behind at halftime: 30.
- Defense tier from the as-of ranking (only games before that week): teams went 20-22 vs top-5 defenses and 21-20 vs
  bottom-5, so the opponent tier alone did not move the result much. Player-level splits are in `player_splits.csv`.
