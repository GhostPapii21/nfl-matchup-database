# CORE phase4 verification

CORE engineering verification: **PASS**, with two market review-log changes observed during the interval. No market edits, network requests, paid pulls, spend, or projection runs. No projection readiness or predictive improvement claimed.

## Regression results

- Joint producer: 77 passed; exit 0. [Log](joint_producer.log), [JUnit](joint_producer.xml), [command/timing](joint_producer_run.json).
- Source run gate: 66 passed; exit 0. [Log](source_run_gate.log), [JUnit](source_run_gate.xml), [command/timing](source_run_gate_run.json).

## Integrity

Immutable JSONL example SHA-256: `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd` — matches requested digest.

Current core_contract.md SHA-256: `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`.
Historical SHA-256 reconstructed by removing only the one companion-link line: `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`.
The reconstruction was performed in memory; the contract was not edited. [Exact one-line diff](contract_companion_link_only.diff).

[Before](before_snapshot.json) and [after](after_snapshot.json) snapshots record SHA-256/size for CORE files (including all possession tests), source-gate files, wire artifacts, contract documents, and market trees listed in the snapshots. CORE, source-gate, contract, and wire inventories were unchanged during verification. Two market review logs changed during the same interval; their before/after hashes are recorded in the JSON evidence. This verifier did not write them. Other writers were not audited, so attribution is not established. Git status and tracked diff are unchanged; the existing dirty state was preserved. Market coverage is the recorded inventory roots, including the external market worktree parent research directory; it is not a claim about every filesystem location. The tree-wide market-unchanged check is false and is preserved explicitly.

## CORE diff assessment

Git HEAD: `3448ad77ef3ce46488b4cccfb0cd7478c4d4b6b6`. The worktree has four inherited tracked modifications (README.md, config_load.py, simulate.py, validation/accounting.py) and six untracked producer files, including test_joint_producer.py. [Status](git_status_before.txt), [tracked diff](core_tracked_before.diff), [untracked hashes](core_untracked_inventory.json).

Relative to the pre-phase4 integration snapshot, CORE changes are:

| File | Historical SHA-256 | Phase4 SHA-256 |
| --- | --- | --- |
| research/possession_engine_v0/tests/test_joint_producer.py | 3effe50027ff2a98de4d6c8386b253e4f94d96fea0c9f10c491ceb802c45c6ab | 0496d8b619e29376c021973caec5b6ec1a0b50f70399539ab1c865c35c60f275 |

The [phase4 test diff](test_joint_producer_phase4.diff) adds exactly 58 lines and removes none: an immutable-fixture loader and two wire-shape tests. Removing that block reproduces the historical test hash `3effe50027ff2a98de4d6c8386b253e4f94d96fea0c9f10c491ceb802c45c6ab` exactly. This proves the rest of the test file is unchanged against that recorded baseline. Production CORE hashes match the historical snapshot.

The additions pin fixture SHA and schema/version, exact canonical JSONL export, top-level keys, the nested status object, freeze.input_manifest_digest, engine.component_version/dependencies, and team_periods[].stats.points. They reject alternate field spellings and keep adapter_projection_allowed false. No producer field renames or runtime code changes occurred for this wire lock. Git itself cannot show an incremental diff for the untracked test; the hash-verified historical reconstruction supplies that comparison.

## Predictive metrics

**NOT_MEASURED**: no frozen forecast vs actual evaluation in this engineering pass; insufficient paired data for predictive metrics. Accuracy, calibration, bias, and predictive improvement remain NOT_MEASURED. Passing synthetic engineering tests supplies no predictive evidence.

Direct adapter acceptance and final integration acceptance were not exercised or claimed. Full machine-readable checks, before/after evidence, commands, and artifact hashes are in [PHASE4_VERIFY_EVIDENCE.json](PHASE4_VERIFY_EVIDENCE.json).

Observed market log changes (no edits by this verifier):

- `/workspace/wt-market-calibration/research/market_calibration/reviews/pytest_parent_verify_binding_local.txt`
- `/workspace/wt-market-calibration/research/market_calibration/reviews/pytest_parent_verify_direct_post_rebind.txt`
