# NFL-85: sim_v6 three-method authority audit

Status: **BLOCKED_ENTRYPOINT_ABSENT**. Production integration of the PHASE_SCRIPT triad is blocked. Calibrated Bias is **EXPERIMENTAL_UNVALIDATED**. `projection_ready` was not changed.

Machine-readable copy of the working-tree checks:

```bash
python -m evaluation.sim_v6_authority
```

That command exits 2 while the documented entrypoint is not production-ready. It does not simulate.

Audited tree: `main` @ `ef4cc69035b8827fe897a574a0d7d22091ee26b3` (equal to `origin/main` at audit time).

## Documented command

`workflows/operational_specs/PHASE_SCRIPT.md` step 9 requires `tools/sim_v6.py` at 100,000 trials each for Monte Carlo, calibrated Bias, and Game Randomness, for runs dated on or after 2026-11-05.

The command named by the engine docstring in the historical snapshot and in the vendored scratch copy is:

```bash
python3 tools/sim_v6.py run <legs.json> <out.json>
```

On this tree:

```text
python3: can't open file '/agent/repos/nfl-matchup-database/tools/sim_v6.py': [Errno 2] No such file or directory
```

`git ls-tree origin/main tools/sim_v6.py` returns nothing. `git log --all --full-history -- tools/sim_v6.py` is empty: that path was never committed on any branch. There is no `pyproject.toml` or `setup.py` entry point.

No process started, so there is no runtime, memory benchmark, or representative output artifact.

## What exists, kept separate

| System | Path | Callable command | Trials | Methods | This is sim_v6? |
|---|---|---|---|---|---|
| PHASE_SCRIPT sim_v6 | `tools/sim_v6.py` | `python3 tools/sim_v6.py run <legs.json> <out.json>` | — | — | Required path. **Absent.** |
| Scratch copy | `calibration/simv56/engines/cc_sim_v6.py` | Not a package command. Imported by the ensemble worker. | Declares `N=100_000`. The caller below overrides it. | `mc`, `bias`, `gr` inside one `Engine.sim` | **No.** File starts `# SCRATCH COPY for confidence_check_2026-11-03`. SHA256 `2248cd17d31f65d6575c324f049d5b274dee6d5f6910fef145d44bb685e05028`, matching `SHA256SUMS`. |
| simv56 ensemble | `calibration/simv56_pmodel.py` | `python -m calibration.simv56_pmodel run ...` | `N_TRIALS = 20000` | Three **engines** (`sim_v5`, `sim_v6`, `sim_v6_fix`), then means of `p_mc` / `p_bias` / `p_gr` | **No.** Research probability source `sim_v5_v6_ensemble`. |
| pipeline.sim100k | `pipeline/sim100k.py` | `python -m pipeline.sim100k --game <game_id>` | `TRIALS = 100_000` | One possession-engine run | **No.** Engine is `core/possession_engine_v0` via `snapshots/lock.py`. `default_engine` does not name Monte Carlo or sim_v6. NFL-43 / NFL-56. |
| Week 9 empirical runners | `research/week9_1pm_live/run_current_week9_1pm.py` | Script `main` | Research boards | `season_empirical`, `rolling5_empirical`, `opponent_shrunk_rolling5` | **No.** Does not mention sim_v6. |
| Lightning | Not in this repo | — | — | External opportunity-count experiment | **No.** Local note only: `data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md`. |

No adapter module maps any of those systems onto `tools/sim_v6.py`.

Parsed module constants, read from each file's semicolon assignment line (`N=100_000; ...; SHRINK_K=...; K_BIAS=...`). A start-of-line regex misses both names. These two files are not the same engine.

| File | `SHRINK_K` | `K_BIAS` | Bias fit column | Role |
|---|---:|---:|---|---|
| `calibration/simv56/engines/cc_sim_v6.py` | 30 | 30 | `pred_mc` | Scratch copy. With no calibration file, Bias uses multiplier 1.0 and differs from Monte Carlo by draw seed. |
| `calibration/simv56/engines/cc_sim_v6_fix.py` | 30 | 5 | that model's own `pred_bias` (`BIAS_WIN=4`) | Deprecated redesign. Not promoted. Not `tools/sim_v6.py`. |

