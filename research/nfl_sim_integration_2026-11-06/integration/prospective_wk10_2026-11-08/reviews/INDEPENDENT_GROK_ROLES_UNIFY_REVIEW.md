# Independent Grok review — empirical roles + SHARED_ACCOUNTING_V1
**Reviewed_et:** 2026-11-06 08:07 EST  
**Scope:** CORE DAL@IND roles unify; not Ghost final; not schema-count acceptance.

## 1. Assumptions honesty
- Empirical target/carry/passer shares replace equal-weight depth roles: **verified** in promoted model (all six role cells `equal_weight=False`). DAL carry ~0.705 / 0.147 / 0.126 matches PBP mass; Pierce absent from IND weights.
- Half-state Dirichlet shrinkage (α prior ×20 team empirical) is disclosed regularization, not holdout-tuned — acceptable research assumption if labeled.
- Heldout W1–6→W7–8: most roles improve KL/MAE vs equal; **IND carry KL worsens 0.45→2.26** while MAE improves — Codex retained this; **no predictive superiority claim**. Correct honesty.
- Coverage/routes still disabled; Phase15 NOT_YET; quotes NOLINE — preserved.

## 2. Shared accounting
- PATH upgraded SHARED_PARTIAL → **SHARED_ACCOUNTING_V1**: joint events → derive_tables → one forecast/trial lineage; 60 opp/yard crosschecks fail_count=0.
- Legacy n=500 empirical path **not** retroactively unified (correct). Old sim summary still has stale JAX_BAL string (documented; not rewritten).
- New `source_composition(cfg)` for DAL@IND emits `..._DAL_IND_...` and cannot emit JAX_BAL — verified by import assert.

## 3. Outputs vs research DK (still NOLINE actionable)
- Equal-depth before means DAL 27.2 / IND 14.2 → after roles DAL **18.8** / IND 14.2 (n=5 smoke).
- Research DK: DAL −5.5 / total 51.5. After total ~33 still well below DK; margin DAL−IND=4.6 closer to 5.5 than prior 13.0 — **diagnostic only**, high-variance n=5, **not** edge/acceptance.

## 4. Tests / reproducibility
- Targeted 86 passed including OT/unusual; seeded repeat identical True.
- Full suite 126/36 fail — **not** whole-engine green; missing parquet + legacy API. Do not claim repo-wide green.
- DEFERRED_100K_UNFINISHED_SEMANTICS justified (penalties/returns/OT/coverage unfinished).

## 5. Verdict
Engineering path for roles+shared accounting is **substantially advanced**, not exhausted. Remaining genuine blockers: Phase15 inactives; verified quotes; coverage/NGS; IND carry heldout KL; full-suite legacy fails; unfinished football semantics before any 100k Bias triad. **No picks. projection_ready=false.**
