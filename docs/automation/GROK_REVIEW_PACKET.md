# Independent review packet (NFL-82 / GitHub #147)

Self-contained handoff for an adversarial review. The reviewer is not connected to this workspace. Evidence below was read from `main` at `ef4cc69035b8827fe897a574a0d7d22091ee26b3`. Challenge it. Do not treat this packet as authority over the files it cites.

Companion files in the same commit: `docs/automation/INVENTORY.md`, `docs/automation/inventory_manifest.json`, `pipeline/tests/test_phase0_inventory.py`.

The inspected main commit is still `ef4cc69035b8827fe897a574a0d7d22091ee26b3`. The open-PR snapshot was refreshed on 2026-11-28. `evaluation/tests/test_readiness.py` is not part of this diff. Draft PR #137 is the only owner of that assertion: it discovers `snapshots/2026_12_*/*/LOCK.json`, requires `locked_utc` before `kickoff_utc`, and keeps `projection_ready` false. Hardcoded copies on #149, #151, and #152 are removed so they cannot drift.

`projection_ready` is false. This packet does not recommend changing it, production data controls, model weights, or deployment.

## Task (verbatim)

You are the independent adversarial architecture reviewer for GhostPapii21/nfl-matchup-database. Review GitHub issue #147 and the current main-branch implementation, especially pipeline/phases.py, docs/PHASE_WORKFLOWS.md, workflows/operational_specs/PHASE_SCRIPT.md, pipeline/sim100k.py, pregame/build_packets.py, pipeline/freshness.py, and all existing simulation/model entrypoints. Do not edit files or assume code exists because documentation mentions it. Return: (1) verified component inventory with paths and callable entrypoints; (2) exact contradictions between current implementation and #147 acceptance criteria; (3) whether sim_v6's three methods are actually runnable and distinct from NFL-43 sim100k/Main/Lightning; (4) missing dependencies and fail-open risks; (5) a minimal dependency-ordered architecture for one idempotent per-game orchestrator; (6) test cases that prove all 15 phases execute rather than merely pass freshness checks; (7) an independent critique of scheduler options that does not rely on GitHub Actions; (8) explicit unknowns and evidence links. Cite exact file paths, function names, and tests. Never fabricate evidence, never mark research-only as production-ready, and never recommend changing projection_ready or production data controls.

## What was verified on disk

| Claim | Check |
| --- | --- |
| Inventory commit is the #146 merge | `git rev-parse HEAD` on main before this branch was `ef4cc69035b8827fe897a574a0d7d22091ee26b3`, subject `Merge pull request #146` |
| `tools/sim_v6.py` absent | Path test, exit missing |
| `tools/sim_v6_calib.json` absent | Path test |
| `calibration/simv56/engines/__no_calib__.json` absent | Path test |
| `rules/rulebook.py` absent | Path test |
| `render.yaml` and `Procfile` absent | Path test |
| `pipeline/orchestrator.py` absent | Path test |
| Scratch engine present | `calibration/simv56/engines/cc_sim_v6.py` line 1 `SCRATCH COPY`; line 21 `MODES=('mc','bias','gr')`; line 19 `CALIB_F=...__no_calib__.json`; lines 23–24 read parquet at import; line 44 `os.environ['CC_OPP']` |
| sim100k is possession-only | `pipeline/sim100k.py` `TRIALS = 100_000`; docstring names `simulate_games` via `snapshots/lock.py` `run_sim`. File text has no `monte_carlo` and no `game_randomness` |
| Phase checker statuses | `pipeline/phases.py` `BLOCKING = ("MISSING", "STALE", "GAP", "NOT_YET")`. No `status = "PASS"`. Docstring: no model run |
| Period-engine Bias | `core/period_engine_v0/monte_carlo.py` header `Bias: UNIMPLEMENTED` |
| BUF@MIN disclaimer | `research/third_down/BUF_MIN_W9_MC_100K_X_3_SCENARIOS_X_3_METHODS_20261109.json` keys `not_run_actual_main_or_lightning: true` and methods `historical_shares`, `injury_protection_downside`, `route_drive_opportunity` |
| DEN@PIT package on main | `runs/2026-11-27_DEN@PIT/POSTGAME_REVIEW.md` and `snapshots/2026_12_DEN_PIT/20261127T111648Z/LOCK.json` exist. `SCORE.json`, `pipeline/ledgers/2026_12_DEN_PIT.json`, and `grading/results/2026_12_DEN_PIT.jsonl` do not |
| Inactives hook is bound | `pipeline/hooks.py` `REGISTRY["official_inactives"] = "phase15.official_inactives:hook"` while `docs/PHASE_WORKFLOWS.md` still says no owner |
| Books default | `pipeline/hooks.py` `REQUIRED_BOOKS` default `fanduel,draftkings,betmgm,williamhill_us`. `docs/DATA_FRESHNESS.md` still says Bovada |
| Actions late start | `.github/workflows/nfl-gameday-gate.yml` comments: scheduled jobs start hours late; window is 40–88 minutes before kickoff |
| Lightning not in this repo | No trainer path. Only `data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md`. External repo was not opened |

