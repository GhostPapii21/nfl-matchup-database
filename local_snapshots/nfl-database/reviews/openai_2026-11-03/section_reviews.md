## Section review 1/4

## 1. v6 graded results: no demonstrated edge

`backtests/v6_brainstorm_proedge/results.md` is the strongest evidence in this chunk—and it is negative.

- **READS, priced Wk3–8:** 66–90 overall (**42.3%**); **−$264.95 / −19.1% ROI** on 139 priced legs. Losses span every market: receiving **−14.0%**, rush+receiving **−13.6%**, rushing **−30.4%**.
- **GATED:** 49–69 (**41.5%**); **−$237.41 / −21.6%** on 110 priced legs. The gate reduced exposure, **not loss per dollar wagered**. CUT legs returned **−9.5%**, versus PASS **−21.3%** and FLAG **−22.3%**. These small, selected groups do not establish a reversed signal, but provide no evidence that gating adds value.
- **Target-format slips:** READS lost all **30**, costing **$300**. GATED won **1/26**, losing **$134.73**, approximately **−51.8% ROI** at the reported $10 stakes. One Week 8 winner is not validation.
- **Baseline:** every main rushing under hit **296/525, 56.4%**, with **+$116.45 / +2.8%** on 421 priced legs. This is a useful benchmark, not a proven profitable strategy: uncertainty, dependence and price availability remain material.

Zero winning READS slips is not independently extraordinary: at a hypothetical independent **42.3%** per leg, three-/four-leg win probabilities are only **7.6%/3.2%**. Actual ticket dependence matters. The **0/16** six-/seven-leg results add little and lie outside the stated 3–4-leg objective.

Week 8 improvement—GATED **12–5, +32.4%**—does not erase five losing weeks. Wk1–2 stand-in results must remain separate: GATED **62.5%** there is neither executable-price evidence nor a reason to discount the priced losses.

## 2. Accounting and comparison need repair

**Hit rates and ROI describe different populations.** READS has **156 settled legs but 139 priced**; GATED **118 versus 110**; baseline **525 versus 421**. Report priced-subset wins/losses alongside ROI. Otherwise readers cannot distinguish price effects from missing-price selection. Explain all unpriced, unresolved, pushed and voided records.

The baseline is not a matched control: it covers a much larger, different market population. Retain it as a broad benchmark, but add same-game, same-market, same-timestamp comparisons. Do not mechanically invert losing overs: opposite-side prices and selection effects can eliminate any apparent advantage.

GATED totals exactly equal READS’ PASS+FLAG totals, while the heading says “including mirror overs.” Provide a flow table: original candidates → cuts → mirrors generated → final legs, with stable identifiers. The current aggregation does not establish the mirrors’ incremental contribution.

The saved-read comparison is also unmatched: original reads are **7–7, eight priced**; v6 on those games is **4–14, fifteen priced**. Same games are not the same wagers. This is concerning reproducibility evidence, not a controlled estimate of method deterioration.

## 3. Leakage and overfitting remain unresolved

The chronology is a central flaw. `PHASE_SCRIPT.md` incorporates Oct. 29–Nov. 2 amendments, explicit postmortem examples and later-effective requirements. Applying these retrospectively to earlier weeks evaluates an **outcome-informed strategy**, not the strategy available then.

Distinguish three claims:

1. **As-operated replay:** only rules and information available before each kickoff.
2. **Reconstructed historical experiment:** newly specified rules on historical data.
3. **Prospective validation:** frozen rules on genuinely untouched games.

Only the third cleanly tests the current, repeatedly revised system. Wk7–8 is no longer a defensible holdout after repeated comparisons and revisions. The brief’s v5 **60.8% holdout** and conflicting slip summaries—**4/29** versus **9/25 elsewhere**—require denominator and version reconciliation.

`backtests/v5_leak_audit/` does not establish absence of leakage. **33 clean prompt checks**, winner guesses of **14/27** and **4/10**, and model denials cannot exclude implicit result knowledge, contaminated retrieval or outcome-informed analyst inputs. Masking is useful but not definitive: statistics can identify games.

**Fix:** freeze prompts, model identifier, retrieval permissions, inputs and outputs before kickoff; archive source publication timestamps and raw snapshots. Enforce an as-of boundary for statistics, injuries, rosters, weather and odds. Historical reruns remain exploratory unless every input’s availability is verified.

