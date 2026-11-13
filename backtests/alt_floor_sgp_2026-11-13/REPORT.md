# Alt-floor SGP backtest: Rico's target slip style (2026-11-13)

**Research only. Not a pick list. `projection_ready` stays false. Engine weights, `pregame/` and workflows are untouched. refs NFL-75**
Run: 2026-11-13 12:19 AM ET. Odds API cost: **0 credits** (balance check via the 0-credit `/v4/sports` call at 12:15 AM ET: 1,740 remaining). Only saved prices were used.

Template: TNF WAS@NYG FanDuel SGP, $125 at +413, 8 legs, all cashed (Likely 20+, Fields 15+, Nabers 40+, Diggs 25+, A. Williams 20+, Okonkwo 15+ rec yds; Skattebo 25+ rush yds; alt Under 54.5).

## Inputs (sources and pull times)
- Prices: `sportsbook_latest_verified_pregame.csv` from the 2026-11-07 historical odds inventory (files written 2026-11-12 6:58 PM ET). Latest verified pre-kick quote per book/rung. All quotes assert snapshot < kickoff.
  Leg price = **FanDuel** quote when FanDuel listed the rung (79-90% of graded legs), else **median across books** (flagged `median_books`). FanDuel-only results are shown separately.
- Outcomes: nflverse pbp 2026 Weeks 1-9, pulled 2026-11-12 11:16 AM ET (sha256 1028614b...). Player-game rec, rec yds, rush yds were checked against the 1,355 Week 6-9 main-line legs in `confidence_check_2026-11-03`: **100% exact match**.
- Usage features use **only weeks before the game week**: the player's last 6 games with at least one touch/target.

## Data coverage (real alt prices)
| | Wk 4 | Wk 5 | Wk 6 | Wk 7 | Wk 8 | Wk 9 |
|---|---|---|---|---|---|---|
| Player alt overs (rec, rec yds, rush yds) | **UNKNOWN** (none saved) | **UNKNOWN** | 14 games | 14 games | 14 games | 1 game (JAX@BAL) |
| Rush+rec alt | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 14 games | 1 game |
| Alt game totals (Under) | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 1 game (CHI@SEA) | 1 game (JAX@BAL) |

So **train = Weeks 6-7** (Weeks 4-5 have no alt prices) and **OOS = Weeks 8-9** (effectively Week 8 plus one Week 9 game). I did not backfill Weeks 4-5 from the Odds API: historical alt props cost 10x per market per event (about 30 events x 3-4 markets x 10 = about 900-1,200 credits) against 940 credits above the 800 floor, and Blitz needs that budget for the Week 11 live freeze.

## Rules
- **Steady-volume gate:** receiving legs need average target share >= 15% and median >= 4 targets over the prior games. Rush and rush+rec legs need an RB with >= 60% of team carries in at least 3 of his last 4 games (the do-not-play rule). QB rushing is excluded. Passing yards are excluded. At least 3 prior games are required.
- **Defender gate:** a main-defender assignment is **UNVERIFIABLE historically**, so every receiving result is flagged UNGATED.
- **Floor:** alt line <= the player's 40th-percentile prior output (p25 also tested). For each player-market, take the highest such rung (best price).
- **Cushion (minimum-cushion rule):** cushion = the player's prior median minus the alt line. The grid was searched on **train only**, and the rule was frozen in `cushion_rule_frozen_train_wk6_7.json` before OOS scoring.
  - **Chosen for yards (rec, rush, rush+rec):** cushion >= max(25 yds, 100% of the line), so the line is at or below half the median and at least 25 yds under it.
  - **Chosen for receptions:** cushion >= max(2 catches, 50% of the line).
  - The search was monotone. Every safer rung was less negative, and **no cushion setting reached a positive margin in train**. The rule reduces losses; it does not create an edge.
  - For reference, Nabers 40+ (cleared by 4) would need a prior median of >= 80 yds under this rule. Otherwise the rule pushes the leg down the ladder.

