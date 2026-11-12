<!-- Phase 15 re-check 11:45 ET gate output -->
```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_BAL@BUF  checked_at=2026-11-01 11:41 ET
Live legs: none
Cut legs: ['DJ Moore Rec Yds Over 49.5', 'DJ Moore Receptions Under 4.5', 'Dalton Kincaid Rec Yds Under 46.5', 'Dalton Kincaid Receptions Under 3.5', 'Derrick Henry Rush Yds Under 78.5', 'Derrick Henry Rush+Rec Yds Under 89.5', 'James Cook Rush Yds Under 82.5', 'James Cook Rush+Rec Yds Under 96.5', 'Josh Allen Pass Yds Under 247.5', 'Keon Coleman Rec Yds Over 29.5', 'Keon Coleman Receptions Over 2.5', 'Khalil Shakir Rec Yds Under 41.5', 'Khalil Shakir Receptions Under 3.5', 'Lamar Jackson Pass Yds Under 237.5', 'Mark Andrews Rec Yds Over 27.5', 'Mark Andrews Receptions Under 3.5', 'Rashod Bateman Rec Yds Over 23.5', 'Rashod Bateman Receptions Under 2.5', 'Zay Flowers Rec Yds Over 82.5', 'Zay Flowers Receptions Over 6.5']
Notes:
  - cross-check (pick-side only, not a gated source): PFF player props page cross-check (pick side only, book unknown/logo only; not a no-vig source) pulled 2026-11-01T07:34
```
Phase 15 (1 PM inactives and reprice, 11:35–11:45 ET): see /workspace/nfl-database/week8/inactives/phase15_1pm_2026-11-01.md

GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_BAL@BUF  checked_at=2026-11-01 07:36 ET
Live legs: none
Cut legs: ['DJ Moore Rec Yds Over 49.5', 'DJ Moore Receptions Under 4.5', 'Dalton Kincaid Rec Yds Under 46.5', 'Dalton Kincaid Receptions Under 3.5', 'Derrick Henry Rush Yds Under 78.5', 'Derrick Henry Rush+Rec Yds Under 89.5', 'James Cook Rush Yds Under 82.5', 'James Cook Rush+Rec Yds Under 96.5', 'Josh Allen Pass Yds Under 247.5', 'Keon Coleman Rec Yds Over 29.5', 'Keon Coleman Receptions Over 2.5', 'Khalil Shakir Rec Yds Under 41.5', 'Khalil Shakir Receptions Under 3.5', 'Lamar Jackson Pass Yds Under 237.5', 'Mark Andrews Rec Yds Over 27.5', 'Mark Andrews Receptions Under 3.5', 'Rashod Bateman Rec Yds Over 23.5', 'Rashod Bateman Receptions Under 2.5', 'Zay Flowers Rec Yds Over 82.5', 'Zay Flowers Receptions Over 6.5']

# BAL @ BUF — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): Derrick Henry Rush Yds Under 78.5. Pass count 1 -> 0.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: none.
- Live legs now: none

## 1. Header
- Game: BAL @ BUF, game ID 401873026, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_BAL@BUF/checklist.md
- Candidate legs: 20 (key players × FD main market); passed 1, cut 19.

