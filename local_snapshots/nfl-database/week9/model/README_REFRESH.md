# Week 9 model — daily refresh (run from /workspace/nfl-database/week9/model)
Each run appends a dated, timestamped section; never overwrite.
1. Odds: pull The Odds API spreads/totals (FanDuel + DraftKings) to raw/odds_<YYYYMMDD>_<HHMM>.json (key from env, never printed), then `python3 tools/slate.py`. NYG@PHI and LAR@WAS post after Sun SNF.
2. Weather: `python3 tools/weather.py` daily; final run ~2h before each kick (TNF Thu 6:15 PM; Madrid Sun 7:30 AM; 1 PM; 4 PM; SNF) + NWS hourly cross-check. Check the Bernabéu roof call.
3. Injuries/practice: ESPN injuries -> raw/espn_injuries_<date>.json; track Wed–Fri DNP/LP/FP (BAL QB, DET C, SF McCaffrey, SEA Lock, MIN Murray, HOU Montgomery, NYG Skattebo, CIN Chase).
4. Run-D tiers / leans: rerun `python3 tools/build.py` once nflverse Week 8 pbp lands (Mon/Tue), then refresh RUN_D_TIERS and LEANS.
5. Travel: confirm ATL/CIN Madrid arrival times when the teams announce them.
6. Once props post: sim_v6 exploratory medians (3 models × 100k, seeded) for the lean backs; the gate is not touched.
