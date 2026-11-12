# Deep-dive review (gpt-6.1-sol; full per-chunk reviews in section_reviews.md)

# NFL yardage-prop backtest: deep-dive

## Bottom line

**No reviewed version demonstrates a reliable betting edge.** The strongest findings are overconfidence, losing executable or proxy returns, unreliable replay chronology, and operational failures—not evidence that adding exceptions will improve results.

The objective remains **FanDuel/PrizePicks 3–4-leg rushing, receiving, and rush+receiving yardage slips**. TDs, passing yards, receptions, and larger slips cannot validate that objective. Treat all inspected weeks as development data; proceed shadow-only.

## 1. Statistical design fixes

### Sample size, power, and endpoints

- Preregister the candidate universe, placement time, rules, exclusions, staking, settlement, and success criterion.
- Use **priced singles to diagnose selection/calibration** and **actual 3–4-leg slip ROI to evaluate the product**. Declare their hierarchy before testing.
- Power the study for a meaningful **after-vig return**, incorporating game/week clustering, repeated players, overlapping slips, and missing quotes. The reviews do not establish a defensible sample-size target.
- Six weeks are insufficient. Thousands of correlated replay legs are not thousands of independent prospective observations. V5’s 31/51 has an illustrative independent interval of roughly **47–73%**, before selection and clustering.
- Report turnover, drawdown, game/player exposure, clustered intervals, and sensitivity to unavailable prices and unresolved settlements.

### Overfitting and controls

Freeze versions and prohibit postgame rescues. Compare, on the **same eligible universe**:

1. Market benchmark.
2. Raw model.
3. Gates without mirrors.
4. Mirrors separately.
5. Prior-only calibrated model.
6. Simple main-line rushing unders.

Test weather, role, scheme, shrink, and manual exceptions through preregistered ablations. Named-player exceptions and missed winners are hypotheses, not validation. Never mechanically invert unsuccessful overs.

### Leakage and reproducibility

Separate **as-operated**, **reconstructed**, and **prospective** results. Archive code, prompts, model/retrieval configuration, inputs, outputs, and rules with effective timestamps.

Record event time, publication/observation time, and retrieval time. “Week earlier than evaluation week” is insufficient if historical features were subsequently revised. Exclude unverifiable injury, roster, QB, weather, defensive, or odds inputs from clean evaluation.

LLM denials, masking, passing tests, and code hashes do not establish information isolation.

### Calibration and economics

Every reviewed simulation scored worse than market Brier around **.248**, and worse than a .250 coin benchmark. In CC, 87.2% forecasts won only **52.5%**; 70–80% forecasts won **49.3%**.

Use earlier-only calibration/blending, reliability plots, Brier/log loss, and matched executable ROI. More simulations reduce Monte Carlo error—not model bias. Three related engines are not independent confirmation.

Define **P(yards > line)** explicitly; a median, percentile, or “3 of last 4” is not that probability. At −110, break-even is **52.38%**; an unvalidated three-point advantage over a no-vig estimate is insufficient.

### CLV and accounting

Archive prospective executable opening/placement/closing quotes within budget; no historical pulls before December. A T−29–39-minute snapshot is not automatically closing.

Compare identical markets and rungs, distinguishing line movement from price movement. CLV is supporting evidence, not proof. PrizePicks payout economics require separate treatment.

Reconcile settled versus priced counts, priced W/L, pushes, voids, exclusions, and unavailable tickets.

## 2. Per-version review

| Version/test | Assessment |
|---|---|
| **V1 / 100,000 simulations** | Simulation count supplies no validation. The reviewed replay reported roughly **67.3% predicted versus 48.5% realized**, with Brier **.267 versus market .247**. Candidate pools changed—293 versus 463—so apparent version improvements are not controlled comparisons. Exact version/result linkage needs manifests. |
| **Rulebook replays, Weeks 6–8** | Current rules were reconstructed backward; chronology and input availability were compromised. Missing film blocked every strict run. Patched gates and synthetic attribution did **not** constitute approval. Target-sized Test A lost **$1,070.42/$2,450, or 43.7%**, across 245 slips. The 6–7-leg test was outside scope. Book mixing and multiplied decimal odds did not establish executable tickets. |
| **Rico method, Week 8** | An exposed, reconstructed exercise—not an untouched holdout. Reviewed singles lost **$29.52 on $270, or 10.9%**; eight slips lost. Saving money by betting less does not establish better selection. Saved reads and v6 wagers were unmatched, so their comparison is not causal. |
| **V5** | **31/51, or 60.8%**, is promising only descriptively. Claimed **+17.2% ROI on 40 priced** needs reconciliation with 51 settled. Slip counts **4/29 versus 9/25** conflict. Reused Weeks 7–8, variant selection, and incomplete leakage assurance invalidate a clean holdout claim. |
| **V6** | Priced READS: **42.3%, −19.1% ROI**; GATED: **41.5%, −21.6%**. Gates reduced exposure, not losses per dollar. READS slips **0/30**; GATED **1/26, about −51.8%**. Week 8’s improvement cannot erase preceding losses. |

**Cross-version evidence:** CC’s 2,411-leg comparison strongly disfavors the tested probability models; full opponent adjustment worsened scoring. Yet CC did not evaluate the complete deployed slip policy. Main rushing unders—**296/525, 56.4%; +2.8% across 421 priced**—remain exploratory, not proven profitable.

## 3. Verdict on the ChatGPT MNF audit

