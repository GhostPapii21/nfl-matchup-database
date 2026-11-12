GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_KC@DEN  checked_at=2026-11-01 08:40 ET
Live legs: ['Xavier Worthy Rec Yds Over 29.5']
Cut legs: ['Bo Nix Pass Yds Under 208.5', 'Courtland Sutton Rec Yds Under 40.5', 'Courtland Sutton Receptions Under 3.5', 'Evan Engram Rec Yds Under 24.5', 'Evan Engram Receptions Under 2.5', 'J.K. Dobbins Rush Yds Over 29.5', 'Jonah Coleman Rush Yds Under 44.5', 'Jonah Coleman Rush+Rec Yds Under 70.5', 'Kenneth Walker III Rush Yds Over 85.5', 'Kenneth Walker III Rush+Rec Yds Over 107.5', 'Patrick Mahomes Pass Yds Under 220.5', 'Rashee Rice Rec Yds Under 51.5', 'Rashee Rice Receptions Under 4.5', 'Travis Kelce Rec Yds Under 46.5', 'Travis Kelce Receptions Under 4.5', 'Xavier Worthy Receptions Over 3.5']
APPROVED EXCEPTIONS:
  - leg Xavier Worthy Rec Yds Over 29.5 defender Riley Moss: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Xavier Worthy Rec Yds Over 29.5: avg p 0.589, no-vig 0.500, edge +8.9, shrunk +6.2

# KC @ DEN — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): none. Pass count 1 -> 1.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: none.
- Live legs now: Xavier Worthy Rec Yds Over 29.5 (MC+GR avg p 0.603, no-vig 0.500, edge +10.3, shrunk +7.2)

## 1. Header
- Game: KC @ DEN, game ID 401873033, kickoff 04:25 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_KC@DEN/checklist.md
- Candidate legs: 17 (key players × FD main market); passed 1, cut 16.

## 2. Phases run
- 1 Data pull: FAIL 2, PASS 15
- 2 Opportunity: PASS 17
- 3 Defense profile: FAIL 1, PASS 16
- 4 Defender coverage: FAIL 1, N/A 3, PASS 5, UNVERIFIED 8
- 5 Pressure/blitz/checkdown: N/A 3, PASS 14
- 6 QB card: FAIL 1, PASS 16
- 7 Role: FAIL 1, PASS 16
- 8 Injuries: PASS 17
- 9 NGS: PASS 17
- 10 Film: PASS 17
- 11 Environment: PASS 17
- 12 Source audit: PASS 17
- 13 Game script 10G: PASS 17
- 14 Models/price/edge: FAIL 4, PASS 4, UNVERIFIED 9
- 15 Inactives: PASS 17
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
| Patrick Mahomes Pass Yds Under 220.5 | 0.532 / 214.1 | 0.704 / 179.5 | 0.543 / 212.2 |
| Kenneth Walker III Rush Yds Over 85.5 | 0.624 / 99.2 | 0.500 / 86.1 | 0.593 / 97.3 |
| Kenneth Walker III Rush+Rec Yds Over 107.5 | 0.571 / 116.6 | 0.444 / 100.6 | 0.558 / 115.4 |
| Rashee Rice Rec Yds Under 51.5 | 0.560 / 45.3 | 0.645 / 36.8 | 0.609 / 35.1 |
| Rashee Rice Receptions Under 4.5 | 0.647 / 3.0 | 0.708 / 3.0 | 0.662 / 3.0 |
| Xavier Worthy Rec Yds Over 29.5 | 0.618 / 37.3 | 0.534 / 30.7 | 0.588 / 36.1 |
| Xavier Worthy Receptions Over 3.5 | 0.544 / 4.0 | 0.456 / 3.0 | 0.513 / 4.0 |
| Travis Kelce Rec Yds Under 46.5 | 0.576 / 39.6 | 0.644 / 31.9 | 0.576 / 39.6 |
| Travis Kelce Receptions Under 4.5 | 0.652 / 4.0 | 0.715 / 3.0 | 0.655 / 4.0 |
| Bo Nix Pass Yds Under 208.5 | 0.735 / 169.0 | 0.869 / 143.0 | 0.741 / 169.0 |
| J.K. Dobbins Rush Yds Over 29.5 | 0.707 / 39.6 | 0.598 / 34.0 | 0.673 / 38.6 |
| Jonah Coleman Rush Yds Under 44.5 | 0.752 / 33.0 | 0.835 / 29.2 | 0.742 / 33.0 |
| Jonah Coleman Rush+Rec Yds Under 70.5 | 0.841 / 49.4 | 0.920 / 42.7 | 0.828 / 48.8 |
| Courtland Sutton Rec Yds Under 40.5 | 0.824 / 20.2 | 0.878 / 16.0 | 0.818 / 20.2 |
| Courtland Sutton Receptions Under 3.5 | 0.856 / 2.0 | 0.893 / 2.0 | 0.848 / 2.0 |
| Evan Engram Rec Yds Under 24.5 | 0.722 / 13.3 | 0.782 / 9.9 | 0.718 / 11.4 |
| Evan Engram Receptions Under 2.5 | 0.737 / 2.0 | 0.787 / 1.0 | 0.731 / 1.0 |

