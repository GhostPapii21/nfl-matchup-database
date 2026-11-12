# v6: brainstorm + pro-edge in the Grok prompt, then the data check (grok-4.7)

**Ghost6 should vet this before Rico sees it.** No bets were placed, no messages were sent, and 0 Odds API credits were used.

## Commits
- 2026 LOCK: `9308c91`. This holds 120/120 reads for Weeks 1–8 plus `locked_picks.csv`, which went through the gate before any grading. The leak test passed.
- 2026 GRADE: `84c7c73` (`results.md`, `graded_*.csv`).
- 2025: `finish25.sh` writes the LOCK and GRADE commits once `reads25.py` ends, whether it finishes or hits QUOTA_STOP. See `results_2025.md` and `finish25.done`.

## Method
1. For each game, the Grok prompt contains both SKILL.md files, betting-game-brainstorm (all 12 steps) and then pro-edge-scan, plus precomputed pro-edge inputs and a pre-kick-only data pack.
2. After that comes the data check: §7 3-of-4 with the current QB, edge of at least +3 vs no-vig (NOSHRINK), SCHEME_EDGE as a flag rather than a cut, N1, N2 (approximated), the depth rule, mirror overs, and a flag on prices of −250 or shorter. N3 is N/A.
3. Markets are rush, rec and rush+rec yards, main lines only. There are no TDs and no passing yards.

## 2026 results (from `results.md`; buckets are never blended)
| Set | (a) Wk3–8 priced | (b) Wk1–2 STAND-IN (hit rate only) |
|---|---|---|
| READS, all Grok legs | 66–90 (42.3%), ROI −19.1% on 139 | 29–27 (51.8%) |
| GATED (PASS+FLAG) | 49–69 (41.5%), ROI −21.6% on 110 | 20–12 (62.5%) |
| Baseline: every main rush-yds under | 296–229 (56.4%), ROI +2.8% | 66–41 (61.7%) |
| v5 RECONSTRUCTED, for comparison | 73–76 (49.0%); Wk7–8 holdout +20.2% | — |

- **By week, GATED (a):** 3: 8–14 · 4: 4–13 · 5: 4–14 · 6: 9–12 · 7: 12–11 · 8: 12–5 (+32.4%).
- **By market, GATED (a):** rec 37–47 · rush+rec 5–6 · rush 7–16.
- **Over/under, GATED (a):** over 44–57 · under 5–12.
- **READS overs vs unders (a):** overs 53–76 (−22.0%), unders 13–14 (−6.5%).
- **Slips, about 5 per week at $10:**
  - GATED 3–4 legs: 1 of 26 won, −$134.73. The only winner was in Week 8.
  - GATED 6–7 legs: 0 of 12 won, −$120.
  - READS 3–4 legs: 0 of 30 won, −$300.
  - READS 6–7 legs: 0 of 16 won, −$160.
- **(d) Saved vs reconstructed reads:**
  - SAVED_READ: 7–7, +16.9% on 8 priced.
  - v6 Grok on the same games: 4–14, −62.5%.
  - v6 Grok on all other games: 62–76, −13.8%.

**Verdict:** v6 underperforms both the rush-under baseline and v5. Putting both skills in the prompt pushes Grok toward overs, mostly receiving overs, and the gate doesn't fix that. Weeks 7–8 are positive, but the sample is small.

## 2025 (bucket c: HINDSIGHT RISK, STAND-IN medians, hit rate only)
Results are in `results_2025.md` once the run finishes. Week 1 is skipped because there's no 2024 pbp on the box. This bucket can't be compared with ROI.

## Grok spend
- 2026: $23.19 for 120 reads.
- 2025: running total in `usage_log_2025.jsonl`.
