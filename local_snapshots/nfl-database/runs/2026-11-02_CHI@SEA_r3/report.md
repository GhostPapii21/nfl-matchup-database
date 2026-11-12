## Gate output
```
GATE: PASS  run=/workspace/nfl-database/runs/2026-11-02_CHI@SEA_r3  checked_at=2026-11-02 16:48 ET
Live legs: none
Cut legs: ['AJ Barner Rec Yds Under 29.5', 'AJ Barner Receptions Under 3.5', 'Caleb Williams Pass Yds Over 224.5', 'Colston Loveland Rec Yds Under 42.5', 'Colston Loveland Receptions Under 4.5', 'Cooper Kupp Rec Yds Over 29.5', 'Cooper Kupp Receptions Over 2.5', "D'Andre Swift Rec Yds Over 21.5", "D'Andre Swift Receptions Over 2.5", "D'Andre Swift Receptions Over 3.5", "D'Andre Swift Rush Yds Under 59.5", "D'Andre Swift Rush+Rec Yds Under 86.5", 'Emanuel Wilson Rush Yds Over 19.5', 'Jaxon Smith-Njigba Rec Yds Over 109.5', 'Jaxon Smith-Njigba Rec Yds Over 89.5', 'Jaxon Smith-Njigba Rec Yds Over 99.5', 'Jaxon Smith-Njigba Receptions Over 7.5', 'Luther Burden III Rec Yds Under 52.5', 'Luther Burden III Receptions Under 4.5', 'Rome Odunze Rec Yds Under 38.5', 'Rome Odunze Receptions Under 3.5', 'Roschon Johnson Rush Yds Over 10.5', 'Sam Darnold Pass Yds Over 238.5']
SHARP coverage confirmed by StatRankings CoverageIQ team pages
```

# Projection report: MNF Chicago Bears @ Seattle Seahawks (r3, game-day 4:30 PM ET routine)

**Header.** Mon Nov 2 2026, Lumen Field (open air). Kickoff is 8:15 PM ET per ESPN (The Odds API lists 8:20 PM ET). ESPN calls this **Week 8**; the task called it Week 9. Week 8 is recorded. Price-sensitive data (FanDuel/DK/Pinnacle odds, ESPN injuries and news, NWS/Open-Meteo weather, nflverse pbp) was pulled at **4:38 PM ET**. Coverage was reused from 5:09 AM ET, PFR defenders from 5:10 and 6:40 AM ET, and NGS/FTN/snaps from 5:03 AM ET (all under 48h). Checklist: `checklist.md`. Manifest: `run_manifest.json`. Gate: `gate_output.txt`.

**Bottom line: no card. All 23 legs evaluated are CUT, and 0 are live. No MANUAL_REVIEW leg is open: JSN O89.5 met the press/manual-review numbers but is barred as a nested rung of the open JSN 70+ ticket.**

