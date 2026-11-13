#!/usr/bin/env bash
# Run every offline test suite in the repository. Each suite resolves its imports
# relative to its own directory, so they run as separate pytest invocations.
# No network, no data fetch, no model fit. Tests that need local-only inputs
# (saved quote CSVs, optional Outlier exports) report as skipped with the reason.
# Not covered: research/nfl_sim_integration_2026-11-06/integration, an archived
# record bound to the original /workspace paths and file hashes.
#   pip install -r requirements-test.txt && bash scripts/test_offline.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
status=0
run() {
  local dir="$1"; shift
  echo "== $dir"
  ( cd "$ROOT/$dir" && python3 -m pytest -q -p no:cacheprovider -rs "$@" ) || status=1
}
run .                                   test_*.py
run core/period_engine_v0               tests
run core/possession_engine_v0           tests
run data/gamebooks                      tests
run .                                   pregame/tests
run .                                   dashboard/tests
run .                                   pipeline/tests
run .                                   grading/tests
run data/redistributable/teams          tests
run market_calibration                  tests reviews/test_independent_false_pass.py
run research/nfl_sim_integration_2026-11-06/source_run_gate tests
run .                                   rocket_gate/tests
run .                                   phase15/tests
run .                                   snapshots/tests
run .                                   calibration/tests
run .                                   slips/tests
[ "$status" = 0 ] && echo "test_offline: all suites passed" || echo "test_offline: FAILURES above"
exit "$status"
