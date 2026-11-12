# Routine addendum (parent: UpdateRoutine)

Append to the existing ~15-min JAX@BAL live log routine prompt (do not create a second routine):

Also maintain both-team possession/drive logs on each refresh: rebuild `drive_log.csv`, `third_down_log.csv`, `red_zone_log.csv`, `team_conversion_summary.csv`, `drive_conversions.md`, plus `quarter_results.csv/md` and `period_line_grades.csv` by running the live folder’s ESPN updater (it chains the quarter/drive builder). Flag any ongoing drive and any 3rd-down NA_NO_PLAY penalty. Report source (ESPN boxscore TOP / 3rd-down) vs derived (PBP/drive) discrepancies. Keep grading stored pregame Q1/H1 period lines from r6 odds snapshots only — no new odds pulls, no bets/predictions. When the game is final, settle remaining H1 grades then stop refreshing; delete or pause this routine after the final report.

Deliver the brief delta to the user in this chat. If nothing new since last fire, say so briefly and do not spam.
