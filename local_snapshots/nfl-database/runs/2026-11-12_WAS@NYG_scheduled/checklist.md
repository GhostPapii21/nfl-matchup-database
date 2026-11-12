# Checklist — WAS@NYG TNF Week 10 — SCHEDULED RUN (research only)

VETTED: Ghost6, research-only (four fixes applied: Skattebo ~60% share labeled ASSUMPTION + 65% sensitivity, Phase 7 WARN with miss audit, Phase 13 SCRIPT CONFLICT, +3.6/+4.0 vs same-book no-vig with Pinnacle 50.5 as sharp reference).

Run: 2026-11-12 08:59-09:10 AM ET · packet aca9406 (Updated 6:16 AM ET) · projection_ready=false · gates NFL-49/NFL-56 unmet · SIMULATION NOT RUN (0 trials, no seed) · label cap Lean (inactives pending).

## Skattebo rush yds U55.5 DK -109 / U56.5 FD -113

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|---|---|---|---|---|---|
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 1 Data pull | PASS | nflverse pbp Wk1-9: 81/36/60/58/59/124; RB carries Wk5 13/21, Wk7 17/28 | nflverse pbp sha 1028614beb74 | 09:01 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 2 Opportunity | PASS (ASSUMPTION) | 13-16 car × 3.6-4.0 YPC = ~47-64, median ~53 vs 55.5, using a ~60% RB-carry share. That share is a hamstring snap-limit **ASSUMPTION**, not measured (measured share 62%/61% last 2 healthy, 61-69% season; N1 ≥60% PASS, borderline). At a 65% share: 14-17 car of the 22-26 RB carries, same 3.6-4.0 YPC basis, median ~57 (15.5 × 3.66), which clears 55.5. The under note depends on the snap-limit assumption. | nflverse pbp | 09:02 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 3 Defensive profile | PASS | WAS 3.66 YPC (8th), RB rush 79.1/g, middle 2.93 YPC, 0.88 15+ runs/g | packet brief | 06:16 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 4 Defender coverage | N/A | pure rushing leg | - | - |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 5 Routes/scheme | N/A | rushing leg; WAS heavy box 26.8%, light 39.3% (Sharp) | Sharp tendencies (upd Nov 10) | 09:05 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 6 Usage trend | PASS | first game back from hamstring (missed Wk9); FP Tue/Wed | Giants.com report | 09:02 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 7 Recent form (warning only) | WARN | Miss audit already written: 4 of 6 games over 55.5; the 58-60 games cleared by 2-4 yards; the hamstring is a new cause this week. Cross-check disagrees with the ~53 projection; flagged as WARN. | nflverse pbp | 09:02 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 8 Injuries | PASS | no designation (official); ESPN API 'Out' is stale | NFL.com/Giants.com/PFT | 09:02 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 9 NGS | MISSING | NGS page empty render (RYOE unavailable) | nextgenstats.nfl.com | 09:03 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 10 Film | MISSING | not reviewed this run | - | - |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 11 Environment | PASS (FLAG) | 74% rain, gusts 29.5; WEATHER ALERT, rushing reviewed first | weather_forecast.py | 09:01 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 12 Source audit | PASS | all inputs <48h; props 6:16 AM ET | packet/live | 09:10 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 13 Script gate | SCRIPT CONFLICT | Under on the favorite's RB. NYG are a moderate favorite / toss-up (-2.5); rain and a favorite script add NYG rushes (26-30). The under runs against that script. | Pinnacle live | 09:03 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 14 Models/price/edge | MISSING | SIMULATION NOT RUN (gates NFL-49/56 unmet); analyst P(U55.5)=53% vs DK no-vig 49.4% = +3.6; FD U56.5 54% vs 50.0% = +4.0. Those +3.6/+4.0 figures are vs the same book's no-vig, not a sharp-book edge. Sharp reference: Pinnacle 50.5 (retail sits 5-6 yards above), which supports the under. At a 65% carry share the yards median is ~57, which clears 55.5, so the note depends on the snap-limit ASSUMPTION. EV +1.6%/+1.8% | packet no-vig; Pinnacle 50.5; analyst read | 09:10 |
| Skattebo rush yds U55.5 DK -109 / U56.5 FD -113 | 15 Inactives | MISSING | pending ~6:45 PM ET | - | - |

