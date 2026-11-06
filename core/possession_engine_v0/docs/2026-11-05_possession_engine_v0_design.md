# possession_engine_v0 — bounded design (2026-11-05)

**Authorization:** Rico direct room approval to build possession/PBP research module from both-team W1–8 + dated QB/injury updates. No further approvals inside research scope.
**Tree:** `/workspace/wt-period-engine` branch `research-period-engine-2026-11-05`. Preserves `period_engine_v0`.

## Goal
Research-only possession / play-by-play Monte Carlo for JAX@BAL using **only** 2026 W1–8 PBP involving JAX and BAL (offense and defense as observed), plus an explicit dated adjustment layer for QB/injuries/workload swaps. No betting edge claims.

## Approaches considered
1. **Full per-play EP model with league priors** — rejected: silent league pooling forbidden; would overclaim.
2. **Port NFLSimulatoR R code** — rejected: no cloning; we take **conceptual** inspiration only (drive/play resampling from nflfastR-shaped PBP) under MIT provenance, original Python.
3. **Recommended: team-only empirical vertical slice** — resample team plays/drives with explicit sparse-state statuses; dated adjustments forward-only; freeze `data_only` vs `script_adjusted` configs.

## Vertical slice (this delivery)
- State: quarter, clock seconds, down, distance, yardline_100, possession, score_home/away, half.
- Events: kickoff, snap (pass/run), punt, FG, PAT, turnover, turnover-on-downs, score, half, OT start.
- Joint player accounting: counts from the **same** resampled historical play rows (passer/rusher/receiver).
- Evidence: every state sample reports `n_evidence`; if below `min_n`, status `SPARSE_STATE` — **no silent pool**.
- Proposed pooling: config field only; default `enabled=false`.
- Adjustments: dated JSON; exclude OUT QBs from forward offense pools; do not invent Fagnano history; do not rewrite past weeks.
- Seeds: SHA256 stable seed (same pattern as period_engine_v0).
- Holdout: W1–8 = development; future weeks reserved untouched.
- Run size: attempt practical N; 100k only if completes in reasonable time; else report blocker.

## Explicitly out of slice / missing
- Full NFL strategy optimizer (4th-down EV tables)
- Opponent-adjusted EPA models / player prop engine
- Weather physics, OL/skill interaction graphs
- Pinnacle calibration / ROI
- Silent league bootstrap
- Fabricated replacement-QB careers
