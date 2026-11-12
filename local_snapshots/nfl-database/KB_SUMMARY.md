# KB Summary — Blitz (Oct 29, 2026)
1. The repo DB (107 games, through MNF Oct 26) is now the primary game data; deep layers (FTN, snaps, NGS, PFR) cover Weeks 1–6 only. — /workspace/nfl-database/repo/manifest.json, README.md
2. The repo has 4 open defects (penalty yards, returning-player workload, participation, QB rushing), and its projection model is withheld. — repo/DATA_GAPS.md
3. Three current masters: PHASE_SCRIPT (projections), SKILL (bet gates), MASTER_PROMPT (data collection). — /workspace/nfl-database/PHASE_SCRIPT.md; /home/box/agent-data/workflows/nfl-betting-script/SKILL.md §20; MASTER_PROMPT.md
4. Oct 11 = Week 5 and Oct 25 = Week 7, so this weekend is Week 8. — /workspace/nfl-sim/HANDOFF_FOR_SMOKE.md; /workspace/nfl-contest/ACCURACY_AUDIT.md
5. Anytime TDs went 0/12 on TNF Oct 15 and 3/17 all-time; no ungraded TDs on main slips. — /workspace/nfl-sim/postmortem_2026-10-15.md; bets/leg_hit_rates.md
6. Receiving-yards legs hit 46/52; RB rushing legs hit 7/23 (30%). — /workspace/nfl-sim/bets/leg_hit_rates.md
7. The 55–70% sim bucket hit only 36% (5/14), so raw sim probabilities run hot; shrink them. — /workspace/nfl-sim/postmortem_oct11_early.md
8. Overs lose 9–14% flat at FanDuel closing lines, and unders are about breakeven. — /workspace/nfl-sim/backtest/hist_props/SUMMARY.md
9. Out of sample, the model lost to the market in every prop market; the only real edge was receptions (edge3 63.4% / +10.5%, Wk2–5). — backtest/hist_props/SUMMARY.md; /workspace/nfl_engine/BACKTEST_REPORT.md
10. The 500k-run engine failed on real data and is not production. — /workspace/nfl_engine/BACKTEST_REPORT.md, VERIFICATION.json
11. The pressure check wrongly cut Caleb O241.5 (308) and Maye O246.5 (321) on Oct 22. — /workspace/nfl-sim/postmortem_2026-10-22.md
12. Over-strict gates produced zero-bet days on Oct 18 and Oct 19 that cut winners (Bowers, Kittle, Purdy, Daniels). — postmortem_2026-10-18.md, postmortem_2026-10-19.md
13. User (Oct 24): don't play too safe; take the middle rung when the matchup shows an edge. — shared memory (Ghost6, Oct 24)
14. Questionable players are decided at the ~90-minute inactives check, not auto-cut (this conflicts with SKILL §5). — shared memory Oct 19; SKILL.md §5
15. Locked board: late adds go only on a separate small slip. — shared memory Oct 21
16. If the backup RB has 25%+ of carries, no starter rushing overs on safe tiers. — shared memory Oct 13
17. "Could trail" team: no RB rush over (unless 4+ targets), no check-down TE/RB yards under, no QB yards under. — SKILL.md §14
18. Bankroll is unresolved: $90 stated vs about $355.80 in the log, and $240 was staked Oct 22 (−$190). — /workspace/nfl-sim/notes/bankroll_reconcile_2026-10-22.md
19. Every user win came from boosted or single tickets; long parlays lose (Week 6 +$13.53 came from one boost). — postmortem_2026-10-18.md
20. Tipster @MrBearBets/@GameGridAppp is 3-14 verified; don't follow. — /workspace/nfl-sim/notes/tipster_summary.md
21. The v4 grader uses 14 weighted inputs (recent form 16, LB/CB matchup 12) on Week 1–6 data. — /workspace/sb-fix/data/grades/build_nfl_v4.py
22. No free 2026 man/zone or pass-rush win-rate data; the 2026 personnel CSV is actually 2025. — /workspace/nfl-sim/DATA_REGISTRY.md; blitz_db/STATUS.md
23. No postmortem exists for Week 7 (Oct 25–26), and bet-log.csv is only partly logged for Oct 25. — file search; /workspace/bet-log.csv
