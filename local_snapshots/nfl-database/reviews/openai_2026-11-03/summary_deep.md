# Deep-dive OpenAI review: top 10 ideas (gpt-6.1-sol, Nov 3 2026)
Files: response_deep.md (final synthesis), section_reviews.md (4 chunk reviews + ChatGPT-audit review), section_digests.md, brief_deep.md (v6 results first + full brief). Calls were paced 65-70 s apart under the 10k tokens/min cap. Usage: usage_log.jsonl.

**Verdict:** no version shows a reliable edge. Simplify, freeze, audit and shadow-test. Don't loosen gates to recover winners we remember.

1. **Reconcile the ledger before any new test.** v5's 31/51 vs "+17.2% on 40 priced", slips 4/29 vs 9/25, the 293 vs 463 pools, and alt rungs substituted for original lines. [test-design-only]
2. **Pre-register each test** (universe, placement time, rules, staking, success criterion), and make any amendment a new version. Treat all weeks we've already inspected (Weeks 1-8) as development data only. [test-design-only]
3. **Keep three buckets separate:** as-operated, reconstructed, and prospective. Log publish and retrieval timestamps for every input. LLM denials and masking don't prove the reads were blind. [test-design-only]
4. **Run paired shadow variants on the same games:** market only, plain main rush-yds unders, raw model, gates without mirrors, mirrors alone, and a prior-only calibrated model. [test-design-only]
5. **Keep shrinking toward the market.** Removing the shrink made calibration worse, and the 70-80% forecasts won 49.3%. Fit the shrink strength on earlier weeks only. [needs-Rico-OK: reverses NOSHRINK]
6. **Reject the ChatGPT MNF audit's two rule changes.** Swapping §7 3-of-4 for a warning undoes §7, and swapping the WR3/WR4 exclusion for an opportunity ranking undoes the #3/#4 rule. Shadow-test the rejected legs instead. Keep the -250 flag; the alt-rung review is fine only if the flag stays. SCHEME_EDGE stays research-only with no overrides. Calibration in place of the 30%/50% cuts and the RB <60% carry-share change are test-first. [needs-Rico-OK only if changed; recommendation is no change]
7. **Spend the ~250 credits a week on prospective snapshots** for bettable games only: placement-time quotes plus a true near-close quote, cached. A snapshot 29-39 minutes before kickoff isn't the close. CLV is supporting evidence, not proof. [test-design-only]
8. **Grade slips at the real FanDuel/PrizePicks payouts**, not multiplied singles prices. Track shared exposure (player, QB, script, weather). Stop drifting to 5-8 legs. At a 42.3% leg rate, 3-leg slips win about 7.6% and 4-leg slips about 3.2%. [test-design-only]
9. **8-step per-game checklist:** freeze scope → verify availability (timestamped) → opportunity/usage → honest matchup (no invented coverage; tackler ≠ coverage) → script and weather from the issued forecast → probability vs executable price plus gates → log every candidate and rejection → settle on the original line. [test-design-only as a shadow; needs-Rico-OK if it replaces phase steps]
10. **Treat main rush-yds unders (296-229, 56.4%, +2.8% on 421 priced) as the leading hypothesis** for a prospective test from Week 10 on. It's not proven. [test-design-only]

## Pushback
- **"Strict policy may yield no bets":** probably true, since the film and PFF gates can't be met on free data. Rico needs to choose between a versioned free-data successor and no live bets.
- **N1/N2 "undefined":** the compact brief excerpts didn't carry their text. Its "UNKNOWN" marks on N1/N2 are a gap in our brief, not a finding. We should check those two items against PHASE_SCRIPT ourselves.
- **Receptions "out of scope":** Rico has used catches overs (e.g. the NYG checkdown note). Whether they're in scope is his call, not the model's.
- **Credits:** it asks for opening, placement and closing quotes. On 250 credits a week, that's only affordable for the handful of games we'd actually bet.
- **No sample-size target:** unlike gpt-5.5, which estimated ~350-1,500 legs, it wouldn't give one because of clustering. Either way, one season of ~5 slips a week can't prove an edge, and that's why the plan leans on calibration and CLV.
