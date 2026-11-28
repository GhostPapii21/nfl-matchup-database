# Phase 0 inventory (NFL-82)

Read-only inventory of `main` at `ef4cc69035b8827fe897a574a0d7d22091ee26b3` (merge of PR #146). Machine-readable twin: [inventory_manifest.json](inventory_manifest.json). Review packet: [GROK_REVIEW_PACKET.md](GROK_REVIEW_PACKET.md).

This phase does not change model weights, projections, betting gates, `projection_ready`, the production database, secrets, deployment, or any scheduler. `projection_ready` stays false. Nothing here is production-ready.

## Verdict

`python -m pipeline.phases` is a freshness and field-presence checker. It does not prove that the 15 phases executed. The canonical three-method entrypoint `tools/sim_v6.py` is **missing**. `python -m pipeline.sim100k` is a different thing: one NFL-43 possession-engine run of 100,000 trials. There is no per-game orchestrator. GitHub Actions is not an available required clock, and this repo has no Render worker or cron blueprint.

Scratch code under `calibration/simv56/engines/cc_sim_v6.py` contains `mc`, `bias`, and `gr` branches. It is a scratch copy, it is not `tools/sim_v6.py`, its calib file is absent, and it is not labeled calibrated.

## How a phase row is decided

`pipeline/phases.py` `run_phase` does four things:

1. Looks up dotted fields on the packet. A non-empty value is filled. An empty or missing value is missing.
2. Looks up each freshness source. `FRESH` and `NOT_REQUIRED` count as filled. `STALE`, `GAP`, `NOT_YET`, and anything else become those statuses.
3. Phase 14 appends `NOT_YET` when `sim100k.preflight` did not run the engine. The checker does not call the engine.
4. Phase 15 uses `phase15_status` (official inactives after T-90). ESPN is not accepted.

If nothing is blocking, the status copied from the packet ledger is `AUTO` or `PARTIAL`. The word `PASS` is not a phase status. `BLOCKED` on the packet becomes `MISSING` in this ledger. There is no phase-level `NOT_APPLICABLE` (`NOT_REQUIRED` exists only on a source row, for indoor weather).

Default CLI exit is 0. `--strict` exits 3 when a selected phase is `MISSING`, `STALE`, `GAP`, or `NOT_YET`. A green default run is not a completed analysis.

Issue #147 asks for `PASS / PARTIAL / MISSING / STALE / BLOCKED / NOT_YET / NOT_APPLICABLE`, plus inputs actually read, source ids, timestamps, data-through date, hash, sample size, denominators, equations invoked, output paths, and an evidence-versus-inference label. The current ledger schema is `nfl56-phase-ledger/1`. It does not carry those fields. Availability is not execution.

| # | Phase | What the checker actually does | Analytical command on main |
| --- | --- | --- | --- |
| 1 | Slate, schedule, venue | Packet fields + schedule freshness | none |
| 2 | Player identity and position | Roster fields | none |
| 3 | Verified player game history | By-game logs present | none |
| 4 | Role, snaps, routes, opportunity | Snaps present. Routes are listed as not in free public NGS, not zero | none |
| 5 | Team offense/defense baselines | Allowed / produced / rank fields present | filled earlier by `pregame.build_packets` |
| 6 | Opponent context and game script | Spread and total present. The script call is explicitly not in a free source | none |
| 7 | Coverage structure and shell | Charted dropbacks. Man/zone and shell are a free-source gap | none. Open PRs #143 and #144 |
| 8 | Defender assignment and explosives | PFR defender rows present. Who covers whom is unknown | none. Open PR #143 |
| 9 | QB pressure, blitz, scramble | Allowed block present. True pressure rate is a floor, not a rate | none |
| 10 | Offensive line, pass rush, coaching | Depth chart and coaches. Line grades are a paid gap | none |
| 11 | Injury and depth chart | Official report, ESPN live list, depth chart | none |
| 12 | Weather, roof, travel | Roof and weather status | none. Open PR #140 adds an hourly weather grade flag |
| 13 | Timestamped book prices | `books.markets` plus odds / four-book freshness | `python -m pregame.multibook --game <id>` writes a freeze. It does not grade a phase |
| 14 | Projection and simulation (100k) | `NOT_YET` until `pipeline.sim100k` actually runs | `python -m pipeline.sim100k --game <id>` possession engine, 100,000 trials, one method family |
| 15 | Final inactive pregame freeze | Official inactives hook after T-90 | `python -m phase15.official_inactives --game <id>` pulls. The checker only reads |

Names match `PHASES` in `pipeline/phases.py`.

## sim_v6 versus sim100k versus Main / Lightning

| Piece | Path | Runnable as the #147 three-method contract? |
| --- | --- | --- |
| Canonical sim_v6 | `tools/sim_v6.py` | No. File not in the tree. `workflows/operational_specs/PHASE_SCRIPT.md` step 9 and `source_adapters/tools/run_gate.py` `check_simv6` both require a script path ending in `sim_v6.py`. |
| Fitted calib | `tools/sim_v6_calib.json` and `calibration/simv56/engines/__no_calib__.json` | No. Both absent. |
| Scratch engine | `calibration/simv56/engines/cc_sim_v6.py` and `cc_sim_v6_fix.py` | No. Header says scratch copy. `MODES=('mc','bias','gr')` and default `N=100_000` are in the file. Import reads parquet from `SIMV6_SRC`, defaulting to `calibration/simv56/runs/2026-11-01_shared_src/`, which is not in the tree. `oppadj` reads `CC_OPP` from the environment. With no calib file, `mult()` returns 1.0, so `mc` and `bias` share a volume branch and differ by seed. `gr` is a different volume branch. Not a game orchestrator. Not calibrated. Not a substitute. |
| simv56 ensemble | `calibration/simv56_pmodel.py` | No. `N_TRIALS = 20000`. Three engine files, not the gate path. |
| Possession 100k | `pipeline/sim100k.py` → `snapshots/lock.py` `run_sim` → `core/possession_engine_v0/simulate.py` `simulate_games` | Runs only when G0–G7 pass. Exactly 100,000 trials, one engine, research only, `projection_ready` false. The file does not mention Monte Carlo, Bias, or Game Randomness. |
| Period engine | `core/period_engine_v0/monte_carlo.py` | Experimental. Header: `Bias: UNIMPLEMENTED`. Its game-randomness shock is not sim_v6. sim100k used to call this engine and no longer does. |
| BUF@MIN artifact | `research/third_down/BUF_MIN_W9_MC_100K_X_3_SCENARIOS_X_3_METHODS_20261109.json` | Methods are `historical_shares`, `route_drive_opportunity`, `injury_protection_downside`. `not_run_actual_main_or_lightning` is true. |
| Main | no entrypoint in this repo | Missing. Do not alias it to sim100k. |
| Lightning | `data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md` | The report is in-repo and dated 2026-11-09. It points at another repository. This phase did not open that repository. No Lightning trainer exists here. Not a sim_v6 method. |

`source_adapters/tools/run_gate.py` names the three models and would check a finished run directory. It imports `rules.rulebook`, and `rules/rulebook.py` is not on main, so the gate cannot be imported. `README_run_gate.md` is also absent. Recover the rulebook before treating that gate as executable. Do not invent its thresholds.

## Source adapters, freshness, evaluation

Freshness keys in `pipeline/freshness.py` `POLICY`: schedule, play_by_play, rosters, depth_charts, snap_counts, ftn_charting, pfr_defense, official_injuries, news_injuries, weather, odds, ngs_passing, ngs_receiving, ngs_rushing.

Hooked keys: official_inactives, four_book_prices, ngs_defender_matchup.

Age is from the publisher stamp when the source is publisher-dated. No stamp is `MISSING`, not fresh. A completed game absent from a latest-release file is `GAP`, not `STALE`. `pipeline/cadence.py` labels those rules. It does not start a process.

Callable adapters and gates that do exist:

| Command | Role | Status |
| --- | --- | --- |
| `python3 -m pregame.build_packets --game <id>` | Writes `packet.json` and `brief.md`. Research only | Integrated. `--offline` warns and still writes |
| `python -m pregame.multibook --game <id>` | Four-book freeze | Integrated |
| `python -m phase15.official_inactives --game <id>` | Official inactives | Integrated. Bound in `pipeline/hooks.py` |
| `python -m pipeline.sim100k --game <id> --write` | Possession 100k or refuse (exit 2) | Integrated, research only |
| `python3 -m snapshots.lock ...` | Immutable lock | Integrated. `projection_ready` false |
| `python3 -m snapshots.score --snapshot <dir>` | ESPN final vs lock | Executable. DEN@PIT lock has no `SCORE.json` |
| `python -m grading.grade --game <id> --write` | Packet vs final | Integrated. No `grading/results/2026_12_DEN_PIT.jsonl` on this commit |
| `python -m evaluation.readiness` | Report only | Does not set `projection_ready` |
| `python3 -m evaluation.protocol freeze\|ledger\|evaluate` | Pristine protocol | Fail-closed on a missing line |
| `./rocket [game_id]` | sim100k G6 | Does not run phases or sim_v6 |
| `python3 source_gap_ledger.py` | Stored-coverage inventory | Local DB, no network |
| `python -m source_adapters.circa.build_rows <capture>` | Circa OCR | Experimental, manual |
| `python3 data/scheme_profiles/build_profiles.py` | Scheme tables | Experimental relative to the phase board |

`docs/PHASE_WORKFLOWS.md` says the inactives hook has no owner. `hooks.REGISTRY["official_inactives"]` is `phase15.official_inactives:hook`. The code governs.

`docs/DATA_FRESHNESS.md` lists Bovada in the four-book default. `hooks.REQUIRED_BOOKS` default is `fanduel,draftkings,betmgm,williamhill_us`. The code governs.

## DEN@PIT (PR #146)

Merged. Package: `runs/2026-11-27_DEN@PIT/` (`POSTGAME_REVIEW.md`, `PREGAME_PROJECTION.md`, `RICO_SLIPS_LOCK.md`, pbp). Packet: `pregame/packets/2026_12_DEN_PIT/packet.json`. Possession lock: `snapshots/2026_12_DEN_PIT/20261127T111648Z/LOCK.json` with `projection_ready` false.

Not on this commit: `pipeline/ledgers/2026_12_DEN_PIT.json`, `pipeline/ledgers/2026_12_DEN_PIT.sim100k.json`, `snapshots/.../SCORE.json`, `grading/results/2026_12_DEN_PIT.jsonl`.

Use the package as a postgame regression fixture later. Do not feed its final box into a pregame run.

## Open PRs — do not duplicate

The code inventory stays pinned to main `ef4cc690`. The open-PR list below was refreshed on 2026-11-28. Live PR state can still move.

| PR | What it already owns | This phase |
| --- | --- | --- |
| [#140](https://github.com/GhostPapii21/nfl-matchup-database/pull/140) | `pipeline/read_rules/` targets-first, defense-allowed profile, hourly weather grade, flags only. Also touches `docs/PHASE_WORKFLOWS.md` | Do not reimplement. Do not edit that doc here |
| [#143](https://github.com/GhostPapii21/nfl-matchup-database/pull/143) | `data/coverage/defender_profiles_2026/` for all 32 defenses, inferred attribution kept separate from verified | Do not duplicate |
| [#144](https://github.com/GhostPapii21/nfl-matchup-database/pull/144) | `data/coverage/positional_allowances_2026/` windows, opponent adjustment, situational splits. Also touches `scripts/test_offline.sh` | Do not duplicate |
| [#146](https://github.com/GhostPapii21/nfl-matchup-database/pull/146) | DEN@PIT postgame, merged | Fixture only |
| [#137](https://github.com/GhostPapii21/nfl-matchup-database/pull/137) | The only edit to `evaluation/tests/test_readiness.py`. It discovers Week 12 locks from `snapshots/2026_12_*/*/LOCK.json`, requires each lock to be before kickoff, and keeps `projection_ready` false | This inventory does not edit that test. Later phases must not add a second assertion |

Other open PRs are lock/holdout work (#134, #135, #136, #138, #139, #145, #148), postgame or grading logs (#119, #120, #131, #132, #142), board or parser fixes (#107, #113, #116), research drafts (#14, #18, #30, #39, #41, #55, #63, #64, #69), a separate sim_v6 absence note (#150), execution receipts (#151), and a non-Actions scheduler (#152). #151 and #152 had copied the readiness assertion with hardcoded game ids. Those copies are removed; #137 remains the only implementation. The orchestrator should call existing graders and lockers, not replace those branches. Full rows are in the manifest.

## Scheduler

Cursor or a local shell is the development and validation path.

| Option | In this repo | Use as the required clock? |
| --- | --- | --- |
| `.github/workflows/nfl-gameday-gate.yml` | Cron every 15 minutes on game days, then window → inactives → packet → lock → `pipeline.sim100k` → ledger | No. Actions usage is unavailable. The workflow comment says scheduled jobs on this repo start hours late, which misses a 40–88 minute pre-kickoff window. It also runs sim100k, not sim_v6 |
| `.github/workflows/nfl-pregame-packets.yml` | Packet refresh | No, same constraint. It does not run the phase checker |
| `pipeline/window.py` | Selects due games | It does not run unless something calls it |
| `pipeline/cadence.py` | Freshness labels | Not a worker |
| `render.yaml` / `Procfile` | Absent | Not configured. Not deployed by this phase |

A later phase can measure a real orchestrator dry-run locally, then propose an always-on cron as a reviewed blueprint. Runtime of 100,000 × 3 trials is unknown because that entrypoint is not runnable. Do not deploy from this inventory.

## Fail-open risks

- `pipeline.phases` without `--strict` exits 0 on a ledger full of `MISSING`.
- `pregame.build_packets --offline` writes from cache.
- Direct `simulate_games()` can skip the NFL-42 guard. `pipeline.sim100k` and `./rocket` are the closed paths.
- If someone later imported `cc_sim_v6.py` with data present and no calib file, Bias multipliers would be 1.0 instead of a refusal.
- `run_gate.py` crashes on import, so it never reaches its fail-closed checks.
- A packet field that merely exists can inherit `AUTO`.

Fail-closed today, and left unchanged: sim100k exit 2, snapshot lock, rocket, `grading.grade` exit 2, `evaluation.protocol` on a missing line, phase 15 rejecting ESPN, public NGS gaps staying missing rather than zero.

## Dependency-ordered plan (Phase 1 onward)

Do not start Phase 2 by writing a new simulator.

1. **Receipt schema.** New module beside the checker. A row cannot be `PASS` without inputs, source ids, hashes, equations, and artifacts. Keep `pipeline.phases` labeled as a checker. No gate, weight, or `projection_ready` change.
2. **Recover sim_v6 or stop.** Authoritative `tools/sim_v6.py` plus a fitted calib and a prospective holdout. Scratch `cc_sim_v6.py` is evidence of an approach, not the source to ship. Until then Bias stays experimental and uncalibrated. `rules/rulebook.py` is a separate blocker for `run_gate.py`.
3. **Orchestrator dry-run.** One game command and one slate command. New timestamped directory every run. Never overwrite a lock or a prior run. Subprocess the existing packet builder and the checker. Call `pipeline.sim100k` only under an NFL-43 label. sim_v6 stays blocked. `projection_ready` stays false.
4. **Defense, after #140 / #143 / #144.** Consume those artifacts. Keep inferred assignment distinct from verified. Do not add a second coverage tree.
5. **Opportunity and scripts.** Volume before efficiency. At least three scripts, probabilities sum to 1, features available before kickoff. Unknown routes stay unknown.
6. **Three-method 100k.** Only after step 2. 100,000 trials each, seeds, commit, hashes, per-script counts. Short runs fail closed. sim100k remains a separate receipt.
7. **Red team.** Must be able to return no play. Not scored on producing picks.
8. **Postgame.** Grade the DEN@PIT lock and the #146 package without using finals as pregame input. New error classes are test candidates, not automatic promotions.
9. **Clock.** Local runner first. A Render cron (or equivalent) is a candidate only after a measured dry-run, as a blueprint, not a deploy. Actions stays off the required path.

## Tests

Registry checks, not model runs:

```bash
python3 -m pytest -q -p no:cacheprovider pipeline/tests/test_phase0_inventory.py
```

The tests parse `PHASES`, `POLICY`, and `HOOKED` from source and compare them to the manifest, require every `exists: true` path to be on disk, require every `exists: false` path to be absent, and require `tools/sim_v6.py` to stay missing. They do not import `cc_sim_v6.py` (that import reads parquet immediately).

Ran on this branch with `python3 -m pytest` 9.2.0, after the manifest was written, from the repo root:

```text
python3 -m pytest -q -p no:cacheprovider pipeline/tests/test_phase0_inventory.py
......                                                                   [100%]
6 passed in 0.04s
```

The six tests are `test_manifest_is_phase0_and_research_only`, `test_code_enums_match_source`, `test_component_paths_match_the_tree`, `test_sim_v6_contract_is_missing_and_not_sim100k`, `test_named_prs_are_not_duplicated_by_this_inventory`, and `test_human_docs_match_the_manifest_verdict`.

Re-run the same command before treating the manifest as current. The inspected tree stays main `ef4cc690`. This branch is stacked on #137 so CI uses that PR's readiness assertion, and this diff does not change `evaluation/tests/test_readiness.py`. The full `scripts/test_offline.sh` suite was not re-run here. `evaluation/tests/test_readiness.py` on the #137 branch, after main was merged into it, passed 7 tests.
