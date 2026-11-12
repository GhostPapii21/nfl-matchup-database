# Drive-killer offensive penalties, 2026 Weeks 1-8 (BetGuru, for Blitz to merge)
Source: public ESPN summary API (drives.previous[].plays[].text), 119 final games pulled 2026-11-01 ~8:50 PM ET. Week 8 PHI@WSH and CHI@SEA were NOT final yet, so they aren't included. Raw JSON is in raw/. Rebuild with: python3 fetch.py && python3 build.py
drive_killers_2026.csv: one row per ACCEPTED penalty on the drive's offense (penalty team = drive team) on a drive whose ESPN result was PUNT, INT, FUMBLE, DOWNS, MISSED FG or BLOCKED punt/FG with no score. Return-TD results are counted as killers.
Excluded: declined penalties (no yardage in the text), offsetting fouls, kick/punt/FG/PAT plays and between-downs fouls. ten_plus means 10+ yards; no_play means the snap was wiped out. raw_text is ESPN's play text.
Caveats: penalty team is matched on ESPN abbreviations. Player names come straight from ESPN. ESPN can occasionally mislabel a drive result. This file does not prove the penalty caused the drive to stall.
Validation: see the v2 section below. The v1 result was invalid because of an LA/LAR team-abbreviation bug.

## penalties_2026.csv (every flag, built by build_all.py)
Columns: game_id, week, team, opp, home_away, side, status, type (normalized), raw_type, yards, quarter, clock, player, down, distance, yardline (yards to the end zone), drive_id, drive_outcome, auto_first_down, drive_killer, raw_text. 1,918 flags: 1,264 no-play, 445 accepted, 209 declined.
Side is special teams for any kick, punt or FG play, offense when the penalized team had the ball on the drive, and defense otherwise. auto_first_down is a rules-based guess: an accepted defensive DPI, defensive holding, illegal contact, roughing or face mask.
drive_killers_2026.csv is now built from the rows of penalties_2026.csv where drive_killer is true: 418 rows, with offensive pre-snap flags included even on kick plays.
Coverage: 119 final games. By week: 16, 16, 16, 16, 15, 14, 14, 12. Weeks 5-8 are below 16 because of byes. GAP: Week 8 PHI@WSH and CHI@SEA weren't final when this was pulled. Rerun fetch.py and both build scripts to add them, plus MNF.
Known issues:
- Offsetting fouls: FIXED, 44 found. ESPN abbreviation aliases: FIXED. ESPN uses LA in play text but LAR as the drive team. This had been mislabeling every Rams offensive flag as a defensive one.
- Flags on plays outside the drives array (pre-snap between drives, or on PATs) can be missed.
- Summed over all team-games, accepted plus no-play counts differ from the box-score 'Penalties' totals by 294 after the fixes, down from 397. Use the box totals for team counts and this file for type, player and timing.

## Validation v2 (validate.py)
Unit: team-game, n=238. Offensive penalty means side=offense with status accepted or no-play, so pre-snap No Play flags are included. Each outcome is that game's value minus the team's Weeks 1-8 average. Partial r controls for final margin.
Margin alone: r=-0.14 with completions and -0.31 with attempts. Game script is the much bigger driver.
(a) Q1 offensive penalties vs. completions: r=+0.02, partial +0.04. Buckets: 0 penalties -0.05 (n=122), 1 penalty -0.05 (n=72), 2+ penalties +0.23 (n=44).
(b) Whole-game offensive penalties vs. completions: r=+0.07, partial +0.08. Buckets: 0-2 penalties -0.42 (n=88), 3-4 -0.03 (n=86), 5-6 +0.75 (n=48), 7+ +0.21 (n=16).
    Whole-game offensive penalties vs. attempts: r=+0.05, partial +0.08. Buckets: 0-2 -0.46, 3-4 -0.06, 5-6 +1.29, 7+ -1.03.
(c) Drive killers vs. offensive plays: r=-0.09, partial -0.07. Buckets: 0 +0.31 (n=63), 1 -0.24 (n=62), 2 +1.54 (n=41), 3+ -0.94 (n=72).
    Drive killers vs. attempts: r=+0.08, partial +0.04.
Conclusion: none of these correlations is meaningfully different from zero. With n=238, |r| needs to be about 0.13 to reach p<.05. Penalties don't predict lower completions. If anything, more pass plays create more flags. LAR Week 8 (2 Q1 offensive flags, 4 total, 3 drive killers, 17 completions, -8.75 vs. average, won by 15) is better explained by the 15-point win (game script) than by penalties.
Sim use: model penalties as drive-level kill risk and field-position noise, not as a direct cut to completions.
