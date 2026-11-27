# NO defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 16.9 | 38.0 | — |
| Zone % | 74.2 | 59.9 | — |
| Single-high / MOFC % | 64.2 | 66.2 | — |
| Two-high / MOFO % | 32.2 | 33.8 | — |
| Blitz % | 34.4 | 39.7 | 37.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 43.5 / 23.0, 70.0 | — | — |

Sharp YPT allowed: WR 8.5, TE 8.0, RB 7.4, **outside 8.6 vs slot 8.9** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #19 vs StatRankings #11; blitz rank Sharp #8 vs SR #5 (raw gaps: man -21.1 pts, blitz -5.3 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 16.5 | 139.5 | 8.45 | 7 | 0.123 | 21 |
| TE | 7.9 | 64.1 | 8.11 | 6 | 0.381 | 6 |
| RB | 5.3 | 39.0 | 7.36 | 2 | 0.105 | 7 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 25 | 15 | 431 | 1 | 1 | 17.24 | 11.46 | 2 | **WEAK** |
| deep middle | 12 | 6 | 183 | 2 | 1 | 15.25 | 14.39 | 14 |  |
| deep right | 24 | 10 | 285 | 2 | 0 | 11.88 | 12.14 | 18 |  |
| short left | 97 | 69 | 587 | 5 | 1 | 6.05 | 5.99 | 14 |  |
| short middle | 58 | 43 | 371 | 1 | 1 | 6.4 | 7.32 | 29 |  |
| short right | 81 | 60 | 569 | 4 | 1 | 7.02 | 6.02 | 3 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NO: **2.97 yds** (league 2.93; rank 15/32 most allowed). WR 2.94, TE 3.03, cushion 6.63. Sample: 18 receiver-games, 150 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kool-Aid McKinstry | CB | 10 | 94.0 (100.0 wk11) | 47 | 28 | 392 | 2 | 0 | 8.34 | 100.7 | 11.3 | 1 | 7 | 1 | 8 | 23 (314) | MISSING |
| Quincy Riley | CB | 10 | 68.3 (100.0 wk11) | 36 | 21 | 275 | 4 | 0 | 7.64 | 119.6 | 10.3 | 2 | 5 | 0 | 5 | 15 (171) | MISSING |
| Martin Emerson | CB | 7 | 52.9 (57.0 wk10) | 27 | 14 | 247 | 1 | 2 | 9.15 | 64.9 | 11.6 | 1 | 2 | 2 | 6 | 16 (194) | MISSING |
| Jordan Howden | DB | 8 | 29.1 (100.0 wk11) | 6 | 2 | 32 | 0 | 0 | 5.33 | 52.1 | 20.0 | 0 | 1 | 0 | 1 | 3 (70) | MISSING |
| Lorenzo Styles Jr. | DB | 1 | 3.0 (3.0 wk6) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Julian Blackmon | S | 10 | 97.6 (100.0 wk11) | 26 | 16 | 268 | 4 | 2 | 10.31 | 103.8 | 16.4 | 1 | 0 | 0 | 2 | 17 (251) | MISSING |
| Justin Reid | S | 9 | 89.9 (79.0 wk10) | 35 | 24 | 328 | 3 | 0 | 9.37 | 126.8 | 7.1 | 1 | 0 | 0 | 0 | 21 (241) | MISSING |
| Jonas Sanker | S | 10 | 69.6 (64.0 wk11) | 50 | 32 | 336 | 1 | 0 | 6.72 | 90.1 | 6.2 | 1 | 4 | 1 | 5 | 26 (305) | MISSING |
| Michael Reid | S | 1 | 2.0 (2.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Kaden Elliss | 7 | 33 | 26 | 280 | 0 | 8.48 | 102.0 | 2 |
| Pete Werner | 9 | 32 | 22 | 201 | 1 | 6.28 | 96.0 | 2 |
| Danny Stutsman | 9 | 13 | 9 | 80 | 0 | 6.15 | 53.4 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | CHI | K.McKinstry | PBU | K.Raymond | short_right |
| 11 | CHI | D.Stutsman | INT | L.Burden | short_middle |
| 11 | CHI | J.Howden | PBU | K.Raymond | deep_middle |
| 10 | CAR | K.McKinstry | DPI | J.Coker | short_middle |
| 10 | CAR | J.Sanker | PBU | J.Coker | short_middle |
| 10 | CAR | K.Elliss | PBU | T.McMillan | short_left |
| 10 | CAR | M.Emerson | DPI | T.McMillan | short_left |
| 10 | CAR | Q.Riley | PBU | T.McMillan | short_middle |
| 10 | CAR | Q.Riley | PBU | T.McMillan | deep_right |
| 10 | CAR | J.Sanker | PBU | J.Coker | short_left |
| 9 | CLE | C.Granderson | PBU | D.Sampson | short_left |
| 9 | CLE | C.Young | PBU | D.Sampson | short_left |
| 9 | CLE | K.Boyd | PBU | D.Sampson | short_right |
| 9 | CLE | A.Jennings | PBU | M.Corley | short_left |
| 9 | CLE | J.Sanker | PBU | B.Whiteheart | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
