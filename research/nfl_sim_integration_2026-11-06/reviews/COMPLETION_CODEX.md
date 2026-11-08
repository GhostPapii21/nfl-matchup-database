# Codex local CORE completion and review handoff

Local producer implementation is complete for the explicitly supported structural model. **Full integration / real-game export: BLOCKED**; see the residuals below and the component-by-component `CORE_MANIFEST.json`. No predictive quality or final-vet PASS is claimed.

Branch `research-nfl-sim-core-2026-11-06`, HEAD `3448ad77ef3ce46488b4cccfb0cd7478c4d4b6b6` (base `3448ad7`), with local uncommitted changes. Only the possession research package and integration review artifacts were edited. The user authorized implementation after the original contract's documentation-only phase.

## Changes

- Added the opt-in frozen `joint_producer` path to `simulate_games`. The producer allocates and increments targets/carries before catch and yard draws. Trial availability, depth-chart, rotation, intended depth and shared environment states and conditional weights retain explicit MODELED provenance; none are claimed to be charted routes or observed personnel.
- Added exact integer attempt/player-yard accounting, visible unassigned buckets and signed field/lateral/provider credit adjustments. Validation recomputes the event ledger and primitive/aggregate totals, verifies actual causal stage counts, and turns corrupted evidence into INVALID with projection blocked. Invalid/incomplete trials stay in the output population with explicit counts/exclusions.
- Added canonical frozen input/run identities, per-trial SHA-256 seeds, immutable JSONL and manifest artifacts, exact dirty source snapshots, versioned cutoff/split references, and runtime/mutation checks. Player/team/period rows, scores and adapter fields share one ledger and trial-ID population.
- Added explicit regulation/period/halftime/reset/runoff/try boundaries, possession continuity and cap INCOMPLETE handling. Unplayed OT is known zero; unfinished totals remain incomplete/null. The frozen OT profile stays the declared single-possession approximation.
- Propagated coverage UNKNOWN, routes MISSING and personnel 11/12/13 MISSING as null, effect-disabled records on every event. The TNF audit is only a postgame contract reference and is not read as a predictive input.
- Separated independent data_only/script_adjusted from market inputs and market-derived lineage. Split validation rejects overlap and inspected/evidence holdout assignments; UNASSIGNED blocks split-dependent claims. Quote matching and settlement remain BetGuru responsibilities.
- Flagged the legacy yard-row path as ineligible for shared-contract projection. Removed its unconditional declared-clock PASS and added both-team score reconciliation; it cannot report a complete contract PASS.

## Captured checks

`python3 -m pytest research/possession_engine_v0/tests/test_joint_producer.py research/possession_engine_v0/tests/test_adversarial_review.py research/possession_engine_v0/tests/test_final_review.py research/possession_engine_v0/tests/test_missing_feature_adapters.py -q --junitxml=.../reviews/core_producer_pytest.xml`

**88 passed; 0 failures; 0 errors; 0 skipped.** These are tiny synthetic plumbing/accounting fixtures. No historical PBP/TNF simulations, source pulls, fits, calibration, odds or large batches were run. Syntax compilation and `git diff --check` passed.

The durable smoke run requested two synthetic targeted-pass trials: 2 COMPLETE, 0 INCOMPLETE, 0 INVALID, **0 adapter-usable** (both explicitly SCENARIO_ONLY). All ledger checks passed. `core_producer_smoke_result.json` links the complete input/code/forecast artifacts and trial IDs. This is engineering evidence, not a validated NFL forecast.

## Review note and Ghost final-vet residuals

Codex performed a separate self-review of identity/cutoff gates, frozen bytes, runtime replay, opportunity causality, count/yard conservation, clock boundaries, missingness and false-PASS corruption paths. Prior `grok_contract_review.md` was consulted as a risk checklist. It predates this implementation and is **not** a fresh independent review of this diff. No independent reviewer approval is fabricated; fresh independent implementation review and Ghost final vet remain pending.

- Verified canonical real-game/player/team registry and crosswalk joins have not been supplied or independently authenticated.
- Certified as-of frozen source bundles and sourced availability/depth/rotation/target-depth/outcome distributions remain absent; only synthetic inputs were run.
- Official OT, penalty/untimed-down semantics and defensive/special-teams return production remain unsupported and explicitly blocked when requested.
- Legacy raw-PBP ingestion remains a historical yard-row bootstrap and cannot emit usable shared-contract projections.
- Authoritative populated split/inspection registry is absent; synthetic membership stays UNASSIGNED and split-dependent claims are blocked.
- Ghost6/BetGuru consumer population/profile/evidence displays and BetGuru quote compatibility remain external work.
- Fresh independent implementation review and Ghost final vet are pending; prior Grok review predates this code.

## Evidence and scope

See `EVIDENCE_CODEX.json` for the exact command, HEAD/branch, touched-file hashes, pytest XML/log, durable artifact hashes, source snapshot, blockers and scope audit. `JOINT_PRODUCER.md` documents the API/input format; the clearly labeled synthetic fixture is the runnable format example. No real player identity, role charting, coverage, route or personnel data was invented. No excluded calibration tree contents were accessed or edited, and no betting rules, settlement code or consumer quote matching were changed. Cursor Cloud was not used.

**Impact: NOT MEASURED.** No same-evaluation baseline → after predictive metrics exist for this pass.
