# Joint-trial producer export wire v1

Contract ID: `nfl-sim-core-contract-v1`; contract schema version: `1.0.0`.
Wire schema ID: `nfl-sim-joint-trial-producer-wire`; wire version: `1.0.0-producer`.
This additive companion documents the existing producer serialization. These
wire identifiers label the interface; they do not add payload fields or claim
that synthetic engineering exports are projection-ready.

The immutable reference is
`/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/producer_joint_trial_example_v1.jsonl`,
SHA-256 `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd`.
Hash the exact JSONL bytes, including the trailing newline. The example is a
synthetic workflow fixture with projection blockers, not an observed game or a
certified forecast. [Frozen metadata](integration/wire/WIRE_SCHEMA_V1_META.json)
and [coordination](integration/wire/BETGURU_WIRE_COORDINATION.md) retain its original
contract binding. The core contract link added in this pass changes the contract
bytes; the old contract digest is historical. See the current and previous
digests in [CORE_WIRE_LOCK](integration/wire/CORE_WIRE_LOCK.md) and the acceptance
packet addendum. This documentation change is not a joint wire schema bump.

## Canonical key shapes

Each JSONL line is one joint trial object with these top-level keys:

```text
aggregates contract_version engine events feature_availability flags forecast_id
freeze game latent_state player_periods possessions provenance rng status
team_periods trial_id trial_index validation
```

| Object | Required producer shape |
| --- | --- |
| `status` | Object containing `state`, `completion_reason`, `terminal_state`, `went_ot`, `adapter_projection_allowed`, `projection_blockers`. `state` is a string, `terminal_state` an object, `went_ot` and `adapter_projection_allowed` booleans, and blockers an array. Completion fields stay inside this object. |
| `freeze` | Object with `config_id`, `cutoff_utc`, `frozen_at_utc`, `generated_at_utc`, `input_content_hash`, `input_manifest_digest`, `input_manifest_ref`, `mode`, `split_dependent_claims_allowed`, `split_manifest_hash`, `split_manifest_id`, `split_membership`. Digests use `sha256:` plus 64 lowercase hex digits. The manifest field is `input_manifest_digest`. |
| `engine` | Object with `component_version`, `dependencies`, `dirty_patch_hash`, `engine_version`, `limitations`, `ot_rule_profile`, `source_artifact_ref`, `source_content_hash`, `stat_credit_profile`. `component_version` is a string; `dependencies` maps dependency names to version strings (currently `python`, `numpy`). OT/stat profiles are objects and limitations an array. |
| `team_periods` | Array of objects with `period_id`, `provenance`, `stat_status`, `stats`, `team_id`. Points are integer `team_periods[].stats.points` alongside the accounting stats below. |

The full team-period `stats` shape is:

```text
aborted_dropbacks_no_attempt completions credited_aborted_rushes designed_rushes
dropback_pass_attempts dropbacks eligible_target_attempts field_advance_yards
gross_pass_yards kneels net_pass_yards non_dropback_pass_attempts
other_untargeted_attempts pass_attempts pass_receiving_credit_adjustment points
possession_seconds receiving_yards rush_attempts rush_yards sack_loss_yards sacks
scrambles spikes throwaways turnovers unassigned_carries unassigned_catches
unassigned_pass_attempts unassigned_pass_yards unassigned_rec_yards
unassigned_rush_yards unassigned_sacks unassigned_targets
```

OT rows can include known-zero or played OT rows; preserve the producer's
`status.went_ot` and row provenance. Do not discard rows or change scores to
satisfy consumer expectations. Incomplete/invalid trials retain their blockers
and must not be promoted to complete draws. Core contract accounting, clock,
missingness, cutoff, identity and opportunity-generation requirements still
apply; field-shape regression tests alone do not certify those requirements.

## Joint change rule

CORE will not rename producer fields without an explicit joint schema bump
agreed with BetGuru and recorded in the contract and both owners' test suites.
Until that decision, the adapter targets the unchanged example hash above and
wire `1.0.0-producer`. Do not flatten `status`, rename manifest/version fields,
lift `points` out of `stats`, or silently map fields in acceptance tests.
Direct producer-to-adapter acceptance remains **BLOCKED**, waiting on BetGuru
alignment. Research transport remains NOLINE; Bias remains
UNIMPLEMENTED_NO_FITTED_CALIB; impact is NOT_MEASURED.