## 1. Floor legs vs real price (hit / break-even, margin in points, ROI at price; 95% game-cluster bootstrap CI)
| rule | split | market | n | hit | BE | margin [CI] | ROI |
|---|---|---|---|---|---|---|---|
| floor<=p40, no cushion | train 6-7 | rec | 128 | 61.7 | 67.0 | -5.3 [-13.3, +2.0] | -9.1% |
| | train 6-7 | rec yds | 128 | 53.9 | 61.8 | -7.9 [-17.9, +1.4] | -15.1% |
| | train 6-7 | rush yds | 22 ⚠ | 54.5 | 59.7 | -5.1 | -4.6% |
| | train 6-7 | ALL | 278 | 57.6 | 64.1 | -6.5 [-14.4, +0.7] | -11.5% |
| | OOS 8-9 | rec | 68 | 60.3 | 68.3 | -8.0 [-20.0, +2.8] | -15.7% |
| | OOS 8-9 | rec yds | 68 | 54.4 | 64.7 | -10.2 [-18.5, -1.9] | -18.6% |
| | OOS 8-9 | rush yds | 13 ⚠ | 61.5 | 55.7 | +5.8 [-18.0, +29.3] | +6.0% |
| | OOS 8-9 | rush+rec | 12 ⚠ | 33.3 | 55.8 | -22.5 | -29.9% |
| | OOS 8-9 | ALL | 161 | 55.9 | 64.8 | -8.9 [-17.9, -0.1] | -16.2% |
| **floor<=p40 + cushion** | train 6-7 | rec | 96 | 83.3 | 85.9 | -2.6 [-8.7, +3.2] | -3.3% |
| | train 6-7 | rec yds | 88 | 84.1 | 84.4 | -0.3 [-7.2, +6.3] | -0.8% |
| | train 6-7 | rush yds | 18 ⚠ | 83.3 | 87.1 | -3.8 | -7.0% |
| | train 6-7 | ALL | 202 | 83.7 | 85.4 | -1.7 [-6.8, +3.0] | -2.5% |
| | OOS 8-9 | rec | 56 | 80.4 | 86.9 | -6.5 [-15.8, +1.3] | -8.1% |
| | OOS 8-9 | rec yds | 52 | 86.5 | 87.4 | -0.9 [-11.2, +7.7] | -1.0% |
| | OOS 8-9 | rush yds | 11 ⚠ | 81.8 | 84.1 | -2.3 | -8.9% |
| | OOS 8-9 | rush+rec | 7 ⚠ | 71.4 | 82.6 | -11.2 | -20.7% |
| | OOS 8-9 | ALL | 126 | 82.5 | 86.6 | -4.1 [-11.5, +2.9] | -5.9% |
| + cushion, FanDuel-priced only | train / OOS | ALL | 170 / 99 | 82.4 / 82.8 | 84.1 / 85.2 | -1.8 / -2.4 | -2.6% / -3.9% |

A floor at p25 instead of p40 (no cushion): train 68.4 vs 74.1 (-5.7, n=263); OOS 71.5 vs 74.3 (-2.8, n=151). Neither split is positive.
**NFL-75 readiness: no market passes** (no market has n>=30 with margin >= +3 and CI low > 0).

Breakdowns of the cushion legs flip sign between train and OOS, which looks like noise rather than signal:
- TE: train -15.4 (n=37), OOS +8.7 (n=33).
- WR: train +1.6 (n=136), OOS -9.7 (n=70).
- Break-even 80-90% price band: train -0.6 (n=72), OOS +7.1 (n=43).
These are not usable as selection rules yet.

## 2. Wide alt total unders
- **Real alt Under prices:** only 2 games (Wk8 CHI@SEA, Wk9 JAX@BAL). Both won at main+7, +10 and +14. **n=2. UNKNOWN for practical purposes.**
- **Hit rate without price** (main total from the inventory, Weeks 6-9; break-even UNKNOWN):

| final total below | train hit (n=28) | OOS hit (n=29) |
|---|---|---|
| main+7 | 71.4% | 79.3% |
| main+10 | 78.6% | 82.8% |
| main+14 | 89.3% | 86.2% |

  For comparison, the 2 real FanDuel quotes at main+14 implied break-evens of 87.8% and 92.3%. That looks roughly fairly priced, with no visible edge, but this is unproven.

