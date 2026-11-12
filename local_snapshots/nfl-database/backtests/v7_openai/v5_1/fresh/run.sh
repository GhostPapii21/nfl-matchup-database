#!/bin/bash
cd "$(dirname "$0")"
python3 reads_v51.py > reads.log 2>&1 &
P=$!
R=/workspace/nfl-database
commit(){ for i in 1 2 3 4 5; do (cd $R && git add backtests/v7_openai/v5_1/fresh && git -c user.name=Blitz -c user.email=blitz@local commit -qm "$1" ) && return; sleep 7; done; }
while kill -0 $P 2>/dev/null; do sleep 240; commit "v5_1 fresh reads WIP (auto)"; done
commit "v5_1 fresh reads: run finished (auto)"; echo RUN_DONE >> reads.log
