# v5.1 CODEX full rerun
Model gpt-6.1-sol (OpenAI Responses API, reasoning medium, json_object). Swap of model client only; packs (808dc89 v4 as-of, assert pbp week<w), SYSTEM_PROMPT, validator, 3-attempt retry identical to fresh/. 0 Grok calls, 0 Odds credits.
87/88 games read (w5_CIN@MIA dropped after 3 validator rejects). Reads sha256-locked in reads_LOCK.sha256 before grading.
Spend est $8.92 at assumed $5/M in, $40/M out (388,462 in / 174,537 out tokens, 92 requests) - token counts exact, $ rate assumed.
Pre-registered selector (strong+agree): model tagged only 3/149 legs strong -> 1 graded leg -> FAIL/INSUFFICIENT. results.md.
Nov-4 rules + exploratory lean|strong arm: results_today_rules.md (POST-HOC, disclosed). §7 needs 4 prior games so Wk3-4 legs all fail §7.
Not apples-to-apples with Grok reads (different model).

## Ghost6 vet fixes (Nov 4, no model/OpenAI/Odds calls)
- LOCK ORDER: the read lock (reads_LOCK.sha256) and the grading landed in the SAME commit (3369e16), so lock-before-grade is NOT demonstrated for this run. Future runs: commit the lock in its own commit before any grading.
- SPEND: $8.92 is an ESTIMATE. Token counts are exact (388,462 in / 174,537 out, 92 requests); per-token prices ($5/M in, $40/M out) are assumed, not billed figures.
- today_rules.py: N1 now RB rushyds OVERS only (matches review-branch rico_nov2_rules B13; rushrec and unders exempt); games played from nflverse snap counts (offense_snaps>0) with zero-touch games kept as 0; UNRESOLVED legs listed explicitly; Rico +1/+3 anchored-edge tiers added as arm CT (anchored p from avg3 Platt on sims_replay Wk6-8; no sim = no model edge = cut).
- spec.md baseline: priced bar = 231-190, +2.8% on 421 priced legs; 296-229 is the all-legs (incl. unpriced) count.
- All results here are EXPLORATORY / post-hoc, not evidence of an edge.
