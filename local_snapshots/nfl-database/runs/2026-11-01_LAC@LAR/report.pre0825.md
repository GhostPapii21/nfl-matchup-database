GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_LAC@LAR  checked_at=2026-11-01 07:36 ET
Live legs: ['Puka Nacua Receptions Over 7.5']
Cut legs: ['Blake Corum Rush Yds Under 46.5', 'Blake Corum Rush+Rec Yds Under 56.5', 'Justin Herbert Pass Yds Under 205.5', 'Kyren Williams Rush Yds Under 58.5', 'Kyren Williams Rush+Rec Yds Under 85.5', 'Ladd McConkey Rec Yds Under 47.5', 'Ladd McConkey Receptions Under 3.5', 'Matthew Stafford Pass Yds Over 248.5', 'Omarion Hampton Rush Yds Over 31.5', 'Omarion Hampton Rush+Rec Yds Over 40.5', 'Oronde Gadsden II Rec Yds Under 15.5', 'Oronde Gadsden II Receptions Under 1.5', 'Puka Nacua Rec Yds Over 91.5', 'Quentin Johnston Rec Yds Under 33.5', 'Quentin Johnston Receptions Under 2.5', 'Tyler Higbee Rec Yds Under 36.5', 'Tyler Higbee Receptions Under 3.5']
APPROVED EXCEPTIONS:
  - leg Puka Nacua Receptions Over 7.5 defender Donte Jackson: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Puka Nacua Receptions Over 7.5: avg p 0.593, no-vig 0.542, edge +5.1, shrunk +2.3

# LAC @ LAR — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): none. Pass count 1 -> 1.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: none.
- Live legs now: Puka Nacua Receptions Over 7.5 (MC+GR avg p 0.624, no-vig 0.542, edge +8.2, shrunk +4.5)

## 1. Header
- Game: LAC @ LAR, game ID 401873032, kickoff 04:05 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_LAC@LAR/checklist.md
- Candidate legs: 18 (key players × FD main market); passed 1, cut 17.

## 2. Phases run
- 1 Data pull: PASS 18
- 2 Opportunity: PASS 18
- 3 Defense profile: FAIL 3, PASS 15
- 4 Defender coverage: FAIL 1, N/A 3, PASS 7, UNVERIFIED 7
- 5 Pressure/blitz/checkdown: N/A 3, PASS 15
- 6 QB card: FAIL 2, PASS 16
- 7 Role: FAIL 1, PASS 17
- 8 Injuries: PASS 18
- 9 NGS: PASS 18
- 10 Film: PASS 18
- 11 Environment: PASS 18
- 12 Source audit: PASS 18
- 13 Game script 10G: FAIL 13, PASS 5
- 14 Models/price/edge: FAIL 6, PASS 4, UNVERIFIED 8
- 15 Inactives: PASS 18
- Gaps: Phase 4 has no ruled mapping for TE and RB-receiving legs (UNVERIFIED → cut); Phase 9 uses the NGS backup; Phase 5 pressure is a PROXY.

## 3. Sources used, by category
- Core stats and play-by-play: nflverse pbp, snaps and players (curl, 07:09 ET); ESPN depth-chart API (07:14 ET); ESPN box scores (Oct 31, 7:19 PM ET) as the second source for targets. The PFR live pull returned HTTP 403, so the PFR cache from Oct 29 was used (Rico exception).
- Coverage schemes and matchups: FTN charting via nflverse (blitz rate); Sharp coverage-schemes page via Firecrawl (man/zone and MOF; data updated Oct 27); ESPN WR/CB cheatsheet (07:12 ET); PFR per-defender cache. The Sharp pressure page and SumerSports are on hold, so pressure uses the labelled PROXY. PFF was not pulled (logged-out preview only).
- Next Gen Stats: BACKUP only, the nflverse nextgen_stats release (TTT, separation, cushion, YAC+, RYOE). nextgenstats.nfl.com is on hold per Ghost6.
- Film: official NFL YouTube highlights (oEmbed-checked); only caption plays that re-matched a fresh pbp row are cited.
- Injuries and news: ESPN injuries API (07:09 ET).
- Weather: NWS hourly + Open-Meteo (07:10 ET).
- Odds and props: The Odds API, FanDuel main and alt ladders (price of record), Pinnacle and DraftKings no-vig comparison, PrizePicks and Underdog lines (props 07:30 ET; spreads/totals 07:30 ET).