## 4. Rulebook complexity exceeds the evidence and data

`PHASE_SCRIPT.md` contains many plausible narratives, but plausibility is not validation.

- **Unavailable coverage evidence:** mandatory defender mapping, route matching and man/zone/MOF checks conflict with the stated free-data limitations. PFF approval also conflicts with “NO PFF.” Define one executable data contract. Missing required evidence means abstention—not an LLM proxy presented as measurement.
- **Postmortem-specific exceptions:** named-player rules, weather thresholds, mirror overs and manual overrides create extensive researcher discretion. Corrections motivated by individual losses can manufacture historical fit.
- **Recent-form screening:** “clear the line in 3 of the last 4 with current QB” is a noisy, line-dependent selection filter—not calibrated probability evidence.
- **Percentile confusion:** calling the **15th percentile “MAIN”** while also using a consensus median invites interpretation errors. Define \(P(Y>L)\), not merely projection labels.
- **Alt-line ambiguity:** moving an under from 75.5 to 55.5 makes it harder to win; switching to an over changes the proposition. Every alternative requires its own probability and price.
- **Injury accounting:** “injury during game = bet protect” is invalid unless the actual operator/product voided that wager. Grade according to settlement terms.

The supplied file ends mid-rule; that unfinished exception cannot be evaluated.

## 5. Simulations do not rescue misspecification

The brief reports **all nine sim versions worse on Brier score than the market’s 0.248 and a 0.250 coin forecast**. Its priced replay produced **48.5% hits where the model predicted approximately 67%**. Those are direct warnings against model-based edge thresholds.

**100,000 simulations reduce Monte Carlo noise, not model bias.** Three related models are not three independent confirmations. Averaging their outputs cannot establish a “true median.”

Before selecting bets, report out-of-sample calibration curves, Brier/log loss, uncertainty and performance against contemporaneous no-vig prices. A claimed **+3-percentage-point edge** is unusable when calibration error is much larger.

## 6. Concrete next experiment

1. **Freeze one version** and preregister the eligible universe, timing, exclusions, staking, settlement and primary endpoint. No discretionary rescue rules.
2. **Use priced singles as the primary diagnostic.** Keep 3–4-leg slips secondary; stop six-/seven-leg expansion.
3. **Archive executable odds:** book, timestamp, line, both-side prices, availability and payout rules. Separate FanDuel parlays from PrizePicks formats.
4. **Run paired ablations:** raw reads, gate without mirrors, mirrors, calibrated model and baseline, on common eligible observations.
5. **Model joint outcomes:** shared pace, script, injuries and player/team dependence. Report unique exposure and repeated legs across tickets.
6. **Quantify uncertainty:** game/week-clustered intervals, turnover, drawdown and sensitivity to unresolved bets. Six weeks is too little for stable cluster inference.
7. **Treat all reviewed weeks as development data.** Accumulate a preregistered prospective sample; log amendments without rewriting prior predictions.

**Bottom line:** this chunk demonstrates substantial losses, poor calibration and no established gate benefit. It supports simplifying and prospectively testing the process—not adding more narrative rules.

## Section review 2/4

## Chunk 2 review: confidence inflation, not demonstrated edge

**Verdict:** This chunk provides strong evidence against trusting the raw simulation probabilities—and no evidence supporting the new discretionary exceptions. The confidence check is materially better designed than the evolving rulebook, but it tests the **raw model layer**, not the complete selection policy or 3–4-leg slips. The rulebook replay is operationally blocked, and its hypothetical singles lose substantially.

References below: **CC** = `backtests/confidence_check_2026-11-03/report.md`; **RR** = `backtests/rulebook_replay_wk6_8/REPORT.md`.

### 1. What the evidence actually establishes

- **Probability quality is poor.** Across the same 2,411 legs, market Brier is **0.2481**, versus **0.2600–0.2602** with old shrink, **0.2723–0.2730** without shrink, and **0.2767–0.2771** with full opponent adjustment. Every reported game-clustered 95% interval for the model–market Brier difference excludes zero. All model variants also score worse than a flat 50% forecast *in this sample*.
- **Removing shrink amplifies miscalibration.** For sim_v6 V2, predictions averaging **87.2%** win only **52.5%** across 162 model-favored selections. The 70–80% bin wins **49.3%** across 371. These are not credible “found edges” awaiting managerial confidence; they are severely overstated probabilities.
- **Full-strength matchup adjustment worsens observed scoring.** Raising `oppadj` from 0.5 to 1.0 adds approximately **0.004–0.005 Brier**. However, CC reports intervals against the market, not paired intervals for this incremental deterioration.
- **No tested +3-point strategy makes money.** Flat-stake ROI ranges from **−3.7% to −5.8%**. Importantly, no-shrink V2 loses *less* than V1 in every engine despite worse probability scoring. Therefore, distinguish “worse forecasts” from “worse realized betting returns”; changing shrink changes which bets qualify.

