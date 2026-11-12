# v5: brainstorm-first Grok reads, Weeks 3–8 (lock c71af73, graded after)

**Structure change:** every RECONSTRUCTED read uses the betting-game-brainstorm 12-step format: GAME, SCRIPT (base case + 2 flips), INJURY FALLOUT, MATCHUP (shell, pressure, where the defense bleeds, primary target overlap), FORM, EDGE PLAYERS (≤2, with must be true, kills it and confidence), DATA CHECK (flag, not cut), MARKET+RUNG+price, PRE-MORTEM, SLIP STORY, and the step6/step12_limited flags. The earlier free-form reads were superseded and moved to superseded_oldformat/. They weren't used.

## Steps per leg (locked_picks.csv `steps` column)
- PRO_EDGE: **approximated.** edge_scan.py only works against the live API, so proedge.py reimplements it offline. It covers implied team totals, best saved price vs the anchor no-vig (betonlineag, then consensus; there is no Pinnacle in the packs), and lagging props where snapshots exist. The sleeper check is N/A because the packs have no structured injury data. It ran AFTER the reads as a gate or tag and was NOT fed into the Grok prompt, because of time and cost after the late steer.
- BRAINSTORM: **full** for all 88 games (grok-4.7, pack-only, validated).
- PHASE_SCRIPT: **approximated.** The main line and the latest saved price only. No 3-sim gate.

## Leg results (hit rate counts all settled legs; ROI uses $10 flat on priced legs only)
| Set | Train wk3–6 | Holdout wk7–8 | Holdout ROI (priced) |
|---|---|---|---|
| PRIMARY (saved where available, else Grok) | 49–63 (43.8%), −13.8% | 31–20 (60.8%) | 25–15, +17.2% |
| RECONSTRUCTED (Grok) | 43–58 (42.6%) | 30–18 (62.5%) | +20.2% |
| SAVED_READ | 6–5 (54.5%) | 1–2 | n is tiny |
| GROK_ON_SAVED_GAME (comparison) | 3–9 | 1–3 | −52.9% |
| ZONE_MOF | 44–58 (43.1%) | 29–18 (61.7%) | +19.8% |
| PRO_EDGE pass | 4–9 | 15–10 (60.0%) | +25.2% |
| Baseline: every main rush-yds under | 161–128, +4.3% | 70–62, −0.6% | |

Primary by week (W–L): wk3 11–21, wk4 12–17, wk5 15–10, wk6 11–15, wk7 16–10, wk8 15–10.
Primary holdout by market: recyds 15–12, rushyds 11–7, rushrecyds 5–1. Train by market: recyds 26–35, rushyds 16–20, rushrecyds 7–8.

## Slips (3–4 legs, ≤5 per week, $10 each, prices are independent products, so estimates)
PRIMARY: wk3 0/5, wk4 0/5, wk5 1/5, wk6 0/5, wk7 1/5, wk8 2/4. 4 of 29 won, +$145.38 (all of it from wk5, wk7 and wk8).
ZONE_MOF: 4 of 27 won, +$223.82. PRO_EDGE: 1 of 7 won, +$52.67.

## Targets (PRIMARY holdout)
- 100+ holdout legs: **FAIL** (51).
- 57%+: **PASS** (60.8%).
- +3% ROI: **PASS** (+17.2% on priced legs).
- No losing week: **PASS in the holdout** (wk7 and wk8 both up), but **FAIL across the full run** (wk3, wk4 and wk6 lost, and train is −13.8%).
- The holdout beating train by this much on a small n looks like variance, not a proven edge.

## Rico placed legs (outcomes.csv): see results.md
Yardage legs: rec yds 32/37 (86%), receiving yds 18/20, rush+rec 18/24 (75%), receptions 33/46, **rush yds 9/25 (36%)**. Ticket cash P&L: wk5 +197.72, wk6 +18.53, wk7 −193.87, wk8 −104.50.

Full tables are in results.md. Grok usage is in GAPS.md.