## 4. Simulations
- Monte Carlo, Bias and Game Randomness each ran 100,000 sims per leg. Seed 20261101 (md5 per-leg offset). Script /workspace/nfl-database/runs/2026-11-01_shared_src/sim_v5.py (sha 906ec6350e5bbe06).

| Leg | MC p / median | Bias p / median | GR p / median |
|---|---|---|---|
| Justin Herbert Pass Yds Under 205.5 | 0.691 / 174.3 | 0.842 / 146.9 | 0.693 / 174.3 |
| Omarion Hampton Rush Yds Over 31.5 | 0.698 / 43.9 | 0.599 / 37.6 | 0.674 / 42.8 |
| Omarion Hampton Rush+Rec Yds Over 40.5 | 0.716 / 56.2 | 0.619 / 48.3 | 0.693 / 55.6 |
| Ladd McConkey Rec Yds Under 47.5 | 0.802 / 22.8 | 0.847 / 19.2 | 0.786 / 16.7 |
| Ladd McConkey Receptions Under 3.5 | 0.812 / 2.0 | 0.841 / 1.0 | 0.788 / 1.0 |
| Quentin Johnston Rec Yds Under 33.5 | 0.735 / 11.2 | 0.773 / 8.6 | 0.739 / 9.1 |
| Quentin Johnston Receptions Under 2.5 | 0.825 / 1.0 | 0.860 / 1.0 | 0.806 / 1.0 |
| Oronde Gadsden II Rec Yds Under 15.5 | 0.532 / 13.5 | 0.613 / 10.9 | 0.551 / 11.5 |
| Oronde Gadsden II Receptions Under 1.5 | 0.439 / 2.0 | 0.497 / 2.0 | 0.475 / 2.0 |
| Matthew Stafford Pass Yds Over 248.5 | 0.620 / 282.4 | 0.463 / 238.9 | 0.613 / 279.3 |
| Kyren Williams Rush Yds Under 58.5 | 0.487 / 59.2 | 0.618 / 52.1 | 0.505 / 58.4 |
| Kyren Williams Rush+Rec Yds Under 85.5 | 0.486 / 86.6 | 0.636 / 74.7 | 0.493 / 86.1 |
| Blake Corum Rush Yds Under 46.5 | 0.637 / 38.3 | 0.727 / 33.1 | 0.637 / 38.3 |
| Blake Corum Rush+Rec Yds Under 56.5 | 0.614 / 48.8 | 0.720 / 41.9 | 0.615 / 48.1 |
| Puka Nacua Rec Yds Over 91.5 | 0.563 / 102.2 | 0.454 / 84.9 | 0.562 / 102.2 |
| Puka Nacua Receptions Over 7.5 | 0.622 / 9.0 | 0.531 / 8.0 | 0.626 / 9.0 |
| Tyler Higbee Rec Yds Under 36.5 | 0.482 / 38.0 | 0.573 / 30.8 | 0.487 / 36.9 |
| Tyler Higbee Receptions Under 3.5 | 0.501 / 3.0 | 0.570 / 3.0 | 0.502 / 3.0 |

