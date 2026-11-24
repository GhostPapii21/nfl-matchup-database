#!/bin/bash
# MNF late run (CIN@WSH, ESPN 401873078), 2026-11-24. Order matters. refs NFL-56, NFL-49.
set -e; cd "$(dirname "$0")"
ONLY='CIN @ WSH' python3 build_logs.py      # ESPN summary + AN pre-game lines + Open-Meteo; merges into data/_all_games.json
python3 video_evidence.py > /dev/null         # caption mentions for all mapped official videos (video/map.json)
python3 late_video_cinwsh.py                  # hand-checked source=video rows + late notes
python3 nflverse_check.py > /dev/null         # nflverse pbp cross-check (free release)
python3 post.py > /dev/null                   # NGS snapshot, SLIP_LEG_RESULTS, DEFENSE_PROFILES, defense_db_w11_rows.csv
python3 summary.py > /dev/null                # INDEX.md + COVERAGE_MATRIX.md
