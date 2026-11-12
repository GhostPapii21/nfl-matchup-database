# OpenAI response (gpt-5.5-2026-04-23, reasoning low (10k TPM cap))

## Executive verdict

- Your current evidence says **the market is beating the model**, not just by ROI but by **probability quality**: every sim has worse Brier than market and coin flip; rulebook passed legs hit 48–52% while model claims ~67%; parlays crater.
- The biggest failure is not one bad rule. It is **experimental invalidity**: small samples, after-the-fact rule edits, approximated unavailable data, possible LLM hindsight leakage, and selecting on noisy backtest pockets.
- Under your constraints, the goal should shift from “find 3–4 leg parlay winners” to: **build a leakage-proof, CLV-first single-leg research loop**. Parlays come later, only from legs with demonstrated closing-line edge and calibrated probabilities.

---

# 1. Statistical design fix list

## Sample size / power

### Singles at -110

Break-even at -110 is **52.38%** before any market movement/slippage.

Approximate legs needed to detect true edge versus 52.38% with 80% power, two-sided 5% alpha:

| True hit rate | Edge over -110 breakeven | Legs needed, rough |
|---:|---:|---:|
| 55% | +2.6 pts | ~2,800–3,000 legs |
| 56% | +3.6 pts | ~1,500–1,700 legs |
| 57% | +4.6 pts | ~900–1,000 legs |
| 58% | +5.6 pts | ~600–700 legs |
| 60% | +7.6 pts | ~325–400 legs |

Your samples — 34 legs, 293 legs, 463 legs, 50-ish holdout legs — are **far too small** to validate a modest real edge. They can falsify huge overconfidence, though, and they already do.

### Parlays

For independent -110 legs:

- 3-leg parlay break-even win rate is roughly **14.4%**.
- 4-leg parlay break-even win rate is roughly **7.5%**.
- If each leg is truly 55%, independent 3-leg win rate is **16.6%**.
- If each leg is truly 57%, independent 3-leg win rate is **18.5%**.
- If each leg is truly 55%, independent 4-leg win rate is **9.2%**.

But with correlated legs, stale prices, alt pricing, and model overconfidence, effective edge evaporates fast.

Roughly, to prove a 3-leg parlay improves from 14.4% to 17–18%, you may need **700–1,500+ slips**, and more if legs are correlated or selection rules change. So current slip results are directionally useful, not conclusive — but 0/8, 4/29, 20/245 are not encouraging.

## Overfitting from repeated rule tweaks

Current process has severe “garden of forking paths” risk:

- Rules are changed after looking at outcomes.
- Failed gates are relaxed or proxied.
- New tags like `SCHEME_EDGE`, `PRO_EDGE`, `ZONE_MOF`, depth rules, mirror overs, etc. are evaluated after exploratory discovery.
- Holdout sets are reused in discussions, postmortems, and prompt development, so they cease being true holdouts.

Fix:

- Freeze a **versioned protocol** before the week starts.
- Record all candidate legs, rejected legs, lines, prices, model probabilities, reasons, timestamps.
- Do not change rule thresholds intra-week.
- Use **pre-registered evaluation windows**:
  - Exploration: weeks A–B.
  - Calibration: weeks C–D.
  - Blind test: weeks E–F.
- Once a blind week is analyzed manually, it cannot be reused as blind data.

## Strict LLM-leakage protocol

Your v5 holdout result is not reliable until fully masked. The audit is helpful but insufficient.

Required protocol:

- LLM prompt receives only:
  - Data with timestamps before kickoff.
  - No final scores.
  - No post-game stats.
  - No “week result” filenames.
  - No graded file paths.
  - No team/player aliases that can let the model infer famous results if using a broadly knowledgeable model.
- Use **masked IDs** for teams/players/games during backtests:
  - `TEAM_A`, `TEAM_B`, `PLAYER_17`.
  - Provide only pregame features.
- Remove calendar clues where possible:
  - Avoid exact dates, broadcast windows, “Week 8 MNF CHI@SEA,” etc.
