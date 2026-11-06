# Period grading + realism (post-12a7768 continuation)

**Not an approved pick.** Development W1–8 only. Prior FG 0/15 and 13/15 artifacts preserved.

## As-of FG coverage
GRADED_FULL: 13/15 (W1 skips remain)

## Period grading (N=150/game, 13 games, 35.6s)
| Period | MAE home | MAE away | Brier home-win |
|---|---:|---:|---:|
| Q1 | 2.7466666666666666 | 3.763076923076923 | (see H1+) |
| H1 | 5.33 | 6.46 | 0.254 |
| H2 | 6.87 | 7.05 | 0.296 |
| Reg | 9.16 | 9.28 | 0.334 |
| FG  | 9.19 | 8.73 | 0.343 |

Period metrics are **separate** from FG (FG row repeated for comparison).

## Realism (development diagnostic)
Actual per-team offense snaps mean: 59.9 (n_team_games=15)
≈2× actual (both offenses): 119.7
Sim mean snaps/game: 133.4
Drive length plays actual mean/median: 7.54 / 7.0 (n_drives=161)
Delta sim − 2×actual snaps: 13.7

## Residual blockers (unchanged / no invent)
- True pressure (FTN qbp): MISSING paid
- Man/zone/MOFO/routes: MISSING free FTN 29-col
- CB/S/DT replacement coeffs: MISSING
- Weather: hook only PENDING_NWS — no DK auto-downgrade
