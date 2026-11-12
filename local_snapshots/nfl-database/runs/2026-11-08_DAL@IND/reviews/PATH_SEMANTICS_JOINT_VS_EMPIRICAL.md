# Joint producer vs empirical possession — path semantics (updated after usage-cell fit)

## Status: SHARED_PARTIAL_SEMANTICS (not full integration)

### Shared
- Pre-cutoff PBP evidence: DAL/IND season 2026 weeks 1–8 only.
- Bridge check `reviews/codex_usage_fit/pbp_bridge_verification.json`: **PASS_SHARED_SUBSET** — every training-extract row equals matching empirical parquet row; extract ⊂ empirical population (excludes no_play/NULL extras).
- Leakage controls: no week≥9 rows; no 401873040 postgame; no market prices in model.
- Quotes remain NOLINE / uses_market false on both paths.

### Still nonintegrated (do not blend as one forecast)
| Aspect | Joint (fitted n=5) | Empirical (n=500) |
| --- | --- | --- |
| Opportunity | Frozen usage_cells (team×down multinomial) + role_states | Resample historical play rows by state key |
| Yards | Discrete outcome_cells (empirical yards distributions per terminal) | Direct yards from resampled PBP row |
| Roles/identity | Registry ACT + availability; depth-informed roles | Player from historical play row |
| Accounting | Integer joint_accounting + conservation validators | Aggregate score/player_joint summaries |
| OT | Declared single_possession_approx profile | Config ot_rule approx |
| Forecast lineage | freeze_run forecast_id / input_content_hash | stable_seed(config) summary JSON |
| Catch model | catch_distributions pooled across teams by terminal | Implied by resampled complete_pass |

### Integration acceptance (still NOT claimed)
Full acceptance requires shared forecast lineage OR an explicit cross-check harness proving opportunity→yard→credit conservation equivalence trial-by-trial. Current: complementary evidence only. `projection_ready=false`.