- Make LLM output machine-readable:
  - probability, side, confidence, kill conditions, features used.
- No postmortem files in retrieval context.
- No analyst who has seen results should perform manual replacement, tie-breaking, or “mechanical” choices unless the procedure is deterministic and code-locked.
- Keep a **leakage manifest** per run:
  - prompt hash,
  - input file hash,
  - output hash,
  - model name,
  - timestamp,
  - permitted data cutoff.

Where I’m unsure: I cannot know whether Grok memorized or inferred specific 2026 results. The clean direct-answer tests reduce concern but do not eliminate leakage. Masked rerun is the real test.

## CLV as primary metric

Switch primary score from hit rate/ROI to **closing-line value**.

Track for every leg:

- Open/book line and price at pick time.
- Consensus no-vig fair probability at pick time.
- Same market close line and close price.
- Whether the side beat close:
  - Over 45.5 taken, closes 48.5 = good CLV.
  - Under 45.5 taken, closes 42.5 = good CLV.
- Price CLV:
  - Took -110, closes -135 same line = good.
- No-vig implied probability movement.

Primary metrics:

- Average line CLV.
- Average no-vig probability CLV.
- % legs beating close.
- Calibration versus closing no-vig.
- ROI is secondary until sample is large.

If you cannot pull full history, save live snapshots religiously going forward.

## Calibration

Your model probabilities are unusable raw. Saying ~67% and hitting 48.5% is catastrophic miscalibration.

Fix:

- Shrink hard toward market:
  - `p_final = w * p_model + (1-w) * p_market`
  - Start with `w <= 0.1–0.2` unless proven otherwise.
- Calibrate by market type:
  - rec yards,
  - receptions,
  - rush yards,
  - rush+rec if used,
  - overs/unders separately.
- Use isotonic/logistic calibration only on past weeks.
- Report reliability bins:
  - 50–52%,
  - 52–55%,
  - 55–58%,
  - 58–62%,
  - 62%+.
- If a bin says 65% and hits 50%, cap future probabilities.

---

# 2. Per-version review

## 100k sims / confidence check

What went wrong:

- More simulation volume did not create signal.
- Model had poor resolution: high-confidence bins did not hit more.
- Opponent adjustment, especially full strength, worsened results.
- No-shrink stretched noise away from 50%.

What should have been done:

- Benchmark against market first.
- Use market as prior, not opponent-adjusted stat projections as truth.
- Calibrate on earlier weeks only.
- Kill any version whose Brier/log loss is worse than market.
- Treat sim output as feature generator, not as autonomous probability.

Verdict: **current sim probabilities should not drive bets.**

## Rulebook replays Wk6–8

What went wrong:

- Rulebook gates depended on unavailable data: film, defender matchups, historical coverage snapshots.
- Replay used proxies for hard rules, changing the actual system under test.
- Passed legs hit 48.5–52.1%, negative ROI.
- `SCHEME_EDGE` overrides were awful: 20–34, 37%.
- Alts/short prices bled money.
- Slip construction magnified weak edges into large losses.

What should have been done:

- If a required input is unavailable historically, either:
  - remove it from the rulebook, or
  - mark the version non-backtestable.
- Evaluate each rule as an additive filter with confidence intervals.
- Do not allow qualitative flags to override empirical form/price gates.
- Do not replay 6–7 leg slips if live plan is 3–4 legs.
- Separate line-selection quality from side-selection quality.

Verdict: **rulebook as written is too data-hungry for your constraints.**

## Rico method Week 8

What went wrong:

- Not blind. Analyst had seen postmortems and possibly graded files.
- Mechanical proxy was not the actual phase script.
- 34 legs is noise.
- 0/8 slips says correlation/selection failed, but sample is tiny.

What should have been done:

- Run prospectively only.
- Lock picks before any games.
- Grade after all results.
- Save all prices and closes.
- Treat as smoke test, not validation.

Verdict: **not usable as evidence of edge. Useful as workflow rehearsal.**

