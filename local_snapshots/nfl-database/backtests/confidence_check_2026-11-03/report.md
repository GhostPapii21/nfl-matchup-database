# NFL confidence check — Brier / log loss vs market (Tue Nov 3 2026, TEST ONLY)

Nothing was bet or sent. **No Odds API credits were spent** (0 pulls); every price is from data already saved in the repo.
Originals were not edited: the sim code here is in scratch copies under `engines/` (patch list below).

## Plain verdict
- **All 9 model versions score worse than the market's no-vig probabilities.** All 9 also score worse than a flat 50% guess (Brier 0.2500).
  Every Brier gap vs the market has a game-clustered 95% CI that sits fully above zero.
- **No shrink is worse than the market:** Brier +0.024 and log loss +0.065 to +0.069, on all three sims. It is also clearly worse than the old 30% shrink, which itself is +0.012 worse than the market.
- **Full-strength oppadj (1.0) is worse still**, both vs the market (+0.029) and vs half strength (another +0.004 to +0.005 Brier on top of no-shrink), on all three sims.
- The sims barely differ from each other. sim_v5, sim_v6 and sim_v6_fix are within about 0.001 Brier of one another in every version.
- **Why:** the models have almost no resolution. When the model says 70–80% or 80%+, the leg hits about 45–55%, about the same as its 50–55% bin. Removing the shrink just stretches that noise further from 50%.
  The NBA result had the same shape (BetGuru: no-shrink Brier 0.289 vs market 0.248, and full matchup factor worse).

### Recommendation (applying the task's rule)
1. **Keep oppadj at half strength (0.5).** Full strength scores worse than the market, and worse than half strength, on every sim.
   Production `tools/sim_v6.py` and Thursday's `runs/2026-11-05_shared_src/sim_v5.py` currently run it at 1.0 (phase3 commit 6322cc5). Reverting is a code change under the edit hold, so it is listed here and not made.
2. **FLAG FOR RICO:** no-shrink scores worse than the market (and worse than the old shrink) on every sim. Under Rico's Nov 2, 9:13 PM ET rule this is **his call. Nothing is changed without his OK.**
3. Context for Rico, not a rule change: even the old shrink is worse than the market. No version showed +3 edges that make money. Flat $10 on every +3 leg loses 3.7–5.8% under every version.

## Main table (same 2,411 legs in all 9 rows; Brier/log loss scored on the Over side; log loss clips p to [0.001, 0.999])
| sim | version | N legs | Brier | log loss | market Brier | market log loss | Δ Brier vs mkt (95% CI, game-clustered) |
|---|---|---|---|---|---|---|---|
| sim_v5 | V1 old (30% shrink, opp 0.5) | 2411 | 0.2602 | 0.7159 | 0.2481 | 0.6894 | +0.0121 (+0.0057 to +0.0186) |
| sim_v5 | V2 no shrink, opp 0.5 | 2411 | 0.2730 | 0.7581 | 0.2481 | 0.6894 | +0.0249 (+0.0157 to +0.0334) |
| sim_v5 | V3 no shrink, opp 1.0 | 2411 | 0.2770 | 0.7716 | 0.2481 | 0.6894 | +0.0289 (+0.0189 to +0.0388) |
| sim_v6 | V1 old (30% shrink, opp 0.5) | 2411 | 0.2600 | 0.7154 | 0.2481 | 0.6894 | +0.0119 (+0.0056 to +0.0183) |
| sim_v6 | V2 no shrink, opp 0.5 | 2411 | 0.2724 | 0.7557 | 0.2481 | 0.6894 | +0.0243 (+0.0156 to +0.0331) |
| sim_v6 | V3 no shrink, opp 1.0 | 2411 | 0.2767 | 0.7690 | 0.2481 | 0.6894 | +0.0286 (+0.0183 to +0.0388) |
| sim_v6_fix | V1 old (30% shrink, opp 0.5) | 2411 | 0.2600 | 0.7152 | 0.2481 | 0.6894 | +0.0119 (+0.0055 to +0.0182) |
| sim_v6_fix | V2 no shrink, opp 0.5 | 2411 | 0.2723 | 0.7547 | 0.2481 | 0.6894 | +0.0241 (+0.0156 to +0.0329) |
| sim_v6_fix | V3 no shrink, opp 1.0 | 2411 | 0.2771 | 0.7699 | 0.2481 | 0.6894 | +0.0290 (+0.0194 to +0.0390) |

