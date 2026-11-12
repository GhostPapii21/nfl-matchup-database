<!-- Phase 15 re-check 11:45 ET gate output -->
```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_CLE@PIT  checked_at=2026-11-01 11:41 ET
Live legs: none
Cut legs: ['Aaron Rodgers Pass Yds Under 218.5', 'DK Metcalf Rec Yds Under 52.5', 'DK Metcalf Receptions Under 4.5', 'Darnell Washington Rec Yds Under 20.5', 'Darnell Washington Receptions Under 2.5', 'Denzel Boston Rec Yds Under 47.5', 'Denzel Boston Receptions Under 3.5', 'Deshaun Watson Pass Yds Under 210.5', 'Germie Bernard Rec Yds Over 43.5', 'Germie Bernard Receptions Under 4.5', 'Harold Fannin Jr. Rec Yds Under 34.5', 'Harold Fannin Jr. Receptions Under 3.5', 'Jaylen Warren Rush Yds Over 64.5', 'Jaylen Warren Rush+Rec Yds Over 91.5', 'Jerry Jeudy Rec Yds Over 21.5', 'Jerry Jeudy Receptions Over 2.5', 'KC Concepcion Rec Yds Under 46.5', 'KC Concepcion Receptions Under 4.5', 'Quinshon Judkins Rush Yds Over 47.5', 'Quinshon Judkins Rush+Rec Yds Over 61.5']
Notes:
  - cross-check (pick-side only, not a gated source): PFF player props page cross-check (pick side only, book unknown/logo only; not a no-vig source) pulled 2026-11-01T07:34
```
Phase 15 (1 PM inactives and reprice, 11:35–11:45 ET): see /workspace/nfl-database/week8/inactives/phase15_1pm_2026-11-01.md

GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_CLE@PIT  checked_at=2026-11-01 07:36 ET
Live legs: none
Cut legs: ['Aaron Rodgers Pass Yds Under 218.5', 'DK Metcalf Rec Yds Under 52.5', 'DK Metcalf Receptions Under 4.5', 'Darnell Washington Rec Yds Under 20.5', 'Darnell Washington Receptions Under 2.5', 'Denzel Boston Rec Yds Under 47.5', 'Denzel Boston Receptions Under 3.5', 'Deshaun Watson Pass Yds Under 210.5', 'Germie Bernard Rec Yds Over 43.5', 'Germie Bernard Receptions Under 4.5', 'Harold Fannin Jr. Rec Yds Under 34.5', 'Harold Fannin Jr. Receptions Under 3.5', 'Jaylen Warren Rush Yds Over 64.5', 'Jaylen Warren Rush+Rec Yds Over 91.5', 'Jerry Jeudy Rec Yds Over 21.5', 'Jerry Jeudy Receptions Over 2.5', 'KC Concepcion Rec Yds Under 46.5', 'KC Concepcion Receptions Under 4.5', 'Quinshon Judkins Rush Yds Over 47.5', 'Quinshon Judkins Rush+Rec Yds Over 61.5']

# CLE @ PIT — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): Deshaun Watson Pass Yds Under 210.5, KC Concepcion Rec Yds Under 46.5. Pass count 3 -> 1.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: Denzel Boston Receptions Under 3.5 - P14 FAIL: conflicts with placed UD Boston o29.5 rec yds (Ghost6 vet).
- Live legs now: none

## 1. Header
- Game: CLE @ PIT, game ID 401873027, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_CLE@PIT/checklist.md
- Candidate legs: 20 (key players × FD main market); passed 3, cut 17.

