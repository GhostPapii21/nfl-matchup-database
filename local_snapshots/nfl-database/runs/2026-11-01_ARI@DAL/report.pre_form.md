GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_ARI@DAL  checked_at=2026-11-01 07:36 ET
Live legs: none
Cut legs: ['Bam Knight Rush Yds Over 19.5', 'CeeDee Lamb Rec Yds Over 80.5', 'CeeDee Lamb Receptions Over 6.5', 'Dak Prescott Pass Yds Under 271.5', 'George Pickens Rec Yds Over 59.5', 'George Pickens Receptions Over 3.5', 'Jacoby Brissett Pass Yds Under 258.5', 'Jake Ferguson Rec Yds Over 14.5', 'Jake Ferguson Receptions Over 1.5', 'Javonte Williams Rush Yds Under 76.5', 'Javonte Williams Rush+Rec Yds Under 92.5', 'Michael Wilson Rec Yds Under 56.5', 'Michael Wilson Receptions Under 4.5', 'Ryan Flournoy Rec Yds Over 36.5', 'Ryan Flournoy Receptions Over 3.5', 'Trey McBride Rec Yds Under 71.5', 'Trey McBride Receptions Over 7.5', 'Tyler Allgeier Rush Yds Over 13.5']

# ARI @ DAL — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): none. Pass count 0 -> 0.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: none.
- Live legs now: none

## 1. Header
- Game: ARI @ DAL, game ID 401873024, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_ARI@DAL/checklist.md
- Candidate legs: 18 (key players × FD main market); passed 0, cut 18.

## 2. Phases run
- 1 Data pull: PASS 18
- 2 Opportunity: FAIL 6, PASS 12
- 3 Defense profile: PASS 18
- 4 Defender coverage: MISSING 2, N/A 3, PASS 6, UNVERIFIED 7
- 5 Pressure/blitz/checkdown: N/A 3, PASS 15
- 6 QB card: FAIL 3, PASS 15
- 7 Role: FAIL 4, PASS 14
- 8 Injuries: PASS 18
- 9 NGS: PASS 18
- 10 Film: PASS 15, UNVERIFIED 3
- 11 Environment: PASS 18
- 12 Source audit: PASS 18
- 13 Game script 10G: FAIL 9, PASS 9
- 14 Models/price/edge: FAIL 10, PASS 7, UNVERIFIED 1
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
| Jacoby Brissett Pass Yds Under 258.5 | 0.484 / 260.7 | 0.706 / 220.6 | 0.506 / 256.3 |
| Tyler Allgeier Rush Yds Over 13.5 | 0.763 / 30.3 | 0.715 / 26.1 | 0.771 / 31.8 |
| Bam Knight Rush Yds Over 19.5 | 0.567 / 25.3 | 0.507 / 20.2 | 0.587 / 26.1 |
| Michael Wilson Rec Yds Under 56.5 | 0.535 / 53.4 | 0.648 / 44.1 | 0.552 / 51.1 |
| Michael Wilson Receptions Under 4.5 | 0.485 / 5.0 | 0.569 / 4.0 | 0.509 / 4.0 |
| Trey McBride Rec Yds Under 71.5 | 0.542 / 68.1 | 0.677 / 57.9 | 0.556 / 66.1 |
| Trey McBride Receptions Over 7.5 | 0.632 / 8.0 | 0.508 / 8.0 | 0.571 / 8.0 |
| Dak Prescott Pass Yds Under 271.5 | 0.427 / 287.3 | 0.630 / 243.6 | 0.446 / 284.0 |
| Javonte Williams Rush Yds Under 76.5 | 0.566 / 70.4 | 0.683 / 61.7 | 0.593 / 67.1 |
| Javonte Williams Rush+Rec Yds Under 92.5 | 0.571 / 85.8 | 0.699 / 73.7 | 0.589 / 82.5 |
| CeeDee Lamb Rec Yds Over 80.5 | 0.562 / 90.0 | 0.457 / 75.1 | 0.550 / 88.9 |
| CeeDee Lamb Receptions Over 6.5 | 0.538 / 7.0 | 0.449 / 6.0 | 0.521 / 7.0 |
| George Pickens Rec Yds Over 59.5 | 0.621 / 71.7 | 0.511 / 61.0 | 0.581 / 69.6 |
| George Pickens Receptions Over 3.5 | 0.775 / 5.0 | 0.693 / 5.0 | 0.709 / 5.0 |
| Ryan Flournoy Rec Yds Over 36.5 | 0.563 / 41.8 | 0.471 / 34.2 | 0.541 / 40.7 |
| Ryan Flournoy Receptions Over 3.5 | 0.512 / 4.0 | 0.427 / 3.0 | 0.482 / 3.0 |
| Jake Ferguson Rec Yds Over 14.5 | 0.615 / 18.6 | 0.540 / 15.2 | 0.565 / 17.3 |
| Jake Ferguson Receptions Over 1.5 | 0.691 / 2.0 | 0.629 / 2.0 | 0.614 / 2.0 |

