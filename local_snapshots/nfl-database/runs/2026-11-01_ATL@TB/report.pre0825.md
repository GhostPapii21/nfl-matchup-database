GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_ATL@TB  checked_at=2026-11-01 07:36 ET
Live legs: ['Jahan Dotson Rec Yds Under 25.5']
Cut legs: ['Baker Mayfield Pass Yds Under 215.5', 'Bijan Robinson Rush Yds Under 80.5', 'Bijan Robinson Rush+Rec Yds Under 117.5', 'Bucky Irving Rush Yds Under 70.5', 'Bucky Irving Rush+Rec Yds Under 90.5', 'Cade Otton Rec Yds Under 33.5', 'Cade Otton Receptions Under 3.5', 'Chris Godwin Jr. Rec Yds Under 39.5', 'Chris Godwin Jr. Receptions Under 4.5', 'Drake London Rec Yds Under 79.5', 'Drake London Receptions Under 6.5', 'Jahan Dotson Receptions Under 2.5', 'Kyle Pitts Rec Yds Under 35.5', 'Kyle Pitts Receptions Under 3.5', 'Michael Penix Jr. Pass Yds Under 229.5']
APPROVED EXCEPTIONS:
  - leg Jahan Dotson Rec Yds Under 25.5 defender Zyon McCollum: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Jahan Dotson Rec Yds Under 25.5: avg p 0.595, no-vig 0.500, edge +9.5, shrunk +6.7

# ATL @ TB — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): Michael Penix Jr. Pass Yds Under 229.5, Drake London Rec Yds Under 79.5, Bucky Irving Rush Yds Under 70.5. Pass count 5 -> 2.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: Jahan Dotson Receptions Under 2.5 - P14 FAIL: same-player duplicate of Dotson Rec Yds Under 25.5 (Ghost6: pick one; kept the -113 yds leg).
- Live legs now: Jahan Dotson Rec Yds Under 25.5 (MC+GR avg p 0.574, no-vig 0.500, edge +7.4, shrunk +5.2)

## 1. Header
- Game: ATL @ TB, game ID 401873025, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_ATL@TB/checklist.md
- Candidate legs: 16 (key players × FD main market); passed 5, cut 11.

## 2. Phases run
- 1 Data pull: PASS 16
- 2 Opportunity: PASS 16
- 3 Defense profile: FAIL 1, PASS 15
- 4 Defender coverage: N/A 2, PASS 6, UNVERIFIED 8
- 5 Pressure/blitz/checkdown: N/A 2, PASS 14
- 6 QB card: PASS 16
- 7 Role: PASS 16
- 8 Injuries: PASS 16
- 9 NGS: PASS 16
- 10 Film: PASS 14, UNVERIFIED 2
- 11 Environment: PASS 16
- 12 Source audit: PASS 16
- 13 Game script 10G: PASS 16
- 14 Models/price/edge: FAIL 3, PASS 8, UNVERIFIED 5
- 15 Inactives: PASS 16
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
| Michael Penix Jr. Pass Yds Under 229.5 | 0.550 / 221.2 | 0.740 / 185.6 | 0.560 / 217.5 |
| Bijan Robinson Rush Yds Under 80.5 | 0.640 / 65.9 | 0.733 / 57.5 | 0.648 / 63.6 |
| Bijan Robinson Rush+Rec Yds Under 117.5 | 0.703 / 92.9 | 0.803 / 79.7 | 0.694 / 89.7 |
| Drake London Rec Yds Under 79.5 | 0.511 / 78.2 | 0.634 / 65.3 | 0.534 / 74.8 |
| Drake London Receptions Under 6.5 | 0.597 / 6.0 | 0.702 / 5.0 | 0.607 / 6.0 |
| Jahan Dotson Rec Yds Under 25.5 | 0.573 / 22.5 | 0.637 / 19.4 | 0.576 / 22.5 |
| Jahan Dotson Receptions Under 2.5 | 0.726 / 2.0 | 0.777 / 1.0 | 0.726 / 2.0 |
| Kyle Pitts Rec Yds Under 35.5 | 0.584 / 31.0 | 0.668 / 25.4 | 0.598 / 28.9 |
| Kyle Pitts Receptions Under 3.5 | 0.568 / 3.0 | 0.646 / 3.0 | 0.590 / 3.0 |
| Baker Mayfield Pass Yds Under 215.5 | 0.731 / 160.9 | 0.826 / 134.5 | 0.732 / 150.7 |
| Bucky Irving Rush Yds Under 70.5 | 0.517 / 69.3 | 0.627 / 60.0 | 0.535 / 66.7 |
| Bucky Irving Rush+Rec Yds Under 90.5 | 0.584 / 82.5 | 0.699 / 70.9 | 0.588 / 79.8 |
| Chris Godwin Jr. Rec Yds Under 39.5 | 0.498 / 39.7 | 0.600 / 33.2 | 0.586 / 30.1 |
| Chris Godwin Jr. Receptions Under 4.5 | 0.629 / 4.0 | 0.709 / 3.0 | 0.667 / 3.0 |
| Cade Otton Rec Yds Under 33.5 | 0.777 / 17.6 | 0.827 / 13.0 | 0.767 / 13.7 |
| Cade Otton Receptions Under 3.5 | 0.798 / 2.0 | 0.838 / 2.0 | 0.783 / 2.0 |

## 5. Projections and picks
- **Michael Penix Jr. Pass Yds Under 229.5 @ -113 (FanDuel)**: projection MC mean 226.6, median 221.2. No-vig 0.500; avg p 0.617; edge +11.7 pts before shrink, +8.2 after. FD main.
  - Opportunity: starter by dropbacks last game: True; proj 31.3 pa; MC mean 226.6
  - Matchup/coverage: QB leg vs TB secondary: Zyon McCollum 22t 63.6% 6.9 YPT; Benjamin Morrison 17t 64.7% 5.2 YPT; Jacob Parrish 28t 60.7% 8.2 YPT | man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6%
  - Script: ATL +2.5 (toss-up); total 43.5; FD main
