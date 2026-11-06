#!/usr/bin/env bash
# Bounded offline smoke for the portable possession-engine subset.
# Does not init a git repository, pull data, or run a projection.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/inventory"
cd "$ROOT/core/possession_engine_v0"
python3 -m pytest tests/test_suite_fix.py tests/test_roles_unify.py -q --tb=line \
  | tee "$ROOT/inventory/smoke_offline.log"
exit "${PIPESTATUS[0]}"
