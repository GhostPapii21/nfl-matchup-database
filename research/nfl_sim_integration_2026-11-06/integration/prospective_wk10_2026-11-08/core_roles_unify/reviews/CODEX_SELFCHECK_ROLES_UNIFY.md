# Codex self-check — roles and unify

This is the implementing agent's self-check, not an independent human or second-agent review. All substantial code was written in this session; no delegation.

Assumptions: registry ACT/availability/positions authoritative for this replay; questionable retained with uncertainty; no unpublished Phase15 inference. Team empirical prior has zero mass for unobserved actors and half-state concentration 20, chosen as documented regularization, not tuned on holdout. Posterior intervals do not cover game correlation, estimated-prior uncertainty or model bias. Role IDs from all W1–8 extract rows are conditional eligible-actor shares; outcome/usage support has different exclusions. Role-only pooled holdout does not validate half-state forecasts or overall joint score accuracy.

| Role | W1–8 n | Same-set KL equal / empirical | Heldout KL equal / empirical | Heldout MAE equal / empirical |
|---|---:|---:|---:|---:|
| DAL passer | 316 | 0.6931 / 0.0000 | 0.6931 / 0.0000 | 0.5000 / 0.0000 |
| DAL target | 297 | 0.5479 / 0.0000 | 0.8695 / 0.2156 | 0.0926 / 0.0391 |
| DAL carry | 190 | 0.7384 / 0.0000 | 0.6668 / 0.0712 | 0.1829 / 0.0518 |
| IND passer | 293 | 1.0415 / 0.0000 | 0.9001 / 0.7648 | 0.4111 / 0.0333 |
| IND target | 247 | 0.5664 / 0.0000 | 0.5790 / 0.0912 | 0.0638 / 0.0188 |
| IND carry | 218 | 0.8375 / 0.0000 | 0.4528 / 2.2576 | 0.1303 / 0.1047 |

IND carry KL deterioration is retained. All metrics and raw sample sizes are in JSON. Same-set identity is expected. Legacy-depth baseline also reported separately, avoiding confusion with eligible-player equal baseline.

One forecast_id lineage and common event credits in shared mode; adapter rederives team/player/period/aggregate tables and rejects mismatch/failed validation. n=5 before and after: zero conservation/bridge failures; exact after repeat including player opportunities. Legacy empirical path is not retroactively unified. No full NGS/coverage integration claim.

86 targeted tests green; broader suite 126 pass / 36 fail, including missing parquet and legacy API failures. Frozen source/input snapshots and forecast IDs are retained. No old JSON edits.

Blocked: external delivery under restricted writable roots (exact copy commands staged); Phase15 NOT_YET; actionable quotes NOLINE; coverage/routes/personnel/NGS unavailable and effects disabled; full football semantics incomplete. DEFERRED_100K_UNFINISHED_SEMANTICS. No picks or betting-rule changes; data_only independent from market anchoring.

Additional explicit cross-check: 60 player + residual = team opportunity/yard assertions passed across all five trials and both teams. See shared_opportunity_yards_crosscheck.json. Period tables and score attribution also match derive_tables.
