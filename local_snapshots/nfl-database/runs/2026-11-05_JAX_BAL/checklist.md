# Checklist — TNF JAX @ BAL, 2026-11-05 20:15 ET (week 9) — run 2026-11-05_JAX_BAL

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|-----|-------|------|--------|--------|-------------|
| Lawrence rush yds U12.5 | 1 Data pull | PASS | last-4 w/ current QB (T.Lawrence): [2.0, 25.0, 12.0, 10.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Lawrence rush yds U12.5 | 2 Opportunity | PASS | 31.4 db/g x 4.1% own scramble x 5.89 yd + 1.14 designed x 3.75 - kneels = 11.0 < 12.5; FLAG SCRAMBLE_CONFLICT: BAL allows 7.3% (lg 4.8%) -> adj 6.2% -> 14.8 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Lawrence rush yds U12.5 | 3 Defensive profile | PASS | BAL D: rush 102.8/g, RB YPC 3.727 (lg 4.16), pass 241.9/g, WR YPT 9.17 (n155), TE 7.44, rec20+ 24, rush15+ 10, scramble 7.3% (lg 4.8%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Lawrence rush yds U12.5 | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| Lawrence rush yds U12.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% (L4 36.0%), press PROXY 24.1%; Lawrence TTT 2.75 s; checkdown 21.2%; tgt under press PROXY {'J.Meyers': 7, 'P.Washington': 6, 'B.Strange': 2, 'Bri.Thomas': 2, 'L.Allen': 2, 'B.Tuten': 2, 'C.Rodriguez': 1} n23 LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Lawrence rush yds U12.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Lawrence rush yds U12.5 | 7 Role/RB rules + §7 | PASS | §7 under 12.5: [2.0, 25.0, 12.0, 10.0] = 3/4; last-2 [12.0, 10.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Lawrence rush yds U12.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Lawrence rush yds U12.5 | 9 Next Gen Stats | PASS | Lawrence TTT 2.75 s, intended air 8.9 (198 att) | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Lawrence rush yds U12.5 | 10 Film | PASS | 2026_06_HOU_JAX play 292, Q1 11:08, T.Lawrence scrambles up the middle to JAX 49 for 4 yards; 2026_05_PHI_JAX play 3937, Q4 10:30, 3rd-and-4, T.Lawrence scrambles left guard for 16 | official NFL YouTube captions matched to pbp (film_verified.json) | 2026-11-05 16:48 |
| Lawrence rush yds U12.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Lawrence rush yds U12.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Lawrence rush yds U12.5 | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Lawrence rush yds U12.5 | 14 Models/price/edge | PASS | MC p 0.636 med 8.0; Bias p 0.640 med 8.0; GR p 0.638 med 8.2; FD 12.5 -113, no-vig 0.500 (Pin 0.5) -> edge +13.8 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Lawrence rush yds U12.5 | 15 Inactives | PASS | Official inactives posted ~18:52 ET. Lawrence ACTIVE. JAX: Tuten+Travon Walker ACTIVE (were Q); BAL: Wiggins INACTIVE (illness), Hawkins OUT, Slovis/Sarratt/E.Jones/Peebles inactive. Fagnano starts (Reed No.2). FD Lawrence rush still 12.5 -113/-113 (no >0.5yd/20¢ move). NWS kickoff precip 76% WEATHER FLAG holds (rush under OK). No placed TNF tickets. | @JaguarsPR/@Ravens + ESPN summary 401873037 + Odds API odds_p15_1855.csv + NWS hourly | 2026-11-05 18:56 |
| Henry rush yds U71.5 | 1 Data pull | PASS | last-4 w/ current QB (J.Fagnano): [53.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Henry rush yds U71.5 | 2 Opportunity | PASS | Fagnano wk8: Henry 11 of 16 RB car (69%), 53 yd; wk7 17 car 45 yd; at 15-17 car x JAX RB YPC 3.29 = 49-56 < 71.5 (car range is an assumption, trailing script) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Henry rush yds U71.5 | 3 Defensive profile | PASS | JAX D: rush 77.4/g, RB YPC 3.285 (elite), WR YPT 9.72, TE 4.81, RB catch 0.822 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Henry rush yds U71.5 | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| Henry rush yds U71.5 | 5 Pressure/blitz | PASS | JAX blitz 30.4%, press PROXY 21.5%; Fagnano TTT 2.86 s (21 att), sack rate 12% LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Henry rush yds U71.5 | 6 QB grade card | FAIL | Fagnano 25 dropbacks: INCOMPLETE card (LOW-SAMPLE) -> backup-QB WEAK; dependent legs flagged | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Henry rush yds U71.5 | 7 Role/RB rules + §7 | MISSING | §7 needs 3 games with current QB Fagnano; have 1 ([53.0]) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Henry rush yds U71.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Henry rush yds U71.5 | 9 Next Gen Stats | PASS | Henry RYOE +0.11/att, 8+ box 31% (158 att) | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Henry rush yds U71.5 | 10 Film | UNVERIFIED | no caption-to-pbp match for this player | official NFL YouTube | 2026-11-04 15:37 |
| Henry rush yds U71.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Henry rush yds U71.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Henry rush yds U71.5 | 13 Game script/10G | PASS | BAL +9.5/+10 big underdog; under legs not underdog-blocked; Flip B (Henry volume in rain) flagged | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Henry rush yds U71.5 | 14 Models/price/edge | FAIL | MC p 0.763 med 53.7; Bias p 0.761 med 53.7; GR p 0.738 med 54.0; FD 71.5 -113, no-vig 0.500 (Pin None) -> edge +25.4 MODEL-SUSPECT | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Henry rush yds U71.5 | 15 Inactives | N/A | leg already CUT |  |  |
| Meyers rec yds U38.5 | 1 Data pull | PASS | last-4 w/ current QB (T.Lawrence): [33.0, 37.0, 83.0, 24.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Meyers rec yds U38.5 | 2 Opportunity | PASS | L3 w/ Lawrence 16/102 PA tgt (16%); at L4 avg 32.5 PA x .16 = 5.1 tgt x BAL WR YPT 9.17 = 47 > 38.5 (no room for under) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Meyers rec yds U38.5 | 3 Defensive profile | PASS | BAL D: rush 102.8/g, RB YPC 3.727 (lg 4.16), pass 241.9/g, WR YPT 9.17 (n155), TE 7.44, rec20+ 24, rush15+ 10, scramble 7.3% (lg 4.8%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Meyers rec yds U38.5 | 4 Defender coverage | PASS | Marlon Humphrey 42 tgt 59.5% 8.5 YPT (P); Nate Wiggins 36 tgt 55.6% 6.1 YPT (P); Kyle Hamilton 34 tgt 70.6% 6.0 YPT; BAL man 15.9/zone 77.7, MOF open 59.5 (SR agrees) | PFR advanced defense (week10/bal_secondary/defender_table.csv) | 2026-11-04 07:05 |
| Meyers rec yds U38.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% (L4 36.0%), press PROXY 24.1%; Lawrence TTT 2.75 s; checkdown 21.2%; tgt under press PROXY {'J.Meyers': 7, 'P.Washington': 6, 'B.Strange': 2, 'Bri.Thomas': 2, 'L.Allen': 2, 'B.Tuten': 2, 'C.Rodriguez': 1} n23 LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Meyers rec yds U38.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Meyers rec yds U38.5 | 7 Role/RB rules + §7 | PASS | §7 under 38.5: [33.0, 37.0, 83.0, 24.0] = 3/4; last-2 [83.0, 24.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Meyers rec yds U38.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Meyers rec yds U38.5 | 9 Next Gen Stats | PASS | Meyers sep 3.12, cushion 7.7, IAY 12.0 | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Meyers rec yds U38.5 | 10 Film | PASS | 2026_05_PHI_JAX play 1690, Q2 5:24, T.Lawrence pass short middle to J.Meyers for 18 yards | official NFL YouTube captions matched to pbp (film_verified.json) | 2026-11-05 16:48 |
| Meyers rec yds U38.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Meyers rec yds U38.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Meyers rec yds U38.5 | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Meyers rec yds U38.5 | 14 Models/price/edge | FAIL | MC p 0.466 med 41.5; Bias p 0.466 med 41.5; GR p 0.492 med 40.3; FD 38.5 -113, no-vig 0.500 (Pin 0.49031841652323577) -> edge -2.5 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Meyers rec yds U38.5 | 15 Inactives | N/A | leg already CUT |  |  |
| Strange rec yds O32.5 | 1 Data pull | PASS | last-4 w/ current QB (T.Lawrence): [95.0, 68.0, 44.0, 55.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange rec yds O32.5 | 2 Opportunity | PASS | L4 tgt [8,8,7,2] of PA [28,41,41,20] (19%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange rec yds O32.5 | 3 Defensive profile | PASS | BAL D: rush 102.8/g, RB YPC 3.727 (lg 4.16), pass 241.9/g, WR YPT 9.17 (n155), TE 7.44, rec20+ 24, rush15+ 10, scramble 7.3% (lg 4.8%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange rec yds O32.5 | 4 Defender coverage | PASS | Malaki Starks 20 tgt 85.0% 12.2 YPT (P); Kyle Hamilton 34 tgt 70.6% 6.0 YPT (P); BAL man 15.9/zone 77.7, MOF open 59.5 (SR agrees) | PFR advanced defense (week10/bal_secondary/defender_table.csv) | 2026-11-04 07:05 |
| Strange rec yds O32.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% (L4 36.0%), press PROXY 24.1%; Lawrence TTT 2.75 s; checkdown 21.2%; tgt under press PROXY {'J.Meyers': 7, 'P.Washington': 6, 'B.Strange': 2, 'Bri.Thomas': 2, 'L.Allen': 2, 'B.Tuten': 2, 'C.Rodriguez': 1} n23 LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Strange rec yds O32.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange rec yds O32.5 | 7 Role/RB rules + §7 | PASS | §7 over 32.5: [95.0, 68.0, 44.0, 55.0] = 4/4; last-2 [44.0, 55.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange rec yds O32.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Strange rec yds O32.5 | 9 Next Gen Stats | PASS | Strange sep 3.39, IAY 7.8 | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Strange rec yds O32.5 | 10 Film | PASS | Strange Q2 11:33 nine yards (play 1151) | official NFL YouTube captions matched to pbp (film_verified.json) | 2026-11-04 15:37 |
| Strange rec yds O32.5 | 11 Environment | FAIL | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5 -> receiving OVER cut | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Strange rec yds O32.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Strange rec yds O32.5 | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Strange rec yds O32.5 | 14 Models/price/edge | PASS | MC p 0.622 med 41.0; Bias p 0.621 med 41.9; GR p 0.574 med 38.9; FD 32.5 -113, no-vig 0.500 (Pin 0.5021645958699511) -> edge +10.5 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Strange rec yds O32.5 | 15 Inactives | N/A | leg already CUT |  |  |
| Strange 4+ rec (O3.5) | 1 Data pull | PASS | last-4 w/ current QB (T.Lawrence): [7, 7, 5, 2] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange 4+ rec (O3.5) | 2 Opportunity | PASS | L4 tgt [8,8,7,2] of PA [28,41,41,20] (19%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange 4+ rec (O3.5) | 3 Defensive profile | PASS | BAL D: rush 102.8/g, RB YPC 3.727 (lg 4.16), pass 241.9/g, WR YPT 9.17 (n155), TE 7.44, rec20+ 24, rush15+ 10, scramble 7.3% (lg 4.8%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange 4+ rec (O3.5) | 4 Defender coverage | PASS | Malaki Starks 20 tgt 85.0% 12.2 YPT (P); Kyle Hamilton 34 tgt 70.6% 6.0 YPT (P); BAL man 15.9/zone 77.7, MOF open 59.5 (SR agrees) | PFR advanced defense (week10/bal_secondary/defender_table.csv) | 2026-11-04 07:05 |
| Strange 4+ rec (O3.5) | 5 Pressure/blitz | PASS | BAL blitz 33.3% (L4 36.0%), press PROXY 24.1%; Lawrence TTT 2.75 s; checkdown 21.2%; tgt under press PROXY {'J.Meyers': 7, 'P.Washington': 6, 'B.Strange': 2, 'Bri.Thomas': 2, 'L.Allen': 2, 'B.Tuten': 2, 'C.Rodriguez': 1} n23 LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Strange 4+ rec (O3.5) | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange 4+ rec (O3.5) | 7 Role/RB rules + §7 | PASS | §7 over 3.5: [7, 7, 5, 2] = 3/4; last-2 [5, 2] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Strange 4+ rec (O3.5) | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Strange 4+ rec (O3.5) | 9 Next Gen Stats | PASS | Strange sep 3.39, IAY 7.8 | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Strange 4+ rec (O3.5) | 10 Film | PASS | Strange Q2 11:33 nine yards (play 1151) | official NFL YouTube captions matched to pbp (film_verified.json) | 2026-11-04 15:37 |
| Strange 4+ rec (O3.5) | 11 Environment | FAIL | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5 -> receiving OVER cut | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Strange 4+ rec (O3.5) | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Strange 4+ rec (O3.5) | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Strange 4+ rec (O3.5) | 14 Models/price/edge | PASS | MC p 0.562 med 4.0; Bias p 0.562 med 4.0; GR p 0.526 med 4.0; FD 3.5 +102, no-vig 0.462 (Pin 0.5) -> edge +8.8 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Strange 4+ rec (O3.5) | 15 Inactives | N/A | leg already CUT |  |  |
| Washington rec yds O60.5 | 1 Data pull | PASS | last-4 w/ current QB (T.Lawrence): [7.0, 124.0, 64.0, 16.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Washington rec yds O60.5 | 2 Opportunity | FAIL | L4 tgt [3,9,11,2], yds [7,124,64,16] (median 40 < 60.5); volatile role | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Washington rec yds O60.5 | 3 Defensive profile | PASS | BAL D: rush 102.8/g, RB YPC 3.727 (lg 4.16), pass 241.9/g, WR YPT 9.17 (n155), TE 7.44, rec20+ 24, rush15+ 10, scramble 7.3% (lg 4.8%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Washington rec yds O60.5 | 4 Defender coverage | PASS | Kyle Hamilton 34 tgt 70.6% 6.0 YPT (P); Marlon Humphrey 42 tgt 59.5% 8.5 YPT (P); BAL man 15.9/zone 77.7, MOF open 59.5 (SR agrees) | PFR advanced defense (week10/bal_secondary/defender_table.csv) | 2026-11-04 07:05 |
| Washington rec yds O60.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% (L4 36.0%), press PROXY 24.1%; Lawrence TTT 2.75 s; checkdown 21.2%; tgt under press PROXY {'J.Meyers': 7, 'P.Washington': 6, 'B.Strange': 2, 'Bri.Thomas': 2, 'L.Allen': 2, 'B.Tuten': 2, 'C.Rodriguez': 1} n23 LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Washington rec yds O60.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Washington rec yds O60.5 | 7 Role/RB rules + §7 | FAIL | §7 over 60.5: [7.0, 124.0, 64.0, 16.0] = 2/4; last-2 [64.0, 16.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Washington rec yds O60.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Washington rec yds O60.5 | 9 Next Gen Stats | PASS | Washington sep 2.08, IAY 12.6, YAC+ 1.10 | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Washington rec yds O60.5 | 10 Film | PASS | Washington Q2 3:57 sixteen yards / QB hit (play 1711) | official NFL YouTube captions matched to pbp (film_verified.json) | 2026-11-04 15:37 |
| Washington rec yds O60.5 | 11 Environment | FAIL | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5 -> receiving OVER cut | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Washington rec yds O60.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Washington rec yds O60.5 | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Washington rec yds O60.5 | 14 Models/price/edge | PASS | MC p 0.455 med 54.9; Bias p 0.453 med 54.9; GR p 0.446 med 54.1; FD 60.5 -113, no-vig 0.500 (Pin None) -> edge -4.8 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Washington rec yds O60.5 | 15 Inactives | N/A | leg already CUT |  |  |
| Flowers rec U4.5 | 1 Data pull | PASS | last-4 w/ current QB (J.Fagnano): [0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Flowers rec U4.5 | 2 Opportunity | MISSING | Fagnano sample 1 game (4-5 tgt, 0 rec); projection would rest on Lamar-era share | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Flowers rec U4.5 | 3 Defensive profile | PASS | JAX D: rush 77.4/g, RB YPC 3.285 (elite), WR YPT 9.72, TE 4.81, RB catch 0.822 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Flowers rec U4.5 | 4 Defender coverage | MISSING | JAX per-defender map not built (leg already cut on §7) | Sharp coverage schemes + StatRankings (firecrawl); PFR adv defense cache | 2026-11-05 16:42 |
| Flowers rec U4.5 | 5 Pressure/blitz | PASS | JAX blitz 30.4%, press PROXY 21.5%; Fagnano TTT 2.86 s (21 att), sack rate 12% LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Flowers rec U4.5 | 6 QB grade card | FAIL | Fagnano 25 dropbacks: INCOMPLETE card (LOW-SAMPLE) -> backup-QB WEAK; dependent legs flagged | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Flowers rec U4.5 | 7 Role/RB rules + §7 | MISSING | §7 needs 3 games with current QB Fagnano; have 1 ([0]) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Flowers rec U4.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Flowers rec U4.5 | 9 Next Gen Stats | PASS | Flowers sep 2.99, YAC+ 3.18 (Lamar-era) | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Flowers rec U4.5 | 10 Film | UNVERIFIED | no caption-to-pbp match for this player | official NFL YouTube | 2026-11-04 15:37 |
| Flowers rec U4.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Flowers rec U4.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Flowers rec U4.5 | 13 Game script/10G | PASS | BAL +9.5/+10 big underdog; under legs not underdog-blocked; Flip B (Henry volume in rain) flagged | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Flowers rec U4.5 | 14 Models/price/edge | PASS | MC p 0.262 med 6.0; Bias p 0.264 med 6.0; GR p 0.287 med 6.0; FD 4.5 -114, no-vig 0.500 (Pin 0.4956702459300312) -> edge -22.9 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Flowers rec U4.5 | 15 Inactives | N/A | leg already CUT |  |  |
| Tuten rush yds O (no line) | 1 Data pull | PASS | last-4 w/ current QB (T.Lawrence): [73.0, 72.0, 39.0, 104.0] | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Tuten rush yds O (no line) | 2 Opportunity | PASS | L4 car [17,22,12,16]; wx-boosted (x1.073) model median 61.6 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Tuten rush yds O (no line) | 3 Defensive profile | PASS | BAL D: rush 102.8/g, RB YPC 3.727 (lg 4.16), pass 241.9/g, WR YPT 9.17 (n155), TE 7.44, rec20+ 24, rush15+ 10, scramble 7.3% (lg 4.8%) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Tuten rush yds O (no line) | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| Tuten rush yds O (no line) | 5 Pressure/blitz | PASS | BAL blitz 33.3% (L4 36.0%), press PROXY 24.1%; Lawrence TTT 2.75 s; checkdown 21.2%; tgt under press PROXY {'J.Meyers': 7, 'P.Washington': 6, 'B.Strange': 2, 'Bri.Thomas': 2, 'L.Allen': 2, 'B.Tuten': 2, 'C.Rodriguez': 1} n23 LOW-SAMPLE | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Tuten rush yds O (no line) | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Tuten rush yds O (no line) | 7 Role/RB rules + §7 | FAIL | RB share L4 74/100/52/57% -> 60%+ in 2 of 4 (wx waiver needs a live priced leg; no line) | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Tuten rush yds O (no line) | 8 Injuries | FAIL | Q ankle/foot, DNP all week (lower rung + flag rule); no book line while Q | ESPN injuries API | 2026-11-05 16:43 |
| Tuten rush yds O (no line) | 9 Next Gen Stats | PASS | Tuten RYOE +0.15/att, 8+ box 14.5% | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Tuten rush yds O (no line) | 10 Film | PASS | 2026_05_PHI_JAX play 3968, Q4 9:44, B.Tuten left guard to PHI 28 for 13 yards (C.DeJean) | official NFL YouTube captions matched to pbp (film_verified.json) | 2026-11-05 16:48 |
| Tuten rush yds O (no line) | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Tuten rush yds O (no line) | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Tuten rush yds O (no line) | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Tuten rush yds O (no line) | 14 Models/price/edge | MISSING | NOLINE (no FD/DK/Pin rush line) | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Tuten rush yds O (no line) | 15 Inactives | N/A | leg already CUT (Phase 7). Note: Tuten ACTIVE at inactives; FD rush line now 61.5 -113 (was NOLINE). Still fails 60% carry share 2/4. Not on placed tickets. | @JaguarsPR + Odds API odds_p15_1855 | 2026-11-05 18:56 |
| JAX -9.5 | 1 Data pull | PASS | JAX 7 g / BAL 8 g team logs (PA/RA per game) reconciled to ESPN finals | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| JAX -9.5 | 2 Opportunity | N/A | game-line leg (team totals/spread, no player volume) |  |  |
| JAX -9.5 | 3 Defensive profile | PASS | JAX D pts 15.9/g, RB YPC 3.285; BAL D pts 25.4/g, RB YPC 3.727 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| JAX -9.5 | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| JAX -9.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% press PROXY 24.1%; JAX blitz 30.4% press PROXY 21.5% | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| JAX -9.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| JAX -9.5 | 7 Role/RB rules + §7 | N/A | game-line leg (no player role) |  |  |
| JAX -9.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| JAX -9.5 | 9 Next Gen Stats | PASS | Lawrence TTT 2.75 / aDOT 8.9; Henry RYOE +0.11/att, 8+ box 31% | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| JAX -9.5 | 10 Film | UNVERIFIED | no play-level film read for game lines | official NFL YouTube | 2026-11-05 16:48 |
| JAX -9.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| JAX -9.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| JAX -9.5 | 13 Game script/10G | PASS | JAX blowout favorite; base script JAX leads by half (N3 match) | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| JAX -9.5 | 14 Models/price/edge | MISSING | no sim_v6 game-line model; FD price -120.0 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| JAX -9.5 | 15 Inactives | N/A | leg already CUT |  |  |
| Game total U39.5 | 1 Data pull | PASS | JAX 7 g / BAL 8 g team logs (PA/RA per game) reconciled to ESPN finals | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Game total U39.5 | 2 Opportunity | N/A | game-line leg (team totals/spread, no player volume) |  |  |
| Game total U39.5 | 3 Defensive profile | PASS | JAX D pts 15.9/g, RB YPC 3.285; BAL D pts 25.4/g, RB YPC 3.727 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Game total U39.5 | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| Game total U39.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% press PROXY 24.1%; JAX blitz 30.4% press PROXY 21.5% | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| Game total U39.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| Game total U39.5 | 7 Role/RB rules + §7 | N/A | game-line leg (no player role) |  |  |
| Game total U39.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| Game total U39.5 | 9 Next Gen Stats | PASS | Lawrence TTT 2.75 / aDOT 8.9; Henry RYOE +0.11/att, 8+ box 31% | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| Game total U39.5 | 10 Film | UNVERIFIED | no play-level film read for game lines | official NFL YouTube | 2026-11-05 16:48 |
| Game total U39.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| Game total U39.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| Game total U39.5 | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| Game total U39.5 | 14 Models/price/edge | MISSING | no sim_v6 game-line model; FD price -110.0 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| Game total U39.5 | 15 Inactives | N/A | leg already CUT |  |  |
| BAL team total U13.5 | 1 Data pull | PASS | JAX 7 g / BAL 8 g team logs (PA/RA per game) reconciled to ESPN finals | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| BAL team total U13.5 | 2 Opportunity | N/A | game-line leg (team totals/spread, no player volume) |  |  |
| BAL team total U13.5 | 3 Defensive profile | PASS | JAX D pts 15.9/g, RB YPC 3.285; BAL D pts 25.4/g, RB YPC 3.727 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| BAL team total U13.5 | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| BAL team total U13.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% press PROXY 24.1%; JAX blitz 30.4% press PROXY 21.5% | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| BAL team total U13.5 | 6 QB grade card | FAIL | Fagnano 25 dropbacks: INCOMPLETE card (LOW-SAMPLE) -> backup-QB WEAK; dependent legs flagged | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| BAL team total U13.5 | 7 Role/RB rules + §7 | N/A | game-line leg (no player role) |  |  |
| BAL team total U13.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| BAL team total U13.5 | 9 Next Gen Stats | PASS | Lawrence TTT 2.75 / aDOT 8.9; Henry RYOE +0.11/att, 8+ box 31% | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| BAL team total U13.5 | 10 Film | UNVERIFIED | no play-level film read for game lines | official NFL YouTube | 2026-11-05 16:48 |
| BAL team total U13.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| BAL team total U13.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| BAL team total U13.5 | 13 Game script/10G | PASS | JAX blowout favorite (-9.5/-10); margin 8.5+ -> late kneels/run-out favor unders | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| BAL team total U13.5 | 14 Models/price/edge | MISSING | no sim_v6 game-line model; FD price -108.0 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| BAL team total U13.5 | 15 Inactives | N/A | leg already CUT |  |  |
| JAX 1H -6.5 | 1 Data pull | PASS | JAX 7 g / BAL 8 g team logs (PA/RA per game) reconciled to ESPN finals | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| JAX 1H -6.5 | 2 Opportunity | N/A | game-line leg (team totals/spread, no player volume) |  |  |
| JAX 1H -6.5 | 3 Defensive profile | PASS | JAX D pts 15.9/g, RB YPC 3.285; BAL D pts 25.4/g, RB YPC 3.727 | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| JAX 1H -6.5 | 4 Defender coverage | N/A | pure rushing / game-line leg |  |  |
| JAX 1H -6.5 | 5 Pressure/blitz | PASS | BAL blitz 33.3% press PROXY 24.1%; JAX blitz 30.4% press PROXY 21.5% | FTN charting via nflverse + pbp | 2026-11-05 06:07 |
| JAX 1H -6.5 | 6 QB grade card | PASS | Lawrence vs-blitz C (7.016 YPA), no-blitz A, protection D, money C, clutch A; no gate trips for this leg | nflverse pbp 2026 wk1-8 | 2026-11-05 06:07 |
| JAX 1H -6.5 | 7 Role/RB rules + §7 | N/A | game-line leg (no player role) |  |  |
| JAX 1H -6.5 | 8 Injuries | PASS | BAL: Lamar+Huntley IR, Hawkins (S) OUT, Wiggins (CB) Q illness, Randall IR; JAX: Tuten Q, T.Walker Q, Hamilton/Murray IR; player not designated | ESPN injuries API | 2026-11-05 16:43 |
| JAX 1H -6.5 | 9 Next Gen Stats | PASS | Lawrence TTT 2.75 / aDOT 8.9; Henry RYOE +0.11/att, 8+ box 31% | nflverse NGS (nextgenstats.nfl.com data) | 2026-11-05 16:43 |
| JAX 1H -6.5 | 10 Film | UNVERIFIED | no play-level film read for game lines | official NFL YouTube | 2026-11-05 16:48 |
| JAX 1H -6.5 | 11 Environment | PASS | open air, NWS window precip 76% (WEATHER FLAG), wind 5 mph, gust 12.5; leg not wx-sensitive (rush/under); short week both; no travel issue | NWS api.weather.gov hourly + tools/weather_forecast.py | 2026-11-05 16:52 |
| JAX 1H -6.5 | 12 Source audit | PASS | all 7 categories present and inside age limits at gate time | run_manifest.json source list (all 7 categories) | 2026-11-05 16:49 |
| JAX 1H -6.5 | 13 Game script/10G | PASS | JAX blowout favorite; base script JAX leads by half (N3 match) | read_addendum5_2026-11-05.md (sha256 590b5c875e84) + r2 locked read | 2026-11-05 16:50 |
| JAX 1H -6.5 | 14 Models/price/edge | MISSING | no sim_v6 game-line model; FD price -105.0 | Odds API FD/DK/Pinnacle (odds_r1_1650.csv) | 2026-11-05 16:49 |
| JAX 1H -6.5 | 15 Inactives | N/A | leg already CUT |  |  |

## Summary
- **Lawrence rush yds U12.5**: PASS | flags: SCRAMBLE_CONFLICT: BAL allows 7.3% scramble rate vs 4.8% league; opp-adjusted projection 14.2 > 12.5 (flag, not a cut; Rico Nov 4 6:17 AM); MARKET_GAP: FD alt over 9.5 at -180 implies ~62% over 9.5 vs model ~44% (independent model vs market kept separate)
- **Henry rush yds U71.5**: CUT — §7 MISSING: only 1 game with current QB Fagnano (need 3 of 3 or 3 of 4); P14 MODEL-SUSPECT: all 3 sim medians ~54 vs line 71.5 (17+ yds off the market main)
- **Meyers rec yds U38.5**: CUT — P14 edge -2.5 pts < +3; P14 median does not clear ([41.5, 41.5, 40.28] vs 38.5)
- **Strange rec yds O32.5**: CUT — Phase 11 WEATHER FORECAST + NWS: precip 75% in the game window (open air) - receiving OVER must be CUT (stop, no mirror)
- **Strange 4+ rec (O3.5)**: CUT — Phase 11 WEATHER FORECAST + NWS: precip 75% in the game window (open air) - receiving OVER must be CUT (stop, no mirror)
- **Washington rec yds O60.5**: CUT — Phase 11 WEATHER FORECAST + NWS: precip 75% in the game window (open air) - receiving OVER must be CUT (stop, no mirror)
- **Flowers rec U4.5**: CUT — §7 MISSING: only 1 game with current QB Fagnano; sims built on Lamar/Huntley-era BAL targets (QB-RETURN-type flag; model on wrong QB)
- **Tuten rush yds O (no line)**: CUT — NOLINE: no FanDuel/DK/Pinnacle rush line posted (Q, DNP all week); Phase 7: 60%+ carry share in only 2 of last 4 (74,100,52,57%)
- **JAX -9.5**: CUT — P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable
- **Game total U39.5**: CUT — P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable
- **BAL team total U13.5**: CUT — P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable
- **JAX 1H -6.5**: CUT — P14 MISSING: tools/sim_v6.py has no game-line (spread/total/team-total/period) model - 3 model p unavailable

Sims: tools/sim_v6.py (code sha 1c81119e879acc39), seed 20261101, n 100000 per model (MC/Bias/GR). Builder: build/build_run.py, build/make_checklist.py.
Data gaps: no native game-line model in sim_v6 (spread/total/team total/1H CUT); Fagnano 1-game sample (all BAL player legs CUT on §7); Bias model multipliers equal MC (BIASDUP, see BUGLOG); pressure is PROXY; targets-under-pressure LOW-SAMPLE.


## Phase 15 update (2026-11-05 18:56 ET)
- Official inactives in `phase15_inactives.md` / `inactives/`.
- **Lawrence rush yds U12.5**: Phase 15 HOLD → **PASS**. Price unchanged FD 12.5 -113. No placed-ticket Q issues.
- Tuten ACTIVE + FD 61.5 posted; leg remains CUT on Phase 7.
- Wiggins OUT; receiving overs still weather-cut (NWS 76%).
- User placed TNF exposure: 0. Week 8 KWIII check N/A (past).
- Odds: `odds/odds_p15_1855.csv` (9 credits).

- Gate re-check 18:57 ET: **PASS** (`gate_output_p15.txt`).