The three engines’ near-identical results are evidence of shared behavior, **not three independent confirmations**. Earlier overlapping NFL replays are likewise not independent replications.

### 2. Confidence-check design: good safeguards, incomplete causal audit

Credit is due for paired evaluation on a common universe, game-clustered uncertainty, fixed simulation seeds, scratch-code isolation, and walk-forward refitting. Avoiding committed `sim_v6_calib.json` files trained on Week 4–7 outcomes prevents an obvious leakage channel. Twenty thousand simulations per model-leg are adequate; more Monte Carlo draws will not repair structural miscalibration.

But “leak-free inputs” needs stronger substantiation:

- **Audit residual provenance.** Filtering saved residuals to weeks `< W` is insufficient if those residuals were originally generated using future-aware features or fitted models. Reconstruct each training prediction with its historical information set.
- **Archive feature availability, not merely game dates.** Depth charts, current-QB assignments, injury reports, defensive classifications and source revisions need `observed_at` timestamps. A pre-week play-by-play cutoff is necessary, not sufficient.
- **Activity grading may create hindsight selection.** CC requires players to be active “graded from nflverse pbp.” Establish whether this excludes dressed players with no snaps or zero outcomes. Use historical eligibility and book settlement rules, not retrospective participation alone.
- **Reconcile counts before relying on the report.** CC says 2,448 legs were built, 43 unmatched quotes dropped, and 2,411 retained after simulation exclusions. Read literally, those counts cannot reconcile: **2,448 − 43 = 2,405**, already below 2,411. Publish a row-level exclusion ledger.

Coverage also limits generalization: Weeks **1–2 are absent**, Weeks **3–5 lack receptions/passing prices**, and passing yards has only **83 legs**. Thin-history simulation failures, mostly Week 3, make complete-case selection potentially nonrandom. Report operational abstentions separately.

### 3. Rule changes are an expanding researcher-degrees-of-freedom problem

The Nov 2 changes introduce numerous pathways for overriding negative evidence:

- `SCHEME_EDGE` turns §7 and simulation checks into flags using four qualitative judgments.
- WR3 overs gain a depleted-secondary exception, a **four-target** threshold and a **4.0–4.9 borderline** category.
- Split-backfield/weak-backup-QB cases become manual review.
- Rejected unders generate mirror overs; press eligibility expands.

These may be sensible hypotheses, but **none is validated here**. Named examples—Rachaad White, Loveland and Burden—and same-day timestamped amendments raise post-hoc selection concerns. The excerpt does not establish what information or outcomes were known when each amendment was chosen.

Sources attached to judgments improve auditability; they do not establish predictive value. `SCHEME_EDGE` can become an unfalsifiable override if reviewers know prices, model rejection reasons or outcomes. “Last two games with current QB” and last-four target thresholds are particularly noisy and invite threshold tuning.

**Fix:** Version and freeze the complete rulebook before an untouched evaluation period. Define ranks, corner absences, QB grades and scheme criteria mechanically where possible. Log every candidate, rejection and override before kickoff. Use blinded independent coding for subjective fields and report reviewer agreement. Treat each exception as a preregistered ablation, not a production privilege.

### 4. Market comparison and betting economics need separation

CC’s market benchmark averages multiplicative no-vig probabilities across books quoting the modal line; returns use a saved executable-side price, “FanDuel when quoted.” Document exact line, book, timestamp and availability for every wager. A consensus benchmark is not necessarily a tradable price.

A **+3-point edge against no-vig is not automatically sufficient against vig**. At −110, break-even is **52.38%**; a model probability of 53% against a 50% fair benchmark leaves little room for estimation error.

The T−29–39-minute snapshots are legitimate near-close references, **not closing prices**. If selections were intended for earlier publication, replaying against later prices and information would mismatch the deployment decision.

