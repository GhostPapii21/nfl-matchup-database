# FanDuel alt ladders, 2026 NFL Weeks 8-9 (historical, T-90 min)

Approved by Rico in Betting Hub, 2026-11-13 ~11:14 AM ET (spec via Ghost6). Research data only. Refs NFL-75.

- Source: The Odds API `/v4/historical/sports/americanfootball_nfl/events/{id}/odds`, `bookmakers=fanduel`,
  `markets=player_rush_yds_alternate,player_reception_yds_alternate`, `date` = kickoff - 90 min. Pinnacle skipped (no alts).
- Event ids: one historical events call (1 credit) at 2026-10-29T18:00Z -> `events_wk8_9.json` (29 games).
- Pulled 26 games (all Weeks 8-9 except DAL@IND, JAX@BAL, BUF@MIN, already in PR #41).
- Measured cost: **20 credits per event** (first event measured before continuing). Total this job: **521 credits**
  (1 events + 26 x 20). Remaining after: **1,093** (start 1,614). Stop rule: next call would drop remaining below 950 (never hit).
- Every call is in `pull_log.jsonl` (time UTC, cost, remaining, status, snapshot timestamp). API key redacted everywhere.
- Coverage: all 26 returned 200 with both markets; FanDuel over rungs only (no unders).
