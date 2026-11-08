# Data & license manifest — possession_engine_v0

Assessed **read-only remote** (no repository clone) on 2026-11-05 America/New_York.

| Source | Role | License | Provenance | Our use |
|---|---|---|---|---|
| [nflverse/nflfastR](https://github.com/nflverse/nflfastR) | PBP schema / community data conventions | **MIT** (Copyright 2020 Sebastian Carl; Ben Baldwin) — LICENSE.md fetched via raw.githubusercontent.com | Public GitHub + nflfastr.com | Local parquet already on machine (`play_by_play_2026.parquet`); schema-compatible columns. **No nflfastR R source copied.** |
| [rtelmore/NFLSimulatoR](https://github.com/rtelmore/NFLSimulatoR) | Conceptual drive/play resampling inspiration | **MIT** (`MIT + file LICENSE`; Copyright Ryan Elmore and Ben Williams; YEAR 2019) — DESCRIPTION + license page datacolorado.com/r/nflsimulator/license | Public docs/DESCRIPTION fetched; **repository not cloned** | Conceptual only. Original Python implementation. **No R package source copied.** |
| Local PBP 2026 | Team filter JAX/BAL weeks 1–8 | nflverse-compatible play-by-play already materialized as a regular file | `core/period_engine_v0/data/play_by_play_2026.parquet` (former local symlink removed) | Read-only filter; research |
| Dated QB/injury notes | Adjustment layer inputs | Internal research notes | `runs/2026-11-05_JAX@BAL_r2/brainstorm_read.md` (ESPN/team IR notes dated 2026-11-03) | Forward-only config JSON; not applied retroactively |

## NOTICE
This module is independent research code. MIT notices for conceptual sources retained above. Do not redistribute as a derivative of NFLSimulatoR without including its MIT notice; we did not copy its code.
