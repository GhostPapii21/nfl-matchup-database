# Rare special-teams plays: before / after evidence (refs NFL-75, refs NFL-43)

Research only, not validated. BACKTEST on already-seen weeks 4-9 (not a clean holdout). No engine weights changed,
nothing fitted to outcomes; every rare-play rate is a count ratio over nflverse PBP. Brier vs the close is a diagnostic
only. `projection_ready` stays false; `nfl43.still_unsupported` still lists "kick-play fouls" and "blocked
kicks/onside/fakes", so no lock / 100k / rocket path can turn this on.

## Runs
| Arm | Engine | Command | Finished (ET) | Runtime |
|---|---|---|---|---|
| Before = `new_off` (rare plays off) | 0cb05ea, engine tree f9775c4 (clean) | `python3 -m calibration.backtest --n 2000 --arms new_off,rare_v1 --workers 7 --tag rare_plays` | 2026-11-12 9:39 PM ET | 2,397 s (both arms) |
| After = `rare_v1` (`semantics.rare_plays = "asof_league_v1"`) | ec4bba3, engine tree 12396d1 (clean) | `python3 -m calibration.backtest --n 2000 --arms rare_v1 --workers 7 --tag rare_plays_v2` | 2026-11-12 10:06 PM ET | 1,267 s |

Both: 88 games, weeks 4-9 2026, n=2,000 per game, seed base 20261112, h2h off, default accounting, history weeks 1..w-1.
PBP `data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet` (sha256 1028614b..., pulled 2026-11-12
11:16 AM ET). Close: `ba83615:data/lines/lines_wk04_09_2026.csv` (sha256 6e330ca1..., matches data/lines/README.md).
Off mode is the engine at main d817a3b bit for bit: the `new_off` numbers equal `backtest_after_wp12_n2000.json`
(PR #26) to every printed digit, and the golden test (WAS@NYG, n=60, seed 20261112, sha 18984268e877d4cb) passes.
ec4bba3 changed only rare-mode code after 0cb05ea (band-usage output, pooled clean punt-return rate), so `new_off` from
the 0cb05ea run is the valid before arm. The 0cb05ea `rare_v1` arm is kept in the same files for transparency.

## Backtest (88 games)
| Metric | Before (off) | After (rare_v1, ec4bba3) | rare_v1 at 0cb05ea | Close |
|---|---|---|---|---|
| Brier, home win (diagnostic) | 0.2515 | 0.2530 | 0.2517 | 0.2055 |
| Log loss, home win | 0.7101 | 0.7109 | 0.7071 | 0.6017 |
| Total MAE (pts) | 11.39 | 11.41 | 11.43 | 10.33 |
| Margin MAE (pts) | 10.69 | 10.80 | 10.80 | 8.98 |
| Total bias, sim minus actual (pts) | -0.09 | +0.35 | +0.20 | |
| Mean sim total / actual 46.05 | 45.95 | 46.39 | 46.25 | |
| Corr(sim total, close total) | 0.542 | 0.553 | 0.554 | |
| Corr(sim margin, close margin) | 0.539 | 0.542 | 0.547 | |
| PIT total quartiles | .273/.193/.284/.250 | .295/.170/.284/.250 | .295/.182/.273/.250 | |
Reading: rare plays add about +0.4 points per game (blocked-kick and fake TDs, safeties, onside), and every
accuracy metric moves within simulation noise for 88 games. They are not an accuracy fix; they add events the engine
could not produce before.

## Special teams by type vs actual (per game, both teams, weeks 4-9; `rare_plays_st_compare_n2000.json`)
| Event | Actual (88 games) | Before (off) | After (rare_v1) |
|---|---|---|---|
| Punt plays (incl. blocked / flagged / fake) | 7.727 | 8.970 | 8.977 |
| FG plays | 4.364 | 3.686 | 3.673 |
| FG made | 3.682 | 3.124 | 3.119 |
| PAT good | 4.182 | 4.980 | 5.041 |
| PAT blocked | 0.011 | 0.044 (team pools) | 0.038 |
| Defensive two-point on blocked PAT | 0 | 0 | 0 (0 of 40 blocked PATs in the source rows) |
| Kick-return TD | 0.011 | 0.002 | 0.004 |
| Punt-return TD (clean punts) | 0 | 0.013 | 0.021 |
| Safety | 0.011 | 0.068 | 0.074 |
| Blocked punt | 0.011 | 0 | 0.053 |
| Blocked FG | 0.068 | 0 | 0.062 |
| Blocked-kick return TD | 0.011 | 0 | 0.016 |
| Fake / aborted kick-formation snap | 0.057 | 0 | 0.110 |
| Kick-formation pre-snap foul | 0.330 | 0 | 0.328 |
| Penalty-flagged punt / FG | 0.761 | 0 | 0.809 |
| Flagged-kick return TD | 0 | 0 | 0.002 |
| Onside attempt | 0.170 | 0 | 0.152 |
| Onside recovered by kicking team | 0 | 0 | 0.007 |
| Special-teams points (FG, PAT, return / block / fake TDs) | 15.36 | 14.44 | 14.66 |
Notes: the sim punts about 16% more often than actual and kicks fewer FGs, which is an existing engine property
(off mode has the same numbers). Rare-event counts scale with it: blocked punts and fakes per punt are as-of league
rates (0.56% and 1.07% at week 10), so the per-game counts run high where punts run high. Actual weeks 4-9 counts are
small samples (1 blocked punt, 5 fakes, 0 onside recoveries in 88 games).

## Rates used (as of week 10; each run's `semantics.rare_plays` meta lists file, sha256, pull time and n)
Rows: 2026 REG weeks 1-9 (`pbp_2026_w1_9_pulled_20261112T1116ET.parquet`) + 2018 / 2020 / 2022 / 2024 REG
(`data/historical/nflverse/pbp_<season>.parquet`, pulled 2026-11-06 7:28-7:29 AM ET, `data/historical/MANIFEST.md`).
| Formation | Rows | Pre-snap foul | Fake / aborted | Blocked | Penalty-flagged | Clean |
|---|---|---|---|---|---|---|
| Punt | 9,765 | 267 (2.73%) | 104 (1.07%) | 55 (0.56%) | 853 (8.74%) | 8,486 |
| Field goal | 4,767 | 94 (1.97%) | 15 (0.31%) | 78 (1.64%) | 9 (0.19%) | 4,571 |
PAT: 40 blocked of 5,620 (0.71%), 0 defensive two-pointers. Onside (2024 + 2026 W1-9 only, dynamic kickoff): 72
onside of 4,207 kickoffs, 3 recovered by the kicking team; outside Q4-trailing 0 of 3,905. Clean punt-return TD:
25 of 7,840 clean non-touchback punts (pooled; current season alone 0 of 866 because its only return TD carried a
flag). Clean kick-return TD: current-season non-onside kickoffs (1 of 1,382).

## Outcome sampling bands (`rare_plays_band_usage.json`, WAS@NYG w10, BUF@KC w9, LV@DEN w7, n=2,000 each, seed 777)
Of 8,674 kick-formation outcome draws: exact line of scrimmage 5,291 (61.0%), within 1 yard 2,154 (24.8%),
2 yards 481, 5 yards 426, 10 yards 256, 20 yards 63, whole pool 3 (FG flagged; no distance bound). 1,067 onside draws
use the row's absolute spot. Non-touchback rows outside the exact band are translated by the LOS shift (declared
limitation, error up to the band width).

