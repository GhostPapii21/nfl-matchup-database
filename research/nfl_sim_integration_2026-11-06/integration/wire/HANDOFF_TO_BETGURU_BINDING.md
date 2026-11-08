# Handoff → BetGuru (binding only)

CORE phase4 complete. Adapter implementation from B01 Codex is present.
Current-env verification failed solely on contract SHA guard.

**Do this next (market_calibration only; CORE will not edit it):**
1. Read `CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md`
2. Point adapter/MANIFEST bound SHA to `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`
3. Update `WIRE_AGREEMENT_v1.0.1.md` to cite the authorization (content contract still v1.0.0 semantics; wire still `1.0.0-producer`)
4. Re-run market suite + DIRECT without override/remap
5. Prefer also proving against immutable example `producer_joint_trial_example_v1.jsonl` @ `50be826a…` in addition to smoke `1f9ac512…`

Preserve NOLINE / Bias UNIMPLEMENTED / no Ghost final claim until DIRECT greens.