## 5. Projections and picks
- **Xavier Worthy Rec Yds Over 29.5 @ -113 (FanDuel)**: projection MC mean 43.8, median 37.3. No-vig 0.500; avg p 0.580; edge +8.0 pts before shrink, +5.6 after. FD main.
  - Opportunity: rank 1 by tgt last3 (pbp [7, 7, 6]; ESPN box [7, 7, 6]); proj 34.2 pa x 0.208 = 7.1 tgt x cr 0.63 = 4.5 rec; MC mean 43.8
  - Matchup/coverage: cheatsheet: Xavier Worthy (R: L31/S28/R41%) vs Riley Moss | PFR Riley Moss: 22 tgt, 50.0% cmp, 6.6 YPT, rtg 91.9 | man 24.5% / zone 70.3%, MOF closed 48.0% / open 48.3% | volume margin +48%
  - Script: KC -1.5 (toss-up); total 40.5; FD main

### Cut legs
- Patrick Mahomes Pass Yds Under 220.5: Phase 14 FAIL (placed-ticket bar: PP20 Mahomes o0.5 pass yds)
- Kenneth Walker III Rush Yds Over 85.5: Phase 14 FAIL (placed-ticket bar: PP40 o97.5; UD20 o69.5; MODEL-SUSPECT: MC median 99.2 vs FD main 85.5 / book consensus 86.8 (>=12 yds) -> Debugging)
- Kenneth Walker III Rush+Rec Yds Over 107.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 24.5% / zone 70.3%, MOF closed 48.0% / open 48.3%; awaiting ruling); Phase 14 FAIL (edge +2.4 < +3; model p 0.444 < .45; a model median does not clear the line)
- Rashee Rice Rec Yds Under 51.5: Phase 4 FAIL (yds under vs YPT>10 defender)
- Rashee Rice Receptions Under 4.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +15.3 pts > +15 implausible vs market (FD 4.5, consensus 4.5; possible role change the history-based sim cannot see) -> )
- Xavier Worthy Receptions Over 3.5: Phase 14 FAIL (a model median does not clear the line)
- Travis Kelce Rec Yds Under 46.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 24.5% / zone 70.3%, MOF closed 48.0% / open 48.3%; no stand-in allowed)
- Travis Kelce Receptions Under 4.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 24.5% / zone 70.3%, MOF closed 48.0% / open 48.3%; no stand-in allowed)
- Bo Nix Pass Yds Under 208.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 169.0 vs FD main 208.5 / book consensus 207.2 (>=12 yds) -> Debugging)
- J.K. Dobbins Rush Yds Over 29.5: Phase 3 FAIL (RB YPC allowed <=3.8 suppression); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4; rush-only over on possible trailer needs 4+ tgt/g)
- Jonah Coleman Rush Yds Under 44.5: Phase 1 FAIL (2 games; last3 09-20 3t/3r/19y/10c/39ry, 10-25 2t/2r/15y/9c/54ry); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +27.6 pts > +15 implausible vs market (FD 44.5, consensus 44.2; possible role change the history-based sim cannot see) -)
- Jonah Coleman Rush+Rec Yds Under 70.5: Phase 1 FAIL (2 games; last3 09-20 3t/3r/19y/10c/39ry, 10-25 2t/2r/15y/9c/54ry); Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 17.6% / zone 79.1%, MOF closed 44.6% / open 52.8%; awaiting ruling); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 49.4 vs FD main 70.5 / book consensus 70.0 (>=12 yds) -> Debugging)
- Courtland Sutton Rec Yds Under 40.5: Phase 4 UNVERIFIED (defender sample 7 tgt < 8: too thin to grade); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 20.2 vs FD main 40.5 / book consensus 40.5 (>=12 yds) -> Debugging)
- Courtland Sutton Receptions Under 3.5: Phase 4 UNVERIFIED (defender sample 7 tgt < 8: too thin to grade); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +35.1 pts > +15 implausible vs market (FD 3.5, consensus 3.5; possible role change the history-based sim cannot see) -> )
- Evan Engram Rec Yds Under 24.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 17.6% / zone 79.1%, MOF closed 44.6% / open 52.8%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +24.1 pts > +15 implausible vs market (FD 24.5, consensus 24.2; possible role change the history-based sim cannot see) -)
- Evan Engram Receptions Under 2.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 17.6% / zone 79.1%, MOF closed 44.6% / open 52.8%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +26.6 pts > +15 implausible vs market (FD 2.5, consensus 2.5; possible role change the history-based sim cannot see) -> )

