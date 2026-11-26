# 2026 NFL Weeks 1–9 market grades (backfill, research only) — refs NFL-49, refs NFL-56

Built 2026-11-26 (America/New_York) by `research/grading_backfill_w1_9/grade_markets_w1_9.py`. No Odds API or other paid call. `projection_ready` is false on every row. Nothing here is a validated pick.

## Why this is not in `grading/results/`
`python -m grading.grade` refused all 136 W1–9 games (exit 2, nothing written); see `grader_refusals.log`. The grader only grades a pregame packet committed before kickoff, and packets start in Week 10. The grader is unchanged. These rows live in a separate folder so they never enter the grader's packet CLV holdout (`load_graded_rows` reads every `grading/results/*.jsonl`).

## What is graded
Full game, H1, H2, Q1–Q4 spread / total / moneyline, one row per saved quote, in `<game_id>.markets.jsonl`. Any period × market with no saved price gets one row with `result: "unknown"` and a reason. Summary counts are in `summary.json`.

- **Actuals:** nflverse play-by-play already on main (`data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet`, pulled 2026-11-24T22:17:40Z). Finals matched a fresh nflverse `games.parquet` (pulled 2026-11-26T09:56:16Z) for all 136 games. W1–8 quarters matched `data/historical/period_w1_8/data/games_w1_8.csv`. There were 0 mismatches.
- **Consensus close:** nflverse schedule values already in the repo. W1–8 come from `period_w1_8/data/coverage_ledger_w1_8.csv` (fetched 2026-11-06T14:16:34Z, with prices). W9 comes from the consensus rows in `data/lines/lines_wk04_09_2026.csv` (fetched 2026-11-09T22:25:18Z, spread/total prices unknown). The sportsbook and the quote time are unverified, and the files were fetched after kickoff by design.
- **Named books:** the latest verified pre-kickoff snapshot per game × book × market × period × line (alt lines kept separate) from the local inventory `sportsbook_observations.csv` (sha256 `d59d7cc9…0b65`, `pregame_status = verified_capture_before_start`). These are latest-on-file, not certified closers. Each row records its snapshot time and minutes before kickoff.
- **Conventions:** FT and H2 include OT, and Q4 excludes it. A 2-way moneyline tie counts as a push; the book's own tie rule wasn't verified.

## Coverage
| Weeks | Games | Period-markets graded (of 21/game) | Named-book quotes |
| --- | --- | --- | --- |
| 1–5 | 79 | 3 (FT consensus only) | none: no verified W1–5 pregame book quotes on file |
| 6–8 | 42 | 3 (FT) | yes, FT only |
| 9 | 15 | 3 (FT); JAX@BAL 21 | yes; halves and quarters only for JAX@BAL |

Totals: 426 of 2,856 period-markets graded, 2,430 unknown (no saved half or quarter prices). Quote rows: 5,533 graded (2,743 W / 2,742 L / 48 push).

Caveat: in 3 W9 named-book quotes, the main spread sits 3.5 or more points off the consensus close (CLE@NO lowvig/betonline −1 vs −4.5; ARI@SEA mybookie −12 vs −8.5). These are early snapshots taken before the line moved. They're graded as quoted.

## Locked reads and slips W1–9
None were re-graded here. Their existing grades are in `data/historical/postmortems/` (W7: `WEEK7_SUNDAY_2026-10-25.md`, `DAL_PHI_2026-10-26.md`, `CAR_GB_2026-10-29.md`; W8: `2026-11-01_*`, `2026-11-03_MNF_CHI_SEA.md`, `playlogs/2026_wk8/FINALIZED_*.md`; W9 TNF: `JAX_BAL_2026-11-05.md`). No W1–6 reads are on main. W9 Sunday and MNF reads exist only in local run folders (`nfl-database/runs/2026-11-08_*`, `2026-11-09_*`) and are not graded in the repo.
