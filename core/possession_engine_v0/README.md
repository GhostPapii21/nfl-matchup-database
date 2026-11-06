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

## Commands
```bash
cd core/possession_engine_v0
python3 -m pytest tests/ -q
python3 run_jaxbal_demo.py
```
