```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-01_MIN@DET  checked_at=2026-11-01 07:31 ET
Live legs: ['Jameson Williams Rec Yds Under 51.5', 'Jordan Addison Receptions Under 3.5']
Cut legs: ['Aaron Jones Rush Yds Over 29.5', 'Aaron Jones Rush+Rec Yds Over 43.5', 'Amon-Ra St. Brown Rec Yds Under 77.5', 'Amon-Ra St. Brown Receptions Under 6.5', 'Jahmyr Gibbs Rush Yds Over 87.5', 'Jahmyr Gibbs Rush+Rec Yds Over 121.5', 'Jameson Williams Receptions Over 3.5', 'Jared Goff Pass Yds Under 259.5', 'Jordan Addison Rec Yds Over 37.5', 'Jordan Mason Rush Yds Over 49.5', 'Justin Jefferson Rec Yds Under 75.5', 'Justin Jefferson Receptions Under 5.5', 'Kyler Murray Pass Yds Under 224.5', 'Sam LaPorta Rec Yds Under 45.5', 'Sam LaPorta Receptions Under 4.5', 'T.J. Hockenson Rec Yds Under 40.5', 'T.J. Hockenson Receptions Under 4.5']
APPROVED EXCEPTIONS:
  - leg Jameson Williams Rec Yds Under 51.5 defender Isaiah Rodgers: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
  - leg Jordan Addison Receptions Under 3.5 defender D.J. Reed: coverage.defenders from /workspace/nfl-sim/mnf12/pfr_def_adv_2026.html (staleness waived; approved by Rico on 2026-11-01, valid 2026-11-01, scope receiving legs) — misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only
Notes:
  - Jameson Williams Rec Yds Under 51.5: avg p 0.571, no-vig 0.500, edge +7.1, shrunk +5.0
  - Jordan Addison Receptions Under 3.5: avg p 0.689, no-vig 0.575, edge +11.4, shrunk +5.7
```

# MIN @ DET — Week 8 game-script run (Sunday Nov 1, 2026)

**For Ghost6 vetting only — not for Rico until VETTED.**

## 1. Header
- Game: MIN @ DET, game ID 401873030, kickoff 01:00 PM ET.
- Data pulled 07:09–07:30 ET Nov 1 (odds 07:30 ET, spreads 07:30 ET). pbp through Oct 29 (Week 8 TNF).
- Checklist: /workspace/nfl-database/runs/2026-11-01_MIN@DET/checklist.md
- Candidate legs: 19 (key players × FD main market); passed 2, cut 17.

