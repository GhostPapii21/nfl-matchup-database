# BetGuru wire coordination — producer canonical (2026-11-06)

**Owner split:** CORE owns producer export. BetGuru owns `market_calibration` adapter only. Do not cross-edit.

## Canonical wire
- `wire_schema_id`: `nfl-sim-joint-trial-producer-wire`
- `wire_version`: `1.0.0-producer`
- Bound `core_contract.md` sha256: `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`
- Immutable example (exact JSONL line bytes): `producer_joint_trial_example_v1.jsonl`
- Example sha256: `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`
- Meta: `WIRE_SCHEMA_V1_META.json`

## B01 field differences (adapter must consume producer; CORE will NOT rename without joint decision)

| Topic | Producer 1.0.0-producer (canonical) | Adapter currently expects |
| --- | --- | --- |
| status | object with `state`, `completion_reason`, `terminal_state`, `went_ot`, blockers | scalar `status` + sibling `completion_reason`, `terminal_state`, `went_ot` |
| freeze manifest hash | `input_manifest_digest` | `input_manifest_hash` |
| engine versions | `component_version`, `dependencies` | `component_versions`, `dependency_versions` |
| period points | `team_periods[].stats.points` (+ full accounting stats) | `team_periods[].points` |
| OT rows | may include known-zero / played OT rows with `went_ot` | no OT rows when `went_ot=false`; OT requires regulation tie |

**Joint decision rule:** any rename of producer fields requires explicit shared schema bump (e.g. `1.1.0`) recorded in `core_contract.md` + both test suites against the same immutable example hash. Until then, adapter aligns to producer 1.0.0-producer.

## Restrictions unchanged
- Research score transport; actionable **NOLINE**
- Bias **UNIMPLEMENTED_NO_FITTED_CALIB**
- No fabricated readiness / coverage / routes

## Related producer smoke artifact (also producer-shaped; not the freeze)
BetGuru B01 adapter tests currently also reference:
- `/workspace/research/nfl_sim_integration_2026-11-06/reviews/core_producer_synthetic_smoke/forecasts/sha256_d89f251bd9c3994e66f7d24a0731abbcfb2b3e25bf5302e936eb29fd338653c0/trials.jsonl`
- content sha256 `1f9ac51296d4d760510b46f77f56de0c4a4df437c94895e327c3b794434f5e6d`

The **immutable contract freeze** remains `producer_joint_trial_example_v1.jsonl` @ `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`.
Both artifacts are producer 1.0.0-producer shape; adapter must accept either without CORE renames.
Market may publish `market-producer-wire-v1.0.1` as *adapter agreement id* while producer wire_version stays `1.0.0-producer`.
