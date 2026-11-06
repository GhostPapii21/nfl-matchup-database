# Completion phases and fit — preliminary research

Empirical fit, same-clock refreeze, n=5 replay and conservation checks are complete in CORE staging. Requested external delivery remains MISSING because both destination folders are outside writable roots.

| Metric | Before (same current engine) | After |
|---|---|---|
| Empirical sample size | null / placeholder | 1,068 supported plays |
| Usage cells | 1 placeholder | 8 team/down cells |
| Outcome cells | 5 deterministic | 20 empirical cells |
| Complete / invalid / incomplete draws | 5 / 0 / 0 | 5 / 0 / 0 |
| DAL score mean (n=5) | 22.0 | 27.2 |
| IND score mean (n=5) | 30.4 | 14.2 |
| Conservation | 5/5 PASS | 5/5 PASS |
| Forecast ID | sha256:95030358bf7828484619af6561febb9544390071a9f7602a1da9901264727481 | sha256:40c23caa5a0327c8ebc757520ad430e1401305518cd653549d542cc0300a3919 |

Fitted repeat forecast ID and score means match exactly. Base seed 20261108; PCG64 and sha256-first-eight-big-endian-v1 trial derivation. All individual seeds are in reproducibility.json. Joint pytest: 82 passed, including three new zero-yard OT cases and generated-source enumeration regression. Five draws provide no accuracy evidence. Original packet summary had a contradictory 5/5 claim alongside an INCOMPLETE row; this report uses newly computed trial populations instead.

Fit evidence: training_evidence.json, training_records.json, inputs/model.json, pbp_bridge_verification.json. Selected rows strictly season 2026 W1–8, no target-game actuals, no market prices. Fitted model provenance_refs is exactly ['model','registry']; feature effects stay false. Model/cell counts and Wilson uncertainty retained in decision traces. Catch pooling is explicitly DAL+IND; all other cross-team pooling is absent. 14 outcome cells are SPARSE_STATE/LOW-SAMPLE. Missing support never silently pools.

Cutoff 2026-11-06T12:40:00Z, freeze 12:45Z, generated 12:50Z retained verbatim as requested. These are inherited as-of replay clocks, not new wall-clock fit timestamps or independent source certification. No frozen certified_asof rewrite. Week is 9; 2026-11-06T01:15Z is TNF kickoff.

PATH: SHARED_PARTIAL_SEMANTICS. The exact overlap and remaining separate opportunity/role/outcome/accounting/OT/seed/forecast paths are documented in PATH_SEMANTICS_JOINT_VS_EMPIRICAL.md. No full integration claim.

Temporal blockers: inactives not published at cutoff (Phase 15 NOT_YET); odds auth LOGIN_REQUIRED (packet status, no bypass or fresh spend). Other missing phases are research gaps, not temporal blockers. data_only; quotes NOLINE; no picks. See nfl-database-run/checklist.md and report.md for all 15 truthful phase dispositions.

The source-hash reproducibility defect was fixed: generated runs/artifacts snapshots no longer enter runtime source hashes. Old frozen artifacts are untouched; newly frozen runs have new engine/input identities. Before-fix failed experiments were diagnostic, not accepted forecasts.

A second fresh Python process matched all existing artifact bytes, forecast IDs and score means. A dedicated different-PYTHONHASHSEED regression verifies trial byte stability. External packet/run copies appeared during this session; they were not written or reconciled by this agent. Local staging is the verified deliverable.

## Superseding roles/accounting update

See ../dal_ind_roles_unify/COMPLETION_ROLES_UNIFY.md and completion_metrics.json there. New path SHARED_ACCOUNTING_V1, empirical team/half roles, role W7–8 holdout, same-clock n=5 replay and exact seeded repeat. Historical results above are unchanged; no whole-suite green claim (86 targeted pass; broader suite 126 pass / 36 fail). External delivery remains staged. Phase15 NOT_YET, quotes NOLINE, no picks.