## Game total Under 40.5

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|---|---|---|---|---|---|
| Game total Under 40.5 | 1 Data pull | PASS | 8 games each team | nflverse | 09:01 |
| Game total Under 40.5 | 2 Opportunity | N/A | game market | - | - |
| Game total Under 40.5 | 3 Defensive profile | PASS | NYG 21.5 PA, WAS 25.2 PA; WAS 3rd-down 31.1% | packet | 06:16 |
| Game total Under 40.5 | 4 Defender coverage | N/A | game market | - | - |
| Game total Under 40.5 | 5 Scheme | PARTIAL | NYG 70% zone / WAS 78.4% zone (Sharp only, SHARP CAUTION) | Sharp | 09:05 |
| Game total Under 40.5 | 6 Usage | N/A | - | - | - |
| Game total Under 40.5 | 7 Recent form | PASS | Wk5 27-27 OT; NYG Wk9 19-11 | ESPN | 09:00 |
| Game total Under 40.5 | 8 Injuries | PASS | official report | NFL.com | 09:02 |
| Game total Under 40.5 | 9 NGS | MISSING | empty | NGS | 09:03 |
| Game total Under 40.5 | 10 Film | MISSING | - | - | - |
| Game total Under 40.5 | 11 Environment | PASS (FLAG) | precip 74%, gusts 29.5 | weather_forecast.py | 09:01 |
| Game total Under 40.5 | 12 Source audit | PASS | <48h | - | 09:10 |
| Game total Under 40.5 | 13 Script gate | PASS | toss-up | Pinnacle | 09:03 |
| Game total Under 40.5 | 14 Models/price/edge | FAIL | SIM NOT RUN; analyst Under 51% vs Pinnacle no-vig 48.7% = +2.3 (below +3 flag; market moved 43.5/47.5→40.5 already) | live de-vig | 09:03 |
| Game total Under 40.5 | 15 Inactives | MISSING | pending | - | - |

## Isaiah Likely rec yds (estimate only)

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|---|---|---|---|---|---|
| Isaiah Likely rec yds (estimate only) | 1 Data pull | PASS | McCarthy-era tgts 12/65 (18%) | nflverse | 09:02 |
| Isaiah Likely rec yds (estimate only) | 2 Opportunity | PASS | 5-7 tgt; SHRINKING vs 27% season share | nflverse | 09:02 |
| Isaiah Likely rec yds (estimate only) | 3 Defensive profile | PASS | WAS TE 68.8 yds/g (29th) | packet | 06:16 |
| Isaiah Likely rec yds (estimate only) | 4 Defender coverage | FAIL | main defender NOT verified (who-covers-whom unknown; Styles/Reaves/Sainristil inferred) | PFR via packet | 06:16 |
| Isaiah Likely rec yds (estimate only) | 5 Routes/scheme | PARTIAL | WAS zone 78.4%, MOF open 60.2% (Sharp only) | Sharp | 09:05 |
| Isaiah Likely rec yds (estimate only) | 6 Usage trend | PASS | snaps 75-91% | snap counts | 09:01 |
| Isaiah Likely rec yds (estimate only) | 7 Recent form | PASS | 12, 53 yds in McCarthy full starts | nflverse | 09:02 |
| Isaiah Likely rec yds (estimate only) | 8 Injuries | PASS | no designation | NFL.com | 09:02 |
| Isaiah Likely rec yds (estimate only) | 9 NGS | MISSING | - | NGS | 09:03 |
| Isaiah Likely rec yds (estimate only) | 10 Film | MISSING | - | - | - |
| Isaiah Likely rec yds (estimate only) | 11 Environment | PASS (FLAG) | rain; wind takes TE share (packet rain model) | packet | 06:16 |
| Isaiah Likely rec yds (estimate only) | 12 Source audit | PASS | - | - | 09:10 |
| Isaiah Likely rec yds (estimate only) | 13 Script gate | PASS | favorite side | - | 09:03 |
| Isaiah Likely rec yds (estimate only) | 14 Models/price/edge | MISSING | SIM NOT RUN; scenario vs opportunity conflict, flagged to Rico | - | 09:10 |
| Isaiah Likely rec yds (estimate only) | 15 Inactives | MISSING | pending | - | - |

## Game-level items

| Item | Status | Note |
|---|---|---|
| Passing-yards legs | CUT | banned (Rico Nov 3/4) |
| WAS RBs White (44-47% RB carries), Ekeler; NYG Singletary | CUT | N1 do-not-play (<60%) |
| All receiving legs | CUT | no verified main defender (Phase 4/8 MISSING) |
| Spread NYG -2.5 / ML | NO EDGE | Pinnacle no-vig 48.4/51.6; ML 54.1/45.9 (9:03 AM ET) |
| Daniels rush yds | FLAG | scenario vs logs conflict; no edge stated |
| Van Jefferson | DROP | naive estimate 20+ pts over market = likely missing roster info; recheck at inactives |
| Weather | FLAG | precip 74% (NWS), gusts 29.5 mph (Open-Meteo), sustained 13 |

## Summary

- Passed (research-only, Lean cap): none as picks. One research note: Skattebo rushing yards UNDER (retail 55.5/56.5), +3.6/+4.0 vs same-book no-vig (not a sharp-book edge; Pinnacle 50.5 is the sharp reference, retail 5-6 yards above). SCRIPT CONFLICT (under on the favorite's RB). The note depends on a hamstring snap-limit ASSUMPTION (~60% share; 65% share median ~57 clears 55.5). Thin +EV, needs inactives and gates.
- Cut: Game total Under (edge +2.3, already priced), every receiving leg (no defender), passing yards (ban), committee backs (N1).
- Seeds / scripts: none, SIMULATION NOT RUN.
- Data gaps: NGS (empty render), PFF/FTN model (owner-supplied only, none supplied), man/zone second source, who-covers-whom, McLaurin status, film, true props movement. ESPN injury API contradicts the official report (Skattebo/McCarthy).
- Artifacts: report.md, src/ (packet copies, live game lines, weather json, usage/qb tables).
