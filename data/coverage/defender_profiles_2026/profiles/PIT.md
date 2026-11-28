# PIT defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.7 | 19.5 | — |
| Zone % | 79.5 | 80.0 | — |
| Single-high / MOFC % | 44.6 | 45.9 | — |
| Two-high / MOFO % | 50.5 | 54.1 | — |
| Blitz % | 28.5 | 29.5 | 28.2 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 48.5 / 21.9, 72.0 | — | — |

Sharp YPT allowed: WR 7.5, TE 8.6, RB 6.2, **outside 7.8 vs slot 7.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #24 vs StatRankings #32; blitz rank Sharp #16 vs SR #21 (raw gaps: man -5.8 pts, blitz -1.0 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.1 | 152.8 | 7.6 | 5 | 0.127 | 12 |
| TE | 6.1 | 52.2 | 8.56 | 3 | 0.282 | 17 |
| RB | 7.2 | 43.9 | 6.1 | 3 | -0.002 | 2 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 25 | 12 | 358 | 0 | 1 | 14.32 | 11.46 | 6 | **WEAK** |
| deep middle | 8 | 3 | 91 | 1 | 2 | 11.38 | 14.39 | 23 |  |
| deep right | 19 | 10 | 339 | 1 | 0 | 17.84 | 12.14 | 3 | **WEAK** |
| short left | 127 | 98 | 781 | 4 | 1 | 6.15 | 5.99 | 13 |  |
| short middle | 59 | 44 | 440 | 1 | 0 | 7.46 | 7.32 | 12 |  |
| short right | 97 | 62 | 477 | 4 | 3 | 4.92 | 6.02 | 30 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs PIT: **3.04 yds** (league 2.93; rank 11/32 most allowed). WR 2.82, TE 4.14, cushion 6.98. Sample: 23 receiver-games, 192 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jalen Ramsey | CB | 10 | 99.6 (98.0 wk11) | 54 | 33 | 285 | 6 | 0 | 5.28 | 112.0 | 4.4 | 2 | 3 | 0 | 3 | 26 (281) | MISSING |
| Asante Samuel Jr. | CB | 10 | 83.1 (8.0 wk11) | 53 | 24 | 453 | 2 | 0 | 8.55 | 88.0 | 12.2 | 3 | 9 | 1 | 10 | 24 (358) | MISSING |
| Jamel Dean | CB | 9 | 85.4 (100.0 wk11) | 60 | 35 | 391 | 0 | 1 | 6.52 | 70.9 | 8.8 | 1 | 8 | 0 | 9 | 27 (264) | MISSING |
| Daylen Everette | CB | 10 | 41.3 (100.0 wk11) | 34 | 19 | 283 | 1 | 1 | 8.32 | 80.9 | 13.2 | 1 | 5 | 1 | 7 | 15 (236) | MISSING |
| Brandin Echols | CB | 6 | 7.0 (9.0 wk11) | 2 | 1 | 7 | 0 | 0 | 3.50 | 58.3 | 4.5 | 0 | 0 | 0 | 0 | 1 (7) | MISSING |
| Jaquan Brisker | S | 10 | 97.2 (74.0 wk11) | 45 | 22 | 338 | 1 | 1 | 7.51 | 72.3 | 9.8 | 0 | 2 | 0 | 3 | 29 (367) | MISSING |
| Robert Spears-Jennings | S | 8 | 54.0 (83.0 wk11) | 21 | 12 | 137 | 0 | 1 | 6.52 | 57.0 | 11.5 | 0 | 1 | 0 | 2 | 12 (128) | MISSING |
| Rayshawn Jenkins | S | 4 | 54.5 (20.0 wk4) | 6 | 2 | 90 | 0 | 0 | 15.00 | 81.9 | 17.2 | 1 | 0 | 0 | 0 | 8 (132) | MISSING |
| DeShon Elliott | S | 3 | 31.0 (26.0 wk11) | 3 | 2 | 33 | 0 | 0 | 11.00 | 103.5 | 13.0 | 0 | 0 | 0 | 0 | 1 (24) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Payton Wilson | 10 | 57 | 37 | 337 | 1 | 5.91 | 79.3 | 3 |
| Patrick Queen | 10 | 49 | 26 | 238 | 0 | 4.86 | 58.0 | 3 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | PHI | C.Heyward | PBU | D.Smith | short_left |
| 11 | PHI | J.Ramsey | PBU | D.Smith | short_left |
| 11 | PHI | P.Wilson | PBU | D.Smith | short_middle |
| 11 | PHI | D.Everette | PBU | D.Cooper | short_right |
| 10 | CIN | J.Dean | PBU | J.Chase | deep_right |
| 10 | CIN | T.Watt | PBU | C.Brown | short_right |
| 10 | CIN | A.Samuel | PBU | J.Chase | short_middle |
| 10 | CIN | A.Samuel | DPI | D.Meyers | deep_middle |
| 8 | CLE | T.Watt | PBU | D.Sampson | short_right |
| 8 | CLE | K.Benton | PBU | D.Boston | short_right |
| 8 | CLE | A.Samuel | PBU | D.Boston | short_right |
| 8 | CLE | C.Heyward | PBU | K.Concepcion | short_left |
| 8 | CLE | P.Queen | PBU | D.Sampson | short_middle |
| 7 | NO | C.Heyward | PBU | J.Johnson | short_middle |
| 7 | NO | Y.Black | PBU | J.Johnson | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Jamel Dean | CB | 51.2 | 32.5 | 347.7 | 6.79 | 1.58 | 82 (53) |
| Asante Samuel Jr. | CB | 50.9 | 31.3 | 417.1 | 8.19 | 1.37 | 61 (26) |
| Jalen Ramsey | CB | 49.9 | 33.9 | 389.6 | 7.81 | 1.21 | 51 (14) |
| Patrick Queen | LB | 33.7 | 25.3 | 224.5 | 6.66 | 1.2 | 42 (12) |
| Payton Wilson | LB | 29.7 | 22.9 | 225.6 | 7.6 | 1.04 | 35 (7) |
| Daylen Everette | CB | 24.8 | 14.4 | 196.8 | 7.94 | 0.41 | 22 (15) |
| Jaquan Brisker | S | 24.7 | 17.5 | 207.4 | 8.4 | 1.26 | 29 (2) |
| T.J. Watt | LB | 16.9 | 12.1 | 98.9 | 5.85 | 0.81 | 11 (0) |
| Alex Highsmith | LB | 14.8 | 11.0 | 94.8 | 6.41 | 0.51 | 0 (0) |
| Nick Herbig | LB | 12.4 | 9.2 | 76.3 | 6.15 | 0.47 | 1 (0) |
| Robert Spears-Jennings | S | 9.1 | 6.4 | 69.4 | 7.63 | 0.3 | 1 (0) |
| Jack Sawyer | LB | 7.7 | 5.6 | 50.2 | 6.52 | 0.27 | 0 (0) |

