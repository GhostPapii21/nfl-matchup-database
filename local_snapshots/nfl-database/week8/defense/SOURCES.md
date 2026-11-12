# Sources (Week 8 defense build, retrieved 2026-10-29 ~05:08–05:10 ET)
- ESPN scoreboard API: https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20261101 (12 Sunday games incl. SNF PHI@WSH) — raw espn_scoreboard_20261101.json
- Sharp Football Analysis (page dateModified 2026-10-20 12:18 ET; cross-check: Sharp WR YPT matches our pbp WR YPT within 0.1 for SEA/DAL/WAS/LA):
  - https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-stats-by-position/
  - https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/
  - https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/
- Sharp advanced box scores (game pressure-rate-allowed, EPA/play): repo external_observations source sharp_advanced, source_updated max 2026-10-27 09:34 ET (last fetch 2026-10-28 08:08 ET). Defensive pressure rate = PROXY (mean of opponents' pressure-allowed in games vs that defense).
- ESPN win rates (team PRWR/PBWR): repo espn_win_rates, article https://www.espn.com/nfl/story/_/id/49742016/... updated 2026-10-20 09:38 ET — STALE (thru wk6).
- NGS: nflverse mirror of Next Gen Stats https://github.com/nflverse/nflverse-data/releases/download/nextgen_stats/ngs_{receiving,rushing,passing}.parquet (season rows week=0, data thru wk7). Direct nextgenstats.nfl.com API (appapi.ngs.nfl.com) unreachable from box = GAP for direct pull.
- FTN charting (blitzers): https://github.com/nflverse/nflverse-data/releases/download/ftn_charting/ftn_charting_2026.parquet (thru wk7).
- nflverse pbp/rosters/injuries/snaps (fixes/src, fetched 2026-10-29 04:53 ET), weeks 1–7. Position allowances computed from pbp with weekly-roster positions; outside/middle split = pass_location PROXY (left/right vs middle), not true slot alignment.
- Overlay fixes.sqlite: fix_team_explosives (explosives allowed, defense = opponent of posteam), fix_player_role (L3 shares/snaps), fix_qb_rushing.
- Power rankings: FantasyPros ECR via https://leaguelogs.com/rankings/week-8/ppr/flex (consensus updated 2026-10-29 00:11 EDT) → power_rankings_flex_ppr.csv; FantasyPros TE (Oct 28–29) top: Bowers, McBride, Kraft, Goedert, Loveland.
## Gaps
- PFF grades / coverage grades, true slot-alignment allowances, team pressure counts from PFF: paid → not estimated.
- ESPN win rates stale (wk6). Sharp position/scheme/tendency pages dated Oct 20.
- 10G: no numeric thresholds supplied; no stakes evidence collected → no class assigned.
- Raiders Rundown CB page FETCH_ERROR in repo; individual CB matchups not built.
- Week 8 injury rows are early-week (practice) only; another worker owns injuries.
- NGS route/carry chart images not re-read (counts only).
