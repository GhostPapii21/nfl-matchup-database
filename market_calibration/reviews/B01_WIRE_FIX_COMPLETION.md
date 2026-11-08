# B01 wire fix — Codex self-review

2026-11-06, coordinator policy t353u. MARKET implementation is written;
**current-environment verification is BLOCKED by external contract drift**.
This is a separate post-implementation self-review by the same Codex session,
not a claim of a second independent reviewer or Ghost acceptance.

Native producer object status, manifest digest, component/dependency names and
nested points are read without transforming the row. Conflicting aliases and
incomplete status reject the batch. OT requires a Boolean, contiguous paired
periods and a regulation tie; false plus even known-zero primitive OT rows is
rejected, never dropped. `deepcopy(row)` remains the sole source retention path.
No diagnostic trial remap enters production. Existing scalar callers remain
supported. Agreement: [market-producer-wire-v1.0.1](../tracking/WIRE_AGREEMENT_v1.0.1.md).

The first new direct smoke test failed before implementation with exactly
`ValueError: missing trial fields` ([red log](pytest_b01_wire_red.txt)). It uses
the unchanged real JSONL (SHA `1f9ac512…`) and ordered IDs from prior producer
`reviews/EVIDENCE_CODEX.json`, not IDs reconstructed from the consumer rows.

| Verification | Actual result |
| --- | --- |
| Required market suite, unchanged current environment | **106 passed / 67 failed**, exit 1; failures are at the contract guard or assertions affected by that guard. |
| Required B01 direct integration test | **1 failed**, exit 1: `bound core contract absent or changed; alignment required`. |
| Full unchanged adversarial suite, all 60 tests | **32 passed / 28 failed**, exit 1. |
| Separate historical-contract rehearsal of entire market suite | **173 passed**, exit 0, including all 64 new native-wire tests. This is not current-environment acceptance. |

The contract was SHA `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`
at the start. During this run another owner added the producer-wire companion
link, producing SHA
`6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`.
The read-only `integration/wire/CORE_WIRE_LOCK.md` documents that change. This
task explicitly requires the original binding; the adapter constant and MANIFEST
binding remain unchanged. The coordinator was asked to restore the original
bytes; no new SHA has been authorized in this session.

For the explicitly labeled rehearsal only, the single newly added link line was
removed from an in-memory copy, its resulting bytes independently hashed to the
exact required SHA, and a temporary MARKET-local contract file was supplied via
an in-process `CORE_CONTRACT` path override. The shared contract, SHA constant,
test source and producer rows were untouched. The temporary file was removed.
The checked-in direct regression has no contract override or trial mapping.
The official commands above used no override. Exact commands, outputs and hashes
are in [codex_b01_wire_evidence.json](codex_b01_wire_evidence.json).

The full integration run also exposes its frozen pre-fix MARKET inventory and
old CORE touched-file hashes. Its staged diagnostic tests still expect the
old wire rejections, and its score-sensitivity probe changes only flat points
while leaving nested points different; the new agreement must reject that
conflict. These integration tests and inventories were left unchanged. Full-suite
green cannot be inferred from the successful historical MARKET rehearsal.
Fixture writes for the full integration run were confined to a temporary
directory under MARKET reviews and removed; no integration output was replaced.

Self-review found no remaining implementation defect against the requested wire
rules under the bound contract. Residual limitations remain: opaque accounting
payloads are transported without full validation; expected IDs are optional in
the library, mandatory for the integration procedure; component provenance is
retained rather than reconciled into an invented version map. Current completion
requires the contract owner to restore the authorized bytes (or a separate
explicitly authorized binding change), followed by the official tests.

All smoke artifact files, retained producer evidence and the integration test
file match their start-of-run hashes. No CORE, smoke or integration file was
written by this session. MARKET remains research transport, actionable NOLINE;
Bias remains UNIMPLEMENTED_NO_FITTED_CALIB with null coefficients;
FULL_CORE_ACCEPTANCE_NOT_RUN. Network=0, sims=0, paid odds=0. No projection,
FITTED/VALIDATED/actionable MATCHED, predictive improvement or Ghost acceptance.