## 2. Phases run
- 1 Data pull: PASS 20
- 2 Opportunity: FAIL 2, PASS 18
- 3 Defense profile: FAIL 1, PASS 19
- 4 Defender coverage: FAIL 1, N/A 2, PASS 11, UNVERIFIED 6
- 5 Pressure/blitz/checkdown: N/A 2, PASS 18
- 6 QB card: FAIL 2, PASS 18
- 7 Role: FAIL 1, PASS 17, UNVERIFIED 2
- 8 Injuries: PASS 20
- 9 NGS: PASS 20
- 10 Film: PASS 20
- 11 Environment: PASS 20
- 12 Source audit: PASS 20
- 13 Game script 10G: FAIL 4, PASS 16
- 14 Models/price/edge: FAIL 9, PASS 9, UNVERIFIED 2
- 15 Inactives: PASS 20
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
| Deshaun Watson Pass Yds Under 210.5 | 0.519 / 206.7 | 0.723 / 174.9 | 0.520 / 206.7 |
| Quinshon Judkins Rush Yds Over 47.5 | 0.556 / 51.2 | 0.440 / 44.0 | 0.556 / 51.2 |
| Quinshon Judkins Rush+Rec Yds Over 61.5 | 0.659 / 72.6 | 0.517 / 62.6 | 0.643 / 71.9 |
| Jerry Jeudy Rec Yds Over 21.5 | 0.641 / 29.6 | 0.553 / 24.0 | 0.605 / 28.5 |
| Jerry Jeudy Receptions Over 2.5 | 0.547 / 3.0 | 0.473 / 2.0 | 0.513 / 3.0 |
| KC Concepcion Rec Yds Under 46.5 | 0.580 / 39.8 | 0.667 / 32.7 | 0.592 / 38.7 |
| KC Concepcion Receptions Under 4.5 | 0.630 / 4.0 | 0.700 / 3.0 | 0.632 / 4.0 |
| Denzel Boston Rec Yds Under 47.5 | 0.613 / 36.2 | 0.688 / 29.2 | 0.615 / 36.2 |
| Denzel Boston Receptions Under 3.5 | 0.658 / 3.0 | 0.727 / 2.0 | 0.655 / 3.0 |
| Harold Fannin Jr. Rec Yds Under 34.5 | 0.544 / 31.7 | 0.641 / 26.3 | 0.561 / 29.7 |
| Harold Fannin Jr. Receptions Under 3.5 | 0.550 / 3.0 | 0.626 / 3.0 | 0.566 / 3.0 |
| Aaron Rodgers Pass Yds Under 218.5 | 0.443 / 228.4 | 0.645 / 192.9 | 0.455 / 227.3 |
| Jaylen Warren Rush Yds Over 64.5 | 0.592 / 72.9 | 0.481 / 63.0 | 0.583 / 72.0 |
| Jaylen Warren Rush+Rec Yds Over 91.5 | 0.568 / 98.4 | 0.433 / 85.0 | 0.561 / 98.1 |
| DK Metcalf Rec Yds Under 52.5 | 0.545 / 47.8 | 0.621 / 40.3 | 0.546 / 47.8 |
| DK Metcalf Receptions Under 4.5 | 0.564 / 4.0 | 0.641 / 4.0 | 0.565 / 4.0 |
| Germie Bernard Rec Yds Over 43.5 | 0.564 / 50.8 | 0.484 / 41.2 | 0.539 / 48.3 |
| Germie Bernard Receptions Under 4.5 | 0.505 / 4.0 | 0.581 / 4.0 | 0.524 / 4.0 |
| Darnell Washington Rec Yds Under 20.5 | 0.641 / 14.1 | 0.699 / 11.6 | 0.649 / 13.2 |
| Darnell Washington Receptions Under 2.5 | 0.626 / 2.0 | 0.690 / 2.0 | 0.641 / 2.0 |

## 5. Projections and picks
- **Deshaun Watson Pass Yds Under 210.5 @ -113 (FanDuel)**: projection MC mean 212.0, median 206.7. No-vig 0.500; avg p 0.588; edge +8.8 pts before shrink, +6.1 after. FD main.
  - Opportunity: starter by dropbacks last game: True; proj 34.1 pa; MC mean 212.0
  - Matchup/coverage: QB leg vs PIT secondary: Asante Samuel Jr. 19t 52.6% 12.7 YPT; Jamel Dean 18t 66.7% 8.9 YPT; Jalen Ramsey 18t 66.7% 6.6 YPT | man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5%
  - Script: CLE +3.5 (underdog); total 38.5; FD main
- **KC Concepcion Rec Yds Under 46.5 @ -113 (FanDuel)**: projection MC mean 45.2, median 39.8. No-vig 0.500; avg p 0.613; edge +11.3 pts before shrink, +7.9 after. FD main.
  - Opportunity: rank 2 by tgt last3 (pbp [1, 6, 10]; ESPN box [1, 6, 10]); proj 34.1 pa x 0.156 = 5.3 tgt x cr 0.65 = 3.5 rec; MC mean 45.2 (under: volume recorded)
  - Matchup/coverage: cheatsheet: KC Concepcion (S: L20/S59/R21%) vs Jalen Ramsey | PFR Jalen Ramsey: 18 tgt, 66.7% cmp, 6.6 YPT, rtg 124.8 | man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5% | volume margin -3%
  - Script: CLE +3.5 (underdog); total 38.5; FD main