Fit any calibration or market-anchored blend only on prior data. Test a market-only baseline and require positive incremental value. Do not simply choose the least-bad variant from these already-inspected weeks.

### 5. The rulebook replay does not validate deployment or slips

RR’s strict result is **zero live legs and zero of 369 slips approved**, because every run lacks a `film` source. That is an operational failure, not evidence that the strategy would necessarily lose—or a technicality to waive afterward.

Ignoring that blocker, the reported singles cohort goes **241–222**, losing **$569.78 on $4,630 staked: −12.3% ROI**. Clarify “463 more pass door”: the win/loss totals imply 463 total graded singles, not 463 additional successes.

Low-rung alts lose **$423**, and passing-yard overs go **5–17**. These samples differ from CC’s main-line universe; their returns are not directly comparable. The excerpt ends before slip results, so **no slip-performance conclusion is available**.

### 6. Required next experiment

1. **Keep this shadow-only.** Reconcile why full `oppadj=1.0` already appears in `tools/sim_v6.py` and Thursday’s sim despite the pending test; record commit **6322cc5** and rollback criteria.
2. Run a paired **2×2 shrink/oppadj experiment**, including the missing shrink-plus-full-adjustment cell. Report paired score and ROI intervals.
3. Reserve untouched future weeks for the frozen complete pipeline, including missing-data failures, manual decisions, injury/QB handling and actual publication-time prices.
4. Evaluate 3–4-leg slips using **joint outcomes and actual payout schedules**, not multiplied marginal probabilities. Include within-game dependence, exposure limits and drawdowns.

**Bottom line:** The evidence supports restricting confidence and deployment—not relaxing gates to preserve attractive narratives.

## Section review 3/4

## Chunk 3 review: useful diagnostics, not validated betting evidence

**Bottom line:** the losses are credible warnings; the apparent improvements are not credible evidence of an edge. This chunk mixes retrospective rule execution, synthetic approvals, non-executable parlay prices, and repeatedly examined weeks. Its disclosures are valuable, but several limitations invalidate the headline interpretation rather than merely widening error bars.

### 1. What the results actually show

- **The target 3–4-leg strategy lost heavily:** Test A returned **−$1,070.42/$2,450 = −43.7% ROI**, winning 20/245 slips. Test B lost **34.6%**, but its 6–7-leg construction violates `SLIP_SIZE` and is outside the target strategy.
- **Filtering did not demonstrate economic value.** In `graded_legs.csv`/the replay tables, the 463-leg pool lost **12.3%** at $10 flat, versus **8.2%** for blocked legs. This is descriptive—not a causal rule comparison—but certainly not evidence that passing the gates improves returns.
- Higher hit rates were misleading: SCHEME_EDGE legs hit **61.1%** yet lost **$25.95**; low-rung alts hit **53.0%** yet lost **$422.70**, or **21.3%**. Price matters more than an arbitrary hit-rate target.
- Passing-yard overs, **5–17 and −$131.15**, look problematic. Rush-yard unders, **20–6 and +$114.73**, are promising only as a hypothesis: 26 observations amid many inspected subgroups cannot establish an edge.

### 2. The “as-of” replay is not point-in-time clean

`gate_replay.py` forces activation dates to 2000 and `_rb.active=True`. That tests **today’s rules on reconstructed history**, not what the historical system could actually have selected.

More serious information-timing problems remain:

- Sharp coverage dated **2026-10-27** is hindsight for Weeks 6–7. Stamping it `now − 5m` does not make it historically available.
- Postgame ESPN injuries stamped kickoff −90 minutes cannot establish pregame availability. Using the actual starting QB can also leak information unless that starter was confirmed before the decision.
- Historical weather products need issuance timestamps, not inferred replay timestamps. The kickoff-value precipitation substitutions and pbp roof status require separate availability checks.
- Removing known Sharp hindsight reduces Weeks 6–7 leg passes **368→308**. Respecting Week 8 coverage age reduces them **102→17**, with only **15 pool legs**. These are material changes to the strategy, not minor sensitivities.

**Fix:** preserve distinct `event_time`, `publication_time`, `retrieval_time`, and provenance fields. Unverifiable inputs must be unavailable—not backdated. Separate the contaminated reconstruction from a point-in-time-valid subset.

### 3. “Door PASS” is not deployment approval

The report says every strict run fails because film is absent, yet **245 Test A slips PASS** under leg-level handling. Patching `door.run_gate`, forcing `ok=True`, and admitting legs without leg-named misses can bypass run-level failures.

