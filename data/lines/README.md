# Weeks 4–9 2026 game lines (open / close)

File: `data/lines/lines_wk04_09_2026.csv`

Built for BetGuru's NFL-49 calibration backtest (weeks 4–9 of the 2026 regular season). Local saved odds only. Zero Odds API credits spent. Nothing in this folder is a validated pick.

## Columns

Exact order:

`game_id`, `week`, `pulled_utc`, `book`, `line_type`, `home_spread`, `total`, `home_ml`, `away_ml`, `source`

- One row per game × book × line_type (`open` or `close`).
- `game_id` is nflverse format (example: `2026_05_WAS_NYG`).
- `home_spread` is the home team's spread. Negative means the home team is favored.
- Blank cells are unknown, not zero. Do not fill them in.
- `pulled_utc` is ISO-8601 UTC. For book quotes it is the snapshot/pull time of that quote. For the nflverse consensus row it is the games.csv fetch time, which is after kickoff by design.

## Sources and pull times

1. **Named-book pregame snapshots** — `/workspace/research/historical_nfl_odds_inventory_2026-11-07/sportsbook_observations.csv` (sha256 `d59d7cc9af0854d8990863abc10e19beb829809bdff285fdf088062c79650b65`). Inventory packaged 2026-11-07 (America/New_York). Used only rows with `pregame_status=verified_capture_before_start`, full-game `spreads`/`spread`, `totals`/`total`, or `h2h`, and `snapshot_timestamp` strictly before event start. This file is a superset of `SCOPED_2026_W1_9_STRICT_PREGAME.csv` from `NFL_HISTORICAL_ODDS_2026_W1_9_v2.zip` (built 2026-11-07 19:14 ET) and of `canonical/CANONICAL_PREGAME_BLITZ.csv.gz`. The canonical file was reviewed and not used as the line source: it keeps the earliest snapshot per line key, which is the wrong row for a close.

2. **Source-labeled open/close** — already saved line-watch CSVs, used only where the file itself labels the snapshot `open` or `close`. T-120 / T-60 / T-30 files were not relabeled.
   - `nfl-database/runs/line_movement_wk10/odds_20261105_JAXBAL_open_game.csv` — pulled `2026-11-05T14:02:23Z` (draftkings, fanduel, pinnacle).
   - `nfl-database/runs/line_movement_wk10/odds_20261105_JAXBAL_close_game.csv` — pulled `2026-11-06T01:12:42Z` (same three books; kickoff `2026-11-06T01:20:00Z`).
   - `nfl-database/runs/line_movement_wk10/odds_20261109_BUFMIN_close_game.csv` — pulled `2026-11-10T01:14:01Z` (same three books; kickoff `2026-11-10T01:18:00Z`).
   These override a reconstructed earliest/latest row for the same game × book × line_type. The JAX@BAL files label Thursday-morning quotes as `open`; that is the series label, not a claim that it is the official weekend opener.

3. **nflverse closing consensus** — `/workspace/nfl-database/runs/2026-11-09_BUF@MIN_r2/raw/games.csv` (sha256 `724d2866f5c01207ad43aae40fcf5d48acd32990f8a0eb543541d77817d4f84f`), pulled `2026-11-09T22:25:18Z` (2026-11-09 17:25:18 EST, from that run's `raw/pull_start.txt`). `book` is `consensus`. `source` is exactly `nflverse games.csv (nfldata)`. This is a close/consensus line, not a specific book. nflverse `spread_line` is the home-favored convention (positive means the home team is favored), so `home_spread = -spread_line`. A 2026-11-07 07:20:50 ET copy at `/workspace/research/nfl_week9_usage_2026-11-07/raw/games.csv` was not used: it predates the Week 9 Sunday and Monday games, and several Sunday lines later moved.

The 11:14 AM ET 2026-11-12 price freeze in this repo is Week 10 WAS@NYG and is out of scope for weeks 4–9.

## Open / close rules

- A mid-week snapshot is never relabeled as open or close on its own.
- If a source file already labels the snapshot `open` or `close`, that label is kept (and the row is dropped if `pulled_utc` is at or after kickoff).
- Otherwise, for each game × book with two or more distinct verified pre-kickoff snapshots, the earliest is `open` and the latest is `close`. These are the earliest and latest pre-kickoff pulls on file, not certified official openers or closers.
- If a game × book has only one verified pre-kickoff snapshot, it is labeled `close` only when that pull is within 2 hours of kickoff (near-kick, not mid-week). A single mid-week snapshot is omitted.
- Book quotes captured at or after kickoff are dropped. The nflverse consensus row is the exception: games.csv is a retrospective schedule file of closing lines, and its `pulled_utc` is the fetch time of that file.

## Row counts

- 1,285 rows (593 open, 692 close).
- 88 games in weeks 4–9 (16 + 15 + 14 + 14 + 14 + 15). That is the full regular-season slate, including bye weeks.

By source family: 1,189 reconstructed book snapshots, 9 source-labeled JAX@BAL / BUF@MIN rows, 87 nflverse consensus closes.

## Coverage (game level, out of 88)

A game is counted as having open or close if at least one row of that type exists, from any book or from the consensus line.

- Both open and close: **56**
- Close only: **32** (all 16 Week 4 games, all 15 Week 5 games, and `2026_06_SEA_DEN`)
- Open only: **0**
- Neither: **0**

## Gaps and limits

- **Weeks 4–5:** no named-book game-line snapshots were in the saved inventory (only player-yardage quotes). Closes are the nflverse consensus line only. There are no book opens.
- **`2026_06_SEA_DEN` (TNF):** every book on file has a single snapshot about 34 minutes before kickoff, so those rows are close only. The consensus close is also present. No book open.
- **Week 6–8 book closes** are generally strong: the latest snapshot is usually about 35 minutes before kickoff. Exceptions: `2026_08_CHI_SEA` pinnacle (latest pull ~12.5 hours before kick) and williamhill_us (about 24.5 hours before kick).
- **Week 9 Sunday book "closes"** from the inventory are typically 25–36 hours before kickoff (latest saved verified snapshot `2026-11-07T13:10:14Z`, Saturday morning ET). They are the latest pre-kickoff pulls on file, not certified Sunday closes. Use the nflverse consensus close for a settled close on those 13 Sunday games plus Thursday `2026_09_JAX_BAL`.
- **`2026_09_BUF_MIN`:** no nflverse consensus close. The 2026-11-09 17:25:18 EST games.csv pull is before the 8:15 PM ET kickoff, so that line was not labeled close. DraftKings, FanDuel, and Pinnacle have source-labeled closes from `2026-11-10T01:14:01Z`. Other books' latest inventory snapshots are from Nov 2–3, about a week early. No later local nflverse copy was found after kickoff.
- **29 single mid-week book snapshots** (almost all Week 9, 72–242 hours before kick) were not labeled open or close.
- Some book rows have a spread and total but a blank moneyline, or the reverse, because that snapshot did not include every market. Blanks were left blank.
- Some Week 9 "opens" use an Oct 29 snapshot, which is an early future line posted during Week 8, not an official opener. JAX@BAL in particular moves sharply after that first pull (home spread from around −3 to around +8.5/+10). The source-labeled Thursday morning opens for DK/FD/Pinnacle are also not weekend openers.
- Weeks 1–2 have no named-book quotes in the inventory at all; they are outside this file's scope.

CSV sha256: `6e330ca155e285e919716ecc3d53dce0d0c74c4cc3d83c927fbdcba872a85212`
