# Readiness report (report only)

Evaluated 2026-11-26T13:07:53+00:00 UTC by `python -m evaluation.readiness`. projection_ready on main: **False**. May flip: **False**. Nothing here changes a flag.

## Evidence boundary (derived live)

- Stamp: `2026-11-26T13:07:53+00:00` UTC. Counts only committed files on this tree (`derived_live=True`).
- Pristine holdout cited: **14** scored games, weeks **['10', '11']** (`evaluation/EVALUATION.json`).
- Snapshot LOCKs on tree: **23** game ids, weeks **['10', '11', '12']**.
- Week 12 packets: **16**; with LOCK: **9**; scored: **0**; pre-kickoff without LOCK: **6**; post-kickoff without LOCK (not retroactive): **1**.
- Open drafts / price freezes do **not** count (`price_freeze_dir_count=29`).
- Ceiling if unscored W12 LOCKs score and remaining pre-kickoff packets lock+score: **14+9+6=29** (shortfall vs min games at ceiling: **1**; min_coverage={'games_scored': 30, 'weeks': 3}).
- Pristine requires: `snapshots/<game_id>/<lock>/LOCK.json scored under the frozen protocol (pre-kickoff, n=100000, code_dirty=false, asof_checks=PASS, intact file hashes, SCORE.json)`.
- Holdout coverage is only SCORED rows from committed evaluation/EVALUATION.json (discovered via snapshots/*/*/LOCK.json): 14 scored, weeks ['10', '11']. Committed snapshot LOCKs cover weeks ['10', '11', '12'] (23 game ids). Week 12 pregame packets on this tree: 16; with LOCK: 9; already scored: 0. Price-freeze directories and open draft PRs never count toward pristine coverage. 1 Week 12 packet(s) already past kickoff without a LOCK (2026_12_GB_LA) — cannot be added retroactively. 9 Week 12 LOCK(s) committed but not yet scored (2026_12_ATL_MIN, 2026_12_BAL_HOU, 2026_12_CHI_DET, 2026_12_DEN_PIT, 2026_12_KC_BUF, 2026_12_NO_CIN, 2026_12_NYG_IND, 2026_12_NYJ_MIA, 2026_12_PHI_DAL) — count toward the ceiling only after FINAL + SCORE.json. 6 Week 12 packet(s) still pre-kickoff without a LOCK; each still needs final inactives/quote freshness and a valid 100k LOCK. Ceiling if unscored LOCKs score and remaining packets lock+score: 14+9+6=29. Even at that ceiling, shortfall vs min_coverage {'games_scored': 30, 'weeks': 3} is 1 game(s) — later-week eligible LOCKs (e.g. Week 13+) are still required. All readiness flags stay fail-closed.

## NFL-49: FAIL

| Pillar | Result | Evidence / blockers |
| --- | --- | --- |
| NFL-49 P1 source freshness/completeness | PASS | Phase15='AUTO' (known_flags/KNOWN_LIMITATIONS.json); quotes='FREE_FEED_ACCEPTED' (known_flags/KNOWN_LIMITATIONS.json); per-game freshness is checked live by pipeline/freshness.py (publisher as-of time, NFL-56) |
| NFL-49 P2 integrated sim accounting | PASS | entrypoint_enforced=True (known_flags/KNOWN_LIMITATIONS.json); NFL-43 review: ACCEPTED by Ghost6 for SEMANTICS_BOUNDS.md sha256 975e84cc... at 32b9b92 (Nov 12 ~3:05 PM ; still unsupported (bounded, enforced): ['kick-play fouls', 'joint_producer penalties/return yards', 'blocked kicks/onside/fakes']; SHARED_ACCOUNTING: core/possession_engine_v0/shared_accounting.py; contaminated validator superseded by core/possession_engine_v0/runs/dal_ind_invariance_decontam_2026-11-06/validate.py |
| NFL-49 P3 calibration evidence | FAIL | calibration_fitted_claim=False (known_flags/KNOWN_LIMITATIONS.json); no fitted calibration (NFL-45); no market meets Rico's market-readiness rule (see market table) |
| NFL-49 P4 end-to-end acceptance | FAIL | full_integration_acceptance=False (known_flags/KNOWN_LIMITATIONS.json); production_validated=False (known_flags/KNOWN_LIMITATIONS.json); pristine evaluation status='UNSCORABLE_INSUFFICIENT_COVERAGE', games_scored=14, weeks_scored=['10', '11'] vs min {'games_scored': 30, 'weeks': 3} (evaluation/EVALUATION.json); pristine_protocol_complete=False (known_flags/KNOWN_LIMITATIONS.json) |

## NFL-56: PASS

| Criterion | Result | Evidence | Note |
| --- | --- | --- | --- |
| 1 runnable phase workflows with explicit MISSING/NOT_YET | PASS | pipeline/phases.py statuses; .github/workflows/nfl-gameday-gate.yml runs python -m pipeline.window | pipeline/workflow_to_install/nfl-source-of-truth.yml is still not installed (workflow changes need Rico) |
| 2 news/weather adapters documented with freshness windows | PASS | docs/DATA_FRESHNESS.md (windows) + pipeline/freshness.py POLICY |  |
| 2b freshness dated by publisher as-of time | PASS | pipeline/freshness.py + pipeline/source_asof.py |  |
| 3 100k entrypoint exists and fails closed | PASS | pipeline/sim100k.py (no override; G0-G7 gates) |  |
| 4 routine bootstrap without continuous sessions | PASS | workflow_dispatch on nfl-gameday-gate.yml / nfl-pregame-packets.yml, dispatched by external cron-job.org jobs (not verifiable from the repo; last verified dispatch run 44943361282 on main, success) |  |
| 5 README distinguishes goal vs current readiness | PASS | README.md 'Projection pipeline: goal vs current status (NFL-56)' |  |

## Market readiness (Rico's rule: 30+ real-price graded spots on unseen games, >= +3 pts over break-even, CI > 0, >= 4 weeks)

Unseen = week >= 10. Excluded rows: {'push_or_unknown': 873, 'no_real_price': 20, 'price_after_kickoff': 0, 'seen_week': 0}.

| Market | Spots | Hit | Mean BE | Edge (pts) | 95% CI (pts) | Weeks | Live |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALL | 1067 | 0.4845 | 0.5433 | -5.88 | [-8.79, -2.88] | 10,11 | no |
| prop:carries | 3 | 0.0 | 0.5384 | -53.84 | [-54.55, -53.27] | 10 | no |
| prop:passing_yards | 4 | 0.5 | 0.5289 | -2.89 | [-52.94, 47.17] | 10 | no |
| prop:receiving_yards | 443 | 0.5102 | 0.5384 | -2.82 | [-7.45, 1.76] | 10,11 | no |
| prop:receptions | 334 | 0.506 | 0.5434 | -3.74 | [-8.96, 1.45] | 10,11 | no |
| prop:rushing_yards | 219 | 0.3836 | 0.5388 | -15.52 | [-21.88, -9.13] | 10,11 | no |
| team:moneyline | 22 | 0.5909 | 0.7236 | -13.27 | [-31.27, 4.17] | 10,11 | no |
| team:spread | 20 | 0.55 | 0.5251 | 2.49 | [-17.93, 22.89] | 10,11 | no |
| team:total | 22 | 0.5455 | 0.5255 | 2.0 | [-20.38, 20.44] | 10,11 | no |
