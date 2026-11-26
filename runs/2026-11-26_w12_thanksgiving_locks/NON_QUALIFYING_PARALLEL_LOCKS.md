# Non-qualifying W12 `snapshots.lock` artifacts (parallel worker)

**Confirmed correction:** Creating `LOCK.json` via `python3 -m snapshots.lock` while
`pipeline.sim100k` G0–G7 refuse does **not** invent pristine-protocol eligibility.
These artifacts are **research / NOT_FINAL only**. They are **not** pristine holdout
inventory. Do **not** merge as holdout completion. Do **not** count them toward the
30-game / 3-week minimum.

Branch: `origin/cursor/w12-pristine-holdout-23b6`
(worker [Week 12 pristine holdout eval](bc-621b3725-f09e-5863-b942-60ca89b823b6)).

## Rule (fail-closed)

Pristine inventory requires **`pipeline.sim100k` G0–G7 PASS** (then lock under the
approved gameday chain). `asof_checks=PASS` + `n=100000` + `code_dirty=false` alone
are insufficient when G4 freshness / G5 phases refuse.

Evidence from the worker’s own run:

- `python3 -m pipeline.sim100k --game 2026_12_CHI_DET` → exit **2 REFUSED**
  (FTN/PFR GAP for completed `2026_12_GB_LA`; CHI inactives INCOMPLETE; phases 7–9 GAP)
- Early CHI lock `20261126T110635Z` is **pre-T-90** (before official inactives window)

## All parallel LOCK.json paths — **0 qualifying**

| game_id | Snapshot dir | Why non-qualifying |
| --- | --- | --- |
| 2026_12_CHI_DET | `20261126T110635Z` | Pre-T-90; sim100k would refuse (inactives NOT_YET + FTN/PFR GAP) |
| 2026_12_CHI_DET | `20261126T165631Z` | sim100k **REFUSED** exit 2 in same window (GAP + CHI inactives incomplete) |
| 2026_12_PHI_DAL | `20261126T112220Z` | Locked while G4/G5 refuse (same slate GAP); no sim100k PASS |
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

**Count:** 16 LOCK.json files on the parallel branch across 15 games → **0** pristine-qualifying.

Ledger may list them as `NOT_FINAL` under `evaluation.protocol evaluate`. That status is
research bookkeeping only — **not** SCORED holdout evidence and **not** a pass of G0–G7.

## This PR branch (`cursor/w12-thanksgiving-locks-9aff`)

Intentionally has **no** protocol-qualified `snapshots/2026_12_*/` LOCK for pristine inventory.
CHI@DET T-90 decision: **NO_LOCK** (see `STATUS.md`).

## Holdout (unchanged)

- Unique qualifying **SCORED** games: **14** (weeks **10, 11**)
- Week 12 pristine-qualifying LOCKs: **0**
- `projection_ready`: **false**
