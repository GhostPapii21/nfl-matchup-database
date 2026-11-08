import json
from pathlib import Path
H=Path(__file__).resolve().parent
load=lambda n:json.loads((H/n).read_text())
i=load('invariance_metrics.json');m=load('materiality_metrics.json');a=load('activation_result.json');p=load('PROTECTED_HASH_CHECK.json');external=load('EXTERNAL_BEFORE_HASH_CHECK.json')
assert i['status']=='PASS' and a['returncode']==0 and p['all_unchanged']
(H/'INVARIANCE_CERTIFICATION.md').write_text(f'''# Attribution invariance certification
PASS: {i['total_trials']} policy trials; 5 seed bases {i['seed_bases']}; 20 trials per seed per policy. Policies: equal_eligible, mix_equal_0.25, empirical_mle, legacy_depth. Only role weights vary; usage/outcome cells identical; coupling=false.
Exact assertions cover all team period stats (scores, yards, play/terminal counts), terminal states, every team event path including boundary events, possession sequence lengths. Q1–Q4, lead/trail/tied states, half transitions, and {len(i['ot_trials'])} naturally reached OT trials in the base policy are included. Paired policies assert exact paths on those same OT trials. Player attribution differs in {i['player_attribution_changed_comparisons']} seed/policy comparisons and is permitted to differ.
Forced role_efficiency_coupling=true raises UNSUPPORTED. No RNG engine changes were needed. Fixed one-draw role-stream split is preserved. Scope is the frozen DAL/IND model and tested seed range, not a universal statistical claim.
Reproduce: python3 research/possession_engine_v0/runs/dal_ind_invariance_decontam_2026-11-06/validate.py
The first harness run failed a boundary-coverage check because it inspected pre/post periods; the engine emits transitions through boundary metadata. The harness now asserts explicit boundary coverage and exact equality; no team assertion was relaxed. See validation.log and invariance_metrics.json.
''')
rows=[]
for scope,v in m['scopes'].items():
 rows.append(f"| {scope} | {v['rows']} | {v['penalty_plays']} ({v['penalty_rate_all_rows']:.2%}) | {v['penalty_yards_sum']} | {v['kicks']['punt']['return_yards_sum']} | {v['kicks']['kickoff']['return_yards_sum']} | {v['ot_games']}/{v['games']} ({v['ot_game_rate']:.2%}) |")
with (H/'MATERIALITY_SCOPE.md').open('a') as f:f.write('\n| Scope | PBP rows | Penalty rows | Penalty yards | Punt return yards | Kickoff return yards | OT games |\n|---|---:|---:|---:|---:|---:|---:|\n'+'\n'.join(rows)+'\n')
metrics={'invariance':i,'materiality':m,'activation':json.loads(a['stdout']),'protected':p,'external_before_hashes_all_match':all(external.values()),'external_before_hashes':external,'policy_status':'RESEARCH_PROVISIONAL_NOT_PROMOTED','engine_pytest':{'exit_code':0,'tests':167,'log':'pytest_engine.log'},'repository_pytest':{'status':'COLLECTION_BLOCKED','errors':2,'reason':'missing historical parquet inputs','log':'pytest_full.log'},'PFF':'NOT_READY_NO_DUPLICATE','quotes':'NOLINE','Phase15':'NOT_YET','scale':'DEFERRED_100K','promotion':False,'projection_ready':False,'Ghost':False}
(H/'NFL16_METRICS.json').write_text(json.dumps(metrics,indent=2))
(H/'reviews/CODEX_SELFCHECK.md').write_text(f'''# Codex self-check
Protected file hashes unchanged: {p['files']}. Supplied external before-hash matches: {all(external.values())}; full detail in EXTERNAL_BEFORE_HASH_CHECK.json. No market_calibration, protected validator, certified_asof, prior role/usage/forecast tree edits. No Odds spend/auth bypass, PFF duplication, picks, 100k run or fabricated Phase15.
New work confined to this run. Provisional packet overlay staged in DELIVERY.md because external paths are outside writable roots. No metadata delivery is claimed.
Engine pytest exit 0 (167 tests). Repository pytest: two collection errors due absent historical parquet fixtures; not green. Invariance validator and frozen-source activation passed. Parent independent adversarial review remains outstanding.
Independent versus anchored modes preserved. quotes NOLINE; Phase15 NOT_YET; DEFERRED_100K.
''')
(H/'COMPLETION_INVARIANCE_DECONTAM.md').write_text(f'''# Completion
Attribution invariance PASS across 400 policy trials, five seed bases, regulation/halftime and naturally reached OT. Team stats, paths, counts, yards and possession lengths match exactly; forced coupling rejects. No engine RNG fix needed.
Decontaminated validator selects only W1–3/W4–5; W7–8 reporting only; W6 secondary audit separate. mix_equal_0.25 is RESEARCH_PROVISIONAL_NOT_PROMOTED with EMPIRICAL_IND_CARRY_REGRESSION retained. Future-only evaluation plan registered; no untouched historical claim.
Materiality quantified from packet W1–8; narrow existing punt-net field-position semantics documented; penalties/return credits/official OT remain unsupported. No invented causal score effects or fantasy return credits.
Frozen-source external consumer activation reproduces forecast ID and exact trials/team means. Engineering only; not projection_ready or Ghost. {p['files']} protected file hashes unchanged. Packet/run overlays staged in DELIVERY.md; external files not changed.
Engine full suite: 167 passed. Repository full suite: 2 collection errors from missing historical parquet fixtures, classified in FAILURE_MODES.md and pytest_full.log. No green repository-wide claim.
PFF NOT_READY_NO_DUPLICATE. DEFERRED_100K; quotes NOLINE; Phase15 NOT_YET. Parent independent adversarial review pending.
''')