Call these **research-eligible legs**, not approved bets. Missing analyst attestations and checklist N/As are correctly disclosed, but cannot become implicit passes.

The **406 tests**, hash `ff7a42188e06e1b9`, establish neither historical data integrity nor correctness of the patched execution path. A copied test result and reused ledger check also do not prove each replay’s state was valid.

**Fix:** make global, leg, and slip failures explicit structured objects; avoid name-regex attribution. Add tests showing global failures propagate through the exact replay path.

### 4. The prices do not establish executable returns

Products of decimal odds are not valid SGP quotes. Positive same-game dependence commonly reduces payouts relative to that product; negative dependence can move the other way. **M2 needs actual bookmaker quotes**, not a blanket approximation.

Even cross-game M1 has a timing problem: combining each game’s **kickoff-minus-30-minute snapshot** may use late-game prices or information unavailable when the earliest leg had to be placed. FanDuel-first, otherwise-first-book pricing also does not guarantee a single bookmaker could accept the whole slip.

The main-line-margin adjustment for one-sided alts is not an identified fair probability. Missing alt events after the budget stop may change selection non-randomly.

**Fix:** construct each ticket at one feasible placement time, using one bookmaker’s available lines and quoted payout. Report unmatched or unavailable tickets separately. Treat proxy-priced results as simulations, not executable backtest P/L.

### 5. Model quality and rule attribution need harder scrutiny

The strongest diagnostic is in `backtests/current_rules_wk6_8/REPORT.md`: **Brier 0.267 versus market 0.247**, and passed legs predicted **67.3%** against **48.5% realized**. Larger claimed edges performed worse. That points toward overconfidence, misspecification, or selection error—not insufficient parlay legs.

Avoiding calibration fitted on Weeks 4–7 was correct. But **100k simulations and a fixed seed** reduce Monte Carlo noise; they do not validate distributions, opponent adjustments, proxies, or uncertainty.

Other weaknesses:

- Pbp-credit “coverage,” fixed WR→CB assignments, and hit-based pressure proxies are not equivalent to their named concepts.
- “Slip killers” are loss counts without exposure denominators; reused legs can dominate mechanically.
- Rule-miss totals need declared units: **3,951 over + 1,652 under** median misses exceed 4,487 candidates.
- v1’s **293 best-player legs** and v2’s **463 pool legs** differ in universe and possibly deduplication. Their hit rates are not an apples-to-apples improvement.

**Fix:** compare calibration, scoring rules and executable ROI on a common universe; run preregistered rule ablations. Cluster uncertainty by game/week and preserve repeated-leg dependence.

### 6. Rico and v5 remain exploratory

`backtests/rico_method_wk8/REPORT.md` explicitly admits result exposure and prior postmortems. Commits before grading help traceability, but **locking after games is not prospective blinding**. Mechanical replacements reduce discretion only if their complete rules were frozen before exposure. Reconstructed singles lost **$29.52/270 = 10.9%**; all eight slips lost. Fewer dollars lost than rules-only largely reflects fewer bets.

`backtests/yardage_markets_wk3_8/v5/report.md` is more encouraging but fragile:

- Holdout **31/51 = 60.8%** has an illustrative independent-binomial 95% interval around **47–73%**, before dependence.
- **+17.2% ROI** covers only **40 priced legs**, not all 51 settled legs. Explain price missingness and test adverse missing-price scenarios.
- Weeks 7–8 already appear throughout this research program. Superseded formats and numerous variants create substantial selection risk.
- Four winning PRIMARY slips out of 29, using approximate payouts, do not establish repeatability.

The `v5_leak_audit/direct_answer.md` excerpt ends at the question; **no audit conclusion is available here**. An LLM’s own assurance would not establish uncontaminated packs or absent outcome knowledge anyway.

### 7. Required next experiment

Freeze code, prompts, thresholds, data contracts and ticket construction **before genuinely unseen games**. Calibrate only on earlier data; retain a final untouched evaluation period. Preregister one primary 3–4-leg strategy, executable ROI and uncertainty methods; treat other markets and variants as exploratory. Benchmark against bookmaker probabilities and simple market-matched selections.

Finally, replace shared-key monitoring with atomic credit reservations and headroom: **5,959 remaining breached the 6,000 floor by 41**. Stopping afterward was appropriate, but the control failed—and incomplete acquisition altered the experiment.

