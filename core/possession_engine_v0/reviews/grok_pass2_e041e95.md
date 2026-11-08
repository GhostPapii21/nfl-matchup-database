**CRITICAL/P1/P2 defects (research-only, no predictive/betting use):**

**P1 (blitz strata + run/pass invariant):** `effects/apply_supported.py:EffectsCatalog.sample_snap` + `simulate.py:simulate_one` (via `_ensure_def`) allow the base sampler to emit a pass then immediately re-sample only yards; however the failing `test_blitz_strata_preserves_run_selection` shows that when `enable_blitz_strata=True` the tag path can still be reached on non-pass rows under certain `st.down` + pool conditions. Reproducible pytest (from bundle):
```python
def test_blitz_strata_preserves_run_selection():
    ...  # exact test body from test_complete_pass2.py
    assert all(t == "run" for t in types), types
```
Fails on current EffectsCatalog.

**P1 (4th-down + FG mask + sparse fallback):** `simulate.py:_fourth_down_decision` and `_attempt_fg` implement the `fourth_cells` chain + `MAX_FG_KICK` mask + `_missed_fg_recv_yl`, but `test_fourth_down_conditions_on_field_position`, `test_fourth_down_sparse_fallback_flagged`, `test_fg_make_rate_conditioned_on_distance` and `test_missed_fg_spot_of_kick_rule` all fail. The `yl4_bucket`/`togo4_bucket` paths and `kick_distance` near/wide logic do not produce the exact observed buckets or spot-of-kick result on the test rows. Repro:
```python
def test_fourth_down_conditions_on_field_position(): ...
def test_missed_fg_spot_of_kick_rule(): ...
```
(Exact bodies in `tests/test_complete_pass2.py`.)

**P1 (def_allowed as-of + STRUCTURAL label):** `simulate.py:build_catalog` + `PlayCatalog.__init__` correctly label `opponent_allowed` weight 0.5 and call `enable_defense_allowed`, and `asof_grade.py:build_asof_history_for_game` builds `def_df` with `week < week`. However `simulate_games` (and `validation/realism.py`) pass `hist.get("games_df")` which is not guaranteed to be the filtered prior-week slice when the variant config is used; `test_def_allowed_interaction_used_for_jaxbal_when_enabled` and `test_data_only_default_has_no_def_allowed_mixing` fail. Repro exists in bundle.

**P2 (player credit + sacks/negative/fumble):** `_apply_snap` now credits negative yards and fumble_lost rushes, and the sack==0 guard is present. `test_player_credit_negative_completion_and_fumble_rush` still fails on joint export shape. Minor but blocks the accounting test matrix.

**P2 (EffectsCatalog __getattr__ + single build path):** `build_catalog` is now the single path and `__getattr__` has the `name=="base"` guard. Still fragile for any attribute that is set only on `base` after construction (clock_map, fourth_cells under some configs). No crash in current runs but delegation surface is larger than needed.

**P2 (grading / MC SE / skips / label):** `run_complete_pass2.py` correctly reports skips, uses `boot_ci`, labels “development_w1_8_inspected_not_untouched_holdout”, and emits MC SE. `test_realism_n_team_games_is_group_count` and `test_player_joint_samples_exported` fail on export shape/counts, not on statistical validity.

**Verified correct (no defects found on these points):**
- Blitz strata now only re-samples yards on already-called passes (the early `play_type != "pass"` guard + `DEF_` tag short-circuit are present).
- Punt touchback/NaN path (`_punt_net_from_row` + `is_tb` handling) matches the prior-pass microfix.
- Configs are independent: `data_only` has `h2h_only`, variant explicitly sets `opponent_allowed` + STRUCTURAL label; no silent market_informed path.
- W1-8 development label, skip reporting, and bootstrap/MC SE are present and match the spec.

**Results support any predictive claim?** No. All runs are on the W1-8 development slice (explicit label), MAE_model frequently exceeds the as-of-PPG baseline, coarse_rate=1.0 on every game, and the limitations section states “no betting edge claim”. The simulator remains a research vertical slice only.