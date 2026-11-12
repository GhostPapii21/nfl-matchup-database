# Free-source discovery — NFL data gaps (2026-11-01)
**STATUS: Pending Ghost6 vetting, NOT in the official source map.**
Tool: Firecrawl CLI (npx firecrawl-cli) search/map/scrape, about 36 calls. Parallel skills were skipped because there is no PARALLEL key on the box.
Pulled 2026-11-01 ~2:00–2:25 AM ET. Raw scrapes are in /workspace/.firecrawl/*.md.
Trusted cross-check sources used: nflverse pbp 2026 (nfl-database/fixes/src/play_by_play_2026.parquet, through Wk7), nflverse NGS receiving parquet (week8/player_types/src), and the PFR adv-defense cache /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (Oct 29). All read only.

## Summary table
| URL | Gap | Freshness | Free/no login | Sample number | Cross-check | Verdict |
|---|---|---|---|---|---|---|
| sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/ | 1 man/zone + MOF closed/open | Updated Oct 27 (thru Wk7) | Yes, full 32 teams | TEN man 16.5 / zone 77.2 / MOF-closed 45.6 / open 51.2 | vs StatRankings zone: SEA 90.0 vs 82.3, PIT 82.2 vs 80.2 (same direction, different charting); no pbp equivalent (FTN fields not in 2026 pbp cache) | RECOMMEND |
| statrankings.com/nfl/advanced/teams/coverage/zone-coverage-rate (+ /man-coverage-rate, /single-high-rate) | 1 | "through games played Oct 30, 2026" | Partial: table shows top 5 free; prose lists ranks ~1–25 | SEA zone 82.3%; CLE single-high 69.9% | CLE single-high 69.9 vs Sharp CLE MOF-closed 72.6 (consistent); SEA vs Sharp above | MAYBE (second source/tiebreak) |
| statrankings.com/nfl/advanced/players/cb/yards-allowed, /yards-per-target-allowed (+ ~15 CB sub-metrics incl. man/zone rate, slot/left/right targets) | 2 per-defender | Oct 30, 2026 | Partial: only top 5 rows free, the rest paywalled (statrankings+) | K. Fulton (KC) 18 yds allowed; T. McDuffie YPT 1.6 | PFR cache: Fulton 13 yds (3 G), McDuffie 2.0 YPT; Nick Cross SR 4 yds vs PFR 57 yds. **Mismatch**: different charting provider and PFR cache is staler | MAYBE (can't get a full defender list free) |
| statrankings.com/nfl/coverage/team/{abbr} | 1/2 by shell & alignment | n/a | Rendered empty (JS/paywalled cells) | none | n/a | REJECT |
| sharpfootballanalysis.com/stats-nfl/nfl-coverage-stats-by-position/ | 2 (team-level proxy: YPT by WR/TE/RB, outside vs slot) | Oct 27 | Yes | CIN YPT allowed slot 11.3, outside 5.7, TE 9.4 | No direct trusted equivalent; could rebuild a WR/TE/RB split from pbp + rosters (not done) | MAYBE (team, not per-defender) |
| sharpfootballanalysis.com/stats-nfl/nfl-defensive-line-stats/ | 3 real pressure rate | Oct 27 | Yes, 32 teams | TEN pressure 29.8%, no-blitz 27.9%; MIN 47.6% | vs StatRankings defense pressure: MIN 47.6 vs 39.7 (both rank MIN #1, but scales differ by ~8 pts); PFR cache is per-player Prss only, so no team total check | RECOMMEND (pick one provider and stay on it) |
| statrankings.com/nfl/advanced/teams/defense/pressure-rate | 3 | Oct 30 | Partial (top 5 table + prose) | MIN 39.7%, KC 37.3%, LV 35.9% | see above | MAYBE |
| espn.com/nfl/story/_/id/49742016/2026-win-rates-team-player-rankings-pass-rush-run-stop-blocking | 3 (PRWR, NGS tracking based) | "Through Week 7, Oct 27 10 AM ET" | Yes | Team table not captured by scrape (embedded); no number | not possible | MAYBE (try the browser before using it) |
| nextgenstats.nfl.com/stats/receiving | 4 separation/cushion | Season to date (thru Wk7) | Yes | Higgins SEP 2.4, CUSH 5.5, 33-50-571 | nflverse NGS parquet: Higgins sep 2.433, cushion 5.537, 50 tgt 571 yds ✅; pbp 50 tgt/33 rec/571 ✅ | RECOMMEND |
| nextgenstats.nfl.com/stats/passing | 4 time to throw | thru Wk7 | Yes | Burrow TT 2.64, 219 att, 1653 yds | pbp counts consistent (not separately recomputed); nflverse NGS passing not cached, so TT can't be cross-checked | RECOMMEND |
| sumersports.com/players/wide-receiver/ , /tight-end/ , /running-back/ | 5 routes run, TPRR, YPRR | "Updated 10-31-2026 4:17 AM ET" | Yes (about 120–180 rows per page; coverage filters are SumerPass only) | Higgins 202 routes, .25 TPRR, 2.83 YPRR; Bowers 198 routes .26 TPRR; Bijan 131 routes | Higgins 33 rec/571 yds = pbp ✅ (routes have no trusted equivalent) | RECOMMEND |
| statrankings.com/nfl/advanced/players/usage/targets-per-route-run | 5 | Oct 30 | Partial (top 5) | Kamara 0.38 TPRR | not possible | MAYBE |
| sumersports.com/teams/defensive/ | context (EPA, rush-man %) | 10-30-2026 | Yes | MIN EPA/play -0.21 | not checked | MAYBE |
| rotowire.com/football/te-route-data.php | 5 route % for TEs | 2026 | Top 10 only, the rest is subscriber-only | McBride route% ~62 (column parse unclear) | n/a | REJECT |
| ftnfantasy.com/nfl/stats | 1/3/5 | n/a | No: "Sign Up for FTN to Access" on every coverage/pressure tab | none | n/a | REJECT |
| Not scraped (credit budget): rbsdm.com, playerprofiler.com, nfeloapp, PropsMadness, Fantasy Points, sportsdataio | — | — | — | — | — | UNTESTED |

## Notes per candidate
- **Sharp coverage schemes**: the best free single table for gap 1. It covers all 32 teams, with man, zone, MOF-closed and MOF-open on one page, updated weekly (Monday or Tuesday). Man + zone doesn't add up to 100 (e.g. LAC 10.6+58.0), probably because of uncharted or "other" snaps. Flag LAC.
- **StatRankings**: has deep per-CB metrics (the exact gap 2 we need: yards allowed, YPT, catch rate, man/zone rate, left/right/slot targets) and is fresher (Oct 30). But logged-out it shows only the top 5 rows of each table. A full list would need statrankings+ (paid), which the rules don't allow. Its numbers don't line up with the PFR cache (Cross 4 vs 57 yds), so they shouldn't be mixed with PFR in one ledger. The page also carries a Polymarket promo; ignored.
- **Pressure**: Sharp and StatRankings rank teams similarly but on different scales. Use Sharp as primary (full table, free) and log the provider each time.
- **ESPN win rates**: an official tracking-based PRWR. The scrape got the article text and date but not the team table. Needs a browser read or a different parse.
- **NGS**: the public pages match the nflverse NGS parquet exactly, so they're safe. The parquet already on the box is enough for separation; the passing page adds TT.
- **SumerSports player pages**: free routes run, TPRR and YPRR for WR/TE/RB, and the receiving totals match pbp. Coverage-split filters need SumerPass (not used).
- **FTN / RotoWire**: paywalled, rejected. PFR was not re-tried live; we used the cache only.
- The nflverse participation parquet at week8/betguru_.../pbp_participation_2026.parquet is **corrupt or not a parquet file** (bad magic bytes), so it couldn't be used as a trusted cross-check for man/zone or pressure.

## Gaps still uncovered
1. **Per-defender coverage allowed, full list, free**: no free source found. StatRankings has it only for the top 5; PFR cache (Oct 29) is still the only full list. Per-defender data is the gap that gets legs cut under 8A.
2. **Man/zone and MOF have no trusted cross-check.** Sharp vs StatRankings agree only directionally. The FTN charting fields aren't in our 2026 pbp cache, and the participation file is broken.
3. **Team pressure rate has no trusted cross-check** (the sources disagree on scale).
4. **ESPN PRWR team numbers** weren't extracted.
5. **QB time to throw** isn't independently verified (only the NGS page).
6. Untested: rbsdm, PlayerProfiler, nfelo, PropsMadness, Fantasy Points, SportsDataIO.
