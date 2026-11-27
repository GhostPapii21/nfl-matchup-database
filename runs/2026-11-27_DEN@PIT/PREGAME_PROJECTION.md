# PREGAME PROJECTION — DEN @ PIT (Friday Nov 27, 2026)

**Write time:** 2026-11-27 3:02:19 PM ET (America/New_York)  
**Scheduled kickoff:** 3:01 PM ET (America/New_York); ESPN list time 3:00 PM EST / 2026-11-27T20:00:00Z  
**Timing vs kickoff:** This file was written at 2026-11-27 3:02:19 PM ET, which is after the scheduled 3:01 PM ET kickoff. It is NOT a true pregame freeze. ESPN still showed STATUS_SCHEDULED at a 3:01:11 PM ET check, but the clock time is after the listed kick, so this document is a post-scheduled-kick write-up of the earlier lock, not a pre-kick freeze. The real pregame record is PR #141's 100k-sim lock, locked 2026-11-27 06:16:48 AM ET (UTC 2026-11-27T11:16:48Z), committed 2026-11-27 06:20:29 AM ET as 09555ad92e2c2bee90ca94adaa15b8f82d3daa32 on branch blitz/nfl49-w12-fri-locks-20261127 (https://github.com/GhostPapii21/nfl-matchup-database/pull/141).

**Labels:** paper / unvetted / research only. `projection_ready=false`. Not Ghost6 vetted. Not picks. No stakes.

**Separation of projections (both graded postgame, head to head):**
- **Rico's projections** = his three locked slips in `RICO_SLIPS_LOCK.md` (relabeled RICO'S PROJECTIONS; locked 2:58:25 PM ET from FanDuel screenshots). Those are Rico's card, not this model freeze.
- **Our projection** = this file, restating the PR #141 100k lock plus verified news and one derived total probability from that lock's sim arrays.

---

## Headline (paper / unvetted)

- **Projected score (100k-sim means):** Broncos 20.22, Steelers 20.01. **Medians:** DEN 20, PIT 20. Most common sim scoreline: DEN 17–PIT 20 (1.08% of trials).
- **Projected total:** mean 40.22, median 40 (p10 / p25 / p75 / p90 = 26 / 32 / 48 / 55). First-half total mean 19.93, median 20.
- **Win probs:** DEN 50.18%, PIT 48.66%, tie 1.17%. P(OT) 4.47%.
- **Rico Slip C alt Under 51.5:** P(total ≤ 51) = **84.08%** (84,084 / 100,000 trials from the locked `sim_arrays.npz`). Median 40.
- **All other Rico legs (TDs, receptions, rec yds, rush+rec yds):** **no projection.** The PR #141 snapshot explicitly withheld player outputs: they are team-bootstrap credits, not a player projection model.

---

## Where this comes from

| Item | Value |
|---|---|
| Source | Draft PR #141, https://github.com/GhostPapii21/nfl-matchup-database/pull/141 |
| Branch | `blitz/nfl49-w12-fri-locks-20261127` |
| PR commit | `09555ad92e2c2bee90ca94adaa15b8f82d3daa32` at 6:20:29 AM ET |
| Lock stamp | `snapshots/2026_12_DEN_PIT/20261127T111648Z/` locked **6:16:48 AM ET** |
| Engine / config | `core/possession_engine_v0` + NFL-43 semantics; `den_pit_2026-11-27_data_only_nfl43` |
| Engine code commit (inside LOCK.json) | `aa60efa49fce9f309f2d7ab6559912d9de2b9896` (clean tree) |
| Trials / seed / runtime | 100,000 in 7 chunks; seed 1969908846; 819.2 s |
| History | 2026 weeks 1–11 only; PBP sha256 `e0f532a73338bbd4…` |
| Price freeze inside the lock | Packet books block pulled 2026-11-27T04:26:21Z (11:26 PM ET Nov 26). Status `PACKET_TWO_BOOK_NOT_FOUR_BOOK`. **No Odds API pull was made for this write-up.** |
| This file's added work | Restated lock means/probs; computed P(U51.5) from the locked sim arrays; NWS weather refresh; verified QB/RB news. No new simulation was run. |

Local copies of the lock files used: `/tmp/pr141-denpit-lock/`.

---

## Verified news vs what the lock assumed

The lock is a **data_only** config: **no injury / inactive adjustment.** Phase 15 inactives were not applied to the sim. Team snaps are historical 2026 weeks 1–11 resampling, not a Rudolph-specific or Coleman-specific player model.

1. **Mason Rudolph starts for Pittsburgh.** Aaron Rodgers was released Wednesday and cleared waivers Thursday (Steelers / NFL.com). The Nov 25 dashboard already listed Rudolph as the PIT QB, but the 100k sim still uses Pittsburgh's weeks 1–11 team offense (mostly Rodgers-era snaps). This freeze does **not** invent a Rudolph-adjusted score.
2. **J.K. Dobbins is suspended one game** (AP: conduct detrimental). **Jonah Coleman is the lead back** (24 of 27 RB carries last week). The sim does **not** reallocate Denver carries to Coleman and does **not** publish a Coleman rushing/receiving projection.

These updates are recorded so postgame grading can see what changed after (or around) the 6:16 AM ET lock. They are not a reason to invent new player numbers.

---

## Game projection (from the locked 100k arrays / summary.json)

