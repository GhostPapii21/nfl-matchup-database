#!/bin/bash
cd /workspace/nfl-database/week8/tnf
for i in $(seq 1 25); do
  out=$(python3 live_full.py 2>&1 | tail -1); echo "$(date +%H:%M) $out"
  if [ "$out" = "COMPLETED" ]; then python3 live_full.py --final >/dev/null && echo FINAL_DONE; exit 0; fi
  sleep 720
done
