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
| 1 | `SEMANTICS_BOUNDS.md` with descriptive sensitivity bounds (yards/points exposure, % possessions), not causal claims if unidentified | **met, one residual** (unmerged, PR #19 at [677dd1e](https://github.com/GhostPapii21/nfl-matchup-database/commit/677dd1e828593068800a9e6d81a8d42b20f88deb)) | Every figure now cites a source and pull time (section 0). `bounds/derive_bounds.py --check` reproduces section 3, and `bounds/sensitivity.py` reproduced section 4 exactly (re-run by Ghost6, all 6 arms, about 2:35 PM ET). Residual R1: the penalty log is also missing two week 8 games, and the doc does not label them unknown (re-review below). |
| 2 | Any new SUPPORTED path has conservation tests; reject inventible return TDs / full penalty enforcement / official OT match until implemented | **met** (unmerged, PR #19 at [677dd1e](https://github.com/GhostPapii21/nfl-matchup-database/commit/677dd1e828593068800a9e6d81a8d42b20f88deb)) | `core/possession_engine_v0/tests/test_nfl43_semantics.py`: 37 tests pass offline, up from 21. T1-T3 are closed (re-review below). Rejection side is still met on `joint_producer.py`. |
| 3 | Punt-net remains a separate PBP field-position quantity | **met** (main) | `_punt_net_from_row` in `core/possession_engine_v0/simulate.py` computes net from PBP `kick_distance - return_yards` ([86649e8](https://github.com/GhostPapii21/nfl-matchup-database/commit/86649e86da46a76552e72c0f95974c725109d582)); `joint_producer.py` keeps `punt_net_yards` as its own field ([fe2e371](https://github.com/GhostPapii21/nfl-matchup-database/commit/fe2e3711b766d8894c49ec4dc571e6731628dc55)). |
| 4 | No 100k / projection_ready while still UNSUPPORTED without documented bounds accepted by review | **not accepted yet; second Ghost6 review, Nov 12 about 2:40 PM ET** | All 13 first-round defects are fixed except part of F1. Two residuals block acceptance: R1 (week 8 penalty gap not labeled unknown) and R2 (`still_unsupported` is not read by any code). Guards hold: `DEFERRED_100K` is back to true, the semantics are listed unsupported again, and `known_flags/NFL43_REVIEW.json` says PENDING. `sim100k` (G1/G2), `snapshots/lock.py` (exit 2, nothing simulated) and `rocket` R2 all refuse (verified offline). The earlier locks are flagged in `snapshots/KNOWN_MODEL_ERROR.md`. `NFL43_REVIEW.json` stays PENDING; Ghost6 has not flipped it. |

## NFL-56: GitHub as source of truth

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Runnable workflows for each phase with explicit MISSING/NOT_YET statuses (no silent skip) | **partial** (unmerged) | `pipeline/phases.py`, `pipeline/slate.py`, `docs/PHASE_WORKFLOWS.md`, `pipeline/tests/test_pipeline.py` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), PR #16, not merged). Each phase is a runnable command with FILLED/MISSING/STALE/NOT_YET. Missing: the GitHub Actions workflow that runs them is not installed (sits in `pipeline/workflow_to_install/`), and PR #16 is unmerged. |
| 2 | News/weather adapters documented with freshness windows | **met** (unmerged) | `docs/DATA_FRESHNESS.md` and `pipeline/freshness.py` `POLICY` ([9ee4b5b](https://github.com/GhostPapii21/nfl-matchup-database/commit/9ee4b5bfe265e1599e02cfa67e40b6447d38de43), PR #16). Documents the gap honestly: the only news adapter is the ESPN injury list; no general news feed. |
| 3 | 100k entrypoint exists but fail-closed while DEFERRED_100K | **partial** (re-checked at [677dd1e](https://github.com/GhostPapii21/nfl-matchup-database/commit/677dd1e828593068800a9e6d81a8d42b20f88deb), about 2:35 PM ET) | `pipeline/sim100k.py` refuses again on G1 (DEFERRED_100K) and G2 (unsupported semantics, review PENDING), plus G4/G5. Still open: `sim100k.py` is unchanged by the fixes and still runs the **period engine** (`default_engine()` L80 -> `core/period_engine_v0/monte_carlo.simulate_game` L91), not the NFL-43 possession engine that the G2 gate checks. |
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

## PR #19 review: NFL-43 bounds and possession-sim changes (Ghost6, Thu Nov 12, 2026, about 12:45 PM ET)

Reviewed branch `betguru/nfl49-rocket-nfl43-e2e` at [08b8cee](https://github.com/GhostPapii21/nfl-matchup-database/commit/08b8cee290833378623db9d50baa561515c03e4a) (base PR #16 `nfl56/repo-source-of-truth`). Read-only review: no model,
weight, formula or flag changes, nothing merged. Line numbers are at [08b8cee](https://github.com/GhostPapii21/nfl-matchup-database/commit/08b8cee290833378623db9d50baa561515c03e4a).

**Verdict: NFL-43 criterion 4 does not pass.** The penalty and OT mechanics are sound and the tests pass, but the bounds file
is not fully sourced, one of its rows does not match what the code does, and the flags were opened before review.

### Tests (run offline: `unshare -rn`, no network, no workflows triggered)

* `test_nfl43_semantics.py`: 21 passed.
* `scripts/test_offline.sh`: all suites pass, 725 passed, 41 skipped (52 + 40/1s + 202 + 13 + 18 + 35 + 7 + 271/40s + 87).
* `rocket_gate/tests`, `phase15/tests`, `snapshots/tests`: 8 + 8 + 9 = 25 passed, but they are **not** in `scripts/test_offline.sh` (T4).

### Bounds-file defects (`core/possession_engine_v0/SEMANTICS_BOUNDS.md`)

* **D1 (lines 16-17, 26-27, 39-46, 50-56): no pull time on any figure.** The return figures (1/1,404 kickoffs, 1/1,033 punts, 20.6/4.0, 2 in 136, 9/197, 6/157) match
  `/workspace/nfl49_data/pbp_2026_20261112T1116.parquet` (a local W1-9 file pulled about 11:16 AM ET), but the doc does not cite it. The repo's bundled PBP covers W1-8 only.
* **D2 (line 18 vs `simulate.py:375-391`): the "Defensive returns `asof_league_v1`" row is wrong.** The engine does not use a league rate. It uses
  `return_yards`/`return_touchdown` from the sampled NYG/WAS rows. Those teams' 16 W1-9 turnover rows have zero return TDs, so the TNF lock has
  `def_td_home = def_td_away = 0.0` over 100k games (`summary.json` `nfl43`). League rate in the same file: 15 TDs on 354 turnovers. Line 45 describes a rate the sim does not apply.
* **D3 (line 16, `semantics.py:88-89`): week 9 penalty gap not disclosed.** The canonical penalty log stops at W8, so the TNF run (as-of W10) has
  `coverage_gap_weeks: [9]` (`sim_meta.json`). The doc says "weeks strictly before target" and should label W9 unknown. Also, `semantics.py:89` filters games by week only, with no season filter.
* **D4 (line 46): OT rate denominator 11/121 conflicts with line 35's 119 W1-8 games.** It comes from an older run artifact
  (`runs/dal_ind_invariance_decontam_2026-11-06/materiality_metrics.json`) with no pull time.
* **D5 (lines 59-63): wrong comparisons.** The "~12 flags, ~45 yards per team" figure mixes units: 12 is per game, about 6 per team. Like for like,
  league scrimmage-only is 6.35 flags and 51.0 yards per team-game (1,512 flags and 12,147 yards over 238). Line 60 credits the margin shift to "NYG 5.9% vs WAS defense 3.1%",
  but WAS offense is 6.9% vs NYG defense 3.7% (`sim_meta.json`), and simulated penalty yards are even (45.3 vs 44.7).
* **D6 (lines 48-56): the sensitivity table has no committed script or artifact,** so it cannot be reproduced from the repo. Ghost6's
  independent run (all paths, seed 777, n=2,000) got NYG 12.46 / WAS 22.08 / P(NYG win) 0.208, which is consistent with the table.
* **D7 (lines 65-68): wrong root cause for the level gap** (see the sanity note below).

### Code/test defects

* **F1 `known_flags/KNOWN_LIMITATIONS.json:16-17`:** flags flipped before review (NFL-43 row 4). `pipeline/hooks.py:146-148` and `rocket_gate/cli.py` R2
  check only `unsupported_semantics`. They ignore `nfl43.still_unsupported` (3 items) and `nfl43.review` (PENDING), so `rocket` R2 passes while review is pending.
* **T1 `test_nfl43_semantics.py:194-199`:** `test_return_tds_are_scored_once` compares the event count with `special_scores`, which the same code increments
  together, so it is tautological. It does not check that 6 points plus the try were added once.
* **T2:** nothing tests the untimed down (`simulate.py:551-555`), the live-ball drop on a possession change or score (`simulate.py:560-566`), the
  10-minute OT length, the end-zone defensive-return touchback, or that kick-play rows are actually filtered (line 75 only checks a meta flag).
* **T3 `test_nfl43_semantics.py:23-28`:** full-sim tests run as-of W9 on the bundled W1-8 PBP, not the as-of-W10 config used for the locks.
  They use 120 sims, and none checks a bounds figure.
* **T4 `scripts/test_offline.sh:18-26`:** omits `rocket_gate/tests`, `phase15/tests` and `snapshots/tests`, so CI never runs them.
* **T5:** running the offline suite still rewrites tracked `core/period_engine_v0/artifacts/demo_jaxbal_period_report.json`. c4e64e2 reverted the
  file but not the test side effect.
* OT tracker (`semantics.py:184-226`), half distance and enforcement: no defects found. They match the 2025 regular-season rule as described.

### Sanity note: locked TNF sim WAS 22.1 / NYG 12.6, P(NYG win) 0.21 vs market about 0.55 (diagnosis only, nothing tuned)

* **Main cause: head-to-head-only defense conditioning.** `simulate.py:502-508` always enables `_defense_cond`. Config `defense_interaction.mode`
  is `h2h_only` (`simulate.py:784`). `sample_snap` (`simulate.py:149-163`) then draws every snap from `by_team_vs_def[(offense, defense)]`, filtered
  by down only, whenever that pool has at least 5 plays. For WAS@NYG that pool is the single W5 game `2026_05_NYG_WAS` (27-27). Instrumented run (seed 777, n=2,000):
  **100% of snaps** were tagged `DEF_COND` (NYG 52.5%, WAS 47.5%). Distance, field position and the other 14 games are ignored.
* **Local diagnostic, not a model change:** turning that conditioning off in memory gives NYG 16.15 / WAS 17.50, P(NYG win) 0.45 (n=2,000). That one path
  explains about 24 of the 34-point win-probability gap.
* **The total stays low (about 33.7 vs 40.5) with it off,** so a second level issue remains. Candidates: pace (about 114 snaps per game simulated),
  no QB/injury adjustment, and 99.8% of games carrying coarse-cell flags. Not isolated.
* Actual NYG points per game W1-9 in the same PBP file: 22.75. The sim's 12.6 is not a plausible team level.
* This problem predates NFL-43 (the legacy arm in bounds line 52 is already 13.0 / 21.9). It is a model problem to log under NFL-49, not an edge.

## PR #19 second review: NFL-43 fixes (Ghost6, Thu Nov 12, 2026, about 2:40 PM ET)

Reviewed PR #19 head [677dd1e](https://github.com/GhostPapii21/nfl-matchup-database/commit/677dd1e828593068800a9e6d81a8d42b20f88deb) (commits [13d83e4](https://github.com/GhostPapii21/nfl-matchup-database/commit/13d83e409391affdb6d752d3b00ba9cc8dcce4bc), [0428db9](https://github.com/GhostPapii21/nfl-matchup-database/commit/0428db9), [9c401d6](https://github.com/GhostPapii21/nfl-matchup-database/commit/9c401d6), [677dd1e](https://github.com/GhostPapii21/nfl-matchup-database/commit/677dd1e828593068800a9e6d81a8d42b20f88deb)) against every first-round defect. Read-only: nothing merged,
no flag or weight change, and `NFL43_REVIEW.json` was not flipped. Line numbers are at 677dd1e.

**Tests, run with networking disabled:** `scripts/test_offline.sh` passes **775, with 41 skipped and no failures**:

| Suite | Passed | Skipped |
|---|---|---|
| repo root | 52 | 0 |
| period engine | 40 | 1 |
| possession engine | 218 | 0 |
| gamebooks | 13 | 0 |
| pregame | 18 | 0 |
| pipeline | 41 | 0 |
| teams | 7 | 0 |
| market calibration | 271 | 40 |
| source_run_gate | 87 | 0 |
| rocket_gate | 10 | 0 |
| phase15 | 8 | 0 |
| snapshots | 10 | 0 |

NFL-43 file: 37 passed. The working tree was clean afterwards.

| Defect | Status | Evidence |
|---|---|---|
| D1 pull times | **fixed** | `SEMANTICS_BOUNDS.md` section 0 (lines 16-27): PEN pulled 2026-11-01 about 9 PM ET (exact minute labeled unknown, per `PENALTY_NOTES.md:1`). PBP9 is committed as `data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet`, with sha256 matching the lock input (1028614b...). Section 3 rows each cite a source and pull time. `derive_bounds.py --check` passes. Minor: the market figures on lines 106-107 cite a chat thread, not a repo file. |
| D2 def returns at league rate, in code | **fixed** | `semantics.py:186` `draw_def_return`, with pools built in `build_return_model` (league, all teams, weeks < target, by turnover kind: 197 INT / 9 TD, 157 FL / 6 TD). `simulate.py:376` -> `_defensive_return` `simulate.py:421`. Sensitivity: 0.086 defensive TDs per game, up from 0. Test `test_defensive_returns_use_league_pool`. |
| D3 W9 unknown + season filter | **fixed, residual R1** | `semantics.py:97-101` season filter (game_id must be in the season-filtered log, since the file has no season column). `semantics.py:134-135` reports `unknown_weeks: [9]`. **R1:** PEN also lacks two week 8 games, `2026_08_CHI_SEA` and `2026_08_PHI_WAS` (121 PBP W1-8 games vs 119 in PEN). So WAS has 6 team-games, not 7, and its W8 game is missing. Lines 20 and 60 present PEN as covering W1-8 without labeling those games unknown, and `unknown_weeks` only catches weeks missing league-wide. |
| D4 OT source | **fixed** | Line 68: 8.8% (12/136) from PBP9. Ghost6 re-derived 12 games with a 5th quarter out of 136. The old 11/121 artifact is no longer cited (line 26). |
| D5 comparisons | **fixed** | Lines 59-60 and 90-100: scrimmage-only 6.35 flags / 51.0 yards per team-game; foul probabilities paired correctly (NYG offense sees 9.0%, WAS offense sees 10.6%); the margin-shift cause is labeled not identified. |
| D6 reproducible sensitivity | **fixed** | `bounds/sensitivity.py`, which refuses n > 20,000. Ghost6 re-ran it offline (n=6,000, seed 777): all 6 arms are **identical** to the committed `bounds/sensitivity_was_nyg_w10.json`. The engine files are unchanged between code_head 13d83e4 and 677dd1e. |
| D7 scoring-gap cause | **fixed** | Lines 104-122: h2h-only defense conditioning is named as the main cause. DIAG arm: NYG 15.68 / WAS 17.48, P(NYG win) 0.439. The residual total gap is labeled not isolated. |
| F1 100k blocked while review pending | **partly fixed, residual R2** | Flags reverted: `known_flags/KNOWN_LIMITATIONS.json:16-21` (unsupported list restored, `DEFERRED_100K: true`). New `known_flags/NFL43_REVIEW.json` (PENDING, with sha256-bound acceptance). `pipeline/hooks.py:143` `nfl43_review`, `:178-180` in `nfl43_semantics`; `snapshots/lock.py:49,245` refuses before simulating; `rocket_gate/cli.py:74` R2 fails and `:168` R5 flags earlier locks. All verified refusing offline. **R2:** `nfl43.still_unsupported` (kick-play fouls, joint producer, blocked kicks/onside/fakes; `KNOWN_LIMITATIONS.json:30-34`) is not read by any code (grep finds no reference). Once the review is accepted and the flags are cleared, nothing enforces it. |
| T1 tautological return-TD test | **fixed** | `test_return_tds_are_scored_once` (test file line 198) now requires each return-TD event to be followed by one 6-point credit to the same team, and 6-point credits to equal TD events. |
| T2 missing tests | **fixed** | Untimed down (lines 277, 291), live-ball drop (301-307), 10-minute OT (325, 330), end-zone touchback (346), league return yards (355), kick-play filter on a synthetic log (362). |
| T3 W10 config, bounds checked | **fixed** | The `sims` fixture uses the real as-of-W10 config on PBP9, with 300 games (test file around line 154). Bounds tests at lines 380, 386 and 396. |
| T4 suites in CI script | **fixed** | `scripts/test_offline.sh:27-29`. |
| T5 artifact rewrite | **fixed** | `core/period_engine_v0/demo_jaxbal_report.py:13` takes `out_dir`; the test passes `tmp_path` (test_e2e_ghost6_remaining.py:108). After the full offline run, `git status` was clean. |

**Not part of AC4 but still open:**
* `pipeline/sim100k.py` still runs the period engine (NFL-56 row 3).
* `bounds/sensitivity.py:60` patches the class inside a worker process. It is safe only because the DIAG arm is queued last; a sturdier design would isolate it.

**To accept:**
* R1: label the two missing W8 games unknown in the doc and in `unknown_*` meta, per team.
* R2: make the hooks/rocket check honor `nfl43.still_unsupported`, or record a documented Rico decision that those three exclusions are accepted as part of the bounds.

Then Ghost6 flips `NFL43_REVIEW.json` to ACCEPTED for the new bounds sha256. `DEFERRED_100K` stays Rico's call.

## Bottom line

As of about 2:40 PM ET (PR #19 head 677dd1e):

* **NFL-43:** criteria 1-3 met (criterion 1 with residual R1). Criterion 4 is **not accepted yet**: two small residuals remain (R1 week 8 penalty gap not labeled unknown; R2 `still_unsupported` not enforced). 100k stays refused everywhere.
* **NFL-56:** 2 of 5 met, 3 partial. Criterion 3 stays partial because `sim100k` still runs the period engine.
* **Status:** nothing is merged and `projection_ready` stays `false`.
