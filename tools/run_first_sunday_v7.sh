#!/usr/bin/env bash
# First-game SIM V7 independent test and full acceptance gate (no GitHub Actions).
set -Eeuo pipefail
cd "$(dirname "$0")/.."
GAME="${GAME:-2026_12_NO_CIN}"
AS_OF="${AS_OF:-2026-11-28T18:00:00+00:00}"
OUT="${OUT:-runs/sim_v7_first_game_acceptance}"
mkdir -p "$OUT"
echo "REPO=$(pwd) GAME=$GAME AS_OF=$AS_OF OUT=$OUT"
echo "HEAD=$(git rev-parse HEAD)"
python -m pytest -q engines/sim_v7/tests sunday/tests 2>&1 | tee "$OUT/pytest.log"
python -m engines.sim_v7.cli smoke --game "$GAME" 2>&1 | tee "$OUT/smoke.log"
SUNDAY_SIM_V7_N=2000 python -m sunday game --game "$GAME" --as-of "$AS_OF" --out "$OUT/stack_2000" 2>&1 | tee "$OUT/stack_2000.log"
python - "$OUT/stack_2000/manifest.json" <<'PY'
import json, sys
from pathlib import Path
p=Path(sys.argv[1])
assert p.is_file(), f"Missing acceptance manifest: {p}"
d=json.loads(p.read_text())
print("FIRST-GAME COMPONENT STATUS:")
for c in d.get("components", []):
    print(f"{c.get('id')}: {c.get('status')} required_for_v7={c.get('required_for_v7', True)} {c.get('reason','')}")
assert d.get("kickoff",{}).get("verification") == "VERIFIED", "official kickoff unverified"
assert d.get("projection_ready") is False, "incorrect readiness promotion"
r=next((x for x in d.get("components",[]) if x.get("id")=="sim_v7"), None)
assert r and r.get("status") == "EXECUTED" and r.get("trials") == 18000, "nine 2000-trial V7 cells did not execute"
assert d.get("result") == "PASS", f"Sunday acceptance still {d.get('result')}; review component reasons above"
PY
python -m engines.sim_v7.cli run --game "$GAME" --n 100000 --out "$OUT/full_100k" 2>&1 | tee "$OUT/full_100k.log"
python - "$OUT/full_100k/$GAME.sim_v7.json" <<'PY'
import json,sys
from pathlib import Path
p=Path(sys.argv[1])
assert p.is_file(),f"Missing full 100K artifact: {p}"
d=json.loads(p.read_text())
assert d.get("meta",{}).get("status") == "RESEARCH_ONLY_NOT_PROJECTION_READY"
rows=[r for r in d.get("records",[]) if r.get("market")=="total_points"]
assert len(rows)==9 and all(r.get("trial_count")==100000 and r.get("execution_status")=="OK" for r in rows), "Missing 9x100K accepted cells"
res=[r for r in d.get("residual_records",[]) if r.get("market")=="total_points"]
assert len(res)==3 and all(r.get("trial_count")==100000 and r.get("execution_status")=="OK" for r in res), "Missing residual cells"
print("PASS: 9 primary + 3 residual cells, each 100,000 accepted trials")
PY
echo "PASS: first-game tests, Sunday acceptance, full 100K simulation"