- **Denzel Boston Receptions Under 3.5 @ -174 (FanDuel)**: projection MC mean 2.9, median 3.0. No-vig 0.594; avg p 0.680; edge +8.7 pts before shrink, +3.3 after. FD main.
  - Opportunity: rank 1 by tgt last3 (pbp [7, 5, 8]; ESPN box [7, 5, 8]); proj 34.1 pa x 0.183 = 6.3 tgt x cr 0.47 = 3.0 rec; MC mean 2.9 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Denzel Boston (L: L49/S8/R43%) vs Jamel Dean | PFR Jamel Dean: 18 tgt, 66.7% cmp, 8.9 YPT, rtg 94.7 | man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5% | volume margin -16%
  - Script: CLE +3.5 (underdog); total 38.5; FD main

### Cut legs
- Quinshon Judkins Rush Yds Over 47.5: Phase 3 FAIL (RB YPC allowed <=3.8 suppression); Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4; rush-only over on possible trailer needs 4+ tgt/g); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Quinshon Judkins Rush+Rec Yds Over 61.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5%; awaiting ruling); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Jerry Jeudy Rec Yds Over 21.5: Phase 2 FAIL (not top-2 target earner (#4)); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Jerry Jeudy Receptions Over 2.5: Phase 2 FAIL (not top-2 target earner (#4); 5+ tgt in <3 of last 4); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception)); Phase 14 FAIL (a model median does not clear the line)
- KC Concepcion Receptions Under 4.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +18.2 pts > +15 implausible vs market (FD 4.5, consensus 4.5; possible role change the history-based sim cannot see) -> )
- Denzel Boston Rec Yds Under 47.5: Phase 14 FAIL (placed-ticket bar: UD20 Boston o29.5; MODEL-SUSPECT: MC median 36.2 vs FD main 47.5 / book consensus 48.8 (>=12 yds) -> Debugging)
- Harold Fannin Jr. Rec Yds Under 34.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5%; no stand-in allowed)
- Harold Fannin Jr. Receptions Under 3.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5%; no stand-in allowed)
- Aaron Rodgers Pass Yds Under 218.5: Phase 14 FAIL (edge +1.5 < +3; model p 0.443 < .45; a model median does not clear the line)
- Jaylen Warren Rush Yds Over 64.5: Phase 14 FAIL (a model median does not clear the line)
- Jaylen Warren Rush+Rec Yds Over 91.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 42.4% / zone 54.0%, MOF closed 72.6% / open 24.4%; awaiting ruling); Phase 6 FAIL (no-blitz D/F vs <25% blitz D); Phase 14 FAIL (placed-ticket bar: PP25 Warren o69.5 rush+rec; edge +2.1 < +3; model p 0.433 < .45; a model median does not clear the line)
- DK Metcalf Rec Yds Under 52.5: Phase 4 FAIL (yds under vs YPT>10 defender); Phase 7 UNVERIFIED (offense snap% last2 [] (snap rows missing))
- DK Metcalf Receptions Under 4.5: Phase 7 UNVERIFIED (offense snap% last2 [] (snap rows missing)); Phase 14 FAIL (edge +0.7 < +3; shrunk edge -2.0 not > 0)
- Germie Bernard Rec Yds Over 43.5: Phase 6 FAIL (no-blitz D/F vs <25% blitz D); Phase 14 FAIL (edge +2.9 < +3; a model median does not clear the line)
- Germie Bernard Receptions Under 4.5: Phase 14 FAIL (edge +0.9 < +3; shrunk edge -0.2 not > 0)
- Darnell Washington Rec Yds Under 20.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 42.4% / zone 54.0%, MOF closed 72.6% / open 24.4%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +16.3 pts > +15 implausible vs market (FD 20.5, consensus 21.2; possible role change the history-based sim cannot see) -)
- Darnell Washington Receptions Under 2.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 42.4% / zone 54.0%, MOF closed 72.6% / open 24.4%; no stand-in allowed)

## 6. Risks and checks still to come
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. No PFF row matches a live leg in this folder.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
