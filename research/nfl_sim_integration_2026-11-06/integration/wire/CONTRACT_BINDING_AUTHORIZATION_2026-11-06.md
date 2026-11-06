# Contract binding authorization — 2026-11-06 (CORE owner)

**To:** BetGuru market adapter (`market-producer-wire-v1.0.1`)
**From:** CORE / producer owner
**Purpose:** Unblock current-environment adapter verification after an additive `core_contract.md` documentation link. No producer field renames. No wire_schema bump.

## Authorized binding

| Item | Value |
| --- | --- |
| Content contract path | `/workspace/research/nfl_sim_integration_2026-11-06/core_contract.md` |
| **Authorized SHA-256 (current)** | `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367` |
| Historical SHA-256 (pre-link) | `d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9` |
| Change class | Additive documentation only: link to `core_contract_wire_v1.md` |
| Producer `wire_version` | still `1.0.0-producer` (unchanged) |
| `wire_schema_id` | still `nfl-sim-joint-trial-producer-wire` |
| Immutable example sha256 | still `50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd` |
| Field names | unchanged (`status` object, `input_manifest_digest`, `component_version`/`dependencies`, `team_periods[].stats.points`) |

## Instruction to adapter owner

1. Update MARKET contract-binding constant / MANIFEST from historical `d6a4689f…` to authorized current `6471e69b…`.
2. Re-run official market suite + `test_DIRECT_actual_producer_to_market_acceptance` **without** any in-memory contract override and **without** silent trial remap.
3. Keep NOLINE / Bias `UNIMPLEMENTED_NO_FITTED_CALIB` / no Ghost final claim until DIRECT greens on the unchanged producer example (or smoke trials of identical producer shape).
4. Do not edit CORE trees. CORE will not edit `market_calibration`.

## Why not restore historical bytes

Steering required retaining canonical producer schema/version **in** `core_contract` + acceptance packet. The companion link is that retention path. Restoring historical bytes would remove the in-contract pointer. Binding bump is the coordinated alternative to a field rename.

## References

- `integration/wire/CORE_WIRE_LOCK.md`
- `integration/wire/BETGURU_WIRE_COORDINATION.md`
- `core_contract_wire_v1.md`
- `integration/wire/INTEGRATION_WIRE_EVIDENCE.json`
- BetGuru `tracking/WIRE_AGREEMENT_v1.0.1.md` (adapter interpretation; should cite this authorization for the new SHA)
