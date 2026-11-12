# Week 8 Sunday baseline (built Oct 29 2026)
- slate.json/md — ESPN scoreboard 20261101 (12 games). TNF CAR@GB noted separately.
- injuries.json/md — ESPN injuries API; designation + source ts (UTC). Wed practice only where news comment states it; official Wed/Thu practice table = GAP. Thursday practice not yet reported at build time.
- team_baselines/<TEAM>.md (24 teams) — W1–6 scoring plays, big plays, PBP direction concepts, RZ usage, overlay usage shares (season vs L3, snap% L3), 20+ plays allowed. Regenerate: python3 week8/build_baselines.py (from /workspace/nfl-database).
- GAPS: no video/film; personnel groupings, coverage shells, defenders beaten in coverage not in sources; recap = ESPN headline blurb only; DAL/DET/LAR roof is retractable/fixed — ESPN only gives indoor flag; overlay usage runs through latest synced week (W7), not cut at W6.
