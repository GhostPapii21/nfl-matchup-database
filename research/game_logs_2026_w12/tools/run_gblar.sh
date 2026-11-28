#!/bin/bash
# W12 GB@LAR run (ESPN 401873079), 2026-11-26. Order matters. refs NFL-56, NFL-49.
set -e; cd "$(dirname "$0")"
ONLY='GB @ LAR' python3 build_logs.py   # ESPN summary + AN pre-game lines; writes GB_at_LAR.md, pbp CSV, defender log
python3 nflverse_check.py > /dev/null   # nflverse pbp cross-check (free release), air yards, PBU/INT names
python3 post.py > /dev/null             # NGS W12 snapshot, DEFENSE_PROFILES, defense_db_w12_rows.csv
python3 gblar_grade.py > /dev/null      # lock grading vs freeze_20261125T233144Z, reads graded, QB production, inactives, who got burned
python3 summary.py > /dev/null          # INDEX.md + COVERAGE_MATRIX.md
# then: WT=/tmp/nfl56-w12-gblar python3 to_repo.py
