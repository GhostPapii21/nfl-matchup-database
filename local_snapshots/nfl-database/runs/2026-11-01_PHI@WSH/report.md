
## CUT 08:46 ET (BUG-2026-11-01-FORM, standing rule: gate fail = cut)
- Stefon Diggs Rec Yds Over 42.5: CUT — WITHDRAWN by Ghost6; fails §14
- Remaining live legs: []

GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_PHI@WSH  checked_at=2026-11-01 08:40 ET
Live legs (after 08:46 cuts): []
(superseded) Live legs: ['Stefon Diggs Rec Yds Over 42.5']
Cut legs: ['Chig Okonkwo Rec Yds Under 32.5', 'Chig Okonkwo Receptions Over 3.5', 'Dallas Goedert Rec Yds Over 45.5', 'Dallas Goedert Receptions Under 4.5', 'Darius Cooper Rec Yds Under 27.5', 'Darius Cooper Receptions Under 2.5', 'Dyami Brown Rec Yds Under 12.5', 'Dyami Brown Receptions Under 1.5', 'Jayden Daniels Pass Yds Under 198.5', 'Makai Lemon Rec Yds Under 43.5', 'Makai Lemon Receptions Under 4.5', 'Rachaad White Rush Yds Under 39.5', 'Rachaad White Rush+Rec Yds Under 56.5', 'Saquon Barkley Rush Yds Under 52.5', 'Saquon Barkley Rush+Rec Yds Under 69.5', 'Stefon Diggs Receptions Over 4.5']
APPROVED EXCEPTIONS:
  - leg Stefon Diggs Rec Yds Over 42.5 defender Cooper DeJean: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Stefon Diggs Rec Yds Over 42.5: avg p 0.607, no-vig 0.500, edge +10.7, shrunk +7.5

# PHI @ WSH — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): none. Pass count 1 -> 1.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: none.
- Live legs now: Stefon Diggs Rec Yds Over 42.5 (MC+GR avg p 0.625, no-vig 0.500, edge +12.4, shrunk +8.7)

## 1. Header
- Game: PHI @ WSH, game ID 401873035, kickoff 08:20 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_PHI@WSH/checklist.md
- Candidate legs: 17 (key players × FD main market); passed 1, cut 16.

## 2. Phases run
- 1 Data pull: PASS 17
- 2 Opportunity: FAIL 2, PASS 15
- 3 Defense profile: FAIL 1, PASS 16
- 4 Defender coverage: MISSING 4, N/A 2, PASS 5, UNVERIFIED 6
- 5 Pressure/blitz/checkdown: FAIL 1, N/A 2, PASS 14
- 6 QB card: FAIL 1, PASS 16
- 7 Role: PASS 17
- 8 Injuries: PASS 17
- 9 NGS: PASS 17
- 10 Film: PASS 13, UNVERIFIED 4
- 11 Environment: PASS 17
- 12 Source audit: PASS 17
- 13 Game script 10G: FAIL 2, PASS 15
- 14 Models/price/edge: FAIL 5, PASS 4, UNVERIFIED 8
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
| Saquon Barkley Rush Yds Under 52.5 | 0.748 / 28.9 | 0.793 / 23.7 | 0.724 / 27.3 |
| Saquon Barkley Rush+Rec Yds Under 69.5 | 0.794 / 36.8 | 0.839 / 31.1 | 0.772 / 35.1 |
| Makai Lemon Rec Yds Under 43.5 | 0.549 / 39.7 | 0.650 / 32.7 | 0.572 / 37.1 |
| Makai Lemon Receptions Under 4.5 | 0.594 / 4.0 | 0.679 / 4.0 | 0.610 / 4.0 |
| Darius Cooper Rec Yds Under 27.5 | 0.714 / 14.1 | 0.763 / 12.6 | 0.719 / 10.2 |
| Darius Cooper Receptions Under 2.5 | 0.758 / 1.0 | 0.803 / 1.0 | 0.748 / 1.0 |
| Dallas Goedert Rec Yds Over 45.5 | 0.550 / 49.5 | 0.446 / 40.9 | 0.519 / 47.3 |
| Dallas Goedert Receptions Under 4.5 | 0.458 / 5.0 | 0.555 / 4.0 | 0.500 / 4.0 |
| Jayden Daniels Pass Yds Under 198.5 | 0.566 / 185.3 | 0.706 / 155.3 | 0.516 / 196.2 |
| Rachaad White Rush Yds Under 39.5 | 0.753 / 27.9 | 0.830 / 24.5 | 0.732 / 26.9 |
| Rachaad White Rush+Rec Yds Under 56.5 | 0.742 / 41.7 | 0.832 / 36.3 | 0.721 / 40.5 |
| Stefon Diggs Rec Yds Over 42.5 | 0.631 / 52.3 | 0.509 / 43.5 | 0.618 / 51.0 |
| Stefon Diggs Receptions Over 4.5 | 0.500 / 4.0 | 0.404 / 4.0 | 0.494 / 4.0 |
| Dyami Brown Rec Yds Under 12.5 | 0.650 / 8.7 | 0.687 / 3.5 | 0.667 / 3.7 |
| Dyami Brown Receptions Under 1.5 | 0.615 / 1.0 | 0.662 / 1.0 | 0.642 / 1.0 |
| Chig Okonkwo Rec Yds Under 32.5 | 0.490 / 33.4 | 0.569 / 28.9 | 0.509 / 32.4 |
| Chig Okonkwo Receptions Over 3.5 | 0.533 / 4.0 | 0.441 / 3.0 | 0.498 / 3.0 |

