# BAL defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 15.6 | 30.8 | — |
| Zone % | 77.3 | 69.2 | — |
| Single-high / MOFC % | 38.8 | 45.6 | — |
| Two-high / MOFO % | 58.7 | 54.4 | — |
| Blitz % | 31.3 | 34.7 | 33.4 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 50.2 / 20.7, 74.0 | — | — |

Sharp YPT allowed: WR 9.1, TE 8.8, RB 3.1, **outside 9.3 vs slot 10.0** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #20 vs StatRankings #18; blitz rank Sharp #11 vs SR #13 (raw gaps: man -15.2 pts, blitz -3.4 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.8 | 162.5 | 9.12 | 7 | 0.28 | 8 |
| TE | 6.2 | 54.3 | 8.78 | 7 | 0.312 | 15 |
| RB | 5.1 | 16.0 | 3.14 | 0 | -0.36 | 32 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 18 | 10 | 314 | 3 | 0 | 17.44 | 11.46 | 1 | **WEAK** |
| deep middle | 15 | 9 | 267 | 1 | 0 | 17.8 | 14.39 | 5 | **WEAK** |
| deep right | 18 | 12 | 342 | 1 | 0 | 19.0 | 12.14 | 1 | **WEAK** |
| short left | 100 | 69 | 544 | 2 | 0 | 5.44 | 5.99 | 25 |  |
| short middle | 64 | 46 | 478 | 4 | 4 | 7.47 | 7.32 | 11 |  |
| short right | 106 | 75 | 615 | 3 | 1 | 5.8 | 6.02 | 21 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs BAL: **2.88 yds** (league 2.93; rank 22/32 most allowed). WR 2.85, TE 3.05, cushion 5.71. Sample: 26 receiver-games, 183 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nate Wiggins | CB | 10 | 94.4 (94.0 wk11) | 42 | 22 | 233 | 1 | 0 | 5.55 | 76.8 | 9.7 | 1 | 5 | 1 | 6 | 18 (174) | MISSING |
| Marlon Humphrey | CB | 10 | 79.0 (74.0 wk10) | 49 | 27 | 395 | 1 | 0 | 8.06 | 88.4 | 13.3 | 2 | 9 | 0 | 9 | 26 (398) | MISSING |
| Chidobe Awuzie | CB | 11 | 29.7 (44.0 wk11) | 14 | 10 | 135 | 1 | 0 | 9.64 | 125.6 | 13.3 | 0 | 2 | 1 | 3 | 7 (68) | MISSING |
| Keyon Martin | CB | 8 | 29.4 (30.0 wk11) | 13 | 11 | 64 | 2 | 0 | 4.92 | 126.8 | 2.8 | 0 | 1 | 1 | 2 | 9 (76) | MISSING |
| Chandler Rivers | CB | 4 | 38.2 (30.0 wk5) | 16 | 11 | 132 | 1 | 0 | 8.25 | 114.6 | 8.0 | 1 | 0 | 0 | 0 | 6 (55) | MISSING |
| T.J. Tampa | CB | 4 | 34.0 (56.0 wk11) | 8 | 5 | 78 | 1 | 1 | 9.75 | 94.8 | 10.0 | 0 | 1 | 0 | 2 | 4 (58) | MISSING |
| Malaki Starks | S | 11 | 97.3 (93.0 wk11) | 26 | 20 | 331 | 4 | 0 | 12.73 | 157.9 | 9.1 | 0 | 2 | 1 | 3 | 19 (243) | MISSING |
| Kyle Hamilton | S | 11 | 93.2 (97.0 wk11) | 43 | 31 | 384 | 1 | 1 | 8.93 | 97.4 | 6.6 | 2 | 4 | 1 | 6 | 33 (411) | MISSING |
| Jaylinn Hawkins | S | 6 | 81.3 (87.0 wk6) | 18 | 12 | 213 | 1 | 0 | 11.83 | 125.5 | 6.6 | 1 | 0 | 0 | 0 | 15 (216) | MISSING |
| K'Von Wallace | S | 6 | 31.7 (38.0 wk11) | 9 | 8 | 121 | 0 | 0 | 13.44 | 118.8 | 8.4 | 0 | 0 | 1 | 1 | 8 (117) | MISSING |
| Keondre Jackson | S | 6 | 22.8 (20.0 wk11) | 4 | 3 | 39 | 1 | 0 | 9.75 | 144.8 | 2.2 | 0 | 0 | 0 | 0 | 2 (48) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Roquan Smith | 11 | 41 | 24 | 258 | 0 | 6.29 | 66.9 | 2 |
| Trenton Simpson | 11 | 29 | 21 | 144 | 0 | 4.97 | 68.8 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | CAR | C.Campbell | PBU | T.McMillan | deep_middle |
| 11 | CAR | T.Tampa | INT | T.McMillan | short_right |
| 11 | CAR | T.Tampa | PBU | J.Coker | short_left |
| 11 | CAR | N.Wiggins | PBU | J.Coker | short_middle |
| 11 | CAR | T.Hendrickson | PBU | T.McMillan | short_left |
| 10 | LAC | M.Starks | PBU | T.Wease | short_left |
| 9 | JAX | N.Madubuike | PBU | J.Meyers | short_left |
| 9 | JAX | K.Hamilton | PBU | P.Washington | short_left |
| 9 | JAX | N.Madubuike | PBU | L.Allen | short_left |
| 9 | JAX | M.Humphrey | PBU | P.Washington | short_left |
| 9 | JAX | B.Washington | PBU | P.Washington | short_right |
| 9 | JAX | M.Humphrey | PBU | P.Washington | short_right |
| 8 | BUF | M.Humphrey | PBU | D.Moore | short_left |
| 8 | BUF | R.Smith | PBU | K.Shakir | short_middle |
| 8 | BUF | R.Smith | PBU | D.Moore | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
