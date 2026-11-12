# Acceptance status: NFL-43, NFL-56, NFL-49

Checked by Ghost6 on Thu Nov 12, 2026, about 11:45 AM ET, against `main` at
[aca9406](https://github.com/GhostPapii21/nfl-matchup-database/commit/aca94069ac4a5614bf5ed0a9b92f74797950cbd0)
and every open PR branch (`nfl56/repo-source-of-truth` = PR #16, `research/was-nyg-week10-odds-2026-11-11` = PR #14)
plus the unmerged branch `research/multibook-price-feed-2026-11-12`. Criteria are copied from the Linear issues
(read with `get_issue` at the same time). Linear status at that time: NFL-43 Todo, NFL-56 In Progress, NFL-49 Todo.

Rules used: **met** only if verified in code; **partial** names what is missing; **not met** means nothing on GitHub
satisfies it. Unmerged work is labelled. Nothing here closes an issue or changes `projection_ready` (still `false`
in `known_flags/KNOWN_LIMITATIONS.json`).

## NFL-43: official semantics (penalties, returns, overtime)

| # | Criterion | Status | Evidence (file, commit, branch) |
| --- | --- | --- | --- |
| 1 | `SEMANTICS_BOUNDS.md` with descriptive sensitivity bounds (yards/points exposure, % possessions), not causal claims if unidentified | **not met** | No `SEMANTICS_BOUNDS.md` on main or any branch. Raw materiality numbers exist in `core/possession_engine_v0/runs/dal_ind_invariance_decontam_2026-11-06/materiality_metrics.json` ([fe2e371](https://github.com/GhostPapii21/nfl-matchup-database/commit/fe2e3711b766d8894c49ec4dc571e6731628dc55), main), but they are not the bounds document. Owner: BetGuru. |
| 2 | Any new SUPPORTED path has conservation tests; reject inventible return TDs / full penalty enforcement / official OT match until implemented | **partial** | Rejection side is met: `core/possession_engine_v0/joint_producer.py` marks penalties, returns, official_overtime `UNSUPPORTED` with `allows_sim_effect=False` and raises on penalty / return / OT profiles; tests `test_unsupported_rule_effects_are_blocked_not_silently_approximated` and `test_unsupported_category_or_official_ot_profile_blocks_run` in `core/possession_engine_v0/tests/test_joint_producer.py` ([fe2e371](https://github.com/GhostPapii21/nfl-matchup-database/commit/fe2e3711b766d8894c49ec4dc571e6731628dc55), main). No SUPPORTED path exists yet, so there are no conservation tests for one. |
| 3 | Punt-net remains a separate PBP field-position quantity | **met** (main) | `_punt_net_from_row` in `core/possession_engine_v0/simulate.py` computes net from PBP `kick_distance - return_yards` ([86649e8](https://github.com/GhostPapii21/nfl-matchup-database/commit/86649e86da46a76552e72c0f95974c725109d582)); `joint_producer.py` keeps `punt_net_yards` as its own field ([fe2e371](https://github.com/GhostPapii21/nfl-matchup-database/commit/fe2e3711b766d8894c49ec4dc571e6731628dc55)). |
| 4 | No 100k / projection_ready while still UNSUPPORTED without documented bounds accepted by review | **partial** | Flags hold it: `known_flags/KNOWN_LIMITATIONS.json` has `DEFERRED_100K: true`, `projection_ready: false`, `unsupported_semantics` listed ([fe2e371](https://github.com/GhostPapii21/nfl-matchup-database/commit/fe2e3711b766d8894c49ec4dc571e6731628dc55), main). Enforcement in code exists only on unmerged PR #16: `pipeline/sim100k.py` gates G1/G2 refuse ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43)). Gap: main still has `.github/workflows/nfl-mnf-100k-conditional-simulation.yml` (`workflow_dispatch`) that runs a research 100k outside any gate. |

## NFL-56: GitHub as source of truth

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Runnable workflows for each phase with explicit MISSING/NOT_YET statuses (no silent skip) | **partial** (unmerged) | `pipeline/phases.py`, `pipeline/slate.py`, `docs/PHASE_WORKFLOWS.md`, `pipeline/tests/test_pipeline.py` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), PR #16, not merged). Each phase is a runnable command with FILLED/MISSING/STALE/NOT_YET. Missing: the GitHub Actions workflow that runs them is not installed (sits in `pipeline/workflow_to_install/`), and PR #16 is unmerged. |
| 2 | News/weather adapters documented with freshness windows | **met** (unmerged) | `docs/DATA_FRESHNESS.md` and `pipeline/freshness.py` `POLICY` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), PR #16). Documents the gap honestly: the only news adapter is the ESPN injury list; no general news feed. |
| 3 | 100k entrypoint exists but fail-closed while DEFERRED_100K | **met** (unmerged) | `pipeline/sim100k.py` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), PR #16). Verified 11:4x AM ET: `python -m pipeline.sim100k --game 2026_10_WAS_NYG` refuses on G1 DEFERRED_100K, G2 NFL-43, G4/G5 stale weather, missing four-book freeze, inactives NOT_YET. No override flag. |
| 4 | Routine bootstrap pulls/runs/pushes without continuous awake sessions | **partial** | Pull side runs on main: `.github/workflows/nfl-pregame-packets.yml` (scheduled; latest bot commit [aca9406](https://github.com/GhostPapii21/nfl-matchup-database/commit/aca94069ac4a5614bf5ed0a9b92f74797950cbd0)). Run-and-push of ledgers: `pipeline/workflow_to_install/nfl-source-of-truth.yml` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43)) is written but **not installed**; the bot token lacks `workflow` scope, so Rico has to move it into `.github/workflows/`. |
| 5 | README distinguishes production goal vs current readiness false | **met** (unmerged) | `README.md` section "Projection pipeline: goal vs current status (NFL-56)" ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), PR #16). |

## NFL-49: production acceptance gate

### Acceptance criteria

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | All linked child blockers closed or explicitly waived by Rico with evidence | **not met** | Linked issues all open at check time: NFL-42 Todo, NFL-43 Todo, NFL-44 Todo, NFL-45 Todo, NFL-46 Todo, NFL-47 Todo, NFL-53 Todo, NFL-56 In Progress. No waivers recorded. |
| 2 | READINESS `projection_ready=true` only after gate evidence attached | **holding** (constraint, not yet satisfiable) | `projection_ready: false` in `known_flags/KNOWN_LIMITATIONS.json` ([fe2e371](https://github.com/GhostPapii21/nfl-matchup-database/commit/fe2e3711b766d8894c49ec4dc571e6731628dc55), main). No gate evidence exists. |
| 3 | No picks published from this track until then | **holding** (cannot be fully proven from the repo) | Repo outputs are labelled research only; packets say `projection_ready` false. Chat posts outside the repo are not verifiable here. |
| 4 | No self-expanding research loop; deferred items stay labeled deferred | **holding / at risk** | `DEFERRED_100K` still labelled on main. Risk: the four-book feed branch `research/multibook-price-feed-2026-11-12` ([c50fb4c](https://github.com/GhostPapii21/nfl-matchup-database/commit/c50fb4cdc378090c21100d26f5c5f38c4d361055), unmerged) is feature growth outside the blockers (owner's review item 1). |

### Four pillars

| Pillar | Status | Evidence |
| --- | --- | --- |
| 1 Source freshness/completeness (Phase15, quotes, coverage) | **partial** | Freshness checks: `pipeline/freshness.py` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), unmerged). Four-book quotes: [c50fb4c](https://github.com/GhostPapii21/nfl-matchup-database/commit/c50fb4cdc378090c21100d26f5c5f38c4d361055), unmerged, under review. Phase 15 official inactives: no source on GitHub (not met). Coverage/NGS/FTN gaps (NFL-47) open. |
| 2 Integrated sim accounting (entrypoint enforced, SHARED_ACCOUNTING, semantics bounds) | **not met** | `entrypoint_enforced: false` on main; NFL-42 single validation entry point and its 2 tests not on GitHub; `rocket` not on GitHub; `SEMANTICS_BOUNDS.md` missing. Only the PR #16 gate exists (unmerged). |
| 3 Calibration evidence (not NOLINE / not false FITTED) | **not met** | `quotes: NOLINE`, `calibration_fitted_claim: false` on main. No grading loop, no holdout, no calibration on GitHub. |
| 4 End-to-end acceptance (gate + Ghost final) | **not met** | No end-to-end run on GitHub; no Ghost6 final vet. |

## Bottom line

Nothing in NFL-43 or NFL-49 is closable. NFL-56 has 3 of 5 met and 2 partial, all on unmerged PR #16.
`projection_ready` stays `false`.