## 5. Projections and picks
- **Stefon Diggs Rec Yds Over 42.5 @ -113 (FanDuel)**: projection MC mean 54.7, median 52.3. No-vig 0.500; avg p 0.586; edge +8.6 pts before shrink, +6.0 after. FD main.
  - Opportunity: rank 2 by tgt last3 (pbp [7, 9, 7]; ESPN box [7, 9, 7]); proj 32.8 pa x 0.202 = 6.6 tgt x cr 0.61 = 4.1 rec; MC mean 54.7
  - Matchup/coverage: cheatsheet: Stefon Diggs (S: L18/S63/R19%) vs Cooper DeJean | PFR Cooper DeJean: 17 tgt, 70.6% cmp, 6.4 YPT, rtg 102.1 | man 15.1% / zone 72.8%, MOF closed 49.1% / open 43.4% | volume margin +29%
  - Script: WSH -5.5 (moderate favorite); total 40.5; FD main

### Cut legs
- Saquon Barkley Rush Yds Under 52.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 28.9 vs FD main 52.5 / book consensus 52.2 (>=12 yds) -> Debugging)
- Saquon Barkley Rush+Rec Yds Under 69.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 12.9% / zone 76.9%, MOF closed 29.6% / open 62.8%; awaiting ruling); Phase 13 FAIL (underdog leg BLOCKED (10G)); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 36.8 vs FD main 69.5 / book consensus 68.0 (>=12 yds) -> Debugging)
- Makai Lemon Rec Yds Under 43.5: Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player)
- Makai Lemon Receptions Under 4.5: Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player)
- Darius Cooper Rec Yds Under 27.5: Phase 4 MISSING (no ESPN WR/CB cheatsheet mapping for Darius Cooper; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 14.1 vs FD main 27.5 / book consensus 26.5 (>=12 yds) -> Debugging)
- Darius Cooper Receptions Under 2.5: Phase 4 MISSING (no ESPN WR/CB cheatsheet mapping for Darius Cooper; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +25.6 pts > +15 implausible vs market (FD 2.5, consensus 2.5; possible role change the history-based sim cannot see) -> )
- Dallas Goedert Rec Yds Over 45.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 12.9% / zone 76.9%, MOF closed 29.6% / open 62.8%; no stand-in allowed); Phase 5 FAIL (top-10 blitz D and player blitzed share drops >4 pts; Panthers rule CAUTION: user decides); Phase 6 FAIL (vs-blitz D/F vs 35%+ blitz D; clutch D/F: no trailing-script overs)
- Dallas Goedert Receptions Under 4.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 12.9% / zone 76.9%, MOF closed 29.6% / open 62.8%; no stand-in allowed); Phase 14 FAIL (a model median does not clear the line)
- Jayden Daniels Pass Yds Under 198.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 185.3 vs FD main 198.5 / book consensus 199.5 (>=12 yds) -> Debugging)
- Rachaad White Rush Yds Under 39.5: Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 27.9 vs FD main 39.5 / book consensus 41.8 (>=12 yds) -> Debugging)
- Rachaad White Rush+Rec Yds Under 56.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 15.1% / zone 72.8%, MOF closed 49.1% / open 43.4%; awaiting ruling); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 41.7 vs FD main 56.5 / book consensus 57.5 (>=12 yds) -> Debugging)
- Stefon Diggs Receptions Over 4.5: Phase 2 FAIL (proj rec 4.1 < 4.5); Phase 14 FAIL (model p 0.404 < .45; a model median does not clear the line)
- Dyami Brown Rec Yds Under 12.5: Phase 4 MISSING (no ESPN WR/CB cheatsheet mapping for Dyami Brown; no stand-in allowed); Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +16.8 pts > +15 implausible vs market (FD 12.5, consensus 12.5; possible role change the history-based sim cannot see) -)
- Dyami Brown Receptions Under 1.5: Phase 4 MISSING (no ESPN WR/CB cheatsheet mapping for Dyami Brown; no stand-in allowed); Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player)
- Chig Okonkwo Rec Yds Under 32.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 15.1% / zone 72.8%, MOF closed 49.1% / open 43.4%; no stand-in allowed); Phase 14 FAIL (edge +2.3 < +3; a model median does not clear the line)
- Chig Okonkwo Receptions Over 3.5: Phase 2 FAIL (5+ tgt in <3 of last 4); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 15.1% / zone 72.8%, MOF closed 49.1% / open 43.4%; no stand-in allowed); Phase 14 FAIL (model p 0.441 < .45; a model median does not clear the line)