## Section review 4/4

## Bottom line

This chunk documents useful operational failures—exposure concentration, role uncertainty, inconsistent grading and overly rigid gates—but **does not establish a profitable player-yardage strategy**. The strongest replay result is actually negative: **12/19 winning legs, −$2.59 at $10 each**, and both rules-built 3–4-leg slips lose. The postmortems generate hypotheses; they do not validate the proposed fixes.

I treat the reported 2026 results as supplied claims, not independently verified box scores. Several underlying files are referenced but not provided.

## 1. What the results actually show

- **Live gate performance is barely observed.** `postmortems/2026-11-01_1pm.md` reports one vetted leg, Tre Tucker receptions, which lost; the 4 PM postmortem reports no vetted legs at kickoff. MNF’s original `r3` gate cut all **23** candidates. A largely abstaining policy may control losses, but these observations cannot demonstrate profitable selection.
- **Cut accuracy is not economic value.** Good cuts were **63/124 (50.8%)** early, **35/51 (68.6%)** late, and **15/23 (65.2%)** on MNF. These mix thresholds, odds, markets and repeated players. Rejecting a bet that subsequently wins can still be correct; rejecting a loser can still be poor ex ante.
- **Winning legs did not produce winning portfolios.** Sunday’s reported placed legs total **26–19 plus one push**, yet all listed Sunday tickets ultimately lost except the Walker single. MNF was **13/20**, while the $75 and $20 slips lost. This demonstrates payout and concentration risk—not necessarily predictive skill.
- In `backtests/mnf_chi_sea_replay_2026-11-03/`, **12/19 = 63.2%**, but ROI is approximately **−1.36%** on $190 staked. Six winning JSN yardage rungs share one outcome; reception rungs add further dependence. Nineteen legs are nowhere near nineteen independent experiments.

The replay’s “$0 risked versus −$95” is a hindsight loss-avoidance comparison, not evidence of positive expected return.

## 2. The original experiment is not cleanly graded

The opening Week 7–8 yardage selections are not reconciled to an immutable settlement ledger. Later reporting shifts among cuts, leans, vetted bets, user bets, alternative lines, receptions, TDs, sides and **5–8-leg** slips—outside the stated 3–4-leg yardage program.

A material example: the opening Puka selection is **over 84.5 receiving yards**. The 4 PM report celebrates placed **69.5** and **60+** wins against a reported **80 yards**. The original 84.5 selection would lose under that reported result. These cannot be interchangeable evidence.

**Fix:** assign every original selection a permanent ID containing market, direction, line, price, book, timestamp, policy version, stake, slip ID and settlement. Report original recommendations separately from later alternatives and user overrides. Preserve withdrawn recommendations rather than replacing them.

## 3. Outcome-driven rule changes contaminate the replay

The MNF replay uses **“current” `tools/sim_v6.py`**, revised rules and an expanded **209-leg** pool after the game. The documentation does not establish which components were frozen beforehand.

Examples of outcome-conditioned development include:

- Weather fixtures requiring cuts to specific ATL/TB receiving overs.
- A backup-CB exception supported by **“2/2”** examples.
- Zone-hole and mirror-over rules motivated by Loveland/Burden/Odunze results.
- Candidate expansion after Emmett Johnson’s **128 receiving yards**.
- New restrictions after losing QB unders and Walker rush/TD bets.

These are legitimate discovery observations, but replaying the same games cannot validate the changes. User approval does not prevent statistical overfitting. A regression fixture can verify intended software behavior while merely encoding yesterday’s winners.

Further concerns:

- The replay waives a failed run-level **“film”** requirement. Report strict and waived results separately.
- “Kickoff minus 30 minutes” prices require archived snapshots, not reconstructed quotes.
- A DraftKings-priced Darnold leg sits inside a nominal FanDuel pool; executable price provenance must be explicit.
- **406 passing tests** establish implementation consistency only, not profitability or freedom from leakage.

Freeze these revised rules now; evaluate them only on untouched future windows.

## 4. Several explanations overstate what the data identify

**Weather:** A **76%** rain forecast and seven losing receiving overs do not validate a **50% precipitation/20 mph** cutoff. NE–MIA’s **53–69%** forecast with reported zero rain illustrates forecast uncertainty, not necessarily a bad forecast. Model probability, expected intensity and sustained wind separately; archive the forecast available when betting. Actual weather belongs in outcome analysis, not reconstructed pregame inputs.

