#!/usr/bin/env bash
# Re-run the public checkpoint tests. Does not merge, fetch paid data, or scale to 100k.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="${1:-$ROOT/inventory/verify_run}"
mkdir -p "$OUT"
python3 -m pip install --user -r requirements-verify.txt
run() {
  local name="$1"
  shift
  echo "===== $name ====="
  set +e
  "$@" >"$OUT/$name.txt" 2>&1
  local code=$?
  echo "$code" >"$OUT/$name.exit"
  echo "$name exit $code"
  tail -n 12 "$OUT/$name.txt"
}
run smoke bash "$ROOT/scripts/smoke_offline.sh"
run possession bash -c "cd '$ROOT/core/possession_engine_v0' && python3 -m pytest tests -q --tb=line"
run period bash -c "cd '$ROOT/core/period_engine_v0' && python3 -m pytest tests -q --tb=line"
run market python3 -m pytest "$ROOT/market_calibration/tests" -q --tb=line -p no:cacheprovider
run repo python3 -m pytest "$ROOT/test_export.py" "$ROOT/data/redistributable/teams/tests" "$ROOT/research/nfl_sim_integration_2026-11-06/source_run_gate/tests" -q --tb=line
run historical env PYTHONPATH="$ROOT:$ROOT/core/possession_engine_v0:$ROOT/research/nfl_sim_integration_2026-11-06" \
  python3 -m pytest "$ROOT/research/nfl_sim_integration_2026-11-06/integration/tests/historical" -q --tb=line -rs
echo "logs in $OUT"
