# PROPOSAL (not applied): six weather categories and how each may adjust opportunity

Status: **proposal only**, for Rico's review. refs NFL-47. Does not change Phase 11a, any gate, skill or
`pregame/*.py`. Sources: NWS and Open-Meteo only (as today). Effect sizes below are the ones already measured in
`research/weather/README.md` (nflverse 2018-2026, same-team dry-vs-rain comparison); only effects marked "clear" there
are used. Nothing new was fitted for this proposal.

## Current rule (unchanged by this file)

Phase 11a: flag a game on precip >= 50%, gusts >= 20 mph or sustained wind >= 15 mph; in a flagged game cut passing and
receiving overs and lean toward rushing.

## Why a change is worth reviewing

The repo's own measurements say rain mostly hurts efficiency, not volume: about -4% pass attempts, -6% completion
rate, -12% yards per attempt, and **no clear change** in depth of target or in WR/TE/RB target shares. Wind is what
shortens throws (deep share -13% per 10 mph above 10) and moves targets from TEs (-7.5%) to RBs (+5.1%). Rushing
efficiency in rain has not been fitted. So "lean toward rushing" in every flagged game is not supported by our data for
light rain, and catch overs are hurt less than yardage overs.

## Proposed categories (at kickoff hour plus the next 3 hours)

| Category | Proposed trigger (NWS / Open-Meteo) | Proposed handling |
|---|---|---|
| 0 Indoor | dome, or retractable roof confirmed closed | no adjustment. Retractable with unknown roof status is treated as open until confirmed |
| 1 Normal | precip probability < 30%, sustained < 15, gusts < 20 | no adjustment |
| 2 Light rain | precip probability >= 30% and hourly rate < 2.5 mm/h, wind below Category 5 | small efficiency haircut only (catch rate, yards per target); **no** rushing-volume increase |
| 3 Moderate rain | 2.5-7.6 mm/h for 2+ hours | efficiency haircut; review short-area routes; rushing volume only where the team's own history supports it |
| 4 Heavy rain | > 7.6 mm/h, or 3-hour accumulation > 15 mm | efficiency and explosive-play haircut; ball-security note; review rushing volume |
| 5 Wind-impact | sustained >= 15 or gusts >= 20 (today's thresholds kept) | deep-target share down, TE share down, RB share up, per the measured wind effects; kicking note |
| 6 Combined | Category 3 or 4 plus Category 5 | apply both; never assume every team responds the same way |

Rain thresholds are the standard meteorological light / moderate / heavy rates; the wind thresholds are today's.

## What each category may change (separately, as the mission asks)

Play selection (pass rate), opportunity volume (attempts, carries, targets by position), efficiency (catch rate,
yards per target, YPC), explosive-play probability, turnover probability. Each is applied only where the measured
effect is "clear"; the rest stay at zero and are listed as untested.

## Gaps before this could be adopted

- Team- and QB-specific weather response is not built. 2026 has very few rain games per team; a per-team version needs
  2018-2025 pbp grouped by head coach / play-caller, with uncertainty reported.
- Rushing volume and YPC in rain are not fitted.
- Field conditions are not in any free feed we hold.
- The existing weather backtest used kickoff observations, not forecasts (optimistic). A forecast-snapshot backtest is
  required, chronological, before any category changes a projection.
- Note: the committed training file `rain_effects_train_2018_2025.json` shows larger effects in its "light" tier than
  in "rain" or "heavy" (42 light-rain team-games). That ordering needs a check before light rain gets any haircut.
