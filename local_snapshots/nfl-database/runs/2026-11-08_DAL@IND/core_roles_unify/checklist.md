# DAL @ IND preliminary research checklist

Game 401873040 / 2026_09_DAL_IND, week 9. Cutoff 2026-11-06T12:40:00Z. Mode data_only. Quotes NOLINE. No picks.

Statuses assess research completion, not wager approval. Phase 15 uses the explicitly requested NOT_YET status.

| Phase | Research item | Status | Evidence / limitation |
|---|---|---|---|
| 1 | Data pull | PASS | Guarded 2026 W1–8 PBP fit; 2,665 extract rows, 1,068 supported DAL/IND offense rows retained. Scope is PBP, not all ancillary research sources. |
| 2 | Opportunity | UNVERIFIED | Empirical team/down terminal cells and team/half player rotations fitted; pooled W7–8 role holdout reported, including IND carry KL deterioration. Target depth/availability remain assumptions. |
| 3 | Defense profile | MISSING | No opponent-adjusted defense profile fitted; team offensive cells do not establish defensive matchup effects. |
| 4 | Defender coverage | MISSING | Coverage UNKNOWN; routes/personnel MISSING; all allows_sim_effect=false. |
| 5 | Pressure/blitz/checkdown | MISSING | No charted pressure/blitz/checkdown integration. Historical sacks/scrambles alone do not certify this phase. |
| 6 | QB card | MISSING | No graded QB card or protection/clutch validation completed. |
| 7 | Role/snaps | UNVERIFIED | Empirical ACT/available role shares fitted; no charted routes/snaps fit or final inactive confirmation. |
| 8 | Injuries | UNVERIFIED | Frozen preliminary availability retained; no new source acquisition. Inactives unresolved; questionable players remain uncertain. |
| 9 | NGS | MISSING | No NGS evidence integrated. |
| 10 | Film | UNVERIFIED | No film-to-PBP re-match performed. |
| 11 | Environment | UNVERIFIED | Existing retractable-roof environment retained; roof state not certified, no new weather acquisition. |
| 12 | Source audit | UNVERIFIED | PBP leakage assertions and source overlap PASS; inherited as-of declarations retained, not independently reauthenticated. Destination delivery blocked by filesystem policy. |
| 13 | Game script | UNVERIFIED | Shared score state drives the joint engine, but fitted usage cells condition only on team/down. Half-state roles fitted with team-prior shrinkage; no calibrated lead/trail effects or market anchoring. |
| 14 | Models/price/edge | UNVERIFIED | Joint fit/replay/conservation PASS; role-only retrospective heldout measured; score accuracy NOT MEASURED, n=5 smoke only. Quotes NOLINE; price/edge N/A, no picks. |
| 15 | Inactives | NOT_YET | Inactives unpublished at frozen cutoff. Final inactive checks must wait until publication; do not infer Active from absence of an Out designation. |

Shared path SHARED_ACCOUNTING_V1; 86 targeted tests pass, broad suite 126 pass / 36 fail. n=5 joint/shared conservation failures zero; exact repeat verified. Delivery staged. 100k DEFERRED_100K_UNFINISHED_SEMANTICS. See core_roles_unify/COMPLETION_ROLES_UNIFY.md.