## 2. Phases run
- 1 Data pull: PASS 20
- 2 Opportunity: FAIL 6, PASS 14
- 3 Defense profile: FAIL 5, PASS 15
- 4 Defender coverage: N/A 2, PASS 10, UNVERIFIED 8
- 5 Pressure/blitz/checkdown: FAIL 2, N/A 2, PASS 16
- 6 QB card: PASS 20
- 7 Role: FAIL 2, PASS 16, UNVERIFIED 2
- 8 Injuries: PASS 20
- 9 NGS: PASS 20
- 10 Film: PASS 20
- 11 Environment: PASS 20
- 12 Source audit: PASS 20
- 13 Game script 10G: FAIL 5, PASS 15
- 14 Models/price/edge: FAIL 9, PASS 5, UNVERIFIED 6
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
| Lamar Jackson Pass Yds Under 237.5 | 0.666 / 206.3 | 0.819 / 174.2 | 0.646 / 205.4 |
| Derrick Henry Rush Yds Under 78.5 | 0.585 / 72.5 | 0.715 / 63.5 | 0.588 / 71.5 |
| Derrick Henry Rush+Rec Yds Under 89.5 | 0.598 / 81.9 | 0.734 / 71.2 | 0.598 / 81.0 |
| Zay Flowers Rec Yds Over 82.5 | 0.595 / 93.7 | 0.472 / 79.3 | 0.580 / 92.8 |
| Zay Flowers Receptions Over 6.5 | 0.566 / 7.0 | 0.449 / 6.0 | 0.542 / 7.0 |
| Rashod Bateman Rec Yds Over 23.5 | 0.550 / 26.5 | 0.472 / 21.7 | 0.511 / 24.7 |
| Rashod Bateman Receptions Under 2.5 | 0.581 / 2.0 | 0.638 / 2.0 | 0.606 / 2.0 |
| Mark Andrews Rec Yds Over 27.5 | 0.568 / 30.1 | 0.440 / 25.0 | 0.527 / 28.8 |
| Mark Andrews Receptions Under 3.5 | 0.579 / 3.0 | 0.659 / 3.0 | 0.599 / 3.0 |
| Josh Allen Pass Yds Under 247.5 | 0.603 / 227.7 | 0.785 / 192.6 | 0.607 / 225.8 |
| James Cook Rush Yds Under 82.5 | 0.496 / 82.5 | 0.638 / 71.4 | 0.515 / 80.9 |
| James Cook Rush+Rec Yds Under 96.5 | 0.564 / 91.0 | 0.704 / 78.8 | 0.576 / 89.1 |
| DJ Moore Rec Yds Over 49.5 | 0.302 / 24.5 | 0.248 / 17.9 | 0.301 / 18.8 |
| DJ Moore Receptions Under 4.5 | 0.781 / 2.0 | 0.812 / 2.0 | 0.767 / 2.0 |
| Khalil Shakir Rec Yds Under 41.5 | 0.507 / 40.8 | 0.588 / 33.8 | 0.516 / 39.7 |
| Khalil Shakir Receptions Under 3.5 | 0.465 / 4.0 | 0.552 / 3.0 | 0.488 / 4.0 |
| Keon Coleman Rec Yds Over 29.5 | 0.679 / 43.8 | 0.596 / 36.2 | 0.638 / 41.9 |
| Keon Coleman Receptions Over 2.5 | 0.634 / 3.0 | 0.556 / 3.0 | 0.584 / 3.0 |
| Dalton Kincaid Rec Yds Under 46.5 | 0.641 / 34.5 | 0.717 / 28.1 | 0.651 / 32.9 |
| Dalton Kincaid Receptions Under 3.5 | 0.546 / 3.0 | 0.619 / 3.0 | 0.567 / 3.0 |

## 5. Projections and picks
- **Derrick Henry Rush Yds Under 78.5 @ -113 (FanDuel)**: projection MC mean 75.4, median 72.5. No-vig 0.500; avg p 0.629; edge +12.9 pts before shrink, +9.0 after. FD main.
  - Opportunity: proj 28.5 ra x 0.690 = 19.7 car; 1.5 tgt; MC mean 75.4; primary back last2: True
  - Matchup/coverage: pure rushing leg: no coverage defender
  - Script: BAL +3 (underdog); total 54.5; FD main