- **Drake London Rec Yds Under 79.5 @ -113 (FanDuel)**: projection MC mean 84.1, median 78.2. No-vig 0.500; avg p 0.560; edge +6.0 pts before shrink, +4.2 after. FD main.
  - Opportunity: rank 1 by tgt last3 (pbp [11, 10, 10]; ESPN box [11, 10, 10]); proj 31.3 pa x 0.284 = 8.9 tgt x cr 0.68 = 6.0 rec; MC mean 84.1 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Drake London (L: L37/S38/R25%) vs Jacob Parrish | PFR Jacob Parrish: 28 tgt, 60.7% cmp, 8.2 YPT, rtg 83.9 | man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6% | volume margin +6%
  - Script: ATL +2.5 (toss-up); total 43.5; FD main
- **Jahan Dotson Rec Yds Under 25.5 @ -113 (FanDuel)**: projection MC mean 25.7, median 22.5. No-vig 0.500; avg p 0.595; edge +9.5 pts before shrink, +6.7 after. FD main.
  - Opportunity: rank 4 by tgt last3 (pbp [4, 5, 3]; ESPN box [4, 5, 3]); proj 31.3 pa x 0.110 = 3.4 tgt x cr 0.48 = 1.7 rec; MC mean 25.7 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Jahan Dotson (R: L33/S23/R44%) vs Zyon McCollum | PFR Zyon McCollum: 22 tgt, 63.6% cmp, 6.9 YPT, rtg 99.1 | man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6% | volume margin +1%
  - Script: ATL +2.5 (toss-up); total 43.5; FD main
- **Jahan Dotson Receptions Under 2.5 @ -180 (FanDuel)**: projection MC mean 1.8, median 2.0. No-vig 0.601; avg p 0.743; edge +14.2 pts before shrink, +6.9 after. FD main.
  - Opportunity: rank 4 by tgt last3 (pbp [4, 5, 3]; ESPN box [4, 5, 3]); proj 31.3 pa x 0.110 = 3.4 tgt x cr 0.48 = 1.7 rec; MC mean 1.8 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Jahan Dotson (R: L33/S23/R44%) vs Zyon McCollum | PFR Zyon McCollum: 22 tgt, 63.6% cmp, 6.9 YPT, rtg 99.1 | man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6% | volume margin -33%
  - Script: ATL +2.5 (toss-up); total 43.5; FD main
- **Bucky Irving Rush Yds Under 70.5 @ -113 (FanDuel)**: projection MC mean 76.8, median 69.3. No-vig 0.500; avg p 0.560; edge +6.0 pts before shrink, +4.2 after. FD main.
  - Opportunity: proj 29.6 ra x 0.587 = 17.4 car; 3.0 tgt; MC mean 76.8; primary back last2: True
  - Matchup/coverage: pure rushing leg: no coverage defender
  - Script: TB -2.5 (toss-up); total 43.5; FD main

### Cut legs
- Bijan Robinson Rush Yds Under 80.5: Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 65.9 vs FD main 80.5 / book consensus 80.8 (>=12 yds) -> Debugging)
- Bijan Robinson Rush+Rec Yds Under 117.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6%; awaiting ruling); Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 92.9 vs FD main 117.5 / book consensus 117.5 (>=12 yds) -> Debugging)
- Drake London Receptions Under 6.5: Phase 14 FAIL (placed-ticket bar: UD20 o5.5; Ticket 2 5+)
- Kyle Pitts Rec Yds Under 35.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6%; no stand-in allowed)
- Kyle Pitts Receptions Under 3.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 17.2% / zone 78.0%, MOF closed 58.6% / open 39.6%; no stand-in allowed)
- Baker Mayfield Pass Yds Under 215.5: Phase 3 FAIL (under vs top-8 pass yds allowed (rank 4)); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 160.9 vs FD main 215.5 / book consensus 214.2 (>=12 yds) -> Debugging)
- Bucky Irving Rush+Rec Yds Under 90.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 21.9% / zone 70.3%, MOF closed 59.5% / open 34.3%; awaiting ruling)
- Chris Godwin Jr. Rec Yds Under 39.5: Phase 4 UNVERIFIED (defender sample 7 tgt < 8: too thin to grade); Phase 14 FAIL (a model median does not clear the line)
- Chris Godwin Jr. Receptions Under 4.5: Phase 4 UNVERIFIED (defender sample 7 tgt < 8: too thin to grade); Phase 14 FAIL (placed-ticket bar: Ticket 2 Godwin 4+; $51.50 SGP 3+ (brief-only))
- Cade Otton Rec Yds Under 33.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 21.9% / zone 70.3%, MOF closed 59.5% / open 34.3%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 17.6 vs FD main 33.5 / book consensus 33.5 (>=12 yds) -> Debugging)
- Cade Otton Receptions Under 3.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 21.9% / zone 70.3%, MOF closed 59.5% / open 34.3%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +30.6 pts > +15 implausible vs market (FD 3.5, consensus 3.5; possible role change the history-based sim cannot see) -> )

## 6. Risks and checks still to come
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. Jahan Dotson Rec Yds Under 25.5: PFF pick UNDER 25.5 -113, proj 19.5 - AGREES; Jahan Dotson Receptions Under 2.5: PFF lists Recs 1.5 OVER -175 (proj 1.63, edge -0.7%); different line; proj 1.63 < 2.5 supports our under - no opposite-side flag at our line
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 2 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
