# v5 leak audit: did Grok (grok-4.7) pick Weeks 7–8 blind?

**Verdict: CLEAN, as far as these tests can show.** The tests found no sign that Grok knew the results. The 31–20 holdout still rests on a small sample, so it is **not proven to be an edge**.

## 1. Prompt audit (prompt_audit.py, prompt_audit.csv)
- 33 checks, **0 leaks**. The checks covered all 27 Weeks 7–8 prompts and, for each pack, the PBP weeks plus the timing of every prop and game-line quote.
- PBP in the packs: Week 7 used weeks 1–6 only and Week 8 used weeks 1–7 only. The L3 windows never include the target week.
- Prop quotes: 0 of 2,553 (Week 7) and 0 of 2,330 (Week 8) were taken at or after kickoff. The closest was 0.5 h before kickoff. Game lines: 0 of 616 and 0 of 572.
- The Week 8 checklist excerpts were built 2026-10-29 at 05:25 EDT, before the first Week 8 kickoff (TNF, 8:15 PM ET). None of the prompts contain scores, recaps or result words.
- Caveat 1: the prop list comes from snapshots taken up to about 30 minutes before kickoff. That can reveal late inactives, but that is legitimate pregame information.
- Caveat 2: the v5 ZONE_MOF tag (GAPS.md) used a snapshot through Week 7, which is a hindsight tag. It was not used in the Grok prompts.

## 2. Knowledge-cutoff probe (probe.py, probe_forced.py)
- Strict mode (answer only if known): Grok marked every item unknown. That was 27 of 27 holdout game scores, 12 of 12 early-2026 scores, 10 of 10 2025 scores and 51 of 51 leg stat lines. It correctly refused all 12 fake games and fake player-games.
- Forced best guess:
  - Winner picked correctly: 14 of 27 holdout games, 7 of 12 early-2026 games and 4 of 10 2025 games, which is coin-flip level. 0 exact scores, and recall=true on 0 items. It flagged 4 of 6 fake games as never played.
- Leg stat guesses: 0 exact and 4 of 51 within 10 yards. The guesses missed by 69.6 yards on average, while the betting line missed by 29.3. The guessed side matched the real outcome only 39% of the time.
- Positive control: it correctly gave Super Bowl LVIII (KC 25–22 OT) and Super Bowl LIX (PHI 40–22). It said "unknown" for Super Bowl LX and for 2025 Week 1, and described its knowledge as reliable "through early 2025". **Its knowledge ends before the 2025 season.**

## 3. Recall vs hit split
- Grok recalled 0 of 51 legs, so all 51 fall in the "not recalled" bucket, which went 31–20 (60.8%). There is no recalled bucket to compare against, and no hits can be explained by memory.

## 4. Masked rerun (masked.py, masked_reads/, masked_picks_graded.csv)
- Setup: 16 of the 25 Grok-read games (8 from Week 7, 8 from Week 8), drawn with a seeded random sample. Teams became AWAY/HOME, players became PLY codes, and week numbers and dates were removed. The system prompt, skill and stats were the same as v5. The Week 8 saved-checklist excerpt was dropped because it is full of names. Picks were written to disk before grading.
- The original v5 legs in those games went **21–8 (72%)**. The masked legs went **24–8 (75%)**. 14 legs were identical and 15 used the same player.
- By side, masked went overs 17–7 and unders 7–1. The original went overs 19–7 and unders 2–1.
- **The hit rate did not drop after names were hidden.** Recall would need names, so this points to reasoning from the numbers, not memory.
- These 16 games ran hotter than the full holdout (72% vs 61%), so the sample is lucky.

## 5. Direct question (direct_answer.md)
> "No. I did not know the actual outcomes of those 2026 Week 7 or Week 8 games or player stat lines when those picks were made, and I do not know them now from training data."

This is weak evidence on its own, but it matches tests 2–4.

## Caveats
- n = 51 legs (29 and 32 in the masked set). A 95% interval on 31 of 51 runs roughly from 47% to 74%. The training weeks (3–6) went 43.8%.
- "Clean" means no leakage was found. It does not mean v5 has a real edge. The honest next step is still the live Week 10 paper test.
- A note on the method: Weeks 7–8 sit after its knowledge cutoff, so the masked rerun was mainly a check on how stable the picks are.

## Cost
- About **$1.71**, from xAI's cost_in_usd_ticks across 27 logged calls in usage_log.jsonl. Odds API credits used: 0.
