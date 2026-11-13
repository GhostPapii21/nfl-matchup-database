# WP1 + WP2 engine mechanics: before / after evidence (refs NFL-75)

Research only, not validated. BACKTEST on already-seen weeks 4-9 (not a clean holdout). No weights tuned, nothing
fitted to outcomes. Overall Brier vs the close is a diagnostic only.

## Runs
| | Engine | Command | Finished (ET) | Runtime |
|---|---|---|---|---|
| Before | main 9beb9b0, engine tree 72f1116 (clean) | `python3 -m calibration.backtest --n 2000 --arms new_off --workers 4 --tag before_9beb9b0` | 2026-11-12 6:28 PM ET | 1,504 s |
| After | 440dd6a, engine tree 1065695 (clean) | `python3 -m calibration.backtest --n 2000 --arms new_off --workers 4 --tag after_wp12` | 2026-11-12 6:48 PM ET | 1,600 s |

Both: 88 games, weeks 4-9 2026, n=2,000 per game, seed base 20261112, h2h off, point-in-time history (weeks 1..w-1).
PBP: `data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet` (sha256 1028614b..., pulled 2026-11-12 11:16 AM ET).
Close: `ba83615:data/lines/lines_wk04_09_2026.csv` (sha256 6e330ca1..., matches data/lines/README.md). That commit is not in
this checkout's object store, so both per-game CSVs were re-graded against the same file with `calibration/regrade_close.py`
(outputs `*_regraded_close.json`). The before numbers reproduce PR #21 exactly (Brier 0.249, total MAE 11.34, margin MAE 10.43).
The merged commit only adds the clock-cache key (rebuild a cached clock map when a reused catalog changes clock accounting)
on top of 440dd6a; fresh-catalog results are identical (golden check: n=60, seed 20261112, WAS@NYG: sha 18984268e877d4cb on both).

## Backtest (88 games)
| Metric | Before | After | Close |
|---|---|---|---|
| Brier, home win (diagnostic) | 0.2490 | 0.2515 | 0.2055 |
| Log loss, home win | 0.7007 | 0.7101 | 0.6017 |
| Total MAE (pts) | 11.34 | 11.39 | 10.33 |
| Margin MAE (pts) | 10.43 | 10.69 | 8.98 |
| Total bias, sim minus actual (pts) | -1.10 | -0.09 | |
| Mean sim total / actual 46.05 | 44.94 | 45.95 | |
| Corr(sim total, close total) | 0.487 | 0.542 | |
| Corr(sim margin, close margin) | 0.554 | 0.539 | |
| PIT total quartiles (0.25 each if calibrated) | .239/.216/.239/.307 | .273/.193/.284/.250 | |

## Pace: snaps per team-game vs actual (diagnose_total, weeks 4-9, n=200 per game, seed 4949, 88 games)
Actual = the same two teams' as-of rate (weeks 1..w-1) from the PBP above, pass/run/kneel/spike with a down.
| | Sim | Actual | Gap |
|---|---|---|---|
| Before (9beb9b0), runs finished 6:25-6:37 PM ET | 66.89 | 62.08 | +4.81 |
| After (440dd6a), runs finished 6:30-6:40 PM ET | 63.73 | 62.08 | +1.65 |
Actual includes 0.78 kneels per team-game that the sim pool excludes by design (NFL-49 B), so the like-for-like
residual is about +2.4. Drives per team-game: before 12.05, after 11.64, actual 10.84.
Per-week files: `diag_total_w0{4..9}_off_{before,after}_wp12_n200.json`.

## Red zone (WP2), league pool replay of every actual W1-9 red-zone pass/run state, 12 draws per state
| Offensive TD share per snap | Actual | Before | After |
|---|---|---|---|
| Inside the 20 | 19.8% | 16.1% | 21.2% |
| 11-20 yard band | 8.6% | 4.2% | 8.6% |
| Inside the 10 | 32.3% | 29.4% | 35.2% |
| Inside the 3 | 46.5% | 45.1% | 51.7% |
Truncation rate (red-zone snaps drawing a censored TD from closer than the ball, used as a short gain): about 10.6%
before, 0 after. Pool censoring share (data property): 19.9% of W1-9 red-zone pass/run rows.
Declared limitation: inside the 10 the fix swaps a ~3-pt under-count for a ~3-pt over-count (largest inside the 3),
because redistribute-to-the-right assumes gains are independent of field position within the red-zone cell. A local
band variant (only rows between y0 and the ball) was tried as a sensitivity check and was not better; not adopted.

## Tests and gate
`./rocket`: PASS (R1-R4), possession engine suite 258 passed (`WP12_rocket.json`).
New: `core/possession_engine_v0/tests/test_penalty_clock.py` (10 tests), `tests/test_goal_line_truncation.py` (13 tests).

## Independent review
Three static review passes by a separate reviewer (codex, read-only sandbox): pass 1 REQUEST CHANGES (clock-window
conservation claim, unresolved chain returned a replacement, redraw cap, test gaps), pass 2 REQUEST CHANGES (cached clock
map reused across accounting modes), pass 3 APPROVE. Every finding was addressed in code or listed as a follow-up.
Files: `WP12_REVIEW_pass{1,2,3}.md`.
