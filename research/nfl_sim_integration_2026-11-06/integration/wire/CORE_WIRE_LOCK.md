# CORE producer wire lock — 2026-11-06

CORE owns producer export; BetGuru owns the adapter and `market_calibration`.
CORE will not change producer field names without an explicit joint schema bump
with BetGuru, recorded in the contract and both owners' tests. Until then the
canonical wire is `nfl-sim-joint-trial-producer-wire`, `1.0.0-producer`.

The adapter should target the unchanged immutable example:
`/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/producer_joint_trial_example_v1.jsonl`
with SHA-256 `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`.
CORE did not rename fields. `status` remains an object; the manifest key remains
`freeze.input_manifest_digest`; engine keys remain `component_version` and
`dependencies`; period points remain `team_periods[].stats.points`. No acceptance
mapping or alternate fixture replaces the producer example.

The contract now links the additive [wire companion](../../core_contract_wire_v1.md).
The contract SHA-256 changed honestly:

| Binding | SHA-256 |
| --- | --- |
| Historical core_contract.md bound by the frozen metadata and original adapter handoff | `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9` |
| Current core_contract.md, after adding the wire companion link | `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367` |

`WIRE_SCHEMA_V1_META.json` and `BETGURU_WIRE_COORDINATION.md` are retained as
original freeze records; their old contract binding is historical, not a claim
about current contract bytes. BetGuru must align its contract binding as well as
its adapter fields. No producer wire schema bump was made by this documentation
update. Direct acceptance remains **BLOCKED**, waiting on BetGuru adapter
alignment to producer `1.0.0-producer` and acceptance of the unchanged example.

All `market_calibration` trees remain unedited by CORE. Research transport stays
NOLINE; Bias stays UNIMPLEMENTED_NO_FITTED_CALIB; impact NOT_MEASURED.

## Binding authorization for adapter

BetGuru must rebind to current contract SHA `6471e69b…` per [CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md](CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md). Historical `d6a4689f…` remains documented as pre-link. This is not a producer field rename or wire_schema bump.
