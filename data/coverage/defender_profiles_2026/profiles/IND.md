# IND defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 23.3 | 44.3 | — |
| Zone % | 70.6 | 55.5 | — |
| Single-high / MOFC % | 47.9 | 56.0 | — |
| Two-high / MOFO % | 47.7 | 44.0 | — |
| Blitz % | 21.1 | 22.7 | 21.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 37.4 / 25.2, 66.0 | — | — |

Sharp YPT allowed: WR 8.8, TE 7.4, RB 7.3, **outside 8.6 vs slot 10.4** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #8 vs StatRankings #3; blitz rank Sharp #29 vs SR #31 (raw gaps: man -21.0 pts, blitz -1.6 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 16.7 | 148.0 | 8.85 | 10 | 0.182 | 16 |
| TE | 6.2 | 45.5 | 7.35 | 8 | 0.236 | 22 |
| RB | 5.5 | 40.1 | 7.35 | 2 | 0.195 | 6 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 18 | 7 | 257 | 2 | 0 | 14.28 | 11.46 | 8 | **WEAK** |
| deep middle | 9 | 6 | 121 | 1 | 0 | 13.44 | 14.39 | 18 |  |
| deep right | 40 | 19 | 600 | 3 | 2 | 15.0 | 12.14 | 8 | **WEAK** |
| short left | 87 | 63 | 525 | 3 | 0 | 6.03 | 5.99 | 17 |  |
| short middle | 63 | 39 | 472 | 3 | 0 | 7.49 | 7.32 | 10 |  |
| short right | 96 | 67 | 607 | 8 | 1 | 6.32 | 6.02 | 11 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs IND: **2.68 yds** (league 2.93; rank 26/32 most allowed). WR 2.64, TE 2.82, cushion 6.19. Sample: 18 receiver-games, 136 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Charvarius Ward | CB | 10 | 87.2 (51.0 wk10) | 45 | 19 | 283 | 1 | 0 | 6.29 | 70.9 | 16.0 | 1 | 8 | 1 | 9 | 11 (136) | MISSING |
| Sauce Gardner | CB | 9 | 87.2 (59.0 wk10) | 33 | 19 | 331 | 1 | 0 | 10.03 | 102.0 | 13.0 | 1 | 7 | 2 | 9 | 21 (323) | MISSING |
| Justin Walley | CB | 9 | 75.2 (94.0 wk11) | 50 | 33 | 355 | 2 | 0 | 7.10 | 100.0 | 6.2 | 1 | 5 | 0 | 5 | 23 (191) | MISSING |
| Kenneth Harris | CB | 6 | 34.7 (42.0 wk11) | 11 | 5 | 132 | 1 | 0 | 12.00 | 120.3 | 16.3 | 1 | 0 | 0 | 0 | 0 (0) | MISSING |
| Kapena Gushiken | CB | 6 | 31.3 (71.0 wk11) | 6 | 5 | 31 | 0 | 0 | 5.17 | 88.2 | 4.5 | 0 | 1 | 1 | 2 | 5 (34) | MISSING |
| Cam Taylor-Britt | CB | 6 | 25.0 (42.0 wk7) | 8 | 4 | 41 | 2 | 0 | 5.12 | 104.7 | 9.9 | 0 | 2 | 1 | 3 | 3 (47) | MISSING |
| Johnathan Edwards | CB | 2 | 35.0 (64.0 wk11) | 2 | 2 | 19 | 0 | 0 | 9.50 | 106.2 | 6.0 | 0 | 0 | 0 | 0 | 1 (11) | MISSING |
| Camryn Bynum | S | 11 | 99.3 (100.0 wk11) | 27 | 18 | 289 | 4 | 1 | 10.70 | 126.4 | 12.0 | 1 | 3 | 0 | 4 | 14 (237) | MISSING |
| A.J. Haulcy | S | 10 | 82.5 (77.0 wk11) | 31 | 12 | 299 | 5 | 1 | 9.65 | 100.7 | 12.7 | 2 | 2 | 0 | 3 | 15 (232) | MISSING |
| Hunter Wohler | S | 9 | 29.0 (23.0 wk11) | 8 | 7 | 99 | 1 | 0 | 12.38 | 157.8 | 10.4 | 0 | 0 | 0 | 0 | 5 (91) | MISSING |
| Jonathan Owens | S | 7 | 2.9 (2.0 wk11) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Bryce Boettcher | 9 | 23 | 14 | 184 | 2 | 8.00 | 115.1 | 0 |
| Akeem Davis-Gaither | 8 | 21 | 18 | 190 | 0 | 9.05 | 104.4 | 1 |
| CJ Allen | 8 | 19 | 12 | 88 | 1 | 4.63 | 91.6 | 2 |
| Jaylon Carlies | 7 | 14 | 12 | 202 | 1 | 14.43 | 112.8 | 0 |
| Austin Ajiake | 8 | 12 | 8 | 47 | 0 | 3.92 | 74.0 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | HOU | A.Ajiake | PBU | D.Montgomery | short_middle |
| 11 | HOU | J.Tuimoloau | PBU | X.Hutchinson | short_right |
| 11 | HOU | A.Haulcy | INT | N.Collins | deep_right |
| 10 | MIA | J.Tuimoloau | PBU | K.Coleman | short_middle |
| 10 | MIA | G.Stewart | PBU | C.Douglas | short_middle |
| 10 | MIA | J.Walley | PBU | C.Douglas | deep_right |
| 10 | MIA | K.Harris | DPI | C.Douglas | short_left |
| 10 | MIA | G.Stewart | PBU | O.Gordon | short_middle |
| 10 | MIA | C.Ward | PBU | K.Coleman | short_right |
| 10 | MIA | G.Stewart | PBU | G.Dulcich | short_left |
| 10 | MIA | A.Gardner | DPI | K.Coleman | short_left |
| 10 | MIA | C.Ward | PBU | K.Coleman | short_right |
| 10 | MIA | C.Allen | PBU | K.Coleman | short_middle |
| 10 | MIA | J.Walley | PBU | C.Douglas | short_right |
| 9 | DAL | K.Gushiken | DPI | R.Flournoy | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
