#!/bin/bash
cd /workspace/nfl-database/backtests/v6_brainstorm_proedge
while pgrep -f "python3 reads.py" >/dev/null; do sleep 30; done
[ -f QUOTA_STOP ] && exit 0
python3 reads.py >> reads.log 2>&1   # resume pass for any failed 2026 games
[ -f QUOTA_STOP ] && exit 0
python3 reads25.py >> reads25.log 2>&1
