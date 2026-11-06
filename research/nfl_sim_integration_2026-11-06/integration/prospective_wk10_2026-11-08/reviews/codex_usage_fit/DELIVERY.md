# Staged delivery — external destinations not writable

No external packet/run files were modified. The session only permits workspace and /tmp writes; approvals are unavailable.

- `inputs/model.json` → packet `inputs/model.json` (fitted replacement).
- `inputs/registry.json`, `splits.json`, `run_spec.json` are byte-preserved copies; original packet versions remain authoritative.
- `PATH_SEMANTICS_JOINT_VS_EMPIRICAL.md` → packet same filename.
- `training_evidence.json`, `training_records.json`, `pbp_bridge_verification.json`, `reproducibility.json`, `pytest_joint_producer.txt`, `COMPLETION_PHASES_AND_FIT.md` → packet `runs/usage_fit/` or `reviews/`.
- `nfl-database-run/checklist.md`, `nfl-database-run/report.md`, `COMPLETION_PHASES_AND_FIT.md` → `/workspace/nfl-database/runs/2026-11-08_DAL@IND/`.
- `joint_producer_n5/` and `baseline_n5/` retain exact frozen bytes/source/trials/ledgers locally. Preserve these paths or copy their whole trees for delivery.

Replay: from the CORE workspace run `python3 research/possession_engine_v0/runs/dal_ind_usage_fit/reproduce.py`. It uses frozen packet input declarations and seed 20261108 and checks identical fitted repeat identity/means. Fitter command is recorded in the fit script interface; it reads only the guarded W1–8 extract. Replays after engine modifications appropriately change IDs.
