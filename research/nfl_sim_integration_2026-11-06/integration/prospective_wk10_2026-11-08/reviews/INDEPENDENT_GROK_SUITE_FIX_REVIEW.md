# Independent Grok adversarial review — suite fix / robust roles / score invariance
**Reviewed_et:** 2026-11-06 08:25 EST

## Full suite
- Before 36 fail / 126 pass → after **167 pass / 0 fail**. Classification claims all 36 = MISSING_DEPENDENCY_OR_FIXTURE (PBP symlink). Cascading KeyErrors (player_samples, NoneType) are consistent with missing history. Accept fixture restore; note that “0 REAL_REGRESSION” is only as strong as classification honesty — protected old artifact hashes still match.

## IND carry
- Unshrunk MLE inspected KL 2.26 correctly flagged **EMPIRICAL_IND_CARRY_REGRESSION** and **not promoted**.
- Selected `mix_equal_0.25` on train/dev only; W7–8 inspected-holdout KL 0.15 vs equal 0.45 / MLE 2.26 — better on that metric but **mixed** across roles; W6 is one-game limited. Same-set KL≈0 correctly called tautological. Accept ROLES_POLICY_ROBUST staging with limits.

## Score sensitivity 27.2→18.8
- Root cause: trial seed hashed full inputs including rotation weights → RNG confound. Fix: seed policy v2 + separate player-attribution RNG; team scores/play counts identical across equal/empirical/robust (DAL 21.8 / IND 13.6). Original 8.4-pt delta **not** causal efficiency. Good adversarial finding.

## Semantics
- Penalties/returns/official OT = UNSUPPORTED stubs, not fitted — correct engineering honesty. DEFERRED_100K justified.

## Blockers
Phase15 NOT_YET; quotes NOLINE; coverage MISSING; role validation still thin (W6 one game); OT approx. projection_ready=false. No picks.
