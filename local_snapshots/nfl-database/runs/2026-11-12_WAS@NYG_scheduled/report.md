# WAS at NYG — Week 10 Thursday Night Football — SCHEDULED RUN (research only)

## 1. Header
- **Game:** Washington Commanders (2-5-1) at New York Giants (5-2-1), Week 10, TNF, MetLife Stadium (outdoors, FieldTurf). Kickoff **Thu Nov 12, 2026, 8:15 PM ET**. nflverse game_id 2026_10_WAS_NYG; ESPN event 401873052. Division game; rematch of the Wk5 27-27 OT tie.
- **Run type:** SCHEDULED RUN of "NFL enhanced edge analysis (TNF, Sunday, MNF)". Started 8:59 AM ET; inputs cut off 9:10 AM ET.
- **Gate status:** projection_ready = **false** (packet.json). Gates NFL-49 and NFL-56 are unmet, so this is **RESEARCH ONLY: no picks, no slips. SIMULATION NOT RUN** (0 trials, no seed). The 3×100k models were not run because the gates are unmet.
- **Packet:** GhostPapii21/nfl-matchup-database main **aca9406** ("pregame: refresh packets 2026-11-12T11:17Z"). Packet "Updated" 2026-11-12T11:16:38Z = **6:16 AM ET** (about 3 hours old at run time, under 24h). ANALYST_PROMPT.md v2 last changed in 1b146da. Read with `gh api` only, no clone.
- **Book prices:** packet 6:16 AM ET (Odds API via the packet). Live game-line recheck at **9:03 AM ET** (The Odds API, 3 credits, 1,936 left). Props are the packet's 6:16 AM ET prices only, not re-pulled.
- **Weather:** packet NWS 6:16 AM ET. `tools/weather_forecast.py` (NWS + Open-Meteo) at **9:01 AM ET**.
- **Label cap: Lean.** The official final injury report did come out Wed Nov 11 at about 4 PM ET, but final inactives (about 6:45 PM ET) are still pending, so every label stays capped at Lean.
- **Tools used:** gh API (repo), nflverse parquet (pbp, FTN charting, snap counts; hashes match the packet), ESPN public site API (scoreboard and summary), The Odds API (one 3-credit game-line call), tools/weather_forecast.py, WebSearch/WebFetch (NFL.com, Giants.com, Commanders.com, PFT/NBC, theScore, Sharp Football, Covers, VegasInsider, SI, Fanrecap, BettorsInsider).
- **Checked live:** official injury report, ESPN injury list and news, weather, game lines, line history and openers, Sharp coverage and tendencies, NGS (page did not render, so MISSING).
- **Not available / owner-supplied only:** PFF = MISSING (owner-supplied only, none given). FTN betting model = MISSING (owner-supplied only). Outlier true openers = not used (paywalled/signed-in). VegasInsider and Covers public line history used instead.
- **Lessons applied** (latest postmortem `postmortems/JAX_BAL_2026-11-05.md`): in rain, model the run share; take TE target hierarchy from the current QB's games, not season share (the Strange miss); prefer alt rungs when the model and the main line disagree; honor the passing-yards ban.

## 2. Five-line summary
1. Toss-up division rematch. NYG -2.5 / total 40.5 (Pinnacle 9:03 AM ET: NYG no-vig 48.4% to cover, Under 40.5 no-vig 48.7%). The total opened at 43.5 (Covers; VegasInsider's earliest row shows 47.5) and has dropped 3+ points.
2. **WEATHER ALERT (gate flag):** NWS has a 74% chance of light rain at kickoff with 12-13 mph NE wind. Open-Meteo has gusts up to 29.5 mph but only 0.02 in of rain. Rushing gets looked at first; deep and passing overs are cut.
3. Both defenses are blitz-heavy zone teams (NYG 24.8% man / 70.0% zone, 37-40% blitz; WAS 12.6% man / 78.4% zone, 40-43% blitz). NYG blitzed Daniels 63% in Wk5 (5 sacks). McCarthy has been sacked on 11.7% of his dropbacks.
4. Injury picture: per the official report, McCarthy and Skattebo have **no designation and will play**. ESPN's API still lists them Q and Out; that is stale. WAS is without C/G Lucas Patrick and TE Yankoff. Burks is DNP Wed, no designation, unconfirmed until inactives (ESPN lists him Out). WAS DT Daron Payne and WR Dyami Brown are on IR.
5. **Result: no validated edge.** One Lean research note survives: Skattebo rushing yards UNDER at retail (DK 55.5 / FD 56.5). The +3.6 / +4.0 figures are measured against the same book's no-vig, not against Pinnacle. Pinnacle 50.5 is the sharp reference (retail sits 5-6 yards above); that gap supports the under but is not a sharp-book edge. The note is flagged, not a pick. It depends on a hamstring snap-limit **ASSUMPTION** (~60% carry share; at a 65% share the yards median is ~57, which clears 55.5) and is a **SCRIPT CONFLICT** (an under on the favorite's RB). Spread, total and ML: no edge (already priced). Receiving legs are estimates only (no verified main defender). Passing yards are banned.

