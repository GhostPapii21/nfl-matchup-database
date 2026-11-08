**All prior Codex findings verified as fixed in the shown diff/code at 8a4ce0117cecb051b7eb5b8e5805c057c820d4b4.**

- foreign-row player credit: `sample_snap` (DEF_ALLOWED path) explicitly nulls `passer/rusher/receiver_player_name` before return; `_credit_player` guards `isinstance(name, str) and name and name != "nan"`.
- TD credit cap: `_apply_snap` now bounds `yards` (positive/negative) to remaining field position *before* the `if pass/run` credit blocks.
- mixture-before-H2H order: DEF_ALLOWED block precedes DEF_COND block in `PlayCatalog.sample_snap`.
- blitz coarse/NO_POOL reporting: `EffectsCatalog.sample_snap` emits `BLITZ_NO_POOL` / `COARSE_BLITZ_DOWN_n=...`; `simulate_games` counts `blitz_coarse_down_events` and `startswith("EFFECT_")`.
- target-week guard: `simulate_games` raises `ValueError` if `weeks_inclusive[-1] >= week_asof_exclusive`.
- game-unit bootstrap: `paired_game_diffs` + `diff_boot95_game_unit` now used.
- punt touchback/NaN: `_punt_net_from_row` + `_punt_fixed` handle `touchback`/`punt_in_endzone` flags and `kick_distance` NaNs with explicit own-20 logic.

**No new CRITICAL or P1 defects found** in game-state, clock, settlement, sampling, leakage, accounting, or effect execution vs. FEATURE_EXECUTION_MATRIX. (Minor observation: snap events record pre-bound `yards`; credits use post-bound value. Not a correctness or leakage issue.)

**Predictive claims:** None are supported. COMPLETION_CHECKLIST and FEATURE_EXECUTION_MATRIX both state explicitly that this is a development set (W1–8), no holdout, and “No predictive improvement over naive baselines demonstrated.”

All 71 tests pass per the query; the supplied `test_adversarial_review.py` (now in the tree) covers the prior fixes and passes. No reproducible pytest for new defects.