## 2. Phases run
- 1 Data pull: FAIL 1, PASS 18
- 2 Opportunity: FAIL 3, PASS 16
- 3 Defense profile: FAIL 3, PASS 16
- 4 Defender coverage: FAIL 1, MISSING 2, N/A 3, PASS 7, UNVERIFIED 6
- 5 Pressure/blitz/checkdown: FAIL 2, N/A 3, PASS 12, UNVERIFIED 2
- 6 QB card: PASS 19
- 7 Role: FAIL 2, PASS 17
- 8 Injuries: PASS 19
- 9 NGS: PASS 19
- 10 Film: PASS 17, UNVERIFIED 2
- 11 Environment: PASS 19
- 12 Source audit: PASS 19
- 13 Game script 10G: FAIL 4, PASS 15
- 14 Models/price/edge: FAIL 7, PASS 6, UNVERIFIED 6
- 15 Inactives: PASS 19
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
| Kyler Murray Pass Yds Under 224.5 | 0.684 / 176.4 | 0.790 / 148.4 | 0.680 / 188.1 |
| Jordan Mason Rush Yds Over 49.5 | 0.650 / 58.4 | 0.524 / 50.8 | 0.640 / 58.4 |
| Aaron Jones Rush Yds Over 29.5 | 0.926 / 68.0 | 0.874 / 59.0 | 0.879 / 69.0 |
| Aaron Jones Rush+Rec Yds Over 43.5 | 0.889 / 81.8 | 0.813 / 70.2 | 0.849 / 82.7 |
| Justin Jefferson Rec Yds Under 75.5 | 0.742 / 51.9 | 0.825 / 43.7 | 0.721 / 47.9 |
| Justin Jefferson Receptions Under 5.5 | 0.713 / 4.0 | 0.783 / 4.0 | 0.689 / 4.0 |
| Jordan Addison Rec Yds Over 37.5 | 0.440 / 32.6 | 0.353 / 26.5 | 0.429 / 30.7 |
| Jordan Addison Receptions Under 3.5 | 0.670 / 3.0 | 0.729 / 2.0 | 0.668 / 2.0 |
| T.J. Hockenson Rec Yds Under 40.5 | 0.509 / 40.1 | 0.595 / 32.8 | 0.509 / 40.1 |
| T.J. Hockenson Receptions Under 4.5 | 0.536 / 4.0 | 0.604 / 4.0 | 0.532 / 4.0 |
| Jared Goff Pass Yds Under 259.5 | 0.474 / 265.1 | 0.679 / 223.9 | 0.479 / 264.1 |
| Jahmyr Gibbs Rush Yds Over 87.5 | 0.605 / 96.5 | 0.461 / 84.4 | 0.555 / 93.7 |
| Jahmyr Gibbs Rush+Rec Yds Over 121.5 | 0.592 / 130.9 | 0.414 / 113.2 | 0.555 / 127.9 |
| Amon-Ra St. Brown Rec Yds Under 77.5 | 0.459 / 82.1 | 0.587 / 69.1 | 0.475 / 80.0 |
| Amon-Ra St. Brown Receptions Under 6.5 | 0.410 / 7.0 | 0.529 / 6.0 | 0.444 / 7.0 |
| Jameson Williams Rec Yds Under 51.5 | 0.530 / 48.5 | 0.631 / 41.0 | 0.552 / 45.8 |
| Jameson Williams Receptions Over 3.5 | 0.528 / 4.0 | 0.442 / 3.0 | 0.488 / 3.0 |
| Sam LaPorta Rec Yds Under 45.5 | 0.556 / 39.9 | 0.641 / 33.1 | 0.558 / 39.9 |
| Sam LaPorta Receptions Under 4.5 | 0.655 / 3.0 | 0.717 / 3.0 | 0.657 / 3.0 |

## 5. Projections and picks
- **Jordan Addison Receptions Under 3.5 @ -160 (FanDuel)**: projection MC mean 2.9, median 3.0. No-vig 0.575; avg p 0.689; edge +11.4 pts before shrink, +5.7 after. FD main.
  - Opportunity: rank 4 by tgt last3 (pbp [9, 6, 3]; ESPN box [9, 6, 3]); proj 32.7 pa x 0.180 = 5.9 tgt x cr 0.54 = 3.2 rec; MC mean 2.9 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Jordan Addison (R: L35/S32/R33%) vs D.J. Reed | PFR D.J. Reed: 23 tgt, 65.2% cmp, 12.5 YPT, rtg 137.4 | man 18.2% / zone 76.4%, MOF closed 47.6% / open 49.0% | volume margin -10%
  - Script: MIN +3.5 (underdog); total 46.5; FD main
- **Jameson Williams Rec Yds Under 51.5 @ -113 (FanDuel)**: projection MC mean 53.9, median 48.5. No-vig 0.500; avg p 0.571; edge +7.1 pts before shrink, +5.0 after. FD main.
  - Opportunity: rank 2 by tgt last3 (pbp [8, 4, 9]; ESPN box [8, 4, 9]); proj 39.1 pa x 0.176 = 6.9 tgt x cr 0.58 = 4.0 rec; MC mean 53.9 (under: volume recorded)
  - Matchup/coverage: cheatsheet: Jameson Williams (R: L35/S22/R42%) vs Isaiah Rodgers | PFR Isaiah Rodgers: 19 tgt, 36.8% cmp, 6.1 YPT, rtg 36.1 | man 5.3% / zone 86.5%, MOF closed 31.6% / open 61.2% | volume margin +5%
  - Script: DET -3.5 (moderate favorite); total 46.5; FD main

