```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_LV@NYJ  checked_at=2026-11-01 07:31 ET
Live legs: ['Garrett Wilson Rec Yds Under 63.5', 'Garrett Wilson Receptions Under 5.5', 'Omar Cooper Jr. Receptions Under 3.5', 'Tre Tucker Receptions Over 3.5']
Cut legs: ['Brock Bowers Rec Yds Over 68.5', 'Brock Bowers Receptions Under 5.5', 'Geno Smith Pass Yds Under 225.5', 'Kirk Cousins Pass Yds Over 232.5', 'Omar Cooper Jr. Rec Yds Over 41.5', 'Tre Tucker Rec Yds Over 48.5']
APPROVED EXCEPTIONS:
  - leg Garrett Wilson Rec Yds Under 63.5 defender Eric Stokes: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Garrett Wilson Receptions Under 5.5 defender Eric Stokes: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Omar Cooper Jr. Receptions Under 3.5 defender Taron Johnson: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Tre Tucker Receptions Over 3.5 defender Azareye'h Thomas: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Garrett Wilson Rec Yds Under 63.5: avg p 0.576, no-vig 0.500, edge +7.6, shrunk +5.3
  - Garrett Wilson Receptions Under 5.5: avg p 0.668, no-vig 0.519, edge +14.9, shrunk +9.8
  - Omar Cooper Jr. Receptions Under 3.5: avg p 0.591, no-vig 0.561, edge +3.0, shrunk +0.3
  - Tre Tucker Receptions Over 3.5: avg p 0.591, no-vig 0.510, edge +8.0, shrunk +5.3
```

# LV @ NYJ — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## 1. Header
- Game: LV @ NYJ, game ID 401873029, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_LV@NYJ/checklist.md
- Candidate legs: 10 (key players × FD main market); passed 4, cut 6.

## 2. Phases run
- 1 Data pull: PASS 10
- 2 Opportunity: FAIL 1, PASS 9
- 3 Defense profile: PASS 10
- 4 Defender coverage: PASS 8, UNVERIFIED 2
- 5 Pressure/blitz/checkdown: PASS 10
- 6 QB card: PASS 10
- 7 Role: PASS 10
- 8 Injuries: PASS 10
- 9 NGS: PASS 10
- 10 Film: PASS 10
- 11 Environment: PASS 10
- 12 Source audit: PASS 10
- 13 Game script 10G: PASS 10
- 14 Models/price/edge: FAIL 6, PASS 4
- 15 Inactives: PASS 10
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
| Kirk Cousins Pass Yds Over 232.5 | 0.587 / 250.8 | 0.395 / 211.6 | 0.591 / 250.8 |
| Brock Bowers Rec Yds Over 68.5 | 0.559 / 73.1 | 0.419 / 61.8 | 0.523 / 70.4 |
| Brock Bowers Receptions Under 5.5 | 0.389 / 6.0 | 0.495 / 6.0 | 0.441 / 6.0 |
| Tre Tucker Rec Yds Over 48.5 | 0.600 / 57.9 | 0.498 / 48.3 | 0.572 / 56.1 |
| Tre Tucker Receptions Over 3.5 | 0.636 / 4.0 | 0.544 / 4.0 | 0.592 / 4.0 |
| Geno Smith Pass Yds Under 225.5 | 0.472 / 232.5 | 0.635 / 195.6 | 0.498 / 226.4 |
| Garrett Wilson Rec Yds Under 63.5 | 0.536 / 59.2 | 0.635 / 49.8 | 0.558 / 56.9 |
| Garrett Wilson Receptions Under 5.5 | 0.639 / 4.0 | 0.715 / 4.0 | 0.649 / 4.0 |
| Omar Cooper Jr. Rec Yds Over 41.5 | 0.574 / 48.4 | 0.490 / 41.4 | 0.542 / 46.0 |
| Omar Cooper Jr. Receptions Under 3.5 | 0.561 / 3.0 | 0.624 / 3.0 | 0.588 / 3.0 |