## 5. Projections and picks
- **Puka Nacua Receptions Over 7.5 @ -138 (FanDuel)**: projection MC mean 9.8, median 9.0. No-vig 0.542; avg p 0.593; edge +5.1 pts before shrink, +2.3 after. FD main.
  - Opportunity: rank 1 by tgt last3 (pbp [24, 7, 10]; ESPN box [24, 7, 10]); proj 39.9 pa x 0.339 = 13.5 tgt x cr 0.76 = 10.3 rec; MC mean 9.8
  - Matchup/coverage: cheatsheet: Puka Nacua (R: L24/S24/R52%) vs Donte Jackson [Donte Jackson Questionable: re-check Phase 15] | PFR Donte Jackson: 9 tgt, 66.7% cmp, 7.7 YPT, rtg 89.6 | man 10.6% / zone 58.0%, MOF closed 33.9% / open 40.7% | volume margin +37%
  - Script: LAR -6.5 (moderate favorite); total 45.5; FD main

### Cut legs
- Justin Herbert Pass Yds Under 205.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 174.3 vs FD main 205.5 / book consensus 206.2 (>=12 yds) -> Debugging)
- Omarion Hampton Rush Yds Over 31.5: Phase 3 FAIL (RB YPC allowed <=3.8 suppression); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4; rush-only over on possible trailer needs 4+ tgt/g)
- Omarion Hampton Rush+Rec Yds Over 40.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 22.7% / zone 68.7%, MOF closed 38.7% / open 55.6%; awaiting ruling); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Ladd McConkey Rec Yds Under 47.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 22.8 vs FD main 47.5 / book consensus 47.8 (>=12 yds) -> Debugging)
- Ladd McConkey Receptions Under 3.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +38.9 pts > +15 implausible vs market (FD 3.5, consensus 3.5; possible role change the history-based sim cannot see) -> )
- Quentin Johnston Rec Yds Under 33.5: Phase 4 FAIL (yds under vs YPT>10 defender); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 11.2 vs FD main 33.5 / book consensus 32.5 (>=12 yds) -> Debugging)
- Quentin Johnston Receptions Under 2.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +33.0 pts > +15 implausible vs market (FD 2.5, consensus 2.5; possible role change the history-based sim cannot see) -> )
- Oronde Gadsden II Rec Yds Under 15.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 22.7% / zone 68.7%, MOF closed 38.7% / open 55.6%; no stand-in allowed); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED)
- Oronde Gadsden II Receptions Under 1.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 22.7% / zone 68.7%, MOF closed 38.7% / open 55.6%; no stand-in allowed); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 FAIL (model p 0.439 < .45; a model median does not clear the line)
- Matthew Stafford Pass Yds Over 248.5: Phase 14 FAIL (a model median does not clear the line; MODEL-SUSPECT: MC median 282.4 vs FD main 248.5 / book consensus 249.5 (>=12 yds) -> Debugging)
- Kyren Williams Rush Yds Under 58.5: Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 FAIL (a model median does not clear the line)
- Kyren Williams Rush+Rec Yds Under 85.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 10.6% / zone 58.0%, MOF closed 33.9% / open 40.7%; awaiting ruling); Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 FAIL (a model median does not clear the line)
- Blake Corum Rush Yds Under 46.5: Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +16.7 pts > +15 implausible vs market (FD 46.5, consensus 46.8; possible role change the history-based sim cannot see) -)
- Blake Corum Rush+Rec Yds Under 56.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 10.6% / zone 58.0%, MOF closed 33.9% / open 40.7%; awaiting ruling); Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script)
- Puka Nacua Rec Yds Over 91.5: Phase 14 FAIL (placed-ticket bar: UD20 Puka o69.5; edge +2.6 < +3; a model median does not clear the line)
- Tyler Higbee Rec Yds Under 36.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 10.6% / zone 58.0%, MOF closed 33.9% / open 40.7%; no stand-in allowed); Phase 14 FAIL (edge +1.4 < +3; a model median does not clear the line)
- Tyler Higbee Receptions Under 3.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 10.6% / zone 58.0%, MOF closed 33.9% / open 40.7%; no stand-in allowed)

## 6. Risks and checks still to come
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. No PFF row matches a live leg in this folder.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 2:35 PM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
