#!/bin/bash
# runs after reads25 ends (complete or QUOTA_STOP): lock commit, then grade commit
cd /workspace/nfl-database/backtests/v6_brainstorm_proedge
while pgrep -f "python3 reads25.py" >/dev/null || pgrep -f chain.sh >/dev/null; do sleep 60; done
G="git -c user.name=Blitz -c user.email=blitz@local"
python3 gate25.py > gate25.out 2>&1 || exit 1
cd ../..; git add backtests/v6_brainstorm_proedge/{reads25,locked_picks_2025.csv,gate25.out,usage_log_2025.jsonl,reads25.log} backtests/v6_brainstorm_proedge/QUOTA_STOP 2>/dev/null
$G commit -qm "v6 LOCK 2025: $(ls backtests/v6_brainstorm_proedge/reads25/*.json|wc -l) Grok reads + locked_picks_2025.csv (pre-grade)"
cd backtests/v6_brainstorm_proedge; python3 grade25.py > grade25.out 2>&1 || exit 1
cd ../..; git add backtests/v6_brainstorm_proedge/{graded_*2025*,results_2025.md,grade25.out}; $G commit -qm "v6 GRADE 2025 bucket (c) HINDSIGHT RISK (after lock)"
git log --oneline -2 > backtests/v6_brainstorm_proedge/finish25.done