### Cut legs
- Lamar Jackson Pass Yds Under 237.5: Phase 2 FAIL (starter by dropbacks last game: False; proj 31.8 pa; MC mean 212.2); Phase 3 FAIL (under vs top-8 pass yds allowed (rank 2)); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 206.3 vs FD main 237.5 / book consensus 237.8 (>=12 yds) -> Debugging)
- Derrick Henry Rush+Rec Yds Under 89.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 16.8% / zone 74.9%, MOF closed 45.8% / open 49.2%; awaiting ruling); Phase 13 FAIL (underdog leg BLOCKED (10G))
- Zay Flowers Rec Yds Over 82.5: Phase 5 FAIL (top-10 blitz D and player blitzed share drops >4 pts); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception)); Phase 14 FAIL (placed-ticket bar: UD20 o49.5; FD 7-leg 60+; $51.50 SGP 50+ (brief-only); a model median does not clear the line)
- Zay Flowers Receptions Over 6.5: Phase 5 FAIL (top-10 blitz D and player blitzed share drops >4 pts); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception)); Phase 14 FAIL (placed-ticket bar: PP25 o6; Ticket 2 5+; model p 0.449 < .45; a model median does not clear the line)
- Rashod Bateman Rec Yds Over 23.5: Phase 2 FAIL (not top-2 target earner (#4); not 4+ tgt in each of last 3); Phase 7 FAIL (snap share <60% in last 2); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Rashod Bateman Receptions Under 2.5: Phase 14 FAIL (edge +1.5 < +3; shrunk edge -1.8 not > 0)
- Mark Andrews Rec Yds Over 27.5: Phase 2 FAIL (not 4+ tgt in each of last 3); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 16.8% / zone 74.9%, MOF closed 45.8% / open 49.2%; no stand-in allowed); Phase 7 FAIL (snap share <60% in last 2)
- Mark Andrews Receptions Under 3.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 16.8% / zone 74.9%, MOF closed 45.8% / open 49.2%; no stand-in allowed)
- Josh Allen Pass Yds Under 247.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 227.7 vs FD main 247.5 / book consensus 247.8 (>=12 yds) -> Debugging)
- James Cook Rush Yds Under 82.5: Phase 14 FAIL (a model median does not clear the line)
- James Cook Rush+Rec Yds Under 96.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 15.9% / zone 78.6%, MOF closed 36.4% / open 61.4%; awaiting ruling); Phase 14 FAIL (placed-ticket bar: Ticket 2 Cook 70+ rush+rec)
- DJ Moore Rec Yds Over 49.5: Phase 2 FAIL (not top-2 target earner (#10); not 4+ tgt in each of last 3; proj yds 39.7 < 49.5); Phase 7 UNVERIFIED (offense snap% last2 [] (snap rows missing); 2025 (CHI): target rank 2, share 14.7%, 54+ yds in 35% of 17 games; 2026 share 11.7%); Phase 14 FAIL (edge -26.3 < +3; shrunk edge -19.8 not > 0; model p 0.248 < .45; a model median does not clear the line; MODEL-SUSPECT: MC median 24.5 vs FD)
- DJ Moore Receptions Under 4.5: Phase 3 FAIL (under vs soft WR D (YPT>=9.0)); Phase 7 UNVERIFIED (offense snap% last2 [] (snap rows missing); 2025 (CHI): target rank 2, share 14.7%, 54+ yds in 35% of 17 games; 2026 share 11.7%); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +19.3 pts > +15 implausible vs market (FD 4.5, consensus 4.5; possible role change the history-based sim cannot see) -> )
- Khalil Shakir Rec Yds Under 41.5: Phase 3 FAIL (under vs soft WR D (YPT>=9.0)); Phase 4 UNVERIFIED (defender sample 3 tgt < 8: too thin to grade)
- Khalil Shakir Receptions Under 3.5: Phase 3 FAIL (under vs soft WR D (YPT>=9.0)); Phase 4 UNVERIFIED (defender sample 3 tgt < 8: too thin to grade); Phase 14 FAIL (a model median does not clear the line)
- Keon Coleman Rec Yds Over 29.5: Phase 2 FAIL (not 4+ tgt in each of last 3); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 43.8 vs FD main 29.5 / book consensus 29.2 (>=12 yds) -> Debugging)
- Keon Coleman Receptions Over 2.5: Phase 2 FAIL (5+ tgt in <3 of last 4); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +16.3 pts > +15 implausible vs market (FD 2.5, consensus 2.5; possible role change the history-based sim cannot see) -> )
- Dalton Kincaid Rec Yds Under 46.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 15.9% / zone 78.6%, MOF closed 36.4% / open 61.4%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +17.0 pts > +15 implausible vs market (FD 46.5, consensus 46.2; possible role change the history-based sim cannot see) -)
- Dalton Kincaid Receptions Under 3.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 15.9% / zone 78.6%, MOF closed 36.4% / open 61.4%; no stand-in allowed)

## 6. Risks and checks still to come
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. No PFF row matches a live leg in this folder.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: DJ Moore, Dalton Kincaid.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