Reference: a constant 50% gives Brier 0.2500 and log loss 0.6931. The actual Over hit rate on these legs is 48.4%. The model's mean Over p is 0.43–0.48 against a market mean of 0.497, so the models lean Under.

**Brier by week, sim_v6** (market in brackets):

- W3 0.278 / 0.301 / 0.308 [0.250]
- W4 0.263 / 0.279 / 0.286 [0.250]
- W5 0.260 / 0.272 / 0.275 [0.250]
- W6 0.254 / 0.263 / 0.267 [0.248]
- W7 0.250 / 0.257 / 0.259 [0.245]
- W8 0.264 / 0.277 / 0.279 [0.248]
- MNF 0.252 / 0.257 / 0.283 [0.250] (29 legs)

The values are V1 / V2 / V3. The model loses to the market in every week under every version.

**Brier by market, sim_v6, V1 / V2 / V3** [market]:

- passyds 0.268 / 0.283 / 0.292 [0.248]
- rec 0.249 / 0.256 / 0.257 [0.243]
- recyds 0.262 / 0.275 / 0.281 [0.250]
- rushrec 0.269 / 0.286 / 0.294 [0.250]
- rushyds 0.261 / 0.276 / 0.276 [0.249]

Rushyds V2 = V3 in sim_v5/v6 because oppadj only touches the receiving and passing factors there. The rushing YPC opponent factor is already full strength in every version. Files: `brier_by_week.csv`, `brier_by_market.csv`.

Cross-check vs the earlier Weeks 6–8 replay (model 0.267 vs market 0.247): this run on W6–8 gives sim_v6 V3 0.259–0.279 vs market 0.245–0.248. Same direction, similar size.

## Flat $10 on every leg clearing +3 pts vs no-vig (the side with model p − no-vig ≥ 0.03; price = the saved book price for that side, FanDuel when quoted)
| sim | version | bets | W–L | hit | P/L ($10 flat) | ROI | mean model p (bet side) |
|---|---|---|---|---|---|---|---|
| sim_v5 | V1 old (30% shrink, opp 0.5) | 1929 | 965–964 | 50.0% | -1,044.38 | -5.4% | 0.607 |
| sim_v5 | V2 no shrink, opp 0.5 | 2062 | 1057–1005 | 51.3% | -753.13 | -3.7% | 0.649 |
| sim_v5 | V3 no shrink, opp 1.0 | 2091 | 1056–1035 | 50.5% | -1,081.92 | -5.2% | 0.659 |
| sim_v6 | V1 old (30% shrink, opp 0.5) | 1916 | 965–951 | 50.4% | -902.82 | -4.7% | 0.605 |
| sim_v6 | V2 no shrink, opp 0.5 | 2054 | 1046–1008 | 50.9% | -865.40 | -4.2% | 0.646 |
| sim_v6 | V3 no shrink, opp 1.0 | 2081 | 1043–1038 | 50.1% | -1,210.92 | -5.8% | 0.656 |
| sim_v6_fix | V1 old (30% shrink, opp 0.5) | 1898 | 946–952 | 49.8% | -1,084.20 | -5.7% | 0.605 |
| sim_v6_fix | V2 no shrink, opp 0.5 | 2046 | 1039–1007 | 50.8% | -949.09 | -4.6% | 0.646 |
| sim_v6_fix | V3 no shrink, opp 1.0 | 2077 | 1045–1032 | 50.3% | -1,147.51 | -5.5% | 0.657 |

