# FIXES — overlay layer for nfl_matchups.sqlite (built 2026-10-29 ~4:56 AM ET)

- Working copy: `/workspace/nfl-database/fixes/fixes.sqlite`. This is the repo snapshot (manifest 2026-10-29 08:39 UTC) plus new `fix_*` tables. The original tables and the repo files are unchanged.
- Build: `python3 build_fixes.py`. Tests: `python3 test_fixes.py` (13 pass). The repo's own `test_export.py` also passes (2 tests).
- Sources: the public nflverse-data releases (pbp, snap_counts, weekly_rosters, injuries, stats_player_week for 2026), downloaded 2026-10-29 08:53 UTC to `src/`. They cover all 107 games (Weeks 1–7). Every fix row carries `source`, `source_fetched_at` and `built_at`. No paid feeds were used.
- Game join: `fix_game_map` maps all 107 ESPN games to nflverse game ids by week and home/away team (ESPN LAR/WSH = nflverse LA/WAS). Play join: an ESPN play_id is the game_id followed by the nflverse play_id.

## Fix 1 — credited play yards (`fix_play_credits`, `fix_credit_reconcile`, `fix_team_explosives`)
**What "credited gain" means:**
- Rush: nflverse `rushing_yards` for the original ball carrier.
- Completed pass: `receiving_yards` for the original receiver. Penalty yards are never added.
- Kneels: `credit_kind='kneel'`, kept apart from rushing.
- Sacks: the team's `yards_gained`, never credited as a player rush.
- Incompletions and interceptions: 0 credited gain.
- Plays wiped out by a penalty (nflverse `no_play`): `credit_status='nullified'`, credited yards NULL.
- Two-point tries and administrative ESPN events: not scrimmage gains.
- Fumbles: the yards up to the fumble stay with the carrier (nflverse rule). The recovery or return is not credited.
- Laterals: the original player's yards are credited; lateral yards are stored separately in `lateral_yards`.
- No match in nflverse: `credit_status='unresolved'`, yards NULL (never set to 0).

**Results:**
- 19,815 ESPN plays: 13,331 credited, 1,171 nullified, 5,306 not scrimmage plays, 7 unresolved.
- **316 plays (182 players) had stored ESPN yards that differ from the credited gain.** Most are interception returns (81), fumble-recovery plays (about 100), rushes (51) and receptions (31). On these, the ESPN `yards` field holds net or return yardage.
- **Named example:** game 401873007, play 401873007411. Stored 7 → credited **37** (Golden reception). The 15-yard taunting penalty is in `penalty_yards` and is not credited.

**Reconciliation against official per-player stats (nflverse stats_player_week):**
- Rushing (kneels included, as in official stats): **1920/1920** player-games match.
- Receiving: **1910/1920** match. The 10 that don't are listed in `fix_credit_reconcile` (rec_ok=0). They are lateral credits and plays nflverse charted differently, and are left **unresolved**.

**Derived counts, before (stored ESPN yards and ESPN play types) → after (credited):**
- Rushes of 10+ yards: 580 → 586.
- Rushes of 15+ yards: 252 → 255.
- Receptions of 20+ yards: 603 → 613.
- Run stuffs (rush for 0 or less): 1133 → 946. "Before" counted kneels and nullified rushes.

The per-team-game table `fix_team_explosives` has WR, TE and RB explosive receptions, RB rushes of 10+ and stuffs. The repo's own explosive definition is not published, so these thresholds are labeled in the `definition` column.

## Fix 2 & 3 — participation and returning-player role (`fix_participation`, `fix_player_game_usage`, `fix_player_role`)
**Participation status for each player-game:**
- `played`: snap-count row with more than 0 snaps.
- `inactive`: weekly roster status INA, or injury report Out.
- `not_on_active_roster`: roster status RES, EXE, CUT, DEV and similar.
- `active_no_snaps_recorded`: on the active roster but no snap row. This is **not** treated as a verified zero.
- `unresolved`: no evidence either way.

**Shares:** each player's denominator is the team's targets or carries **only in the games the player played**. Kneels and nullified plays are excluded. A zero is filled in only when the player is verified as playing (snaps above 0) and the play-by-play shows no target or carry for him. The current role is his last 3 played games. 1,566 players have a role row; 480 are flagged `is_returning`.

**Named examples, before (all team games as the denominator) → after:**
- **Josh Jacobs (GB):** status EXE for Weeks 1–6, then played Week 7 (52% of snaps). Before: 1.57 carries and 1.0 target per game over 7 team games. After: **11.0 carries and 7.0 targets per game, with 57.9% of carries and 16.7% of targets**, built only from his Week 7 return.
- **Savion Williams (GB):** reserve (RES) Weeks 1–5, played Weeks 6–7. Before: 1.0 target per game. After: **3.5 targets and 2.0 carries per game**, with 8.5% of targets, 9.3% of carries and 56% of snaps.
- **Jalen Coker (CAR):** played Weeks 1, 2, 3, 6 and 7; inactive Week 4 (INA). CAR has no Week 5 game in the data. Before: 6.5 targets per game (39 over 6 games). After: **7.8 targets per game (39 over 5)**, with 22.5% of targets for the season and 19.6% over the last 3 games.

## Fix 4 — QB rushing (`fix_qb_rushing_game`, `fix_qb_rushing`)
- Each QB game is split by the nflverse flags `qb_scramble` and `qb_kneel` into scrambles, designed runs and kneels (attempts and yards).
- A QB game with dropbacks but no rush is a verified 0.
- Per-QB baseline: 45 QBs with at least one game of 10+ dropbacks. Per-game averages are given for scrambles, designed runs and kneels, plus `rush_yds_ex_kneel` (mean and median) and scramble rate per dropback. This replaces the team templates.
- Example: Josh Allen, 6 games: 2.83 scrambles for 31.8 yds, 3.83 designed runs for 9.5 yds, 1.33 kneels for −1.3 yds → 41.3 rushing yds/game without kneels.

## Unresolved
- 7 plays with no nflverse match.
- 10 player-games where receiving yards don't reconcile (laterals and charting differences).
- `active_no_snaps_recorded` rows: no public source confirms whether the player had zero snaps.
- No 2026 pbp_participation release exists yet (it returned 404), so route and on-field participation for each play is still missing.
- Explosive and stuff thresholds are my definitions, because the upstream definition is not published.
- The withheld projection model was not rebuilt.

## Second pass — stale/failed sources (`fix_source_status`, checked 2026-10-29 ~4:57 AM ET)
- raiders_cb: HTTP 429 twice (Vercel Security Checkpoint bot challenge) and 403 through the fetch provider. Still fails, and is not refreshable with a simple fetch.
- espn_win_rates: HTTP 202 with an empty body, and the fetch provider timed out. Not refreshed.
- sharp_position, sharp_scheme, sharp_tendencies: reachable, HTTP 200. **But the publisher's dateModified is 2026-10-20**, so a refresh returns no newer data. The staleness is at the source. Raw HTML was saved to `src/second_pass/` and not imported.
