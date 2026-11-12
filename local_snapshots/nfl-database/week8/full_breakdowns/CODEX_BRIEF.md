# Codex brief: full Week 8 game breakdown (2 games per run)

Work only inside /workspace/nfl-database. Don't touch nfl-sim/, sb-grades, or repo/ source data (read-only). Never read or print secrets or env files. No network posting, no bets, no messages.

Inputs, for the games named in the run prompt:
- Key players ONLY: /workspace/nfl-database/key_players.md. Ignore everyone else except as defenders or context.
- Outlier pull: /workspace/nfl-database/outlier/key_<AWAY>_<HOME>.csv (FD line/odds, L5/L10/2026/2025/H2H, alt rungs, defense-vs-position, matchup grade)
- Database: PHASE_SCRIPT.md (the model, incl. amendments), week8/defense/, week8/team_baselines/, week8/player_types/, week8/film/, week8/checklist/, week8/rosters/, week8/injuries.md, week8/depth_charts_offense.md, week8/lines/, week8/rematches/, defender_ledger.csv, qb_behavior_log.md, coverage_vs_type_log.md, repo/ play-by-play.
- Fill gaps from public sources (ESPN APIs, NGS, Sharp Football, team sites). No PFF. Cite every number's source. Never invent a number; write "n/a" if unavailable.

Write one file per game: week8/full_breakdowns/<AWAY>_<HOME>.md with these sections:

1. Game context: spread/total, likely script and blowout risk, weather, travel/rest, division/conference, coaching tendencies (OC/DC/HC), 3rd-down and red-zone rates.
2. Defensive coverage profile for EACH defense: MOF closed vs open rate (single-high vs two-high), main coverages (Cover 1/3/2/4/man%), blitz rate, pressure rate, sacks; per game allowed: pass yds, rush yds, receptions, explosive plays (20+ pass, 10+ rush); allowed by position (WR1/WR2/slot/TE/RB receiving, RB rushing).
3. Personnel matchups: each key WR/TE vs the CBs/safeties/LBs he'll most likely face (outside vs slot alignment), plus each defender's ledger record (catches and yards allowed per game, explosives). Note separation (NGS avg separation, cushion), contested-catch/physicality, YAC.
4. QB profile, each QB: vs blitz and vs pressure (comp%, YPA, sacks, INTs, time to throw), who he locks onto and checks down to under pressure (qb_behavior_log.md), and how this defense's blitz and pressure rates fit him. Flag Penix/Bryce Young-type collapse risk.
5. Opportunity per key player: projected targets or carries (team volume x share x script), catch rate (receptions/targets), YPT/YPC, snap %, red-zone share. Apply the opportunity gate BEFORE any matchup boost.
6. Outlier correlation: for each key player and market, the line, L5/L10/season/H2H, alt-rung hit rates, defense-vs-position, and grade. Where Outlier agrees or disagrees with our projection, say why.
7. Projections: low / mid / high for each key player's markets. Then the target props: side, suggested rung (modest middle rung), confidence, the reason, and correlated pairs and pairs to avoid. Questionable players get a low rung or a fade, flagged for the 90-minute inactives check. Passing yards only on a clear over (or an under on a QB who struggles vs the blitz facing a heavy-blitz defense). Anytime TDs on a separate list.

End each file with a 10-line summary block. Report the file paths when done.
