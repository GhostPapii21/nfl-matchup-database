# W12 pristine continue — final status

- Branch: `cursor/w12-pristine-holdout-cont-3852`
- Checked: `2026-11-26T21:19:07.972471+00:00` (2026-11-26T16:19:07.972471-05:00)
- Base at start: `2b82b5c3`; docs commit: `d6ac146e`
- Protocol: pristine LOCK requires `pipeline.sim100k` G0–G7 PASS then snapshot lock. `snapshots.lock`-only artifacts are **non-qualifying**.

## Per-game Week 12

| Game | Pre-KO? | Lock? | Decision | Exact reason |
| --- | --- | --- | --- | --- |
| 2026_12_ATL_MIN | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 11:30 AM ET (T-90); not available yet. |
| 2026_12_BAL_HOU | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 11:30 AM ET (T-90); not available yet. |
| 2026_12_CAR_TB | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Mon 06:45 PM ET (T-90); not available yet. |
| 2026_12_CHI_DET | False | no | NO_LOCK | post-kickoff; final pre-KO sim100k REFUSED (CHI inactives incomplete + FTN/PFR GAP for GB_LA); PR #136 |
| 2026_12_DEN_PIT | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Fri 01:30 PM ET (T-90); not available yet. |
| 2026_12_GB_LA | False | no | NO_LOCK | post-kickoff without committed pristine LOCK — retroactive forbidden |
| 2026_12_KC_BUF | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Thu 06:50 PM ET (T-90); not available yet. |
| 2026_12_LV_CLE | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 06:50 PM ET (T-90); not available yet. |
| 2026_12_NE_LAC | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 02:35 PM ET (T-90); not available yet. |
| 2026_12_NO_CIN | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 11:30 AM ET (T-90); not available yet. |
| 2026_12_NYG_IND | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 11:30 AM ET (T-90); not available yet. |
| 2026_12_NYJ_MIA | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 11:30 AM ET (T-90); not available yet. |
| 2026_12_PHI_DAL | True | no | NO_LOCK | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives MISSING: official_inactives hook returned 'INCOMPLETE', not OK. |
| 2026_12_SEA_SF | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 02:55 PM ET (T-90); not available yet. |
| 2026_12_TEN_JAX | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 11:30 AM ET (T-90); not available yet. |
| 2026_12_WAS_ARI | True | no | NO_LOCK_YET | G4: ftn_charting GAP: latest published asset (as-of 2026-11-26T00:02:05+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: pfr_defense GAP: latest published asset (as-of 2026-11-26T12:02:42+00:00, nflverse_asset_digest_match) is missing completed-game coverage for: 2026_12_GB_LA.; G4: official_inactives NOT_YET: Inactives post about Sun 02:55 PM ET (T-90); not available yet. |

## SCORE.json updates

None. No new pristine LOCKs; nothing to score.

## Holdout arithmetic

- Scored: **14** (weeks 10–11)
- Qualifying W12 LOCKs: **0**
- Post-kickoff without LOCK: **2** (cannot add retroactively)
- Still pre-kickoff: **14**
- Ceiling if all remaining pre-KO later qualify+score: **14+14=28** vs min 30
- Shortfall at that ceiling: **2** → Week 13+ still required
- `independently_calibrated`: false; `projection_ready`: **false**

## Hard blockers requiring user/publisher action

1. **nflverse FTN + PFR** still max week 11 — missing completed `2026_12_GB_LA` → slate-wide G4 GAP (blocks every remaining W12 sim100k).
2. **PHI@DAL**: Cowboys.com never posted inactives article through T-12; window closed → NO_LOCK.
3. **CHI@DET**: already lost (post-KO; Bears inactives never posted at final pre-KO check).
4. Parallel draft LOCKs on #134/#135 remain non-qualifying (sim100k G0–G7 did not PASS).

## Week 13

Packets built locally (14 games starting 2026-12-03 KC@LA). No W13 engine configs / LOCKs yet. Needed for coverage once W12 GAP clears.

## Commands (exit codes)

- `python3 -m pipeline.sim100k --game 2026_12_*` → **2** (REFUSED) for every attempted game
- `python3 -m evaluation.protocol evaluate` → **0**, `games_scored=14`, `UNSCORABLE_INSUFFICIENT_COVERAGE`
- No `snapshots.lock` run (gates never passed)

Evidence: `runs/2026-11-26_w12_pristine_continue/`

## Readiness regen

- Regenerated with `python3 -m evaluation.readiness --write` at `2026-11-26T21:31:36.191592+00:00` (2026-11-26T16:31:36.191592-05:00)
- `w12_remaining_post_kickoff`: ['2026_12_CHI_DET', '2026_12_GB_LA', '2026_12_PHI_DAL']
- `w12_remaining_eligible` count: 13 → ['2026_12_ATL_MIN', '2026_12_BAL_HOU', '2026_12_CAR_TB', '2026_12_DEN_PIT', '2026_12_KC_BUF', '2026_12_LV_CLE', '2026_12_NE_LAC', '2026_12_NO_CIN', '2026_12_NYG_IND', '2026_12_NYJ_MIA', '2026_12_SEA_SF', '2026_12_TEN_JAX', '2026_12_WAS_ARI']
- ceiling: **27**; shortfall at ceiling: **3**
- `projection_ready_flag`: false
- Qualifying LOCKs created this run: **0**
- Branch: `cursor/w12-pristine-holdout-cont-3852`
