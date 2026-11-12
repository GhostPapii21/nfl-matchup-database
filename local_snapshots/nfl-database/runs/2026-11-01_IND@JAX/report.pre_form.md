GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_IND@JAX  checked_at=2026-11-01 07:36 ET
Live legs: none
Cut legs: ['Bhayshul Tuten Rush Yds Over 59.5', 'Bhayshul Tuten Rush+Rec Yds Over 83.5', 'Brenton Strange Rec Yds Under 41.5', 'Brenton Strange Receptions Over 2.5', 'Daniel Jones Pass Yds Over 192.5', 'Jonathan Taylor Rush Yds Over 50.5', 'Jonathan Taylor Rush+Rec Yds Over 70.5', 'Josh Downs Rec Yds Over 32.5', 'Josh Downs Receptions Over 3.5', 'Keenan Allen Rec Yds Over 35.5', 'Keenan Allen Receptions Over 4.5', 'Parker Washington Rec Yds Over 59.5', 'Parker Washington Receptions Under 4.5', 'Trevor Lawrence Pass Yds Under 237.5', 'Tyler Warren Rec Yds Over 39.5', 'Tyler Warren Receptions Over 4.5']

# IND @ JAX — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## Vetting amendments (2026-11-01 07:34 ET)
- Cut, under on primary star (Ghost6 rule): none. Pass count 0 -> 0.
- NGS source relabelled BACKUP with data date (see Risks).

## Vetting amendment 2 (2026-11-01 07:36 ET)
- Edge now scored on MC+GR average (bias model excluded pending fix). Cut this pass: none.
- Live legs now: none

## 1. Header
- Game: IND @ JAX, game ID 401873028, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_IND@JAX/checklist.md
- Candidate legs: 16 (key players × FD main market); passed 0, cut 16.

## 2. Phases run
- 1 Data pull: PASS 16
- 2 Opportunity: FAIL 5, PASS 11
- 3 Defense profile: FAIL 1, PASS 15
- 4 Defender coverage: FAIL 1, N/A 2, PASS 5, UNVERIFIED 8
- 5 Pressure/blitz/checkdown: N/A 2, PASS 14
- 6 QB card: FAIL 9, PASS 7
- 7 Role: FAIL 4, PASS 12
- 8 Injuries: PASS 16
- 9 NGS: PASS 16
- 10 Film: PASS 14, UNVERIFIED 2
- 11 Environment: FAIL 5, PASS 11
- 12 Source audit: PASS 16
- 13 Game script 10G: FAIL 10, PASS 6
- 14 Models/price/edge: FAIL 10, PASS 4, UNVERIFIED 2
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
| Daniel Jones Pass Yds Over 192.5 | 0.676 / 223.6 | 0.470 / 188.2 | 0.657 / 221.4 |
| Jonathan Taylor Rush Yds Over 50.5 | 0.660 / 59.5 | 0.533 / 52.1 | 0.629 / 58.7 |
| Jonathan Taylor Rush+Rec Yds Over 70.5 | 0.627 / 79.4 | 0.472 / 68.6 | 0.605 / 78.9 |
| Josh Downs Rec Yds Over 32.5 | 0.639 / 43.8 | 0.558 / 37.2 | 0.592 / 41.5 |
| Josh Downs Receptions Over 3.5 | 0.485 / 3.0 | 0.407 / 3.0 | 0.456 / 3.0 |
| Keenan Allen Rec Yds Over 35.5 | 0.751 / 56.7 | 0.662 / 47.4 | 0.725 / 55.3 |
| Keenan Allen Receptions Over 4.5 | 0.553 / 5.0 | 0.458 / 4.0 | 0.533 / 5.0 |
| Tyler Warren Rec Yds Over 39.5 | 0.562 / 43.0 | 0.448 / 36.7 | 0.541 / 41.9 |
| Tyler Warren Receptions Over 4.5 | 0.704 / 6.0 | 0.606 / 5.0 | 0.650 / 6.0 |
| Trevor Lawrence Pass Yds Under 237.5 | 0.454 / 247.0 | 0.655 / 207.9 | 0.465 / 245.0 |
| Bhayshul Tuten Rush Yds Over 59.5 | 0.718 / 74.5 | 0.590 / 65.4 | 0.690 / 74.5 |
| Bhayshul Tuten Rush+Rec Yds Over 83.5 | 0.640 / 95.3 | 0.491 / 82.8 | 0.629 / 95.5 |
| Parker Washington Rec Yds Over 59.5 | 0.479 / 56.9 | 0.374 / 47.8 | 0.462 / 55.0 |
| Parker Washington Receptions Under 4.5 | 0.587 / 4.0 | 0.664 / 3.0 | 0.602 / 4.0 |
| Brenton Strange Rec Yds Under 41.5 | 0.451 / 44.7 | 0.560 / 37.2 | 0.495 / 41.9 |
| Brenton Strange Receptions Over 2.5 | 0.850 / 5.0 | 0.783 / 4.0 | 0.756 / 4.0 |

