# Superpowers review: betting-game-brainstorm SKILL.md (2026-11-04)
Method: writing-skills (match form to failure, close loopholes, rationalization table, testable rules, description = triggers only) + requesting-code-review (strengths / Critical / Important / Minor / verdict). Reviewed file as it sits on disk (135 lines, read-only).

## CRITICAL finding first
**The file on disk does not contain the scenario-first rewrite.** No "scenario beats box score" rule, no miss audit, no "no flip-flopping" rule, no "gates flag only". The opposite language is still live:
- L9 (description): "then tests it with data, which can cut it."
- L13: "The read is a hypothesis; data tests it."
- L20: "Data that clearly disagrees with a read can cut it; close calls get flagged."
- L100: "Disagree on a strong read: cut it if the data gap is clear."
- L131: output allows "cut".
Either the edit wasn't saved or it went to a different path. As written, this file still authorizes exactly the Washington reversal (a 2-of-5 log is "clearly disagreeing data"). Verdict: **Not ready**; the rewrite must actually land.

## 1. Strengths
1. Read-before-data ordering with a one-sentence edge test (L13) - a falsifiable minimum.
2. Step 4c ladder forbids naming receivers until possession/pressure/targets/routes/coverage are done (L61) - this is the scenario-first engine.
3. 4c.7 "lockdown claims must be tested" - a real anti-narrative check that applies to defenders too.
4. Step 5b small-sample rule: flag to user, don't quietly cut (L85) - already the flag-not-cut principle in miniature.
5. Step 12 grades READ separately from RESULT; Step 10 pre-mortem; Step 8's 70-80%→~50% calibration warning.

## 2. Important issues (judgment risk / ambiguity)
- **I1. Contradiction between L20/L100 (data cuts) and L85 (small sample flags).** An agent picks whichever supports its mood. Need one rule: what can cut, listed exhaustively.
- **I2. Step 5 "recent form" has no defined role.** It sits between the ladder and the edge with no instruction that it's a cross-check. Agents will treat hit/miss counts as evidence of equal weight. This is the slot the Washington reversal came through.
- **I3. No miss audit exists, and if added loosely it becomes an excuse machine.** Needs: causes from a fixed list, cause must be checkable pre-game, and a cap (if >half of misses are "excused", flag the read as weak).
- **I4. Double-counting.** Possession (4c.1), pressure (4c.2), target ladder (4c.3) and leaks (4c.6) can each be applied as a separate bump off one root cause (third-string QB). No rule says build the number once through plays→dropbacks→share→catch rate, and lead-script pass-rate drop (the Week 8 blowout pattern) isn't required as an offset.
- **I5. Scenario reads aren't calibrated.** Step 12 grades read vs result but there's no tally by confidence label, no driver-level grading (was plays band right? was blitz rate right?). Without it, scenario-first can't prove it beats the box-score approach that lost money.
- **I6. Untestable words:** "clearly disagrees", "clear data gap", "close", "strong/lean", "stands out and repeats". Define with observable predicates (e.g. projection vs line gap, or a named number).
- **I7. House gates not encoded.** The skill never names 3-of-4, last-2 downgrade, N1 <60% carry cut, tiers flag-only, best-price shop. "Sits in front of nfl-game-script-run" (L15) means those later gates can still cut what this skill said to keep. Must say which gates are flags (3-of-4, last-2, tiers) and which remain hard rules (N1 rush-over cut, best price, 3-4 legs).
- **I8. No rule against flip-flopping.** Needs: once a read is written, reversing it requires naming a NEW fact (injury, price, weather, role) dated after the read. Re-reading the same game log isn't new.
- **I9. Track-record not used.** Rush unders are the only proven edge (231-190, +2.8%) - skill should say scenario-built receiving overs are unproven and get tracked separately/sized smaller until they show a record.

## 3. Minor
- Description summarizes workflow (writing-skills says description = triggers only; agents follow the summary instead of the body - and the summary currently says "can cut").
- 135 lines, well over the ~500-word target; consider moving examples (L29-31) out.
- No rationalization table / red-flags list - this is a discipline skill (the agent knew the read and abandoned it under a stats pull), so per writing-skills it needs one.
- Not tested: no pressure scenario (e.g. "here's a good read + a 2-of-5 log, decide") was run before/after. Recommend a 5-rep micro-test.

## Verdict
Strong scaffolding, wrong governing rule on disk. Land the rewrite, then add guardrails I3-I5/I8 so scenario-first can't become storytelling.
