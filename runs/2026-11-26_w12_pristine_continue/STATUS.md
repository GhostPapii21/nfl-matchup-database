# W12 pristine continue — status

- Branch: `cursor/w12-pristine-holdout-cont-3852`
- Base SHA at start: `2b82b5c395a2a5ad3651864ff939c03edc31d294`
- Checked: `2026-11-26T19:29:13.608743+00:00` (2026-11-26T14:29:13.608743-05:00)
- Protocol: `pipeline.sim100k` G0–G7 must PASS before any pristine LOCK. Parallel `snapshots.lock`-only artifacts remain **non-qualifying**.

## Kickoff classification (America/New_York)

| Game | Kickoff ET | Pre-kickoff? | Lock created? | Reason |
| --- | --- | --- | --- | --- |
| GB@LAR | Wed 8:00 PM | no | no | Post-kickoff; retroactive forbidden |
| CHI@DET | Thu 1:00 PM | no | no | Post-kickoff; final pre-KO recheck on #136 was NO_LOCK (CHI inactives + FTN/PFR GAP) |
| PHI@DAL | Thu 4:30 PM | yes | pending T-90 | Quotes refreshed; FTN/PFR GAP for `2026_12_GB_LA` still blocks G4 |
| KC@BUF | Thu 8:20 PM | yes | no | Same GAP; inactives NOT_YET until 6:50 PM ET |
| DEN@PIT | Fri 3:00 PM | yes | no | Same GAP; inactives NOT_YET |
| 10 Sun/Mon games | Sun/Mon | yes | no | Same GAP; inactives NOT_YET |

## Hard blocker (slate-wide)

Cached nflverse `ftn_charting_2026` and `advstats_week_def_2026` max **week 11**. Completed `2026_12_GB_LA` is missing → G4 `ftn_charting`/`pfr_defense` **GAP**. `sim100k` refuses for every remaining W12 game until publisher coverage includes GB@LAR (and any later completed W12 games).

## Holdout arithmetic

- Scored: **14** (weeks 10–11)
- Qualifying W12 LOCKs this run: **0**
- Post-kickoff without LOCK: **2** (GB@LAR, CHI@DET) — cannot add retroactively
- Remaining pre-kickoff candidates: **14**
- Ceiling if all 14 later qualify+score: **14+14=28** (< 30) → Week 13+ still required
- `projection_ready`: **false**

## Evidence files

- `runs/2026-11-26_w12_pristine_continue/W12_ELIGIBILITY_LIVE.json`
- `runs/2026-11-26_w12_pristine_continue/*_post_refresh_preflight.json`
- Prior CHI@DET NO_LOCK: PR #136 / `cursor/w12-thanksgiving-locks-9aff`
