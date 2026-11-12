# Test C — 4–5 leg slips, Weeks 6–8 + MNF rulebook replay (TEST ONLY)
Requested by Rico via Ghost6 (Nov 3, 6:13 AM ET). Base: commit 57d1eb8. **Zero Odds API credits** (saved prices only; no network calls).

## Method
- Same pool: 463 legs (`pool==True` in ../graded_legs.csv: gate leg-pass, no door BLOCK).
- Same slip method as Tests A/B (../slip_method.txt, written before grading). `run_test_c.py` copies the slip/door code from ../grade_slips.py verbatim; the only change is sizes `('C',(4,5))` instead of A=(3,4), B=(6,7).
- M1 cross-game greedy + M2 sequential chunks, each leg once per (method,k), price = product of own-book decimals, $10/slip.
- Check: Test C k=4 slips are identical to Test A k=4 (same legs, results, profit) — expected, since the method is size-deterministic.

## Headline
**187 slips, 8 won (4.3%), −$987.79 on $1,870 (ROI −52.8%).**
- k=4: 104 slips, 6 won, −$377.41. k=5: 83 slips, 2 won, −$610.38.
- 40 slips lost by exactly one leg.

## By week
| week | slips | won | hit | P/L |
|---|---|---|---|---|
| 6 | 55 | 5 | 9.1% | −$70.12 |
| 7 | 72 | 0 | 0.0% | −$720.00 |
| 8 | 58 | 3 | 5.2% | −$177.67 |
| MNF | 2 (M2 only) | 0 | 0.0% | −$20.00 |
| **all** | **187** | **8** | **4.3%** | **−$987.79** |

| week | M1 k4 | M1 k5 | M2 k4 | M2 k5 |
|---|---|---|---|---|
| 6 | 15, 1, −$81.81 | 12, 1, −$8.74 | 16, 2, +$32.07 | 12, 1, −$11.64 |
| 7 | 20, 0, −$200 | 16, 0, −$160 | 20, 0, −$200 | 16, 0, −$160 |
| 8 | 16, 2, +$116.31 | 13, 0, −$130 | 16, 1, −$33.98 | 13, 0, −$130 |
| MNF | — | — | 1, 0, −$10 | 1, 0, −$10 |

## By market (legs inside Test C slips)
| market | legs | W–L | hit | slips killed | only loser |
|---|---|---|---|---|---|
| rec under | 236 | 124–112 | 52.5% | 82 | 12 |
| recyds over | 146 | 62–84 | 42.5% | 70 | 8 |
| recyds under | 163 | 93–70 | 57.1% | 57 | 6 |
| rec over | 106 | 57–49 | 53.8% | 42 | 11 |
| rushyds over | 63 | 35–28 | 55.6% | 28 | 0 |
| passyds over | 28 | 8–20 | 28.6% | 20 | 3 |
| rushyds under | 77 | 57–20 | 74.0% | 20 | 0 |
| passyds under | 12 | 0–12 | 0.0% | 12 | 0 |
(Leg counts repeat legs reused across method/size; "slips killed" = distinct slips with ≥1 losing leg in that market.)

## Comparison
| test | sizes | slips | won | hit | staked | P/L | ROI | door leg-level |
|---|---|---|---|---|---|---|---|---|
| A | 3–4 | 245 | 20 | 8.2% | $2,450 | −$1,070.42 | −43.7% | 245 PASS |
| **C** | **4–5** | **187** | **8** | **4.3%** | **$1,870** | **−$987.79** | **−52.8%** | 104 PASS / 83 SLIP_SIZE |
| B | 6–7 | 124 | 2 | 1.6% | $1,240 | −$428.71 | −34.6% | 124 SLIP_SIZE |
Week 7 lost every slip in all three tests. No size is profitable.

## Door stamps
- Strict: 0/187 stamped (all BLOCKED on GATE_PASS — no replay film source; the 83 five-leg slips also hit SLIP_SIZE).
- Leg-level: 104 PASS (all 4-leg), 83 BLOCKED on SLIP_SIZE (all 5-leg; door limit 3–4). Warnings: SHORT_PRICE 34, SCHEME_EDGE 11.

## Caveats (carried over)
- Sharp man/zone is hindsight for Weeks 6–7 (Oct 27 table); stale for Week 8 under 48h.
- Odds credits were under the floor in the original pull, so some alt events are missing.
- MNF Bears RB sim skipped. M2 allows same-game legs priced as a product (real SGP pays less).
- Alt no-vig is a proxy.

Files: run_test_c.py, slips.csv (door output), slips_graded.csv, by_week.csv, by_market.csv.
