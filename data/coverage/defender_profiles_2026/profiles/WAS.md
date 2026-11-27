# WAS defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.5 | 20.6 | — |
| Zone % | 78.5 | 79.1 | — |
| Single-high / MOFC % | 32.1 | 35.8 | — |
| Two-high / MOFO % | 62.6 | 64.2 | — |
| Blitz % | 40.8 | 44.5 | 42.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 43.9 / 24.4, 60.0 | — | — |

Sharp YPT allowed: WR 7.4, TE 8.8, RB 5.8, **outside 8.7 vs slot 6.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #25 vs StatRankings #31; blitz rank Sharp #3 vs SR #3 (raw gaps: man -7.1 pts, blitz -3.7 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.2 | 142.3 | 7.41 | 10 | 0.117 | 20 |
| TE | 9.1 | 80.4 | 8.84 | 9 | 0.343 | 1 |
| RB | 7.2 | 41.4 | 5.75 | 0 | 0.026 | 3 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 17 | 9 | 216 | 1 | 1 | 12.71 | 11.46 | 15 |  |
| deep middle | 16 | 8 | 214 | 2 | 0 | 13.38 | 14.39 | 19 |  |
| deep right | 28 | 14 | 431 | 2 | 1 | 15.39 | 12.14 | 6 | **WEAK** |
| short left | 121 | 80 | 603 | 5 | 1 | 4.98 | 5.99 | 30 |  |
| short middle | 72 | 58 | 619 | 5 | 1 | 8.6 | 7.32 | 2 | **WEAK** |
| short right | 101 | 76 | 558 | 4 | 2 | 5.52 | 6.02 | 27 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs WAS: **3.05 yds** (league 2.93; rank 9/32 most allowed). WR 2.98, TE 3.18, cushion 5.97. Sample: 24 receiver-games, 190 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Amik Robertson | CB | 9 | 98.4 (98.0 wk10) | 66 | 42 | 451 | 1 | 0 | 6.83 | 88.6 | 6.8 | 2 | 10 | 1 | 11 | 33 (310) | MISSING |
| Rasul Douglas | CB | 10 | 58.1 (100.0 wk11) | 48 | 26 | 308 | 1 | 3 | 6.42 | 54.9 | 10.6 | 0 | 6 | 0 | 9 | 26 (189) | MISSING |
| Trey Amos | CB | 5 | 87.4 (100.0 wk11) | 30 | 16 | 195 | 2 | 0 | 6.50 | 95.8 | 12.0 | 0 | 2 | 1 | 3 | 13 (166) | MISSING |
| Mike Sainristil | CB | 8 | 36.8 (7.0 wk11) | 21 | 15 | 199 | 5 | 0 | 9.48 | 140.7 | 13.8 | 1 | 0 | 0 | 0 | 8 (72) | MISSING |
| Fabian Moreau | CB | 4 | 28.7 (17.0 wk11) | 7 | 6 | 40 | 1 | 0 | 5.71 | 130.1 | 5.9 | 0 | 1 | 0 | 1 | 5 (39) | MISSING |
| Jeremy Reaves | S | 10 | 88.0 (100.0 wk11) | 36 | 21 | 303 | 3 | 0 | 8.42 | 113.5 | 10.8 | 1 | 5 | 1 | 6 | 28 (410) | MISSING |
| Nick Cross | S | 7 | 98.1 (100.0 wk11) | 28 | 18 | 182 | 2 | 1 | 6.50 | 91.7 | 7.6 | 0 | 2 | 0 | 3 | 14 (150) | MISSING |
| Quan Martin | S | 10 | 62.5 (74.0 wk11) | 18 | 10 | 170 | 0 | 0 | 9.44 | 87.7 | 13.2 | 0 | 1 | 1 | 2 | 23 (361) | MISSING |
| Percy Butler | S | 4 | 20.5 (25.0 wk10) | 5 | 0 | 12 | 0 | 0 | 2.40 | 39.6 | 11.0 | 0 | 1 | 0 | 1 | 2 (37) | MISSING |
| Darren Hall | S | 1 | 1.0 (1.0 wk5) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Sonny Styles | 10 | 50 | 34 | 325 | 1 | 6.50 | 84.2 | 3 |
| Frankie Luvu | 8 | 31 | 20 | 190 | 0 | 6.13 | 81.4 | 1 |
| K'Lavon Chaisson | 10 | 14 | 12 | 147 | 1 | 10.50 | 134.2 | 0 |
| Kain Medrano | 5 | 12 | 9 | 83 | 1 | 6.92 | 86.5 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | CIN | T.Amos | DPI | J.Chase | short_right |
| 11 | CIN | R.Douglas | PBU | J.Chase | short_left |
| 11 | CIN | R.Douglas | PBU | C.Young | short_right |
| 11 | CIN | J.Reaves | PBU | M.Gesicki | short_middle |
| 10 | NYG | R.Douglas | INT | M.Nabers | deep_right |
| 10 | NYG | J.Reaves | PBU | D.Mooney | deep_right |
| 10 | NYG | P.Butler | PBU | T.Johnson | short_left |
| 10 | NYG | J.Reaves | DPI | I.Likely | short_left |
| 10 | NYG | A.Robertson | PBU | D.Mooney | short_left |
| 9 | LA | N.Cross | INT | P.Nacua | short_right |
| 9 | LA | N.Cross | PBU | T.Higbee | short_middle |
| 9 | LA | N.Cross | PBU | T.Higbee | deep_right |
| 9 | LA | A.Robertson | PBU | B.Corum | short_left |
| 9 | LA | Q.Martin | PBU | T.Atwell | short_middle |
| 9 | LA | S.Styles | DPI | T.Higbee | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Amik Robertson | CB | 59.7 | 39.0 | 376.5 | 6.31 | 3.34 | 89 (65) |
| Sonny Styles | LB | 41.1 | 29.7 | 328.6 | 8.0 | 2.26 | 69 (19) |
| Rasul Douglas | CB | 41.0 | 26.4 | 248.0 | 6.05 | 1.91 | 44 (29) |
| Jeremy Reaves | S | 29.9 | 21.3 | 296.6 | 9.92 | 2.14 | 24 (0) |
| Trey Amos | CB | 26.7 | 17.4 | 211.4 | 7.92 | 1.29 | 35 (22) |
| Frankie Luvu | LB | 25.6 | 18.9 | 168.6 | 6.59 | 0.56 | 38 (4) |
| Quan Martin | S | 21.3 | 14.3 | 215.7 | 10.13 | 1.61 | 9 (2) |
| K'Lavon Chaisson | LB | 20.2 | 15.0 | 131.4 | 6.5 | 0.75 | 9 (0) |
| Nick Cross | S | 19.2 | 12.6 | 186.7 | 9.72 | 1.4 | 22 (5) |
| Odafe Oweh | LB | 17.0 | 12.3 | 113.2 | 6.66 | 0.72 | 5 (0) |
| Mike Sainristil | CB | 14.3 | 9.9 | 99.2 | 6.94 | 1.09 | 5 (0) |
| Dorance Armstrong | LB | 13.2 | 9.8 | 83.5 | 6.33 | 0.45 | 0 (0) |

