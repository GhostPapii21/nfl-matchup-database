Task: Week 8 2026 NFL QB screen (all 26 starting QBs on the Sun Nov 1 / Mon Nov 2 slate; CAR@GB already played, skip). Work only in /workspace/nfl-database. Don't touch nfl-sim/, sb-grades, or repo/ source data (read-only). Never read or print secrets or env files. No posting, no bets, no messages.

Purpose: pass completions is a placeholder that tells us whether a QB throws and completes enough to support his receivers' receptions and receiving yards. Decide which QBs we should CARE about (their passing game is worth building legs around, or worth fading) and which we IGNORE (e.g., Cam Ward, whose opponent and opposing QB are better, so his side gets outplayed).

Sources: week8/slate.md/json, week8/defense/, week8/team_baselines/, week8/checklist/, week8/player_types/, week8/injuries.md, week8/depth_charts_offense.md, week8/lines/ (FD and PrizePicks props), qb_behavior_log.md, PHASE_SCRIPT.md, repo/ play-by-play, and public data (ESPN APIs, NGS, Sharp Football, team sites). No PFF. Cite sources. Never invent numbers; write n/a if unavailable. The Outlier pass completions pull, if present, is at outlier/qb_completions_2026-10-31.csv.

For each QB, produce:
- Opponent, spread/total, and a game-script read (leading or trailing, blowout risk).
- Opposing QB comparison: is his side likely to be outplayed?
- Completions and attempts per game, comp%, the line(s) if known.
- Protection: sacks taken per game, pressure rate allowed, OL injuries this week.
- Opposing defense: blitz rate, pressure rate, sacks per game, coverage shell (MOF open or closed).
- QB vs blitz and vs pressure: comp%, YPA, sacks and INTs where available.
- 3rd-down conversion rate (team and QB passing on 3rd down).
- Check-down and lock-on targets under pressure (from qb_behavior_log.md and the PBP target distribution on pressured or 3rd-and-long plays).
- Verdict: CARE-OVER (his passing volume supports receiver overs), CARE-UNDER (a blitz or pressure collapse spot, like Penix or Bryce Young), or IGNORE, with a 1-2 line reason.

Output: week8/qb_screen/QB_SCREEN.md, with a summary table at the top (QB, opp, verdict, key reason, top 2 receivers to look at), then a section per QB. Also save week8/qb_screen/qb_screen.csv.