## 5. Projections and picks
**No card.** No leg passed every phase for this game.

### Cut legs
- Daniel Jones Pass Yds Over 192.5: Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 11 FAIL (sustained wind 15+ mph: cut passing/receiving yardage overs); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Jonathan Taylor Rush Yds Over 50.5: Phase 3 FAIL (RB YPC allowed <=3.8 suppression); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (rush-only over on possible trailer needs 4+ tgt/g)
- Jonathan Taylor Rush+Rec Yds Over 70.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 21.0% / zone 73.4%, MOF closed 46.0% / open 51.1%; awaiting ruling); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Josh Downs Rec Yds Over 32.5: Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 11 FAIL (sustained wind 15+ mph: cut passing/receiving yardage overs); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Josh Downs Receptions Over 3.5: Phase 2 FAIL (5+ tgt in <3 of last 4; proj rec 3.4 < 3.5); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Keenan Allen Rec Yds Over 35.5: Phase 2 FAIL (not 4+ tgt in each of last 3); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (snap share <60% in last 2)
- Keenan Allen Receptions Over 4.5: Phase 4 FAIL (rec over vs 54.8% cmp allowed, volume margin +14% < 20%); Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (snap share <60% in last 2)
- Tyler Warren Rec Yds Over 39.5: Phase 2 FAIL (not top-2 target earner (#5)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 21.0% / zone 73.4%, MOF closed 46.0% / open 51.1%; no stand-in allowed); Phase 6 FAIL (clutch D/F: no trailing-script overs)
- Tyler Warren Receptions Over 4.5: Phase 2 FAIL (not top-2 target earner (#5)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 21.0% / zone 73.4%, MOF closed 46.0% / open 51.1%; no stand-in allowed); Phase 6 FAIL (clutch D/F: no trailing-script overs)
- Trevor Lawrence Pass Yds Under 237.5: Phase 14 FAIL (edge +2.5 < +3; a model median does not clear the line)
- Bhayshul Tuten Rush Yds Over 59.5: Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4)
- Bhayshul Tuten Rush+Rec Yds Over 83.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 26.2% / zone 66.5%, MOF closed 50.2% / open 44.7%; awaiting ruling); Phase 13 FAIL (margin 8.5+: lower alt rung required but none available); Phase 14 FAIL (a model median does not clear the line)
- Parker Washington Rec Yds Over 59.5: Phase 2 FAIL (not 4+ tgt in each of last 3); Phase 4 UNVERIFIED (defender sample 2 tgt < 8: too thin to grade); Phase 11 FAIL (sustained wind 15+ mph: cut passing/receiving yardage overs)
- Parker Washington Receptions Under 4.5: Phase 4 UNVERIFIED (defender sample 2 tgt < 8: too thin to grade); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +16.0 pts > +15 implausible vs market (FD 4.5, consensus 4.5; possible role change the history-based sim cannot see) -> )
- Brenton Strange Rec Yds Under 41.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 26.2% / zone 66.5%, MOF closed 50.2% / open 44.7%; no stand-in allowed); Phase 14 FAIL (edge +0.2 < +3; a model median does not clear the line)
- Brenton Strange Receptions Over 2.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 26.2% / zone 66.5%, MOF closed 50.2% / open 44.7%; no stand-in allowed); Phase 14 FAIL (shrunk edge -4.7 not > 0)

## 6. Risks and checks still to come
- Bias model excluded pending fix (BUGLOG BUG-2026-11-01-BIAS): flat haircuts vol x0.92/catch x0.97/yds x0.95 in sim_v5.py skew medians ~-16% vs line. Edge decision now uses the MC+GR average; bias p/median are still recorded and the gate still requires every model p >= .45 and median clearing the line (gate not loosened).
- PFF props cross-check (week8/lines/pff_props_2026-11-01.csv, captured 07:40 ET, page header 7:08am EST): shows PFF pick side only and the book is unknown (logo only); used as cross-check, never as no-vig. No PFF row matches a live leg in this folder.
- NGS from nflverse published copy (BACKUP, data through 2026-10-29 (2026 Week 8 TNF)), accepted by Ghost6 for Nov 1 only.
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 2 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
