# Non-qualifying W12 `snapshots.lock` artifacts (parallel worker)

**Confirmed correction:** Creating `LOCK.json` via `python3 -m snapshots.lock` while
`pipeline.sim100k` G0–G7 refuse does **not** invent pristine-protocol eligibility.
These artifacts are **research / NOT_FINAL only**. They are **not** pristine holdout
inventory. Do **not** merge as holdout completion. Do **not** count them toward the
30-game / 3-week minimum.

Branch: `origin/cursor/w12-pristine-holdout-23b6` @ `ee086274`
(worker [Week 12 pristine holdout eval](bc-621b3725-f09e-5863-b942-60ca89b823b6)).

## Rule (fail-closed)

Pristine inventory requires **`pipeline.sim100k` G0–G7 PASS** (then lock under the
approved gameday chain). `asof_checks=PASS` + `n=100000` + `code_dirty=false` alone
are insufficient when G4 freshness / G5 phases refuse.

Evidence (worker + this machine T-90 and ~17:20Z, CHI@DET still PRE):

```
python3 -m pipeline.sim100k --game 2026_12_CHI_DET
# REFUSED exit 2 — FTN/PFR GAP for completed 2026_12_GB_LA
#                — CHI official inactives INCOMPLETE (DET OK)
#                — later odds/four_book STALE inside T-2h (refreshed)
```

Publisher assets still max week **11** (no `2026_12_GB_LA` in FTN/PFR). That GAP
applies slate-wide until nflverse updates.

## All parallel LOCK.json paths — **0 qualifying**

| game_id | Snapshot dir | Why non-qualifying |
| --- | --- | --- |
| 2026_12_CHI_DET | `20261126T110635Z` | Pre-T-90; sim100k would refuse |
| 2026_12_CHI_DET | `20261126T165631Z` | sim100k **REFUSED** exit 2 (GAP + CHI inactives incomplete) |
| 2026_12_PHI_DAL | `20261126T112220Z` | snapshots.lock only; same slate GAP; no sim100k PASS |
| 2026_12_KC_BUF | `20261126T125422Z` | same |
| 2026_12_DEN_PIT | `20261126T124129Z` | same |
| 2026_12_ATL_MIN | `20261126T120039Z` | same |
| 2026_12_BAL_HOU | `20261126T121453Z` | same |
| 2026_12_CAR_TB | `20261126T122756Z` | same |
| 2026_12_LV_CLE | `20261126T130713Z` | same |
| 2026_12_NE_LAC | `20261126T132014Z` | same |
| 2026_12_NO_CIN | `20261126T133351Z` | same |
| 2026_12_NYG_IND | `20261126T134658Z` | same |
| 2026_12_NYJ_MIA | `20261126T135912Z` | same |
| 2026_12_SEA_SF | `20261126T141205Z` | same |
| 2026_12_TEN_JAX | `20261126T142509Z` | same |
| 2026_12_WAS_ARI | `20261126T143822Z` | same |
| 2026_12_GB_LA | — | Past kickoff; no lock (correct) |

**Count:** 16 LOCK.json files across 15 games → **0** pristine-qualifying.

Ledger `NOT_FINAL` rows are research bookkeeping only — **not** SCORED holdout evidence
and **not** a pass of G0–G7.

## This PR branch (`cursor/w12-thanksgiving-locks-9aff`)

Intentionally has **no** protocol-qualified `snapshots/2026_12_*/` LOCK.
CHI@DET T-90+ decision: **NO_LOCK**. Qualifying W12 locks: **0**. Scored: **14**.
Ceiling if all 15 later truly qualify+score: **29** (&lt; 30); Week 13+ still required.
`projection_ready`: **false**.