### Cut legs
- Kyler Murray Pass Yds Under 224.5: Phase 3 FAIL (under vs top-8 pass yds allowed (rank 1)); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 176.4 vs FD main 224.5 / book consensus 224.8 (>=12 yds) -> Debugging)
- Jordan Mason Rush Yds Over 49.5: Phase 1 FAIL (2 games; last3 09-13 0t/0r/0y/15c/59ry, 10-25 2t/0r/0y/15c/68ry); Phase 2 FAIL (not primary back or proj < line); Phase 7 FAIL (rush over needs 60%+ carry share in 3 of last 4; rush-only over on possible trailer needs 4+ tgt/g)
- Aaron Jones Rush Yds Over 29.5: Phase 7 FAIL (rush-only over on possible trailer needs 4+ tgt/g); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception)); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 68.0 vs FD main 29.5 / book consensus 29.5 (>=12 yds) -> Debugging)
- Aaron Jones Rush+Rec Yds Over 43.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 18.2% / zone 76.4%, MOF closed 47.6% / open 49.0%; awaiting ruling); Phase 5 UNVERIFIED (Panthers rule CAUTION: user decides); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- Justin Jefferson Rec Yds Under 75.5: Phase 4 MISSING (defender not in PFR cache); Phase 14 UNVERIFIED (MODEL-SUSPECT: MC median 51.9 vs FD main 75.5 / book consensus 75.5 (>=12 yds) -> Debugging)
- Justin Jefferson Receptions Under 5.5: Phase 4 MISSING (defender not in PFR cache); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +30.0 pts > +15 implausible vs market (FD 5.5, consensus 5.8; possible role change the history-based sim cannot see) -> )
- Jordan Addison Rec Yds Over 37.5: Phase 2 FAIL (not top-2 target earner (#4); not 4+ tgt in each of last 3); Phase 5 UNVERIFIED (Panthers rule CAUTION: user decides); Phase 13 FAIL (10G: underdog over BLOCKED (no written trap/elimination exception))
- T.J. Hockenson Rec Yds Under 40.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 18.2% / zone 76.4%, MOF closed 47.6% / open 49.0%; no stand-in allowed)
- T.J. Hockenson Receptions Under 4.5: Phase 3 FAIL (under vs soft TE D (YPT>=8.0)); Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 18.2% / zone 76.4%, MOF closed 47.6% / open 49.0%; no stand-in allowed)
- Jared Goff Pass Yds Under 259.5: Phase 14 FAIL (a model median does not clear the line)
- Jahmyr Gibbs Rush Yds Over 87.5: Phase 14 FAIL (a model median does not clear the line)
- Jahmyr Gibbs Rush+Rec Yds Over 121.5: Phase 4 UNVERIFIED (RB receiving defender mapping: no LB/S alignment source; man 5.3% / zone 86.5%, MOF closed 31.6% / open 61.2%; awaiting ruling); Phase 5 FAIL (top-10 blitz D and player blitzed share drops >4 pts); Phase 14 FAIL (edge +2.5 < +3; model p 0.414 < .45; a model median does not clear the line)
- Amon-Ra St. Brown Rec Yds Under 77.5: Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 14 FAIL (placed-ticket bar: UD20 o49.5; Ticket 2 60+; edge +0.7 < +3; a model median does not clear the line)
- Amon-Ra St. Brown Receptions Under 6.5: Phase 10 UNVERIFIED (no cited caption play re-matched a fresh pbp row for this player); Phase 14 FAIL (placed-ticket bar: PP40 o5.5; PP25 o7; edge +2.8 < +3; model p 0.410 < .45; a model median does not clear the line)
- Jameson Williams Receptions Over 3.5: Phase 2 FAIL (5+ tgt in <3 of last 4; same-role teammate >=28%: [('Amon-Ra St. Brown', 0.30493273542600896)]); Phase 4 FAIL (rec over vs 36.8% cmp allowed, volume margin +14% < 20%); Phase 5 FAIL (top-10 blitz D and player blitzed share drops >4 pts)
- Sam LaPorta Rec Yds Under 45.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 5.3% / zone 86.5%, MOF closed 31.6% / open 61.2%; no stand-in allowed)
- Sam LaPorta Receptions Under 4.5: Phase 4 UNVERIFIED (TE defender mapping not ruled (ISS-05); man 5.3% / zone 86.5%, MOF closed 31.6% / open 61.2%; no stand-in allowed); Phase 14 UNVERIFIED (MODEL-SUSPECT: edge +16.2 pts > +15 implausible vs market (FD 4.5, consensus 4.5; possible role change the history-based sim cannot see) -> )

## 6. Risks and checks still to come
- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.
- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.
- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.
- Inactives recheck at 11:30 AM ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.
- Questionable players among the candidates: none.
- UNVERIFIED film: 2 leg(s) had no re-matched film play (cut).
- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).
