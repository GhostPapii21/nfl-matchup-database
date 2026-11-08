# DAL @ IND preliminary research report

The pre-cutoff empirical fit is complete in the CORE staging directory. This is a historical-as-of research replay, not a claim that the new fit was computed at the original freeze time. Original cutoff, freeze, generation clocks, registry and split bytes are preserved. No certified_asof labels were rewritten. Game is week 9 despite the wk10 directory name. 2026-11-06T01:15:00Z denotes the Thursday 20:15 EST kickoff, not postgame.

The fit retained 1068 of 2665 extract rows, with eight team/down usage cells and 20 team/terminal/catch outcome cells. See ../training_evidence.json for exhaustive exclusions and counts, ../training_records.json for selected game/play IDs, and ../inputs/model.json for distribution frequencies and Wilson intervals. 14 outcome cells have n<30 and carry SPARSE_STATE/LOW-SAMPLE. These intervals are descriptive play-level intervals; they do not address game clustering, selection bias or predictive model error.

Usage cells never pool teams. Outcomes remain team-specific, with down/distance/field/score deliberately unconditioned. Catch probabilities explicitly pool the two teams because the current API is terminal-only. Rare or unseen categories get no invented probability; missing states reject execution. Timing uses positive adjacent within-quarter PBP clock deltas up to 60 seconds; excluded zero/long gaps and unsupported penalty/fumble/lateral/return plays cause selection bias. Punt return yards only inform net punt distance; no return-score/defensive credit model is claimed.

Using base seed 20261108, the same-engine placeholder baseline score means were DAL 22.0, IND 30.4; fitted means were DAL 27.2, IND 14.2. These are five-draw diagnostics, not accuracy improvements or picks. Baseline and fitted trials each completed 5/5 with zero invalid/incomplete draws and all conservation validations PASS. The fitted repeat matches forecast_id sha256:40c23caa5a0327c8ebc757520ad430e1401305518cd653549d542cc0300a3919 and score means exactly. Full seed derivation and trial seeds are in ../reproducibility.json and frozen run_spec.json.

PATH status is SHARED_PARTIAL_SEMANTICS. All 2,665 extract rows match the empirical parquet on game/play IDs, team/down/type/yards/completion/interception; the larger filtered parquet also has 121 no_play and 34 null-type rows absent from the extract. Opportunity allocation, conditional-state partitioning, player role weights, yard generation, credit rules, OT implementation, seeds and forecast identities remain nonintegrated. Do not blend forecasts or call this end-to-end integration.

Coverage/routes/personnel stay disabled. Player role/depth/availability, environment and try-point assumptions remain from the existing model. OT is the declared single-possession approximation, not an official NFL rules certification. Predictive calibration, held-out evaluation and complete research phases remain unfinished. The 82-test joint suite passes, including new zero-yard incomplete/punt/missed-FG OT regressions. Validation check order is sorted for cross-process byte stability. Source hashing now excludes generated runs/artifacts so writing replay snapshots cannot change the next forecast identity.

Genuine temporal blockers are unpublished inactives and odds-bridge LOGIN_REQUIRED, inherited from packet evidence and not freshly tested. No Odds requests/spend or auth bypass occurred. Quotes remain NOLINE; no market_informed conditioning or market_calibration edits. Missing charting, film, QB/defense work and held-out validation are unfinished research, not temporal blockers.

Delivery limitation: the requested packet and /workspace/nfl-database/runs/2026-11-08_DAL@IND are read-only under this session policy. This report/checklist and updated packet inputs are staged in CORE; the external folders have not been updated. No permission bypass was attempted. See DELIVERY.md for exact destinations.

All 15 phase dispositions follow.

**Phase 1 — Data pull: PASS.** Guarded 2026 W1–8 PBP fit; 2,665 extract rows, 1,068 supported DAL/IND offense rows retained. Scope is PBP, not all ancillary research sources.

**Phase 2 — Opportunity: UNVERIFIED.** Empirical team/down terminal cells fitted; player rotation, depth and availability remain supplied depth-model assumptions, not empirically validated shares.

**Phase 3 — Defense profile: MISSING.** No opponent-adjusted defense profile fitted; team offensive cells do not establish defensive matchup effects.

**Phase 4 — Defender coverage: MISSING.** Coverage UNKNOWN; routes/personnel MISSING; all allows_sim_effect=false.

**Phase 5 — Pressure/blitz/checkdown: MISSING.** No charted pressure/blitz/checkdown integration. Historical sacks/scrambles alone do not certify this phase.

**Phase 6 — QB card: MISSING.** No graded QB card or protection/clutch validation completed.

**Phase 7 — Role/snaps: UNVERIFIED.** Existing registry/depth rotation preserved; no charted routes/snaps fit or final inactive confirmation.

**Phase 8 — Injuries: UNVERIFIED.** Frozen preliminary availability retained; no new source acquisition. Inactives unresolved; questionable players remain uncertain.

**Phase 9 — NGS: MISSING.** No NGS evidence integrated.

**Phase 10 — Film: UNVERIFIED.** No film-to-PBP re-match performed.

**Phase 11 — Environment: UNVERIFIED.** Existing retractable-roof environment retained; roof state not certified, no new weather acquisition.

**Phase 12 — Source audit: UNVERIFIED.** PBP leakage assertions and source overlap PASS; inherited as-of declarations retained, not independently reauthenticated. Destination delivery blocked by filesystem policy.

**Phase 13 — Game script: UNVERIFIED.** Shared score state drives the joint engine, but fitted usage cells condition only on team/down. No calibrated lead/trail script effects or market anchoring.

**Phase 14 — Models/price/edge: UNVERIFIED.** Joint fit/replay/conservation PASS; predictive accuracy NOT MEASURED, n=5 smoke only. Quotes NOLINE; price/edge N/A, no picks.

**Phase 15 — Inactives: NOT_YET.** Inactives unpublished at frozen cutoff. Final inactive checks must wait until publication; do not infer Active from absence of an Out designation.
