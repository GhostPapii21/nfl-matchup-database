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
