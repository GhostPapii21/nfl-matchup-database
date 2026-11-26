# Week 12 pristine lock eligibility — 2026-11-26

Checked: `2026-11-26T13:08:22Z` (08:08 AM America/New_York).
Branch: `cursor/w12-thanksgiving-locks-9aff`.

Official slate from ESPN scoreboard kickoffs (not packet date alone).

| Game | Kickoff UTC | Status | Hours to KO | Packet | Engine cfg | Quote freshness | Injury/inactives | Lock eligibility | Reason if ineligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GB @ LAR | 2026-11-26T01:00:00Z | FINAL | past | yes | yes | n/a | n/a | **NO** | Kickoff already occurred — retroactive lock forbidden |
| CHI @ DET | 2026-11-26T18:00:00Z | PRE | ~4.9 | yes | yes | freeze OK (~12:43Z) | ESPN refreshed; official inactives NOT_YET | **NO_LOCK_YET** | G4: ftn_charting GAP + pfr_defense GAP for `2026_12_GB_LA`; official_inactives NOT_YET until ~16:30Z |
| PHI @ DAL | 2026-11-26T21:30:00Z | PRE | ~8.4 | yes | yes | needs refresh at lock | not verified for lock | **CANDIDATE** | Same FTN/PFR GAP risk; defer until after CHI T-90 |
| KC @ BUF | 2026-11-27T01:20:00Z | PRE | ~12.2 | yes | yes | needs refresh at lock | not verified for lock | **CANDIDATE** | Same FTN/PFR GAP risk |
| DEN @ PIT | 2026-11-27T20:00:00Z | PRE | ~30.9 | yes | yes | later | later | **CANDIDATE** | Pre-kickoff; gates not yet run for lock |
| ATL @ MIN | 2026-11-29T18:00:00Z | PRE | ~77 | yes | yes | later | later | **CANDIDATE** | Sunday early |
| BAL @ HOU | 2026-11-29T18:00:00Z | PRE | ~77 | yes | yes | later | later | **CANDIDATE** | Sunday early |
| NO @ CIN | 2026-11-29T18:00:00Z | PRE | ~77 | yes | yes | later | later | **CANDIDATE** | Sunday early |
| NYG @ IND | 2026-11-29T18:00:00Z | PRE | ~77 | yes | yes | later | later | **CANDIDATE** | Sunday early |
| NYJ @ MIA | 2026-11-29T18:00:00Z | PRE | ~77 | yes | yes | later | later | **CANDIDATE** | Sunday early |
| TEN @ JAX | 2026-11-29T18:00:00Z | PRE | ~77 | yes | yes | later | later | **CANDIDATE** | Sunday early |
| NE @ LAC | 2026-11-29T21:05:00Z | PRE | ~80 | yes | yes | later | later | **CANDIDATE** | Sunday late |
| WSH @ ARI | 2026-11-29T21:25:00Z | PRE | ~80 | yes | yes | later | later | **CANDIDATE** | Sunday late |
| SEA @ SF | 2026-11-29T21:25:00Z | PRE | ~80 | yes | yes | later | later | **CANDIDATE** | Sunday late |
| LV @ CLE | 2026-11-30T01:20:00Z | PRE | ~84 | yes | yes | later | later | **CANDIDATE** | Sunday night |
| CAR @ TB | 2026-12-01T01:15:00Z | PRE | ~108 | yes | yes | later | later | **CANDIDATE** | Monday night |

## CHI@DET gate evidence (latest)

Command: `python3 -m pipeline.sim100k --game 2026_12_CHI_DET` → exit **2**, nothing simulated.

Cleared by prewarm:
- nflverse digest STALE / UNKNOWN_NO_SOURCE_TIMESTAMP (packet rebuild)
- odds / four_book_prices STALE (`pregame.sportsbooks` + `pregame.direct_books`, freeze `freeze_20261126T124745Z.json`, pulled `2026-11-26T12:42:59Z`)

Still blocking:
1. `ftn_charting` GAP — publisher max week 11; missing completed `2026_12_GB_LA`
2. `pfr_defense` GAP — same
3. `official_inactives` NOT_YET — posts ~Thu 11:30 AM ET (T-90 ≈ 16:30Z)
4. Phases 7/8/9 GAP; phase 15 NOT_YET

## Holdout inventory (unchanged thresholds)

- Unique qualifying scored games: **14** (weeks **10, 11**)
- Week 12 **pristine-qualifying** LOCKs: **0**
- Parallel `snapshots.lock` artifacts on `cursor/w12-pristine-holdout-23b6`: research/NOT_FINAL only — **not** pristine (sim100k G0–G7 did not PASS; see `NON_QUALIFYING_PARALLEL_LOCKS.md`)
- Ceiling if all 15 remaining W12 eventually qualify+score: **29** vs min **30** games / **3** weeks
- Shortfall at ceiling: **≥1 game** (Week 13+ still required)
- `projection_ready`: **false** (must remain false)

## Note on W11 CIN@WAS

Earlier pristine LOCKs for `2026_11_CIN_WAS` were written when FTN/PFR still covered all then-completed games. Later `sim100k` REFUSAL on W11 GAP is post-lock publisher lag — not a bypass for creating locks under GAP today.