`data/historical/postmortems/2026-11-03_code_notes_for_ghost6.md` says sim_v6_fix is deprecated and that `tools/sim_v6.py` is the only source. The fix file's own docstring describes a 4,000-trial leave-one-week-out note. That note is not a committed holdout scorecard, and this audit does not promote the file.

## Historical snapshot (not on main)

Commit `dc36f7f2` on `origin/research/matchup-database-local-2026-11-12` (open PR #18, description says research only, do not merge) stores a squashed local tree at `local_snapshots/nfl-database/tools/sim_v6.py`.

- Blob `ab2144f03f6ca3b57950a1f2528e305193e723cd` (23,086 bytes).
- That commit is not an ancestor of `main`. The path is not in this working tree.
- Header matches the scratch copy's design notes: `N=100_000`, `SEED=20261101`, `MODES=('mc','bias','gr')`, calibration file `tools/sim_v6_calib.json`.
- It is a research snapshot of another working tree, not the entrypoint on `main`.

Open PRs on `GhostPapii21/nfl-matchup-database` (28 at audit time, including #140, #143, #144, and #18) do not add `tools/sim_v6.py` on `main`. GitHub code search for `sim_v6.py` on the default branch returned no indexed hits.

## Three methods, as each scratch file actually implements them

These notes are not a claim that the PHASE_SCRIPT command runs. "Differs by draw seed" applies only to `cc_sim_v6.py`, where the parsed constants are `SHRINK_K=30` and `K_BIAS=30`.

- **Monte Carlo (`mc`)**: negative-binomial volume from season/last-3 means, binomial catches, resampled historical yards, opponent adjustment. Seed is `SEED` plus a digest of `player|market|mode`.
- **Bias in `cc_sim_v6.py`**: the same volume structure as Monte Carlo. `fit()` reads the `pred_mc` column. Parsed `K_BIAS` and `SHRINK_K` are both 30, so the "heavier shrink" described in that file's docstring is not what the constants do. `load_calib()` returns `None` when the calibration file is missing, and `mult()` then returns `1.0`. On this file, Bias then differs from Monte Carlo by draw seed.
- **Bias in `cc_sim_v6_fix.py`**: a different volume window (`BIAS_WIN=4`) and parsed `K_BIAS=5` against `SHRINK_K=30`. `fit()` uses that model's own predictions. Those parsed integers do not make the file the authoritative engine, and they do not supply a dated holdout.
- **Game Randomness (`gr`)**: a different volume path (beta share, lognormal pace, one normal margin draw with `SD_MARGIN=13.5`). That is one shock around the supplied spread, not three retained scenario branches (lead / neutral / trail).

`Engine.sim` stores each mode on its own key, so the three sample summaries are not concatenated before percentiles. `price_game_script` then sets edge from the arithmetic mean of the three probabilities (`sum(r['p'].values())/3`). The simv56 ensemble means again across modes and across v5/v6/v6_fix. Those averages are explicit and sit outside the sample arrays. They are still pooling of method outputs, and they are not the PHASE_SCRIPT entrypoint.

Emitted summary keys are mean, median, p10, p90, and rung probabilities. PHASE_SCRIPT asks for the 5th, 10th, 15th, 20th, 25th, and median. The 5th, 15th, 20th, and 25th are not computed.

## Calibrated Bias evidence

Label: **EXPERIMENTAL_UNVALIDATED**. Production integration is blocked on this point alone.

- No `tools/sim_v6_calib.json`, and no `__no_calib__.json`, anywhere in the tree.
- `calibration/simv56/engines/sim_v6_backtest.csv` has 1,096 rows, weeks 4–7 only, markets `passyds`, `rec`, `recyds`, `rushyds`, `rushrec`. Columns are raw `pred_mc`, `pred_bias`, `pred_gr`, and `actual`. 862 rows have `pred_mc != pred_bias`. That difference is consistent with two seeds of the same generator at a finite trial count. It is not a holdout of fitted multipliers.
- `cross_validate()` exists in the scratch file and defaults to 4,000 trials on weeks 4–7. No scorecard from that function is committed.
- `calibration/simv56_pmodel.py` refits from backtest weeks `< min(W, 8)`. An empty slice becomes `calib = None` (fail open).
- `research/nfl_sim_integration_2026-11-06/integration/certified_asof/workflows/latest_postmortem_context.md` (2026-11-05) records **BIASDUP**: in `sim_v6_calib.json`, Bias multipliers equaled Monte Carlo on every market, so the gate counted three models while two were independent. That calibration file is not in this repository, so the note cannot be re-scored here. It is enough to refuse a "calibrated" label.

`Engine(cutoff=...)` in the scratch copy drops plays on or after the cutoff. That leak control is not reachable, because `tools/sim_v6.py` is not here. Future-data leakage of the authoritative command is **not testable**.

## Gate and dependencies

`source_adapters/tools/run_gate.py` lists `monte_carlo`, `bias`, and `game_randomness`, rejects a sim script that does not end in `sim_v6.py`, and rejects `n < 100000`. It imports `rules.rulebook`. `rules/rulebook.py` is not on this tree, and there is no `tools/run_gate.py`. The gate cannot be imported in a clean checkout of `main`.

The scratch engine imports pandas and numpy and reads parquet at import from `SIMV6_SRC` or `runs/2026-11-01_shared_src`. That directory is not on `main`. The ensemble builds the expected names with symlinks. None of that is the documented command.

## Acceptance tests that did not run

The issue asks for independent method runs, exact 100,000 counts, seed repeats, distinct-method checks, three retained branches, fail-closed missing calibration, leakage checks, malformed-output failure, and a benchmark. Those tests require the entrypoint. Running `cc_sim_v6.py` or `pipeline.sim100k` in their place would substitute another engine. They were not run.

Identity tests that did run:

```bash
python -m pytest evaluation/tests/test_sim_v6_authority.py -q
python -m evaluation.sim_v6_authority
# exit 2, verdict BLOCKED_ENTRYPOINT_ABSENT
```

`test_each_scratch_file_keeps_its_own_semicolon_constants` reads `SHRINK_K` and `K_BIAS` from `cc_sim_v6.py` (30 and 30) and from `cc_sim_v6_fix.py` (30 and 5). A parser that misses the semicolon line fails that test, because two missing values are not treated as equal.

## Minimal remediation

1. Leave `pipeline.sim100k`, `calibration.simv56_pmodel`, the Week 9 empirical runners, and Lightning on their own commands. Do not register them as `tools/sim_v6.py`.
2. Do not revive `cc_sim_v6_fix.py` as the authoritative Bias method.
3. A follow-up review can recover `local_snapshots/nfl-database/tools/sim_v6.py` from `dc36f7f2` and diff it against `cc_sim_v6.py` (`CC_OPP`, `__no_calib__.json`, `volume_fix`, `qb_rush_prior`) before anything is copied to `tools/sim_v6.py`. Recovery is outside this audit.
4. The recovered command has to pass, in a clean environment, without a substitute: 100,000 trials per method per game, repeatable seeds, three method outputs kept intact, PHASE_SCRIPT percentiles, and a missing calibration file that fails the process.
5. Ship the calibration file with a dated training window and a later holdout or walk-forward scorecard. Until those numbers exist, Bias stays experimental and stays out of production wiring.
6. Restore `rules/rulebook.py` or stop the gate from importing it, in a separate change. A gate that cannot import does not make the engine real.
7. Keep `projection_ready` false. Do not merge or deploy from this audit.

NFL-82 (Phase 0 inventory) was still in progress when this audit was written. This report is the simulation-entrypoint section that inventory asked for. It does not close NFL-82.