**Game script:** “Favored by 6+” and “under ~30 attempts” are plausible features, not validated hard gates after DET/DAL/LAR. Blocking all trailing-underdog QB unders is especially crude: expected catch-up volume should already affect the distribution and price.

**Injuries:** Lamar’s first-throw injury supports concentration stress-testing, not proof that a returning-QB rule would predict that event.

**Coverage:** Tacklers and inferred pregame assignments cannot identify the defender responsible for coverage. The files acknowledge this, yet defender-level narratives still lean on those tags. Use verified coverage data or label the mechanism unverified.

**Play-calling:** MNF’s observed run/pass EPA is descriptive, not a causal comparison of available choices. Situation and selection differ; a later interception cannot simply be charged to preceding runs.

## 5. Data integrity needs repair before further modeling

`postmortems/2026-11-03_MNF_CHI_SEA.md` reports:

- **17 runs/40 dropbacks** in its EPA section versus **19/37** in the quarter table.
- **Nine** trailing-by-9+ runs versus **ten** later.
- A Week 8 nflverse identifier stored under `playlogs/2026_wk9/`.
- Burden corrected from **3–41** to **7–56**.

Define scrambles, sacks, kneels, penalties and pre-snap score consistently; reconcile play IDs and recompute EPA summaries. Version corrections and rerun every affected grade.

The quoted training-data denial is also **not a leakage audit**. It does not supply the requested cutoff and cannot inspect the earlier session. Training knowledge, browsing, local files and conversation context are separate exposure channels. Preserve complete prompts, tool outputs, model identifiers and timestamps; obtain cutoff information from authoritative model documentation rather than unsupported self-report.

## 6. Concrete replacement protocol

1. **Freeze scope:** yardage only, executable prices, 3–4 legs, explicit push/void/payout rules. Separate singles and slip performance.
2. **Pre-register comparisons:** market baseline, raw model, existing gate and each proposed modification. Log all candidates and every attempted rule—not only selected examples.
3. **Walk forward chronologically:** fit on past weeks; freeze before the next window. Treat already examined games as development data.
4. **Validate distributions and economics:** calibration, proper scoring rules and net returns after vig/platform payouts. Audit probability coherence across alternate rungs; different prices can legitimately produce different accept/reject decisions.
5. **Model joint exposure:** player/game/QB/weather dependencies, shared legs and portfolio drawdowns. Use game/week-clustered uncertainty; do not count nested rungs as independent evidence.
6. **Audit model coherence:** reconcile Loveland’s reported **25-yard median at 30% target share** through attempts, targets, catch probability and yards per catch. Use only role information available before kickoff.
7. **Test fixes through ablations:** exposure caps, weather adjustments, zone features and role checks separately, then combined. Favor calibrated soft adjustments over accumulating outcome-specific vetoes.

**Conclusion:** the chunk supports better logging, role verification and risk controls. It does not yet support the revised rules’ predictive mechanisms or a profitable betting edge.

## Review of Rico's ChatGPT MNF audit (vs backtest data)

## Bottom line

**Keep research/data-quality fixes; do not use one game to loosen selection gates.** The backtest supports caution about more overs and less shrink—not “change now.”

**N1/N2 limitation:** Their definitions were not supplied. I cannot honestly certify whether a proposal reverses either. The YES/NO column below covers **identifiable** approved-rule reversals; N1/N2 compatibility remains unverified, and no implementation should bypass them.

