**VERDICT: REJECT**

The current implementation in `/workspace/wt-nfl-sim-core-2026-11-06` (and its research subdirectories) does not satisfy the normative requirements of `nfl-sim-core-contract-v1`. The contract and checklist explicitly state that phase 1 is documentation-only; no engine, schema, or adapter implementation exists. The `core_contract.checklist.json` records every gate as `NOT_IMPLEMENTED_IN_PHASE_1`, `NOT_RUN`, or `NOT_RUN`.

**GAPS**

- No stable canonical `game_id` / `player_id` (with `game_id_namespace`, `player_id_namespace`, frozen crosswalk, unresolved-player propagation, or alias joins). Existing code relies on names, nflverse IDs without verified registry joins, and display-name bootstrapping.
- No `forecast_id` (sha256 of canonical run spec), `trial_id` (`<forecast_id>/trial/<trial_index>`), per-trial deterministic seeds derived from the specified SHA-256 scheme, `cutoff_utc` with separate `frozen_at_utc`/`generated_at_utc`, complete frozen input manifest, `input_content_hash`, or versioned `engine`/`rng`/`config`/`mode` objects.
- No joint trial output schema matching the required `trial_required_objects` (no `latent_state`, ordered `events` with opportunity-before-yard provenance, `possessions`, `team_periods`/`player_periods` with primitive + aggregate reconciliation, `feature_availability`, structured `flags`/`validation`/`provenance`).
- No explicit regulation/OT/quarter boundaries, possession transitions, clock partitions, or `INCOMPLETE` flagging for cap termination/safety-cap draws. Existing engines treat period clock and game time inconsistently; OT is labeled `single_possession_approx_declared_limitation`.
- No opportunity-first generation: targets/carries are not allocated before yards with shared depth/rotation uncertainty and traceable `provenance_refs`/`generation_stage`. Research possession engine bootstraps historical outcomes and credits yards via names.
- No attempt-conservation ledger exposing the exact equations for dropbacks, pass/rush attempts, throwaways, spikes, sacks, scrambles, kneels, aborted plays, eligible targets, unassigned buckets, and residuals. No per-trial/per-period/per-team validation that produces `INVALID` status.
- No `catches <= targets`, yard-credit reconciliation with visible laterals/fumbles/adjustments, or zero-opportunity handling. Existing accounting does not enforce or expose these invariants.
- Coverage is treated as UNKNOWN (correctly flagged in TNF audit), but routes and 11/12/13 personnel remain MISSING with no propagation of `default_missing_features` statuses through events or adapters. No prohibition on fabricating effects.
- No BetGuru quote adapter preserving all required fields, exact both-side/all-outcome pairing under identical snapshot/co-observation rules, or deterministic `NOLINE` status for any mismatch (identity, timestamp, line, period, OT scope, settlement, trial population).
- No frozen disjoint train/dev/holdout manifests; TNF game (source alias `401873037`) is postgame inspected evidence and cannot be untouched holdout. Split IDs are `UNASSIGNED` (correct per contract note) but no inspected-data exclusions or lineage are enforced.
- Phase-1 scope violations in surrounding research trees (e.g., period/possession engines, configs, manifests, runs) that mix data-only, script-adjusted, and market-informed modes, use non-deterministic or legacy seeding, and do not isolate the joint ledger.

**FALSE-PASS RISKS**

- A producer could output period aggregates or player-yard samples from independent bootstraps/period engine draws, label them a “joint trial,” and claim C05/C09 pass without opportunity-before-yards causality (C06), attempt equations (C07), or credit conservation (C08). Residuals could be hidden in unassigned buckets or zeroed without visible flags.
- Legacy name-based or post-yard opportunity inference could be presented as “MODELED” with fake provenance, bypassing causal traces.
- Independent marginal resampling or trial shuffling between Ghost6 and BetGuru adapters could masquerade as identical populations if `trial_id` is omitted or only positional.
- TNF/postgame data or inspected W1–8 games could be quietly included in a claimed “untouched holdout” without manifest-level inspected-data exclusion or `UNASSIGNED` enforcement.
- Missing features (routes, personnel, coverage) could be silently dropped instead of propagated as `MISSING`/`UNKNOWN` with `allows_sim_effect: false`, allowing unsupported measured-role claims.
- Quote mismatches could be normalized to a line or dropped instead of emitting `NOLINE` with explicit reason codes.

**REQUIRED TESTS** (before Ghost final vet; must cover contract-specified boundary cases)

- Replay identical `trial_id` across worker order, retries, and runtime versions using the exact seed-derivation hash; verify bitwise match on all ledger fields.
- End-to-end invariant checks on every trial: all §5 attempt equations, catches ≤ targets, yard-credit reconciliations (including unassigned, laterals, fumbles), period aggregations (Q→H→REG→FG, OT separate), clock partitions summing to 3600 regulation seconds.
- Trace every target/carry to a pre-yard generation stage with provenance; reject any yard-derived or post-facto opportunity counts.
- Propagate and assert `feature_availability` defaults for coverage UNKNOWN, routes/personnel MISSING through events, periods, aggregates, and both adapters.
- Quote adapter tests: deliberate mismatches (different snapshots, timestamps, books, periods, OT inclusion, settlement rules, unresolved player IDs, trial population differences) must return `NOLINE`; matched pairs must share exact `pair_id`, snapshot, and rule ref.
- Split-manifest validation: TNF game excluded from untouched holdout; inspected games flagged; no split-dependent claims on `UNASSIGNED` IDs.
- OT, incomplete-cap, safety-cap, throwaway, spike, sack, scramble, kneel, non-QB throw, aborted-snap, nullified-play, target-bearing INT, halftime transition, and zero-opportunity player test cases; all must produce correct status (`COMPLETE`/`INCOMPLETE`/`INVALID`) and visible residuals/flags.
- Adapter join test: Ghost6 and BetGuru must consume identical `(forecast_id, trial_id)` sets with no reseeding or marginal redraws.

**NOTES**

The contract is complete, rigorous, and correctly identifies all phase-1 limitations and out-of-scope items. The research possession and period engines are explicitly called out as non-compliant context (name-based bootstrapping, independent draws, clock mislabeling, approximate OT, postgame TNF audit only). No metrics, betting-rule changes, new coverage/routes fabrication, or calibration work were claimed or performed. The checklist JSON and Markdown together provide a machine-verifiable acceptance framework; current code satisfies none of the runtime gates. Implementation of the shared ledger, deterministic IDs/seeds, opportunity-first causality, conservation invariants, explicit missingness propagation, and quote adapter must precede any vetting or use by Ghost6/BetGuru.