### Upcoming: opposing receivers vs likely PIT defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-27 | DEN | E.Engram (TE) | 13 | short_left 45%, short_right 32% | Jamel Dean (12%) | Daylen Everette (12%) |
| 12 | 2026-11-27 | DEN | C.Sutton (WR) | 11 | short_left 33%, short_right 33% | Daylen Everette (24%) | Jamel Dean (23%) |
| 12 | 2026-11-27 | DEN | P.Bryant (WR) | 9 | short_right 43%, short_left 29% | Daylen Everette (23%) | Jamel Dean (22%) |
| 12 | 2026-11-27 | DEN | J.Coleman (RB) | 9 | short_right 53%, short_left 37% | Patrick Queen (20%) | T.J. Watt (20%) |
| 13 | 2026-12-06 | HOU | N.Collins (WR) | 25 | short_right 30%, short_middle 22% | Jalen Ramsey (21%) | Daylen Everette (21%) |
| 13 | 2026-12-06 | HOU | X.Hutchinson (WR) | 17 | short_middle 30%, short_right 26% | Jalen Ramsey (22%) | Daylen Everette (19%) |
| 13 | 2026-12-06 | HOU | T.Dell (WR) | 17 | deep_right 28%, short_middle 28% | Jalen Ramsey (24%) | Daylen Everette (18%) |
| 13 | 2026-12-06 | HOU | K.Boutte (WR) | 8 | short_middle 26%, short_right 23% | Jalen Ramsey (21%) | Daylen Everette (19%) |