## 5. Projections and picks
**No card.** No leg passed every phase for this game.

### Cut legs
- Jacoby Brissett Pass Yds Under 258.5: Phase 13 FAIL (trailing-team passing/receiving under BLOCKED); Phase 14 FAIL (a model median does not clear the line)
- Tyler Allgeier Rush Yds Over 13.5: Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4; rush-only over on possible trailer needs 4+ tgt/g); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Bam Knight Rush Yds Over 19.5: Phase 2 FAIL (not primary back or proj < line); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4; rush-only over on possible trailer needs 4+ tgt/g)
- Michael Wilson Rec Yds Under 56.5: Phase 4 MISSING (defender not in PFR cache); Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED)
- Michael Wilson Receptions Under 4.5: Phase 4 MISSING (defender not in PFR cache); Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED)
- Trey McBride Rec Yds Under 71.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 21.3% / zone 69.9%, MOF closed 60.2% / open 35.7%; no stand-in allowed); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED)
- Trey McBride Receptions Over 7.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 21.3% / zone 69.9%, MOF closed 60.2% / open 35.7%; no stand-in allowed); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Dak Prescott Pass Yds Under 271.5: Phase 14 FAIL (edge +0.1 < +3; model p 0.427 < .45; a model median does not clear the line; MODEL-SUSPECT: MC median 287.3 vs FD main 271.5 / book consensu)
- Javonte Williams Rush Yds Under 76.5: Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script)
- Javonte Williams Rush+Rec Yds Under 92.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 9.1% / zone 70.9%, MOF closed 21.9% / open 56.7%; awaiting ruling); Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script)
- CeeDee Lamb Rec Yds Over 80.5: Phase 14 FAIL (placed-ticket bar: Ticket 2 Lamb 60+ yds; FD 7-leg Lamb 50+; edge +2.3 < +3; a model median does not clear the line)
- CeeDee Lamb Receptions Over 6.5: Phase 14 FAIL (placed-ticket bar: PP40/PP20/UD20 Lamb o4.5 rec; PP25 o6.5; edge +2.2 < +3; model p 0.449 < .45; a model median does not clear the line)
- George Pickens Rec Yds Over 59.5: Phase 14 FAIL (edge +0.9 < +3; shrunk edge -1.3 not > 0)
- George Pickens Receptions Over 3.5: Phase 2 FAIL (same-role teammate >=28%: [('CeeDee Lamb', 0.2967032967032967)]); Phase 14 FAIL (placed-ticket bar: Ticket 2 Pickens 4+; $51.50 SGP 4.5+; shrunk edge -1.0 not > 0)
- Ryan Flournoy Rec Yds Over 36.5: Phase 2 FAIL (not top-2 target earner (#3)); Phase 4 UNVERIFIED (defender sample 6 tgt < 8: too thin to grade); Phase 14 FAIL (edge +2.5 < +3; a model median does not clear the line)
- Ryan Flournoy Receptions Over 3.5: Phase 2 FAIL (not top-2 target earner (#3); 5+ tgt in <3 of last 4; same-role teammate >=28%: [('CeeDee Lamb', 0.2967032967032967)]; proj rec 3.5 < 3.5); Phase 4 UNVERIFIED (defender sample 6 tgt < 8: too thin to grade); Phase 14 FAIL (edge +1.9 < +3; model p 0.427 < .45; a model median does not clear the line)
- Jake Ferguson Rec Yds Over 14.5: Phase 2 FAIL (not top-2 target earner (#4); not 4+ tgt in each of last 3); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 9.1% / zone 70.9%, MOF closed 21.9% / open 56.7%; no stand-in allowed); Phase 7 FAIL (snap share <60% in last 2)
- Jake Ferguson Receptions Over 1.5: Phase 2 FAIL (not top-2 target earner (#4); 5+ tgt in <3 of last 4); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 9.1% / zone 70.9%, MOF closed 21.9% / open 56.7%; no stand-in allowed); Phase 7 FAIL (snap share <60% in last 2)

## 6. Risks and checks still to come
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. No PFF row matches a live leg in this folder.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: George Pickens.
- UNVERIFIED film: 3 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
