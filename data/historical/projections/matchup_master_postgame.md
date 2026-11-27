# matchup_master_postgame.csv

Companion postgame results file for `data/historical/projections/matchup_master.csv`.

**Why a companion file:** `matchup_master.csv` is the pregame projection table (64 columns). Thursday refresh builders (`runs/2026-11-26_matchup_run/build.py` and earlier weekly copies) read that header with `pd.read_csv(..., nrows=0)` and append pregame rows. Adding postgame columns there would change the header those writers expect. This PR does not include the uncommitted 2026-11-26T06:17 local refresh of `matchup_master.csv` / `.jsonl`.

**Join keys:** `game`, `offense`, `defense`, `run_id`, `run_ts`.

**Games (Week 12 Thanksgiving 2026, all FINAL):**

| Game | Score | Total | Our read | Notes |
|---|---|---|---|---|
| CHI@DET | CHI 39, DET 35 | 74 | C+ | Only vetted lean: Caleb Williams rush U22.5 HIT (official 15 rush yds) |
| PHI@DAL | PHI 39, DAL 38 | 77 | C− | Elliott 59-yd FG at 0:02 |
| KC@BUF | BUF 13, KC 10 | 23 | A− | Bass 57-yd FG at 0:00. Mahomes rush U12.5 HIT; 1H U23.5 HIT; alt U52.5 HIT |

Two rows per game (one per offense). Letter grades, weak coverage zones, TD scorers, and lean HIT/MISS are from each game's `POSTGAME_REVIEW.md`. Path columns in this file are repo-relative.

Research only. `projection_ready=false`.