Defender pool = PIT players with defensive snaps in their most recent game (2026_11_PIT_PHI); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Jaquan Brisker | S | 29.3 | 17.7 | 280.2 | 9.56 | 5.8 | 184.9 | 4 |
| Jalen Ramsey | CB | 39.1 | 24.3 | 301.1 | 7.7 | 5.36 | 159.7 | 8 |
| Jamel Dean | CB | 41.7 | 28.2 | 319.8 | 7.67 | 5.11 | 150.1 | 5 |
| Asante Samuel Jr. | CB | 39.0 | 25.9 | 337.1 | 8.64 | 5.01 | 167.5 | 6 |
| Robert Spears-Jennings | S | 38.5 | 24.3 | 300.8 | 7.81 | 4.62 | 142.4 | 4 |
| Payton Wilson | LB | 47.9 | 36.4 | 288.1 | 6.01 | 2.62 | 69.3 | 1 |
| Patrick Queen | LB | 75.6 | 56.3 | 468.9 | 6.2 | 2.59 | 68.3 | 4 |
| Daylen Everette | CB | 14.9 | 9.1 | 91.2 | 6.12 | 1.06 | 29.7 | 1 |

### Rest of Week 12: receivers vs likely PIT window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-27 | DEN | E.Engram (TE) | 13 | 8% | Robert Spears-Jennings (30%, 4.62) | Payton Wilson (25%, 2.62) |
| 2026-11-27 | DEN | C.Sutton (WR) | 11 | 15% | Jalen Ramsey (24%, 5.36) | Jamel Dean (19%, 5.11) |
| 2026-11-27 | DEN | P.Bryant (WR) | 9 | 5% | Jalen Ramsey (26%, 5.36) | Daylen Everette (16%, 1.06) |
| 2026-11-27 | DEN | J.Coleman (RB) | 9 | 0% | Patrick Queen (46%, 2.59) | Payton Wilson (26%, 2.62) |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Asante Samuel Jr. (CB) 53 tgt, 45.3% catch, 8.55 ypt, rating 88.0 [LIMITS CATCHES, GIVES UP EXPLOSIVES]
**Best / lockdown:** Robert Spears-Jennings (S) 21 tgt, 57.1% catch, 6.52 ypt, rating 57.0 [LOCKDOWN, LIMITS YARDS]
**Weak zones:** deep right 17.8 ypt; deep left 14.3 ypt

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jamel Dean | CB | 9 | 60 | 25% | 58.3 | 6.52 | 11.17 | 0.823 | 70.9 | 0 | 1 | 8 | 51.5 | TARGET MAGNET |  |
| Daylen Everette | CB | 8 | 34 | 14% | 55.9 | 8.32 | 14.89 | 1.097 | 80.9 | 1 | 1 | 5 | 51.5 | GIVES UP EXPLOSIVES | small sample (<35 tgts) |
| Jalen Ramsey | CB | 10 | 54 | 19% | 61.1 | 5.28 | 8.64 | 0.456 | 112.0 | 6 | 0 | 3 | 51.5 | LIMITS YARDS |  |
| Asante Samuel Jr. | CB | 10 | 53 | 19% | 45.3 | 8.55 | 18.88 | 0.855 | 88.0 | 2 | 0 | 9 | 47.5 | LIMITS CATCHES, GIVES UP EXPLOSIVES |  |
| Robert Spears-Jennings | S | 7 | 21 | 10% | 57.1 | 6.52 | 11.42 | 0.493 | 57.0 | 0 | 1 | 1 | 75.0 | LOCKDOWN, LIMITS YARDS | small sample (<35 tgts) |
| Jaquan Brisker | S | 10 | 45 | 16% | 48.9 | 7.51 | 15.36 | 0.552 | 72.3 | 1 | 1 | 2 | 59.0 | LIMITS CATCHES |  |
