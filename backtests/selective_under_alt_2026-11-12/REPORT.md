# Selective under / alt backtest: NFL 2026 Weeks 4-9 (2026-11-12)

**Research only, not validated. This is not a pick list. `projection_ready` is not touched. Refs NFL-75.**
Pre-registration: `SPEC_FROZEN.md`, frozen 2026-11-12 6:26 PM ET, commit [56ef375](https://github.com/GhostPapii21/nfl-matchup-database/commit/56ef375f2b8063a9689c7cf5743201e247343a1f).
The strong-market list and the selector were frozen on Weeks 4-7 only, in commit [513ff6e](https://github.com/GhostPapii21/nfl-matchup-database/commit/513ff6e2741a7cf9fbad7270ec0e20f8084a81ca) at 6:32 PM ET. That was before any Weeks 8-9 outcome was read. Weeks 8-9 were scored at 6:43 PM ET.
Cost: **0 Odds API credits**, because only saved prices were used. Engine, `pregame/` and workflows are unchanged.

## Plain verdict
1. **One market beats its price: gated RB/QB rushing-yards unders.** Out of sample (Weeks 8-9) at X=+5 they went 18-5. That is a 78.3% hit rate against a 52.9% break-even, a +25.3-point margin (95% CI +5.8 to +39.5) and +47.4% ROI. **But n=23 is under 30, so it is too small to trust.** In-sample (Weeks 4-7) they were 50-32: 61.0% vs 52.9%, +8.0 points, CI −2.3 to +18.3.
2. **The market and the gate do the work, not the model's number.** With no edge filter at all, every gated rush under hit 60.6% in train (n=160) and 67.4% out of sample (n=43). Rush unders that fail the RB 60% carry gate hit 53.3% in train and 42.2% out of sample, below break-even. So the edge cutoff adds little, and the 60% carry gate is what separates winners from losers.
3. **Receiving unders (yards and receptions) do not beat their price**, in sample or out. These are also UNGATED, because there is no historical defender data.
4. **Alt plays are not shown to beat their price.** The rule picked long-shot ladder overs, with the median rung 1.0x to 2.5x above the main line and a 4-17% break-even. Alt receiving yards was "strong" in train (+4.4 points, n=110) but only +1.2 points out of sample (CI −8.9 to +12.7, n=41). **No real under-direction alt prices exist for player props in the saved inventory, which has Over-only alternates. Under-alts are UNKNOWN, not tested.** Game alt totals and spreads cover only 2 games (n=2 each).
5. **Game totals unders and spread sides: sample too small**, and the results point the wrong way. Weeks 4-5 have no named-book game prices, which is UNKNOWN. **Team totals: UNKNOWN**, because there are no saved main team-total lines and no team-points SD.
6. **The trained selector did not help.** It learned an edge coefficient of about 0 (−0.007 standardized), and price was its only real input. Out of sample it was 40-106, 27.4% vs a 35.3% break-even (margin −7.9, CI −15.9 to +0.5), worse than the control rule.
7. **The sample is not big enough to call this proven.** Weeks 8-9 out of sample are effectively one slate: Week 9 has only 29 saved prop legs, all from the TNF/MNF games. Weeks 4-9 were also already seen in earlier studies, where rush unders were known to be the edge. **Weeks 10-12 live are the real test.**

## Verdict table: control rule X=+5 with gates (in-sample Weeks 4-7 | out-of-sample Weeks 8-9)
Margin = hit rate minus the average break-even of the real graded price. CI = game-cluster bootstrap, 10k reps, seed 0. ⚠ = n<30, too small to trust.

| market (side) | IS n | IS hit / BE | IS margin [CI] | IS ROI | OOS n | OOS hit / BE | OOS margin [CI] | OOS ROI [CI] | verdict |
|---|---|---|---|---|---|---|---|---|---|
| rush yds UNDER (60% gate) | 82 | 61.0 / 52.9 | +8.0 [−2.3, +18.3] | +15.1% | 23 ⚠ | 78.3 / 52.9 | +25.3 [+5.8, +39.5] | +47.4% [+10.6, +74.4] | beats price, n too small |
| rec yds UNDER (ungated) | 311 | 51.8 / 53.0 | −1.2 [−6.8, +4.5] | −2.3% | 74 | 44.6 / 53.0 | −8.4 [−20.9, +5.8] | −15.8% | does not beat price |
| receptions UNDER (ungated) | 159 | 52.8 / 54.9 | −2.1 [−11.1, +7.2] | −5.3% | 73 | 50.7 / 55.5 | −4.9 [−19.4, +12.2] | −6.7% | does not beat price |
| rush+rec UNDER | 19 ⚠ | 52.6 / 53.1 | −0.5 | −0.8% | 4 ⚠ | 4-0 | n/a | n/a | too small |
| game total UNDER (Wk6-9 prices only) | 13 ⚠ | 38.5 / 51.5 | −13.0 | −25.4% | 11 ⚠ | 27.3 / 51.6 | −24.4 [−51.5, +3.0] | −47.1% | too small, negative |
| spread side | 24 ⚠ | 43.5 / 51.3 | −7.8 | −14.1% | 24 ⚠ | 54.2 / 50.5 | +3.6 [−17.2, +24.2] | +7.4% | too small |
| team total UNDER | unknown | — | — | — | unknown | — | — | — | no data |
| ALT rec yds OVER (ungated) | 110 | 23.6 / 19.2 | +4.4 [−3.5, +12.5] | +44.5% | 41 | 24.4 / 23.2 | +1.2 [−8.9, +12.7] | +11.0% [−64.9, +109.6] | not shown |
| ALT receptions OVER (ungated) | 102 | 9.8 / 9.3 | +0.5 | −3.3% | 36 | 8.3 / 10.9 | −2.6 [−9.4, +4.1] | −11.7% | does not beat price |
| ALT rush yds OVER | 30 | 13.3 / 19.7 | −6.4 | −71.1% | 16 ⚠ | 25.0 / 21.9 | +3.1 | −38.9% | does not beat price |
| ALT rush+rec OVER | 0 | — | — | — | 3 ⚠ | 0-3 | — | −100% | too small |
| ALT game total (O/U) | 0 | — | — | — | 2 ⚠ | 2-0 | — | — | too small |
| ALT spread | 0 | — | — | — | 2 ⚠ | 1-1 | — | — | too small |
| ALT under-direction props | unknown | — | — | — | unknown | — | — | — | no real prices saved |

The X grid {+3, +5, +8} is all reported in `results_control_is_oos.csv`, with no cherry-picking. Out-of-sample rush unders were +24.0 at X=+3 (n=26) and +25.3 at X=+5 (n=23). The X=+8 row is in the file.
Receiving markets and receptions are negative at every X. At X=+8, alt receiving yards turns clearly negative out of sample: 2-25, −15.5 points, CI −26.0 to −4.3.

### Markets flagged "strong" in train (frozen 513ff6e), shown out of sample as required
| market | train n / margin / ROI | OOS n | OOS hit / BE | OOS margin [CI] | OOS ROI |
|---|---|---|---|---|---|
| ALT rec yds over | 110 / +4.4 / +44.5% | 41 | 24.4 / 23.2 | +1.2 [−8.9, +12.7] | +11.0%: **faded to near zero** |
| rush yds under | 82 / +8.0 / +15.1% | 23 ⚠ | 78.3 / 52.9 | +25.3 [+5.8, +39.5] | +47.4%: **held, n too small** |

### Per-week out-of-sample results (control X=+5; full list in `results_oos_by_week.csv`)
- Rush unders: Week 8 went 17-5 (n=22, 77.3% vs 52.7%). Week 9 went 1-0. **So the out-of-sample sample is one week.**
- Receiving-yards unders: Week 8 n=69 (44.9% vs 53.0%), Week 9 n=5 (40.0%). Receptions unders: Week 8 n=70 (50.0% vs 55.4%), Week 9 n=3.
- Spread sides: Week 8 n=12 (58.3% vs 50.1%), Week 9 n=12 (50.0% vs 50.9%). Game total unders: Week 8 n=5 (20%), Week 9 n=6 (33%).

### Probability-cutoff sensitivity, TRAIN ONLY (`results_cutoff_sensitivity_train.csv`): filter vs number
Gated rush unders, picking every leg with p_model ≥ cutoff:

| cutoff | none | 0.50 | 0.55 | 0.58 | 0.60 | 0.62 | 0.65 |
|---|---|---|---|---|---|---|---|
| n | 160 | 101 | 82 | 74 | 68 | 56 | 44 |
| hit % | 60.6 | 60.4 | 62.2 | 59.5 | 60.3 | 58.9 | 59.1 |
| BE % | 53.3 | 53.2 | 53.3 | 53.3 | 53.3 | 53.4 | 53.7 |

The hit rate stays flat as the cutoff rises. **The edge comes from the filter (rush under plus the 60% carry gate), not the model's probability.** Receiving unders stay at or below break-even at every cutoff. Alt rush overs are well below break-even at every cutoff, and alt receiving yards sits within about ±3 points of break-even.

### Selector (L2 logistic, C=0.5, trained Weeks 4-7, frozen 513ff6e) vs control, out of sample
| market | selector OOS n / hit / BE / margin | control X=+5 OOS n / margin |
|---|---|---|
| rush yds under | 2 ⚠ / 50.0 / 53.1 / −3.1 | 23 ⚠ / +25.3 |
| rec yds under | 37 / 37.8 / 53.1 / −15.3 | 74 / −8.4 |
| receptions under | 10 ⚠ / 20.0 / 55.5 / −35.5 | 73 / −4.9 |
| spread | 11 ⚠ / 36.4 / 51.1 / −14.7 | 24 ⚠ / +3.6 |
| ALT rec yds | 46 / 28.3 / 28.2 / +0.1 | 41 / +1.2 |
| ALT receptions | 23 ⚠ / 8.7 / 7.0 / +1.7 | 36 / −2.6 |
| ALL | 146 / 27.4 / 35.3 / −7.9 [−15.9, +0.5] | — |

Overfit verdict: with 3,650 training rows across 6 markets (most of them alt rungs), the regularized model put almost all its weight on break-even (+1.09) and none on edge. It mostly re-learned the price. **Don't use it.** If a selector gets another try, it should be a hand rule: market + gate, then the price.

## Slip study (Weeks 8-9 only, legs from the train-frozen strong markets)
| slips | n slips | cash rate | ROI per $1 |
|---|---|---|---|
| Greedy top-2 / 3 / 4 by margin, one per game, Week 8 | 1 / 1 / 1 | 0 / 0 / 0 | −100% each |
| Every 2-leg combo, one leg per game, Week 8 (exact) | 1,813 | 17.9% | +45.7% |
| Every 3-leg combo, Week 8 | 31,531 | 7.3% | +65.0% |
| Every 4-leg combo, Week 8 | 369,403 | 2.9% | +79.0% |
| Week 9 | 0 | — | not buildable (one strong-market flag) |
| **Rico's actual NFL tickets, Weeks 8-9** (bet log) | 4 | 0 of 4 | −100% (unit) |
| **Rico's actual NFL tickets, Weeks 4-9** | 34 | 2 of 34 = 5.9% | −50.1% (unit) |

Read this with care. The all-combo rows are one week of heavily overlapping combinations, not independent slips. Their positive ROI comes from a few alt-ladder long shots that hit, while the rush unders went 17-5 that week. The greedy "best" slips all lost. Rico's tickets averaged 7.7 legs, against 2-4 here.
Actual-ticket ROI is per $1 flat at the listed odds, because stakes are mostly not in the log. Bonus-bet tickets count as −1. Paper, no-stake, cashed-out, open and pending tickets are excluded (7 in Weeks 4-9).

## Proposed replacement NFL-75 criterion (in place of "overall Brier vs close")
> **Selective-signal gate.** Using a flag rule frozen and committed before Week 10 kickoff (this spec, 56ef375, strong list 513ff6e, X=+5, gates on), the live holdout of Weeks 10-12 must show, **for each market separately**:
> **(a) at least 30 flagged plays with real saved pre-kick prices**,
> **(b) a hit rate at least 3.0 points above the average break-even of the graded price**, and
> **(c) a game-cluster bootstrap 95% CI on that margin with a lower bound above 0.**
> If (a) isn't reached by Week 12, extend through Week 14 rather than lowering the bar. Only markets that pass may be flagged as "strong" to Rico. Receiving markets also need the verified main defender gate captured live. Alts need real alt prices in the same direction as the read (under-alts must be captured, since they don't exist in the saved data). Overall Brier and side accuracy vs the close stay diagnostics only.

Today only rush unders are on track. Week 8 produced 22 flags in a full slate, so about 3 weeks should reach n≥30, *if live props prices are saved each week*. That depends on the price feed/quote ledger. Odds API pulls must keep the 800-credit floor.

## Sources and pull times (no invented numbers; missing = unknown)
- **Props + main prices + walk-forward sim probabilities:** `/workspace/nfl-database/backtests/confidence_check_2026-11-03/legs_with_probs.csv`, sha256 3a945f3c…69a2. These are single-book snapshots taken a median of 34.4 min before kickoff (range 29.4-39.4). Snapshot times run from 2026-10-01 7:40 PM ET to 2026-11-02 7:45 PM ET. Outcomes are nflverse box scores (CC-BY-4.0).
- **Alt rungs and game prices:** `/workspace/research/historical_nfl_odds_inventory_2026-11-07/sportsbook_observations.csv`, sha256 d59d7cc9…0b65, built 2026-11-07 7:14 PM ET. Only rows with `verified_capture_before_start` and snapshot < kickoff were used. Each is the latest pre-kick quote per book, best price across books. Some game quotes are days before kickoff, especially Week 9 Sunday (about 25-36 h).
- **Game sims:** `calibration/outputs/backtest_wk04_09_n2000_per_game.csv` (PR #21, run 2026-11-12 3:45 PM ET, engine eb48efe, arm new_off), using a Normal approximation.
- **Carry shares:** `data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet` (pulled 2026-11-12 11:16 AM ET), prior weeks only.
- **Bet log:** `/workspace/bet-log.csv`, sha256 cf916228…a49a, file time 2026-11-12 10:33 AM ET.
- The alt-rung probabilities come from re-running the same three read-only engine copies with the same leak-free cutoffs. Main-rung probabilities reproduced the saved ones exactly (max diff 2e-16 over 1,270 legs).

## Skeptical self-review (Blitz; no external reviewer was run for this research-only PR)
1. **Not a clean holdout.** Earlier studies found rush unders were the edge on Weeks 3-8. Picking "rush unders" as strong in train therefore isn't independent of that prior knowledge. Weeks 10-12 are the only clean test.
2. **The out-of-sample window is really Week 8.** Week 9 has 29 saved prop legs. One good week of rush unders (17-5) drives the out-of-sample headline.
3. **Alt prices are best-of-books** among saved quotes, which is optimistic. The alt rule ended up picking ladder long shots, not safer "alt-down" rungs, so it doesn't answer Rico's "when to take an alt" question for safety rungs.
4. **The defender gate isn't evaluable** historically, so every receiving result is ungated.
5. **Bootstrap clusters on games.** Within-game correlation is handled, but within-week correlation (weather, slate effects) is not.
6. **Multiple comparisons:** 3 X values × about 12 markets × 2 sets. One market with a CI above 0 out of sample is consistent with chance at this volume, which is one more reason the n≥30 live bar matters.
7. **Code fixes after the first Weeks 8-9 scoring run, disclosed:** (i) the all-combinations slip count was capped and lexicographic, and was replaced by exact enumeration; (ii) a bet-log parse bug counted the no-stake "TNF1029-LEANS" board as a ticket. No flag rule, X, strong list or selector changed. Leg-level files carry book prices and stay off this public repo: `/workspace/research/selective_under_alt_2026-11-12/`.
8. **There is a code-level assertion** that no week or game_id is in both train (Weeks 4-7) and test (Weeks 8-9), in `s5_score_oos.py`.

## Files
SPEC_FROZEN.md (+sha256); strong_markets_wk4_7.json and selector_frozen.json (+FROZEN_WK4_7.sha256); s1-s6 scripts and common.py; results_*.csv (aggregates only); oos_run_meta.json.
Rerun order: `s1_build_alts.py`, then `s2_run_alt_sims.py ENGINE WEEK` (3 engines × weeks 6-8), `s3_candidates.py`, `s4_select_wk4_7.py`, `s4b_cutoff_sensitivity_train.py`, `s5_score_oos.py`, `s6_descriptives.py`.
