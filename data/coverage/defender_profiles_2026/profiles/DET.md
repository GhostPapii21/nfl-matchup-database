# DET defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 20.3 | 38.2 | — |
| Zone % | 74.8 | 59.2 | — |
| Single-high / MOFC % | 48.5 | 57.4 | — |
| Two-high / MOFO % | 49.0 | 42.6 | — |
| Blitz % | 22.1 | 29.8 | 27.3 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 47.8 / 26.6, 54.0 | — | — |

Sharp YPT allowed: WR 7.5, TE 7.9, RB 6.0, **outside 7.3 vs slot 8.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #13 vs StatRankings #10; blitz rank Sharp #27 vs SR #19 (raw gaps: man -17.9 pts, blitz -7.7 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.2 | 150.5 | 7.46 | 10 | 0.268 | 13 |
| TE | 9.5 | 73.3 | 7.75 | 11 | 0.326 | 3 |
| RB | 6.0 | 41.1 | 6.85 | 2 | 0.229 | 4 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 22 | 6 | 146 | 0 | 1 | 6.64 | 11.46 | 31 |  |
| deep middle | 18 | 10 | 296 | 2 | 2 | 16.44 | 14.39 | 11 |  |
| deep right | 38 | 18 | 473 | 5 | 1 | 12.45 | 12.14 | 16 |  |
| short left | 113 | 76 | 542 | 4 | 2 | 4.8 | 5.99 | 32 |  |
| short middle | 60 | 51 | 537 | 3 | 1 | 8.95 | 7.32 | 1 | **WEAK** |
| short right | 142 | 107 | 927 | 9 | 0 | 6.53 | 6.02 | 7 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs DET: **2.67 yds** (league 2.93; rank 27/32 most allowed). WR 2.52, TE 3.08, cushion 5.21. Sample: 33 receiver-games, 253 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Roger McCreary | CB | 11 | 83.8 (89.0 wk12) | 63 | 37 | 469 | 4 | 1 | 7.44 | 96.6 | 10.0 | 2 | 13 | 1 | 15 | 32 (452) | MISSING |
| D.J. Reed | CB | 8 | 87.1 (39.0 wk12) | 36 | 20 | 327 | 2 | 1 | 9.08 | 93.2 | 14.0 | 2 | 6 | 2 | 9 | 25 (349) | MISSING |
| Rock Ya-Sin | CB | 9 | 69.2 (92.0 wk12) | 42 | 25 | 208 | 2 | 0 | 4.95 | 88.2 | 10.0 | 1 | 1 | 1 | 2 | 24 (187) | MISSING |
| Keith Abney | CB | 5 | 44.8 (11.0 wk9) | 9 | 4 | 42 | 0 | 1 | 4.67 | 19.0 | 15.2 | 0 | 1 | 0 | 2 | 5 (51) | MISSING |
| Ennis Rakestraw | CB | 7 | 28.6 (8.0 wk10) | 22 | 13 | 169 | 0 | 0 | 7.68 | 83.3 | 9.7 | 1 | 2 | 1 | 3 | 8 (121) | MISSING |
| Khalil Dorsey | CB | 6 | 23.7 (12.0 wk11) | 11 | 5 | 88 | 0 | 0 | 8.00 | 73.3 | 20.3 | 0 | 1 | 0 | 1 | 6 (78) | MISSING |
| Nick Whiteside | CB | 4 | 12.0 (15.0 wk12) | 1 | 1 | 7 | 0 | 0 | 7.00 | 95.8 | 5.0 | 0 | 0 | 1 | 1 | 1 (7) | MISSING |
| Brian Branch | DB | 6 | 84.3 (97.0 wk12) | 12 | 4 | 38 | 0 | 1 | 3.17 | 8.3 | 11.1 | 0 | 4 | 1 | 6 | 8 (73) | MISSING |
| Christian Izien | DB | 7 | 36.3 (5.0 wk12) | 19 | 14 | 115 | 2 | 0 | 6.05 | 123.8 | 7.7 | 0 | 0 | 0 | 0 | 10 (71) | MISSING |
| Avonte Maddox | DB | 2 | 65.0 (36.0 wk2) | 11 | 6 | 158 | 2 | 0 | 14.36 | 139.2 | 15.6 | 1 | 2 | 0 | 2 | 4 (74) | MISSING |
| Jalen Mills | DB | 2 | 17.5 (30.0 wk5) | 2 | 2 | 12 | 0 | 0 | 6.00 | 91.7 | 4.5 | 0 | 0 | 0 | 0 | 2 (12) | MISSING |
| Chuck Clark | S | 10 | 91.0 (100.0 wk11) | 39 | 15 | 188 | 0 | 2 | 4.82 | 32.9 | 10.2 | 0 | 2 | 0 | 4 | 26 (303) | MISSING |
| Kerby Joseph | S | 2 | 73.5 (80.0 wk12) | — | — | — | — | — | — | — | — | — | 1 | 1 | 2 | 3 (20) | MISSING |
| Thomas Harper | S | 2 | 52.5 (45.0 wk2) | 8 | 5 | 128 | 1 | 0 | 16.00 | 145.8 | 13.9 | 1 | 2 | 0 | 2 | 4 (87) | MISSING |
| Andre Cisco | S | 3 | 20.0 (45.0 wk12) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 3 (29) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jack Campbell | 7 | 41 | 30 | 335 | 4 | 8.17 | 129.6 | 0 |
| Derrick Barnes | 11 | 39 | 23 | 301 | 1 | 7.72 | 81.2 | 2 |
| Malcolm Rodriguez | 10 | 12 | 10 | 51 | 3 | 4.25 | 124.0 | 2 |
| Trevor Nowaske | 11 | 10 | 3 | 29 | 0 | 2.90 | 39.6 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | CHI | D.Barnes | PBU | D.Swift | short_left |
| 12 | CHI | R.McCreary | PBU | S.Carlson | short_middle |
| 12 | CHI | K.Joseph | PBU | J.Walker | deep_right |
| 12 | CHI | R.McCreary | PBU | K.Raymond | short_left |
| 12 | CHI | R.McCreary | PBU | L.Burden | short_right |
| 11 | TB | K.Joseph | DPI | B.Sharp | deep_right |
| 11 | TB | B.Branch | DPI | T.Hurst | deep_right |
| 11 | TB | B.Branch | PBU | B.Irving | short_middle |
| 11 | TB | D.Wonnum | PBU | T.Johnson | short_left |
| 11 | TB | M.Rodriguez | PBU | K.Gainwell | short_right |
| 11 | TB | B.Branch | PBU | E.Egbuka | short_right |
| 11 | TB | R.McCreary | PBU | T.Hurst | short_right |
| 11 | TB | C.Clark | PBU | T.Hurst | short_left |
| 10 | NE | E.O'Neill | PBU | D.Douglas | short_right |
| 10 | NE | N.Whiteside | DPI | K.Williams | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
