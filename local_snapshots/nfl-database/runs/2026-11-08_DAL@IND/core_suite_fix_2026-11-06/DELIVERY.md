# Staged external delivery
Packet and game-run roots are outside this session's writable roots. All new work remains under /workspace/wt-nfl-sim-core-2026-11-06/research/possession_engine_v0/runs/dal_ind_suite_fix_2026-11-06. No external writes were attempted. An authorized operator can copy the full reviewable bundle with these exact commands:

```bash
mkdir -p /workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08/reviews/dal_ind_suite_fix_2026-11-06
cp -a /workspace/wt-nfl-sim-core-2026-11-06/research/possession_engine_v0/runs/dal_ind_suite_fix_2026-11-06/. /workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08/reviews/dal_ind_suite_fix_2026-11-06/
mkdir -p /workspace/nfl-database/runs/2026-11-08_DAL@IND/core_suite_fix_2026-11-06
cp -a /workspace/wt-nfl-sim-core-2026-11-06/research/possession_engine_v0/runs/dal_ind_suite_fix_2026-11-06/. /workspace/nfl-database/runs/2026-11-08_DAL@IND/core_suite_fix_2026-11-06/
```

Selected new model: inputs/selected_robust/model.json. Forecasts: forecasts/selected_robust/. Activate through the existing input-freeze mechanism if consumed externally; do not replace any old sha256 tree or certified_asof artifact. Source changes are in the shared engine checkout and source snapshots in the new forecast trees. Local fixture is a symlink to the packet parquet, with hash in FIXTURE_MANIFEST.json.