## Tests and gate
`./rocket`: PASS (R1-R4), possession engine suite 291 passed (`RARE_PLAYS_rocket.json`). New:
`core/possession_engine_v0/tests/test_rare_plays.py` (33 tests: off-mode golden, gate / research cap / budget,
classification, outcome resampling and bands, presnap live semantics, fakes, PAT, onside, catalog exclusions,
provenance, penalty-model exclusion). `bash scripts/test_offline.sh`: see PR.

## Independent review
Four static passes by a separate reviewer (codex, read-only sandbox): pass 1 REQUEST CHANGES (historical down/distance
overrode the live state; LOS-shift translation at boundaries; punt-return denominator; uncapped research path),
pass 2 REQUEST CHANGES (auto first down inferred from an already-first-down row; boundary translation), pass 3 APPROVE
(P3: expose band usage), pass 4 APPROVE (band usage + pooled clean punt-return rate). Files:
`RARE_PLAYS_REVIEW_pass{1,2,3,4}.md`.

## Still unsupported
PAT fouls carried to the kickoff or re-tries; player yardage credit on fakes (team outcome only); two-point tries
(engine always kicks); rule-coded kick-foul enforcement (resampled from real rows instead); exact spot translation
outside the exact-LOS band; blitz-strata pools may still hold fake-punt / fake-FG snaps; the off-mode punt-return TD
denominator is unchanged (kept for bit-identity); no 2019 / 2021 / 2023 / 2025 PBP in the repo, so priors are four
seasons.
