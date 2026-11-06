# Authorized contract binding rebind — completion

2026-11-06. Coordinator: t353u. Owner: Codex. Scope: `research/market_calibration` only.
Authorized binding rebind complete; official MARKET and DIRECT B01 pass.

## Authorization and provenance

Read CORE's [binding authorization](/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md) and [handoff](/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/HANDOFF_TO_BETGURU_BINDING.md) before editing.
Current `core_contract.md` SHA-256 is `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`.
Removing exactly current line 5 in memory reproduces historical SHA-256
`d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`. No other bytes are removed or changed. The line is 106 bytes,
including two trailing ASCII spaces and its LF newline. Exact line as a JSON string:

```json
"Producer export wire: [`1.0.0-producer`](core_contract_wire_v1.md), frozen example and field-name lock.  \n"
```

Exact reconstructed-historical → current diff:

```diff
--- historical (reconstructed in memory only)
+++ current core_contract.md
@@ -2,6 +2,7 @@
 
 Contract ID: `nfl-sim-core-contract-v1`  
 Schema version: `1.0.0`  
+Producer export wire: [`1.0.0-producer`](core_contract_wire_v1.md), frozen example and field-name lock.  
 Authored: 2026-11-06 (UTC)  
 Coordination: Ghost6 simulation producer; Ghost6 and BetGuru consumer adapters. These are interface responsibilities, not evidence of approval or implementation by either party.
 
```

The immutable [producer example](/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/producer_joint_trial_example_v1.jsonl) still hashes to `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`.
Reconstruction was used only for provenance hashing. It was never supplied to the
adapter or a test as an alternate contract. Protected inputs were rehashed after
all runs and match their before hashes; see the machine evidence.

## Implemented changes

- Updated only `joint_trial_adapter.CONTRACT_SHA256` in production Python. A bytewise
  inverse SHA replacement reproduces the entire before-file hash, confirming no
  other adapter logic changed. `CORE_CONTRACT` retains its canonical absolute path.
- Updated `MANIFEST.json` adapter SHA and added `contract_binding_authorization_path`.
- Updated `tracking/WIRE_AGREEMENT_v1.0.1.md` and `tracking/GHOST_HANDOFF_MARKET_ADAPTER.md`
  with the authorized binding and evidence links. Agreement ID remains
  `market-producer-wire-v1.0.1`; wire remains `1.0.0-producer`; content semantics
  remain v1.0.0.
- Added six market-local regression cases in `tests/test_contract_binding.py`:
  binding/manifest consistency, immutable example transport with retained source,
  two wrong-binding rejection cases, and two wrong-manifest-SHA rejection cases.
  No pre-existing market test hardcoded the historical binding. Its new test use
  is intentionally a negative case. Negative probes temporarily patch only the
  expected SHA constant, never `CORE_CONTRACT`; pytest restores it afterward.

## Exact official reruns

Each log contains the exact merged stdout/stderr bytes. Commands ran in fresh
Python processes, without a contract-path override or trial remapping.

### official_market

Working directory: `/workspace/wt-market-calibration`.

```bash
export PYTHONDONTWRITEBYTECODE=1
python3 -m pytest research/market_calibration/tests research/market_calibration/reviews/test_independent_false_pass.py -q
```

Exact output:

```text
........................................................................ [ 40%]
........................................................................ [ 80%]
...................................                                      [100%]
179 passed in 0.30s
```

Exit code: `0`. Log: [pytest_binding_rebind_market.txt](pytest_binding_rebind_market.txt).

### official_DIRECT_B01

Working directory: `/workspace/research/nfl_sim_integration_2026-11-06`.

```bash
export PYTHONDONTWRITEBYTECODE=1
export GIT_OPTIONAL_LOCKS=0
export PYTHONPATH=/workspace/wt-nfl-sim-core-2026-11-06/research/possession_engine_v0:/workspace/wt-nfl-sim-core-2026-11-06:/workspace/wt-market-calibration:/workspace/research/nfl_sim_integration_2026-11-06
python3 -m pytest integration/integration_adversarial_tests.py::test_DIRECT_actual_producer_to_market_acceptance -q -p no:cacheprovider
```

Exact output:

```text
.                                                                        [100%]
1 passed in 0.18s
```

Exit code: `0`. Log: [pytest_binding_rebind_direct.txt](pytest_binding_rebind_direct.txt).

### market_local_binding_and_immutable_example

Working directory: `/workspace/wt-market-calibration`.

```bash
export PYTHONDONTWRITEBYTECODE=1
python3 -m pytest research/market_calibration/tests/test_contract_binding.py -q
```

Exact output:

```text
......                                                                   [100%]
6 passed in 0.06s
```

Exit code: `0`. Log: [pytest_binding_rebind_local.txt](pytest_binding_rebind_local.txt).

The local check feeds the immutable example directly into `adapt_joint_trials`,
with its independently recorded expected ID and no field edits. It asserts
unchanged input/source equality, independent copied ownership, score transport,
NOLINE, `SCENARIO_ONLY`, and `adapter_projection_allowed=false` retention.
The DIRECT test consumes the unchanged durable producer smoke and retained IDs.
No non-SHA adapter issue remained; no integration or CORE edit was needed.

Before rebinding, the six new regressions produced exactly:

```text
4 failed, 2 passed in 0.07s
```

Exit code: `1`. [Full red log](pytest_binding_rebind_red.txt). The binding and
example cases failed at the historical SHA guard; the two manifest-negative cases
were blocked at the earlier adapter-status guard before reaching digest rejection.
Both wrong-binding probes already passed. After rebinding all six pass.

## Limits and scope checks

All authored persistent changes are under `market_calibration`. CORE contract,
wire companion, authorization/handoff, immutable example and integration test
hashes remain unchanged. No production or official-run contract-path override,
no trial remap, no silent trial exclusion, no new simulation or network request.
The pre-existing active session transcript is an externally appended live log and
is excluded from authored-file hashes.

Actionable status remains NOLINE. Bias remains `UNIMPLEMENTED_NO_FITTED_CALIB`,
coefficients null. Full CORE accounting acceptance remains NOT_RUN. This records
engineering transport checks only; Ghost final acceptance, projection permission,
predictive improvement and untouched-holdout validation are not claimed.
Network: 0. Simulations: 0.

Machine evidence: [codex_binding_rebind_evidence.json](codex_binding_rebind_evidence.json).