### Upcoming: opposing receivers vs likely WAS defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | ARI | T.McBride (TE) | 27 | short_right 50%, short_left 24% | Nick Cross (15%) | Jeremy Reaves (13%) |
| 12 | 2026-11-29 | ARI | S.Fehoko (WR) | 8 | short_right 44%, deep_right 33% | Rasul Douglas (24%) | Trey Amos (15%) |
| 12 | 2026-11-29 | ARI | H.Wallace (WR) | 8 | short_left 38%, short_right 25% | Trey Amos (29%) | Rasul Douglas (26%) |
| 12 | 2026-11-29 | ARI | Mi.Wilson (WR) | 7 | short_right 41%, deep_right 19% | Rasul Douglas (26%) | Trey Amos (23%) |
| 13 | 2026-12-06 | TEN | E.Ayomanor (WR) | 13 | short_left 33%, short_right 33% | Rasul Douglas (26%) | Trey Amos (25%) |
| 13 | 2026-12-06 | TEN | T.Pollard (RB) | 10 | short_left 35%, short_right 32% | Frankie Luvu (20%) | Sonny Styles (17%) |
| 13 | 2026-12-06 | TEN | C.Dike (WR) | 10 | short_left 39%, short_right 30% | Rasul Douglas (27%) | Trey Amos (23%) |
| 13 | 2026-12-06 | TEN | G.Helm (TE) | 7 | short_left 52%, short_middle 24% | Nick Cross (14%) | Jeremy Reaves (14%) |

Defender pool = WAS players with defensive snaps in their most recent game (2026_11_CIN_WAS); check inactives before use.
