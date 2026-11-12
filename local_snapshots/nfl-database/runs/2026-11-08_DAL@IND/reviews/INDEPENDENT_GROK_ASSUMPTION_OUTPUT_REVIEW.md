# Independent Grok review — model assumptions & outputs vs research quotes
**Reviewed_et:** 2026-11-06 07:54 EST
**Scope:** CORE prospective DAL@IND; not schema test counts; not Ghost final.

## Assumptions reviewed
- model_version / flags: dal-ind-w1-8-empirical-v1 / ['COVERAGE_DISABLED', 'QUOTES_NOLINE', 'EMPIRICAL_PARTIAL_SEMANTICS', 'COARSE_DOWN_STATE', 'CLOCK_PROXY', 'ROLES_DEPTH_ONLY', 'NO_OUT_OF_SAMPLE_VALIDATION']
- sample_size: 1068 reason: Retained supported DAL/IND offensive plays; exclusions in training_evidence.json
- uses_market: False provenance_refs: ['model', 'registry']
- usage_cells: 8 outcome_cells: 20
- Coverage/routes/personnel: allows_sim_effect=false (MISSING).
- OT: single_possession_approx_declared_limitation (NOT official).
- Catch distributions pooled across teams by terminal (Codex-noted interface limit).
- Distance/field/score/period deliberately unconditioned in usage cells (down×team only) → structural limitation.
- Training: W1–8 only; leakage controls documented in training_evidence.

## Empirical joint n=5 outputs (fitted, seeded reproducible)
- before (placeholder): forecast sha256:3a418ca043c0f5d1c… means DAL=22.0 IND=30.4
- after (fitted): forecast sha256:09f1c4336d5f62c61ffcc0c2c9771733f924e51d309b9841979369c665961403 means DAL=27.2 IND=14.2 (n_usable=5/5, validations all PASS)
- reproducibility identical_forecast_id_and_score_means: True
- pytest joint_producer: 81 passed (Codex staged)

## Empirical possession n=500 (NONINTEGRATED / SHARED_PARTIAL evidence)
- score_means fg_away(DAL)=22.012 fg_home(IND)=12.722 p_ot=0.026 seed=1329861859
- Do not average joint n=5 with empirical n=500 into one edge.

## vs BetGuru RESEARCH snapshot (NOT verifiedquote; actionable NOLINE)
- DK observed fetch 2026-11-06 07:50:49 ET: DAL spread -5.5, total 51.5, ML DAL -230 / IND 190
- Joint fitted mean margin (DAL-IND)=13.0; DK line implies DAL favored by 5.5.
- Joint fitted mean total=41.4; DK total 51.5.
- Empirical n500 mean margin (DAL-IND)=9.3; total=34.7.
- Interpretation: RESEARCH_OBSERVED_FETCH_TIME_NOT_VERIFIED_QUOTE comparison only. Joint n=5 means are **high-variance** (5 trials) and **not** a market edge. Empirical n500 DAL-heavy means diverge from DK favorite magnitude — diagnostic tension, not acceptance.
- Strict actionable quotes remain **NOLINE** (Pin blocked, Circa missing, bridge LOGIN_REQUIRED, missing book_last_update).

## Verdict
- Conservation/OT/unusual zero-yard plumbing: PASS on fitted joint suite (81).
- Predictive calibration / Ghost acceptance: **NOT CLAIMED**.
- Independent path preserved (data_only); research quotes not conditioned into freeze.
- Remaining genuine blockers: Phase15 inactives; actionable multi-book quotes; coverage/NGS; Bias unfitted; full shared accounting lineage; n=5 ≠ production 100k triad.

## Addendum — forecast ID reconciliation (2026-11-06 07:58 EST)
Authoritative after/repeat forecast_id is now `sha256:40c23caa5a0327c8ebc757520ad430e1401305518cd653549d542cc0300a3919` (means unchanged DAL 27.2 / IND 14.2). Earlier cites of `09f1c433…` / `3a418ca0…` are superseded by engine source-hash / validation-order fixes — see `codex_usage_fit/FORECAST_ID_RECONCILIATION.json`. Independent Codex review flagged this mismatch; score means agreed throughout.