## 6. Risks and checks still to come
- 08:25 refresh (run 08:36 ET): tools/sim_v6.py (calibrated bias model; BUG-2026-11-01-BIAS fixed; tools/tests 35/35 OK at 08:36) replaced sim_v5.py for this re-score, 100,000 sims x 3 models, seed 20261101; v5 numbers kept in run_manifest.json `sims_v5`. Odds re-pulled 08:36 ET via The Odds API (pull_odds.py/pull_lines.py, odds_r0835.csv / lines_r0835.json); the 08:36 odds go stale at 09:36 ET. PFF props csv (captured 07:40 ET) is a pick-side cross-check only and was moved from `sources` to `cross_checks` because it is over 1 h old. PFR per-defender cache pfr_def_adv_2026.html exception still applies (Rico, valid 2026-11-01 only). Pre-refresh files saved as *.pre0825.*.
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. No PFF row matches a live leg in this folder.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 6:50 PM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 4 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).

## 08:25 ET refresh — re-priced 08:36 ET, re-scored on sim_v6 (v5 shown side by side)

All lines unchanged vs the vetted run. Spreads unchanged; FD totals moved KC@DEN 40.5→41.5 and LV@NYJ 45.5→46.5 (sims use spread, not total).

| Leg | 07:30-07:44 price / no-vig | 08:36 price / no-vig | v5 gate edge / shrunk | v5 MC+GR edge | v6 p MC/Bias/GR | v6 medians | v6 gate edge / shrunk | PFF side | Status |
|---|---|---|---|---|---|---|---|---|---|
| Stefon Diggs Rec Yds Over 42.5 | -113 / 0.500 | -113 / 0.500 (FD main) | +8.6 / +6.0 | +12.5 | 0.612/0.610/0.600 | 50.2544/48.9981/49.9423 | +10.7 / +7.5 | no csv row; per Ghost6 PFF leans UNDER 42.5 at 53.7% on 5.6 targets - CONFLICT | PASS |