- The models disagree with the market by 3+ points on 80–87% of legs: the mean |model − market| is 9 pts with the shrink and 13–14 pts without it. That alone says the numbers aren't market-grade.
- V2 (no shrink, opp 0.5) loses the least in all three sims. It still loses 3.7–4.6% and hits 50.8–51.3%.
- Unders hit 51–52% and overs 48–50%; both sides lose money. Week 8 is the worst week for every version (−$341 to −$493). Detail is in `plus3_bets.csv`.

## Calibration highlights (full tables for all 9 rows below and in `calibration.md`)
- **sim_v6 V2 (no shrink, opp 0.5), model-favored side:**
  - 50–55%: 49.7% actual (n 602)
  - 55–60%: 53.7%
  - 60–65%: 50.6%
  - 65–70%: 54.1%
  - 70–80%: 49.3% (n 371)
  - 80%+: 52.5% (n 162; mean prediction 87%)
- **sim_v6 V3 (opp 1.0):**
  - 70–80%: 50.4% (n 413)
  - 80%+: 50.2% (n 201; mean prediction 87.5%)
- **Over-side 0–40% bin:** the model predicts 28–33% but overs hit 47–48% in every version, so the model is much too low on overs it dislikes.
- **The old shrink is the least overconfident, and it still has no lift:** 65–70% → 49.8%, 70–80% → 51.4%.
- The market's own no-vig stays within about 49–51% in every bin. The legs the model is sure about are coin flips that the market priced as coin flips.

## Data coverage (real prices; legs used before the all-6-runs intersection)
| week | passyds | rec | recyds | rushrec | rushyds | games |
|---|---|---|---|---|---|---|
| 3 | 0 | 0 | 186 | 48 | 96 | 16 |
| 4 | 0 | 0 | 190 | 47 | 95 | 16 |
| 5 | 0 | 0 | 172 | 44 | 89 | 15 |
| 6 | 27 | 173 | 173 | 46 | 83 | 14 |
| 7 | 28 | 171 | 172 | 42 | 80 | 14 |
| 8 | 26 | 152 | 155 | 41 | 83 | 13 |
| MNF CHI@SEA | 2 | 11 | 11 | 0 | 5 | 1 |

- **Weeks 1–2: no real prices are saved, so they are not covered.** I found no Odds API snapshot for them anywhere in the repo.
- **Weeks 3–5:** only rec yds, rush yds and rush+rec yds main lines exist (from `backtests/yardage_markets_wk3_8/raw`, pulled this morning). There are no receptions or passing yards prices.
- **Weeks 6–8:** passyds, rec, recyds and rushyds main lines (from `current_rules_wk6_8` real_lines), plus rush+rec yds from the yardage raw.
- **MNF CHI@SEA Nov 2:** 29 main-line props (from `rulebook_replay_wk6_8/mnf_lines.csv`). Actuals come from the ESPN box in that replay.
- **What counts as a leg:**
  - One main line per player-market, with no alts.
  - Half-point lines only, so there are no pushes.
  - The player must be active (graded from nflverse pbp, `runs/2026-11-02_shared_src`).
- **Price data:**
  - Snapshots were taken 29–39 min before kickoff (median 34 min). These are near-close lines, not exact closing lines.
  - No-vig = the mean two-way multiplicative no-vig across books quoting the modal line.
- **Leg counts:**
  - 2,448 legs were built. 43 quotes could not be name-matched and were dropped.
  - **2,411 legs** had a valid sim in all 6 engine × oppadj runs. The excluded legs are sims that error on thin pre-cutoff history (mostly Week 3).
  - Legs are correlated within games, so the CIs are bootstrapped by game (89 games).

## Method
- **Three versions:**
  - V1 = old rules: oppadj 0.5, then p' = 0.5 + 0.7(p − 0.5) on the 3-model average.
  - V2 = oppadj 0.5 with no shrink.
  - V3 = oppadj 1.0 with no shrink.
  - Model p is the mean of the mc, bias and gr P(stat ≥ line), the same as the gate's `avg(p)`.
