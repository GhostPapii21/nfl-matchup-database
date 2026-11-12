#!/bin/bash
# resumable: reads/*.json already present are skipped
cd "$(dirname "$0")"
R=/workspace/nfl-database
commit(){ for i in 1 2 3 4 5; do (cd $R && git add backtests/v7_openai/v5_1/codex_full && git -c user.name=Blitz -c user.email=blitz@local commit -qm "$1" ) && return; sleep 7; done; }
python3 reads_codex.py >> reads.log 2>&1
echo RUN_DONE >> reads.log
python3 post.py > post.log 2>&1 || echo POST_FAILED >> post.log
commit "v5_1 codex_full: reads locked (sha256) + graded results.md"
