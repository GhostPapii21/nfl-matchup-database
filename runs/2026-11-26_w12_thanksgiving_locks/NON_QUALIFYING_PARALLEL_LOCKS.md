# Non-qualifying CHI@DET locks on parallel branch

Branch: `origin/cursor/w12-pristine-holdout-23b6` (worker [Week 12 pristine holdout eval](bc-621b3725-f09e-5863-b942-60ca89b823b6)).

| Snapshot | locked_utc | Why it does **not** count as pristine |
| --- | --- | --- |
| `20261126T110635Z` | 11:06Z | Before T-90 (16:30Z); official inactives not yet required/available |
| `20261126T165631Z` | 16:56Z | Same window as T-90, but `pipeline.sim100k` **REFUSED** (exit 2): FTN/PFR GAP for completed `2026_12_GB_LA`; CHI official inactives INCOMPLETE/MISSING; phases 7–9 GAP |

Worker reports evaluation ledger marks both **NOT_FINAL**. Correct.

**Rule:** A `snapshots.lock` artifact with `n=100000` / `asof_checks=PASS` is **not** pristine holdout evidence if `pipeline.sim100k` G0–G7 refuse. Do not invent eligibility. Do not merge these into the scored inventory.

This branch (`cursor/w12-thanksgiving-locks-9aff`) intentionally has **no** `snapshots/2026_12_CHI_DET/` LOCK.
