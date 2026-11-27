# 2026 defender coverage profiles (all 32 defenses) — research only

Built 2026-11-27 (about 7:30 AM ET) by Blitz. Does **not** change betting rules, gates, `projection_ready` (stays false) or any `pregame/*.py`.
Nothing here is a coverage **assignment**. No free source publishes who covered whom.

## What is in here

| File | Grain | Source |
|---|---|---|
| `profiles/{TEAM}.md` | 1 per defense (32) | everything below, human-readable |
| `team_scheme_rates.csv` | team | Sharp (man/zone/MOFC/MOFO, blitz, box, sub, YPT by WR/TE/RB and **outside vs slot**), StatRankings (man/zone/1-high/2-high/blitz), FTN-via-nflverse blitz %; rank-based conflict flag |
| `defenders_cb_s_lb.csv` | defender × team | every CB/S/DB/LB with a 2026 defensive snap: snaps (PFR snap counts), PFR-charted tgt/cmp/yds/TD/INT/YPT/aDOT, passer rating **computed** from summed PFR totals, pbp-verified PBU/INT/DPI, inferred tackle-after-catch |
| `defender_weekly_log.csv` | defender × game | PFR weekly line (incl. PFR's own rating) + pbp verified/inferred receivers that game |
| `defender_target_log_pbp.csv` | play × defender link | every pbp link: PBU / INT / DPI (**verified**), first tackler on a catch (**inferred**), receiver, zone, yards |
| `team_allowed_by_position.csv` | team × WR/TE/RB | pbp targets, yds, YPT, TD, EPA/tgt, ranks |
| `team_allowed_by_zone.csv` | team × short/deep × left/middle/right | pbp; league YPT and rank; WEAK flag = top-8 YPT allowed with 12+ targets |
| `team_ngs_separation_allowed.csv` | team | target-weighted NGS separation of receivers vs that defense (receiver-side proxy) |
| `inputs/`, `MANIFEST.json` | — | small source snapshots, sha256 + URL of every raw input, pull times |

Counts (this build): 32 teams; 353 CB/S/DB rows (169 CB, 145 S, 39 listed only as DB) + 254 LB; 319 DBs have PFR-charted targets, 171 have 20+;
256 DBs have at least one verified pbp play. Links: 1,668 verified (1,241 PBU, 239 INT, 188 DPI) and 6,335 inferred (tackler).

## INFERRED attribution layer (added 2026-11-27)

`attribution.py` → `defender_attribution_inferred.csv` (each target: inferred defender, probability, runner-up, confidence, method, verified defender if any),
`defender_inferred_coverage_totals.csv` (probability-weighted targets/rec/yds/TD in each defender's vicinity), `upcoming_receiver_vs_likely_defender.csv`
(remaining Week 12 + Week 13 games), `attribution_validation_*.csv`. Held-out top-1 accuracy on verified plays, weeks 9–12: 25% overall, 36% in the high tier.
**INFERRED only**: method, validation and source findings are in `ATTRIBUTION_METHOD.md`.

## v2 window credit (added 2026-11-27)

`coverage_sim.py` simulates each defense's shell mix (10,000 draws per target) on a depth × width grid. It credits each catch to the defender whose window it
landed in, blended with the tackler. Held-out (wk 9–12) window-class accuracy: 32% (majority baseline 20%); exact defender: 24%.
Charts are in `charts/`. **INFERRED only**; see `ATTRIBUTION_METHOD.md`.

## Freshness and leak-free use

| Input | Through | Pulled (UTC) |
|---|---|---|
| nflverse pbp 2026 | week 12, last game 2026-11-26 (GB@LA, CHI@DET, PHI@DAL, KC@BUF) | 2026-11-27T12:26Z |
| nflverse pfr_advstats weekly def (PFR charting) | week 11 | 2026-11-27T12:26Z |
| nflverse snap counts / weekly rosters | week 12 | 2026-11-27T12:26Z |
| NGS receiving (nflverse) | week 12 | 2026-11-27T12:26Z |
| FTN charting (nflverse) | week 11 | 2026-11-27T12:26Z |
| Sharp public tables | page "Updated: November 24" | 2026-11-27T12:26Z |
| StatRankings team chips | last updated 2026-11-26T00:02:20Z | 2026-11-27T12:27Z |

All inputs predate every game still to be played (Fri DEN@PIT and later). For grading or backtesting an earlier week, rebuild with
`--through-week N`: that filters every nflverse table. Sharp and StatRankings are season snapshots with no week filter, so they are
**not** leak-free for weeks before their as-of date; use the dated older snapshots in `nfl-database/defense/coverage_tendencies_2026-11-22`
and `sources/sharp_2026-11-03` for that.

## Source rules

- Sharp and StatRankings chart differently. Sharp man % runs about 15 points lower than StatRankings on average (range 3–24).
  The conflict flag compares league ranks (gap of 8+ on man or blitz). Flagged this build: CHI, DAL, DET, LAC, NE, NO, NYJ, PIT. Do not mix the two sources on one slip.
- Passer rating per defender is computed with the NFL formula from summed PFR-charted totals; PFR's own per-game rating is in the weekly log.
- Pass direction (left/middle/right) is from the offense's view, as in nflverse.
- Slot vs outside alignment per defender: **MISSING**. The only free alignment number is Sharp's team-level YPT outside vs slot.

## Inventory of what we have (checked 2026-11-27)

| Source | Where | What | Teams / players | Date | Leak-free? |
|---|---|---|---|---|---|
| PFR advanced defense (season page) | `nfl-database/defense/pfr_defense_advanced_latest.csv` | per-player tgt/cmp/yds/TD/rating | 787 players, 32 teams | cached HTML ~Nov 4 (live PFR 403s from the box) | stale; superseded here by nflverse PFR weekly |
| PFR weekly via nflverse | this build | same metrics by game | 4,710 player-games wk1–11 | wk11 | yes with `--through-week` |
| Thursday CB/S coverage check (Rico Nov 1 routine) | no dedicated shared file found; closest are the two PFR files above plus `coverage_tendencies_2026-11-22` | — | — | last PFR refresh Nov 5 | this folder is the proposed shared home |
| Sharp coverage / tendencies / by-position | repo `data/coverage/sharp_coverage_2026.csv` (Nov 17), local Nov 3 / Nov 17 / Nov 24 snapshots, fresh pull here | team man/zone/shell, blitz, box, WR/TE/RB and outside/slot YPT | 32 teams | Nov 24 | for games after Nov 24 |
| StatRankings CoverageIQ | local Nov 22 pull, fresh pull here | man/zone/1-high/2-high/blitz | 32 teams | Nov 26 00:02Z | for games after that |
| NGS | repo `data/ngs` (W1–8), `week12/defprof/ngs_*.csv.gz`, nflverse | receiver separation/cushion | receiver-level only | wk12 | yes with `--through-week` |
| FTN charting via nflverse | `sources/nflverse`, nfl-sim | blitzers / rushers per play; **no man/zone column** | 32 teams | wk11 | yes |
| PFF | `nfl-database/pff_matchups/2026_w11/receiver_matchups.csv` (free Matchups tool, W11 projected CB/S per WR/TE); repo `data/pff_captures_w1_8` (121 game recaps, no coverage) | projections, not assignments | W11 slate only | Nov 22 | W11 only |
| Earlier per-team ledgers | `nfl-database/defenders/*_secondary.md` (23 teams), repo `data/redistributable/teams/defense/defense_db.csv` (tackler/PBU tags thru wk11), `dashboard/results/coverage_db_2026.json` (thru wk10) | tackler-tag style | partial | Nov 1–23 | partly |
| Week 9 coverage research ZIP v4 | `research/week9_coverage_routes_2026-11-07/` | 6-team PFR DB profiles, W8 film notes, PFF projected matchups QA | 6 teams | Nov 7 | W9 only |

## Gaps that still block verified-defender receiving legs

1. **No free per-play coverage assignment.** PFR charts the nearest defender but publishes totals, not per-target lines; pbp names a defender only on PBU/INT/DPI (verified) or as tackler (inferred). A clean catch with no flag names nobody reliably.
2. **Per-defender slot vs outside alignment: MISSING.** Team-level only (Sharp).
3. **PFF per-defender coverage grades / man-zone report: paywalled.** Only PFF's free projected-matchups page (W11 saved) is usable, and it is a projection.
4. **Per-defender man vs zone splits and NGS defender-level separation: not public.**
5. **PFR weekly lags pbp by one week** (wk11 vs wk12 here).
6. **39 defensive backs are listed only as "DB"** in snap counts (CB vs S unresolved).