## 3. Game-script narrative (analyst read; the scenario sets the projection)
- **Pre-snap picture:** light rain plus gusty NE wind at night, both teams on 4 days of rest (short week; WAS has a short trip in the same time zone). NYG are slight favorites at home in a "White Out" game, and Nabers has called it "worth double" after the Wk5 tie.
- **Q1-Q2:** NYG come out run-first (neutral pass rate 47.7%, the second-highest time of possession in the league), with Skattebo back from the hamstring at about 60% of RB carries (**ASSUMPTION**, not measured; see Phase 2). Washington's interior run defense is the strength (middle 2.93 YPC; 3.66 YPC allowed, 8th), so early downs gain little and McCarthy gets passing downs against a 42.6% blitz. His sacked-when-blitzed rate is 6 of 24 dropbacks, a small sample. WAS starts with Daniels' quick game (short left/right is 58% of attempts) against a NYG zone that allows 6.03 YPA (2nd). NYG blitz Daniels heavily (63% in Wk5). Daniels has beaten the blitz this season (+0.19 EPA/dropback, 8.55 YPA), but NYG's blitz has been their best defense (-0.106 EPA allowed). **Read:** low first half, about 17-21 points combined, punt-heavy. WAS are 32nd on third down (31.1%), and Sharp: 42.4% of possessions against NYG fail to gain a first down, the highest rate in the league (league average 29.6%).
- **Q3-Q4:** game within one score most of the way (NYG by 0-6 in the central range). Gusts cut deep shots on both sides (NYG deep-left completions are McCarthy's chunk zone at 15.55 YPA). Red zone is where the scoring happens: NYG allow 78.9% RZ TD (31st) and WAS 75% (29th), but both allow few trips. Late, WAS chasing means Daniels scrambles and short targets to Okonkwo, White and Williams.
- **Central projection (analyst read; no sim):** NYG 21 - WAS 18 (range NYG 17-24, WAS 14-21). Total about 40 (range 34-46). NYG margin about +2.5. NYG win about 54-55%.

## 4. Breakdown
**What each defense allows (packet, nflverse Wk1-9, 8 games each; rank 1 = best)**
- **NYG D:** 189.2 pass yds/g (3rd), 6.03 YPA (2nd), WR 123.4 yds/g (5th), TE 45.4 yds/g (6th) but 5.8 TE rec/g (20th), RB rec 20.5 yds/g (4th), explosive passes 1.88/g (3rd). Weak spots: explosive runs 2.12/g (31st), 4.22 YPC (22nd), RZ TD 78.9% (31st), pressure floor (sacks + hits) 12.8% (28th). Run D by direction: right end 6.17 YPC (4 runs of 15+), middle 4.35. Trend: over the last 4 games, 28.1% third downs allowed (Sharp, 2nd); Wk9 at PHI held to 11 points with 7 sacks.
- **WAS D:** 256.0 pass yds/g (27th), 6.94 YPA (14th), TE 68.8 yds/g (29th), WR 13.2 rec/g (29th), RZ TD 75% (29th), pressure floor 14.1% (25th), sack rate 5.1% (24th). Strength: run D at 3.66 YPC (8th), 0.88 explosive runs/g (6th), middle 2.93 YPC. Trend: allowed 393 passing yards to SEA Wk3 and 326 to NYG Wk5 (Winston). Nacua had 14/19/150 in Wk9.
- **WAS O:** 21.5 pts/g; 6.75 YPA (22nd); third down 31.1% (32nd); WR yards 155.6/g (12th); TE 36.8/g (27th). With Daniels: aDOT 8.5, sack rate on dropbacks 16/219 = 7.3%, 24 scrambles for 250 yards, play action 20%. Last 4 games: about 1.84 points per drive (approximate), 8 TD drives in 45.
- **NYG O:** 22.8 pts/g; sack rate allowed 9.0% (28th); pressure floor allowed 18.6% (30th); TE yards 66.5/g (7th). McCarthy (3 games, 77 charted dropbacks, **small sample**): 9.57 YPA, aDOT 11.5, 9 sacks. Last 4 games: about 2.08 points per drive (approximate).

**QB vs pressure/blitz, targets when blitzed, third down** (nflverse pbp + FTN charting, computed 9:02 AM ET)
| QB | Dropbacks | vs blitz EPA/db (YPA) | no blitz EPA/db (YPA) | Hit/sack plays | Top targets when blitzed | 3rd-down conv |
|---|---|---|---|---|---|---|
| Daniels | 219 | +0.190 (8.55) | -0.001 (6.04) | 31 dropbacks, -0.97 EPA | Diggs 12, Burks 11, Williams 9, Okonkwo 6, White 5 | 33.3% (60) |
| McCarthy | 77 | -0.002 (10.19), 6 sacks in 24 | +0.252 (9.37) | 15, -0.99 EPA | Nabers 7, Fields 3, Likely 2 | 35.0% (20) |

**Defense blitz** (FTN, season): WAS 42.6% blitz (Sharp 40.4%, agrees), sack rate 7.7% when blitzing vs 3.1% when not. NYG 40.3% (Sharp 37.4%, agrees), 9.4% vs 2.9%, and -0.106 EPA/dropback when blitzing. Coverage (Sharp only, updated Nov 10): NYG 24.8% man / 70.0% zone, MOF closed 47.8% / open 49.1%; WAS 12.6% man / 78.4% zone, MOF open 60.2%. **SHARP CAUTION:** no free second source for man/zone. The Wk5 NYG 62% blitz-on-Daniels figure (Fanrecap) matches our FTN 63.2%.

**Pass rush (PFR via packet):** WAS Chaisson 17 pressures / 3.5 sacks, Oweh 12 / 4.0; DT Payne on IR. NYG Carter 10 / 2.0 (knee/back, full practice Wed), Reese 8 / 4.5 sacks on 48 blitzes, Thibodeaux 6 / 0, Burns 5 in 3 games.
**Protection:** WAS C Gulbin (knee, full) starts; G/C Lucas Patrick OUT (backup interior depth: Allegretti). NYG OL is fully healthy and practiced in full (Thomas, Runyan, Hudson, Mauigoa, Eluemunor).

**Secondaries and defender tables (PFR via packet):** WAS: LCB Douglas 7.6 YPT, RCB Amos 5.1 (3 g), NB Robertson 7.2 (ankle, LP Wed; backup Sainristil 9.7 YPT with 5 TD allowed), S Reaves 8.6 (3 TD), LB Styles 7.0. NYG: CB Banks 4.2 YPT, Newsome 6.7, NB Phillips 5.2, LB Reese 4.1, S Holland 6.0 (3 INT), Edmunds 8.4 (17/18 completions allowed); CB Hood (finger) had no designation. **Who covers whom is NOT known** (no free source), so every main defender is an estimate.

**Injuries** (official NFL.com / Giants.com / Commanders.com final report Wed Nov 11, ~4 PM ET; checked 9:02 AM ET)
- NYG: LB Malik Harrison Questionable (groin). No designation for McCarthy (hip), Skattebo (hamstring), Carter, Hood, Nabers, Mooney, C. Jones, Thomas or Eluemunor; all full on Wednesday. PFT (Nov 11, 4:29 PM ET) and theScore (via Schefter) say McCarthy and Skattebo will play. RB Tracy Jr. is on IR.
- WAS: OUT C/G Lucas Patrick (concussion) and TE Colson Yankoff (knee). WR Treylon Burks (foot) had no designation but was DNP Wednesday; ESPN lists him "Out" (5:06 PM ET Nov 11). Treat him as **DNP Wed, no designation, unconfirmed until inactives**, not as out. IR: DT Daron Payne, WR Dyami Brown. WR Terry McLaurin is absent from snaps since Wk6, not on the report and not on the depth chart: **status UNKNOWN**.
- **Data conflict for Ghost6:** the ESPN live list (in the packet and still on ESPN's API at 9:00 AM ET) shows Skattebo OUT and McCarthy Q. The official report supersedes it.

**Trades and news:** Nov 10 deadline: no WAS or NYG trades. Roster departures in the last 4 weeks: Charles Snowden (WAS DL) to ATL, Jihad Ward (NYG LB) to MIN. ESPN news feed at 9:00 AM ET had nothing new on WAS or NYG.

**Travel/rest:** 4 days each; WAS short trip, no time-zone change. Neutral.

**Weather:** NWS 6:16 AM ET packet: 52°F, NE 12 mph, 74% light rain likely; low 49°F in-game. tools/weather_forecast.py at 9:01 AM ET: NWS 74% precip / 13 mph sustained / gust n/a; Open-Meteo 43% / 11.9 mph / **29.5 mph gusts** / 0.02 in. **FLAG: precip 74%, gusts 29.5.** Packet rain model (211 rain team-games since 2018): about -15% team passing yards and -4 points of completion rate in rain; at the forecast, WAS 214→190 and NYG 229→204 team pass yards.

**15-phase ledger** (filled vs missing)
1 slate PASS · 2 identity PASS · 3 game history PASS · 4 role/snaps PARTIAL (no route participation) · 5 team baselines PASS · 6 script PARTIAL (analyst read) · 7 coverage shell PARTIAL (Sharp only, SHARP CAUTION) · 8 defender assignment **MISSING** (who covers whom unknown) · 9 QB pressure/blitz PASS (pressure is a hits+sacks floor; no true pressure rate) · 10 OL/pass rush PARTIAL (no grades) · 11 injuries PASS (official final report; inactives pending) · 12 weather/travel PASS (FLAG) · 13 prices PARTIAL (props from 6:16 AM ET; no FTN model; true opener from public history) · 14 projection/sim **NOT RUN** (gates unmet) · 15 inactives **PENDING** (~6:45 PM ET).

## 5. Opportunity table
Team volume (analyst read): NYG about 62-66 plays, 29-32 pass attempts, 26-30 rushes (about 22-26 RB carries). WAS about 58-62 plays, 30-33 attempts, 22-26 rushes. Shares come from nflverse pbp; the QB-specific share is used where the QB changed.
| Player | Role | Snaps | Projected volume | Basis | Label |
|---|---|---|---|---|---|
| Malik Nabers (NYG) | WR1 | 73-90% | 8-10 tgt, 5-7 rec | McCarthy share 32% (21/65); Wk7 9, Wk9 8 tgt | Volume-supported |
| Isaiah Likely (NYG) | TE1 | 75-91% | 5-7 tgt, 3-5 rec | McCarthy share 18% (12/65) vs 27% season; Wk7 4, Wk9 6 | **Shrinking** (QB change) |
| Malachi Fields (NYG) | WR2 | 74-94% | 4-6 tgt, 2-3 rec | McCarthy 20%; 5, 5 | Volume-supported (low ceiling) |
| Darnell Mooney (NYG) | WR3 | ~55% | 1-3 tgt | McCarthy 9% | Depth; efficiency-driven (54 yds Wk9 on 4 tgt) |
| Cam Skattebo (NYG) | RB1 | 55-65% est. | 13-16 car (**ASSUMPTION**, ~60% share), 1-3 tgt; at 65% share: 14-17 car | Measured RB-carry share 62% Wk5, 61% Wk7 (61-69% season). The 13-16 / ~60% range is a hamstring snap-limit **ASSUMPTION**, not measured. | Volume-supported, **shrink risk (ASSUMPTION)** |
| Devin Singletary (NYG) | RB2 | ~25-35% | 4-8 car | 15-25% with Skattebo active (70% Wk9 without him) | **DO NOT PLAY** (<60%) |
| Stefon Diggs (WAS) | WR1 | ~61-65% | 5-7 tgt, 3-5 rec | Daniels games Wk6/8/9: 7, 6, 5 tgt (~19%) | Volume-supported |
| Antonio Williams (WAS) | WR2 | 83-84% | 5-7 tgt, 3-4 rec | Wk8 7, Wk9 6; snaps up from 37% to 84% | Expanding |
| Chig Okonkwo (WAS) | TE1 | 74-77% | 5-7 tgt, 3-5 rec | 7, 4, 7 last 3; Burks is DNP Wed, no designation, unconfirmed until inactives | Expanding |
| Van Jefferson (WAS) | WR3 | 58% Wk9 | 2-6 tgt (wide) | 7 tgt Wk9 with Burks out and D. Brown on IR; 3% season share | Expanding but **unstable** (depends on Burks/McLaurin) |
| Rachaad White (WAS) | RB | 47-69% | 7-11 car, 2-4 tgt | RB-carry share 44% Wk8, 47% Wk9 | **DO NOT PLAY** (<60%) |
| Austin Ekeler (WAS) | RB | 33-45% | 6-9 car | 36%, 53% RB share | **DO NOT PLAY** (<60%) |
| Jayden Daniels (WAS) | QB run | — | 4-8 att incl. scrambles | Carries 8 (Wk5 vs NYG), 3, 2, 4 last 3 | Efficiency-driven (Wk5 104 yds on 8) / shrinking recently |
| J.J. McCarthy (NYG) | QB run | — | 2-4 att | 26 and 23 rush yds in 2 of 3 games | Small sample |

**Phase 2 (Skattebo carries) — ASSUMPTION, not measured.** The 13-16 carry range uses about a 60% share of the 22-26 RB carries, below his measured 61-69% season share (62% Wk5, 61% Wk7). That lower share is a hamstring snap-limit assumption, and it is what drives the under (13-16 car × 3.6-4.0 YPC = ~47-64, median ~53 vs 55.5; implied YPC 53/14.5 = 3.66, the WAS YPC allowed already used in this report). At a 65% share of the same 22-26 RB carries (about 14-17 carries, same 3.6-4.0 YPC basis), the rushing-yards median is ~57 (15.5 × 3.66), which clears 55.5. The under note therefore depends on the snap-limit assumption.

## 6. Brainstorm (divergent) and critical review (convergent)
Angles:
1. **Weather under:** 74% rain plus 29.5 mph gusts; the packet rain model cuts about 15% off team pass yards, so under 40.5.
2. **NYG blitz vs Daniels:** 63% blitz in Wk5 with 5 sacks, against Daniels' +0.19 EPA vs blitz on the season. It cuts both ways: WAS stalls or WAS hits chunk plays.
3. **McCarthy sack-prone vs the WAS blitz:** 11.7% sacked per dropback, 6 sacks in 24 blitzed dropbacks; WAS blitzes 42.6%. NYG drives stall, which supports WAS +2.5 or the under.
4. **Skattebo UNDER at retail:** returning from the hamstring, against WAS's interior run D (middle 2.93 YPC, 3.66 overall), with retail 55.5/56.5 against Pinnacle 50.5.
5. **Red-zone TD leak both ways:** NYG 78.9% and WAS 75% RZ TD allowed, which points to the over and TD scorers.
6. **Likely vs the WAS TE leak:** WAS allows 68.8 TE yds/g and NYG TEs went 13-129 in Wk5, but McCarthy targets Likely at only 18%.
7. **Van Jefferson WR3 expansion:** 58% snaps and 7 targets in Wk9; market is 1.5 receptions at +158/+178.
8. **WAS third-down futility:** 31.1% (32nd) against NYG's 28.1% allowed over the last 4 (Sharp). That means a WAS team-total under and NYG field-position control.
9. **Daniels rushing vs NYG man/blitz looks:** 104 yards on 8 carries in Wk5, against recent 11/23/16 and NYG's rush-spy plan.
10. **WAS nickel downgrade:** Robertson (ankle, LP Wed) could give way to Sainristil (9.7 YPT, 5 TD allowed), a boost for NYG slot routes.

| # | Angle | Verdict | Reason / case against |
|---|---|---|---|
| 1 | Weather under | **WEAKEN** | Already priced: the total moved from 43.5 (Covers open; VegasInsider earliest 47.5) to 40.5, and Pinnacle went 41→40.5 between 6:16 and 9:03 AM ET. Open-Meteo has only 0.02 in of rain and NWS gives no gust value. The rain model measures yards, not points. Proven wrong if the rain clears or the wind drops below 10 mph. |
| 2 | NYG blitz vs Daniels | **WEAKEN** | One game (38 dropbacks). The season blitz split says Daniels wins. Two-sided, and no sack market in the packet. Double-counts with #8. |
| 3 | McCarthy sacks | **WEAKEN** | 77 dropbacks, 24 against the blitz: tiny sample. NYG's OL is now fully healthy. Already inside the spread/total. |
| 4 | Skattebo under (retail) | **KEEP (weakened)** | For: Pinnacle 50.5 sits 5-6 yards below retail, which supports the under but is not a sharp-book edge (the +3.6/+4.0 is vs the same book's no-vig); WAS is strong inside; hamstring return risk; the backtests found rush unders were the only edge. Against: **SCRIPT CONFLICT** — this is an under on the favorite's RB, and rain plus a favorite script add NYG rushes (26-30); the ~53 median uses a ~60% carry-share **ASSUMPTION** (not measured); at a 65% share the median is ~57 on 14-17 carries, which clears 55.5, so the note depends on the snap-limit assumption; his log is 81/36/60/58/59/124 (4 of 6 over 55.5; Phase 7 miss audit / WARN: the 58-60 games cleared by only 2-4 yards, and the hamstring is a new cause this week); he ran 13-59 vs WAS in Wk5. |
| 5 | RZ TD leak | **DROP** | Both defenses allow few RZ trips (NYG tied 3rd fewest), it offsets #1, and no priced market was checked. |
| 6 | Likely vs TE leak | **WEAKEN, flagged to Rico** | The scenario (WAS zone 78%, TE leak, Wk5 13-129) says over. The opportunity check (McCarthy's 18% share, 4 and 6 targets) says under. Per the Nov 4 rule this is flagged, not overruled. No verified main defender, so not playable. |
| 7 | Van Jefferson | **DROP (pending inactives)** | One game. The market at +158/+178 implies information we don't have (McLaurin or Burks status). Our naive estimate is 20+ points above the market, which points to missing information, not an edge. Depth-WR 5% test: 3% season share, 21% in Wk9. Fails the defender rule. |
| 8 | WAS third-down futility | **KEEP (script support only)** | Real and stable (8 games). Already reflected in NYG -2.5 / 40.5. Team-total markets are not in the packet, so no market data. |
| 9 | Daniels rushing | **WEAKEN, flagged to Rico** | Scenario (blitz and man looks) says over; recent logs (3, 2, 4 carries; left elbow on the report, full practice) say under. Pinnacle 34.5 vs DK 38.5: books disagree. No edge stated. |
| 10 | WAS nickel | **WEAKEN** | Robertson has no designation (LP Wed only). Depends on inactives and alignment, and who covers whom is unknown. |

**Strongest case against the overall read (low-scoring, NYG by a field goal):** the teams scored 27-27 in Wk5 (110 NYG plays in OT). McCarthy's 9.6 YPA and WAS's 256 pass yds/g allowed could produce explosives even in rain (NYG deep-left 15.55 YPA). Both red zones leak TDs. The market has already moved 3+ points toward the under, so any edge on the under is gone, and the over could be the value if the rain is as light as Open-Meteo's 0.02 in suggests.

## 7. Market table
Pinnacle no-vig is the sharp reference. Game lines come from the live 9:03 AM ET pull (de-vigged below, multiplicative); props are packet 6:16 AM ET values. "Our prob" is the analyst read (no sim).
| Market | Our fair | Pinnacle no-vig | DK / FD no-vig | Edge (pts) | Best retail (BE) | Movement | Label | Driver | Kill-switch |
|---|---|---|---|---|---|---|---|---|---|
| NYG -2.5 | NYG by ~2.5; cover 48-50% | NYG 48.4% / WAS 51.6% (-2.5 +102/-112) | DK -2.5: 49.6/50.4; FD -1.5: 52.2/47.8 | ~0 to +1.6 NYG | NYG DK -2.5 -108 (BE 51.9%); WAS FD +1.5 +100 (50.0%) | Open NYG -1.5 → -2.5 (McCarthy/Skattebo cleared Tue-Wed); Pinnacle NYG price -106 → -101 → +102 (drifting to WAS) | No edge | — | — |
| Total 40.5 | ~40; Under 51% | Over 51.3% / Under 48.7% (40.5 -112/-101) | DK 40.5: 51.7/48.3; FD 41.5: 47.8/52.2 | Under ~+2.3 (below the +3 flag) | Under 41.5 FD -120 (BE 54.5%); Under 40.5 DK -102 (BE 50.5%) | 43.5 open (Covers) / 47.5 earliest (VegasInsider) → 41.5 → 40.5; Pinnacle 41 → 40.5 at 9:03 AM ET | No edge (already priced) | Weather | Rain forecast drops below 50% or gusts under 15 mph; total at 39.5 or lower |
| Moneyline | NYG 54-55% | NYG 54.1% / WAS 45.9% (-124/+113) | DK 55.1/44.9; FD 54.7/45.3 | ~0 | NYG Pinnacle -124 / WAS DK +114 | Pinnacle NYG -136 → -127 → -124 | No edge | — | — |
| **Skattebo rush yds UNDER** | Median ~53 at the ~60% snap-limit **ASSUMPTION**; ~57 at a 65% share (14-17 car), which clears 55.5, so the note depends on the assumption. P(U55.5) 53%, P(U56.5) 54% (base case) | Sharp reference: Pinnacle **50.5** (O 54.5% / U 45.5%; not comparable to retail lines). Retail sits 5-6 yards above Pinnacle. | DK 55.5: U 49.4%; FD 56.5: U 50.0% | **+3.6 (DK 55.5) / +4.0 (FD 56.5)** vs the same book's no-vig. Pinnacle 50.5 supports the under but this is **not a sharp-book edge**. | FD U56.5 -113 (BE 53.0%) EV ≈ +1.8%; DK U55.5 -109 (BE 52.1%) EV ≈ +1.6% | Packet first-seen not tracked for props; Pinnacle 50.5 is 5-6 yds below retail | **Lean (research only)**; **SCRIPT CONFLICT**; depends on snap-limit **ASSUMPTION** | Line lag at retail + WAS interior run D + hamstring return | Retail moves to 52.5 or lower; reports of a full workload with no pitch count (the 65% share median ~57 already clears 55.5); Singletary inactive; rain upgraded to heavy (more carries) |
| Daniels rush yds | ~33-38 (uncertain) | Line 34.5: O 53.3% / U 46.7% | DK 38.5: 50.2/49.8; FD 37.5: 50/50 | Not stated (scenario and logs conflict) | — | — | No label; flag | — | — |
| Likely rec yds (estimate only) | Scenario over / opportunity ~40 | 48.5: O 50.4% / U 49.6% | DK 47.5: 50.2/49.8; FD 48.5: 50/50 | Not stated (conflict) | — | — | **Not playable** (no verified defender) | — | — |
| Nabers rec yds (estimate only) | ~65-70 | 67.5: O 50.6% | DK/FD 69.5: ~50/50 | ~0 | — | — | Not playable | — | — |
| Diggs rec yds (estimate only) | ~33-37 | 40.5: O 46.2% / U 53.8% | DK 38.5: 49.4/50.6; FD 36.5: 50/50 | Books disagree by 4 yds; ~0 vs FD | — | — | Not playable | — | — |
| Okonkwo receptions (estimate only) | P(4+) ~55% | Line 4.5: O 39.9% | DK/FD 3.5: O 56.6% / 55.9% | ~-1 vs DK | O3.5 FD -148 (BE 59.7%), not +EV | — | Not playable | — | — |
| Passing yards (Daniels, McCarthy) | — | — | — | — | — | — | **BANNED** (Rico, Nov 3/4) | — | — |
| WAS RBs, Singletary | — | — | — | — | — | — | **DO NOT PLAY** (<60% RB carries) | — | — |
- FTN model: MISSING (owner-supplied only). No 40+ point gaps were priced. The naive Van Jefferson estimate was set aside as a likely data gap and never tiered.
- **Live de-vig working (9:03 AM ET):** Pinnacle ML -124 → 55.36%, +113 → 46.95%, sum 102.31% → **54.1 / 45.9**. Pinnacle spread +102 → 49.50%, -112 → 52.83%, sum 102.34% → **48.4 / 51.6**. Pinnacle total -112 → 52.83%, -101 → 50.25%, sum 103.08% → **51.3 / 48.7**. DK ML -135/+114 → 55.1/44.9; DK spread -108/-112 → 49.6/50.4; DK total -118/-102 → 51.7/48.3. FD ML -132/+112 → 54.7/45.3; FD spread -1.5 -120/+100 → 52.2/47.8; FD total 41.5 +100/-120 → 47.8/52.2.
- **EV working:** FD U56.5 -113: 0.54 × (100/113) − 0.46 = +0.018. DK U55.5 -109: 0.53 × (100/109) − 0.47 = +0.016.
- **Edge basis (Skattebo):** +4.0 (FD 56.5) and +3.6 (DK 55.5) are measured against the same book's no-vig, not against Pinnacle. The sharp reference is Pinnacle 50.5; retail sits 5-6 yards above that line. The Pinnacle gap supports the under, but it is not a sharp-book edge.

## 8. Projections
- **Game:** NYG 21 - WAS 18 (ranges 17-24 / 14-21); total about 40 vs 40.5; NYG -2.5 is a coin flip. Packet baselines (no weather): matchup_pair 24.5-22.8 (47.3), independent 22.5-21.0 (43.5). Adjustment: about -4 to -7 total points for rain/gust passing efficiency (packet rain model -15% pass yards), WAS third-down futility and the NYG blitz.
- **1H:** about 17-21 combined (packet matchup_pair 1H 23.2 before weather).
| Player | Stat | Packet baseline (mean / median) | Our number | Adjustment |
|---|---|---|---|---|
| Skattebo | rush yds | 67.4 / 55.1 | ~53 (13-16 car × 3.6-4.0) at the ~60% snap-limit **ASSUMPTION**; ~57 at a 65% share (14-17 car × 3.6-4.0). The 65% median clears 55.5, so the under note depends on the assumption. | WAS run D, hamstring return; rain adds carries; **SCRIPT CONFLICT** (under on the favorite's RB) |
| Nabers | rec yds | 87.3 / 91.7 (rain-forecast 68.2) | ~65-70 | McCarthy share 32%, NYG run-lean, gusts cut deep |
| Likely | rec yds | 63.0 / 66.9 (rain 45.9) | ~40 (opportunity) / higher (scenario) | McCarthy share 18%; flagged |
| Fields | rec yds | 38.7 / 28.0 | ~28 | — |
| Diggs | rec yds | 39.4 / 40.3 (rain 36.5) | ~33-37 | NYG WR D 5th, zone |
| A. Williams | rec yds | 32.5 / 25.7 | ~32 | Snaps up to 84% |
| Okonkwo | rec yds | 39.3 / 40.6 (rain 32.6) | ~32-36 | Burks DNP Wed, no designation, unconfirmed until inactives (+ if he sits), NYG TE yards D 6th (−) |
| Daniels | rush yds | not in packet baselines | ~33-38 | Blitz/scramble (+) vs recent usage (−) |

## 9. Open items (re-check before kickoff)
1. **Final inactives, about 6:45 PM ET (Phase 15):** Burks (DNP Wed, no designation, unconfirmed until inactives), McLaurin (unknown), Robertson, Harrison; confirm Skattebo and McCarthy are active. Reprice if any line moves more than 0.5 point or 20 cents.
2. **Skattebo:** any beat report of a snap or carry limit (the ~60% share is a hamstring snap-limit **ASSUMPTION**, not measured; at a 65% share the yards median is ~57, which clears 55.5, and the under note depends on that assumption). Re-pull props near T-90; if retail drops to 52.5 or lower, the note is dead.
3. **Weather:** rerun tools/weather_forecast.py at about 6:45 PM ET; the flag clears only if precip is under 50% and gusts are under 20 mph.
4. Gates NFL-49 / NFL-56 and projection_ready=false still block picks. The sim was not run.
5. Data issues for Ghost6: (a) the ESPN injury list (packet and API) shows Skattebo OUT / McCarthy Q, contradicting the official report; (b) McLaurin's status is missing everywhere; (c) NGS public page returned empty (JS), so routes/separation are MISSING; (d) man/zone is Sharp only (SHARP CAUTION); (e) who-covers-whom is unknown, so all receiving legs are unplayable.
6. Two conflicts flagged to Rico (Nov 4 rule): Likely (scenario over vs opportunity under) and Daniels rushing (scenario over vs recent usage under).

## 10. Sources and freshness (ET)
- Repo packet/brief/INDEX/ANALYST_PROMPT (gh API, aca9406): read 9:00 AM; packet built 6:16 AM.
- nflverse pbp / FTN / snap counts parquet (sha256 1028614beb74 / 75783665c9e4 / 78c013d97bde, same as packet): pulled 9:01 AM; data through Wk9.
- PFR advanced defense (via packet, nflverse pfr_advstats): 6:16 AM.
- Official injury report: NFL.com /injuries/league/2026/reg, Giants.com (Nov 11, 4:00 PM), Commanders.com injury report: checked 9:02 AM.
- PFT/NBC (Alper, Nov 11, 4:29 PM) and theScore (Schefter) on McCarthy/Skattebo playing: checked 9:02 AM.
- ESPN API summary (event 401873052: injuries, pickcenter DK, last five, news): 9:00 AM.
- Weather: NWS via packet (6:16 AM); tools/weather_forecast.py NWS + Open-Meteo, file src/forecast_2026-11-12_0901.json (9:01 AM).
- The Odds API live game lines (Pinnacle/DK/FD), src/live_gamelines_0903.json, book updates 9:03 AM; packet props 6:16 AM.
- Line history: VegasInsider line-movements page and Covers Week 10 openers (lines as of 11-11), SI Betting: checked 9:08 AM.
- Sharp Football coverage schemes and defensive tendencies (updated Nov 10) and Sharp WAS-NYG worksheet: checked 9:05 AM. Fanrecap Wk5 blitz figure (cross-checked with FTN).
- NGS receiving page: attempted 9:03 AM, empty render, MISSING. PFF: MISSING (owner-supplied only). FTN model: MISSING (owner-supplied only). Outlier: not used.

## Slate-wide table of surviving edges (strongest first)
| # | Game | Market | Side / line | Best price (BE) | Our prob vs no-vig | Edge | Label | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | WAS@NYG | Skattebo rushing yards | UNDER 56.5 FD / 55.5 DK | FD -113 (53.0%) / DK -109 (52.1%) | 54% vs 50.0% / 53% vs 49.4% (same-book no-vig); Pinnacle 50.5 is the sharp reference (retail 5-6 yds above) | +4.0 / +3.6 vs same-book no-vig (supports the under; not a sharp-book edge) | Lean (cap) | Research note only; not a pick; SCRIPT CONFLICT (under on the favorite's RB); depends on hamstring snap-limit ASSUMPTION (~60% share; 65% share median ~57 clears 55.5); inactives and gates pending |
No other edge survived. No edge on spread, total or ML.

Research only. Not validated. Not betting advice.
