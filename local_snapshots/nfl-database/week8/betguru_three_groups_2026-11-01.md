# BetGuru: three groups for Sun Nov 1, 2026 (Week 8) - RESEARCH ONLY, Rico places bets
Built Sat Oct 31 ~7:10 PM ET. FanDuel prices pulled 2026-10-31T18:49 ET (public sbapi, fd_pull_all.py). Rebuild: /workspace/nfl-database/week8/betguru_2026-11-01_raw/ (build_legs.py seeds 101/202/303, legs_all.json, leg_*.json, sims_summary.csv).

## Headline
- Only 6 of 41 candidate props passed every computable gate. That fills ONE group of six, not three. Groups 2 and 3 were NOT padded.
- **Strict-rule warning:** two required inputs are MISSING for every leg: (a) the individual CB/S coverage numbers (per-defender catches/yards allowed are paid-only - PFF/FantasyPoints; checklist P7.cb_suppression = UNAVAILABLE), used here only as a PBP proxy (defender named on completions); (b) NGS route-tendency percentages (public NGS route charts are images of targeted routes; route participation is UNAVAILABLE). Under the 'any missing input cuts the leg' rule, ALL legs fail. Ghost6/Rico must decide whether the proxy is acceptable.
- Outlier / PropsMadness: MISSING (browser-only; not reached). Two volume sources used instead: ESPN box scores (fixes.sqlite player_stats) + nflverse usage/snaps (fix_player_game_usage / fix_player_role).
- Two legs (Lamb, Gibbs) conflict with Rico's placed FD SGP Ticket 2 (same player) - flagged.

## Group A (the only group that passed)
| # | Player | Mkt | Rung | FD | MC | Bias | GameRand | Avg | Flag |
|-|-|-|-|-|-|-|-|-|-|
|1|Puka Nacua (LA vs LAC)|Receiving Yds|70+|-290|0.638|0.787|0.819|0.748||
|2|CeeDee Lamb (DAL vs ARI)|Receiving Yds|60+|-280|0.792|0.681|0.764|0.746|Lamb 60+ yds is already on placed FD SGP Ticket 2 - skill sec.11 bars a player on two slips; Rico/Ghost6 decide|
|3|Trey McBride (ARI vs DAL)|Receptions|7+|-225|0.650|0.668|0.932|0.750||
|4|Brock Bowers (LV vs NYJ)|Receptions|6+|-158|0.629|0.636|0.756|0.674||
|5|DK Metcalf (PIT vs CLE)|Receiving Yds|40+|-225|0.768|0.676|0.722|0.722||
|6|Jahmyr Gibbs (DET vs MIN)|Rushing Yds|70+|-250|0.765|0.686|0.778|0.743|Gibbs (5+ rec) is already on placed FD SGP Ticket 2 - same-player conflict; Rico/Ghost6 decide|

Combined FD price (independent legs, SGP will reprice for same-game Lamb+McBride): +771 (8.71x). Product of avg sim probs = 0.151 (~1 in 6.6).
Without the two placed-ticket conflicts (4 legs): see per-leg prices; alternates = none passed.

## Group B / Group C: NOT BUILT - not enough legs passed (see Cuts).

## Rams backfield verdict (Corum vs Kyren)
Sources: nflverse snaps (fix_player_game_usage) + ESPN box & play-by-play (summary API).
- Wk4 @PHI: Kyren 83% snaps, 16 car/13 tgt, first-drive RB touches = Kyren; Corum 15%, 5 car.
- Wk5 vs BUF: Kyren 73%, 16 car/8 tgt, first RB carry = Kyren; Corum 27%, 5 car.
- Wk6 vs ARI: Kyren 72%, 10 car (first play of game was a Kyren run); Corum 28%, 9 car.
- Wk7 @LV: Kyren 51%, 16 car 99 yds; Corum 44%, 17 car 93 yds (first drive was 3 passes, no RB touch).
**Verdict: Kyren Williams is still the starter** (took the first RB touch in every game where one came on drive 1, and led snaps every week). Corum's role is growing fast: snaps 15→27→28→44% and he out-carried Kyren 17-16 last week. Treat it as a near-split committee going forward; no Rams RB leg passed the gates (Kyren rush+rec failed L4 hit gate).