| | DEN (away) | PIT (home) | Total |
|---|---|---|---|
| Mean points | 20.22 | 20.01 | 40.22 (sd 11.74) |
| Median points | 20 | 20 | 40 |
| Q1 / Q2 / Q3 / Q4 means | 5.11 / 5.33 / 4.33 / 5.34 | 4.22 / 5.27 / 5.15 / 5.26 | |
| H1 / H2 means | 10.44 / 9.67 | 9.49 / 10.42 | H1 total mean 19.93 (median 20) |

Against the lock's frozen FanDuel main lines (research comparison only; the lock itself flagged a large moneyline divergence as **treat as model error until shown otherwise**; not an edge claim, not a lean label):

| Market | Frozen FD line | Model P |
|---|---|---|
| PIT +4.5 | -113 / -113 (no-vig 50%) | 63.08% cover |
| Over 36.5 | -120 / Under -106 (no-vig Over 51.46%) | 61.60% Over |
| Over 39.5 (open line in the lock) | no-vig 50% | 51.90% Over |
| PIT moneyline | +194 (no-vig 32.65%) | 48.66% win (49.23% ex-tie) |

Derived from the same locked arrays (not printed in `summary.json`, computed here from `sim_arrays.npz`):

| Line | P(over) | P(under) |
|---|---|---|
| 36.5 | 61.60% | 38.40% |
| 39.5 | 51.90% | 48.10% |
| 47.5 | 25.33% | 74.67% |
| **51.5** | **15.92%** | **84.08%** |
| 52.5 | 14.85% | 85.15% |

---

## Rico's legs — median and hit probability

Rico's card is in `RICO_SLIPS_LOCK.md`. Only legs the lock/arrays actually support get a number. Everything else is **no projection**.

| Slip | Leg | Median | Hit probability | Source |
|---|---|---|---|---|
| A, B | Jonah Coleman anytime TD | no projection | no projection | player outputs withheld |
| A, B | Pat Freiermuth 2+ receptions | no projection | no projection | player outputs withheld |
| A, B | Jonah Coleman 70+ rush+rec yds | no projection | no projection | player outputs withheld |
| A, B | Courtland Sutton 15+ rec yds | no projection | no projection | player outputs withheld |
| A, B | Evan Engram 2+ receptions | no projection | no projection | player outputs withheld |
| A, B | Jaylen Warren 60+ rush+rec yds | no projection | no projection | player outputs withheld |
| C | Courtland Sutton 30+ rec yds | no projection | no projection | player outputs withheld |
| C | Evan Engram over 2.5 receptions | no projection | no projection | player outputs withheld |
| C | Jaylen Warren 2+ receptions | no projection | no projection | player outputs withheld |
| C | Jaylen Warren anytime TD | no projection | no projection | player outputs withheld |
| C | Jonah Coleman 1st-half anytime TD | no projection | no projection | player outputs withheld |
| C | DK Metcalf 15+ rec yds | no projection | no projection | player outputs withheld |
| C | Alternate game total Under 51.5 | median total **40** | **84.08%** (P(total ≤ 51)) | locked 100k `sim_arrays.npz` |

Flags already on Rico's card (unchanged): Slip C pairs a game-total under with same-game player overs (breaks the Oct 29 rule). None of these slips are Ghost6 vetted.

---

## Weather (NWS only)

Source: US National Weather Service hourly forecast, gridpoint PBZ 77,66,  
https://api.weather.gov/gridpoints/PBZ/77,66/forecast/hourly  
Retrieved for this file from that endpoint. NWS `updateTime` 2026-11-27T19:06:28Z (2:06 PM ET), `generatedAt` 2026-11-27T19:11:15Z (2:11 PM ET). Venue is outdoors (Acrisure Stadium, grass).

| Hour (ET) | Temp | Wind | Forecast | Precip chance | Humidity |
|---|---|---|---|---|---|
| 3:00 PM (kick window) | 36 F | 17 mph SW | Rain Showers | 81% | 100% |
| 4:00 PM | 36 F | 16 mph SW | Rain Showers | 79% | 100% |
| 5:00 PM | 37 F | 16 mph SW | Rain Showers | 75% | 100% |
| 6:00 PM | 37 F | 16 mph SW | Rain Showers Likely | 71% | 100% |

No Open-Meteo pull was needed; NWS responded. ESPN/AccuWeather on the summary endpoint was not used for weather.

The Nov 25 board called this a weather game (rain + wind). The 100k lock does not apply a weather adjustment (data_only team resampling). Do not invent a weather-adjusted total.

---

## Strong leans / vetted leans

**None.** PR #141 did not label any strong lean or vetted lean. Player outputs were withheld. The lock is research-only, `projection_ready=false`, and Rico has not authorized it as playable. Ghost6 has not vetted it. This freeze also does not label any strong or vetted lean.

The live STRONG LEANS tracker will therefore start empty of official leans and will only follow: (a) the team-level model-vs-market comparisons published in the lock (comparison only, including the LARGE_DIVERGENCE moneyline flag), and (b) Rico's own projections as a separate grade stream. A Nov 25 game-day brief with older “strongest reads” and a different score (PIT 17, DEN 20, total 37.5) is **not** part of the PR #141 lock and is not imported as leans.

---

## Known limits (from LOCK.json, carried forward)

- Vertical slice: empirical team-only snap resampling; not a situational clock model.
- data_only: no injury/inactive/weather adjustment; PIT weeks 1–11 offense is not a Rudolph-only unit; DEN backfield is not reallocated for the Dobbins suspension.
- Team scores only; no player projection model.
- Market moneyline divergence was flagged `LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE`.
- W1–8 development set; no betting edge claim.