- **Leak-free inputs:**
  - Every engine sees only pbp with game_date before the first game of week W (MNF: before 2026-11-02).
  - Spreads are the nflverse pregame `spread_line`.
  - sim_v6 and sim_v6_fix per-market multipliers were **refit walk-forward** with each engine's own `fit()`. The fit used its saved residual file restricted to weeks < W: none for W3–4, W4 for W5, and so on, up to W4–7 for W8 and MNF.
  - The committed `sim_v6_calib.json` files were not used, because they were fit on Week 4–7 outcomes inside the test window.
- **Scratch patches in `engines/`:**
  - oppadj strength comes from env `CC_OPP`.
  - sim_v6_fix's bias-model `BIAS_OPP` follows `CC_OPP` too, so V2 is its shipped 0.5 and V3 is 1.0.
  - sim_v5 gets a date cutoff and a gsis lookup. Its flat bias haircut (.92/.97/.95) is kept as written.
  - No other logic changed. sim_v5's base is `runs/2026-11-01_shared_src/sim_v5.py`, whose original oppadj default is 0.5.
- **Simulation size:** 20,000 sims per model per leg with a fixed seed. Monte-Carlo error on p is about ±0.004, which is negligible against the 0.012–0.029 Brier gaps.
- **Not modeled** (same as the prior replays): `current_qb` filter, RB script/promotion boosts, weather and inactives. This is the raw sim layer the gate's edge math uses.
- **Reproduce:** `python3 build_legs.py`, then `run_sims.py <engine> <opp> <week>` for each job (see `sims.log`), then `python3 analyze.py` and `python3 make_report.py`.

## Caveats
- The Odds API balance is lower than the shared notes say. `backtests/yardage_markets_wk3_8/raw/credits.log` shows the Yardage pull this morning went from 5,449 to **3,623 remaining** (1,826 used, ending 06:47 ET). This check used 0 credits.
- Week 1–2 coverage is zero, and Weeks 3–5 have yardage markets only. Passing yards is just 83 legs, and passyds is already off slips per Rico.
- No closing-line feed exists. Prices are about T-35 min snapshots.

## Full calibration tables

### sim_v5 — V1 old (30% shrink, opp 0.5)
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 694 | 0.326 | 0.478 | 0.491 |
| 40-50 | 894 | 0.451 | 0.481 | 0.497 |
| 50-55 | 350 | 0.525 | 0.486 | 0.500 |
| 55-60 | 261 | 0.572 | 0.513 | 0.506 |
| 60-65 | 124 | 0.621 | 0.500 | 0.503 |
| 65-70 | 56 | 0.675 | 0.518 | 0.512 |
| 70-80 | 30 | 0.731 | 0.533 | 0.510 |
| 80+ | 2 | 0.811 | 0.000 | 0.501 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 812 | 0.525 | 0.500 | 0.501 |
| 55-60 | 693 | 0.573 | 0.522 | 0.505 |
| 60-65 | 416 | 0.624 | 0.524 | 0.507 |
| 65-70 | 274 | 0.674 | 0.496 | 0.509 |
| 70-80 | 187 | 0.739 | 0.524 | 0.510 |
| 80+ | 29 | 0.830 | 0.586 | 0.510 |

### sim_v5 — V2 no shrink, opp 0.5
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 938 | 0.285 | 0.471 | 0.491 |
| 40-50 | 650 | 0.449 | 0.492 | 0.498 |
| 50-55 | 242 | 0.524 | 0.479 | 0.499 |
| 55-60 | 228 | 0.573 | 0.522 | 0.505 |
| 60-65 | 152 | 0.620 | 0.474 | 0.503 |
| 65-70 | 99 | 0.670 | 0.515 | 0.506 |
| 70-80 | 75 | 0.745 | 0.520 | 0.509 |
| 80+ | 27 | 0.845 | 0.519 | 0.507 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 567 | 0.525 | 0.504 | 0.501 |
| 55-60 | 553 | 0.574 | 0.505 | 0.503 |
| 60-65 | 413 | 0.621 | 0.518 | 0.506 |
| 65-70 | 319 | 0.673 | 0.536 | 0.508 |
| 70-80 | 373 | 0.744 | 0.501 | 0.509 |
| 80+ | 186 | 0.869 | 0.538 | 0.510 |