**YES means an identifiable Rico-approved rule would be reversed. NO means no identifiable reversal—not verified compliance. N1/N2 are undefined: compatibility remains UNKNOWN throughout. Obtain their exact text before release.**

| Proposal | Undo? | Verdict |
|---|---|---|
| Replace last-four 3-of-4 requirement with warning/opportunity | **YES: §7** | Reject live; shadow-test rejected candidates without admitting them. |
| Replace WR3/WR4 exclusion with opportunity ranking | **YES: #3/#4 rule** | Reject live; research usage exceptions separately. |
| Replace positional averages with opportunity/matchup evidence | **NO**, gates intact | Keep descriptive workflow; test predictive weighting. No unavailable coverage inputs. |
| Replace 30%/50% reductions with calibration | **NO identifiable reversal; N1/N2 unknown** | Test-first against current shrink and market. Removing shrink worsened calibration. |
| Separate tacklers from coverage; repair defensive database | **NO** | Keep provenance and explicit unknowns. Repair is not demonstrated uplift. |
| Raise confidence from verified primary defender | **NO**, absent exemptions | Test-first; zone assignments and uncertainty cannot bypass gates. |
| Replace RB <60% carry-share restriction with opportunity assessment | **NO identifiable reversal; N1/N2 unknown** | Test by market/side; preserve main rushing-under research. |
| Review expensive alternates | **NO if flag retained; YES if removed** | Retain **−250-or-shorter flag**. Flag ≠ ban; require probability/price review, not model-only overrides. |
| Expand `SCHEME_EDGE` | **NO only without overrides** | Research-only; reject exemptions from §7, depth, price, or unresolved N1/N2. |
| Reject wholesale shrink removal | **NO** | Keep shrink; test strength prospectively. |
| Reject forced Loveland/Burden/Odunze selections | **NO** | Keep; hindsight winners do not justify admission. |
| Opportunity → matchup → script → probability → decision | **NO**, mandatory gates intact | Keep logging/workflow; model improvement remains unproven. |
| Log rejection reasons and compare original/revised systems | **NO** | Keep every candidate; CHI@SEA is development only. |
| Separate NBA/repository work | **NO** | Keep independent tests and installation verification. |

One game cannot establish that loosening any gate improves returns. Conversely, aggregate losses do not prove each existing gate is useful.

## 4. Per-game reasoning checklist

1. **Freeze scope:** eligible yardage markets, books, placement time, 3–4-leg limit, rule version.
2. **Verify availability:** active roster, QB, injuries, roles, and timestamped free-source information. Unknown remains unknown.
3. **Estimate opportunity:** attempts, targets, catches, workload shares, and current-QB context—with small-sample uncertainty.
4. **Assess matchup honestly:** no fabricated routes, coverage assignments, PFF grades, or film conclusions. Tackler identity is not coverage evidence.
5. **Assess script/weather:** contemporaneous spread and issued forecast; distinguish precipitation probability, intensity, wind, and actual conditions.
6. **Evaluate distribution and price:** coherent rung probabilities, calibrated uncertainty, executable odds/payout, mandatory gates, and −250 flag.
7. **Log the decision:** every candidate, rejection, exception request, alternative, and unavailable quote.
8. **Settle immutably:** preserve original line/price; do not substitute a winning lower rung. Apply operator injury/void rules—not assumed “bet protection.”

## 5. Slip and correlation advice

At a hypothetical independent **42.3%** leg hit rate, three- and four-leg wins are only about **7.6% and 3.2%**. These are illustrations, not joint forecasts.

- Use actual quoted FanDuel/PrizePicks payouts; never assume multiplied singles prices reproduce same-game pricing.
- Track shared player, team, QB, game script, weather, and overlapping-ticket exposure.
- Several winning rungs on one player are not independent successes.
- Compare slips at matched stakes and exposure; fewer wagers mechanically reduce dollars lost.
- Keep singles and slips separate. A higher hit rate on expensive alternates can still lose money.
- Stop 5–8-leg drift. No reviewed evidence validates discretionary correlation exceptions.

## 6. Top-five plan under the constraints

1. **Reconcile the ledger first.** Resolve counts, version mappings, original versus alternative lines, prices, exclusions, and conflicting slip results.
2. **Freeze a feasible policy.** Free-data-only means no pretend film/PFF approval. The existing strict policy may yield no bets; any feasible successor is a separately versioned experiment.
3. **Spend ~250 API credits/week deliberately.** Narrow games/markets, prioritize executable quotes and prospective close snapshots, cache responses, reserve headroom atomically, and log missingness. No historical pulls before December.
4. **Run paired shadow comparisons.** Market-only, simple rushing unders, raw/current gates, and prior-calibrated variants; isolate shrink/opponent adjustment before adding exceptions.
5. **Evaluate untouched future weeks.** Include operational failures and unavailable tickets. Report calibration, singles economics, actual 3–4-leg payouts, dependence, and uncertainty. Amendments start new versions.

## 7. Remaining uncertainties

N1/N2 wording, some version/result mappings, 2026 claims, missing referenced files, and historical information availability remain unverified. Pricing missingness may be nonrandom; replay approvals and exact executable payouts are unresolved.

Neither the optimal shrink strength nor the isolated value of weather, scheme, mirrors, and role gates is established. The positive rushing-under result needs prospective confirmation.

**Recommendation: simplify, freeze, audit, and shadow-test—not loosen gates to recover remembered winners.**