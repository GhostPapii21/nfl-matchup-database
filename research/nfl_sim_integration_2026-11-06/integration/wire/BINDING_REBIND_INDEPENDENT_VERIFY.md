# BetGuru rebind independent verification

VERDICT: **PASS**

Verified at 2026-11-06T12:13:52.669162+00:00. Scope: current binding hashes and the single authorized DIRECT transport test.

| Check | Independently observed value |
| --- | --- |
| core_contract.md SHA-256 | `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367` |
| producer_joint_trial_example_v1.jsonl SHA-256 | `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd` |
| joint_trial_adapter.py CONTRACT_SHA256 (AST read) | `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367` |
| Adapter file SHA-256 | `f430b71834c5da8c59083218c7f0860cee7fd84c30460d9a167aa72af224384d` |

The contract digest, adapter constant, manifest binding, and frozen example digest match the authorization and completion evidence. Protected inputs were rehashed after the run and are unchanged.

DIRECT result: **PASS**, exit code `0`.

Working directory: `/workspace/research/nfl_sim_integration_2026-11-06`. Environment and command copied from BINDING_REBIND_COMPLETION.md:

```bash
export PYTHONDONTWRITEBYTECODE=1
export GIT_OPTIONAL_LOCKS=0
export PYTHONPATH=/workspace/wt-nfl-sim-core-2026-11-06/research/possession_engine_v0:/workspace/wt-nfl-sim-core-2026-11-06:/workspace/wt-market-calibration:/workspace/research/nfl_sim_integration_2026-11-06
python3 -m pytest integration/integration_adversarial_tests.py::test_DIRECT_actual_producer_to_market_acceptance -q -p no:cacheprovider
```

Exact merged stdout/stderr:

```text
.                                                                        [100%]
1 passed in 0.19s
```

- Ghost FINAL is NOT claimed; ghost_final_acceptance=NOT_CLAIMED.
- NOLINE preserved: manifest inspected and DIRECT asserts actionable_status for every transported trial.
- Bias unfitted preserved: manifest status UNIMPLEMENTED_NO_FITTED_CALIB, fitted=false, coefficients=null; no fit performed.
- impact=NOT_MEASURED. No predictive improvement, projection permission, or holdout validation claimed.
- Only the requested DIRECT test was rerun; full adversarial suite was NOT_RUN here. Earlier full-suite failures in PARENT_VERIFY_POST_REBIND.json remain outside this verdict.
- DIRECT consumes durable producer smoke, not the frozen single-row example; the latter was independently hashed only.
- No contract override, trial remap, market_calibration edit, or new simulation performed.
- Verification writes are limited to the two BINDING_REBIND_INDEPENDENT_VERIFY evidence files under integration/wire/.

All input paths, before/after hashes, individual checks, and command output are recorded in [BINDING_REBIND_INDEPENDENT_VERIFY.json](BINDING_REBIND_INDEPENDENT_VERIFY.json).
