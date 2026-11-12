# Upstream patch spec (for the pipeline on the user's Mac)
Apply these so the fixes survive the 9:00 AM daily sync. Reference implementation: /workspace/nfl-database/fixes/build_fixes.py. Tests: test_fixes.py.

1. **Add nflverse ingest for all weeks:** pbp, snap_counts, weekly_rosters, injuries and stats_player_week from the nflverse-data releases. Store a `fix_game_map` (ESPN event ↔ nflverse game_id, matched on week + home/away team, with LAR→LA and WSH→WAS). Join plays on the ESPN play_id = event_id followed by the nflverse play_id.
2. **Credited yardage:** never take player yardage from the ESPN `plays.yards` field or from the play text.
   - Use nflverse rushing_yards and receiving_yards.
   - no_play → NULL.
   - Kneels kept separate.
   - Sacks go to the team.
   - Laterals and fumbles follow the nflverse credit rules.
   - Unmatched plays → unresolved (NULL).
   - Recompute explosive and stuff counts from the credited yards. Publish the threshold definition.
   - Add a check that, for every player-game, the sum of credited yards equals the official stat. Log the exceptions.
3. **Participation table:** played / inactive / not_on_active_roster / active_no_snaps_recorded / unresolved, from snaps, weekly roster status and the injury report. No player-stat row must never mean 0.
4. **Baseline shares:** use only games the player played as the denominator. Add a current-role window (last 3 played games) and an `is_returning` flag. Weight the current role over the season numbers for returning players such as Jacobs and Savion Williams.
5. **QB rushing:** a per-QB baseline from qb_scramble, designed runs and qb_kneel. Exclude kneels from the projection. Remove the team designed-run templates.
6. **Regression tests to port:**
   - Golden play 401873007411 credits 37.
   - Jacobs: 1 game played, 6 games not on the roster, 11 carries per game.
   - Savion: 2 games played, 3.5 targets per game.
   - Coker: 5 games played, Week 4 inactive, 7.8 targets per game.
   - QB rushing splits add up.
   - All rushing reconciles to official stats.
7. **Sources:** mark the Sharp pages "source last modified 2026-10-20" rather than stale-fetch. raiders_cb needs a browser-capable fetch or should be dropped (bot challenge). The ESPN win-rate story returns 202 to scripted clients.
