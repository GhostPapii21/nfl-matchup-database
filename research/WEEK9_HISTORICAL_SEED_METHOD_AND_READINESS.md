# NFL Week 9 research-only historical projection inputs
**Generated:** 2026-11-07, before Sunday's Nov 8 kickoffs
**Status:** UNADJUSTED OBSERVED HISTORY. **NOT** fitted forecasts, player predictions, score projections, market edges or bet-eligible recommendations.

## Source and output
Source: connected Render PostgreSQL `sportsbook-odds-history`, `player_game_observations` joined to `historical_packages`, 2026 NFL, `verified=true`, `source=nflverse`, `p.source=nflverse`, and `game_date < 2026-11-08`. This is read-only. The reviewed W1–8 additive package SHA is `e542672edd68d37b90bb554b12964a818733e1d8ca525d31ffb7d295c1bba31c`. Source: public nflverse CC-BY-4.0 game observations archived in Odds Bridge. [Official Week 9 schedule](https://www.nfl.com/schedules/2026/by-week/week-9).

Deduplication: `ROW_NUMBER() OVER (PARTITION BY game_id,player_id,market_key ORDER BY historical_packages.imported_at DESC,package_id DESC)`; **keep only the first**. Old and new packages share games. The account's live DB has 121 W1–8 regular-season games; duplicate source rows are *not* additional games.

Generated across **13 Sunday Nov 8 games and 26 teams**, without altering any existing data, model weights, source tables, or production deployments:
- `WEEK9_VERIFIED_HISTORICAL_REFERENCE_20261107.csv`: **283** market-specific historical rows for selected player/market pairs. Four keys: passing yards (QB context), receptions, receiving yards, rushing yards. Conditional history **only games where the player's selected stat has positive recorded opportunities**. Top opportunities on each team by market, not automatically verified Week 9 starters. Includes observed minimum/maximum and last 3/5 positive-opportunity game averages; no Q1/Q2 stat adjustments. Some 2026 W1–8 teams have a bye in prior weeks; counts vary.
- `WEEK9_HISTORICAL_RUSH_RECEIVE_REFERENCE_20261107.csv`: **104** market-specific combined rush+receive history rows, calculated by adding that **same player's two stats within each actual game**, with at least one positive carry or target; avoids independently combining unrelated market draws. This is **only the observed average**, not `P(over)`.
- `WEEK9_DEFENSE_ALLOWED_HISTORICAL_REFERENCE_20261107.csv`: **26** defenses' raw game-level averages for pass/rush yards, receptions, targets, and pass attempts by the opposing offense. Each game counted once. Opponent quality, garbage time and personnel are **NOT** adjusted. Pressure, blitz, man/zone, safety shell, explosive counts and defender attribution intentionally blank.

IMPORTANT: conditioning on `opportunities>0` **excludes zero-opportunity games**, which can bias a receiver or RB historical reference upward. It must not be used directly as a pregame mean without verified route/snap participation, DNP status and chance of zero targets or carries. Transferred/injured players and Sunday starters are NOT validated from this extract. Missing is unknown, not zero.

## Sample research checks (examples, not picks)
- **Cowboys @ Colts:** CeeDee Lamb 88.63 mean receiving yards over 8 positive-target games; George Pickens 66.63 over 8; Indianapolis allowed 226.25 passing and 131.75 rushing yards per W1–8 game (raw team totals). No conditional receiver-vs-CB projection can be inferred without usable route/coverage records.
- **Packers @ Patriots:** Christian Watson 88.50 and Matthew Golden 77.38 receiving yards per positive-target game (8 each); Patriots allowed 235.50 passing and 92.63 rushing yards/game. No inferred shadow, no injury or pressure adjustment.
- **Buccaneers @ Bears:** D'Andre Swift averaged 88.38 combined rush+receiving yards in 8 games with at least one rush/receiving opportunity; Luther Burden III averaged 72 combined (including 3.63 rush + 68.38 receiving, same game). Tampa Bay allowed 80.00 rushing yards/game (raw). Do not assume Swift's rushing efficiency or Burden's routes are constant.
- The Week 8 source checks match the official reconciliation in Grok's audit: Golden **7 receptions, 79 receiving yards (13 targets)**; Burden **7 receptions, 56 yards (9 targets)**; Caleb Williams **34 passing attempts, 247 passing yards**. Golden's conflicting 83-yard derived PBP value remains unresolved; this database uses 79.

## Still required before generating actual Sunday probabilistic projections

| Model requirement | Present in this seed? | Blocker |
|---|---|---|
| Historical 2026 player-game source outcomes | YES | source audits and sample filtering still needed |
| Team-level raw opponent passing/rushing allowed | YES | opponent-adjusted pace and current personnel not fitted |
| True Q1/Q2/Q3/Q4 spreads and 1H winners | NO | quarter scoring by drive, pace/game-state model and market scope missing |
| Current QB, RB, WR, TE routes, targets and personnel | PARTIAL | Grok's **187-player full source rows remain only in bot local bundle**, not in PR #2 |
| Individual 249 PFR and 76 free-PFF defender charts | NO | only summary counts in PR #2; numbers, rights, IDs, clocks missing |
| Man/zone and MOFO/MOFC + middle completion/explosive | NO | no redistributable audited post-snap charting |
| Blitz vs 4-rusher pressure, sack finishing | NO | validated per-dropback rates and time-to-pressure missing |
| Allen/Lamar/Purdy/Maye scramble-vs-designed run model | NO | verified play-level scramble/pressure inputs needed |
| Current official injuries/inactives and verified Week 9 starters | PARTIAL | Friday reports exist, game-day inactives pending |
| Frozen out-of-sample scenario calibration and error | NO | no backtest-ready pregame scenario predictor |
| Exact sportsbook book, line, period, captured_at and house rules | NO | no validated current quote ledger; no EV or picks |
| Real Suave OAuth consumer read and hosted projection board | NO | NFL-71 access/auth and rollout remain unresolved |

## Next steps with the two-bot research handoff

1. Obtain the actual **authorized numeric CSVs** and data-rights manifest from Blitz and Ghost6, not just the summaries. See [Grok draft PR #2](https://github.com/GhostPapii21/nfl-matchup-database/pull/2). No bot-local `/workspace` path can be treated as an API/file delivered to this repository.
2. Join Grok's stable GSIS player IDs and canonical game IDs to this verified history. Independently spot check 3+ players per role and at least one injured replacement. Require a source-at-kickoff clock and true zero-usage games.
3. Fit opponent and personnel conditional opportunities on W1–8 with strict chronological validation, separate forecast uncertainty, and compare against the unchanged baseline. Do NOT claim calibrations from 8 games.
4. Fit quarter scoring from verified **play-by-play/team drive scoring and score states**, and pressure / CB / explosive / scramble mechanics only from authorized tracking. No empty metric should turn into a guessed rate.
5. Run the PR #108 `nfl-scenario-pro-bets` joint game-script distributions with calibrated inputs. Output research-only until NFL-68 and NFL-71 gates pass.

**No wagers or real-money recommendation generated.**


## Nov 7 additional source-verified defensive mechanics and TE audit

Four new read-only research files now accompany this historical seed:

- `WEEK9_DEFENSIVE_EXPLOSIVE_SACK_FLAG_RATES_20261107.csv`: **26 teams**, calculated from the existing Odds Bridge `data_packages/nfl_2026_w1_8/team_play_counts.csv` (Git blob `f7a7d350b923b2506bc476f68378e935639c96d9`), which contains **242 team-game rows / 121 completed games**. For each defense, records total and per-game completed explosive pass **play flags with yards_gained >=20**, rush play flags >=10, sacks, QB hits, pass attempts and rush attempts. `explosive_passes / pass_attempts` is the empirical pass-play flag rate; `sacks / (pass_attempts+sacks)` is an explicitly imperfect *sack-play proxy* that excludes QB scramble dropbacks, NOT true sack rate per dropback. `qb_hit` flag is NOT charted pressure, and may overlap sacks. QB hit and sack counts must NEVER be added as disjoint events. Two-sided Wilson 95% intervals assume independent Bernoulli attempts and do NOT adjust for intra-game clustering; treat as descriptive uncertainty, not calibrated future coverage probabilities. Game-level counts, share of games with >=3 explosives and games with any explosive reflect historical volatility.
- `WEEK9_PLAYER_DEFENSE_JOIN_RESEARCH_ONLY_20261107.csv`: **283** player-market rows aligned to opponents using stable team names, showing prior positive-opportunity averages alongside those opponents' **team-level only** explosive and sack flags. **Estimated opportunities, matchup-adjusted predictions and calibrated probabilities are intentionally BLANK** until Grok source usage and opponent pressure/coverage files are verified.
- `WEEK9_TE_USAGE_SOURCE_CROSSCHECK_20261107.csv`: audited all **10** named TEs from Grok's newly published `research/WEEK9_TE_USAGE_TARGET_ROUTE.csv` against deduplicated `player_receptions` nflverse target totals, GSIS ID by name/team, source dates. **8 reported target totals matched**, **Tyler Warren has no Grok total** (verified Render has 46), and **AJ Barner CONFLICTS: Grok says 51, Render says 34**. Do not silently choose the higher number. Grok CSV's `routes_run`, snap shares, defender named assignments and target shares do not carry exact per-row provider URLs or per-game denominator provenance and therefore are **not approved** as model inputs.
- `WEEK9_RETROSPECTIVE_ROLLING_BASELINE_ERRORS_20261107.csv`: an **unadjusted retrospective active-game** rolling-five forecast error audit for 2026 Weeks 5–8, using only earlier games of the same player and market. Evaluated samples: passing yards 104 (MAE **69.42**), receptions 682 (MAE **1.53**), receiving yards 682 (MAE **21.60**), rushing yards 304 (MAE **21.13**), combined rushing+receiving 846 (MAE **23.48**). This reports actual variability and supports conservative research uncertainty. Crucial limitations: no historical bookmaker prices/prop lines, selection conditional on `opportunities>0` in the evaluated game (known only after the game, hence **NOT** a valid unconditional prospective backtest), only four retrospective evaluation weeks, no dynamic injury/starting-lineup chronology, no defender charting or alternate/game/quarter scoring markets. **No calibrated `P(over)`, betting edge, or claimed win rate follows from these MAE values.** Combined yards are summed from each *same* game before calculating a rolling five.

### Specific descriptive defensive comparisons, not picks

| Week 9 offense versus defense | Explosive passes (>=20) / pass attempts allowed | Pass-play flag rate | Sack flags / (attempts+sacks) | Interpretation |
|---|---:|---:|---:|---|
| Dallas at Indianapolis | 23 / 246 | 9.35% | 16 / 262 = 6.11% | IND has historically allowed more 20+ pass attempts than GB/SEA, but individual corner responsibility unknown |
| Green Bay at New England | 25 / 281 | 8.90% | 22 / 303 = 7.26% | NE opponent wide/deep opportunity context is materially different from CB man assignment |
| Arizona at Seattle | 12 / 266 | 4.51% | 18 / 284 = 6.34% | SEA allowed fewer explosive passes in its observed W1–8 sample; does not prevent a one-play tail event |
| Tampa Bay at Chicago | 23 / 254 | 9.06% | 22 / 276 = 7.97% | CHI has a stronger observed sack-flag proxy, but pressure and blitz-by-QB decision are not measured |

**Defense flags and rolling error audits are joined source descriptors only.** They are not validated causal effects, matchups against specific CB/S, sack conversion probabilities, QB true scramble tendencies or a calibrated scoring simulator. Until per-play man/zone, defender attribution, packages and actual 2026 offense pressure/route data arrive, **NO** numeric CB matchup multiplier may be applied.

