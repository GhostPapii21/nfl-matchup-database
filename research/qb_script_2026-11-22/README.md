# Backup QB and game script, tested on past seasons (Nov 22, 2026)

Asked after Week 11 Sunday: DeVonta Smith (backup QB Joe Milton) and Buffalo's receivers (projected for 24 passes because
BUF was a 16.5-point favourite; Allen threw 46) pointed at two parts of the board. `python3 study.py` -> `results.json`.

## A. Backup QB: PASS, added (true backups only)

Update, same day: the owner pointed out that Kirk Cousins (7 starts for LV this season, then MIN's starter) is not a
backup. Split by the QB's starts for any team in the previous two seasons:

| Starter | Receiver-games 2024-25 | Yards vs simulation, relative | 95% CI | 2026 check |
|---|---|---|---|---|
| Veteran (8+ recent starts) who changed teams or returned | 472 | 0.979 | 0.901-1.052 (no reliable effect) | 0.848 (34 rows) |
| True backup (under 8) | 747 | 0.909 | 0.844-0.975 | 0.844 (66 rows) |

The board now applies 0.909 to true backups only. The first-pass numbers below (all backups together) are kept for the record.

Usual QB = most starts in the team's earlier games that season (2+). Rows: the board's own simulation run on 2024-2026
receiver-games (`pregame/.cache/opportunity_backtest_rows.parquet`), which knows nothing about the QB.

| | Receiver-games | Yards vs simulation, relative to usual-QB games | 95% CI | 80+ hit vs simulated, relative |
|---|---|---|---|---|
| Fit 2024-25 | 1,219 backup / 3,867 usual | 0.937 (6.3% fewer) | 0.885-0.990 | 0.89 |
| Check 2026 | 100 / 708 | 0.845 (15.5% fewer) | 0.704-0.996 | 0.76 |

About half is fewer targets (0.97), half fewer yards per target (0.97). On 2026, scaling backup-QB games by the 2024-25
factor moves the 80+ chance from 10.7% to 9.5% (actual 9.0%) and lowers the Brier score (0.0645 to 0.0643).
First pass (superseded): `BACKUP_QB_YARDS = 0.937` on yards per catch when the projected starter is not the
usual QB; the 80+ star formula (`dashboard/watch.py`) applies the same factor.

## B. Game script: the old rule FAILED, replaced by the refit
Board rule was: pass attempts x (1 - 0.01 x margin), rushes x (1 + 0.012 x margin), margin capped at 10. With each team's
own pass rate already in the base, 2025-26 team-games (fit 2022-24):

| Pass attempts | MAE |  | Rushes | MAE |
|---|---|---|---|---|
| No script | 6.52 | | No script | 5.96 |
| Old rule | 6.65 (worse than nothing) | | Old rule | 5.99 (worse than nothing) |
| Refit 0.9855 - 0.0006 x margin | 6.49 | | Refit 1.0016 + 0.0037 x margin | 5.94 |
| Refit + QB quality interaction | 6.48 (no real gain; not used) | | | |

10+ point favourites threw 94% of their base (old rule said 90%); 10+ point underdogs threw 89% (old rule said 110%).
Favourites do run more, about a third as much as the old rule assumed.

## C. Teammate out (already tested Nov 16, `research/teammate_out_2026-11-16`)
Other positions gain nothing when a receiver sits; most of his work goes to players with no history. Unchanged.

Research only.