## 6. Risks and checks still to come
- 08:25 refresh (run 08:36 ET): tools/sim_v6.py (calibrated bias model; BUG-2026-11-01-BIAS fixed; tools/tests 35/35 OK at 08:36) replaced sim_v5.py for this re-score, 100,000 sims x 3 models, seed 20261101; v5 numbers kept in run_manifest.json `sims_v5`. Odds re-pulled 08:36 ET via The Odds API (pull_odds.py/pull_lines.py, odds_r0835.csv / lines_r0835.json); the 08:36 odds go stale at 09:36 ET. PFF props csv (captured 07:40 ET) is a pick-side cross-check only and was moved from `sources` to `cross_checks` because it is over 1 h old. PFR per-defender cache pfr_def_adv_2026.html exception still applies (Rico, valid 2026-11-01 only). Pre-refresh files saved as *.pre0825.*.
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. Xavier Worthy Rec Yds Over 29.5: PFF pick OVER 29.5 -110, proj 34.5 - AGREES
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 2:35 PM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).

## 08:25 ET refresh — re-priced 08:36 ET, re-scored on sim_v6 (v5 shown side by side)

All lines unchanged vs the vetted run. Spreads unchanged; FD totals moved KC@DEN 40.5→41.5 and LV@NYJ 45.5→46.5 (sims use spread, not total).

| Leg | 07:30-07:44 price / no-vig | 08:36 price / no-vig | v5 gate edge / shrunk | v5 MC+GR edge | v6 p MC/Bias/GR | v6 medians | v6 gate edge / shrunk | PFF side | Status |
|---|---|---|---|---|---|---|---|---|---|
| Xavier Worthy Rec Yds Over 29.5 | -113 / 0.500 | -113 / 0.500 (FD main) | +8.0 / +5.6 | +10.3 | 0.598/0.597/0.571 | 35.8315/35.8315/35.3046 | +8.9 / +6.2 | PFF OVER 29.5 (proj 34.5; 57.3% per Ghost6) - agrees | PASS |
