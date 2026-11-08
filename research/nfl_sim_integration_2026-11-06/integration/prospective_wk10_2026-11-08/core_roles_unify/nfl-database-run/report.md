# CORE roles and accounting completion

Implemented empirical pre-cutoff rotation weights and SHARED_ACCOUNTING_V1. Research-only; external delivery staged, not executed. Completion metrics (including NFL-16 parent logging payload): completion_metrics.json.

Training reads only packet records/pbp_DAL_IND_w1_8.csv.gz, season 2026 W1–8, with assertions excluding week >=9, target game and dates at/after cutoff. The supported usage/outcome fit retains 1,068 plays. Role counts use all identified offensive PBP actors in the permitted extract, not only the 1,068 clock-filtered plays: passer IDs (including sack-associated IDs), receiver IDs and rusher IDs. Counts are conditional on registry ACT ∩ AVAILABLE/AVAILABLE_WITH_UNCERTAINTY and position eligibility QB / WR,TE,RB / RB,QB respectively. Missing IDs are dropped; explicit exclusion counts cover identified actors failing eligibility. Pierce IR/RES is excluded. Questionable status is unchanged. No unsupported player is invented.

Team empirical proportions replace depth-role equal weights. Half 1 (Q1–Q2) and half 2 (Q3 onward including OT) use Dirichlet counts + 20 times team empirical prior; sample sizes, posterior alpha, shrinkage strength and SPARSE_STATE/LOW-SAMPLE (<30) are stored per cell. A team role with no supported actors gets explicit UNASSIGNED, never uniform or league pooling. Zero observed team player mass stays zero: this is an empirical-Bayes assumption, not evidence a player cannot appear. Within-game dependence and estimated-prior uncertainty are unadjusted. Coverage/routes/personnel remain allows_sim_effect=false.

Role validation is chronological W1–6 train, W7–8 holdout, at pooled team-role share level; half-conditioned rotations are not separately heldout-validated. Same-set evaluation uses W1–8. Equal baseline is explicitly equal over registry eligible players; legacy_depth baseline over the old depth-role weights is also in JSON. Evaluation adds 1e-6 count per eligible player to avoid infinite heldout KL; production weights do not use this floor. MAE is mean absolute share error over eligible players. Same-set near-zero error is fit identity, not accuracy evidence. Heldout is retrospective within the inspected development set, not untouched prospective evaluation.

| Role | W1–8 n | Same-set KL equal / empirical | Heldout KL equal / empirical | Heldout MAE equal / empirical |
|---|---:|---:|---:|---:|
| DAL passer | 316 | 0.6931 / 0.0000 | 0.6931 / 0.0000 | 0.5000 / 0.0000 |
| DAL target | 297 | 0.5479 / 0.0000 | 0.8695 / 0.2156 | 0.0926 / 0.0391 |
| DAL carry | 190 | 0.7384 / 0.0000 | 0.6668 / 0.0712 | 0.1829 / 0.0518 |
| IND passer | 293 | 1.0415 / 0.0000 | 0.9001 / 0.7648 | 0.4111 / 0.0333 |
| IND target | 247 | 0.5664 / 0.0000 | 0.5790 / 0.0912 | 0.0638 / 0.0188 |
| IND carry | 218 | 0.8375 / 0.0000 | 0.4528 / 2.2576 | 0.1303 / 0.1047 |

IND carry heldout KL worsens materially (0.4528 → 2.2576), although MAE improves. Unseen W1–6 usage is a limitation; no predictive superiority claim. Full before/after same-set MAE and legacy-depth metrics are in role_training_evidence.json and completion_metrics.json.

Frozen same clocks: cutoff 2026-11-06T12:40:00Z; freeze 12:45Z; generated 12:50Z. No frozen certified_asof rewrite. Week 9 (packet wk10 is a directory misnomer), ESPN 401873040 / nflverse 2026_09_DAL_IND. 2026-11-06T01:15Z is TNF kickoff Thu 20:15 ET, not postgame.

Current-engine equal-depth before vs empirical after, seed 20261108, n=5: score means {'DAL': 27.2, 'IND': 14.2} → {'DAL': 18.8, 'IND': 14.2}. Complete draws 5/5 each; joint conservation fail counts 0 → 0; shared-bridge fail counts 0 → 0. These are smoke results, no betting edges. After forecast: sha256:5cf792ce2fdc9351362ec77c9ed856a46314980745ec4b23622413312803d485. Repeat forecast ID, score means and key player opportunity means match exactly. Frozen trial seeds, model/source bytes and input manifest are in the content-addressed run. Shared projection uses one forecast/trial lineage and derives periods/aggregates from the same event ledger, not a separately simulated forecast.

Tests: red new test collection (missing fit module) → green; 86 targeted tests pass including empirical roles, IR exclusion, questionable retention, config source label, shared projection drift rejection, shared dispatcher, seeded repeat, existing OT/incomplete-pass/punt/FG zero-yard conservation cases. Broader suite: 126 pass, 36 fail; missing historical parquet and legacy API expectations among failures. See test_status.json; no whole-engine green claim.

New empirical summaries derive source_composition from cfg season/history weeks/away/home. Old DAL@IND summary still has stale JAX_BAL; historical JSON bytes were not rewritten.

Phase15 NOT_YET (unpublished); quotes actionable NOLINE; DK snapshot research only. data_only never conditions on quotes and remains independent of market-anchored mode. No market_calibration changes, Odds spend/auth bypass, fabricated inactives, picks or betting-rule changes.

DEFERRED_100K_UNFINISHED_SEMANTICS: shared accounting implemented, but fitted penalties/returns/official OT/target-depth and missing real coverage/routes/personnel/NGS sources prevent full semantics/input readiness. See PATH_SEMANTICS_JOINT_VS_EMPIRICAL.md. External packet/run outside writable roots; DELIVERY.md contains exact parent copy commands.
