**Addressed (code evidence confirms explicit handling/documentation, no silent fixes claimed):**

- **1 (sparse_rate≈1.0 / coarse fallbacks)**: `empirical.lookup_plays` and `simulate.PlayCatalog.sample_snap` return explicit `SPARSE_STATE`/`SPARSE_STATE_FALLBACK_SAME_DOWN`/`EMPTY_TEAM_SNAPS` (never silent league pool). `simulate_games` collects `sparse_flags` + `evidence_summary.sparse_rate`; `validation/accounting.py` asserts `sparse_rate_reported`; `config/*` + `adjustment_ledger.py` + `provenance.py` document `no_league_fallback=true` + `SPARSE` status. `tests/test_asof_both_teams.py` asserts `silent_pool_applied=False`.
- **3 (fixed clock-cost)**: `simulate._clock_cost` hardcodes `means={"pass":22,"run":28,...}` + `rng.normal(mu,4)` (no empirical fit).
- **5 (OT single-possession)**: `state.start_ot_if_tied` + `simulate_one` + configs declare `"single_possession_approx_declared_limitation"`; `accounting.py` checks `ot_only_if_reg_tie`.
- **7 (missing pressure/man-zone/MOFO/CB-S-DT)**: `provenance.py` marks `MISSING`/`PROXY` (qb_hit only); `situational.py` + `effects/evidence_tables.py` + `effects/definitions.py` list absent columns + `man_zone_mofo_mofc_in_ftn=False`; `adjustment_ledger.py` forbids treating proxy as measured.
- **8 (some accounting/leakage)**: `validation/accounting.py` runs `reg_clock_target...`, `halftime_present_rate`, `period_quarter_scores_in_sim`, `ot_only_if_reg_tie`, `sparse_rate_reported`; `pbp_filter.py` + `config/*` enforce `weeks_inclusive`, `no_future_weeks`, `no_league_fallback`; `tests/test_audit_scoring_realism.py` + `test_asof_both_teams.py` assert no retroactive/future leakage.

**Open (confirmed by code; no resolution present):**

- **2 (offense-only / weak defense)**: Core sampler (`load_team_history` + `PlayCatalog`) is strictly `posteam in teams`; `load_involvement_plays` exists but is unused for defense sampling in `simulate_one`/`_apply_snap`. `effects/apply_supported.py` only adds optional blitz strata on offense rows.
- **4 (pace diagnostic sim~133 vs 2×59.9)**: `validation/realism.py:compare_sim_vs_actual_pace` explicitly computes `sim_snaps_minus_2x_team_snaps` (actual = per-team offense snaps; sim = joint both offenses) and reports the delta; no calibration applied.
- **6 (period grading 13/15, N=150 development only)**: `run_period_realism_grade.py` + `validation/period_grade.py` hardcode `N_SIMS=150`, label `"development_w1_8_inspected_not_untouched_holdout"`, preserve prior 0/15 artifacts; `metrics.json` + `SUMMARY.md` document W1 skips + separate period vs FG MAE.
- **8 (remaining settlement/sampling/accounting)**: `simulate.py` limitations list notes "Vertical slice... not calibrated"; `accounting.py` still shows `MIXED` on period recon in some runs; no settlement or full leakage matrix beyond the listed checks.

**Prioritized defects (highest first, with reproducible regression ideas):**
1. High `sparse_rate` + fine state buckets (test: `tests/test_audit_scoring_realism.py:test_data_only_mean_total_not_nfl_impossible` + assert `sparse_rate < 0.3` on 200 sims).
2. Offense-only sampling (test: extend `test_effects_supported.py:test_blitz_strata...` to assert defense interaction rows never sampled).
3. Fixed `_clock_cost` (test: `accounting.py` mean_plays band + assert `np.std(clock_costs) > 10` on 1000 plays).
4. Pace apples-to-apples mismatch (test: `validation/realism.py` delta assert `abs(delta) < 20` fails on current data).
5. Missing pressure features (test: `test_effects_supported.py` asserts `man_zone..._in_ftn is False` + no `CB_S_DT` columns).

**Rubric notes (no invented claims):** Math/game-state/clock correct where implemented (period reconciliation, OT tie check, geo-TD scoring); leakage prevented by explicit filters; discrete scoring uses actual yards (not historical TD flags); feature honesty explicit in provenance/ledger; calibration honesty stated as "research only... not calibrated"; next steps limited to existing tests + `EffectsCatalog` strata. No market-fit or three-model claims present.
