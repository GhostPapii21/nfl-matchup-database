```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_NE@MIA  checked_at=2026-11-01 07:31 ET
Live legs: ['Ollie Gordon II Rush Yds Under 64.5']
Cut legs: ['DeMario Douglas Rec Yds Under 40.5', 'DeMario Douglas Receptions Under 3.5', 'Drake Maye Pass Yds Over 239.5', 'Eli Raridon Rec Yds Under 27.5', 'Eli Raridon Receptions Under 2.5', 'Greg Dulcich Rec Yds Over 29.5', 'Greg Dulcich Receptions Over 3.5', 'Hunter Henry Rec Yds Under 45.5', 'Hunter Henry Receptions Under 4.5', 'Malik Washington Rec Yds Over 41.5', 'Malik Washington Receptions Under 4.5', 'Malik Willis Pass Yds Under 185.5', 'Ollie Gordon II Rush+Rec Yds Under 78.5', 'Rhamondre Stevenson Rush Yds Under 58.5', 'Rhamondre Stevenson Rush+Rec Yds Under 87.5']
Notes:
  - Ollie Gordon II Rush Yds Under 64.5: avg p 0.609, no-vig 0.500, edge +10.9, shrunk +7.6
```

# NE @ MIA — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## 1. Header
- Game: NE @ MIA, game ID 401873034, kickoff 04:25 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_NE@MIA/checklist.md
- Candidate legs: 16 (key players × FD main market); passed 1, cut 15.

## 2. Phases run
- 1 Data pull: PASS 16
- 2 Opportunity: FAIL 3, PASS 13
- 3 Defense profile: FAIL 4, PASS 12
- 4 Defender coverage: MISSING 2, N/A 2, PASS 4, UNVERIFIED 8
- 5 Pressure/blitz/checkdown: N/A 2, PASS 11, UNVERIFIED 3
- 6 QB card: FAIL 3, PASS 13
- 7 Role: PASS 16
- 8 Injuries: PASS 16
- 9 NGS: PASS 16
- 10 Film: PASS 16
- 11 Environment: PASS 16
- 12 Source audit: PASS 16
- 13 Game script 10G: FAIL 8, PASS 8
- 14 Models/price/edge: FAIL 6, PASS 6, UNVERIFIED 4
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
| Drake Maye Pass Yds Over 239.5 | 0.608 / 259.5 | 0.382 / 220.1 | 0.610 / 259.5 |
| Rhamondre Stevenson Rush Yds Under 58.5 | 0.807 / 36.5 | 0.863 / 31.9 | 0.799 / 36.5 |
| Rhamondre Stevenson Rush+Rec Yds Under 87.5 | 0.793 / 59.4 | 0.865 / 50.8 | 0.778 / 58.2 |
| DeMario Douglas Rec Yds Under 40.5 | 0.518 / 38.4 | 0.603 / 31.4 | 0.527 / 37.3 |
| DeMario Douglas Receptions Under 3.5 | 0.493 / 4.0 | 0.576 / 3.0 | 0.521 / 3.0 |
| Hunter Henry Rec Yds Under 45.5 | 0.517 / 44.4 | 0.622 / 37.7 | 0.535 / 42.5 |
| Hunter Henry Receptions Under 4.5 | 0.544 / 4.0 | 0.635 / 4.0 | 0.564 / 4.0 |
| Eli Raridon Rec Yds Under 27.5 | 0.534 / 24.9 | 0.607 / 22.9 | 0.558 / 24.1 |
| Eli Raridon Receptions Under 2.5 | 0.515 / 2.0 | 0.587 / 2.0 | 0.550 / 2.0 |
| Malik Willis Pass Yds Under 185.5 | 0.671 / 153.5 | 0.794 / 129.4 | 0.674 / 153.5 |
| Ollie Gordon II Rush Yds Under 64.5 | 0.584 / 55.3 | 0.657 / 47.5 | 0.585 / 54.4 |
| Ollie Gordon II Rush+Rec Yds Under 78.5 | 0.614 / 63.8 | 0.689 / 53.9 | 0.616 / 62.3 |
| Malik Washington Rec Yds Over 41.5 | 0.567 / 46.3 | 0.458 / 37.7 | 0.544 / 45.2 |
| Malik Washington Receptions Under 4.5 | 0.607 / 4.0 | 0.687 / 3.0 | 0.612 / 4.0 |
| Greg Dulcich Rec Yds Over 29.5 | 0.585 / 35.4 | 0.489 / 29.4 | 0.549 / 33.7 |
| Greg Dulcich Receptions Over 3.5 | 0.529 / 4.0 | 0.441 / 3.0 | 0.490 / 3.0 |

