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
