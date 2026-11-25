# Model audit, Nov 24, 2026 (five audit prompts, applied to our prop model)

Read-only. Nothing in the model, the board, the weights or any saved record was changed. Numbers come from
`audit.py` (`results.json`). Every prediction uses earlier weeks only.

**What was audited**
- The opportunity simulation, with the board's calibration layer. It drives the chance tables, the book-line columns
  and the brief.
- The 80-yard star model (`dashboard/watch_model.json`).

The game model (100k locks) has only 2 scored games, and both are known-error locks, so it is not audited here.

## 1. Edge auditor: model vs FanDuel, 2026 Weeks 8-9

**Data**
- 4,396 FanDuel alternate rungs, saved at T-90 (427 player-games), matched to the simulation.
- FanDuel posts overs only. Prices are de-vigged with the main-line average hold (6.4%).

**Brier score** (lower is better):

| Source | Brier |
|---|---|
| Market, de-vigged | **0.1603** |
| Model | 0.1660 |
| 50/50 blend | 0.1607 |

The market was better than the model, and the blend did not beat the market for the simulation. (For the 80-yard star
model the blend was best: 0.1118 vs 0.1133. That is where the blend's support comes from.) On average the model sits
4 points below the market, which is the known slate-wide lean the brief removes.

**Did bigger edges pay?** Overs bet at FanDuel, grouped by model-minus-market gap:

| Gap | Player-games | Model | Market | Hit | Over ROI (95% CI) |
|---|---|---|---|---|---|
| 0 to +5 | 183 | 37% | 35% | 35% | -16% (-36 to +4) |
| +5 to +10 | 92 | 44% | 37% | 38% | +2% (-30 to +42) |
| +10 to +15 | 47 | 49% | 37% | 43% | +10% (-29 to +53) |
| **+15 or more** | 21 | 55% | 34% | **32%** | **-18% (-58 to +33)** |

- Edges up to about 15 points did a little better as they grew, but every interval includes zero.
- The biggest edges (15+ points) were the worst group. Bigger projected edges have not reliably produced better results.

**The 20 biggest gaps** are in `results.json` (`1_edge_auditor.top20`), with model, market, edge, result and inputs
(expected volume, share, earlier games, trailing mean, simulation mean). What they show:
- **Most are "model far below the book" (17 of 20), and the book was right in 11 of those.** Examples: Singletary 29.5
  rush (model 23%, book 82%, ran for 31), McConkey 24.5 receiving (book 77%, 86 yards), Chase 69.5 (book 62%, 141 yards).
- **Missing data is the main cause.** The backtest has no injury or teammate-out information
  (`dashboard/backtest_opportunity.py:10`). The books knew who was out; the backtest did not. Singletary's expected
  carries were 5 because his share came from games where he was the backup.
- **Model far above the book:** Aaron Jones 39.5 rush (model 77%, book 31%, ran for 22). Tremayne and Sample were thin
  roles (2-4 expected targets) that the books priced far lower; both missed.

**Checks**
- 60 player-games had 4 or fewer earlier games (small samples).
- 1,623 rungs were priced at -500 or longer, or +500 or more. These are ladder tails where a few points of de-vig error
  dominate the edge.
- 104 of the 522 gaps over 15 points sat on rungs below half or above double the player's trailing mean.
- No stale-price problem was found: every price is from the T-90 snapshot (`pull_log.jsonl`). No calculation errors were
  found in the de-vig or grading. The one known approximation is the hold proxy, because FanDuel posts no alt unders.

## 2. Feature eliminator

### Simulation parts, switched off one at a time (2026 Weeks 5-11)

Nothing in the simulation was fitted on 2026. That gives 6,495 predictions across 9 lines (40/60/80 receiving yards,
4/6 catches, 50/70 rushing yards, 12/15 carries).

| Version | Brier | Log loss | Calibration gap | Yards miss | FanDuel overs, model +5 pts (bets, ROI) |
|---|---|---|---|---|---|
| **Full (as the board runs it)** | **0.13421** | **0.4191** | **0.013** | **22.1** | 549, +0.8% |
| Without the volume correction | 0.13708 | 0.4254 | 0.040 | 23.2 | 1,245, -6.8% |
| Without shrinking to league rates | 0.13576 | 0.4260 | 0.021 | 22.4 | 674, -5.9% |
| Without the output calibration layer | 0.13461 | 0.4219 | 0.021 | 22.1 | 485, +2.5% |
| Without the game-script adjustment | 0.13449 | 0.4196 | 0.014 | 22.2 | 588, -0.3% |
| Without role uncertainty | 0.13440 | 0.4210 | 0.013 | 22.1 | 597, 0.0% |
| **Without the defense adjustment** | **0.13429** | **0.4195** | **0.012** | **22.1** | 573, -2.1% |

- **Carry the model:** the volume correction and shrinking to league rates. Removing either clearly hurts accuracy and
  betting results.
- **Small but real:** the calibration layer, game script and role uncertainty.
- **Little measurable value: the defense adjustment.** Removing it changes Brier by 0.00008, and the calibration gap is
  slightly better without it. This matches the Nov 23 defense-gate test.

### 80-yard star model, one input group dropped (fit on earlier seasons only, tested on the next season)

Held-out log loss (lower is better); "better" means the result improved when the group was removed.

| Dropped group | 2024 | 2025 | 2026 (370 rows) |
|---|---|---|---|
| None (all inputs) | 0.28239 | 0.26280 | 0.30053 |
| Volume (targets) | 0.28761 (worse) | 0.26569 (worse) | 0.29835 (better) |
| His production (yards a game) | 0.28476 (worse) | 0.26494 (worse) | 0.30837 (worse) |
| Game environment (team total, pass volume) | 0.28228 (better) | 0.26407 (worse) | 0.29971 (better) |
| **Defense (big plays allowed, 80+ games allowed)** | **0.28211 (better)** | **0.26296 (worse, tiny)** | **0.29934 (better)** |

- The defense inputs add nothing measurable here either. Dropping them helped in 2 of 3 seasons, and Brier was better
  without them in all 3.
- Production is the one group that helps every season.
- Per the prompt, nothing is removed until you review this.

## 3. Confidence checker (2026, the simulation's favoured side)

| Said | Predictions | Average said | Happened | Flag |
|---|---|---|---|---|
| 50-60% | 846 | 54.9% | 53.5% | ok |
| 60-70% | 895 | 65.0% | 65.9% | ok |
| 70-80% | 989 | 75.4% | 77.2% | ok |
| 80-90% | 1,316 | 85.3% | 84.3% | ok |
| 90%+ | 2,449 | 95.9% | 95.1% | slightly overconfident (0.8 points; mostly lines far from the player's mean) |

| Model or baseline | Brier |
|---|---|
| **Model** | **0.1342** |
| Player's own hit rate | 0.1426 |
| League base rate | 0.1707 |

- The model beats both baselines in every one of the 9 markets.
- Under-called: carries 15+ (said 27.5%, happened 31.8%) and rushing yards 50+ (said 36.7%, happened 38.7%).
- The 80-yard stars (2025-26, weights from 2022-24) are also on target:

  | Stars | Said | Hit |
  |---|---|---|
  | 3 | 56% | 54% |
  | 2 | 44% | 45% |
  | 1 | 34% | 33% |

- Small samples: MNF is the only game with book prices saved before kickoff (30 prop markets). Prices for a market's
  calibration need weeks of saved boards. Week 12 is the first full slate.
- No recalibration was made.

## 4. Backtest investigator

### Confirmed problems

1. **Our own season-by-season test used future seasons.** `research/shadow_2026-11-23/by_season.py:36` fits on
   "every other season", so testing 2023 used 2024-26.
   - Effect: "rising role helped in 2 of 3 seasons" was optimistic.
   - Strictly chronological (section 5), it is inconclusive.
2. **Part of the headline simulation backtest is in-sample.** The volume correction and output calibration were fitted
   on 2024-25 backtest rows (`dashboard/opportunity.py:38-40`, `research/calibration_2026-11-22`), and game script on
   2022-24 (`opportunity.py:207`). `dashboard/results/opportunity_backtest.md` pools 2024-2026.
   - Effect: its 2024-25 rows flatter the model.
   - Only 2026 (reported separately as `holdout_2026`, and used in sections 2-3 here) is clean.
3. **The MNF brief was made after the game.** `research/briefs/2026/2026_11_CIN_WAS/brief.json` has `made_utc`
   05:34Z Nov 24, after kickoff. The rules it shows (blitz-heavy WR1 fade, under penalty, 56% floor) were chosen after
   seeing MNF.
   - Effect: it must never be counted as a pregame pick record.
   - The rules are graded only from Week 12 on.
4. **The backtested model is not the live model.** The backtest has no injury or teammate-out shift, no backup-QB
   factor and no weather (`dashboard/backtest_opportunity.py:10`). Those pieces rest only on their own studies.
   - Effect: the live board's full combination has no backtest.
   - Section 1 shows missing injury information is the main source of the biggest gaps.
5. **The game-model evaluation contains only known-error locks.** `evaluation/EVALUATION.json`'s 2 scored games are both
   listed in `snapshots/KNOWN_MODEL_ERROR.md`. Its status is correctly "UNSCORABLE", but its aggregate numbers are not
   evidence.

### Potential risks (not shown to matter yet)

- **Closing lines.** The backtest uses the closing spread and team totals (`backtest_opportunity.py:95`; `implied` in the
  receiver rows). The live board uses the line at build time, earlier than the close. Mild optimism.
- **Live star weights include 2026 through Week 9** (`research/watch_model_2026-11-16/fit.py`). This is fine for
  Week 10+ grading, but any star result on 2026 Weeks 1-9 with live weights is in-sample.
- **Weeks 8-9 alt ladders** were used to choose the blend for the stars (`watch_model.json` `book_grade`). Judging the
  blend again on Weeks 8-9 is circular. The prereg discloses that Weeks 8-9 were seen in earlier studies.
- **Same game counted twice.** `snapshots/score.py:120` averages DraftKings and FanDuel lines on the same game together
  (Pinnacle excluded), so n overstates independent results.
- **One nflverse row is labeled "close" but was pulled after kickoff** (`data/lines/README.md`). It is labeled
  correctly; it just must not be used as a pregame capture.
- **Selections left out:**
  - Alt-ladder grading voids players with 0 snaps (as books do).
  - 742 rungs were left out of section 1, because the simulation doesn't project players under 8 earlier targets or
    15 carries.
  - Both are disclosed, but results describe projected players only.

### Validation tests to add

- Score every new candidate strictly forward: fit on earlier seasons, test on the next.
- Grade the brief's picks only from Week 12, using `made_utc` before kickoff as the entry ticket.
- Backtest the injury shift on past seasons, using each week's inactives.
- Re-run section 1 on Week 12 main lines, which are two-sided, so the de-vig is exact.

## 5. Change tester: rising role (the side-by-side candidate)

**Current model:** the board's receiver 80+ chance (six inputs).
**Change:** add `log(last game's target share / season share)`.
**Hypothesis:** a role that just grew is under-counted by season averages.

Fit on earlier seasons only; tested on the next season:

| Season tested | Fit on | Log-loss change (95% CI) | Brier, current -> with |
|---|---|---|---|
| 2024 | 2022-23 | +0.0007 (-0.0012 to +0.0026) worse | 0.08625 -> 0.08665 |
| 2025 | 2022-24 | -0.0010 (-0.0022 to +0.0001) better | 0.07615 -> 0.07602 |
| 2026 | 2022-25 | +0.0008 (-0.0024 to +0.0043) worse | 0.08904 -> 0.08921 |

- **Inconclusive, leaning no.** It is better in 1 of 3 seasons and every interval includes zero.
- By subgroup:
  - Starred players: mixed (better in 2024, worse in 2025-26).
  - Players whose role fell last game: hurt in 2024 and 2026.
- **Recommendation:** keep it in the side-by-side run (it never moves stars), and do not deploy it.