### sim_v5 — V3 no shrink, opp 1.0
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 999 | 0.276 | 0.478 | 0.492 |
| 40-50 | 561 | 0.449 | 0.501 | 0.499 |
| 50-55 | 249 | 0.524 | 0.438 | 0.497 |
| 55-60 | 216 | 0.571 | 0.523 | 0.504 |
| 60-65 | 165 | 0.622 | 0.461 | 0.507 |
| 65-70 | 106 | 0.671 | 0.481 | 0.503 |
| 70-80 | 85 | 0.744 | 0.588 | 0.509 |
| 80+ | 30 | 0.850 | 0.500 | 0.510 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 531 | 0.526 | 0.460 | 0.499 |
| 55-60 | 495 | 0.574 | 0.521 | 0.503 |
| 60-65 | 442 | 0.622 | 0.489 | 0.506 |
| 65-70 | 309 | 0.672 | 0.540 | 0.508 |
| 70-80 | 403 | 0.747 | 0.519 | 0.508 |
| 80+ | 231 | 0.873 | 0.524 | 0.509 |

### sim_v6 — V1 old (30% shrink, opp 0.5)
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 601 | 0.329 | 0.473 | 0.490 |
| 40-50 | 801 | 0.455 | 0.478 | 0.496 |
| 50-55 | 397 | 0.525 | 0.501 | 0.499 |
| 55-60 | 300 | 0.575 | 0.500 | 0.505 |
| 60-65 | 184 | 0.622 | 0.527 | 0.504 |
| 65-70 | 78 | 0.674 | 0.474 | 0.509 |
| 70-80 | 48 | 0.733 | 0.479 | 0.507 |
| 80+ | 2 | 0.816 | 0.000 | 0.501 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 843 | 0.525 | 0.510 | 0.500 |
| 55-60 | 655 | 0.573 | 0.515 | 0.506 |
| 60-65 | 442 | 0.622 | 0.527 | 0.508 |
| 65-70 | 269 | 0.672 | 0.498 | 0.509 |
| 70-80 | 175 | 0.737 | 0.514 | 0.510 |
| 80+ | 27 | 0.830 | 0.630 | 0.511 |

### sim_v6 — V2 no shrink, opp 0.5
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 780 | 0.285 | 0.474 | 0.490 |
| 40-50 | 622 | 0.451 | 0.477 | 0.497 |
| 50-55 | 273 | 0.524 | 0.469 | 0.500 |
| 55-60 | 245 | 0.573 | 0.551 | 0.502 |
| 60-65 | 199 | 0.623 | 0.492 | 0.505 |
| 65-70 | 138 | 0.672 | 0.529 | 0.502 |
| 70-80 | 119 | 0.744 | 0.454 | 0.508 |
| 80+ | 35 | 0.857 | 0.514 | 0.509 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 602 | 0.525 | 0.497 | 0.501 |
| 55-60 | 538 | 0.574 | 0.537 | 0.503 |
| 60-65 | 405 | 0.623 | 0.506 | 0.506 |
| 65-70 | 333 | 0.672 | 0.541 | 0.508 |
| 70-80 | 371 | 0.744 | 0.493 | 0.510 |
| 80+ | 162 | 0.872 | 0.525 | 0.510 |

### sim_v6 — V3 no shrink, opp 1.0
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 839 | 0.276 | 0.480 | 0.491 |
| 40-50 | 577 | 0.450 | 0.489 | 0.498 |
| 50-55 | 241 | 0.523 | 0.469 | 0.499 |
| 55-60 | 245 | 0.573 | 0.494 | 0.500 |
| 60-65 | 189 | 0.624 | 0.481 | 0.507 |
| 65-70 | 146 | 0.673 | 0.548 | 0.504 |
| 70-80 | 132 | 0.744 | 0.492 | 0.506 |
| 80+ | 42 | 0.856 | 0.429 | 0.508 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 531 | 0.524 | 0.488 | 0.500 |
| 55-60 | 532 | 0.574 | 0.508 | 0.502 |
| 60-65 | 416 | 0.624 | 0.495 | 0.506 |
| 65-70 | 318 | 0.674 | 0.550 | 0.508 |
| 70-80 | 413 | 0.746 | 0.504 | 0.509 |
| 80+ | 201 | 0.875 | 0.502 | 0.509 |

