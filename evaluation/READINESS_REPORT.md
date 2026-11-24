# Readiness report (report only)

Evaluated 2026-11-24T22:17:43+00:00 UTC by `python -m evaluation.readiness`. projection_ready on main: **False**. May flip: **False**. Nothing here changes a flag.

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

Unseen = week >= 10. Excluded rows: {'push_or_unknown': 33, 'no_real_price': 18, 'price_after_kickoff': 0, 'seen_week': 0}.

| Market | Spots | Hit | Mean BE | Edge (pts) | 95% CI (pts) | Weeks | Live |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALL | 51 | 0.5882 | 0.5355 | 5.27 | [-8.52, 18.96] | 10 | no |
| prop:carries | 3 | 0.0 | 0.5384 | -53.84 | [-54.55, -53.27] | 10 | no |
| prop:passing_yards | 4 | 0.5 | 0.5289 | -2.89 | [-52.94, 47.17] | 10 | no |
| prop:receiving_yards | 16 | 0.5 | 0.5294 | -2.94 | [-27.97, 22.07] | 10 | no |
| prop:receptions | 16 | 0.8125 | 0.5455 | 26.7 | [5.72, 45.08] | 10 | no |
| prop:rushing_yards | 6 | 0.6667 | 0.5297 | 13.69 | [-19.68, 46.91] | 10 | no |
| team:moneyline | 2 | 0.0 | 0.5495 | -54.95 | [-54.95, -54.95] | 10 | no |
| team:spread | 2 | 0.5 | 0.518 | -1.8 | [-52.38, 48.78] | 10 | no |
| team:total | 2 | 1.0 | 0.5349 | 46.51 | [46.51, 46.51] | 10 | no |
