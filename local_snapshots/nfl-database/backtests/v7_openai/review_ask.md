## A) PLAN

**Status and hypothesis.** This is a locked development backtest, not a fresh confirmatory test: Weeks 1–8 have already informed prior work. Hypothesis: a strongly regularized, market-anchored adjustment using only earlier player-game logs improves probability accuracy and identifies profitable singles. I ignore the existing simulator, QB streak, depth-chart, and slip rules.

**Universe and deduplication.** Use FanDuel only, avoiding best-book execution assumptions and enabling FanDuel slip grading. Keep its latest valid pre-kick quote per `(game, player, market, side, line)`; ties favor the better price. Modeling requires both sides at the identical line. Normalize their implied probabilities to remove vig. Exclude missing player IDs from modeling. The broader baseline retains all priced FanDuel rush unders, including one-sided quotes.

**Probability method.** Predict over probability with a market-logit offset plus ridge-penalized logistic coefficients, including a penalized intercept. Fixed penalty: 20 on summed negative log-likelihood. Features: last-four average yards relative to line, last-two versus historical yardage trend, last-four rushing/target opportunity share, and prior-game count. All logs must have `week < target week`. Scaling uses training data only; standardized features are clipped to ±5. Fit only over contracts, avoiding duplicated complementary observations. Under probability is the complement. With fewer than 30 graded training contracts, use market probabilities unchanged.

**Walk-forward and selection.** Weeks 3–4 warm up; predict Weeks 5–8, refitting on earlier weeks only. No tuning or retrospective disabling. Select legs with probability edge ≥3 percentage points and modeled expected return ≥2%. Retain at most one selected leg per player per game, ranked by edge, then expected return. Stake $10 per single. Pushes and missing outcomes refund stakes and do not enter binary scoring.

**Slips.** Separately stake $10 per slip. Deterministically attempt five distinct slips weekly, preferring four legs, otherwise three. Each slip has distinct players and games; overlap between slips is permitted and reported. Use selected singles only; insufficient qualifying legs means fewer slips. FanDuel payout is the product of decimal prices, with pushes/voids removed. Also report a **hypothetical PrizePicks Power** grading at these same lines: 3-pick 6x, 4-pick 10x total return. These are not saved PrizePicks offers. For this hypothetical comparison, any push/void refunds the whole slip.

**Metrics and comparisons.** Report weekly/market/side singles results, hit rate, profit, ROI on all stakes including refunded stakes, Brier and log-loss against de-vigged market on identical graded legs, and slips by week. Universe probability scoring uses one over per paired contract. Compare selected singles with both eligible paired FanDuel rush unders and all priced FanDuel rush unders in Weeks 5–8. The historical +2.8% baseline covers different weeks/books and is context, not a like-for-like hurdle.

**Leakage and success.** Features never access outcomes or supplied `prior_*` fields. Assert valid snapshot timing, earlier-week log access, and earlier-week training. Success requires positive selected-single ROI, ROI exceeding **both** rush-under baselines, and lower universe Brier than market. Empty comparisons fail. Slips are secondary, not success criteria. Report counts without claiming statistical proof: four evaluation weeks, overlapping contracts, and reused slip legs make the effective sample small.

## B) CODE — `v7.py`



# RESULTS of your locked v7 (run on box, 1 approved crash fix)
# v7 locked development backtest

**Predeclared result: FAIL**

Weeks 5–8 only. $10 flat stakes; ROI includes refunded stakes. Brier/log-loss exclude voids and pushes; universe scores only overs. Paired contracts have both FanDuel sides at the identical line. No CLV is available. This is not an independent confirmatory sample.

Fixed model: market-logit offset; ridge 20; minimum 30 training overs; prior-log features; train-only scaling/clipping; edge >= .03, EV >= .02.

## Baseline comparison and probability scores

| strategy | bets | graded | wins | pushes | voids | hit | profit | roi | p_brier | p_logloss | q_brier | q_logloss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Selected singles | 505 | 475 | 238 | 30 | 0.5011 | -256.8464 | -0.0509 | 0.2581 | 0.7099 | 0.2503 | 0.6938 |
| Eligible rush unders | 346 | 325 | 175 | 21 | 0.5385 | 40.9665 | 0.0118 | 0.2515 | 0.6963 | 0.2492 | 0.6915 |
| All priced FD rush unders | 346 | 325 | 175 | 21 | 0.5385 | 40.9665 | 0.0118 | nan | nan | nan | nan |
| Paired universe: over scoring | 1230 | 1163 | 558 | 67 | 0.4798 | -1100.9030 | -0.0895 | 0.2531 | 0.6996 | 0.2498 | 0.6927 |

