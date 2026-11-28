# CAR defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 10.0 | 23.6 | — |
| Zone % | 84.8 | 76.4 | — |
| Single-high / MOFC % | 55.2 | 59.5 | — |
| Two-high / MOFO % | 40.2 | 40.5 | — |
| Blitz % | 32.2 | 32.3 | 31.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 44.2 / 18.8, 74.0 | — | — |

Sharp YPT allowed: WR 7.7, TE 6.0, RB 4.5, **outside 8.2 vs slot 8.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #29 vs StatRankings #28; blitz rank Sharp #10 vs SR #15 (raw gaps: man -13.6 pts, blitz -0.1 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.5 | 148.7 | 7.63 | 7 | 0.158 | 14 |
| TE | 7.3 | 44.1 | 6.04 | 5 | 0.259 | 26 |
| RB | 6.7 | 30.0 | 4.48 | 2 | -0.158 | 21 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 13 | 6 | 181 | 3 | 0 | 13.92 | 11.46 | 11 |  |
| deep middle | 11 | 4 | 114 | 0 | 0 | 10.36 | 14.39 | 27 |  |
| deep right | 26 | 8 | 270 | 2 | 1 | 10.38 | 12.14 | 22 |  |
| short left | 105 | 75 | 614 | 1 | 0 | 5.85 | 5.99 | 18 |  |
| short middle | 58 | 45 | 451 | 3 | 1 | 7.78 | 7.32 | 8 | **WEAK** |
| short right | 122 | 87 | 598 | 5 | 5 | 4.9 | 6.02 | 31 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs CAR: **3.37 yds** (league 2.93; rank 2/32 most allowed). WR 3.25, TE 3.79, cushion 7.9. Sample: 22 receiver-games, 188 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Will Lee | CB | 8 | 76.4 (100.0 wk11) | 52 | 28 | 340 | 1 | 0 | 6.54 | 80.6 | 10.2 | 2 | 7 | 4 | 11 | 24 (274) | MISSING |
| Akayleb Evans | CB | 5 | 72.8 (100.0 wk7) | 31 | 21 | 292 | 2 | 0 | 9.42 | 119.3 | 11.9 | 1 | 2 | 2 | 4 | 13 (176) | MISSING |
| Chau Smith-Wade | CB | 8 | 42.4 (54.0 wk11) | 18 | 11 | 108 | 0 | 0 | 6.00 | 78.0 | 10.2 | 0 | 3 | 0 | 3 | 12 (107) | MISSING |
| Michael Jackson | CB | 4 | 76.8 (100.0 wk11) | 11 | 7 | 58 | 0 | 0 | 5.27 | 77.1 | 4.9 | 0 | 2 | 1 | 3 | 4 (41) | MISSING |
| Marco Wilson | CB | 3 | 100.0 (100.0 wk10) | 25 | 16 | 140 | 0 | 0 | 5.60 | 78.8 | 10.0 | 0 | 3 | 2 | 5 | 13 (104) | MISSING |
| Jaycee Horn | CB | 3 | 87.3 (91.0 wk3) | 12 | 6 | 106 | 1 | 0 | 8.83 | 108.3 | 7.8 | 1 | 1 | 0 | 1 | 4 (59) | MISSING |
| Corey Thornton | CB | 2 | 75.5 (51.0 wk10) | 8 | 6 | 39 | 1 | 1 | 4.88 | 84.9 | 8.9 | 0 | 2 | 3 | 6 | 5 (36) | MISSING |
| Malcolm DeWalt | CB | 1 | 2.0 (2.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Tre'von Moehrig | S | 10 | 96.5 (100.0 wk11) | 33 | 18 | 163 | 0 | 0 | 4.94 | 68.1 | 6.9 | 0 | 1 | 0 | 1 | 14 (157) | MISSING |
| Nick Scott | S | 9 | 74.3 (34.0 wk11) | 27 | 18 | 212 | 2 | 0 | 7.85 | 115.0 | 7.9 | 0 | 2 | 0 | 2 | 15 (147) | MISSING |
| Zakee Wheatley | S | 9 | 68.3 (100.0 wk11) | 22 | 14 | 332 | 3 | 1 | 15.09 | 127.8 | 15.0 | 2 | 3 | 0 | 4 | 15 (173) | MISSING |
| Lathan Ransom | S | 8 | 31.6 (2.0 wk11) | 11 | 2 | 88 | 0 | 0 | 8.00 | 60.4 | 16.3 | 0 | 2 | 0 | 2 | 6 (104) | MISSING |
| Isaiah Simmons | S | 2 | 4.0 (1.0 wk4) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Devin Lloyd | 9 | 58 | 37 | 329 | 2 | 5.67 | 68.8 | 1 |
| Bobby Okereke | 7 | 20 | 15 | 70 | 2 | 3.50 | 91.7 | 4 |
| Tyrel Dodson | 5 | 18 | 14 | 75 | 1 | 4.17 | 79.4 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | BAL | T.Dodson | INT | R.Bateman | short_right |
| 11 | BAL | D.Brown | PBU | Z.Flowers | short_middle |
| 11 | BAL | C.Smith-Wade | PBU | R.Bateman | short_left |
| 11 | BAL | M.Jackson | PBU | Z.Flowers | short_right |
| 11 | BAL | M.Jackson | PBU | R.Bateman | deep_left |
| 11 | BAL | W.Lee | DPI | J.Lane | short_right |
| 10 | NO | C.Thornton | DPI | C.Olave | deep_right |
| 10 | NO | T.Wharton | PBU | T.Etienne | short_middle |
| 10 | NO | T.Moehrig | PBU | T.Etienne | short_left |
| 10 | NO | D.Lloyd | INT | C.Olave | short_right |
| 9 | DEN | C.Thornton | DPI | P.Bryant | short_right |
| 9 | DEN | C.Smith-Wade | PBU | E.Engram | short_right |
| 9 | DEN | M.Wilson | PBU | M.Mims | deep_left |
| 9 | DEN | C.Smith-Wade | PBU | T.Franklin | deep_right |
| 9 | DEN | C.Thornton | PBU | C.Sutton | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Will Lee III | CB | 42.5 | 24.0 | 273.6 | 6.44 | 1.47 | 49 (28) |
| Devin Lloyd | LB | 30.7 | 23.1 | 183.4 | 5.97 | 1.07 | 53 (7) |
| Akayleb Evans | CB | 27.0 | 15.7 | 204.3 | 7.57 | 0.84 | 33 (29) |
| Marco Wilson | CB | 25.0 | 17.1 | 169.6 | 6.78 | 1.18 | 37 (23) |
| Bobby Okereke | LB | 22.1 | 15.7 | 125.3 | 5.67 | 0.8 | 29 (3) |
| Tre'von Moehrig | S | 20.6 | 14.1 | 136.5 | 6.63 | 0.77 | 10 (0) |
| Chau Smith-Wade | CB | 20.0 | 15.1 | 144.0 | 7.2 | 0.71 | 15 (5) |
| Nick Scott | S | 17.4 | 12.4 | 142.9 | 8.21 | 1.06 | 17 (0) |
| Mike Jackson | CB | 16.7 | 10.7 | 155.4 | 9.31 | 1.02 | 28 (8) |
| Zakee Wheatley | S | 16.6 | 10.7 | 123.3 | 7.43 | 0.83 | 13 (2) |
| Patrick Jones II | LB | 14.8 | 10.6 | 80.2 | 5.42 | 0.52 | 0 (0) |
| Jaelan Phillips | LB | 13.6 | 9.2 | 73.6 | 5.41 | 0.49 | 3 (0) |

### Upcoming: opposing receivers vs likely CAR defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-30 | TB | C.Otton (TE) | 11 | short_right 46%, short_middle 22% | Zakee Wheatley (14%) | Tre'von Moehrig (12%) |
| 12 | 2026-11-30 | TB | E.Egbuka (WR) | 10 | short_right 34%, short_left 29% | Mike Jackson (26%) | Will Lee III (24%) |
| 12 | 2026-11-30 | TB | B.Irving (RB) | 9 | short_left 47%, short_right 44% | Tyrel Dodson (19%) | Devin Lloyd (18%) |
| 12 | 2026-11-30 | TB | K.Gainwell (RB) | 8 | short_right 58%, short_left 35% | Tyrel Dodson (19%) | Devin Lloyd (18%) |
| 13 | 2026-12-06 | MIN | J.Jefferson (WR) | 33 | short_left 36%, short_right 29% | Mike Jackson (28%) | Will Lee III (25%) |
| 13 | 2026-12-06 | MIN | T.Felton (WR) | 17 | short_left 38%, short_right 25% | Mike Jackson (28%) | Will Lee III (23%) |
| 13 | 2026-12-06 | MIN | T.Hockenson (TE) | 14 | short_left 33%, short_right 25% | Tre'von Moehrig (15%) | Zakee Wheatley (15%) |
| 13 | 2026-12-06 | MIN | M.Price (WR) | 10 | short_left 41%, short_right 24% | Mike Jackson (29%) | Will Lee III (25%) |

Defender pool = CAR players with defensive snaps in their most recent game (2026_11_BAL_CAR); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Tre'von Moehrig | S | 77.7 | 49.4 | 512.2 | 6.59 | 5.08 | 141.1 | 4 |
| Will Lee III | CB | 33.7 | 21.0 | 258.7 | 7.68 | 2.69 | 110.0 | 4 |
| Marco Wilson | CB | 13.8 | 10.0 | 106.0 | 7.68 | 2.14 | 50.2 | 3 |
| Nick Scott | S | 13.5 | 7.2 | 132.6 | 9.82 | 1.7 | 72.2 | 1 |
| Jaycee Horn | CB | 7.1 | 4.4 | 61.7 | 8.69 | 1.56 | 39.6 | 2 |
| Chau Smith-Wade | CB | 21.5 | 13.9 | 130.6 | 6.07 | 1.38 | 39.0 | 2 |
| Akayleb Evans | CB | 16.5 | 9.3 | 121.6 | 7.37 | 1.15 | 50.3 | 1 |
| Devin Lloyd | LB | 59.7 | 44.9 | 352.6 | 5.91 | 0.89 | 20.7 | 0 |
| Corey Thornton | CB | 11.0 | 8.8 | 80.9 | 7.35 | 0.88 | 21.1 | 1 |
| Mike Jackson | CB | 8.9 | 5.6 | 70.1 | 7.88 | 0.72 | 27.1 | 1 |
| Tyrel Dodson | LB | 19.8 | 14.8 | 104.3 | 5.27 | 0.22 | 6.1 | 0 |
| Patrick Jones II | LB | 5.8 | 3.4 | 25.7 | 4.43 | 0.05 | 1.2 | 0 |

### Rest of Week 12: receivers vs likely CAR window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-30 | TB | C.Otton (TE) | 11 | 7% | Tre'von Moehrig (34%, 5.08) | Devin Lloyd (24%, 0.89) |
| 2026-11-30 | TB | E.Egbuka (WR) | 10 | 15% | Chau Smith-Wade (27%, 1.38) | Tre'von Moehrig (16%, 5.08) |
| 2026-11-30 | TB | B.Irving (RB) | 9 | 0% | Devin Lloyd (49%, 0.89) | Tyrel Dodson (23%, 0.22) |
| 2026-11-30 | TB | K.Gainwell (RB) | 8 | 0% | Devin Lloyd (46%, 0.89) | Tyrel Dodson (24%, 0.22) |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Akayleb Evans (CB) 31 tgt, 67.7% catch, 9.42 ypt, rating 119.3 [GIVES UP EXPLOSIVES, TARGET MAGNET, WEAK LINK]
**Best / lockdown:** Tre'von Moehrig (S) 33 tgt, 54.5% catch, 4.94 ypt, rating 68.1 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS]
**Weak zones:** short middle 7.8 ypt

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Will Lee | CB | 8 | 52 | 26% | 53.8 | 6.54 | 12.14 | 0.825 | 80.6 | 1 | 0 | 7 | 54.5 | LIMITS CATCHES, TARGET MAGNET |  |
| Marco Wilson | CB | 3 | 25 | 32% | 64.0 | 5.6 | 8.75 | 0.676 | 78.8 | 0 | 0 | 3 | 47.5 | LIMITS YARDS, TARGET MAGNET | small sample (<35 tgts) |
| Akayleb Evans | CB | 5 | 31 | 24% | 67.7 | 9.42 | 13.9 | 1.202 | 119.3 | 2 | 0 | 2 | 9.5 | GIVES UP EXPLOSIVES, TARGET MAGNET, WEAK LINK | small sample (<35 tgts) |
| Tre'von Moehrig | S | 10 | 33 | 13% | 54.5 | 4.94 | 9.06 | 0.247 | 68.1 | 0 | 0 | 1 | 85.5 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS | small sample (<35 tgts) |
| Nick Scott | S | 8 | 27 | 13% | 66.7 | 7.85 | 11.78 | 0.46 | 115.0 | 2 | 0 | 2 | 38.0 |  | small sample (<35 tgts) |
| Zakee Wheatley | S | 8 | 22 | 10% | 63.6 | 15.09 | 23.71 | 0.806 | 127.8 | 3 | 1 | 3 | 11.2 | GIVES UP EXPLOSIVES, WEAK LINK | small sample (<35 tgts) |
