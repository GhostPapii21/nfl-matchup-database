# MIA defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.8 | 22.2 | — |
| Zone % | 77.2 | 77.5 | — |
| Single-high / MOFC % | 42.1 | 47.3 | — |
| Two-high / MOFO % | 51.9 | 52.7 | — |
| Blitz % | 18.9 | 23.1 | 21.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 38.5 / 26.6, 56.0 | — | — |

Sharp YPT allowed: WR 9.2, TE 8.0, RB 6.0, **outside 9.6 vs slot 9.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #23 vs StatRankings #29; blitz rank Sharp #31 vs SR #30 (raw gaps: man -8.4 pts, blitz -4.2 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 14.0 | 128.2 | 9.16 | 7 | 0.299 | 28 |
| TE | 7.3 | 58.2 | 7.97 | 6 | 0.261 | 11 |
| RB | 6.2 | 37.5 | 6.05 | 5 | 0.199 | 9 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 15 | 9 | 209 | 0 | 1 | 13.93 | 11.46 | 10 |  |
| deep middle | 15 | 9 | 305 | 1 | 2 | 20.33 | 14.39 | 3 | **WEAK** |
| deep right | 22 | 13 | 383 | 2 | 0 | 17.41 | 12.14 | 4 | **WEAK** |
| short left | 82 | 67 | 527 | 6 | 0 | 6.43 | 5.99 | 10 |  |
| short middle | 46 | 32 | 279 | 5 | 4 | 6.07 | 7.32 | 30 |  |
| short right | 95 | 77 | 536 | 4 | 2 | 5.64 | 6.02 | 25 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs MIA: **3.44 yds** (league 2.93; rank 1/32 most allowed). WR 3.56, TE 3.19, cushion 6.04. Sample: 13 receiver-games, 100 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chris Johnson | CB | 10 | 97.8 (99.0 wk11) | 45 | 32 | 408 | 3 | 2 | 9.07 | 102.8 | 7.1 | 2 | 3 | 0 | 5 | 29 (339) | MISSING |
| Jason Marshall | CB | 10 | 71.6 (71.0 wk11) | 37 | 25 | 347 | 2 | 0 | 9.38 | 115.5 | 8.3 | 1 | 1 | 1 | 2 | 15 (188) | MISSING |
| Julius Brents | CB | 10 | 69.9 (72.0 wk11) | 33 | 23 | 258 | 1 | 0 | 7.82 | 102.8 | 9.5 | 1 | 2 | 1 | 3 | 17 (145) | MISSING |
| Darrell Baker | CB | 1 | 23.0 (23.0 wk11) | 1 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 12.0 | 0 | 0 | 0 | 0 | 1 (12) | MISSING |
| Jaylin Simpson | CB | 3 | 4.3 (3.0 wk9) | 1 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 6.0 | 0 | 1 | 0 | 1 | 0 (0) | MISSING |
| Marcellas Dial | CB | 1 | 1.0 (1.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Michael Taaffe | S | 10 | 95.4 (99.0 wk11) | 33 | 19 | 341 | 3 | 3 | 10.33 | 85.5 | 11.8 | 0 | 0 | 0 | 3 | 20 (263) | MISSING |
| Dante Trader | S | 9 | 85.2 (100.0 wk10) | 16 | 9 | 122 | 0 | 1 | 7.62 | 54.7 | 12.7 | 0 | 1 | 0 | 2 | 13 (237) | MISSING |
| Zayne Anderson | S | 8 | 33.9 (100.0 wk11) | 17 | 6 | 55 | 3 | 1 | 3.24 | 60.0 | 13.5 | 0 | 3 | 0 | 4 | 10 (166) | MISSING |
| Kyle Louis | S | 5 | 20.0 (17.0 wk11) | 3 | 2 | 11 | 0 | 0 | 3.67 | 72.9 | 8.7 | 0 | 0 | 0 | 0 | 1 (7) | MISSING |
| Julius Wood | S | 4 | 9.5 (4.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jacob Rodriguez | 10 | 51 | 34 | 299 | 3 | 5.86 | 85.3 | 0 |
| Jordyn Brooks | 10 | 45 | 29 | 249 | 1 | 5.53 | 86.3 | 2 |
| Willie Gay Jr. | 9 | 13 | 11 | 128 | 2 | 9.85 | 147.3 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | BUF | Z.Anderson | INT | K.Shakir | short_middle |
| 11 | BUF | J.Rodriguez | INT | K.Latu | short_middle |
| 11 | BUF | Z.Anderson | PBU | K.Latu | deep_right |
| 11 | BUF | Z.Anderson | PBU | K.Shakir | deep_right |
| 11 | BUF | J.Brents | PBU | K.Coleman | deep_right |
| 11 | BUF | C.Johnson | PBU | K.Shakir | short_right |
| 10 | IND | C.Johnson | INT | A.Ogletree | short_right |
| 10 | IND | M.Taaffe | INT | D.Burks | short_middle |
| 10 | IND | J.Brooks | PBU | A.Gould | short_right |
| 9 | DET | J.Marshall | DPI | — | deep_right |
| 9 | DET | J.Marshall | PBU | J.Williams | deep_left |
| 9 | DET | C.Johnson | INT | A.St. Brown | short_right |
| 9 | DET | C.Robinson | PBU | I.TeSlaa | short_middle |
| 7 | NYJ | J.Brents | DPI | — | unk_unk |
| 7 | NYJ | Z.Biggers | PBU | B.Allen | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Chris Johnson | CB | 52.5 | 39.4 | 421.3 | 8.02 | 2.7 | 81 (48) |
| Jacob Rodriguez | LB | 40.9 | 32.0 | 264.5 | 6.47 | 3.06 | 48 (18) |
| Jordyn Brooks | LB | 38.6 | 30.9 | 244.6 | 6.34 | 2.57 | 50 (25) |
| Julius Brents | CB | 34.7 | 25.5 | 302.6 | 8.72 | 2.3 | 38 (24) |
| Jason Marshall Jr. | CB | 33.3 | 24.7 | 286.5 | 8.6 | 1.88 | 20 (9) |
| Michael Taaffe | S | 26.4 | 19.3 | 254.6 | 9.64 | 1.78 | 19 (2) |
| Dante Trader Jr. | S | 18.6 | 13.9 | 197.3 | 10.61 | 1.6 | 8 (2) |
| Willie Gay Jr. | LB | 11.6 | 9.0 | 99.7 | 8.59 | 1.16 | 2 (1) |
| Zayne Anderson | S | 10.8 | 6.8 | 109.7 | 10.16 | 0.42 | 9 (5) |

### Upcoming: opposing receivers vs likely MIA defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | NYJ | G.Wilson (WR) | 19 | short_left 34%, short_right 28% | Chris Johnson (23%) | Julius Brents (20%) |
| 12 | 2026-11-29 | NYJ | A.Mitchell (WR) | 18 | short_left 29%, deep_right 27% | Jason Marshall Jr. (20%) | Chris Johnson (20%) |
| 12 | 2026-11-29 | NYJ | B.Hall (RB) | 11 | short_right 52%, short_left 38% | Jordyn Brooks (33%) | Jacob Rodriguez (30%) |
| 12 | 2026-11-29 | NYJ | O.Cooper (WR) | 11 | short_right 50%, short_left 25% | Chris Johnson (29%) | Julius Brents (20%) |
| 13 | 2026-12-06 | DEN | E.Engram (TE) | 13 | short_left 45%, short_right 32% | Zayne Anderson (18%) | Michael Taaffe (17%) |
| 13 | 2026-12-06 | DEN | C.Sutton (WR) | 11 | short_left 33%, short_right 33% | Chris Johnson (23%) | Julius Brents (21%) |
| 13 | 2026-12-06 | DEN | P.Bryant (WR) | 9 | short_right 43%, short_left 29% | Chris Johnson (27%) | Jason Marshall Jr. (19%) |
| 13 | 2026-12-06 | DEN | J.Coleman (RB) | 9 | short_right 53%, short_left 37% | Jordyn Brooks (33%) | Jacob Rodriguez (30%) |

Defender pool = MIA players with defensive snaps in their most recent game (2026_11_MIA_BUF); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Michael Taaffe | S | 43.1 | 31.0 | 404.7 | 9.39 | 7.61 | 223.7 | 7 |
| Dante Trader Jr. | S | 11.1 | 8.1 | 226.9 | 20.44 | 4.62 | 184.3 | 4 |
| Chris Johnson | CB | 33.0 | 24.9 | 308.0 | 9.33 | 4.15 | 151.7 | 8 |
| Jason Marshall Jr. | CB | 43.8 | 32.0 | 349.8 | 7.99 | 3.76 | 111.9 | 1 |
| Julius Brents | CB | 32.3 | 24.5 | 252.6 | 7.82 | 3.1 | 79.4 | 2 |
| Jacob Rodriguez | LB | 55.9 | 44.4 | 370.6 | 6.63 | 2.87 | 79.3 | 3 |
| Jordyn Brooks | LB | 51.8 | 40.0 | 287.6 | 5.55 | 1.69 | 48.1 | 2 |

### Rest of Week 12: receivers vs likely MIA window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | NYJ | G.Wilson (WR) | 19 | 13% | Jason Marshall Jr. (26%, 3.76) | Julius Brents (18%, 3.1) |
| 2026-11-29 | NYJ | A.Mitchell (WR) | 18 | 36% | Jason Marshall Jr. (21%, 3.76) | Chris Johnson (21%, 4.15) |
| 2026-11-29 | NYJ | B.Hall (RB) | 11 | 0% | Jacob Rodriguez (44%, 2.87) | Jordyn Brooks (24%, 1.69) |
| 2026-11-29 | NYJ | O.Cooper (WR) | 11 | 12% | Jason Marshall Jr. (28%, 3.76) | Chris Johnson (21%, 4.15) |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Jason Marshall (CB) 37 tgt, 67.6% catch, 9.38 ypt, rating 115.5 [GIVES UP EXPLOSIVES, WEAK LINK]
**Best / lockdown:** Michael Taaffe (S) 33 tgt, 57.6% catch, 10.33 ypt, rating 85.5 [GIVES UP EXPLOSIVES, TARGET MAGNET]
**Weak zones:** deep middle 20.3 ypt; deep right 17.4 ypt

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Julius Brents | CB | 9 | 33 | 19% | 69.7 | 7.82 | 11.22 | 0.584 | 102.8 | 1 | 0 | 2 | 35.8 |  | small sample (<35 tgts) |
| Chris Johnson | CB | 10 | 45 | 24% | 71.1 | 9.07 | 12.75 | 0.66 | 102.8 | 3 | 2 | 3 | 20.5 |  |  |
| Jason Marshall | CB | 9 | 37 | 21% | 67.6 | 9.38 | 13.88 | 0.766 | 115.5 | 2 | 0 | 1 | 18.5 | GIVES UP EXPLOSIVES, WEAK LINK |  |
| Michael Taaffe | S | 10 | 33 | 18% | 57.6 | 10.33 | 17.95 | 0.567 | 85.5 | 3 | 3 | 0 | 37.0 | GIVES UP EXPLOSIVES, TARGET MAGNET | small sample (<35 tgts) |