`python3 -c` import of `cc_sim_v6` was not used as a run. The module reads parquet at import time, and the default source directory is missing. That is sufficient to call it not runnable as checked in. Pandas availability on one machine would not make it the contract entrypoint.

## (1) Inventory (callable entrypoints)

Checker: `python -m pipeline.phases --game <id> [--phase N] [--write] [--strict]` → `pipeline.phases.ledger` / `run_phase`. Output schema `nfl56-phase-ledger/1`. Tests: `pipeline/tests/test_pipeline.py`.

Freshness: `pipeline.freshness.check`. Policy dict `POLICY`, hooked dict `HOOKED`. Tests: `pipeline/tests/test_pipeline.py`, `test_newest_release.py`, `test_source_asof.py`.

Packet pull: `python3 -m pregame.build_packets --game <id>`. Writes `pregame/packets/<id>/packet.json` and `brief.md`. `pregame.packet` sets `projection_ready` false. Tests: `pregame/tests/test_pregame.py`.

Possession 100k: `python -m pipeline.sim100k --game <id> [--write]`. Gates G0–G7 in `preflight`. Engine: `default_engine` → `snapshots.lock.run_sim`. Tests: `pipeline/tests/test_pipeline.py` (`test_all_green_runs_engine_with_fixed_100k`, `test_default_engine_is_possession_engine_not_period_engine`, `test_engine_not_called_when_refused`).

Lock: `python3 -m snapshots.lock`. Score: `python3 -m snapshots.score`. Grade: `python -m grading.grade`. Readiness: `python -m evaluation.readiness` (does not set `projection_ready`). Protocol: `python3 -m evaluation.protocol`. Rocket: `./rocket`.

Slate (closest current chain, still not an orchestrator): `python -m pipeline.slate`. Due-game select: `python -m pipeline.window`. Inactives pull: `python -m phase15.official_inactives --game <id>`.

There is no `pipeline/orchestrator.py`.

Fifteen phase names are the `PHASES` tuple names in `pipeline/phases.py` lines 36–57. None of phases 1–13 or 6 has an analytical command that the checker invokes. Phase 14's analytical command is sim100k, which the checker does not run. Phase 15's pull is separate from the check.

## (2) Contradictions with #147 acceptance

1. No single command runs the full process for one game or the slate. `pipeline.slate` runs the checker and the possession gate only.
2. No supported clock triggers that process. The GitHub workflow exists and is disqualified by the issue.
3. The 15-phase ledger is not an execution receipt. Statuses differ (`AUTO`/`GAP` versus `PASS`/`BLOCKED`/`NOT_APPLICABLE`). Hashes, equations, and artifacts are not required.
4. Three methods do not each complete 100,000 trials. The canonical script is missing.
5. Main and Lightning are not runnable here. The BUF@MIN file says they were not run. Do not include them as if they were.
6. Game-script probabilities are not produced by phase 6. The checker only looks for `market.home_spread` and `market.total`. The script call is in `not_available_from_free_sources`.
7. Defense grades do not modify a numerical distribution inside `pipeline.phases`. Open PRs #140, #143, and #144 are the in-flight defense work and were not merged.
8. No automated red-team command can abstain.
9. Postgame scoring exists (`grading.grade`, `snapshots.score`) but DEN@PIT has neither a score file nor a grading jsonl, and neither tool implements the #147 error taxonomy or a sim_v6 comparison.
10. Tests prove gate refusal and field presence. They do not prove 15 analytical executions. `test_every_phase_has_explicit_status_and_command` asserts the checker, not execution.
11. This phase did not run the full offline suite, a research audit, or a per-game dry run of an orchestrator, because that orchestrator does not exist. The new tests only validate the inventory.
12. `projection_ready` was not changed. Writers that hard-code false include `pregame/packet.py`, `pipeline/phases.py` `ledger`, `pipeline/sim100k.py`, `snapshots/lock.py`, and `pipeline/__init__.py`.

## (3) sim_v6 versus sim100k / Main / Lightning

sim_v6 three methods: **not runnable**.

Distinct from sim100k: yes. sim100k is one possession simulation. sim_v6, as specified, is three prop methods at 100,000 trials each.

Distinct from Main and Lightning: yes. Those are not in this tree as executables. The scratch `cc_sim_v6.py` must not be renamed into either of them, and it must not be called calibrated. `calibration/simv56/engines/sim_v6_backtest.csv` is a table on disk, not a loaded parameter file and not prospective proof tied to a runnable entrypoint.

`core/period_engine_v0/monte_carlo.py` is a third, older family. Bias there is unimplemented. It is not one of the three methods.

## (4) Missing dependencies and fail-open risks

Missing: `tools/sim_v6.py`, both calib JSON paths, `rules/rulebook.py`, `README_run_gate.md`, `pipeline/orchestrator.py`, `render.yaml`, a Main entrypoint, a Lightning entrypoint, DEN@PIT score and grading outputs, phase execution receipts.

Fail-open:

