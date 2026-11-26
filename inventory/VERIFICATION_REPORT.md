# Verification report — public checkpoint

**When:** 2026-11-26 03:15 EST (America/New_York)  
**Base commit tested:** `fe2e3711b766d8894c49ec4dc571e6731628dc55`  
**Branch:** `cursor/nfl-model-checkpoint-3c89`  
**Pull request:** https://github.com/GhostPapii21/nfl-matchup-database/pull/1  
**Merge:** not authorized and not performed.

This run is the working tree of that commit plus the harness files named below. No model weights, frozen validator bytes, or excluded quote bodies were changed. No 100k simulation was started.

## Environment

| Item | Value |
| --- | --- |
| Python | 3.12.3 |
| Platform | Linux x86_64 |
| pytest | 9.2.0 |
| numpy | 2.5.5 |
| pandas | 3.1.1 |
| pyarrow | 26.0.1 |
| jsonschema | 4.26.0 |

Install command, from a clean checkout:

```sh
python3 -m pip install --user -r requirements-verify.txt
bash scripts/verify_public_checkpoint.sh
```

`requirements-smoke.txt` is only the two-module smoke. Parquet tests import PyArrow. The source-run gate imports `jsonschema`. Both are listed in `requirements-verify.txt`.

## Commands and results

| Suite | Command shape | Result |
| --- | --- | --- |
| Smoke | `bash scripts/smoke_offline.sh` | **9 passed** (0.53s) |
| Possession engine | `cd core/possession_engine_v0 && python3 -m pytest tests -q --tb=line` | **167 passed** (19.99s) |
| Period engine | `cd core/period_engine_v0 && python3 -m pytest tests -q --tb=line` | **23 passed, 12 failed** (2.35s) |
| Market calibration | `python3 -m pytest market_calibration/tests -q --tb=line -p no:cacheprovider` | **262 passed, 16 failed, 22 errors** (0.40s) |
| Repo export, penalty parser, source-run gate | `python3 -m pytest test_export.py data/redistributable/teams/tests research/nfl_sim_integration_2026-11-06/source_run_gate/tests -q --tb=line` | **96 passed** (1.90s) |
| Historical pre-rebind | `PYTHONPATH` includes the repo, `core/possession_engine_v0`, and `research/nfl_sim_integration_2026-11-06` | **6 skipped** (`HISTORICAL_PRE_REBIND_RECORD`) |

The market delivery-guard tests that do not need saved book files passed, including inclusive ±40 percentage-point quarantine in both directions, single-book and missing-quote fail-closed paths, and consumer payloads that stay non-surfaceable when quarantined. Quote tests that load the saved CSVs did not pass. They were not skipped or deleted.

## Packaging fixes in this follow-up

These were harness gaps, not model promotions:

- `requirements-verify.txt` documents PyArrow and jsonschema.
- `research/market_calibration` and `research/period_engine_v0` are import aliases. The implementation stays at `market_calibration/` and `core/period_engine_v0/`.
- `market_calibration/tests/conftest.py` puts the repository root on `sys.path`. The old `parents[3]` path matched a deeper worktree layout and made every market module fail to import.
- `scripts/verify_public_checkpoint.sh` runs the suites above and keeps going after a failure.

Without PyArrow, the possession suite on this commit did not finish the parquet tests (`ModuleNotFoundError: No module named 'pyarrow'`). That was an install gap, not a change in engine results. With PyArrow, the possession suite is 167 passed.

## Preexisting gaps (not “fixed” by skipping)

| Gap | Evidence | Class |
| --- | --- | --- |
| `core/period_engine_v0/data/play_by_play_2025.parquet` is not in the package | 11 period tests, `FileNotFoundError` | Missing prior-season input. Not downloaded. |
| Outlier CSV is not published | `test_outlier_csv_loads_and_flags_gaps` asserts `len(rows) > 0` and gets 0 | Private/unpublished input. |
| Saved FanDuel/DraftKings/Pinnacle CSVs and `artifacts/saved_quote_audit.json` | 22 market errors and 16 market failures. Paths are under `market_calibration/saved_quotes/` or the excluded audit | Intentional hash-only exclusion. Tests fail closed. |
| `python3 source_adapters/tools/run_gate.py` | `ModuleNotFoundError: No module named 'rules'` | The rulebook was not in the sanitized package. The CLI does not run. |
| 15-phase and 100k workflows | README states they are deferred. `known_flags/KNOWN_LIMITATIONS.json` has `DEFERRED_100K: true` and `Phase15: NOT_YET`. No test or script in this run set a 100k trial count | Goal, not an execution. Source-run gate tests use synthetic phase rows and still refuse a diagnostic run as projection-ready. |
| ORCA, FTN mirrors, Pinnacle actionability | Unchanged `ACCESS_UNKNOWN` / `NOLINE` | No auth bypass and no paid pull. |

Public HEAD checks only, bodies not saved: `https://github.com/nflverse/nflverse-data` returned 200, and the public ESPN NFL scoreboard URL returned 200.

## Safety checks

- Contaminated validator `core/possession_engine_v0/runs/dal_ind_suite_fix_2026-11-06/validate.py` SHA-256 is still `29b6b0c2644f256a705b09b5e1a56716dd355d79eb07a6187b9c3df495ff93e9`. Nothing imports it. `known_flags` marks it `HISTORICAL_CONTAMINATED_DO_NOT_USE_FOR_PROMOTION`.
- Decontamination validator SHA-256 is still `8a9d72949c122923ca149b635cd04290373112abc50930b85de5332491a201a1`.
- `projection_ready` is false. `entrypoint_enforced` is false. Unsupported semantics are penalties, returns, and official overtime. `test_semantics_are_explicitly_unsupported` is inside the 167 passing possession tests and rejects those features.
- Symlinks in the tree: 0.
- Secret scan of text files found no live token. The only `ghp_` bytes are the credential *pattern* in `export_snapshot.py` and the synthetic string the exporter test builds to prove that pattern is rejected.
- `OPEN_LINEAR_ITEMS.md` has 22 rows, including NFL-16 and NFL-54.
- Machine paths remain in historical integration scripts and in `source_adapters/tools/run_gate.py` (`SLIPS`). Current possession and period modules used by the passing suites do not point at `/workspace`. Those historical files were left byte-stable.

## What this does not certify

A passing possession suite is not production acceptance. Calibration is not fitted. Quotes stay `NOLINE` until authenticated book files exist outside this public tree. The pristine protocol is incomplete. Phase 15 is `NOT_YET`. 100k remains deferred because penalties, returns, and official overtime are unsupported.
