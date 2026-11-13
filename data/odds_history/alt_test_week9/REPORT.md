# Week 9 alt-price test (historical Odds API) — no backtest

**Research only. Not a pick list. `projection_ready` stays false. refs NFL-75.**

Pulled Friday, Nov 13, 2026, 11:08–11:09 AM ET (America/New_York). No backtest was run.

## Credits (from response headers; not invented)

| Step | Time (ET) | Call | `x-requests-last` | `x-requests-remaining` | `x-requests-used` | Job running total |
|---|---|---|---:|---:|---:|---:|
| Precheck | 11:08:55 AM | `GET /v4/sports` (0-cost) | 0 | 1,734 | 18,266 | 0 |
| Event 1 | 11:08:55 AM | historical event-odds, `2026_09_DAL_IND` | **40** | 1,694 | 18,306 | 40 |
| Event 2 | 11:09:38 AM | historical event-odds, `2026_09_JAX_BAL` | **40** | 1,654 | 18,346 | 80 |
| Event 3 | 11:09:38 AM | historical event-odds, `2026_09_BUF_MIN` | **40** | 1,614 | 18,386 | 120 |

- **Credits used this job:** 120
- **Credits remaining after the job:** 1,614
- **Cost per event-call:** 40 (measured on the first call, then repeated exactly on the next two)
- **Formula confirmed:** 10 × 4 markets × 1 region-equivalent. `bookmakers=fanduel,pinnacle` counted as one region-equivalent (every 10 named books = 1 region). Official docs: 10 per market per region per event on the historical event-odds endpoint.
- **Hard limits honored:** job cap 150; remaining never allowed to fall below 950 (800 floor + 150 reserved for Sunday morning's live rush-yard pull). After 120 used, a fourth event at 40 would have been 160 > 150, so the job stopped. Remaining 1,614 is above 950.

EU region was **not** added. Pinnacle already came back on the `bookmakers=` parameter at the 1-region cost. Adding `regions=eu` is estimated at another 40 credits per event (10 × 4 × 1) and would have cut coverage under the 150 cap. That estimate was not spent to confirm.

## Request shape

- Endpoint: `GET /v4/historical/sports/americanfootball_nfl/events/{event_id}/odds`
- Markets: `player_rush_yds`, `player_rush_yds_alternate`, `player_reception_yds`, `player_reception_yds_alternate`
- Books: FanDuel and Pinnacle (`bookmakers=fanduel,pinnacle`), American odds
- Snapshot request: 90 minutes before kickoff (ET). The API returns the closest snapshot at or before that timestamp (5-minute grid).
- Event IDs came from the already-saved inventory `week9_verified_pregame.csv` (32-character Odds API ids, not ESPN ids). No historical-events discovery call was made.

## Events covered (3 of 15 Week 9 games)

| Game | Kickoff (ET) | Requested snapshot (UTC) | Snapshot returned (UTC) | HTTP | Cost |
|---|---|---|---|---:|---:|
| `2026_09_DAL_IND` (Sun 1:00 PM) | Sun Nov 8, 2026, 1:00 PM ET | 2026-11-08T16:30:00Z | 2026-11-08T16:25:36Z | 200 | 40 |
| `2026_09_JAX_BAL` (TNF) | Thu Nov 5, 2026, 8:15 PM ET | 2026-11-05T23:45:00Z | 2026-11-05T23:40:36Z | 200 | 40 |
| `2026_09_BUF_MIN` (MNF) | Mon Nov 9, 2026, 8:15 PM ET | 2026-11-09T23:45:00Z | 2026-11-09T23:40:36Z | 200 | 40 |

Week 9 games **not** pulled (job cap): `CIN_ATL`, `DEN_CAR`, `NYJ_KC`, `DET_MIA`, `CLE_NO`, `NYG_PHI`, `LA_WAS`, `HOU_LAC`, `LV_SF`, `GB_NE`, `ARI_SEA`, `TB_CHI` (12 games).

## What actually came back

All three events returned **both FanDuel and Pinnacle**. Pattern was the same on TNF, Sunday, and MNF.

### FanDuel

- **Standard** `player_rush_yds` and `player_reception_yds`: both **Over and Under** on the main line, one line per player.
  - DAL@IND: 6 rush / 10 rec players, both sides.
  - JAX@BAL: 6 rush / 16 rec players, both sides.
  - BUF@MIN: 6 rush / 16 rec players, both sides.
- **Alternate** `player_rush_yds_alternate` and `player_reception_yds_alternate`: **Over only**. Outcome names were exclusively `"Over"`. Zero Under outcomes on all three events.
  - Rush alt rungs seen: 16 or 17 steps from 4.5 up to 149.5 or 174.5 (not every player has every rung).
  - Rec alt rungs seen: 16 or 17 steps from 4.5 up to 149.5 or 174.5.

### Pinnacle

- **Standard** `player_rush_yds` and `player_reception_yds`: both **Over and Under**.
- **No alternate markets** on any of the three events. Pinnacle did not return `player_rush_yds_alternate` or `player_reception_yds_alternate`.

### Gaps

- FanDuel historical alt ladders at these T-90 snapshots have no under side. A historical alt-under test cannot be graded from this feed as returned.
- Pinnacle cannot be used as an alt-ladder reference; only as a main-line reference.
- 12 of 15 Week 9 games are not in this pull.
- This is one snapshot per game (~T-90), not a line-history series.
- EU-region Pinnacle coverage was not separately tested.

## Projected cost of a full Weeks 8–9 pull at this rate

Same request shape: 4 markets, FanDuel + Pinnacle, one T-90 snapshot per game, no second region.

- Week 8 games in the inventory schedule: **14**
- Week 9 games: **15**
- Combined: **29** event-calls × **40** credits = **1,160** credits

That is the cost of the pull only. It does not include a 1-credit historical-events lookup (not used here) or an EU-region add-on (not used here; would be +40 per event if it were).

Against the current remaining 1,614 and the 950 floor, a full 1,160-credit Weeks 8–9 pull would leave 454, which is **below the 950 floor**, so it cannot be run as one job under the standing reserve rule. Completing the remaining 26 games at 40 each would cost 1,040 and has the same floor problem. Rico would need to approve either a lower reserve or a cheaper request shape (fewer markets, or fewer games).

Raw responses and the credit ledger are in this folder (`raw/`, `ledger.json`). The API key is not stored in these files.
