# possession_engine_v0 (research)

Team-only (JAX/BAL 2026 W1–8) possession / PBP vertical slice. Preserves `period_engine_v0`.

**Not a betting engine. No edge claims.**

The opt-in [frozen joint CORE producer](JOINT_PRODUCER.md) generates targets and
carries before yards and exports a checked event ledger. See
[CORE_MANIFEST.json](CORE_MANIFEST.json) for implemented components and blockers.
Only tiny synthetic trials have validated that path; real-game source inputs and
consumer integration remain blocked. Legacy yard-row outputs are explicitly
ineligible for shared-contract projection.

## Configs (frozen, distinct)
- `config/jax_bal_tnf_2026-11-05_data_only.json` — empirical baseline, no QB adjustments, no market
- `config/jax_bal_tnf_2026-11-05_script_adjusted.json` — forward-only QB/injury filter (Fagnano; Lamar OUT)
- `config/jax_bal_tnf_2026-11-05_market_informed.json` — **separate**; must not contaminate data_only

## Key docs
- `FEATURE_MATRIX.md` — implemented / missing / scenario-only with sources & n
- `LICENSE_MANIFEST.md` — nflfastR + NFLSimulatoR MIT provenance (no clone; no R source copied)
- `docs/2026-11-05_possession_engine_v0_design.md`
- `scenarios/bal_upset_fagnano_200_sensitivity.json` — SCENARIO_ONLY

## Engine mechanics fixes WP1 / WP2 (NFL-75, 2026-11-12)
Default accounting now also sets (see `simulate.accounting_from_cfg`; `accounting: "pre_wp12"` reproduces the
engine at main 9beb9b0, `"legacy"` the pre-NFL-49 engine):
- `no_play_clock: "asof_mean"`: a no-play foul charges the as-of mean clock of no-play penalty rows (~11 s on
  W1-9) instead of a flat 4 s (falls back to 4 s with < 30 as-of rows).
- `unmodeled_row_clock: "attribute_to_prior_play"`: timeout (non-penalty no_play) rows are dropped before the
  mean per-play clock is built, so their seconds land on the prior play instead of being lost.
- `goal_line_censoring: "redistribute_right"`: a resampled pass/run that scored from y0 is right-censored
  (gain >= y0); drawn with the ball at y > y0 it is redrawn from same-pool, same-play-type rows known to gain
  >= y0 (Efron redistribute-to-the-right). Snaps carry `goal_line_censoring` tags; unresolved ones are flagged.
Nothing is fitted to scores or lines. Tests: `tests/test_penalty_clock.py`, `tests/test_goal_line_truncation.py`.
Note: `SEMANTICS_BOUNDS.md` still says "a flat 4 s per no-play"; it is NOT edited here because any edit
invalidates the accepted NFL-43 review hash (`known_flags/NFL43_REVIEW.json`) and blocks the 100k gate until
Ghost6 re-reviews. That doc update is a separate, reviewer-owned step.

## Commands
```bash
cd core/possession_engine_v0
python3 -m pytest tests/ -q
python3 run_jaxbal_demo.py
```
## Rare special-teams plays (NFL-75 / NFL-43, 2026-11-12) - opt-in, still gated
`cfg["semantics"]["rare_plays"] = "asof_league_v1"` adds `rare_plays.py`: kick-play fouls (penalty-flagged punts and
FGs, pre-snap no-play fouls in punt / FG formation), blocked punts / FGs / PATs (incl. defensive two-point returns),
onside kicks (decision by kicking-team deficit x 4th-quarter seconds, recovery) and fake / aborted kick-formation
snaps. Absent or `"off"` is the engine at main d817a3b bit for bit (golden test in `tests/test_rare_plays.py`).
- Rates are count ratios over nflverse PBP: the current season's weeks before the target
  (`pbp_2026_w1_9_pulled_20261112T1116ET.parquet`, pulled 2026-11-12 11:16 AM ET) plus the committed prior seasons
  2018 / 2020 / 2022 / 2024 (REG; `data/historical/MANIFEST.md`, pulled 2026-11-06 07:28-07:29 ET). Onside kicks use
  2024 + current season only (dynamic-kickoff rules). Each run's `semantics.rare_plays` meta lists every file, sha256,
  pull time and n. A class with no rows is UNKNOWN (never drawn), not zero.
- Outcomes are resampled from the real rows of each class (next possessor, spot relative to the line of scrimmage,
  points). Rows are taken from the first band around the live line of scrimmage with at least 5 rows: exact LOS
  (no translation), then 1 / 2 / 5 / 10 / 20 yards, else the whole class pool (no distance bound). Touchback rows keep
  their absolute next spot. Pre-snap fouls apply only the spot change at the live down and distance (automatic first
  down only when the row shows the foul reset the down); fakes run through the normal snap mechanics at the live state.
  Research outputs carry `rare_band_usage` (draws per kind / class / band). Nothing is fitted.
- Clean punts use a pooled return-TD rate over the same rows as the class rates (the current season alone has 0 clean
  punt-return TDs before week 10); clean kickoffs keep the current-season non-onside rate.
- In rare mode, kick-formation pre-snap fouls leave the canonical scrimmage penalty rates (the log files them as
  "Penalty"), fakes leave the pass/run pools and count as kick decisions, blocked / flagged kicks leave the team kick
  pools, and onside kicks leave the kickoff start pool, so nothing is counted twice. Kickoff fouls stay in the as-of
  kickoff start pool (they were already there).
- Gate: `known_flags` `nfl43.still_unsupported` still lists "kick-play fouls" and "blocked kicks/onside/fakes", and
  `semantics.rare_plays` is an enabling path for both (`pipeline/nfl43_exclusions.py`), so every lock / 100k / rocket
  config that turns it on is refused. Only a research call `simulate_games(..., research_unaccepted=("rare_plays",))`
  with n <= 20,000 runs it (labeled UNACCEPTED_RESEARCH_ONLY; the model carries a game budget). Lifting the gate is
  Ghost6's NFL-43 review step; proposed bounds text is in the PR.
- Not supported: PAT fouls carried to the kickoff or re-tries, player yardage on fakes, two-point tries, rule-coded
  kick-foul enforcement (resampled instead), exact spot translation for non-touchback rows drawn outside the exact
  LOS (error up to the band width; unbounded for whole-pool fallback). Evidence: `calibration/outputs/RARE_PLAYS_EVIDENCE.md`.