## v5 LLM brainstorm + tags

What went wrong:

- Train Wk3–6 43.8%, holdout Wk7–8 60.8% is suspiciously inverted.
- Possible hindsight leakage or selection artifact.
- `PRO_EDGE` approximated offline and not equivalent to actual live edge.
- `ZONE_MOF`/coverage style likely unreliable under free-data constraints.
- Holdout sample around 50 legs is too small.

What should have been done:

- Masked rerun before reporting holdout performance.
- No team/player/date identifiers.
- Same locked prompt across all weeks.
- Compare LLM picks to:
  - market no-vig,
  - simple last-4 baseline,
  - random market-side baseline,
  - closing-line movement.
- Score CLV, Brier, log loss, ROI.

Verdict: **promising only if masked rerun preserves CLV and calibration. Hit rate alone is not enough.**

## v6 plan

What to avoid:

- Do not add more complexity before proving signal.
- Do not use unavailable defender/coverage data as hard gate.
- Do not let LLM “story strength” override price.
- Do not use full opponent adjustment given confidence-check result.
- Do not optimize parlays first.

What v6 should be:

- Market-anchored.
- Free-data-only.
- CLV-first.
- Low degrees of freedom.
- Strictly prospective.
- Small number of stable features:
  - role,
  - volume,
  - line movement,
  - current QB,
  - injury/snap opportunity,
  - game total/spread,
  - team pass/run rate,
  - opponent allowance adjusted modestly.

---

# 3. Better per-game yardage prop checklist using free data

Use this as a compact deterministic checklist.

## A. Market / price

- Current line, price, book.
- Consensus line if available.
- No-vig probability.
- Has line moved since open / earlier snapshot?
- Are you beating current consensus?
- Is this an alt line with bad hold? If yes, default cut.

## B. Player role

- Snap share last 3–4 games.
- Routes run / team dropback participation for receivers.
- Targets, target share, air-yard share.
- Carries, route share, targets for RBs.
- Red flags:
  - role declining,
  - returning injured teammate,
  - rotation ambiguity,
  - low route participation,
  - gadget usage.

## C. QB / offensive environment

- Same QB as last-4 sample?
- Team pass rate over expectation, if available free.
- Dropbacks per game.
- Sack/pressure vulnerability proxy:
  - sacks allowed,
  - pressure if available from public FTN/nflverse.
- Offensive pace/play volume.
- Implied team total.

## D. Opponent defense — free-data version

Avoid fake precision. Use broad allowed metrics:

- Yards allowed to position:
  - WR,
  - slot/TE if available,
  - RB rushing/receiving.
- Explosive pass/rush allowed.
- Opponent run defense:
  - YPC,
  - rushing success rate if available.
- Opponent pass defense:
  - yards/attempt,
  - completion rate,
  - sack rate,
  - explosive pass rate.
- Injuries to defense:
  - starting CB/S/LB/DL out,
  - but do not pretend to know exact shadow matchups unless sourced.

## E. Game script

- Spread and total.
- Favorite/dog role.
- Is over dependent on trailing pass volume?
- Is under vulnerable to overtime?
- Blowout risk:
  - favorite WR overs can die in Q4 run-out,
  - dog RB rush overs can die if trailing,
  - dog receiving overs can benefit if target role stable.

## F. Line-specific fit

For overs:

- Needs normal volume, not ceiling outcome.
- Player clears line

---
# Follow-up call (sections 4-5; first answer truncated at output cap)

## 4. Parlay/correlation advice for 3-4 leg yardage slips — FanDuel/PrizePicks

### Core critique

Your single-leg work already says the model is not beating the market yet. That matters more for parlays than for straight bets: a small calibration error becomes much larger when multiplied across 3-4 legs. Until the single-leg CLV / calibration loop is positive, parlays should be treated as a **diagnostic format**, not an edge deployment format.

For now, the goal should be: **avoid hidden negative correlation, measure realized correlation, and stop treating legs as independent unless proven otherwise.**

### Practical parlay rules

