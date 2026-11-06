# Label corrections addendum (do not mutate frozen originals)

## Retrospective JAX@BAL kickoff clock
- Frozen cutoff / kickoff UTC in `integration/certified_asof`: **2026-11-06T01:15:00Z**.
- America/New_York conversion: **2026-11-05 20:15:00 EST** (Thursday night kickoff).
- Correct label: **kickoff / pregame freeze boundary for TNF**, not “postgame”.
- Postgame evidence (final box, gamebook) is separately classified EVIDENCE_ONLY_POSTGAME when pulled after the game ends; the **01:15Z instant itself is kickoff**, not postgame.
- This addendum corrects narrative misstatements in later prospective docs without rewriting frozen certified_asof bytes.

## Prospective directory / week naming
- Path `prospective_wk10_2026-11-08` is a **directory misnomer**.
- Authoritative week for DAL@IND: **NFL 2026 regular season week 9** (`nflverse` `2026_09_DAL_IND`, ESPN week 9).
- Week 10 in balldontlie/nflverse starts ~2026-11-13 (TNF WSH@NYG). Do not call Sunday 2026-11-08 “week 10”.
- Canonical game IDs remain: ESPN `401873040`, nflverse `2026_09_DAL_IND`, balldontlie `1392339`.

## Roster count vs active eligibility
- ESPN roster endpoint returns full squad (~78) including practice squad / non-game-day.
- Predictive active pool must use `status==ACT` (nflverse) ∩ injury designations, not raw 78.

## Verification evidence (re-checked 2026-11-06 07:51 EST)
- ESPN summary `401873040`: date `2026-11-08T18:00Z`, week **9**, season year 2026 type REG, status STATUS_SCHEDULED / detail "Sun, November 8th at 1:00 PM EST".
- nflverse `2026_09_DAL_IND`: season 2026, week **9**, gameday 2026-11-08, gametime 13:00, ESPN 401873040, gsis 60302, Lucas Oil Stadium.
- America/New_York conversion of retrospective freeze clock `2026-11-06T01:15:00Z` → **Thu 2026-11-05 20:15 EST** = **kickoff**, not postgame.
- America/New_York conversion of prospective kickoff `2026-11-08T18:00:00Z` → **Sun 2026-11-08 13:00 EST**.