### sim_v6_fix — V1 old (30% shrink, opp 0.5)
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 599 | 0.330 | 0.477 | 0.490 |
| 40-50 | 809 | 0.455 | 0.477 | 0.496 |
| 50-55 | 391 | 0.524 | 0.499 | 0.499 |
| 55-60 | 310 | 0.574 | 0.510 | 0.503 |
| 60-65 | 179 | 0.623 | 0.497 | 0.505 |
| 65-70 | 75 | 0.675 | 0.480 | 0.509 |
| 70-80 | 46 | 0.733 | 0.500 | 0.507 |
| 80+ | 2 | 0.817 | 0.000 | 0.501 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 856 | 0.524 | 0.512 | 0.500 |
| 55-60 | 654 | 0.573 | 0.517 | 0.505 |
| 60-65 | 454 | 0.624 | 0.504 | 0.508 |
| 65-70 | 252 | 0.673 | 0.504 | 0.509 |
| 70-80 | 169 | 0.737 | 0.527 | 0.510 |
| 80+ | 26 | 0.831 | 0.615 | 0.511 |

### sim_v6_fix — V2 no shrink, opp 0.5
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 792 | 0.287 | 0.477 | 0.490 |
| 40-50 | 616 | 0.453 | 0.477 | 0.498 |
| 50-55 | 277 | 0.524 | 0.477 | 0.499 |
| 55-60 | 246 | 0.573 | 0.508 | 0.501 |
| 60-65 | 198 | 0.623 | 0.545 | 0.504 |
| 65-70 | 135 | 0.673 | 0.489 | 0.509 |
| 70-80 | 112 | 0.746 | 0.473 | 0.506 |
| 80+ | 35 | 0.855 | 0.486 | 0.509 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 611 | 0.525 | 0.507 | 0.500 |
| 55-60 | 528 | 0.573 | 0.509 | 0.502 |
| 60-65 | 415 | 0.623 | 0.540 | 0.506 |
| 65-70 | 333 | 0.674 | 0.505 | 0.510 |
| 70-80 | 364 | 0.744 | 0.495 | 0.508 |
| 80+ | 160 | 0.870 | 0.537 | 0.511 |

### sim_v6_fix — V3 no shrink, opp 1.0
Over-side probability bins:

| bin | n | mean pred | actual hit | market nv |
|---|---|---|---|---|
| 0-40 | 855 | 0.277 | 0.480 | 0.491 |
| 40-50 | 574 | 0.452 | 0.488 | 0.499 |
| 50-55 | 234 | 0.523 | 0.479 | 0.498 |
| 55-60 | 236 | 0.574 | 0.496 | 0.500 |
| 60-65 | 193 | 0.623 | 0.477 | 0.507 |
| 65-70 | 140 | 0.672 | 0.529 | 0.503 |
| 70-80 | 137 | 0.743 | 0.511 | 0.507 |
| 80+ | 42 | 0.858 | 0.429 | 0.509 |

Model-favored side (prob of the side the model leans):

| bin | n | mean pred | actual hit | market nv (same side) |
|---|---|---|---|---|
| 50-55 | 533 | 0.524 | 0.492 | 0.500 |
| 55-60 | 511 | 0.574 | 0.511 | 0.501 |
| 60-65 | 421 | 0.623 | 0.494 | 0.508 |
| 65-70 | 315 | 0.672 | 0.540 | 0.507 |
| 70-80 | 424 | 0.743 | 0.507 | 0.509 |
| 80+ | 207 | 0.874 | 0.512 | 0.509 |