## 3. 6-8 leg same-game slips (cushion legs, one leg per player, plus the alt total Under at main+10 when quoted)
- **Price is the independent product of leg prices.** Real FanDuel SGP prices are **UNKNOWN** (none saved). Correlation-adjusted SGP odds are usually shorter than the product, which would make these results worse.
- Few games produce 6+ qualifying legs: 6 train and 6 OOS games for 6-leggers, and 1 and 2 games for 7-leggers. No game produced 8.

| k | split | slips | wins | hit | median indep price | ROI at indep price |
|---|---|---|---|---|---|---|
| 6 | train 6-7 | 6 ⚠ | 4 | 66.7% | 2.29 (+129) | +44.0% |
| 6 | OOS 8-9 | 6 ⚠ | 3 | 50.0% | 2.05 (+105) | -8.9% |
| 7 | train / OOS | 1 / 2 ⚠ | 0 / 0 | 0% | 2.59 / 2.83 | -100% |

- Enumerating all 6-leg combos per game (cushion pool) gives a game-weighted hit of 66.7% in train and 38.1% OOS, with ROI at independent price of +44.0% and -27.7%.
- The no-cushion p40 pool (6-leg, about +950 independent) won 1 of 13 train games' combos and 0 of 8 OOS.
- Arithmetic check: an average cushion leg returns -2.5% to -5.9% at price, which compounds to roughly -14% to -31% over 6 legs if the legs were independent. **The style only wins long-run if same-game correlation is real and the SGP price does not already charge for it.** That cannot be tested without saved SGP prices.

## 4. Thin-clear diagnostic (p40 floor legs, yardage markets)
- Train: 118 losses out of 278 legs; 38 of those losses had cushion < 10 yds; 13 wins cleared by 5 yds or less.
- OOS: 71 losses out of 161; 20 losses had cushion < 10; 1 win cleared by 5 or less.
- Nabers-type thin legs are common, which is why the cushion rule cuts the loss rate so much (hit 58% -> 84%). The price moves with it, though, and that cancels most of the gain.

## Verdict
1. **Alt floors on steady-volume players are priced close to fair, minus vig.** At p40 floors they lose 6.5-8.9 points against break-even. The frozen cushion rule shrinks that to -1.7 (train) and -4.1 (OOS), so it is a loss limiter, not an edge.
2. **The best sub-slices (TE, the 80-90% band, OOS rush yds) all have n<30 or flip sign between splits.** None meets NFL-75.
3. **Rico's slip style can cash often** (6-leg cushion SGPs won 7 of 12 games across both splits), **but at independent prices the long-run ROI is negative or unproven.** The open variable is the real SGP price. Next step: save the FanDuel SGP quote for every built slip starting in Week 11 (no extra API credits, because it comes from the slip screen), so correlation pricing can be tested live in Weeks 10-12.
4. **Data gaps:** Weeks 4-5 alt prices UNKNOWN; Week 9 alt prices exist for 1 game only; alt totals exist for 2 games; historical defender assignments UNVERIFIABLE; SGP prices UNKNOWN; 597 rungs voided where the player had no touch and no snap record (2 of the graded floor legs).

## Caveats
- Multiple comparisons: about 40 grid cells x several markets.
- OOS is essentially one slate (Week 8).
- Median-of-books prices for non-FanDuel rungs are not executable prices.
- Bootstrap clusters on game, not week.
- Week 8-9 players with no touch/target and no snap data (snaps cover Weeks ≤7) are voided, not counted as losses. This may slightly flatter hit rates.

## Files
- Scripts: `a1_build.py`, `a2_score.py`, `a3_extra.py`.
- Frozen rule: `cushion_rule_frozen_train_wk6_7.json`.
- Aggregate results: `results_*.csv`, `meta.json`.
- Leg-level files with book prices stay off this public repo, at `/workspace/research/alt_floor_sgp_2026-11-13/LEGLEVEL_*.csv`.
