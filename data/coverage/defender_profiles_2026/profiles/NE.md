# NE defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 27.6 | 30.3 | — |
| Zone % | 66.6 | 67.7 | — |
| Single-high / MOFC % | 48.5 | 51.9 | — |
| Two-high / MOFO % | 47.6 | 48.1 | — |
| Blitz % | 35.8 | 38.1 | 35.3 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 37.4 / 29.6, 76.0 | — | — |

Sharp YPT allowed: WR 9.7, TE 6.2, RB 7.4, **outside 9.1 vs slot 11.9** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #2 vs StatRankings #19; blitz rank Sharp #6 vs SR #7 (raw gaps: man -2.7 pts, blitz -2.3 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.9 | 174.4 | 9.74 | 15 | 0.449 | 5 |
| TE | 7.2 | 44.7 | 6.21 | 2 | -0.034 | 24 |
| RB | 5.1 | 37.5 | 7.35 | 0 | 0.139 | 9 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 24 | 12 | 359 | 3 | 3 | 14.96 | 11.46 | 3 | **WEAK** |
| deep middle | 12 | 6 | 186 | 2 | 1 | 15.5 | 14.39 | 13 |  |
| deep right | 17 | 12 | 314 | 0 | 0 | 18.47 | 12.14 | 2 | **WEAK** |
| short left | 90 | 64 | 587 | 5 | 0 | 6.52 | 5.99 | 8 | **WEAK** |
| short middle | 56 | 43 | 470 | 4 | 2 | 8.39 | 7.32 | 5 | **WEAK** |
| short right | 103 | 77 | 650 | 3 | 1 | 6.31 | 6.02 | 12 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NE: **2.89 yds** (league 2.93; rank 21/32 most allowed). WR 2.97, TE 2.65, cushion 6.03. Sample: 26 receiver-games, 182 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Marcus Jones | CB | 10 | 81.1 (90.0 wk10) | 45 | 30 | 385 | 3 | 1 | 8.56 | 106.2 | 7.7 | 1 | 5 | 0 | 6 | 25 (264) | MISSING |
| Christian Gonzalez | CB | 8 | 95.8 (90.0 wk10) | 48 | 31 | 472 | 3 | 1 | 9.83 | 109.0 | 10.3 | 2 | 6 | 1 | 8 | 25 (339) | MISSING |
| Carlton Davis | CB | 5 | 87.0 (53.0 wk9) | 32 | 24 | 246 | 0 | 0 | 7.69 | 96.6 | 7.3 | 1 | 2 | 0 | 2 | 19 (204) | MISSING |
| Charles Woods | CB | 9 | 44.1 (48.0 wk10) | 31 | 19 | 267 | 3 | 1 | 8.61 | 107.9 | 10.7 | 1 | 2 | 0 | 3 | 16 (204) | MISSING |
| Kindle Vildor | CB | 3 | 29.7 (2.0 wk6) | 7 | 4 | 59 | 0 | 0 | 8.43 | 84.8 | 13.4 | 0 | 1 | 0 | 1 | 4 (64) | MISSING |
| Karon Prunty | CB | 3 | 15.7 (13.0 wk10) | 3 | 3 | 33 | 1 | 0 | 11.00 | 152.1 | 8.3 | 0 | 0 | 0 | 0 | 1 (9) | MISSING |
| Channing Canada | CB | 4 | 6.5 (10.0 wk10) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Kevin Byard | S | 10 | 95.1 (87.0 wk10) | 27 | 15 | 233 | 2 | 2 | 8.63 | 78.2 | 10.4 | 0 | 3 | 3 | 8 | 18 (294) | MISSING |
| Craig Woodson | S | 9 | 91.2 (80.0 wk10) | 27 | 15 | 240 | 2 | 1 | 8.89 | 94.7 | 10.8 | 1 | 2 | 0 | 3 | 12 (150) | MISSING |
| Jaylen Reed | S | 8 | 33.2 (28.0 wk10) | 9 | 7 | 75 | 1 | 0 | 8.33 | 138.4 | 7.6 | 0 | 0 | 0 | 0 | 4 (35) | MISSING |
| Mike Brown | S | 5 | 16.6 (13.0 wk10) | 1 | 1 | 11 | 0 | 0 | 11.00 | 112.5 | -2.0 | 0 | 0 | 0 | 0 | 2 (19) | MISSING |
| Dell Pettus | S | 1 | 40.0 (40.0 wk1) | 3 | 3 | 26 | 0 | 0 | 8.67 | 102.8 | 2.7 | 0 | 0 | 0 | 0 | 2 (18) | MISSING |
| Brenden Schooler | S | 2 | 9.0 (1.0 wk7) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Elliott Davison | S | 1 | 17.0 (17.0 wk5) | 3 | 1 | 6 | 0 | 0 | 2.00 | 42.4 | 6.3 | 0 | 1 | 0 | 1 | 1 (6) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Christian Elliss | 10 | 41 | 31 | 288 | 2 | 7.02 | 110.6 | 1 |
| Robert Spillane | 10 | 28 | 16 | 159 | 0 | 5.68 | 73.4 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 10 | DET | K.Byard | INT | J.Williams | short_middle |
| 10 | DET | K.Byard | PBU | S.LaPorta | short_middle |
| 10 | DET | C.Gonzalez | INT | A.St. Brown | deep_left |
| 9 | GB | C.Gonzalez | PBU | S.Williams | short_middle |
| 9 | GB | C.Davis | PBU | C.Watson | deep_right |
| 9 | GB | C.Gonzalez | DPI | — | short_right |
| 8 | MIA | R.Spillane | PBU | O.Gordon | short_middle |
| 8 | MIA | R.Spillane | PBU | G.Dulcich | short_middle |
| 8 | MIA | K.Byard | INT | C.Douglas | deep_middle |
| 8 | MIA | M.Jones | PBU | M.Washington | short_left |
| 8 | MIA | E.Ponder | PBU | W.Kacmarek | short_right |
| 7 | CHI | C.Woodson | PBU | C.Loveland | short_right |
| 6 | NYJ | C.Elliss | PBU | M.Taylor | short_left |
| 6 | NYJ | K.Byard | DPI | T.Patrick | deep_left |
| 6 | NYJ | C.Woods | INT | K.Sadiq | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Christian Gonzalez | CB | 49.3 | 35.3 | 526.2 | 10.67 | 3.65 | 67 (49) |
| Marcus Jones | CB | 42.9 | 30.4 | 363.4 | 8.47 | 2.93 | 51 (8) |
| Christian Elliss | LB | 27.2 | 20.5 | 186.9 | 6.87 | 0.87 | 44 (3) |
| Carlton Davis III | CB | 25.1 | 19.1 | 217.7 | 8.67 | 1.66 | 42 (12) |
| Kevin Byard | S | 24.1 | 15.0 | 211.2 | 8.76 | 1.41 | 26 (3) |
| Robert Spillane | LB | 24.1 | 18.0 | 173.2 | 7.19 | 0.79 | 20 (2) |
| Charles Woods | CB | 23.8 | 15.3 | 195.3 | 8.21 | 1.23 | 15 (11) |
| Craig Woodson | S | 20.9 | 13.9 | 188.4 | 9.01 | 1.47 | 21 (6) |
| Elijah Ponder | LB | 17.0 | 12.3 | 118.0 | 6.94 | 0.57 | 1 (0) |
| Gabe Jacas | LB | 12.8 | 9.4 | 95.1 | 7.43 | 0.44 | 3 (0) |
| Dre'Mont Jones | LB | 11.7 | 8.7 | 88.3 | 7.55 | 0.39 | 0 (0) |
| Kindle Vildor | CB | 6.4 | 4.3 | 53.0 | 8.28 | 0.21 | 11 (5) |

