# NFL-42: the single validation entrypoint

**Research only. Not validated. `projection_ready` stays false.**

## The one sanctioned path

`core/possession_engine_v0/validation/entrypoint.py:run_validation` (registered in `ENTRYPOINT_REGISTRY.json`, key
`validation_entrypoint`). It:

1. Checks the authorized decontaminated validator
   `runs/dal_ind_invariance_decontam_2026-11-06/validate.py` by sha256 (`8a9d7294…a201a1`).
2. Checks the contaminated files are byte-for-byte unchanged (immutable historical evidence) and never runs them.
3. Loads the decontam `role_policy_metrics.json` through `load_role_policy`, which refuses any denied file and any
   metrics with a non-null `accepted_policy` or `gate_passed: true` (no W7–8 promotion).
4. Returns `accepted_policy: null` always.

`invoke(path)` is the only sanctioned way to run a validator file. Deny-listed paths (or files with a deny-listed
sha256) raise `ContaminatedEntrypoint`.

## Deny list

| File | Reason |
| --- | --- |
| `runs/dal_ind_suite_fix_2026-11-06/validate.py` (sha256 `29b6b0c2…f93e9`) | `HISTORICAL_CONTAMINATED_W7_8_ACCEPTANCE_GATE` |
| `runs/dal_ind_suite_fix_2026-11-06/role_policy_metrics.json` (sha256 `62b8bc7a…a8e16`) | `CONTAMINATED_METRICS_accepted_policy_from_W7_8` |

## Where it is enforced

All three call `pipeline/hooks.py:nfl42_entrypoint`. It returns OK only if the registry target equals the path above,
`run_validation()` is PASS with `accepted_policy` null, and every deny-listed file is actually rejected by `invoke()`.
A missing file, an unreadable registry, an exception, or tampered bytes are all FAILED (fail closed).

| Path into the engine | Check | Effect when not OK |
| --- | --- | --- |
| `python -m pipeline.sim100k` (the 100k entry point) | gate **G0**, before every other gate; checked again inside `default_engine` right before the sim | REFUSED, exit 2, nothing simulated |
| `python -m snapshots.lock` (the snapshot locker) | right after the NFL-43 review guard | REFUSED, exit 2, nothing simulated |
| `./rocket` | **R1** | rocket FAIL; the 100k gate G6 (which runs rocket) refuses too |

There is no override flag, environment variable or force switch.

## Tests

* `core/possession_engine_v0/tests/test_entrypoint_rejects_contaminated_validator.py`,
  `test_contaminated_metrics_load_rejected.py` (criteria 1–5).
* `pipeline/tests/test_pipeline.py`: `test_entrypoint_guard_*`, `test_g0_*`, `test_default_engine_rechecks_entrypoint`,
  `test_snapshot_locker_refuses_when_entrypoint_not_enforced` (tampered authorized bytes, tampered contaminated bytes,
  promoted metrics, retargeted registry, empty deny list, missing/garbage registry, missing entrypoint).
* `rocket_gate/tests/test_rocket.py`: `test_r1_*`.

## Flag

`known_flags/KNOWN_LIMITATIONS.json` `entrypoint_enforced` is flipped only by a reviewed change after Ghost6 verifies
the commit evidence (Linear NFL-75 / NFL-49 pillar 2). This file documents the enforcement; it does not flip the flag.