## Leg cards
### A1. Puka Nacua - Receiving Yds 70+ @ -290 (FD main: [91.5, -113])
- Game: LA vs LAC, spread LA -6.5, total 45.5. Status: active (not on report). Raw: leg_Puka_Nacua_recyds.json
- Opportunity (src1 ESPN box L4): 10-04 12tg/9rec/125yd/1car/2ru; 10-12 24tg/17rec/138yd/2car/9ru; 10-18 7tg/6rec/80yd/0car/0ru; 10-25 10tg/8rec/68yd/2car/10ru
- Opportunity (src2 nflverse): season tgt share 32%, L3 36%; carry share 4% (L3 5%); 12.4 tgt/g, 1.0 car/g; snaps L3 87% (60% gate PASS); last-4 snap%: [0.9, 0.85, 0.9, 0.85]
- L4 values vs rung: [125, 138, 80, 68] -> 3/4 cleared.
- Coverage/scheme (LAC, Sharp via LAC_at_LAR.md): Man/Zone/MOFC/MOFO % = MISSING; YPT WR/TE/RB 8.9 / 9.1 / 4.5 (rank 8 / 3 / 23); Outside/Slot 10.2 / 7.4 (rank 4 / 22); blitz ['21.7 / 27.0 (rank 30 (1 = most blitz))'].
- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): T.Still 9 rec/95 yds; C.Hart 8 rec/107 yds; G.Smith 6 rec/81 yds
- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): MISSING
- Team allowed/g: WR 15.0 / 10.3 / 132.8 (rank yds 25); TE 6.3 / 4.7 / 57.5 (rank rec 24, yds 13); RB rec 5.7 / 3.8 / 25.7 (rank rec 24); RB rush 25.0 / 104.8, 4.19 (rank ypc 13). Soft: ['soft for outside WRs', 'soft for TEs']; Hard: - None flagged.
- 3rd-down / RZ TD% allowed: 31.1 / 53.3 (30) (rank 27 / 25). EPA/play allowed: -0.036 (rank 21)
- Injuries: LAC: S Derwin James OUT, CB Deane Leonard OUT, G Awosika OUT (helps LAR passing); LAR: TE Parkinson Q, LS Cardona D
- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.
- Weather: indoor/roof (no weather factor)
- Sims (100k each): MC 0.638 (median 85.4), Bias 0.787 (median 88.2), GameRand 0.819 (median 89.4, P(team leads) 0.731). De-vigged FD 0.712. Matchup factor 0.949.
- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS (active (not on report)) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps 87%, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS (3/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+3.6 pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.

### A2. CeeDee Lamb - Receiving Yds 60+ @ -280 (FD main: [80.5, -113])
- Game: DAL vs ARI, spread DAL -7, total 54.5. Status: active (not on report). Raw: leg_CeeDee_Lamb_recyds.json
- Opportunity (src1 ESPN box L4): 10-04 21tg/17rec/189yd/1car/-6ru; 10-08 5tg/2rec/9yd/0car/0ru; 10-18 18tg/9rec/70yd/0car/0ru; 10-26 12tg/5rec/74yd/0car/0ru
- Opportunity (src2 nflverse): season tgt share 31%, L3 29%; carry share 1% (L3 0%); 11.9 tgt/g, 0.3 car/g; snaps L3 75% (60% gate PASS); last-4 snap%: [0.86, 0.57, 0.88, 0.81]
- L4 values vs rung: [189, 9, 70, 74] -> 3/4 cleared.
- Coverage/scheme (ARI, Sharp via ARI_at_DAL.md): Man/Zone/MOFC/MOFO % = MISSING; YPT WR/TE/RB 9.7 / 8.2 / 6.7 (rank 2 / 6 / 8); Outside/Slot 11.3 / 9.9 (rank 1 / 10); blitz ['25.4 / 30.5 (rank 20 (1 = most blitz))'].
- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): B.Baker 10 rec/126 yds; M.Melton 6 rec/80 yds; D.Burke 5 rec/43 yds
- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): MISSING
- Team allowed/g: WR 15.7 / 9.4 / 141.1 (rank yds 19); TE 7.4 / 5.7 / 59.7 (rank rec 13, yds 11); RB rec 4.7 / 3.1 / 31.4 (rank rec 31); RB rush 24.3 / 103.6, 4.26 (rank ypc 10). Soft: ['soft for outside WRs', 'soft for volume WRs (capped boost)', 'soft for TEs', 'soft for rush-receive RBs']; Hard: - None flagged.
- 3rd-down / RZ TD% allowed: 39.7 / 75.8 (33) (rank 18 / 4). EPA/play allowed: +0.095 (rank 6)
- Injuries: ARI: DT Walter Nolen OUT, G Gaines OUT; DAL: Turpin OUT (more Lamb targets), Pickens Q (if he sits, Lamb gains)
- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.
- Weather: indoor/roof (no weather factor)
- Sims (100k each): MC 0.792 (median 92.4), Bias 0.681 (median 78.4), GameRand 0.764 (median 90.9, P(team leads) 0.746). De-vigged FD 0.705. Matchup factor 1.008.
- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS (active (not on report)) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps 75%, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS (3/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+4.1 pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.
- FLAG: Lamb 60+ yds is already on placed FD SGP Ticket 2 - skill sec.11 bars a player on two slips; Rico/Ghost6 decide

### A3. Trey McBride - Receptions 7+ @ -225 (FD main: [7.5, -122])
- Game: ARI vs DAL, spread ARI +7, total 54.5. Status: active (not on report). Raw: leg_Trey_McBride_rec.json
- Opportunity (src1 ESPN box L4): 10-04 12tg/7rec/31yd/0car/0ru; 10-11 10tg/9rec/66yd/0car/0ru; 10-18 9tg/7rec/53yd/0car/0ru; 10-25 13tg/10rec/111yd/0car/0ru
- Opportunity (src2 nflverse): season tgt share 29%, L3 26%; carry share 0% (L3 0%); 11.1 tgt/g, 0.0 car/g; snaps L3 93% (60% gate PASS); last-4 snap%: [0.97, 0.9, 0.97, 0.93]
- L4 values vs rung: [7, 9, 7, 10] -> 4/4 cleared.
- Coverage/scheme (DAL, Sharp via ARI_at_DAL.md): Man/Zone/MOFC/MOFO % = MISSING; YPT WR/TE/RB 9.0 / 7.7 / 4.5 (rank 6 / 9 / 23); Outside/Slot 7.4 / 11.8 (rank 28 / 1); blitz ['23.0 / 26.3 (rank 24 (1 = most blitz))'].
- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): D.Winters 4 rec/26 yds; C.Downs 4 rec/35 yds; M.Hooker 4 rec/46 yds
- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): MISSING
- Team allowed/g: WR 18.1 / 11.9 / 163.1 (rank yds 9); TE 6.4 / 5.1 / 46.6 (rank rec 17, yds 18); RB rec 5.0 / 4.0 / 22.7 (rank rec 20); RB rush 24.4 / 106.6, 4.36 (rank ypc 8). Soft: ['soft for slot', 'soft for volume WRs (capped boost)']; Hard: - Hard outside: Sharp outside YPT 7.4 (rank 28/32)
- 3rd-down / RZ TD% allowed: 52.9 / 67.7 (31) (rank 1 / 12). EPA/play allowed: +0.138 (rank 1)
- Injuries: DAL: LB Dee Winters OUT (coverage LB - helps TE); ARI: G Gaines OUT, TE Reiman OUT (McBride share up)
- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.
- Weather: indoor/roof (no weather factor)
- Sims (100k each): MC 0.650 (median 8.0), Bias 0.668 (median 8.0), GameRand 0.932 (median 8.0, P(team leads) 0.254). De-vigged FD 0.662. Matchup factor 0.932.
- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS (active (not on report)) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps 93%, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS (4/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+8.8 pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.

### A4. Brock Bowers - Receptions 6+ @ -158 (FD main: [5.5, -154])
- Game: LV vs NYJ, spread LV +1.5, total 45.5. Status: active (not on report). Raw: leg_Brock_Bowers_rec.json
- Opportunity (src1 ESPN box L4): 10-04 11tg/6rec/86yd/0car/0ru; 10-11 10tg/8rec/110yd/0car/0ru; 10-18 9tg/4rec/70yd/0car/0ru; 10-25 8tg/6rec/73yd/0car/0ru
- Opportunity (src2 nflverse): season tgt share 26%, L3 23%; carry share 0% (L3 0%); 10.4 tgt/g, 0.0 car/g; snaps L3 84% (60% gate PASS); last-4 snap%: [0.82, 0.7, 0.98, 0.84]
- L4 values vs rung: [6, 8, 4, 6] -> 3/4 cleared.
- Coverage/scheme (NYJ, Sharp via LV_at_NYJ.md): Man/Zone/MOFC/MOFO % = MISSING; YPT WR/TE/RB 7.6 / 7.3 / 4.4 (rank 20 / 13 / 25); Outside/Slot 8.0 / 8.1 (rank 16 / 17); blitz ['40.0 / 38.4 (rank 4 (1 = most blitz))'].
- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): D.Belton 9 rec/90 yds; A.Thomas 5 rec/53 yds; D.Davis 5 rec/60 yds
- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): MISSING
- Team allowed/g: WR 17.4 / 10.7 / 133.3 (rank yds 23); TE 6.6 / 4.7 / 48.0 (rank rec 21, yds 17); RB rec 4.9 / 3.4 / 21.6 (rank rec 26); RB rush 26.1 / 106.6, 4.08 (rank ypc 20). Soft: none; Hard: - None flagged.
- 3rd-down / RZ TD% allowed: 38.2 / 60.7 (28) (rank 21 / 18). EPA/play allowed: -0.002 (rank 18)
- Injuries: NYJ: DT Sweat OUT, DE Ossai OUT, LB Bailey D, OT Max Mitchell OUT (NYJ side); LV: DE P.Johnson OUT
- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.
- Weather: 61F, wind 3 mph (gust 5), precip 0% @kick (Open-Meteo, pulled now)
- Sims (100k each): MC 0.629 (median 6.0), Bias 0.636 (median 6.0), GameRand 0.756 (median 7.0, P(team leads) 0.443). De-vigged FD 0.586. Matchup factor 0.96.
- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS (active (not on report)) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps 84%, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS (3/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+8.8 pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.

### A5. DK Metcalf - Receiving Yds 40+ @ -225 (FD main: [52.5, -113])
- Game: PIT vs CLE, spread PIT -3.5, total 39.5. Status: active (not on report). Raw: leg_DK_Metcalf_recyds.json
- Opportunity (src1 ESPN box L4): 10-01 9tg/5rec/115yd/0car/0ru; 10-11 4tg/3rec/12yd/1car/11ru; 10-18 15tg/11rec/93yd/0car/0ru; 10-25 6tg/2rec/56yd/0car/0ru
- Opportunity (src2 nflverse): season tgt share 23%, L3 25%; carry share 1% (L3 1%); 8.3 tgt/g, 0.1 car/g; snaps L3 93% (60% gate PASS); last-4 snap%: [0.97, 0.92, 0.95, 0.92]
- L4 values vs rung: [115, 12, 93, 56] -> 3/4 cleared.
- Coverage/scheme (CLE, Sharp via CLE_at_PIT.md): Man/Zone/MOFC/MOFO % = MISSING; YPT WR/TE/RB 8.0 / 6.1 / 4.0 (rank 19 / 23 / 29); Outside/Slot 7.6 / 9.8 (rank 24 / 12); blitz ['25.6 / 23.7 (rank 19 (1 = most blitz))'].
- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): D.Ward 10 rec/103 yds; R.Hickman 10 rec/134 yds; C.Schwesinger 9 rec/102 yds
- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): MISSING
- Team allowed/g: WR 19.0 / 11.0 / 151.4 (rank yds 12); TE 8.1 / 5.6 / 49.3 (rank rec 15, yds 16); RB rec 5.1 / 3.9 / 20.0 (rank rec 23); RB rush 22.6 / 104.0, 4.61 (rank ypc 5). Soft: ['good RB rushing environment']; Hard: - None flagged.
- 3rd-down / RZ TD% allowed: 39.0 / 57.7 (26) (rank 20 / 23). EPA/play allowed: -0.037 (rank 22)
- Injuries: CLE: none listed; PIT: CB Slaughter, CB Echols OUT (defense - longer CLE drives); WR Skowronek Q
- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.
- Weather: 59F, wind 4 mph (gust 12), precip 6% @kick (Open-Meteo, pulled now)
- Sims (100k each): MC 0.768 (median 57.8), Bias 0.676 (median 52.3), GameRand 0.722 (median 55.4, P(team leads) 0.631). De-vigged FD 0.662. Matchup factor 1.081.
- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS (active (not on report)) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps 93%, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS (3/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+5.9 pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.

### A6. Jahmyr Gibbs - Rushing Yds 70+ @ -250 (FD main: [87.5, -113])
- Game: DET vs MIN, spread DET -3, total 46.5. Status: active (not on report). Raw: leg_Jahmyr_Gibbs_rushyds.json
- Opportunity (src1 ESPN box L4): 09-27 8tg/7rec/65yd/20car/99ru; 10-04 7tg/4rec/31yd/15car/46ru; 10-11 6tg/5rec/56yd/25car/151ru; 10-25 6tg/5rec/27yd/29car/116ru
- Opportunity (src2 nflverse): season tgt share 18%, L3 17%; carry share 84% (L3 87%); 6.7 tgt/g, 22.3 car/g; snaps L3 82% (60% gate PASS); last-4 snap%: [0.69, 0.87, 0.7, 0.9]
- L4 values vs rung: [99, 46, 151, 116] -> 3/4 cleared.
- Coverage/scheme (MIN, Sharp via MIN_at_DET.md): Man/Zone/MOFC/MOFO % = MISSING; YPT WR/TE/RB 7.3 / 6.1 / 3.9 (rank 23 / 23 / 30); Outside/Slot 8.0 / 6.1 (rank 16 / 28); blitz ['68.4 / 71.4 (rank 1 (1 = most blitz))'].
- Defender matchup: individual CB/S allowed = **MISSING (paid)**. PBP proxy (defender named on completions to his position, Wk1-7): I.Rodgers 4 rec/12 yds; B.Murphy 3 rec/10 yds; B.Cashman 3 rec/27 yds
- Explosives allowed/g (WR20+, TE20+, RB10+run, RB20+rec, stuffs): MISSING
- Team allowed/g: WR 17.0 / 9.8 / 123.8 (rank yds 28); TE 6.3 / 3.0 / 38.8 (rank rec 32, yds 28); RB rec 4.5 / 3.2 / 18.2 (rank rec 30); RB rush 20.7 / 83.8, 4.06 (rank ypc 21). Soft: none; Hard: - Hard slot: Sharp slot YPT 6.1 (rank 28/32)
- 3rd-down / RZ TD% allowed: 28.2 / 33.3 (18) (rank 30 / 32). EPA/play allowed: -0.193 (rank 32)
- Injuries: MIN: none listed; DET: S Kerby Joseph OUT (defense)
- Routes: NGS route-tendency % MISSING (public charts are targeted-route images only). Area read uses Sharp outside/slot YPT above.
- Weather: indoor/roof (no weather factor)
- Sims (100k each): MC 0.765 (median 87.9), Bias 0.686 (median 84.8), GameRand 0.778 (median 97.2, P(team leads) 0.613). De-vigged FD 0.683. Matchup factor 0.944.
- Phase checklist (PHASE_SCRIPT + skill): P0 injury PASS (active (not on report)) | P1 role lock PASS | P2 coverage profile PASS (team) / defender-level MISSING | P3 environment PASS (spread/total above) | P4 opportunity gate PASS (snaps 82%, share above) | P5 role grade PASS (no Hard spot in his area) | P6 triggers checked | P7 recent env PASS (3/4) | P8 projection = model medians > rung PASS | P9 three-model PASS (all >=0.60) | P10-11 FD line + edge PASS (+6.0 pts vs de-vig) | Skill s.14 cushion/catch rules checked by rung choice | NGS routes MISSING | Outlier/PropsMadness MISSING | 11:30 AM inactives recheck REQUIRED.
- FLAG: Gibbs (5+ rec) is already on placed FD SGP Ticket 2 - same-player conflict; Rico/Ghost6 decide

## Anytime TDs
None built (separate section reserved; not requested in the gate pass).

## Cuts (35 of 41 candidate props)
- Puka Nacua Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Amon-Ra St. Brown Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Amon-Ra St. Brown Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- CeeDee Lamb Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Trey McBride Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Zay Flowers Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Zay Flowers Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Drake London Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Drake London Receiving Yds: HARD area cut: TB defense flagged "Hard vs WRs overall" (Sharp WR YPT 7.2, rank 25/32) - over into a strength (skill sec.8)
- Brock Bowers Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Tee Higgins Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Garrett Wilson Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Tyler Warren Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Chris Godwin Jr. Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Justin Jefferson Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Jahmyr Gibbs Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- James Cook Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- James Cook Rushing Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Braelon Allen Rush+Rec Yds: no logs or no FD ladder
- Bijan Robinson Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Bijan Robinson Rushing Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Jonathan Taylor Rushing Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Jonathan Taylor Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Kenneth Walker III Rushing Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Javonte Williams Rushing Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Ashton Jeanty Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Jaylen Warren Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Kyren Williams Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Chase Brown Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Tony Pollard Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Aaron Jones Rushing Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Bucky Irving Rush+Rec Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Braelon Allen Rushing Yds: no logs or no FD ladder
- Dallas Goedert Receptions: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD
- Parker Washington Receiving Yds: no rung passing: price -300..-120, L4 hits>=3, all 3 model medians>=line & p>=60%, consensus 65-82%, edge 3-15pt vs de-vigged FD

## Follow-up (Sat ~7:05 PM ET): name-match fix via ESPN athlete IDs (Cook 4379399 'James Cook III', A. Jones 3042519 'Aaron Jones Sr.', B. Allen 4685247, Godwin 3116165; FD lists Godwin as 'Chris Godwin')
All re-graded through the same gates/three 100k sims (rungs_eval in leg_*.json, sims_summary.csv). Phase checklist: P0 injury PASS (none on report), P1 role PASS, P4 opportunity PASS (snaps L3: Cook 62%, Jones 62%, Allen 84%, Godwin 84%), then failures at P9-P11:
- James Cook rush yds (main 82.5 -113). L4 rushing 135/154/75/111, 71% L3 carry share. 80+ @ -130: MC .730 / Bias .661 / GR .760 (avg .717) vs de-vig .541 -> edge 17.6 pts > 15-pt model-overconfidence cap -> CUT. 70+ @ -210: avg .834 (above 82% mid-rung band) -> CUT. ALSO on placed Ticket 2 (Cook 70+ rush+rec) = same-player conflict.
- James Cook rush+rec 96.5 @ -113 (main only, no FD alt ladder): MC .647 / Bias .577 / GR .713 (avg .646) -> bias <60% and avg <65% -> CUT. Ticket 2 conflict.
- Aaron Jones rush yds: FD main is only 29.5 (-113) vs his 17-25 carry games; last game 8 car/26 yds. Models 94-98% at 30+, de-vig .51 -> edge far beyond cap: the market is pricing a role/health change our data doesn't show -> CUT pending news check (do not bet a model-vs-market gap this size).
- Braelon Allen rush yds: logs now matched (L4 14/24/17/17 car), but FanDuel has NO Braelon Allen rushing market posted -> line MISSING -> CUT.
- Chris Godwin receptions (main 4.5 +100). 4+ @ -225: MC .696 / Bias .641 / GR .735 (avg .691) vs de-vig .663 -> edge 2.8 pts < 3 -> CUT (L4 catches 6/3/4/4). 5+ @ -102: avg .412 -> CUT. ALSO on placed Ticket 2 (Godwin 4+ rec) = conflict.
Result: no new passing legs; Group B still not formed.
## PropsMadness access check (Sat Oct 31, ~7:10 PM ET; no sign-in, no keys)
URL: https://propsmadness.com (NFL: https://propsmadness.com/nfl/props/<market>, e.g. /nfl/props/receiving-yards). Plain curl gets HTTP 200 on public pages and the robots.txt allows them. The server-rendered HTML includes player names and public lines/hit rates. Per its help center, sorting and filters, Man-vs-Zone and the Matchup Analyzer are Pro-only and need a login, which means a browser session. Not used for any leg here.

## Ticket 2 IS placed + real defender/route rule (Sat Oct 31, 7:20 PM ET)
- REMOVED: Lamb 60+ and Gibbs 70+ (both on placed Ticket 2). Also excluded: St. Brown, Godwin, London, Cook, Flowers and Pickens.
- Defender/route audit: betguru_2026-11-01_raw/coverage_routes/defender_route_audit.md
  - Nacua: PASS
  - Bowers: PASS
  - Metcalf: PASS, with Ward shadow risk
  - McBride: CUT (no public TE alignment or defender map)
- Puka vs Outlier: Outlier has LAC 7th vs WR yds and Puka at 40% of his last 5 over 91.5. Our 70+ rung is a different line: he cleared 70 in 4 of his last 5 (74, 125, 138, 80, 68). Sims .638 / .787 / .819 (avg .748) vs .712 de-vigged at -290. That is +3.6 points, the thinnest edge on the card, and the Monte Carlo sim is under 65%.
  - VERDICT: HOLD 70+ only as a low/mid rung; do not move up.
  - He was a DNP Friday (rest) and Donte Jackson is Q -> confirm at the 11:30 AM ET inactives.
- Replacements were re-run: no other non-Ticket-2 prop passed the price/sim/edge gates (Higgins, G. Wilson, Jefferson, P. Washington and others failed them earlier), so defender data cannot revive them.
- SURVIVING CARD: 3 legs -> no group of 6, so Groups A, B and C are NOT formed (no padding).
  - Nacua 70+ rec yds -290
  - Bowers 6+ rec -158
  - Metcalf 40+ rec yds -225
  - A 3-leg parlay would be about +217 (avg-sim product ~.36); listed only for reference, it is not a group.


## 10/31 ~8:15 PM ET — Full-slate rerun: three groups of six (8A HARD, film PENDING)
Defense-strength cuts: Jeudy 20+ (PIT hard vs WR), Dotson 20+ (TB hard vs WR), Worthy 20+ (DEN hard vs WR). 8A cuts: Flournoy 30+ yds, Jameson Williams 40+, Godwin 30+ yds, Worthy 3+ rec, Malik Washington 4+ rec. Snap/Q/RB-trail/no-alignment cuts as in the audit.
Every leg: route_type=PENDING_FILM, alignment=PENDING_FILM. Film gate: if film shows a shadow or role change that breaks the 8A mapping, cut the leg and re-run the group.

### Group 1 (value, ~-170 avg): +1346 (naive leg-price product; FD SGP repricing may differ), $125 bonus profit ≈ $1682.28, sim hit ≈ 0.138
- Tee Higgins Receptions 5+ -166 | sims [0.736, 0.774, 0.684] | Cordale Flott 9-6 66.7% 83y 9.2YPT 96.1 | TEN man16.5/zone77.2 MOFC45.6/MOFO51.2 | T2: none | 
- Brock Bowers Receptions 6+ -158 | sims [0.629, 0.636, 0.756] | D'Angelo Ponds (0 tgt, thin) / LB Sherwood 18-15 83.3% 163y 9.1 122.9 | NYJ man23.8/zone66.6 MOFC45.2/MOFO50.0 | T2: none | 
- Bhayshul Tuten Rushing Yds 60+ -158 | sims [0.654, 0.635, 0.768] | n/a rushing | IND | T2: none | JAX -10, carry share .65
- Laquon Treadwell Receiving Yds 20+ -178 | sims [0.694, 0.672, 0.835] | Travis Hunter as above | JAX same | T2: none | 
- Antonio Williams Receptions 3+ -200 | sims [0.654, 0.628, 0.781] | Q.Mitchell 20-13 65% 140y 7.0 64.6 (alignment mismatch: AW 50% slot) | PHI man15.1/zone72.8 MOFC49.1/MOFO43.4 | T2: none | defender map uncertain -> PENDING_FILM
- Josh Downs Receptions 3+ -225 | sims [0.778, 0.758, 0.89] | Jourdan Lewis 18-10 55.6% 108y 6.0 52.3 | JAX man21.0/zone73.4 MOFC46.0/MOFO51.1 | T2: none | 8A borderline comp%; cleared by 6.6 tgt/g

### Group 2 (higher hit, conditional): +908 (naive leg-price product; FD SGP repricing may differ), $125 bonus profit ≈ $1135.11, sim hit ≈ 0.158
- Jahmyr Gibbs Rushing Yds 70+ -250 | sims [0.765, 0.686, 0.778] | n/a rushing | MIN man5.3/zone86.5 MOFC31.6/MOFO61.2 | T2: T2 Gibbs 5+ rec (same player, positive correlation) | at -250 boundary
- Ryan Flournoy Receptions 3+ -240 | sims [0.765, 0.758, 0.87] | Garrett Williams 6-4 66.7% 21y 3.5YPT 72.2 | ARI man9.1/zone70.9 MOFC21.9/MOFO56.7 | T2: none | low-YPT CB -> rec only, yds cut
- DK Metcalf Receiving Yds 40+ -225 | sims [0.768, 0.676, 0.722] | Campbell 12-9 75% 179y 14.9 116.7; Ward shadow risk 25-10 40% 142y 5.7 82.0 | CLE man42.4/zone54.0 MOFC72.6/MOFO24.4 | T2: none | CONDITIONAL_FILM (fails 8A if Ward shadows)
- Puka Nacua Receiving Yds 70+ -290 | sims [0.638, 0.787, 0.819] | Donte Jackson(Q) 9-6 66.7% 69y 7.7 89.6 | LAC man10.6/zone58.0 MOFC33.9/MOFO40.7 | T2: none | LOW VALUE (<-250); conditional Puka + D.Jackson status 11:30 ET
- Tee Higgins Receptions 5+ -166 | sims [0.736, 0.774, 0.684] | Cordale Flott 9-6 66.7% 83y 9.2YPT 96.1 | TEN man16.5/zone77.2 MOFC45.6/MOFO51.2 | T2: none | 
- Brock Bowers Receptions 6+ -158 | sims [0.629, 0.636, 0.756] | D'Angelo Ponds (0 tgt, thin) / LB Sherwood 18-15 83.3% 163y 9.1 122.9 | NYJ man23.8/zone66.6 MOFC45.2/MOFO50.0 | T2: none | 

### Group 3 (mix): +888 (naive leg-price product; FD SGP repricing may differ), $125 bonus profit ≈ $1110.13, sim hit ≈ 0.176
- Laquon Treadwell Receptions 2+ -245 | sims [0.756, 0.726, 0.853] | Travis Hunter 19-12 63.2% 142y 7.5 63.9 | JAX same | T2: none | 
- Bhayshul Tuten Rushing Yds 60+ -158 | sims [0.654, 0.635, 0.768] | n/a rushing | IND | T2: none | JAX -10, carry share .65
- Josh Downs Receptions 3+ -225 | sims [0.778, 0.758, 0.89] | Jourdan Lewis 18-10 55.6% 108y 6.0 52.3 | JAX man21.0/zone73.4 MOFC46.0/MOFO51.1 | T2: none | 8A borderline comp%; cleared by 6.6 tgt/g
- Antonio Williams Receptions 3+ -200 | sims [0.654, 0.628, 0.781] | Q.Mitchell 20-13 65% 140y 7.0 64.6 (alignment mismatch: AW 50% slot) | PHI man15.1/zone72.8 MOFC49.1/MOFO43.4 | T2: none | defender map uncertain -> PENDING_FILM
- Jahmyr Gibbs Rushing Yds 70+ -250 | sims [0.765, 0.686, 0.778] | n/a rushing | MIN man5.3/zone86.5 MOFC31.6/MOFO61.2 | T2: T2 Gibbs 5+ rec (same player, positive correlation) | at -250 boundary
- Ryan Flournoy Receptions 3+ -240 | sims [0.765, 0.758, 0.87] | Garrett Williams 6-4 66.7% 21y 3.5YPT 72.2 | ARI man9.1/zone70.9 MOFC21.9/MOFO56.7 | T2: none | low-YPT CB -> rec only, yds cut

Film manifest: betguru_2026-11-01_raw/film/manifest.csv

---
## BetGuru Phase 5–10G final card — appended Sat Oct 31, 2026, ~8:30 PM ET (FD 7:37 PM ET snapshot; run runs/betguru_20261031T194324; write_card.py NOT run)

## 10G-7 FINAL CARD (only legs passing every gate; no padding)
Gates applied to each leg: G1 non-underdog (10G) · G2 MC & GR medians ≥ rung (bias median disclosed) · G3 edge vs FD no-vig ≥ +3 and ≤ +15 · G4 shrink-30 robustness ≥ +3 · G5 not a Ticket-2 exact prop · G6 walked Phases 1–4 · G7 weather/injury PASS (9A/9D) · film = GAP disclosed (never a pass) · receiving legs: PFR cache Oct 29 (fresh pull 403).

**Group 1 — 5 legs, 5 different games (not an SGP), ≈ +829 at 7:37 PM FD prices**
| # | Leg | FD | MC / Bias / GR | Avg | No-vig | Edge (shrink-30) | Class/weight | Flags |
|---|---|---|---|---|---|---|---|---|
| 1 | Gibbs 70+ rush yds (DET −3 vs MIN) | −250 | .812 / .701 / .750 | .754 | .673 | +8.1 (+6.3) | toss-up 0.85 | MIN #1 D EPA — ours may be optimistic; Ticket 2 has Gibbs rec (same player, flag) |
| 2 | Cook 70+ rush yds (BUF −3 vs BAL) | −210 | .774 / .654 / .736 | .722 | .638 | +8.3 (+3.6) | toss-up 0.85 | Ticket 2 Cook rushrec → correlated exposure (flag); BUF 9 giveaways L4 |
| 3 | Walker 80+ rush yds (KC −1.5 at DEN) | −144 | .730 / .616 / .688 | .678 | .556 | +12.2 (+6.1) | toss-up 0.85 | largest edge → treat as model-suspect-adjacent |
| 4 | Higgins 60+ rec yds (CIN −10 vs TEN) | −186 | .748 / .652 / .750 | .716 | .613 | +10.4 (+6.9) | blowout 1.00 | open FD SGP has Higgins 50+ (doubled exposure); Q4-sit risk; chart UNVERIFIED; spread −10 vs Ghost6 −12.5 |
| 5 | Puka 8+ rec (LAR −6.5 vs LAC) | −138 | .622 / .531 / .626 | .593 | .542 | +5.1 (+5.1) | moderate fav possession 1.00 | bias median 8 = rung; Adams IR not modeled |
Product of avg probs (different games, independence assumed, UNCALIBRATED) ≈ .157 vs book-implied ≈ .108. Caveat: 3 of 5 are RB rushing overs where our model already runs 10–20 yds above FD mains — model error is correlated across these legs.
Groups 2 and 3: **not built** — no further legs pass every gate (no padding).
Separate edges (requested, not on card): Gibbs 60+ rush −420 +8.1 ⚠bonus; Gibbs 50+ −800 +7.1 ⚠bonus; Lamb 5+ −440 −5.2 FAIL.

## 10G-8 Side by side vs Ghost6's card (~+735)
| Ghost6 leg | FD | Ghost6 avg | Ours avg | No-vig | Our edge | Our verdict |
|---|---|---|---|---|---|---|
| Flournoy 3+ rec | −240 | .660 | .674 | .660 | +1.3 | FAIL edge (also not walked by us) |
| Tuten 60+ rush | −158 | .565 | .572 | .577 | −0.5 | FAIL edge; bias median 59.5 < 60; JAX wind soft review |
| Metcalf 40+ yds | −225 | .609 | .534 | .652 | −11.8 | FAIL edge; bias median 38 |
| Puka 70+ yds | −290 | .668 | .629 | .701 | −7.2 | FAIL edge; ⚠bonus |
| A. Williams 3+ rec | −200 | .598 | .550 | .623 | −7.3 | FAIL edge |
| Gibbs 90+ rush+rec | not posted | .713 (fair −248) | .836 (fair ≈ −510) | — | GAP | UNPRICED → cannot pass |
Agree: underdog blocks (McBride, Bowers, Flowers, etc.); Lamb not a play; Gibbs is the strongest DET piece; Puka is LAR's best angle (we prefer catches 8+ over 70+ yds).
Disagree: none of Ghost6's 5 priced legs beats FD no-vig by 3 in our sims; Ghost6's card is a lower-variance, short-price build, while ours takes rushing overs with larger modeled (uncalibrated) edges.

---
## Morning refresh — Sun Nov 1, 2026, ~6:20 AM ET (FD sbapi pull 6:12 AM ET; run phase_walk/runs/betguru_refresh_20261101T0612; v4 corrected sims reused; write_card.py NOT run)
Rule: raw edge vs FD no-vig >= +3 (cap 15) and shrink-30 edge (p' = 0.5 + 0.7(p - 0.5)) > 0.

| Leg | FD 7:37 PM | FD 6:12 AM | Move | No-vig | v4 MC / Bias / GR | Avg | Raw edge | p' | Shrink edge | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| K. Walker 80+ rush (KC -1.5 @ DEN, 40.5) | -144 | -144 | none | .556 | .676 / .552 / .640 | .623 | +6.7 | .586 | +3.0 | PASS (CAUTION) |
| Puka 8+ rec (LAR -6.5 vs LAC, 45.5) | -138 | -140 | 2c (under 20c flag) | .545 | .622 / .531 / .626 | .593 | +4.8 | .565 | +2.0 | PASS |
| Gibbs 70+ rush (ref) | -250 | -250 | none | .673 | .786 / .668 / .723 | .726 | +5.2 | .658 | -1.5 | FAIL (no re-test, price unmoved) |
| Cook 70+ rush (ref) | -210 | -210 | none | .638 | .661 / .518 / .625 | .601 | -3.7 | .571 | -6.8 | FAIL (no re-test, price unmoved) |
Mains unchanged: Walker rush 85.5 (-113/-113), Walker rush+rec 107.5; Puka rec 7.5 (-138/+104); Puka 9+ +122. Spreads/totals unchanged (KC -1.5/40.5, LAR -6.5/45.5).
**Card: Walker 80+ (-144) + Puka 8+ (-140) ≈ +190** (1.694 × 1.714 = 2.905; was +192). Joint (independent, v4 avgs) .369 vs book no-vig ≈ .303. Uncalibrated.

Status (ESPN injuries API 6:15 AM ET + Running Back Roulette / FOX / EVAnalytics):
- Walker: no designation. KC RB room = Walker, Emmett Johnson (breather/3rd-down; 0 carries in 2 of last 3, ≤3 carries in 4 of 6), Jaydn Ott, FB VanSumeren; Brashard Smith IR. No split back. Watch: Wk7 14 carries at SEA; EVAnalytics notes carries prop bet down 19.5 -> 18.5 (Oct 27) and KC 36% run rate. §9 could-trail gate: Walker 27 tgt / 6 g = 4.5/g -> passes. KC: Rice, Kelce cleared; CB Delane OUT, Sneed IR (defense). DEN: RB RJ Harvey IR (Dobbins/Coleman), S Hufanga OUT; Q DE Zach Allen, S Brandon Jones, OT Bolles, WR Waddle.
- Puka: no designation. LAR WR/TE room: Davante Adams IR (hamstring surgery), Whittington Q (back), Parkinson Q (ribs), Ferguson IR -> concentration helps volume. LAR C Shelton Q, CB McDuffie Q (defense).
- LAC secondary (8A): Derwin James IR, CB Deane Leonard OUT, **CB Donte Jackson Q (hamstring)**. PFR (Oct 29 cache, fresh 403): Still 11-5 45.5% 6.5 YPT; D. Jackson 9-6 66.7% 7.7; Cam Hart 16-10 62.5% 10.4. LAC man 10.6 / zone 58.0, MOFC 33.9 / MOFO 40.7 (StatRankings/FTN, Oct 31); LAC blitz rank 30 (low). 8A = PASS-CAUTION. Film UNVERIFIED (no pbp match) -> GAP, not a pass.
- Weather: DEN outdoor, NWS hourly (game window 2-5 PM MT) 61-63F, SE/SSE 6-7 mph, precip 11-15%. No flag. SoFi indoor.

Correlation / exposure flags:
- Walker is already on Rico's PP $40 (rush 97.5 demon), UD $20 (rush 69.5), PP $20 (Walker+Kyren ATD combo) and FD 7-leg (Walker ATD, placed status unconfirmed). Adding Walker 80+ stacks one player across 5 tickets (§11). Positive correlation: one bad Walker game sinks all.
- Puka: on UD $20 (rec yds 69.5); Stafford completions 22.5 on two PP slips correlate positively with Puka 8+. Kyren ATD legs (PP $25, FD 7-leg) mildly negative to Puka volume in a LAR blowout.
- Ticket 2 ($63 FD 8-leg): no overlap with Walker/Puka.
- Bonus profit-only: neither leg shorter than -250. OK.

11:30 AM ET inactives check (and 2:35 PM, both games 4:05/4:25): Donte Jackson (LAC CB, Puka 8A), Whittington + Parkinson (LAR), Zach Allen + Brandon Jones + Bolles + Waddle (DEN), McDuffie (LAR). Drop Walker if KC actives news shows a split; drop Puka if downgraded. Reprice on a 20c move.
