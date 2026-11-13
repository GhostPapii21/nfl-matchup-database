VERDICT: APPROVE

1. **P3 — `simulate.py:1266`, `rare_plays.py:229`: Expose sampling-band usage in research results.** Events record `los_band`, but `simulate_games` discards those events without aggregating band counts. Report counts by kind/class, including `"all"`, so researchers can assess approximation exposure. Document that whole-pool fallback has **no 20-yard bound**.

2. **Earlier finding 1 — RESOLVED** (`simulate.py:875`; pass-1 #1, pass-2 #1). Automatic-first-down inference now requires historical down > 1, next down 1, and yardage short of the historical distance. Fakes use live snap mechanics.

3. **Earlier finding 2 — NOT RESOLVED in full; accepted research limitation** (`simulate.py:957`, `rare_plays.py:224`; pass-1 #2, pass-2 #2). Exact-LOS sampling eliminates translation when sufficiently populated, and anchored touchbacks fix the reported LOS-67 example. Non-touchback boundary enforcement remains approximate outside exact matches. This is acceptable for the capped, gated, off-by-default research feature, with explicit disclosure and band-usage reporting; it does not establish readiness for lock use.

4. **Earlier finding 3 — RESOLVED** (`rare_plays.py:333`; pass-1 #3, pass-2 #3). Clean punt return-TD rates use the eligible non-touchback population; empty populations remain unknown.

5. **Earlier finding 4 — RESOLVED** (`simulate.py:1462`, `simulate.py:1055`; pass-1 #4, pass-2 #4). Direct attachment requires a validated count, and `simulate_one` consumes and enforces the research budget.

Validation: **33 tests passed**, including off-mode golden reproduction. No protected files changed in the diff. No files modified or network used.