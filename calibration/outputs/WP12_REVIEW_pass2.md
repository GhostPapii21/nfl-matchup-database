Prior findings:

- **PARTIALLY — Clock conservation after filtering.** The loss is now explicitly documented at [simulate.py:132](/tmp/wt-engine-fix/core/possession_engine_v0/simulate.py:132), and bounded on historical data at [test_penalty_clock.py:156](/tmp/wt-engine-fix/core/possession_engine_v0/tests/test_penalty_clock.py:156). Merged intervals above 60 seconds are still discarded at `simulate.py:164`; synthetic quarter-boundary and window-boundary tests remain missing.

- **FIXED — Unresolved chains preserve the original draw.** [simulate.py:547](/tmp/wt-engine-fix/core/possession_engine_v0/simulate.py:547) saves `orig`; both failure exits return it. [test_goal_line_truncation.py:208](/tmp/wt-engine-fix/core/possession_engine_v0/tests/test_goal_line_truncation.py:208) covers failure after a replacement.

- **FIXED — Arbitrary redraw limit.** [simulate.py:548](/tmp/wt-engine-fix/core/possession_engine_v0/simulate.py:548) removes the cap and terminates through increasing thresholds or candidate exhaustion. The new test at `test_goal_line_truncation.py:217` contains 30 censored rows, although random draws do not guarantee traversing more than 25 replacements.

- **PARTIALLY — Mechanics and compatibility coverage.** Added isolated WP1 coverage ([test_penalty_clock.py:175](/tmp/wt-engine-fix/core/possession_engine_v0/tests/test_penalty_clock.py:175)), a pre-WP12 score/RNG golden regression (`:197`), tie handling, and blitz-wrapper integration ([test_goal_line_truncation.py:199](/tmp/wt-engine-fix/core/possession_engine_v0/tests/test_goal_line_truncation.py:199), `:230`). Still missing redistribution-frequency assertions, actual defense-allowed integration, and a legacy behavioral regression. Historical TD tolerances remain correctness gates at `test_goal_line_truncation.py:174–182`.

- **PARTIALLY — “No parameters” wording.** [simulate.py:524](/tmp/wt-engine-fix/core/possession_engine_v0/simulate.py:524) now acknowledges the fallback as a structural choice, and the cap is gone. The test-module description still claims “no parameters” at [test_goal_line_truncation.py:6](/tmp/wt-engine-fix/core/possession_engine_v0/tests/test_goal_line_truncation.py:6).

New issue:

- **SHOULD-FIX — Reusing a catalog silently ignores changes to timeout attribution.** [simulate.py:791](/tmp/wt-engine-fix/core/possession_engine_v0/simulate.py:791) computes the map using the current accounting setting, but `:797–804` only initializes an absent map. Run default accounting once, then `pre_wp12` with the same catalog: pass/run costs retain merged timeout seconds despite requesting `"drop"`. The reverse order silently omits attribution under defaults. Key the cached map by the relevant accounting settings, or reject incompatible catalog reuse; test both orders.

Static review only; I did not execute tests, modify files, run git, or access the network.

REQUEST CHANGES
