# Replacement sources audit — 2026-11-01 (pulled ~11:05 PM ET)
Recommends only. Source list, gates and pipeline are unchanged. Raw pulls are in /tmp on the box.
Reference: ESPN scoreboard says Week 8 has 14 games (NO/NYG/SF/HOU on bye). SNF PHI@WSH was not final at pull time, and MNF CHI@SEA is still to play. So **Week 8 cannot be complete anywhere until Tue Nov 3**.

## Key finding: nflverse covers most categories (public GitHub releases, CC-BY, no key needed)
| File | Weeks present (games) | Wk1-8 complete | Spot-check |
|---|---|---|---|
| play_by_play_2026.parquet | 1-7 complete (16/16/16/16/15/14/14); Wk8 12 of 14 games | Wk1-7 yes | Base truth. KC@DEN 24-28 and LV@NYJ 38-33 match ESPN finals |
| pfr_advstats/advstats_week_pass_2026.csv (pressure, blitz, hurries, hits, sacks) | 1-7; Wk8 TNF only (2 rows) | Wk1-7 yes | Wk7 sacks match pbp: Brissett 3/3, Love 1/1, G.Smith 2/2 |
| nextgen_stats/ngs_passing.csv.gz (time to throw etc.) | 0-7; Wk8 TNF only (GB, CAR) | Wk1-7 yes | Normal 1-week lag (NGS posts Tue/Wed) |
| ftn_charting_2026.csv (n_blitzers, n_pass_rushers, play action, screen, RPO, motion, out of pocket, drops, contested) | 1-7 complete; Wk8 1 game | Wk1-7 yes | Wk1-7 game counts match pbp exactly |
| snap_counts_2026.csv | 1-7 complete; Wk8 1 game | Wk1-7 yes | Wk1-7 game counts match pbp |
| injuries_2026.csv (official report plus practice status) | 1-8 (Wk8 28 teams = 32 minus 4 byes) | YES | All Week 8 teams present |
| depth_charts_2026.csv | Daily snapshots, latest dt 2026-11-01T14:14Z (9:14 AM ET) | YES (current) | — |
| pbp_participation_2026 (coverage type, man/zone, time to throw, was_pressure) | **404: not published for 2026** | NO | We have a local copy from an earlier BetGuru pull, but it is corrupt or unreadable |

## Per category
| Category | Source | URL | Latest week | Wk1-8 complete | Spot-check | Access | Recommendation |
|---|---|---|---|---|---|---|---|
| Coverage (man/zone/single-high) | Sumer Sports team defense | https://sumersports.com/teams/defensive/ | Season 2026, 32 teams with manCoveragePct and zoneCoveragePct. Page dates run to 2026-11-02, but the through-week isn't labeled (one updatedAt is 2026-09-28) | Unverified | Not done: I couldn't parse the values per team | Public, free | Use as the 2nd source for Sharp. Ask a browser agent to confirm the through-week label |
| Coverage | nflverse participation | releases/pbp_participation | none for 2026 | No | — | Public | **Gap**: no free public per-play coverage feed for 2026 |
| Pressure/blitz/TTT | nflverse PFR advstats + NGS + FTN | github.com/nflverse/nflverse-data/releases | Wk7 complete (Wk8 TNF only) | 1-7 | Sacks agree with pbp 3/3 | Public | **Adopt.** Replaces PFF for QB pressure. Gives qb_pressure.json what it needs |
| OL/DL win rates | ESPN PRWR/PBWR/RSWR/RBWR leaderboard | https://www.espn.com/nfl/story/_/id/41246539/nfl-pass-rush-run-stop-blocking-win-rate-leaderboard | Page has "Week 8" mentions and dates to 2026-11-02 | Season-to-date (cumulative) | Not cross-checked | Public | Keep. It replaces the StatRankings OL page (which shows 2025) |
| OL/DL grades | PFF only | — | — | — | — | Paywall | **Gap** (no free equivalent for grades). Use ESPN win rates plus PFR pressure |
| WR vs CB matchups | none free and current | — | — | — | — | — | **Gap.** Build our own from pbp targets plus depth charts. Coverage-shadow data needs participation or PFF |
| Injuries/practice | ESPN injuries API + nflverse injuries | site.api.espn.com/apis/site/v2/sports/football/nfl/injuries (200) | Current / Wk8 | Yes | 28 teams in Wk8 | Public | **Adopt** (replaces the PFF injury tool, which shows "WEEK 3") |
| News | ESPN news API | site.api.espn.com/apis/site/v2/sports/football/nfl/news | Latest article 2026-11-02 03:56Z (10:56 PM ET Nov 1) | Live | Headline matches the KC@DEN final | Public | **Adopt** (replaces the Oct 24 feed). Rotowire's injury page also responds (200) |
| Depth/snaps | nflverse depth_charts + snap_counts | as above | Depth as of Nov 1; snaps through Wk7 | Yes / 1-7 | Game counts match | Public | **Adopt**. FantasyPros snap page is stale (2025 stamps) |
| Film/highlights | NFL YouTube channel | https://www.youtube.com/@NFL/videos | Week 8 titles present (28 mentions) | Yes (highlights) | — | Public | **Adopt** to restart film past Wk6. All-22 is NFL+ Premium only, so **gap** for All-22 |
| Props/lines | ESPN scoreboard odds (game lines) | site.api.espn.com scoreboard | Current | Game lines only | — | Public | Player props: **gap** in free public feeds. Keep DK/FD lines via our existing approved pull. Outlier stays caution-only |
| Weather | NWS api.weather.gov (200) + Open-Meteo | already approved | Live | — | — | Public | No change |

Not reachable: Pro-Football-Reference returns 403 to scripted fetches. I respected that and didn't retry (the nflverse advstats file mirrors PFR's numbers). PropsMadness, Fantasy Points and NFL Football Ops have no replacement.

## Gaps with no current free source
1. Per-play coverage scheme (man/zone/single-high). nflverse participation isn't published for 2026. Sumer gives team-level only, and its through-week is unconfirmed.
2. WR vs CB shadow matchups.
3. OL/DL player grades. ESPN win rates are the only free proxy.
4. Player prop lines in a public feed.
5. All-22 film.

## Recommended common starting week
**Weeks 1-7, validated now. Add Week 8 Wednesday Nov 4** (after MNF CHI@SEA, and after nflverse/NGS/FTN/PFR post Week 8 overnight Tue).
Reasoning: Week 7 is the latest week that every category with a public source covers completely (pbp, pressure/blitz, NGS TTT, FTN, snaps all have 14/14 Wk7 games; injuries and depth are current). Week 8 is partial everywhere (pbp 12/14, others TNF only). Coverage scheme has no Week 1-8 validatable source at all. Until one exists, treat coverage as Sumer team-level plus Sharp, both caution-flagged.