| Audit proposal | Does our evidence support it? | Undo an approved rule? YES/NO* | Verdict |
|---|---|---|---|
| Replace last-4 **3-of-4** eligibility with a warning plus opportunity review | **Not supported.** One missed winner does not validate a weaker gate; aggregate results argue against broader admission. No isolated test of this rule supplied. | **YES — §7 3-of-4.** | **Reject** as a production change; research rejected candidates without admitting them. |
| Replace positional averages with routes, alignment, coverage, QB tendencies and volume | Sensible research improvement, but no evidence these inputs improve predictions or returns. The unsuccessful pro-edge version warrants caution, not causal attribution. | **NO**, if existing eligibility and pricing gates remain. | **Test-first** for predictive weighting; keep better descriptive research. |
| Replace WR3/WR4 exclusion with opportunity ranking | **Not supported.** Risks admitting more receiving overs into an already weak, overs-heavy system. Actual usage may justify studying exceptions, not authorizing them. | **YES — #3/#4 depth-receiver rule.** | **Reject** live relaxation; shadow-test only. |
| Replace 30%/50% reductions with calibrated adjustments | Supports **testing**, not reducing shrink by default. NO-SHRINK worsened calibration; no supplied evidence identifies an optimal percentage. | **NO** identifiable reversal; exact N1/N2 constraints unknown. | **Test-first** against current shrink and market baselines. |
| Separate tackler from coverage defender; repair defensive database | Sound attribution correction. No supplied evidence establishes betting uplift, but tackling does not establish coverage responsibility. | **NO** identifiable reversal. | **Keep** factual separation, provenance and explicit unknowns. |
| Replace mandatory verified primary defender with matchup-confidence levels | Zone-aware descriptions are reasonable. Allowing uncertain coverage to satisfy an eligibility requirement is a separate, unvalidated relaxation. | **NO** identifiable reversal; **N1/N2 unresolved**. | **Test-first** for eligibility; keep confidence labels without bypassing gates. |
| Replace RB <60% carry-share rejection with broader opportunity review | No isolated evidence supports this. The only steady positive is **main rush-yards unders**, so avoid changes that displace or dilute that signal. | **NO** identifiable reversal; **N1/N2 unresolved**. | **Test-first**, separately by market and side. |
| Evaluate expensive alternates by probability rather than automatically reject | Correct to evaluate price, but the approved rule is a **flag**, not a stated automatic ban. Weak model calibration makes model-only overrides unsafe. | **NO**, provided the **-250-or-shorter flag remains**. Removing it would undo approval. | **Keep** price review **with** flag and existing edge/risk requirements. |
| Use `SCHEME_EDGE` to trigger further research, not automatic approval | Compatible with the approved flag. No evidence establishes that scheme narratives justify additional bets. | **NO**, if review cannot override §7, depth, price or N1/N2 gates. | **Keep** research-only interpretation; **reject** any implied gate exemption. |
| Reject removing all shrinkage | **Directly supported:** NO-SHRINK worsened calibration. | **NO** identifiable reversal. | **Keep** shrink; test strengths rather than assume less is better. |
| Reject forcing Loveland/Burden/Odunze onto the card | Supported by sound evaluation design: selecting yesterday’s winners is outcome-fitting, not validation. | **NO**. | **Keep** rejection of forced inclusions. |
| Add opportunity → matchup → script → line probability → decision workflow | Useful organization, but not proof of predictive improvement. Opportunity-first must not become gate-last-and-optional. | **NO**, if all approved gates remain mandatory. | **Keep** workflow/logging; **test-first** any new probability model. |
| Record rejection reasons for every eliminated selection | Improves auditability without requiring more bets. A rejected winning leg is not automatically an error. | **NO**. | **Keep**. |
| Compare original/revised models using pregame-only information | Strongly appropriate. CHI@SEA is development evidence, not an independent validation sample. | **NO**. | **Keep**; require untouched chronological evaluation. |
| Test NBA separately; verify repository changes independently | Appropriate scope control and implementation hygiene; NFL hindsight cannot validate NBA shrink changes or prove code was installed. | **NO**. | **Keep**. |

### Evidence and release requirements

- **Confidence constraint:** Every simulation version had worse Brier scores than market **0.248** and coin flip **0.250**. A claimed model edge is therefore not sufficient evidence for admission.
- **Direction matters:** v6 READS returned **42.3%, −19.1% ROI**; overs **41.1%, −22.0%**; GATED **41.5%, −21.6%**; slips **0/30**. These results reject confidence in wholesale loosening, but do **not** isolate which individual rule caused losses.
- **Protect, don’t extrapolate:** Main rush-yards unders were **296–229, 56.4%, +2.8%**, positive/flat in five of six weeks. Preserve that benchmark; it does not establish that all unders are profitable.
- **Testing controls:** Freeze **N1, N2, #3/#4, -250 flag, §7, +3 vs no-vig, SCHEME_EDGE, mirror overs, no TDs and no passing yards**. Test exceptions separately, with side-specific calibration, ROI, sample size and uncertainty—not hindsight “missed winners.”
- **Before release:** Obtain N1/N2’s exact text. No unresolved compatibility finding should count as approval.

*“NO” means no identifiable reversal from the supplied definitions—not verified N1/N2 compliance.*