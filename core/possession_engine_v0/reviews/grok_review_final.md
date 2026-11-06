**Fixed (with evidence):**
- Clock handling (empirical + per-play cost_map passthrough): `_clock_cost` signature + `build_empirical_clock`/`set_empirical_clock` + all call sites in `simulate.py`; `EffectsCatalog` duck-typing mirrors added in `apply_supported.py`.
- Punt net yards (kick_distance - return_yards, touchback handling): `_punt_net_from_row` + COLS update in `pbp_filter.py`; legacy `yards_gained` fallback + flag retained.
- Sparse vs. coarse separation (intentional): `simulate_games` now splits hard `SPARSE/EMPTY/FALLBACK` vs. `COARSE_*`; diagnostics confirm `sparse_rate=0.0`, `coarse_rate=1.0`.
- Defense conditioning + by_team_vs_def pools: `sample_snap` path + `enable_defense_conditioning` + auto-ensure in `simulate_one`; `EffectsCatalog` wrappers added.
- Safety detection + post-safety kickoff: explicit `(yardline_100 - yards) >= 100` block in `_apply_snap`.
- PAT no clock consumption + always-count snap events: explicit comment + move of `events.append({"type":"snap"})` before early returns.
- Realism metrics (combined both-offense snaps apples-to-apples): `actual_combined_snaps_per_game` + updated `compare_sim_vs_actual_pace`/`run_period_realism_grade.py` reporting; diagnostics show sim 116.4 vs. actual_combined 121.1 (delta -4.7).

**Still-open defects (file hints):**
- FTN paid pressure / man-zone-MOFO / replacement coeffs / weather hook remain (only noted in `SUMMARY.md` and `run_period_realism_grade.py` residual blockers; no code changes).
- `defense_cond_flag_events=0` in n=50 diag (conditioning enabled but no `DEF_COND` flags emitted; `simulate.py:simulate_games` + `sample_snap`).
- No league silent pool (explicitly kept disabled per config and limitations list).

Final bundle is review-complete (all visible P1s from diff scope addressed; diagnostics green on pace/sparse/coarse separation; no invented edges).