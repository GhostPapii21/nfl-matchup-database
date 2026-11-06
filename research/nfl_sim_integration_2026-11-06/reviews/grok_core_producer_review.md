**VERDICT: ACCEPT_WITH_GAPS**

**GAPS**
- Real-game canonical registry, crosswalk joins, sourced availability/depth/rotation/target-depth/outcome distributions, and as-of frozen bundles are absent (synthetic fixtures only; C01, C02, C06, C12 remain BLOCKED per CORE_MANIFEST.json and EVIDENCE_CODEX.json).
- Official OT, penalty/untimed-down semantics, defensive/special-teams returns, and legacy raw-PBP ingestion are explicitly unsupported or projection-blocked (C04, C05, C07).
- Consumer-side Ghost6/BetGuru integration, quote compatibility, evidence displays, and full-population verification are external (C09, C11).
- No predictive metrics, historical PBP/TNF simulations, or same-eval baseline; impact remains NOT_MEASURED as required.

**FALSE-PASS RISKS**
- 88 pytest passes (synthetic plumbing, accounting invariants, corruption detection, opportunity-before-yard ordering via Spy, clock/possession/ledger reconciliation, seed/replay determinism, INVALID on mutation) are fully consistent with the code in joint_producer.py, joint_accounting.py, joint_inputs.py, test_joint_producer.py, JOINT_PRODUCER.md, COMPLETION_CODEX.md, and EVIDENCE_CODEX.json. No re-execution occurred. Tests deliberately target contract §4–5 causal order, §5 exact integer conservation equations (including residuals/unassigned, laterals/signed adjustments, bounds), §2–3 identity/freeze/seed rules, missingness propagation, and fail-closed behavior. No evidence of false positives on real data or unsupported features.
- Validation recomputes the full ledger end-to-end in validate_trial/finalize_validation; trial status is set to INVALID on any invariant failure, residuals, SCENARIO_ONLY, or incompleteness. Projection blockers are explicitly surfaced. No hidden false-PASS paths observed.

**REQUIRED BEFORE GHOST FINAL VET**
- Supply and independently authenticate authoritative real-game/player/team registry + crosswalk (C01).
- Provide certified as-of frozen source bundles for availability, depth, rotation, intended-depth, and outcome distributions (C02, C06).
- Complete external consumer adapter verification for shared trial population and quote pairing (C09, C11).
- Ghost final-vet of full joint schema, provenance, and blocker propagation on non-synthetic inputs.

**NOTES**
- Implementation strictly follows nfl-sim-core-contract-v1 (core_contract.md) for opportunity-first generation (targets/carries before yards/outcomes), exact integer accounting with visible unassigned buckets and signed adjustments, frozen inputs/manifests/hashes/seeds, clock/period/possession boundaries, missingness (coverage UNKNOWN; routes/personnel MISSING with allows_sim_effect=false), and joint JSONL schema with ledger-derived periods/aggregates.
- All synthetic tests, smoke runs (2 COMPLETE trials, 0 usable due to SCENARIO_ONLY), git checks, py_compile, and hash immutability pass per captured evidence. No real data, calibration, betting rules, or excluded trees touched.
- CORE_MANIFEST.json accurately reflects implemented vs. BLOCKED/UNIMPLEMENTED gates. Prior self-review noted; this is independent adversarial read-only review of captured evidence only. No shell, pytest, network, or code writes performed.
