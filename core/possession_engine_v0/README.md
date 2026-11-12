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
