```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_TEN@CIN  checked_at=2026-11-01 07:31 ET
Live legs: none
Cut legs: ['Cam Ward Pass Yds Under 192.5', 'Chase Brown Rush Yds Under 58.5', 'Chase Brown Rush+Rec Yds Under 81.5', "Ja'Marr Chase Rec Yds Under 79.5", "Ja'Marr Chase Receptions Under 6.5", 'Joe Burrow Pass Yds Over 249.5', 'Mike Gesicki Rec Yds Under 22.5', 'Mike Gesicki Receptions Under 2.5', 'Tee Higgins Rec Yds Over 69.5', 'Tee Higgins Receptions Over 4.5', 'Tony Pollard Rush Yds Over 65.5', 'Tony Pollard Rush+Rec Yds Under 84.5']
```

# TEN @ CIN — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## 1. Header
- Game: TEN @ CIN, game ID 401873031, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_TEN@CIN/checklist.md
- Candidate legs: 12 (key players × FD main market); passed 0, cut 12.

## 2. Phases run
- 1 Data pull: PASS 12
- 2 Opportunity: PASS 12
- 3 Defense profile: FAIL 3, PASS 9
- 4 Defender coverage: MISSING 2, N/A 2, PASS 4, UNVERIFIED 4
- 5 Pressure/blitz/checkdown: N/A 2, PASS 10
- 6 QB card: FAIL 1, PASS 11
- 7 Role: FAIL 1, PASS 11
- 8 Injuries: PASS 12
- 9 NGS: PASS 12
- 10 Film: PASS 12
- 11 Environment: PASS 12
- 12 Source audit: PASS 12
- 13 Game script 10G: FAIL 5, PASS 7
- 14 Models/price/edge: FAIL 5, PASS 3, UNVERIFIED 4
- 15 Inactives: PASS 12
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
| Cam Ward Pass Yds Under 192.5 | 0.547 / 184.7 | 0.734 / 156.1 | 0.560 / 182.5 |
| Tony Pollard Rush Yds Over 65.5 | 0.656 / 77.7 | 0.521 / 67.5 | 0.623 / 76.6 |
| Tony Pollard Rush+Rec Yds Under 84.5 | 0.465 / 87.7 | 0.597 / 76.0 | 0.487 / 86.1 |
| Joe Burrow Pass Yds Over 249.5 | 0.693 / 292.5 | 0.489 / 246.8 | 0.688 / 290.5 |
| Chase Brown Rush Yds Under 58.5 | 0.703 / 46.6 | 0.809 / 41.1 | 0.686 / 45.5 |
| Chase Brown Rush+Rec Yds Under 81.5 | 0.496 / 81.8 | 0.651 / 70.1 | 0.507 / 80.9 |
| Ja'Marr Chase Rec Yds Under 79.5 | 0.692 / 57.7 | 0.773 / 47.7 | 0.688 / 53.4 |
| Ja'Marr Chase Receptions Under 6.5 | 0.675 / 5.0 | 0.746 / 5.0 | 0.670 / 5.0 |
| Tee Higgins Rec Yds Over 69.5 | 0.618 / 84.8 | 0.506 / 69.8 | 0.617 / 83.9 |
| Tee Higgins Receptions Over 4.5 | 0.655 / 6.0 | 0.566 / 5.0 | 0.656 / 6.0 |
| Mike Gesicki Rec Yds Under 22.5 | 0.610 / 18.5 | 0.671 / 13.9 | 0.636 / 14.6 |
| Mike Gesicki Receptions Under 2.5 | 0.641 / 2.0 | 0.691 / 2.0 | 0.662 / 2.0 |

## 5. Projections and picks
**No card.** No leg passed every phase for this game.

### Cut legs
- Cam Ward Pass Yds Under 192.5: Phase 3 FAIL (under vs top-8 pass yds allowed (rank 7)); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED)
- Tony Pollard Rush Yds Over 65.5: Phase 6 FAIL (clutch D/F: no trailing-script overs); Phase 7 FAIL (rush-only over on possible trailer needs 4+ tgt/g); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Tony Pollard Rush+Rec Yds Under 84.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 26.6% / zone 65.3%, MOF closed 51.3% / open 43.1%; awaiting ruling); Phase 13 FAIL (trailing-team passing/receiving under BLOCKED; underdog leg BLOCKED (10G)); Phase 14 FAIL (edge +2.0 < +3; a model median does not clear the line)
- Joe Burrow Pass Yds Over 249.5: Phase 14 FAIL (edge -1.0 < +3; shrunk edge -4.7 not > 0; a model median does not clear the line; MODEL-SUSPECT: MC median 292.5 vs FD main 272.5 / book con)
- Chase Brown Rush Yds Under 58.5: Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 46.6 vs FD main 58.5 / book consensus 58.8 (>=12 yds) -> Debugging)
- Chase Brown Rush+Rec Yds Under 81.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 16.5% / zone 77.2%, MOF closed 45.6% / open 51.2%; awaiting ruling); Phase 13 FAIL (6.5+ favorite rush under vs clock-killing script); Phase 14 FAIL (a model median does not clear the line)
- Ja'Marr Chase Rec Yds Under 79.5: Phase 3 FAIL (under vs soft WR D (YPT>=9.0)); Phase 4 MISSING (defender not in PFR cache); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 57.7 vs FD main 79.5 / book consensus 79.8 (>=12 yds) -> Debugging)
- Ja'Marr Chase Receptions Under 6.5: Phase 3 FAIL (under vs soft WR D (YPT>=9.0)); Phase 4 MISSING (defender not in PFR cache); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +22.5 pts > +15 implausible vs market (FD 6.5, consensus 6.5; possible role change the history-based sim cannot see) -> )
- Tee Higgins Rec Yds Over 69.5: Phase 14 FAIL (placed-ticket bar: PP20 Higgins o68.5 rec yds; $51.50 SGP Higgins 50+ yds; MODEL-SUSPECT: MC median 84.8 vs FD main 70.5 / book consensus 70)
- Tee Higgins Receptions Over 4.5: Phase 14 FAIL (placed-ticket bar: PP40 Fantasy/PP20 rec yds/$51.50 SGP Higgins 50+ yds/FD 7-leg 4+ rec)
- Mike Gesicki Rec Yds Under 22.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 16.5% / zone 77.2%, MOF closed 45.6% / open 51.2%; no stand-in allowed)
- Mike Gesicki Receptions Under 2.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 16.5% / zone 77.2%, MOF closed 45.6% / open 51.2%; no stand-in allowed)

## 6. Risks and checks still to come
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 0 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