## 1. Phases run (counts over 23 legs)
- Phase 1 sample: FAIL 1, PASS 22
- Phase 2 opportunity: FAIL 3, PASS 20
- Phase 3 defense profile: FAIL 3, PASS 20
- Phase 4 defender: PASS 17, UNVERIFIED 6
- Phase 5 blitz/pressure: PASS 23
- Phase 6 QB: PASS 23
- Phase 7 role/snaps: FAIL 13, PASS 10
- Phase 8 injuries: FAIL 1, PASS 22
- Phase 9 NGS: PASS 23
- Phase 10 film: PASS 17, UNVERIFIED 6
- Phase 11 weather: PASS 23
- Phase 12 market/price: PASS 23
- Phase 13 game script: FAIL 6, PASS 17
- Phase 14 edge/sims: FAIL 13, PASS 10
- Phase 15 correlation/ticket bar: FAIL 10, PASS 13
Gaps: Phase 4 has 4 UNVERIFIED (ISS-05 has no TE defender data for Loveland/Barner; Kupp's slot CB Gordon has no PFR row). Phase 10 has 6 UNVERIFIED (Kupp, Barner, R. Johnson and Wilson have no caption cue matched to pbp). All of these are on CUT legs.

## 2. Sources used, by category
- **Core stats / pbp:** nflverse play_by_play_2026 (release 2:29 PM ET, through Nov 1 incl. Week 8 SNF; pulled 4:38 PM ET with curl). Gives §7 last-4 with current QB, targets and carries. Snap counts and depth charts are nflverse (5:03 AM ET).
- **Coverage / matchups:** Sharp Football coverage schemes plus StatRankings CoverageIQ as the agreeing second source (5:09 AM ET). SEA plays 90.0% zone / 5.4% man (SR 82.3/17.7) with MOF open 60.6%. CHI plays 29.9% man (SR 39.4%) with MOF closed 53.6%. PFR per-defender advanced defense: CHI 5:10 AM ET; SEA via Firecrawl 6:40 AM ET. FTN charting supplies blitz rates. ESPN WR/CB matchups name defenders (JSN vs Malik Muhammad, Kupp vs Kyler Gordon, Odunze vs Devon Witherspoon, Burden vs Nick Emmanwori).
- **NGS:** nflverse NGS receiving/passing/rushing (5:03 AM ET): separation, aDOT and time to throw (Williams 3.22 s, Darnold 3.00 s).
- **Film:** official NFL YouTube Week 6-7 highlights for CHI and SEA. Auto-captions came through yt-dlp at 4:42 PM ET; the earlier 429 has cleared. 11 plays were matched to pbp rows (see `src/film_matches.md`).
- **Injuries / news:** ESPN injuries API plus league/CHI/SEA news (4:38 PM ET). Official-source checks of the Loeb claims are below.
- **Weather:** tools/weather_forecast.py (NWS + Open-Meteo only), 4:38 PM ET: precip 2%, wind 2.7 mph, gust 3.4 mph, NWS "Cloudy". No flag.
- **Odds / props:** The Odds API via pull_odds.py, FanDuel/DK/Pinnacle pregame only (0 in-play rows dropped), 4:38 PM ET. FD: SEA -3.5 (-102), total 46.5, ML CHI +152 / SEA -180. No PFF was used for weather, script or projections. Outlier was not used.

## Loeb claims (official sources only)
- **Quenton Nelson to SEA:** VERIFIED: ESPN "Seahawks acquire Pro Bowl guard Quenton Nelson in trade with Colts" (Oct 27, 7:51 PM ET)
- **Jeffery Simmons to CHI:** VERIFIED: ESPN "Bears acquire All-Pro DT Jeffery Simmons in trade with Titans"; ESPN injury feed 16:38 ET shows Active
- **Montez Sweat back:** VERIFIED: ESPN injury feed (16:38 ET): reinstated Fri Oct 23 after a two-game suspension; ESPN Oct 28 "Montez Sweat returns to Bears"
- Impact: CHI pass rush gets stronger (Sweat back, plus Simmons in his first CHI game). Neither is in CHI's 22.3% PROXY pressure rate. SEA still has LT Charles Cross OUT; Nelson upgrades the interior, not LT. Pressure is a flag only, because the pressure/pass-rush cuts were not adopted (Rico, 5:01 AM ET).

## Reprice (FD 4:38 PM ET vs r2/Ghost6 morning)
| Market | Earlier | Now | Moved enough to re-run P14? |
|---|---|---|---|
| Williams pass yds | 227.5 | 224.5 | yes (re-run: edge +2.6, cut) |
| Burden rec yds | 51.5 | 52.5 | yes (re-run: §7 1/4, cut) |
| Swift receptions O3.5 | +140 | +112 (alt +108) | yes, 28 cents (re-run: edge +2.5, cut) |
| Swift rush+rec | 81.5 | 86.5 | yes (cut, 10G and §7 1/4) |
| JSN rec yds 99.5 | -113/-113 (alt -114) | -113/-113 | no |
| Roschon rush yds | 12.5 | 10.5 | yes (cut) |

## Zone check: Odunze and Moore
- **Rome Odunze:** SEA is the most zone-heavy defense (90% Sharp / 82.3% SR). Odunze averages 44.8 yds/g against zone-heavy defenses and 67.3 against man-heavier ones (small n). Separation 2.48, aDOT 13.6. In Caleb games he is CHI's WR3 (targets: Burden 24, Raymond 18, Odunze 16), so the WR3 over ban applies. SEA has no CBs out, so the depleted-secondary exception is N/A. Unders: rec yds U38.5 has edge +1.9 and §7 0/4; rec U3.5 has negative edge. Both are cut.
- **D.J. Moore:** he plays for BUF in 2026 (27 targets in nflverse pbp). No Moore is on CHI or SEA and no Moore prop exists for this game, so the check is N/A.

## 3. Simulations
tools/sim_v6.py (LIVE version). Monte Carlo, Bias and Game Randomness each ran **100,000 sims, seed 20261101**. The unit tests passed first (108 OK). Fit was rerun at 4:42 PM ET on new pbp; the calib multipliers are unchanged (the fit window is weeks 4-7). **BUG-2026-11-02-BIASDUP is still present: Bias = MC. The fix is STAGED in tools/sim_v6_fix/ for the 11:45 PM ET swap and was NOT swapped in by this run.** Only MC and GR are independent votes.

| Leg | FD price | no-vig | p MC / Bias / GR | median MC / Bias / GR | edge | shrunk |
|---|---|---|---|---|---|---|
| Caleb Williams Pass Yds Over 224.5 | -113 | 0.500 | 0.527 / 0.528 / 0.524 | 228.8 / 228.8 / 228.3 | +0.026 | +0.018 |
| Luther Burden III Rec Yds Under 52.5 | -113 | 0.500 | 0.553 / 0.551 / 0.560 | 48.6 / 48.6 / 47.0 | +0.055 | +0.038 |
| Luther Burden III Receptions Under 4.5 | -158 | 0.572 | 0.553 / 0.553 / 0.547 | 4.0 / 4.0 / 4.0 | -0.021 | -0.036 |
| Rome Odunze Rec Yds Under 38.5 | -113 | 0.500 | 0.516 / 0.519 / 0.521 | 37.4 / 37.4 / 37.3 | +0.019 | +0.013 |
| Rome Odunze Receptions Under 3.5 | -180 | 0.601 | 0.587 / 0.586 / 0.568 | 3.0 / 3.0 / 3.0 | -0.020 | -0.044 |
| Colston Loveland Rec Yds Under 42.5 | -113 | 0.500 | 0.699 / 0.699 / 0.679 | 30.1 / 30.1 / 28.9 | +0.193 | +0.135 |
| Colston Loveland Receptions Under 4.5 | -154 | 0.567 | 0.620 / 0.620 / 0.603 | 4.0 / 4.0 / 4.0 | +0.047 | +0.013 |
| D'Andre Swift Rush Yds Under 59.5 | -113 | 0.500 | 0.656 / 0.658 / 0.625 | 51.4 / 51.4 / 50.0 | +0.146 | +0.102 |
| D'Andre Swift Rush+Rec Yds Under 86.5 | -113 | 0.500 | 0.622 / 0.626 / 0.604 | 77.6 / 77.4 / 76.8 | +0.117 | +0.082 |
| D'Andre Swift Rec Yds Over 21.5 | -113 | 0.500 | 0.418 / 0.421 / 0.430 | 18.7 / 18.7 / 18.1 | -0.077 | -0.054 |
| D'Andre Swift Receptions Over 3.5 | +112 | 0.442 | 0.463 / 0.465 / 0.470 | 3.0 / 3.0 / 3.0 | +0.025 | +0.035 |
| D'Andre Swift Receptions Over 2.5 | -225 | 0.648 | 0.675 / 0.676 / 0.651 | 3.0 / 3.0 / 3.0 | +0.019 | -0.031 |
| Roschon Johnson Rush Yds Over 10.5 | -113 | 0.500 | 0.654 / 0.653 / 0.602 | 16.3 / 16.3 / 14.8 | +0.136 | +0.096 |
| Sam Darnold Pass Yds Over 238.5 | -113 | 0.500 | 0.523 / 0.521 / 0.570 | 247.3 / 246.1 / 259.7 | +0.038 | +0.027 |
| Jaxon Smith-Njigba Rec Yds Over 99.5 | -113 | 0.500 | 0.640 / 0.642 / 0.592 | 119.1 / 119.1 / 115.2 | +0.125 | +0.087 |
| Jaxon Smith-Njigba Rec Yds Over 89.5 | -166 | 0.588 | 0.711 / 0.715 / 0.647 | 119.1 / 119.1 / 115.2 | +0.103 | +0.046 |
| Jaxon Smith-Njigba Rec Yds Over 109.5 | +124 | 0.421 | 0.565 / 0.569 / 0.534 | 119.1 / 119.1 / 115.2 | +0.135 | +0.118 |
| Jaxon Smith-Njigba Receptions Over 7.5 | +106 | 0.454 | 0.562 / 0.563 / 0.525 | 8.0 / 8.0 / 8.0 | +0.096 | +0.081 |
| Cooper Kupp Rec Yds Over 29.5 | -113 | 0.500 | 0.498 / 0.502 / 0.515 | 29.5 / 30.6 / 30.0 | +0.005 | +0.004 |
| Cooper Kupp Receptions Over 2.5 | -160 | 0.575 | 0.468 / 0.470 / 0.479 | 2.0 / 2.0 / 2.0 | -0.103 | -0.095 |
| AJ Barner Rec Yds Under 29.5 | -113 | 0.500 | 0.587 / 0.587 / 0.588 | 24.8 / 24.8 / 21.9 | +0.088 | +0.061 |
| AJ Barner Receptions Under 3.5 | -168 | 0.586 | 0.687 / 0.690 / 0.676 | 3.0 / 2.0 / 2.0 | +0.098 | +0.043 |
| Emanuel Wilson Rush Yds Over 19.5 | -113 | 0.500 | 0.950 / 0.950 / 0.915 | 63.2 / 63.2 / 63.4 | +0.438 | +0.307 |

## 4. Projections and picks
**No leg passed, so there are no picks.**

Cut legs and the phase that cut them:
- **Caleb Williams Pass Yds Over 224.5** (-113): P13 10G underdog over BLOCKED (CHI +3.5); P14 edge +2.6 < +3. §7: [269.0, 138.0, 305.0, 308.0] with C.Williams.
- **Luther Burden III Rec Yds Under 52.5** (-113): §7 HARD: Williams-only form 1/4 unders (63,32,95,130). §7: [63.0, 32.0, 95.0, 130.0] with C.Williams. Note: line moved 51.5 -> 52.5; edge +5.5 alone not enough
- **Luther Burden III Receptions Under 4.5** (-158): P14 negative edge. §7: [5.0, 3.0, 8.0, 4.0] with C.Williams. Note: Burden 4+ open-ticket status ambiguous (r2/odunze 1:20 PM ET); under not nested in an over ticket but same player
- **Rome Odunze Rec Yds Under 38.5** (-113): P14 edge < +3; §7 0/4 unders. §7: [52.0, 43.0, 39.0, 69.0] with C.Williams. Note: zone check: SEA zone 90% (Sharp)/82.3% (SR). Odunze averages 44.8 yds/g vs zone-heavy teams, so zone does not suppress him
- **Rome Odunze Receptions Under 3.5** (-180): P14 negative edge. §7: [2.0, 3.0, 3.0, 4.0] with C.Williams.
- **Colston Loveland Rec Yds Under 42.5** (-113): §7 2/4; P4 ISS-05 TE defender UNVERIFIED; P13 could-trail TE under; P14 MODEL-SUSPECT (median 12+ below line). §7: [0.0, 3.0, 65.0, 69.0] with C.Williams.
- **Colston Loveland Receptions Under 4.5** (-154): §7 2/4 (0,1,6,7); P4 ISS-05. §7: [0.0, 1.0, 6.0, 7.0] with C.Williams.
- **D'Andre Swift Rush Yds Under 59.5** (-113): §7 HARD: Williams-only 2/4 (124,45,44,78); §11 one slip per player (open SGP). §7: [124.0, 45.0, 44.0, 78.0] with C.Williams. Note: edge is large but form fails
- **D'Andre Swift Rush+Rec Yds Under 86.5** (-113): P13 10G underdog rush+rec under BLOCKED; §7 1/4 (134,99,70,90); §11 one slip per player (open SGP). §7: [134.0, 99.0, 70.0, 90.0] with C.Williams.
- **D'Andre Swift Rec Yds Over 21.5** (-113): P13 10G underdog over; P14 model p < .45; §11 one slip per player (open SGP). §7: [10.0, 54.0, 26.0, 12.0] with C.Williams.
- **D'Andre Swift Receptions Over 3.5** (+112): P2 catches over needs 5+ tgt in 3 of L4 (1,5,5,4 = 2/4); P13 10G underdog over; P14 edge +2.5 < +3 and medians 3.0 do not clear 3.5; P15 open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung. §7: [1.0, 5.0, 4.0, 4.0] with C.Williams. Note: repriced +140 -> +112 (FD main), more than 20 cents; re-run through Phase 14 -> fails
- **D'Andre Swift Receptions Over 2.5** (-225): P14 shrunk edge -3.1; P15 open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung; P2 tgt. §7: [1.0, 5.0, 4.0, 4.0] with C.Williams.
- **Roschon Johnson Rush Yds Over 10.5** (-113): P3 SEA allows 3.40 YPC; P7 RB2 role; P13 underdog RB; P14 MODEL-SUSPECT (fixA boost); §7 only 2 games with carries. §7: [51.0, 13.0] with C.Williams.
- **Sam Darnold Pass Yds Over 238.5** (-113): P8 backup LT (Cross OUT) -> no QB yardage over; §7 2/4. §7: [168.0, 195.0, 278.0, 257.0] with S.Darnold.
- **Jaxon Smith-Njigba Rec Yds Over 99.5** (-113): §14 cushion FAIL at -113 (L4 median 118 < 124.4; 1.10x hit 2/4); P14 MODEL-SUSPECT (MC median 119.1, +19.6 vs line; press -> manual review); §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET). §7: [76.0, 102.0, 134.0, 150.0] with S.Darnold.
- **Jaxon Smith-Njigba Rec Yds Over 89.5** (-166): P14 MODEL-SUSPECT (press -> MANUAL_REVIEW on numbers alone); §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET). §7: [76.0, 102.0, 134.0, 150.0] with S.Darnold. Note: would be MANUAL_REVIEW (press) without the bar; the gate does not accept a MANUAL_REVIEW status for runs dated before 11-05, so status is CUT
- **Jaxon Smith-Njigba Rec Yds Over 109.5** (+124): §7 2/4 at 109.5; §11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET). §7: [76.0, 102.0, 134.0, 150.0] with S.Darnold.
- **Jaxon Smith-Njigba Receptions Over 7.5** (+106): §7 2/4 (5,5,12,9); §11 same player as open SGP (JSN 70+, JSN TD). §7: [5.0, 5.0, 12.0, 9.0] with S.Darnold.
- **Cooper Kupp Rec Yds Over 29.5** (-113): P14 no edge; §7 1/4. §7: [13.0, 15.0, 50.0, 20.0] with S.Darnold.
- **Cooper Kupp Receptions Over 2.5** (-160): P14 negative edge; §7 1/4. §7: [1.0, 2.0, 5.0, 2.0] with S.Darnold.
- **AJ Barner Rec Yds Under 29.5** (-113): P3 soft CHI TE D (TE YPT 8.61); P4 ISS-05. §7: [12.0, 20.0, 16.0, 42.0] with S.Darnold.
- **AJ Barner Receptions Under 3.5** (-168): P3; P4 ISS-05. §7: [1.0, 3.0, 3.0, 4.0] with S.Darnold.
- **Emanuel Wilson Rush Yds Over 19.5** (-113): P2/P7 role change: Charbonnet (no designation) + Price activated 4:05 PM ET -> 3-way committee; P14 MODEL-SUSPECT (sim p .95 on 63 median; no split data); §11 one slip per player (open SGP). §7: [81.0, 61.0, 52.0, 100.0] with S.Darnold. Note: §11: Wilson 15+ rush is on the open SGP
- No SEA RB leg: Charbonnet has 0 games in 2026 (sim can't price him; P1 MISSING), and J. Price was activated at 4:05 PM ET with no 2026 sample. Committee.

## Open-ticket bar (the task's rule: bar same player+stat or nested rung)
- Live SGP (Ghost6 bankroll_slips.md, 4:11 PM ET): JSN 70+ rec yds, JSN TD, Swift 50+ rush+rec, Swift TD, E. Wilson 15+ rush, Under 58.5. **All JSN rec-yds rungs are barred (99.5, 89.5, 109.5).** JSN receptions, Swift and Wilson legs get the §11 one-slip-per-player flag.
- **Ambiguous:** r2/odunze/results.md (~1:20 PM ET) says "Swift 3+ and Burden 4+ placed", and the 7-leg ticket containing Swift 3+ was cashed out (Ghost6, 4:10 PM ET). I could not confirm whether a separate Swift 3+ or Burden 4+ ticket is still open. Swift receptions rungs are treated as barred (fail closed); they fail Phase 14 anyway.

## 5. Risks and checks still to come
- **6:50 PM ET inactives:** Malik Muhammad (CB, Q toe): if out, JSN primary defender -> Jaylon Johnson/Stevenson; rerun P4 (CHI then 1 CB out; depleted-secondary rule needs 2) | D'Marco Jackson (LB, Q) | Drew Lock (QB, Q): backup only | Uchenna Nwosu (LB, Doubtful) | Charbonnet / J. Price usage: SEA RB split | Montez Sweat + Jeffery Simmons active (first CHI game for Simmons); JSN 100+ rerun if both play | Bradford / Pili / O'Connell (Q)
- **LOW-SAMPLE / PROXY:** pressure rate is a PROXY. Roschon Johnson has only 2 carry games. Charbonnet and Price have no 2026 sample. SEA LB coverage on RBs is a first-tackler proxy.
- **UNVERIFIED film:** Kupp, Barner, R. Johnson and Wilson (all cut).
- **Week label:** ESPN says Week 8 and the task says Week 9.
- **Odds staleness:** odds were pulled at 4:38 PM ET and the gate allows 1h. Any later use needs a fresh pull and a re-gate.
- **Applied exceptions:** none. BIASDUP is still staged (see section 3).

