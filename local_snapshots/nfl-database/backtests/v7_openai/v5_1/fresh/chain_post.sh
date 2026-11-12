#!/bin/bash
# waits for RUN_DONE in reads.log (written by run.sh after reads_v51.py exits, incl. cost-cap/quota stop), then final grade + commit
cd "$(dirname "$0")"
R=/workspace/nfl-database
until grep -q RUN_DONE reads.log 2>/dev/null; do sleep 120; done
python3 post.py > post.log 2>&1 || echo POST_FAILED >> post.log
for i in 1 2 3 4 5; do (cd $R && git add backtests/v7_openai/v5_1/fresh && git -c user.name=Blitz -c user.email=blitz@local commit -qm "v5_1 fresh: reads locked (sha256) + FINAL graded results.md") && break; sleep 7; done