## 5. Projections and picks
- **Ollie Gordon II Rush Yds Under 64.5 @ -113 (FanDuel)**: projection MC mean 64.3, median 55.3. No-vig 0.500; avg p 0.609; edge +10.9 pts before shrink, +7.6 after. FD main.
  - Opportunity: proj 29.0 ra x 0.571 = 16.6 car; 1.9 tgt; MC mean 64.3; primary back last2: True
  - Matchup/coverage: pure rushing leg: no coverage defender
  - Script: MIA +7 (underdog); total 43.5; FD main

### Cut legs
- Drake Maye Pass Yds Over 239.5: Phase 14 FAIL (model p 0.382 < .45; a model median does not clear the line; MODEL-SUSPECT: MC median 259.5 vs FD main 239.5 / book consensus 238.8 (>=12 yd)
- Rhamondre Stevenson Rush Yds Under 58.5: Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 36.5 vs FD main 58.5 / book consensus 59.5 (>=12 yds) -> Debugging)
- Rhamondre Stevenson Rush+Rec Yds Under 87.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 18.1% / zone 73.4%, MOF closed 42.1% / open 51.1%; awaiting ruling); Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 59.4 vs FD main 87.5 / book consensus 88.0 (>=12 yds) -> Debugging)
- DeMario Douglas Rec Yds Under 40.5: Phase 4 MISSING (defender not in PFR cache)
- DeMario Douglas Receptions Under 3.5: Phase 4 MISSING (defender not in PFR cache); Phase 14 FAIL (edge +1.6 < +3; a model median does not clear the line)
- Hunter Henry Rec Yds Under 45.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 18.1% / zone 73.4%, MOF closed 42.1% / open 51.1%; no stand-in allowed)
- Hunter Henry Receptions Under 4.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 18.1% / zone 73.4%, MOF closed 42.1% / open 51.1%; no stand-in allowed); Phase 14 FAIL (edge +0.6 < +3; shrunk edge -1.9 not > 0)
- Eli Raridon Rec Yds Under 27.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 18.1% / zone 73.4%, MOF closed 42.1% / open 51.1%; no stand-in allowed)
- Eli Raridon Receptions Under 2.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 18.1% / zone 73.4%, MOF closed 42.1% / open 51.1%; no stand-in allowed)
- Malik Willis Pass Yds Under 185.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 153.5 vs FD main 185.5 / book consensus 184.2 (>=12 yds) -> Debugging)
- Ollie Gordon II Rush+Rec Yds Under 78.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 30.8% / zone 63.8%, MOF closed 51.0% / open 45.4%; awaiting ruling); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED; underdog leg BLOCKED (10G)); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 63.8 vs FD main 78.5 / book consensus 78.0 (>=12 yds) -> Debugging)
- Malik Washington Rec Yds Over 41.5: Phase 2 FAIL (not 4+ tgt in each of last 3); Phase 5 UNVERIFIED (Panthers rule CAUTION: user decides); Phase 6 FAIL (vs-blitz D/F vs 35%+ blitz D; clutch D/F: no trailing-script overs)
- Malik Washington Receptions Under 4.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED)
- Greg Dulcich Rec Yds Over 29.5: Phase 2 FAIL (not top-2 target earner (#3)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 30.8% / zone 63.8%, MOF closed 51.0% / open 45.4%; no stand-in allowed); Phase 5 UNVERIFIED (Panthers rule CAUTION: user decides)
- Greg Dulcich Receptions Over 3.5: Phase 2 FAIL (not top-2 target earner (#3)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 30.8% / zone 63.8%, MOF closed 51.0% / open 45.4%; no stand-in allowed); Phase 5 UNVERIFIED (Panthers rule CAUTION: user decides)

## 6. Risks and checks still to come
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 2:35 PM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
