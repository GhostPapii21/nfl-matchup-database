# NFL-75: per-player box lines on the 100k engine path, WAS@NYG 2026_10 sample (n=20,000)

Research only. `projection_ready` stays false. Not a betting output.

**What changed:** `core/possession_engine_v0/player_box.py` records per-trial, per-player box lines on the engine path
`pipeline.sim100k` runs (simulate_games -> snapshots/lock.run_sim). The lines cover targets, receptions, rec yds,
carries, rush yds, pass att/cmp/yds, sacks taken/made, INT thrown/made, fumbles lost and TDs. Recording is
observational: it makes no RNG draws and no state changes, and it never touches the old yard ledger.
`tests/test_player_box.py` checks game results and every pre-existing output block against digests taken on main
3dad900 (4 configs x 2 seeds, n=100). Weights and formulas are unchanged.

**Reconciliation (every trial):** player sums equal the team ledger for every stat. The team ledger is also checked
against the engine's own records: plays equal engine snap events and the sum of play types, offensive TDs equal
touchdown events, turnovers equal turnover events, yards equal the snap-event yards, rec/rush/pass yds equal the
existing yard ledger, and sacks made equal the opponent's sacks taken. Any failure makes sim100k refuse.
In this sample, 20,000 of 20,000 trials reconcile with 0 failures (`player_box_summary_n20000.json` -> meta.reconciliation).

**Run:** `run_sample.py` uses the sim100k config, as-of PBP (`pbp_2026_w1_9_pulled_20261112T1116ET.parquet`) and
seed derivation (seed 1918467127, 4 chunks). It calls run_sim directly because the game is over and sim100k's
preflight refuses post-kickoff runs. The ESPN box is event 401873052, retrieved 2026-11-13T06:15:47Z (01:15 AM ET).
The raw file is not committed.

**Sanity table:** see `sanity_table_n20000.md` (ESPN actual vs sim median / mean / p10-p90).

What the table shows is the engine's current limits, not recorder errors:
- **QB mix:** the bootstrap resamples W1-9 rows with their original names, so NYG passing splits across Winston
  (21.0 att/game), McCarthy (8.2) and Dart (4.0). McCarthy, who started on Nov 12, has a sim median of 8 attempts
  vs 36 actual. WAS splits Daniels (22.3) with Mariota and Kaliakmanis. No QB or role availability is applied
  (adjustments are off).
- **History caps:** Daniels has 0 INTs in the W1-9 rows, so the sim can never give him one (sim 0.00, actual 2).
  Players with no W1-9 rows (Robert Henry Jr.) cannot appear.
- **Role shares are W1-9 averages:** Nabers sims at 10 targets (median) vs 7 actual, Likely at 9 vs 11, and
  Skattebo at 12 carries vs 18.
These are the inputs the Phase 2 opportunity model has to replace. The recorder only makes them visible.

**Bit-identical at 20k:** `arrays_digest.py` runs run_sim (WAS@NYG config, seed 1918467127, 4 workers, n=20,000) on
main 3dad900 and on this branch (7d5cb36). Both give the same sha256 over all score arrays (`e4650df42d6a45c7`)
and over the old player yard ledger (`7e82e93a70bdaa9b`), with fg_home sum 404,079 and fg_away sum 446,034.
Only the branch carries a player_box (`bit_identical_*_n20000.json`).
