# MARKET ↔ producer transport agreement v1.0.1

Coordinator policy: t353u. Agreement ID: `market-producer-wire-v1.0.1`.
MARKET accepts unchanged CORE `joint_producer` joint-trial wire v1 as transport
input: wire schema `nfl-sim-joint-trial-producer-wire`, version `1.0.0-producer`.
This agreement versions the adapter interpretation; it does not rename producer
fields or bump the content contract. `contract_version` remains `1.0.0`, bound to
`/workspace/research/nfl_sim_integration_2026-11-06/core_contract.md` SHA-256
`6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`.
This binding is explicitly authorized by CORE's
[CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md](/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md).
The only change from historical SHA `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`
is the additive producer-wire companion pointer on contract line 5; content
contract semantics remain v1.0.0.
An absent or changed content contract blocks transport pending owner alignment.
The producer wire companion does not automatically authorize a new content SHA.

## Native reads and compatibility

| Wire input | MARKET interpretation |
| --- | --- |
| `status` object | Require `state == "COMPLETE"` and nested `completion_reason`, `terminal_state`, `went_ot`. Read completion and OT metadata from this object. Reject incomplete/invalid states. Scalar `status="COMPLETE"` with the three sibling fields remains accepted for existing callers. If object and sibling fields coexist, their values and types must agree. |
| `freeze.input_manifest_digest` | Accept this digest alone, legacy `input_manifest_hash` alone, or both when their values and types agree. Require the same `sha256:<64 lowercase hex>` format as the other freeze hashes. Reject missing, invalid or conflicting aliases. |
| `engine.component_version`, `dependencies` | Accept the producer names directly. Legacy `component_versions`, `dependency_versions` remain accepted; at least one component declaration and one dependency declaration are required. Singular component version and plural component map may coexist as distinct opaque provenance declarations; no map is synthesized. If both dependency maps are present they must agree. `engine_version`, nonempty `ot_rule_profile`, nonempty `stat_credit_profile`, and `limitations` remain required. |
| `team_periods[].stats.points` | Read nested points when top-level period `points` is absent. Accept legacy top-level points. If both exist they must be equal nonnegative integers; booleans and floats are rejected. No scores are inferred from events or aggregates. |

Other existing identity, seed derivation, finite JSON, freeze clock, missingness,
forecast population and expected ordered trial-ID checks remain in force. These
are transport checks; opaque completion, engine and accounting payloads do not
receive full CORE validation here.

## OT policy

`status.went_ot` must be a Boolean (or the legacy sibling Boolean for scalar
status). With `false`, no primitive `OT*` rows may be present. With `true`, require
contiguous `OT1` through `OTn`, both team rows in every OT period, nonnegative
integer scores, and a regulation tie. Played OT scores of zero are preserved and
accepted. A present known-zero OT row with `went_ot=false` is an explicit
inconsistency: reject the entire batch, retain the caller's rows, and report the
error. Never drop such rows, invent missing OT scores, or flip `went_ot`.
Aggregate `OT` payloads are opaque and are not primitive `team_periods` rows.
Known no-OT yields scorecard overtime `(0, 0)` only after the false flag and
absence of primitive OT rows agree. H1/H2/REG exclude OT; FG adds the retained OT
scores from the same trial.

## Preservation and result limits

`JointTrial.source = deepcopy(original_row)`: no field injection, renaming,
diagnostic mapping, flattening or silent repair occurs in the producer source.
Projection blockers, flags, full validation payloads, missingness, provenance and
all other producer fields remain unchanged. No batch filtering, reordering,
resampling or source mutation occurs. Supply independently retained ordered
`expected_trial_ids` for integration; the library argument remains optional.

All transported trials remain `CONTRACT_SCORE_TRANSPORT_ONLY`, actionable
`NOLINE`, with `FULL_CORE_ACCEPTANCE_NOT_RUN` and
`QUOTE_RULE_COMPATIBILITY_NOT_VERIFIED`. Producer `SCENARIO_ONLY` and projection
blockers remain retained. Transport does not grant projection permission.
Bias remains `UNIMPLEMENTED_NO_FITTED_CALIB`, coefficients null; no FITTED,
VALIDATED, actionable MATCHED, Ghost acceptance or predictive improvement claim.
Network requests: 0. Simulations: 0. No new prices or defender data.

## Reproducible evidence

The direct regression reads the unchanged durable smoke JSONL at
`/workspace/research/nfl_sim_integration_2026-11-06/reviews/core_producer_synthetic_smoke/forecasts/sha256_d89f251bd9c3994e66f7d24a0731abbcfb2b3e25bf5302e936eb29fd338653c0/trials.jsonl`,
SHA-256 `1f9ac51296d4d760510b46f77f56de0c4a4df437c94895e327c3b794434f5e6d`.
Expected ordered IDs come from the prior `reviews/EVIDENCE_CODEX.json`, before
loading consumer rows. The test asserts exact source equality, copied ownership,
nested primitive scores and nonactionable status without any remap. Synthetic
edge fixtures separately test alias conflicts, nonzero nested scores, status and
OT rejection boundaries. See [completion review](../reviews/B01_WIRE_FIX_COMPLETION.md)
and [machine evidence](../reviews/codex_b01_wire_evidence.json) for actual outcomes,
including the historical external contract drift. The authorized rebind and
current official results are recorded in
[binding completion](../reviews/BINDING_REBIND_COMPLETION.md) and
[binding evidence](../reviews/codex_binding_rebind_evidence.json).
The market-local binding regression also loads the unchanged immutable example
`integration/wire/producer_joint_trial_example_v1.jsonl` at SHA-256
`50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`,
asserting source preservation, NOLINE transport and retained projection blockers.