## 5. Projections and picks
- **Tre Tucker Receptions Over 3.5 @ -120 (FanDuel)**: projection MC mean 4.4, median 4.0. No-vig 0.510; avg p 0.591; edge +8.0 pts before shrink, +5.3 after. FD main.
  - Opportunity: rank 2 by tgt last3 (pbp [5, 7, 12]; ESPN box [5, 7, 12]); proj 38.9 pa x 0.189 = 7.3 tgt x cr 0.61 = 4.5 rec; MC mean 4.4
  - Matchup/coverage: cheatsheet: Tre Tucker (R: L35/S23/R41%) vs Azareye'h Thomas | PFR Azareye'h Thomas: 24 tgt, 70.8% cmp, 5.8 YPT, rtg 113.0 | man 23.8% / zone 66.6%, MOF closed 45.2% / open 50.0% | volume margin +28%
  - Script: LV +1.5 (toss-up); total 45.5; FD main
- **Garrett Wilson Rec Yds Under 63.5 @ -113 (FanDuel)**: projection MC mean 66.1, median 59.2. No-vig 0.500; avg p 0.576; edge +7.6 pts before shrink, +5.3 after. FD main.
  - Opportunity: rank 1 by tgt last3 (pbp [11, 6, 3]; ESPN box [11, 6, 3]); proj 31.7 pa x 0.202 = 6.4 tgt x cr 0.69 = 4.4 rec; MC mean 66.1 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Garrett Wilson (R: L42/S22/R36%) vs Eric Stokes | PFR Eric Stokes: 22 tgt, 50.0% cmp, 6.9 YPT, rtg 87.5 | man 21.4% / zone 70.0%, MOF closed 47.2% / open 47.2% | volume margin +4%
  - Script: NYJ -1.5 (toss-up); total 45.5; FD main
- **Garrett Wilson Receptions Under 5.5 @ -125 (FanDuel)**: projection MC mean 4.8, median 4.0. No-vig 0.519; avg p 0.668; edge +14.9 pts before shrink, +9.8 after. FD main.
  - Opportunity: rank 1 by tgt last3 (pbp [11, 6, 3]; ESPN box [11, 6, 3]); proj 31.7 pa x 0.202 = 6.4 tgt x cr 0.69 = 4.4 rec; MC mean 4.8 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Garrett Wilson (R: L42/S22/R36%) vs Eric Stokes | PFR Eric Stokes: 22 tgt, 50.0% cmp, 6.9 YPT, rtg 87.5 | man 21.4% / zone 70.0%, MOF closed 47.2% / open 47.2% | volume margin -20%
  - Script: NYJ -1.5 (toss-up); total 45.5; FD main
- **Omar Cooper Jr. Receptions Under 3.5 @ -148 (FanDuel)**: projection MC mean 3.6, median 3.0. No-vig 0.561; avg p 0.591; edge +3.0 pts before shrink, +0.3 after. FD main.
  - Opportunity: rank 4 by tgt last3 (pbp [1, 7, 5]; ESPN box [1, 7, 5]); proj 31.7 pa x 0.146 = 4.6 tgt x cr 0.83 = 3.8 rec; MC mean 3.6 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Omar Cooper Jr. (S: L21/S65/R15%) vs Taron Johnson | PFR Taron Johnson: 16 tgt, 50.0% cmp, 7.3 YPT, rtg 74.2 | man 21.4% / zone 70.0%, MOF closed 47.2% / open 47.2% | volume margin +10%
  - Script: NYJ -1.5 (toss-up); total 45.5; FD main

### Cut legs
- Kirk Cousins Pass Yds Over 232.5: Phase 14 FAIL (edge +2.4 < +3; model p 0.395 < .45; a model median does not clear the line; MODEL-SUSPECT: MC median 250.8 vs FD main 232.5 / book consensu)
- Brock Bowers Rec Yds Over 68.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 23.8% / zone 66.6%, MOF closed 45.2% / open 50.0%; no stand-in allowed); Phase 14 FAIL (placed-ticket bar: UD20 Bowers o49.5; FD 7-leg 50+; edge +0.0 < +3; model p 0.419 < .45; a model median does not clear the line)
- Brock Bowers Receptions Under 5.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 23.8% / zone 66.6%, MOF closed 45.2% / open 50.0%; no stand-in allowed); Phase 14 FAIL (edge +0.9 < +3; model p 0.389 < .45; a model median does not clear the line)
- Tre Tucker Rec Yds Over 48.5: Phase 14 FAIL (a model median does not clear the line)
- Geno Smith Pass Yds Under 225.5: Phase 14 FAIL (a model median does not clear the line)
- Omar Cooper Jr. Rec Yds Over 41.5: Phase 2 FAIL (not top-2 target earner (#4); not 4+ tgt in each of last 3); Phase 14 FAIL (a model median does not clear the line)

## 6. Risks and checks still to come
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