## Selected: by week

| group | bets | graded | wins | pushes | voids | hit | profit | roi | p_brier | p_logloss | q_brier | q_logloss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 119 | 111 | 49 | 8 | 0.4414 | -187.0418 | -0.1572 | 0.2719 | 0.7381 | 0.2499 | 0.6930 |
| 6 | 94 | 89 | 47 | 5 | 0.5281 | 0.3010 | 0.0003 | 0.2493 | 0.6916 | 0.2512 | 0.6955 |
| 7 | 147 | 143 | 76 | 4 | 0.5315 | 4.4565 | 0.0030 | 0.2539 | 0.7013 | 0.2503 | 0.6938 |
| 8 | 145 | 132 | 66 | 13 | 0.5000 | -74.5621 | -0.0514 | 0.2572 | 0.7078 | 0.2501 | 0.6933 |

## Selected: by market

| group | bets | graded | wins | pushes | voids | hit | profit | roi | p_brier | p_logloss | q_brier | q_logloss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| recyds | 318 | 296 | 144 | 22 | 0.4865 | -239.1301 | -0.0752 | 0.2597 | 0.7130 | 0.2506 | 0.6943 |
| rushrecyds | 97 | 96 | 51 | 1 | 0.5312 | 0.6023 | 0.0006 | 0.2558 | 0.7053 | 0.2498 | 0.6928 |
| rushyds | 90 | 83 | 43 | 7 | 0.5181 | -18.3186 | -0.0204 | 0.2552 | 0.7040 | 0.2500 | 0.6932 |

## Selected: by side

| group | bets | graded | wins | pushes | voids | hit | profit | roi | p_brier | p_logloss | q_brier | q_logloss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| over | 145 | 127 | 62 | 18 | 0.4882 | -94.7938 | -0.0654 | 0.2648 | 0.7238 | 0.2512 | 0.6956 |
| under | 360 | 348 | 176 | 12 | 0.5057 | -162.0526 | -0.0450 | 0.2557 | 0.7048 | 0.2500 | 0.6931 |

## Slips by week

| week | slips | unique_legs | reused_slots | stake | fd_profit | pp_profit | fd_roi | pp_roi |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 5 | 8 | 12 | 50.0000 | -50.0000 | -40.0000 | -1.0000 | -0.8000 |
| 6 | 5 | 8 | 12 | 50.0000 | -11.5131 | -20.0000 | -0.2303 | -0.4000 |
| 7 | 5 | 8 | 12 | 50.0000 | -50.0000 | -50.0000 | -1.0000 | -1.0000 |
| 8 | 5 | 8 | 12 | 50.0000 | -50.0000 | -50.0000 | -1.0000 | -1.0000 |

FanDuel uses product odds after removing void/push legs. PP is a hypothetical same-line Power assumption: 3 picks 6x, 4 picks 10x; any void/push refunds the entire PP slip. Slips overlap and are not independent. Singles and slip bankrolls are separate.

Historical rush-under +2.8% is not directly comparable to this FD-only Weeks 5–8 test. Small, dependent development samples cannot prove edge.


# Our comparators (priced Wk3-8, all books best-quote): v6 READS 66-90 42.3% ROI -19.1%, slips 0/30; v6 GATED 49-69 41.5% -21.6%, slips 1/26; rush-under baseline 296-229 56.4% +2.8%.
Note: p_* = your model, q_* = de-vigged market on same legs. Spec asked ~5 slips per game DAY; you built 5 per week from 8 unique legs (heavy reuse).
# Ask
1) Honest read (<=300 words): what worked, what failed, why; is anything here signal or noise.
2) Design v7.1, LOCKED to run forward from Week 10 as a shadow test (no tuning on Weeks 1-8 beyond what you justify from first principles). Give plan (<=400 words, pre-declared success criterion, minimum sample before any judgment, weekly ledger fields) and one ```python block `v7_1.py` (<=200 lines) that takes a week number and a lines CSV of the same schema (plus player_games CSV) and writes out/v7_1_week{W}_picks.csv with locked picks (sha256), and a --grade mode that grades a finished week. Must reuse the same as-of guards.
