**VERDICT: REJECT_FINAL_ACCEPTANCE**

**GAPS**
- Direct unchanged producer → market adapter call fails with `ValueError: missing trial fields` (B01, test_DIRECT_actual_producer_to_market_acceptance).
- Producer wire mismatches on status object vs. scalar + siblings, freeze.input_manifest_digest vs. input_manifest_hash, engine.component_version/dependencies vs. component_versions/dependency_versions, and team_periods[].stats.points vs. .points.
- No certified real-game source inventory, canonical crosswalk/registry, as-of frozen bundles, or projection_ready=true (B04; only synthetic SCENARIO_ONLY trials with 0 adapter-usable).
- No verified canonical alias/holdout handling, quote pairing beyond SAVED_ONLY research files (Pinnacle Q2–Q4 missing → NOLINE), book_rules_verified=false, or full OT/penalty/return/PBP rules (B02, B05).
- Bias unfitted, no predictive metrics/same-eval baseline, impact NOT_MEASURED, no live workflow completion (B06/B07).
- Market 109 and CORE 88 are separate engineering suites only; they do not substitute for the failing integration test.

**FALSE-PASS RISKS**
- 59/60 pytest passes rely on diagnostic/test-only field mapping, opaque payload retention, or optional expected_trial_ids omission; these do not exercise the direct unchanged-producer path required for acceptance.
- Synthetic smoke trials validate CORE accounting but remain SCENARIO_ONLY and projection-blocked; diagnostic probes (score sensitivity, red-population, alias rejection) characterize gaps rather than close them.
- Prior Grok_core_producer_review.md issued ACCEPT_WITH_GAPS on captured CORE evidence only; it explicitly notes no re-execution and leaves consumer adapter verification external.
- GHOST_HANDOFF_MARKET_ADAPTER.md documents required fields and procedural guardrails (expected_trial_ids mandatory, no filtering/repair); the integration packet reproduces the exact rejection with no hidden xfail/shim.

**REQUIRED BEFORE GHOST FINAL ACCEPTANCE**
- Align producer wire schema to satisfy adapt_joint_trials without mapping (owner-reviewed change, then rerun direct test with unchanged producer rows).
- Supply and authenticate real as-of inventory, canonical crosswalk, brainstorm/checklist/report, and complete 15-phase workflow to achieve projection_ready=true and v1.1.1 gate passage.
- Verify full population procedure with independently retained expected_trial_ids, alias-wide inspection registry, quote/core envelope, and sportsbook rules.
- Complete external BetGuru/consumer-side integration, bias fitting, predictive validation, and Ghost final vet on non-synthetic inputs.
- Regenerate acceptance packet showing 60/60 passes on direct test plus live evidence.

**NOTES**
- All evidence read-only per instructions; no shell, pytest, network, or writes performed. INTEGRATION_EVIDENCE.json, GHOST_ACCEPTANCE_PACKET.md, and integration_pytest.log consistently report disposition BLOCKED_NO_GHOST_FINAL_ACCEPTANCE with exit code 1.
- GHOST_HANDOFF_MARKET_ADAPTER.md and grok_core_producer_review.md both emphasize that synthetic/diagnostic passes and separate suite counts do not authorize final acceptance or projections.
- Contract SHA-256 matches; file hashes and pre/post snapshots confirm no unauthorized changes. Direct producer→market failure is the explicit blocker noted in the query.
