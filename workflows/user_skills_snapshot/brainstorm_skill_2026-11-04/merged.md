# Merged review: betting-game-brainstorm (2026-11-04)
Sources: openai_review.md (gpt-5-2025-08-07, ~$0.06) and superpowers_review.md.

## HEADLINE
Both reviewers found the file on disk still says data "can cut" a read (L9, L20, L100, L131). The scenario-first rewrite is **not in the saved file** (no miss audit, no flip-flop rule, no flag-only gates). Fix that first.

## Both agree
- Strengths: read-before-data + one-sentence edge (L13); Step 4c ladder order; 5b small-sample "flag, don't cut"; READ vs RESULT grading (Step 12) + pre-mortem; 70-80%→50% calibration warning.
- L20/L100 "cut" language permits the Washington reversal; must become flag-only with a short explicit hard-cut list.
- Step 5 recent form needs an explicit "cross-check, never a veto" role.
- Double-counting risk: one root cause (3rd-string QB) bumped at plays, share and efficiency; needs a single causal chain + lead-script pass-rate offset.
- Miss audit must use fixed causes and be graded, or it becomes an excuse machine.
- Scenario drivers need tracking/calibration (by label and by driver).
- House gates must be written in, with flag vs hard-cut status.

## Only one raised
- OpenAI only: price realism tied to labels; stronger pre-mortem (two concrete disconfirming facts, not a narrative); single-story check per slip; weather hard-cut. **Caution:** its numbers (−3% EV cut, ≥20 mph, strong = −120 fair, "within 1% of no-vig") are invented, not house rules - Rico should set or reject them.
- Superpowers only: file contradiction L20/L100 vs L85; no flip-flop rule (reversal needs a new dated fact); description summarizes workflow; no rationalization table/red flags; untestable words ("clearly", "close", "strong"); miss-audit cap; rush-under track record should be stated and scenario receiving overs tracked separately; skill was never pressure-tested.

## Disagreements
- **Lean disagreement:** OpenAI keeps "drop/pass" on leans; superpowers would flag. Minor.
- **Pricing as a hard cut:** OpenAI makes bad price a hard cut with numeric thresholds; superpowers keeps best-price shop as the existing house rule without new thresholds.
- **Miss audit wording:** OpenAI: "only veto if the same cause is present again" - that re-arms the game log as a veto (WEAKENS FLAG below). Superpowers: a present cause lowers the projection inside the read, and gate conflicts still go to Rico.

## Ranked edits (Rico/Ghost to apply; file untouched)
1. **GUARDRAIL - Ground rules L20 + Step 8 L100 + description L9 + output L131.** Replace L20 with: "Data never cuts a scenario read by itself. Disagreements (game-log counts, 3-of-4, last-2, sims, edge tiers) are FLAGS shown to Rico with the reasons. Only these can cut: a confirmed inactive/snap limit, the N1 rush-over rule (<60% projected carries), no acceptable price after the best-price shop, and the 3-4 leg slip cap." L100 → "Disagree on a strong read: FLAG with the miss audit; Rico decides." L131 → "AGREE / FLAG / HARD-CUT(reason)". Description: end at "...weather." (drop "which can cut it").
2. **GUARDRAIL - new Ground rule (no flip-flop).** "Once a read is written, you may only reverse it by naming a new fact dated after the read (injury, inactive, price, weather, role news). Re-reading a game log is not a new fact."
3. **GUARDRAIL - Step 5 role + miss audit.** Retitle "Step 5. Game-log cross-check (never a veto)". Add: "For every game the player missed the line, record ONE cause from this list: blowout/lead script, low possession, injury/snap limit, coverage lockdown (tested per 4c.7), QB change, fluke/TD. Then say if the cause is present Thursday per the read's own inputs. A cause that is present lowers the projection inside the read; it does not cut. If you can't name a cause from the list, write 'unexplained' - two or more unexplained misses in the last 5 is a FLAG to Rico."
4. **GUARDRAIL - Step 4c new item 8 (one causal chain).** "Build the number once: plays → dropbacks (with lead-script pass rate) → target share → catch rate → yards. Each matchup factor adjusts only ONE link, and you must name which. If the base script has the team leading, lower the second-half pass rate."
5. **STRENGTHEN - Step 12 calibration.** Add: "Log each read's drivers (plays band, blitz rate, target share, leak) and grade each right/wrong. Keep hit rate and ROI at the price taken by confidence label, and separately for scenario-built receiving legs vs rush unders (the only proven edge: 231-190, +2.8% on 421)."
6. **STRENGTHEN - Step 10 falsifiers.** Replace first sentence with: "Before kickoff, write two checkable facts that would prove the read wrong (e.g., 'JAX runs <58 plays', 'Washington <6 targets by the end of Q3'). The pre-mortem is about the read, not the game log."
7. **GUARDRAIL - new Step 8a house gates.** "3-of-4 line check, last-2 downgrade, edge tiers: flag only. N1 <60% carry rush-over: cut. Best-price shop: required. Slips: 3-4 legs, one story."
8. **STRENGTHEN - Step 7 definitions.** "Strong = every ladder layer points the same way and the projection beats the line by a margin Rico sets; Lean = most layers agree." (Leave the margin to Rico; don't adopt invented thresholds.)
9. **STRENGTHEN - add a Red Flags list** (writing-skills): "'He's only 2 of 5' / 'the log says' / reversing after the read without a new fact / adding plays AND share AND efficiency from one cause / excusing every miss."
10. **STRENGTHEN - test it.** Run a 5-rep micro-test: read + contradictory 2-of-5 log; pass = agent keeps the read and flags.

## WEAKENS SCENARIO-FIRST - Rico decides
- OpenAI's "only veto if the same cause is present again" (its edit M): turns the miss audit back into a veto path. Recommended: present cause adjusts the projection, it doesn't veto.
- OpenAI's "disagree on a lean: usually pass" and new hard cuts (−3% EV, 20 mph wind, price-to-label mapping): add cut paths Rico hasn't approved.
- Edit 3's "2+ unexplained misses = FLAG" and edit 4's lead-script offset will sometimes lower a scenario projection (Washington's Week 8 blowout pattern). They're guardrails, but they push against the read.
