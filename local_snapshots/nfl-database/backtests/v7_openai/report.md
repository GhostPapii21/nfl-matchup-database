# OpenAI-built tests: v7 (from scratch) and v5.1 (improve v5) — 2026-11-03

## Models, tokens, cost
gpt-6-astra tried once for v7 design (high effort): 1,302 in / 8,000 out, all reasoning, empty text (status incomplete). Everything else gpt-6.1-sol. Total 5 calls, 6,036 in / 18,920 out ≈ $0.60 (assumes $5/M in, $30/M out; astra/sol prices unverified). 0 Odds API credits, no held files touched, v5/v6 dirs read-only. No new LLM reads (v5.1 is deterministic on locked v5 Grok reads).

## v7 (pre-steer, from scratch) — FAIL
FanDuel-only, market-anchored ridge logit, walk-forward Wk5-8. Selected 238-237 (50.1%), −5.1%; Brier 0.2581 vs market 0.2503 (worse). Rush-under (FD Wk5-8) 175-150, +1.2%. Slips 1 cash of 20. One crash fix (HASHES.items()), OpenAI-approved (FIXES.md). Superseded by the steer.

## v5.1 design (plan in v5_1/plan.md, locked 32bcfd2 before run)
1. Only stake legs Grok marked confidence=strong AND verdict=agree (cut leans and flagged reads). 2. Re-price to best saved pre-kick book at the same line. 3. Deterministic slips, no reused legs, max 5/week.
Pre-declared success (Wk3-6): ≥40 settled priced legs, positive ROI, beats v5 ROI and $.

## Results (shared harness, v5_1/out/results.md)
| set | Wk3-6 | ROI | Wk7-8 | ROI |
|---|---|---|---|---|
| v5 PRIMARY | 49-63 43.8% | −14.8% (88 priced, −$129.83) | 31-20 60.8% | +17.2% |
| v5.1 | 14-12 53.8% | −5.3% (22 priced, −$11.58) | 6-3 | +25.7% (9 priced) |
| gate only @v5 prices | 14-12 | −5.9% | 6-3 | +25.2% |
| v6 READS | 39-68 | −27.1% | 27-22 | −2.1% |
| v6 GATED | 19-38 | −36.4% | 18-12 | +7.2% |
| rush-under baseline | 207-154 | +4.3% | 89-75 | −0.6% |
Slips: v5.1 0/7 (−$70); v5 4/29 (+$145).
OpenAI verdict: FAIL (insufficient sample: 22 < 40, and ROI negative); loses less than v5 on Wk3-6 but almost entirely from the strong+agree selection; repricing added ~$1.4. Still below the rush-under baseline in Wk3-6.

## Forward Week 10+ shadow (v5.1 vs v5 PRIMARY)
Locked plan: freeze code, sha256 picks before kick, append-only ledger (read tag/confidence/verdict, orig vs executed price, book/snap/kickoff, stake, closing price). Judge after 100 settled priced singles over ≥8 weeks; kill at −$200 or any hash/as-of breach. OpenAI's review proposed a first checkpoint at ≥40 legs (not adopted; plan.md lock governs). Slips paper-only. Forward-only prompt changes (separate arm): say "missing" instead of inventing injury fallout, structured must_be_true/kills_it, separate data-contradiction from missing data. At ~6 legs/week, 100 legs ≈ 16 weeks.

## Caveats
Wk3-6 is not a clean holdout (OpenAI saw v5 aggregates). Harness v5 Wk3-6 P/L −$129.83 vs v5 report −$119.83 (one leg settles differently; unreconciled). Hit rates include unpriced legs. Slip prices are synthetic products.