#### 1. Do not mix same-game pass-catcher overs with QB/pass-volume assumptions unless explicitly modeled

You are excluding passing yards, but receiving overs are still implicitly pass-volume bets.

Avoid slips like:

- WR over receiving yards
- TE over receiving yards
- RB receiving over
- opposing pass-catcher over

These often share one or more fragile assumptions:

- high total play volume
- competitive game script
- no 4Q run-out
- pass-heavy script
- QB efficiency
- protection holding up
- weather not suppressing explosives

If that shared assumption is wrong, the slip dies together.

**Free-data alternative:** tag every receiving/rushing leg by likely script dependency:

- `needs_trailing_or_shootout`
- `survives_leading_script`
- `volume_floor`
- `explosive_dependent`
- `4Q_runout_risk`
- `injury_replacement_volume`

Then cap each slip at **one or two legs with the same failure mode**.

#### 2. Prefer cross-game diversification over same-game “story slips”

Given your current data limits, most same-game correlation estimates will be hand-wavy. FanDuel/PrizePicks parlay formats make it tempting to build coherent narratives, but coherent narratives are exactly where LLM hindsight and human selection bias can hide.

Temporary rule:

- 3-leg slip: max **one same-game pair**
- 4-leg slip: max **two legs from one game**, and only if their correlation is plausibly non-negative
- avoid 3+ legs from one game unless you have a pre-registered same-game correlation model

I am unsure whether FanDuel/PrizePicks pricing already bakes in same-game correlation in your exact markets/format; assume it may, and do not give yourself free correlation credit.

#### 3. Separate “positive correlation” from “shared fragility”

A lot of amateur parlay logic confuses these.

Example:  
“Team A WR over + opponent WR over” may look positively correlated through shootout script. But both may also be negatively affected by:

- one team jumping ahead and killing tempo
- red-zone TDs replacing yardage
- sacks/penalties shortening drives
- turnovers creating short fields
- weather reducing explosive passing

So the right question is not “can these both hit in the same story?” It is:

> “What common event causes both to lose?”

Build slips by minimizing common-loss states.

#### 4. Use unders carefully; they are not automatically safer

Your replay showed rush-yard unders doing well, but small-sample and rule-tweak risk are high. Rushing unders can be attractive because they benefit from:

- negative game script
- committee usage
- injury/efficiency uncertainty
- short leash after fumbles/errors

But they are also vulnerable to:

- 4Q clock-killing
- one explosive run
- opponent offensive failure giving extra possessions
- favorite scripts

For parlay construction, do not pair multiple rushing unders that all require the same macro script, e.g. “three favorites dominate and opposing RBs go under.” That is a correlated bet on scoreboard state, not three independent edges.

#### 5. Create a simple correlation/failure-mode matrix

For every candidate leg, store:

| Field | Example values |
|---|---|
| market | rush yds / rec yds / receptions if used |
| team role | RB1, RB2, WR1, slot, TE, depth WR |
| script need | leading / trailing / neutral / any |
| volume type | designed touches / target share / explosive |
| fragility | blowout, committee, weather, injury return, QB downgrade |
| same-game relation | teammate / opponent / unrelated |
| failure state | run-out, low plays, QB collapse, early lead, split usage |

Then apply hard slip constraints:

- no more than **two legs with same failure state**
- no more than **two explosive-dependent overs**
- no more than **one depth-receiver over**
- no more than **one leg requiring a specific injury-news interpretation**
- no more than **two legs dependent on a competitive/pass-heavy game**
- do not combine “favorite RB over” with “same-game underdog WR/RB under” unless you intentionally want a game-script parlay and price it as such

#### 6. Track parlay EV from calibrated leg probabilities, not raw model probabilities

Given model probabilities were badly overconfident, parlay math should use only:

- market no-vig baseline
- market-shrunk calibrated probability
- correlation haircut

Simple placeholder until you have data:

