# GB defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.5 | 24.1 | — |
| Zone % | 78.5 | 75.4 | — |
| Single-high / MOFC % | 34.7 | 36.5 | — |
| Two-high / MOFO % | 61.0 | 63.5 | — |
| Blitz % | 33.3 | 36.8 | 34.8 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 43.5 / 24.5, 72.0 | — | — |

Sharp YPT allowed: WR 7.2, TE 6.5, RB 5.9, **outside 7.6 vs slot 6.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #25 vs StatRankings #27; blitz rank Sharp #9 vs SR #9 (raw gaps: man -10.6 pts, blitz -3.5 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.3 | 148.3 | 7.31 | 10 | 0.096 | 15 |
| TE | 6.4 | 39.9 | 6.27 | 3 | 0.048 | 31 |
| RB | 5.6 | 32.5 | 5.76 | 2 | 0.1 | 19 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 30 | 15 | 432 | 3 | 4 | 14.4 | 11.46 | 5 | **WEAK** |
| deep middle | 11 | 5 | 99 | 1 | 0 | 9.0 | 14.39 | 30 |  |
| deep right | 21 | 9 | 229 | 1 | 2 | 10.9 | 12.14 | 19 |  |
| short left | 113 | 73 | 570 | 4 | 5 | 5.04 | 5.99 | 29 |  |
| short middle | 70 | 48 | 476 | 3 | 4 | 6.8 | 7.32 | 23 |  |
| short right | 110 | 90 | 621 | 3 | 0 | 5.65 | 6.02 | 23 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs GB: **2.93 yds** (league 2.93; rank 17/32 most allowed). WR 2.90, TE 3.14, cushion 5.91. Sample: 25 receiver-games, 205 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Keisean Nixon | CB | 11 | 96.9 (100.0 wk12) | 68 | 46 | 410 | 1 | 1 | 6.03 | 82.4 | 7.3 | 1 | 7 | 2 | 10 | 37 (356) | MISSING |
| Brandon Cisse | CB | 11 | 84.4 (100.0 wk12) | 45 | 25 | 362 | 3 | 1 | 8.04 | 94.9 | 11.2 | 1 | 7 | 2 | 10 | 20 (284) | MISSING |
| Carrington Valentine | CB | 9 | 22.1 (80.0 wk10) | 20 | 12 | 103 | 1 | 0 | 5.15 | 90.2 | 6.4 | 0 | 3 | 0 | 3 | 10 (78) | MISSING |
| Kamal Hadden | CB | 5 | 4.6 (1.0 wk12) | 4 | 3 | 37 | 0 | 0 | 9.25 | 103.1 | 10.5 | 0 | 0 | 0 | 0 | 2 (29) | MISSING |
| Benjamin St-Juste | CB | 2 | 10.5 (19.0 wk9) | 1 | 1 | 21 | 0 | 0 | 21.00 | 118.8 | 19.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Evan Williams | S | 11 | 99.7 (100.0 wk12) | 39 | 22 | 270 | 3 | 3 | 6.92 | 71.5 | 9.8 | 0 | 5 | 0 | 8 | 33 (430) | MISSING |
| Xavier McKinney | S | 11 | 97.2 (100.0 wk12) | 31 | 14 | 191 | 1 | 6 | 6.16 | 36.6 | 10.9 | 0 | 1 | 0 | 7 | 20 (221) | MISSING |
| Javon Bullard | S | 11 | 67.1 (31.0 wk12) | 46 | 27 | 219 | 3 | 0 | 4.76 | 92.6 | 7.2 | 0 | 6 | 0 | 6 | 20 (158) | MISSING |
| Kitan Oladapo | S | 3 | 11.7 (22.0 wk9) | 1 | 1 | 21 | 0 | 0 | 21.00 | 118.8 | 19.0 | 0 | 0 | 0 | 0 | 2 (42) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Isaiah McDuffie | 10 | 23 | 16 | 146 | 0 | 6.35 | 86.5 | 0 |
| Zaire Franklin | 6 | 16 | 12 | 129 | 1 | 8.06 | 119.0 | 1 |
| Ty'Ron Hopper | 9 | 16 | 12 | 91 | 1 | 5.69 | 69.5 | 4 |
| Edgerrin Cooper | 4 | 15 | 10 | 136 | 0 | 9.07 | 67.6 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | LA | T.Hopper | INT | T.Higbee | short_left |
| 12 | LA | B.Cisse | DPI | X.Smith | deep_middle |
| 10 | MIN | K.Nixon | PBU | J.Jefferson | short_middle |
| 10 | MIN | T.Hopper | PBU | J.Mason | short_right |
| 10 | MIN | K.Nixon | PBU | J.Jefferson | short_middle |
| 10 | MIN | X.McKinney | INT | T.Felton | deep_left |
| 10 | MIN | C.Valentine | PBU | J.Jefferson | short_left |
| 10 | MIN | E.Williams | PBU | T.Felton | short_left |
| 9 | NE | C.Valentine | PBU | M.Hollins | short_left |
| 9 | NE | N.Niemann | PBU | L.Larison | deep_right |
| 9 | NE | X.McKinney | INT | E.Raridon | short_left |
| 9 | NE | E.Williams | INT | K.Williams | deep_left |
| 9 | NE | X.McKinney | INT | M.Hollins | deep_left |
| 8 | CAR | D.Dennis-Sutton | PBU | T.McMillan | short_middle |
| 8 | CAR | X.McKinney | PBU | T.Tremble | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
