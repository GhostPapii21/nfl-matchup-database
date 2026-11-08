import json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
O=H.parent/'dal_ind_suite_fix_2026-11-06'
def doc(name,s):(H/name).write_text(s+'\n')
pol=O/'inputs/selected_robust/model.json'
plan={'status':'REGISTERED_FUTURE_ONLY_NOT_EXECUTED','policy_status':'RESEARCH_PROVISIONAL_NOT_PROMOTED','policy':'mix_equal_0.25','frozen_policy_path':str(pol),'frozen_policy_sha256':hashlib.sha256(pol.read_bytes()).hexdigest(),'registration_date':'2026-11-06','evaluation_universe':'DAL and IND regular-season games with kickoff strictly after 2026-11-08T23:59:59Z; evaluate all eligible games through end of 2026 regular season, no optional stopping','exclude':['all W1-8 2026 games','2026_09_DAL_IND explicitly excluded; W1-8 role fit is not a pristine same-season role test'],'selection':'W1-3 train/W4-5 dev only','inspected':'W7-8 INSPECTED_DEV_REPORTING_ONLY, never gate','W6':'secondary audit only; no promotion; untouched status not proven','historical_pristine_claim':False,'evaluation':'role counts and KL/MAE for target/carry/passer, both teams; report zero-count cells explicitly; compare frozen equal_eligible and legacy_depth; report roster changes and unavailable players separately, never refit weights','promotion':'NONE authorized by this plan; future evidence requires independent review and a new preregistered promotion decision','freeze_timing':'hash registered before future games; no future outcomes read in this work'}
(H/'PRISTINE_EVALUATION_PLAN.json').write_text(json.dumps(plan,indent=2))
doc('ROLE_POLICY_STATUS.md','''# Role policy status
RESEARCH_PROVISIONAL_NOT_PROMOTED. Frozen mix_equal_0.25 remains research continuity only. EMPIRICAL_IND_CARRY_REGRESSION retained. No production promotion claim.
W1–3 train / W4–5 dev select the candidate. W7–8 are INSPECTED_DEV_REPORTING_ONLY and cannot accept, reject, or promote policy. W6 is a separate secondary audit; untouched ranking history is not proven here and it confers no promotion.
The old validator remains immutable; validate.py here recomputes selection and reports audits without any promotion threshold. No inspected metric is a gate.
Packet model bytes remain frozen. DELIVERY.md supplies the provisional readiness overlay for consumers.''')
doc('DELIVERY.md','''# Staged delivery
Packet and external run are outside writable roots. Apply these reviewable metadata overlays through an authorized parent delivery; do not rewrite frozen forecast/model bytes:
- active selected_robust: RESEARCH_PROVISIONAL; policy_status RESEARCH_PROVISIONAL_NOT_PROMOTED
- projection_ready=false; Ghost activation NOT_CLAIMED
- flags retain EMPIRICAL_IND_CARRY_REGRESSION; remove any production promotion claim
- W7–8 INSPECTED_DEV_REPORTING_ONLY, promotion_gate=null
All new artifacts are staged here. Prior trees remain immutable. Independent/data_only versus anchored/market_informed modes remain separate; no market artifacts or calibration were changed.''')
doc('MATERIALITY_SCOPE.md','''# Materiality and semantics
materiality_metrics.json uses the packet parquet restricted to W1–8. League rows counted once; DAL/IND scopes include both teams in their games. Rates use all PBP rows as denominator, including administrative rows. Missing return-yard observations are counted separately. These are descriptive exposure counts, not causal estimates of score changes.
Penalty yards and nullified rows expose omitted enforcement/clock/down effects. TD flags on penalty rows do not identify accepted or nullified scoring without adjudication. Exact scoring impact if ignored is NOT_IDENTIFIED. Return yard sums measure field-position displacement exposure, not fantasy credits. OT game rates and TD rows measure exposure; they do not identify a regulation-only counterfactual score.
Existing supported narrow field-position path: fit_prospective_usage.py uses kick_distance minus observed return_yards as punt_net_yards, rejecting missing kick distance and negative net. joint_producer.py flips field position using this net. No player return-yard fantasy credits are created. This does not support return distributions, return TDs, kickoff enforcement or defensive returns.
Penalties, returns and official_overtime remain UNSUPPORTED, allows_sim_effect=false. Injected return/penalty outcomes must raise; existing suite exercises rejection. No new supported semantics were added.
OT single_possession_approx is research-only, NOT_VERIFIED_OFFICIAL_OT: first score can end the trial without matching possession. Official Rule 16 permits both teams an opportunity subject to the regular-season 10-minute limit. Source checked: https://operations.nfl.com/the-rules/nfl-rulebook and https://operations.nfl.com/rules-officiating/featured-rules . This research approximation cannot claim fitted official OT. Modeled no-return touchbacks also remain a residual field-position risk; current official kickoff touchback provisions differ. No readiness inferred.''')
doc('ACTIVATION_ENGINEERING_CHECK.md','''# External activation engineering check
Command from repository root:
python3 research/possession_engine_v0/runs/dal_ind_invariance_decontam_2026-11-06/activation_consumer.py research/possession_engine_v0/runs/dal_ind_invariance_decontam_2026-11-06/activation/selected_robust/sha256_6ecf9e36dc8537af40a598fad2620a44153a9086953f2d0540dfb222e230a8af
The consumer loads copied frozen engine_source, input_root, input manifest and seed from the run spec. It asserts forecast_id and entire trial bytes represented as parsed JSON, which includes team means. activation_result.json records outcome. No protected artifact is edited; copied frozen research tree is preserved byte for byte.
This is narrow reproducibility engineering, not projection_ready, Ghost, predictive validation, promotion, official OT, or consumer operational readiness.''')
doc('FAILURE_MODES.md','''# Failure modes
Contaminated historical acceptance gate: removed only in new validator, not rewritten in place. W7–8 never pristine.
Repository-wide pytest collection is blocked by absent historical parquet fixtures in backtests/v6_brainstorm_proedge/leak_test.py and tools/tests/test_rbmiss_sim.py. See pytest_full.log; this is not a green repository suite claim. Engine suite is recorded separately.
Penalties, return credits, official OT unsupported; descriptive materiality cannot quantify causal scoring impact. W6 untouched status unproven. No retrospective pristine data claimed.
PFF NOT_READY_NO_DUPLICATE: /workspace/research/pff_* contains BLOCKED.txt reporting failed fetch, no content. No acquisition or duplication attempted.
DEFERRED_100K; quotes NOLINE; Phase15 NOT_YET. No picks. No Odds spend or auth bypass.''')
