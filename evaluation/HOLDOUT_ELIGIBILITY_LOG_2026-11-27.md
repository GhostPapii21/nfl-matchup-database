# Pristine holdout eligibility log (2026-11-27)

Research only. `projection_ready` remains false. Price freezes are not pristine LOCKs.
Protocol: pre-kickoff LOCK, n=100000, `code_dirty=false`, `asof_checks=PASS`, intact hashes, SCORE.json.

## Qualifying inventory

| Metric | Value |
| --- | --- |
| Scored pristine games | **14** |
| Weeks covered | 10, 11 |
| Minimum required | 30 games across ≥3 weeks |
| Independent calibration | not passed |
| `projection_ready` | **false** |

## Week 12 attempts (no LOCK created)

| Game | Kickoff (UTC) | Attempt window | Inactives | Other gates | Outcome |
| --- | --- | --- | --- | --- | --- |
| `2026_12_GB_LA` | 2026-11-26T01:00Z | — | — | already final before agent window | **no retro LOCK** |
| `2026_12_CHI_DET` | 2026-11-26T18:00Z | — | — | already final | **no retro LOCK** |
| `2026_12_PHI_DAL` | 2026-11-26T21:30Z | T-80 / T-57 / T-43 | INCOMPLETE (DAL never posted in window) | FTN/PFR GAP on completed GB_LA; packet `roof` null (schedule later showed `closed`) | **REFUSED** |
| `2026_12_KC_BUF` | 2026-11-27T01:20Z | T-78 | OK (KC+BUF) | FTN/PFR/snap_counts missing completed GB_LA + CHI_DET | **REFUSED** |
| `2026_12_DEN_PIT` | 2026-11-27T20:00Z | T-88 → T-75 → T-57 final | OK (DEN+PIT) | FTN/PFR still **0** W12 rows through 2026-11-27T19:02Z; also pbp republish STALE + quotes STALE on final check | **REFUSED — DEN retries stopped** |

## Publisher GAP (blocks remaining W12 locks)

Fresh nflverse pulls through 2026-11-27T18:41Z:

| Asset | SHA-256 (prefix) | W12 completed coverage |
| --- | --- | --- |
| `ftn_charting_2026` | `ee09d5f28f5f…` | **none** |
| `advstats_week_def_2026` (pfr_defense) | `f1217d79cc1e…` | max week **11** |
| `snap_counts_2026` | updated | GB_LA, CHI_DET, PHI_DAL, KC_BUF present |

Until FTN and PFR include finished W12 games, `pipeline.sim100k` fails G4/G5 for every remaining Week 12 game.

## Known empty-schedule `roof` risks (phase 1 / 12)

Fail-closed when packet `game.roof` is null/empty (not inventable):

- W12: `BAL_HOU`, `NYG_IND`, `WAS_ARI` (and PHI_DAL already missed)
- W13: `DET_ATL`, `PHI_ARI`

## Arithmetic

- Past kickoff without LOCK (not retroactive): GB_LA, CHI_DET, PHI_DAL, KC_BUF (+ DEN when T-40 closes)
- If all remaining pre-kickoff W12 games somehow lock+score: ceiling **≤26** vs min **30** → shortfall **≥4**
- **Week 13 required** (14 packets built on branch `cursor/w12-direct-lines-refresh-662b`)

## Branch heads (this work)

- Holdout / packets: see latest commits on `cursor/w12-direct-lines-refresh-662b`
- Do not set `projection_ready=true`
- Do not count price-freeze folders as pristine locks

## Note: LOCK on `main` for KC@BUF (unscored)

`origin/main` contains `snapshots/2026_12_KC_BUF/20261127T003024Z/LOCK.json` (gameday bot, n=100000, `asof_checks=PASS`, no SCORE.json). It does **not** raise pristine scored count above 14 until scored. This agent's local sim100k attempts for KC@BUF were REFUSED on FTN/PFR GAP; the main LOCK came from a separate gameday path.

## Post T-40 (2026-11-27 ~19:25Z)

`2026_12_DEN_PIT` lock window closed (`pipeline.window`: skip, closed at T-40; ~34 min to kickoff). **No pristine LOCK; not retroactive.** Readiness may still list DEN under pre-kickoff packets until kickoff, but a new LOCK is no longer protocol-eligible. Sunday W12 slate remains blocked until nflverse FTN/PFR publish W12 coverage. Holdout scored remains **14**; `projection_ready` stays false.
