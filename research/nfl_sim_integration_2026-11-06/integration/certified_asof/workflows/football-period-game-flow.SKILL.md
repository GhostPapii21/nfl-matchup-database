---
name: Football period game flow
description: >-
  Use with betting-game-brainstorm and NFL script checklists whenever analyzing
  quarter/half winners, spreads, totals, team totals or game flow.
---
# Football period game flow
Run alongside betting-game-brainstorm, nfl-betting-script and nfl-game-script-run; never replace their rules.

1. Record exact market, period, line, both-side prices, timestamp and source. Distinguish standalone quarter scoring from cumulative halftime scoring, 3-way winner from 2-way moneyline, tie loss from push, and overtime treatment. A screenshot is valid quote evidence, not proof of edge.
2. Write scenario-first Q1–Q4 flow: possessions, pace, field position, scoring opportunities, expected score/margin bands, lead/trail play calling and halftime adjustments. Include base and two plausible flips; do not divide full-game points into arbitrary quarter fractions.
3. Reconstruct period scores and possessions from public play-by-play; reconcile to official box scores. For each exact threshold show clears/eligible games, ties/pushes and dates. Keep quarter and half samples separate. Explain misses and whether causes recur now. Historical hit rates cross-check the scenario; they do not veto it alone.
4. Compare relevant conditions: starting/backup/returning QB, offensive line and skill injuries, defensive replacements, home/road, travel/rest/time zone, kickoff window, opponent strength, coaching/personnel regime, wind/rain/temperature and roof status. Use only information known pregame. Separate all-game baseline from matched subsets; show sample sizes and overlapping filters, avoid cherry-picked tiny subsets and flag confounding. Missing historical injury/weather inputs stay missing.
5. Translate each factor into an explicit, sourced adjustment or an uncertainty flag—not an invented numerical effect. Connect period flow to player volume, receiving routes and defensive matchups. Multiple receivers may succeed; no automatic one-check-down cap.
6. For quantitative grading, use a verified period-capable scoring/possession engine. Clearly distinguish actual independent model families from scenarios and random seeds. Report model probabilities, score/margin medians and intervals, base/flip sensitivity, data dates, sample limitations and out-of-sample calibration. Never claim calibrated edge from an unvalidated scenario simulator.
7. Compare to both-side no-vig probability and executable price; use the actual SGP quote for joint value, not multiplied marginal odds. Model correlations explicitly or mark joint probability unavailable. Higher payout alone is not value. Missing engine support remains a model gap, not a fabricated PASS.
8. Feed genuine period outputs and source evidence into the existing gate interface. Do not relax approved rules, fabricate fields or silently convert stat/edge flags into cuts. List missing inputs and user decisions separately from the football read. No bets or publishing.
9. Before kickoff log testable period drivers (possession/scoring bands, early lead, pressure and script changes). Afterward grade each quarter/half prediction and each market separately, including price, ROI and calibration. Never change rules automatically.

Output: exact market/settlement; quarter-by-quarter base/flip flow; conditional historical clear counts and miss causes; injury/location/time/weather adjustments; each genuine model result and validation status; fair-vs-book pricing and actual SGP quote if available; uncertainty, gate gaps and postgame driver ledger.