- `pipeline.phases.main` returns 0 unless `--strict`.
- `pregame.build_packets --offline` writes from cache.
- Direct `simulate_games()` skips G0. The supported closed path is sim100k / the NFL-42 entrypoint.
- `cc_sim_v6.load_calib` returns None when the file is missing, and `mult` then returns 1.0.
- `run_gate.py` cannot reach its FAIL paths because `rules.rulebook` does not import.
- Packet `AUTO` is inherited when fields are merely present (`run_phase` else-branch `status = built["status"]`).

Fail-closed and not to be weakened: sim100k exit 2, lock immutability, rocket, grading exit 2, protocol missing-line refusal, phase 15 source rule, NGS unknowns left unknown.

## (5) Minimal orchestrator, dependency order

1. Receipt schema that cannot mark freshness as execution.
2. Recover real sim_v6 or stop. No substitute.
3. Idempotent runner: new directory per attempt, refuse if the destination exists, never overwrite `snapshots/<game>/<lock>/`, record commit and input hashes, call existing commands as subprocesses with their own labels (packet, checker, sim100k-as-NFL-43). sim_v6 step stays `BLOCKED` until step 2.
4. Defense numbers only from #140 / #143 / #144 outputs, inferred labeled inferred.
5. Scripts and opportunity, pre-kickoff features only.
6. 100k × 3 only through recovered sim_v6.
7. Red team that may abstain.
8. Postgame on the saved DEN@PIT lock, finals isolated from pregame inputs.
9. A clock that is not GitHub Actions, after a measured local dry-run.

`projection_ready` stays false at every step.

## (6) Tests that would prove execution (not implemented)

These are the tests a later phase needs. Shipping them now against `pipeline.phases` would pass for the wrong reason.

- For each phase 1–15, a fixture game whose packet fields are full and fresh, and an assertion that the receipt is still not `PASS` until that phase's equation list and output hash are present.
- Delete one equation output and assert the phase is `MISSING` or `BLOCKED`, not `AUTO`.
- Phase 14: a sim100k refusal must not satisfy a sim_v6 receipt. A sim_v6 receipt needs three methods, `n=100000` each, distinct seeds, and a non-1.0-by-default Bias only when a calib file hash is recorded. Absent calib is a failure, not M=1.0.
- Stale odds, missing PBP week, duplicate player rows, backup QB, inactive, rain, defensive mismatch, low-volume explosive role, script reversal, zero-stat active player, and a post-kickoff as-of must each fail closed.
- Re-running the orchestrator writes a second directory and leaves the first byte-identical.
- DEN@PIT finals are rejected as pregame inputs by the as-of check.

Inventory tests that do exist: `pipeline/tests/test_phase0_inventory.py`. They compare the manifest to `PHASES` / `POLICY` / `HOOKED` via `ast`, and they check paths. They do not execute phases.

## (7) Scheduler critique, Actions excluded

The only cron in-repo is GitHub Actions (`nfl-gameday-gate.yml`, `nfl-pregame-packets.yml`, and 20 other workflows). The issue forbids depending on it. Independently, `nfl-gameday-gate.yml` says scheduled jobs start hours late, so a T-90 inactive pull and a 40–88 minute window are not reliable even if Actions were available. `pipeline/window.py` only classifies. `pipeline/cadence.py` only labels freshness.

No `render.yaml`, no `Procfile`, no systemd unit. A Render cron is a plausible later host because the filesystem on that platform is ephemeral and artifacts would have to be committed or stored elsewhere, and because a web service spin-down does not fit a game clock. That is an option, not a decision. This phase did not deploy, did not create a blueprint, and did not measure 300,000 trials. Local/Cursor remains the validation path. Do not turn the existing workflow file on as a workaround.

## (8) Unknowns

- Where the original `tools/sim_v6.py` lives. The scratch file says originals were untouched. Reconstructing it from `cc_sim_v6.py` would be fabrication.
- Whether the 2026-11-09 Lightning branch still exists. Not opened.
- Whether `rules/rulebook.py` exists on another branch. Absent on this main.
- Render account, time limits, and secret availability. Not inspected.
- Open PRs #140, #143, and #144 may gain commits after 2026-11-27. Re-read them before phase 4.
- Full `scripts/test_offline.sh` was not run for this inventory. The phase-0 file is the test that was added.

## Links

- Issue: https://github.com/GhostPapii21/nfl-matchup-database/issues/147
- PR #140: https://github.com/GhostPapii21/nfl-matchup-database/pull/140
- PR #143: https://github.com/GhostPapii21/nfl-matchup-database/pull/143
- PR #144: https://github.com/GhostPapii21/nfl-matchup-database/pull/144
- PR #146: https://github.com/GhostPapii21/nfl-matchup-database/pull/146
- Checker: `pipeline/phases.py` `run_phase`, `ledger`, `main`
- Gate: `pipeline/sim100k.py` `preflight`, `default_engine`
- Spec: `workflows/operational_specs/PHASE_SCRIPT.md` step 9
- Manifest: `docs/automation/inventory_manifest.json`
