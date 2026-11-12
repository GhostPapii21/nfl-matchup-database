## 1) Verdict: **FAIL — with insufficient sample size**

Against the pre-declared Wk3–6 criterion, v5.1:
- **Misses volume:** 22 settled priced legs versus ≥40 required.
- **Fails profitability:** −5.3% ROI, −$11.58.
- **Beats v5’s ROI and dollar P/L:** −14.8%, −$129.83—but losing less on substantially fewer bets is not evidence of a profitable edge.

The sample shortfall prevents a sufficiently powered assessment; it does not excuse the negative ROI or turn this into a pass.

**Signal or noise:** encouraging selection results, but unproven. The nine priced holdout legs are far too few to establish an edge. v5 itself improved sharply in Wk7–8, so those weeks do not isolate a v5.1-specific advantage.

**Repricing contributed very little:** versus gate-only at original prices, it added **$1.36 train and $0.39 holdout**, improving ROI by approximately **0.6 and 0.4 percentage points**, respectively. Almost all the observed difference from v5 comes from selection, not repricing. Whether those replacement prices were actually executable remains important.

## 2) Week 10+ forward shadow protocol

I don’t have the original protocol text here, so these are proposed minimal terms, not confirmation of unseen details:

- Freeze v5.1 logic, gates, pricing rules, and slip construction **before Week 10**. No tuning using Wk1–8; those weeks are now development evidence.
- Run alongside frozen **v5 PRIMARY**, with identical eligibility, capture times, settlement rules, and $10 flat singles stakes.
- First performance decision: after the **first complete week bringing v5.1 to ≥40 settled priced forward legs**. No rolling performance-based stopping beforehand.
- **Continuation criterion:** positive ROI and beats contemporaneous v5 on ROI and dollar P/L. Otherwise retire this version from promotion consideration. Report exposure-normalized comparisons too; raw dollars are volume-sensitive.
- If season-end arrives below 40, classify **INSUFFICIENT**, not success. Pause immediately for data-integrity problems.
- **Slips remain paper-only and secondary.** Don’t loosen gates, recycle legs, or force extra slips to increase volume. At roughly 1–2/week, slip results will remain highly variable.

## 3) Harness/comparison checks

Nothing shown proves a harness defect, but:

- Reconcile the **$10 v5 settlement discrepancy** to an explicit rule and audit trail.
- Report priced-only W–L/hit rate alongside ROI; current overall hit rates include unpriced legs.
- Product-of-saved-prices slips are **synthetic**, not necessarily executable sportsbook payouts—especially with correlated legs.
- Verify identical leg identities in the repricing ablation and equivalent price timestamps.
- The split × market × side table is truncated, so subgroup claims cannot be checked.
- These are overlapping strategies, not independent samples; comparisons should respect shared legs and game/week clustering.