- independent 3-leg hit prob: `p1*p2*p3`
- apply haircut for shared assumptions:
  - unrelated cross-game: 0% to -3%
  - mild shared macro risk: -3% to -8%
  - same-game / same-script: -8% to -20%+
  - narrative slip: assume no edge unless proven

This is crude, but better than pretending independence. I am unsure of the true haircut magnitudes without a larger logged sample; treat them as conservative placeholders.

---

## 5. Prioritized next-5-steps plan — free data only

### 1. Freeze the single-leg evaluation protocol before adding new rules

Highest priority: stop generating conclusions from moving targets.

Create one frozen file before each week:

- eligible games
- candidate legs
- lines/prices/time pulled
- market-implied no-vig probability
- model probability
- market-shrunk probability
- LLM tags, if any
- rulebook pass/fail
- final inclusion/exclusion reason

Do not edit after kickoff. Save hashes if possible.

Evaluation order:

1. CLV versus close
2. single-leg Brier/log loss versus market
3. hit rate by bucket
4. parlay performance last

Parlay ROI should not drive rule changes until single-leg calibration is at least market-competitive.

### 2. Use Odds API credits only for weekly live snapshots, not broad exploration

With ~250 credits/week, spend them on repeatable snapshots.

Suggested schedule:

- Tuesday/Wednesday: opening-ish player props where available
- Friday: injury-adjusted midweek
- Sunday morning: final snapshot within 1-2 hours of lock

If credits are tight, prioritize only:

- games/slates you may actually bet
- FanDuel/PrizePicks-relevant yardage markets
- no broad historical scraping until December

Store:

- timestamp
- book
- line
- price
- player/team/opponent
- market
- game start
- injury flags known at timestamp

Primary metric: did your selected side beat closing line/price? If not, the model probably is not adding tradable information.

### 3. Build a free-data baseline model that intentionally excludes LLM text

Before judging LLM value, make the non-LLM baseline solid.

Use nflverse / PFR-style variables only:

- player rolling usage: routes proxy if available, targets, carries, snaps if free, rush share, target share
- current QB indicator
- team pass/rush rate
- opponent allowed by position, but shrink heavily
- spread/total from current market if available
- injury status from free reports
- rest/travel/home
- weather for outdoor games
- line movement if you captured it

Model target should be probability of clearing the posted line, not raw yardage only.

Then calibrate with:

- logistic calibration
- isotonic only if enough data
- market-shrink prior: `p_final = w*p_model + (1-w)*p_market`

Pre-register `w`; do not tune it weekly after results. With your current results, `w` should probably be small.

### 4. Run LLM contribution as a masked, additive experiment only

Do not let the LLM select final bets directly yet.

For each leg, have the LLM produce only structured tags:

- injury role uncertainty
- game-script concern
- depth-chart ambiguity
- weather concern
- likely volume stability
- correlation/failure-mode tags
- confidence in data freshness

Use masked prompts where possible:

- no player names
- no team names
- no dates
- no final scores
- no odds outcomes
- only pregame information available at timestamp

Then test:

- baseline model alone
- baseline + LLM tags
- baseline + random/shuffled LLM tags as placebo

If LLM tags do not improve CLV, Brier, or log loss out of sample, keep them as qualitative notes only.

### 5. Create a parlay simulator using calibrated probabilities plus correlation haircuts

Do this after steps 1-4, not before.

For every frozen slate, simulate slips under fixed construction rules:

- cross-game only
- max one same-game pair
- no duplicate player
- no more than two same failure-mode tags
- no more than one depth WR
- no more than two explosive-dependent overs
- unders/overs balanced by rule, not by vibes

Compare:

1. random eligible slips
2. highest raw model edge slips
3. highest market-shrunk edge slips
4. best CLV-ranked slips
5. correlation-constrained slips

Report:

- expected hit rate
- realized hit rate
- payout-adjusted ROI
- average CLV
- common failure states
- whether legs failed independently or clustered

If correlation-constrained slips mainly reduce catastrophic clusters but do not improve EV, that is still useful: it means your issue is single-leg edge, not parlay construction.