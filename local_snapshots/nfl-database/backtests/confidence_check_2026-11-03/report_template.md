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
@@MAIN@@
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
@@ROI@@
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
@@COV@@
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
@@CAL@@
