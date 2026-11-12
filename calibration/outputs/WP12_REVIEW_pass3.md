No merge blockers found in the updated diff.

- Clock-cache fix is correct: the key includes clock mode and timeout attribution, and incompatible cached maps are rebuilt. Other accounting switches consume the map without changing its construction.
- The new regression test covers default → `pre_wp12` and the reverse, comparing each reused map with a fresh catalog and confirming the run-clock values differ.
- The test docstring now acknowledges the fallback order as a structural choice, resolving the wording finding.
- Window-boundary synthetic tests, redistribution-frequency assertions, defense-allowed integration, and legacy behavioral regression can remain PR follow-ups. None is a merge blocker.

Static review only; no tests executed, files modified, Git commands run, or network accessed.

APPROVE