### Upcoming: opposing receivers vs likely NE defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | LAC | T.Harris (WR) | 14 | short_right 31%, short_left 29% | Christian Gonzalez (26%) | Marcus Jones (22%) |
| 12 | 2026-11-29 | LAC | L.McConkey (WR) | 8 | short_right 31%, short_middle 22% | Christian Gonzalez (24%) | Marcus Jones (22%) |
| 12 | 2026-11-29 | LAC | C.Kolar (TE) | 7 | short_right 62%, short_middle 21% | Kevin Byard (13%) | Christian Elliss (11%) |
| 12 | 2026-11-29 | LAC | Q.Johnston (WR) | 7 | short_right 30%, short_left 21% | Christian Gonzalez (26%) | Marcus Jones (21%) |
| 13 | 2026-12-06 | BUF | D.Moore (WR) | 27 | short_left 33%, short_right 24% | Christian Gonzalez (23%) | Marcus Jones (22%) |
| 13 | 2026-12-06 | BUF | K.Shakir (WR) | 22 | short_right 45%, short_middle 27% | Christian Gonzalez (22%) | Marcus Jones (21%) |
| 13 | 2026-12-06 | BUF | K.Coleman (WR) | 14 | short_right 32%, short_left 22% | Christian Gonzalez (26%) | Marcus Jones (21%) |
| 13 | 2026-12-06 | BUF | T.Johnson (RB) | 13 | short_right 54%, short_left 39% | Christian Elliss (19%) | Elijah Ponder (13%) |

Defender pool = NE players with defensive snaps in their most recent game (2026_10_NE_DET); check inactives before use.
