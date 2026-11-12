# checklist.md - BUF@MIN MNF 2026-11-09 (game_id 2026_09_BUF_MIN, Week 9) r2

**UNVETTED. Not picks. Ghost6 vet required. projection_ready=false.**

| Leg | Phase | Status | Number | Source | Pulled (ET) |
|---|---|---|---|---|---|
| Khalil Shakir 3+ rec (FD O2.5 -360) | 1 Data reconcile | PASS | nflverse pbp 2026 thru 2026-11-08 (wk1-9); BUF 7 g (bye wk7), MIN 7 g (wk9 = tonight) | nflverse pbp/snaps/FTN releases | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 2 Opportunity | PASS | tgt share season 19.7% (38/193), last3 18.5%; 5+ tgt in 3 of last 4 (8,3,6,6); proj ~28 team tgt x .19 = 5.3 tgt x catch .71 = 3.8 rec vs 2.5 | nflverse pbp | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 3 Def profile | PASS | MIN WR YPT 7.41 (lg 8.09); WR outside 5.45 (n=86, HARD <10.5) / middle 13.0 (n=30); TE 6.20; rec20+ allowed 13 | nflverse pbp | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 4 Defender coverage | MISSING | no per-defender coverage source (defender_ledger MIN rows = tackler-after-catch, not coverage; no stand-ins); MIN slot CB Byron Murphy Jr. per ESPN depth but alignment unverified | ESPN depth + defender_ledger.csv | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 5 Pressure/blitz | PASS | blitzed share rises 17.9%->22.9% (n=73 blitzed att) -> no volume cut | FTN charting (nflverse) + pbp | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 6 QB card | MISSING | nfl-betting-script s15 QB card not executed this run | - | 2026-11-09 17:30 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 7 Role/RB rules | PASS | WR1 by targets | nflverse pbp | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 8 Injuries | PASS (FLAG) | BUF: LT Dawkins Q (DNP), Anderson Q (LP), Palmer OUT/IR, Shavers Q(NFL.com) vs OUT(ESPN) CONFLICT; MIN: Murray OUT, Jennings OUT, S Ward Q, S T.Jackson Q | ESPN summary + NFL.com wk9 report | 2026-11-09 17:30 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 9 NGS | MISSING | NGS public pages not pulled this run | - | 2026-11-09 17:30 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 10 Film | MISSING | no film reads; nothing verified | - | 2026-11-09 17:30 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 11 Environment | PASS | roof=dome (tools/schedule_2026_wk9.json + nflverse games.csv + ESPN indoor=True); weather_forecast.py status INDOOR, no flag | tools/weather_forecast.py | 2026-11-09 17:25 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 12 Source audit | FAIL | gaps: QB card, NGS, film, man/zone coverage, per-defender coverage; run_gate/feed_week_check not run | source audit | 2026-11-09 17:30 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 13 Script/10G | PASS | BUF moderate fav: FD BUF -3 (-120), DK -3.5, total 45.5; not underdog leg | Odds API FD/DK/Pinnacle | 2026-11-09 17:26 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 14 Models/price/edge | MISSING | no-vig .732 (FD alt -360 vs main 3.5 -154/+116, multiplicative); DK alt -367; model p MISSING -> SIMULATION NOT RUN: main 9e789b5 README projection_ready=false, acceptance fail-closed, 100k triad DEFERRED (NFL-56); NFL-49 not met. tools/sim_v6.py source pbp thru 2026-10-29 = STALE | Odds API pull 17:26 ET | 2026-11-09 17:26 |
| Khalil Shakir 3+ rec (FD O2.5 -360) | 15 Inactives | NOT_YET | official inactives not released at 17:30 ET check (expected ~18:45 ET) | ESPN/NFL.com | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 1 Data reconcile | PASS | nflverse pbp 2026 thru 2026-11-08 (wk1-9); BUF 7 g (bye wk7), MIN 7 g (wk9 = tonight) | nflverse pbp/snaps/FTN releases | 2026-11-09 17:25 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 2 Opportunity | PASS (FLAG) | played wk1-4,8 (missed 5-6); 27 tgt / 145 team tgt in games played = 18.6% (#2/#3 tie w/ Kincaid 18.1%; #3 by season total) -> top-2 status basis-dependent, vetter to rule; 5.2 tgt x 9.6 YPT = ~50 vs 29.5 | nflverse pbp + snaps | 2026-11-09 17:25 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 3 Def profile | FAIL (FLAG) | outside WR YPT allowed 5.45 (n=86) = HARD; Moore outside role assumed, routes unverified | nflverse pbp | 2026-11-09 17:25 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 4 Defender coverage | MISSING | no per-defender coverage (MIN outside CBs Rodgers/Pierre per ESPN depth; no coverage stats); no stand-ins | ESPN depth | 2026-11-09 17:25 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 5 Pressure/blitz | FAIL (FLAG) | Moore blitzed share drops 15.4%->11.4% vs #1 blitz D -> volume caution | FTN charting (nflverse) + pbp | 2026-11-09 17:25 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 6 QB card | MISSING | nfl-betting-script s15 QB card not executed this run | - | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 7 Role/RB rules | PASS | WR2 by tgt/g in games played; LP in practice Sat (no designation) | NFL.com report | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 8 Injuries | PASS (FLAG) | BUF: LT Dawkins Q (DNP), Anderson Q (LP), Palmer OUT/IR, Shavers Q(NFL.com) vs OUT(ESPN) CONFLICT; MIN: Murray OUT, Jennings OUT, S Ward Q, S T.Jackson Q | ESPN summary + NFL.com wk9 report | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 9 NGS | MISSING | NGS public pages not pulled this run | - | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 10 Film | MISSING | no film reads; nothing verified | - | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 11 Environment | PASS | roof=dome (tools/schedule_2026_wk9.json + nflverse games.csv + ESPN indoor=True); weather_forecast.py status INDOOR, no flag | tools/weather_forecast.py | 2026-11-09 17:25 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 12 Source audit | FAIL | gaps: QB card, NGS, film, man/zone coverage, per-defender coverage; run_gate/feed_week_check not run | source audit | 2026-11-09 17:30 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 13 Script/10G | PASS | BUF moderate fav: FD BUF -3 (-120), DK -3.5, total 45.5; not underdog leg | Odds API FD/DK/Pinnacle | 2026-11-09 17:26 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 14 Models/price/edge | MISSING | no-vig .691 (FD alt -275 vs main 45.5 -113/-113); DK -313; model p MISSING -> SIMULATION NOT RUN: main 9e789b5 README projection_ready=false, acceptance fail-closed, 100k triad DEFERRED (NFL-56); NFL-49 not met. tools/sim_v6.py source pbp thru 2026-10-29 = STALE | Odds API | 2026-11-09 17:26 |
| DJ Moore 30+ rec yds (FD O29.5 -275) | 15 Inactives | NOT_YET | official inactives not released at 17:30 ET check (expected ~18:45 ET) | ESPN/NFL.com | 2026-11-09 17:30 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 1 Data reconcile | PASS | nflverse pbp 2026 thru 2026-11-08 (wk1-9); BUF 7 g (bye wk7), MIN 7 g (wk9 = tonight) | nflverse pbp/snaps/FTN releases | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 2 Opportunity | FAIL | WR #3/#4 (27 tgt, 3.9/g; last3 2,6,3) -> #3/#4 WR over ban; no depleted-secondary exception (MIN CBs healthy; only 2 S questionable) | nflverse pbp + injury reports | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 3 Def profile | PASS | MIN WR YPT 7.41 (lg 8.09); WR outside 5.45 (n=86, HARD <10.5) / middle 13.0 (n=30); TE 6.20; rec20+ allowed 13 | nflverse pbp | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 4 Defender coverage | MISSING | no per-defender coverage source | - | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 5 Pressure/blitz | PASS | blitzed share rises 11.4%->18.6% | FTN charting (nflverse) + pbp | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 6 QB card | MISSING | nfl-betting-script s15 QB card not executed this run | - | 2026-11-09 17:30 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 7 Role/RB rules | FAIL | WR3/4 role | nflverse pbp | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 8 Injuries | PASS (FLAG) | BUF: LT Dawkins Q (DNP), Anderson Q (LP), Palmer OUT/IR, Shavers Q(NFL.com) vs OUT(ESPN) CONFLICT; MIN: Murray OUT, Jennings OUT, S Ward Q, S T.Jackson Q | ESPN summary + NFL.com wk9 report | 2026-11-09 17:30 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 9 NGS | MISSING | NGS public pages not pulled this run | - | 2026-11-09 17:30 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 10 Film | MISSING | no film reads; nothing verified | - | 2026-11-09 17:30 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 11 Environment | PASS | roof=dome (tools/schedule_2026_wk9.json + nflverse games.csv + ESPN indoor=True); weather_forecast.py status INDOOR, no flag | tools/weather_forecast.py | 2026-11-09 17:25 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 12 Source audit | FAIL | gaps: QB card, NGS, film, man/zone coverage, per-defender coverage; run_gate/feed_week_check not run | source audit | 2026-11-09 17:30 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 13 Script/10G | PASS | BUF moderate fav: FD BUF -3 (-120), DK -3.5, total 45.5; not underdog leg | Odds API FD/DK/Pinnacle | 2026-11-09 17:26 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 14 Models/price/edge | MISSING | no-vig .643 (FD -220 vs main 2.5 +144/-194); DK -210; model p MISSING | Odds API | 2026-11-09 17:26 |
| Keon Coleman 2+ rec (FD O1.5 -220) | 15 Inactives | NOT_YET | official inactives not released at 17:30 ET check (expected ~18:45 ET) | ESPN/NFL.com | 2026-11-09 17:30 |
| James Cook 60+ rush yds (FD O59.5 -360) | 1 Data reconcile | PASS | nflverse pbp 2026 thru 2026-11-08 (wk1-9); BUF 7 g (bye wk7), MIN 7 g (wk9 = tonight) | nflverse pbp/snaps/FTN releases | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 2 Opportunity | PASS | team rushes ~31/g (season 31.0); Cook share of team rushes last3 63.6% (68/107), >=60% in 3 of last 4 (60.0,67.6,75.9,51.2); ~20 carries x 4.4-4.6 = ~86-90 vs 59.5 | nflverse pbp | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 3 Def profile | PASS | MIN RB YPC allowed 4.56 (n=158) vs lg RB 4.16 -> >4.4 SOFT; 116.7 rush ypg (17th); rush15+ allowed 7 | nflverse pbp | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 4 Defender coverage | N/A | pure rushing leg | - | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 5 Pressure/blitz | N/A | rushing leg; MIN 8+ box rate 5.8% (rank 21) -> stacked-box premise not supported | FTN charting | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 6 QB card | MISSING | nfl-betting-script s15 QB card not executed this run | - | 2026-11-09 17:30 |
| James Cook 60+ rush yds (FD O59.5 -360) | 7 Role/RB rules | PASS | lead back, carry share >=60% 3 of last 4; BUF favored so rush-only OK | nflverse pbp | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 8 Injuries | PASS (FLAG) | LT Dawkins Q (DNP) + G/OT Anderson Q: if both out, check OL rule (C + 2 interior caps RB overs; neither is C) | ESPN/NFL.com | 2026-11-09 17:30 |
| James Cook 60+ rush yds (FD O59.5 -360) | 9 NGS | MISSING | NGS public pages not pulled this run | - | 2026-11-09 17:30 |
| James Cook 60+ rush yds (FD O59.5 -360) | 10 Film | MISSING | no film reads; nothing verified | - | 2026-11-09 17:30 |
| James Cook 60+ rush yds (FD O59.5 -360) | 11 Environment | PASS | roof=dome (tools/schedule_2026_wk9.json + nflverse games.csv + ESPN indoor=True); weather_forecast.py status INDOOR, no flag | tools/weather_forecast.py | 2026-11-09 17:25 |
| James Cook 60+ rush yds (FD O59.5 -360) | 12 Source audit | FAIL | gaps: QB card, NGS, film, man/zone coverage, per-defender coverage; run_gate/feed_week_check not run | source audit | 2026-11-09 17:30 |
| James Cook 60+ rush yds (FD O59.5 -360) | 13 Script/10G | PASS | BUF moderate fav: FD BUF -3 (-120), DK -3.5, total 45.5; not underdog leg | Odds API FD/DK/Pinnacle | 2026-11-09 17:26 |
| James Cook 60+ rush yds (FD O59.5 -360) | 14 Models/price/edge | MISSING | no-vig .738 (FD alt -360 vs main 83.5 -113/-113); DK -411 (DK main 86.5); model p MISSING | Odds API | 2026-11-09 17:26 |
| James Cook 60+ rush yds (FD O59.5 -360) | 15 Inactives | NOT_YET | official inactives not released at 17:30 ET check (expected ~18:45 ET) | ESPN/NFL.com | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 1 Data reconcile | PASS | nflverse pbp 2026 thru 2026-11-08 (wk1-9); BUF 7 g (bye wk7), MIN 7 g (wk9 = tonight) | nflverse pbp/snaps/FTN releases | 2026-11-09 17:25 |
| Josh Allen OR James Cook anytime TD | 2 Opportunity | PASS | Allen 9 rush TD in 7 g (7.9 rush att/g); Cook 7 rush TD in 7 g; BUF implied ~24.5 pts (45.5 total, -3) | nflverse pbp | 2026-11-09 17:25 |
| Josh Allen OR James Cook anytime TD | 3 Def profile | MISSING | red-zone TD% allowed not computed this run | - | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 4 Defender coverage | N/A | rushing TD leg | - | 2026-11-09 17:25 |
| Josh Allen OR James Cook anytime TD | 5 Pressure/blitz | N/A | - | - | 2026-11-09 17:25 |
| Josh Allen OR James Cook anytime TD | 6 QB card | MISSING | nfl-betting-script s15 QB card not executed this run | - | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 7 Role/RB rules | PASS | Cook lead back; Allen goal-line rushing role | nflverse pbp | 2026-11-09 17:25 |
| Josh Allen OR James Cook anytime TD | 8 Injuries | PASS (FLAG) | BUF: LT Dawkins Q (DNP), Anderson Q (LP), Palmer OUT/IR, Shavers Q(NFL.com) vs OUT(ESPN) CONFLICT; MIN: Murray OUT, Jennings OUT, S Ward Q, S T.Jackson Q | ESPN summary + NFL.com wk9 report | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 9 NGS | MISSING | NGS public pages not pulled this run | - | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 10 Film | MISSING | no film reads; nothing verified | - | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 11 Environment | PASS | roof=dome (tools/schedule_2026_wk9.json + nflverse games.csv + ESPN indoor=True); weather_forecast.py status INDOOR, no flag | tools/weather_forecast.py | 2026-11-09 17:25 |
| Josh Allen OR James Cook anytime TD | 12 Source audit | FAIL | gaps: QB card, NGS, film, man/zone coverage, per-defender coverage; run_gate/feed_week_check not run | source audit | 2026-11-09 17:30 |
| Josh Allen OR James Cook anytime TD | 13 Script/10G | PASS | BUF moderate fav: FD BUF -3 (-120), DK -3.5, total 45.5; not underdog leg | Odds API FD/DK/Pinnacle | 2026-11-09 17:26 |
| Josh Allen OR James Cook anytime TD | 14 Models/price/edge | MISSING | NOLINE: anytime TD not in Odds API pull (tools/pull_odds.py market set); "either/or" is not a single book market; no TD model in sim_v6 | Odds API | 2026-11-09 17:26 |
| Josh Allen OR James Cook anytime TD | 15 Inactives | NOT_YET | official inactives not released at 17:30 ET check (expected ~18:45 ET) | ESPN/NFL.com | 2026-11-09 17:30 |

## Summary
- Legs PASSED: none (0). No card.
- CUT: all 5. Common cut phases: P6 MISSING, P9 MISSING, P10 MISSING, P12 FAIL, P14 MISSING (SIMULATION NOT RUN), P15 NOT_YET. Leg-specific: Shakir P4 MISSING; Moore P3/P5 FAIL-FLAG + P4 MISSING; Coleman P2 FAIL (#3/#4 WR ban) + P4 MISSING; Cook P14 MISSING only beyond common gaps; ATD NOLINE.
- Seeds/trials: none (SIMULATION NOT RUN). Script path that would be used: tools/sim_v6.py (N=100000, default SEED=20261101) - not executed.
- Data gaps: man/zone + MOF coverage (2026 pbp participation not published; FTN nflverse has no coverage field), per-defender coverage, NGS, film, QB card, red-zone D, official inactives.

VETTED: (pending Ghost6)
