# DEN defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 23.8 | 43.6 | — |
| Zone % | 71.8 | 55.0 | — |
| Single-high / MOFC % | 50.0 | 58.5 | — |
| Two-high / MOFO % | 46.3 | 41.5 | — |
| Blitz % | 34.8 | 36.1 | 34.2 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 41.2 / 28.8, 65.0 | — | — |

Sharp YPT allowed: WR 6.9, TE 7.5, RB 7.0, **outside 7.5 vs slot 7.5** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #7 vs StatRankings #4; blitz rank Sharp #7 vs SR #10 (raw gaps: man -19.8 pts, blitz -1.3 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.1 | 132.0 | 6.91 | 6 | 0.085 | 26 |
| TE | 9.3 | 70.2 | 7.55 | 8 | 0.268 | 4 |
| RB | 7.0 | 48.8 | 6.97 | 3 | 0.09 | 1 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 25 | 7 | 179 | 0 | 1 | 7.16 | 11.46 | 30 |  |
| deep middle | 12 | 5 | 124 | 0 | 1 | 10.33 | 14.39 | 28 |  |
| deep right | 26 | 8 | 260 | 2 | 1 | 10.0 | 12.14 | 24 |  |
| short left | 96 | 66 | 672 | 6 | 5 | 7.0 | 5.99 | 4 | **WEAK** |
| short middle | 63 | 43 | 486 | 4 | 0 | 7.71 | 7.32 | 9 |  |
| short right | 132 | 96 | 789 | 5 | 1 | 5.98 | 6.02 | 17 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs DEN: **2.61 yds** (league 2.93; rank 30/32 most allowed). WR 2.57, TE 2.74, cushion 6.08. Sample: 25 receiver-games, 196 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Riley Moss | CB | 9 | 77.8 (100.0 wk11) | 43 | 20 | 244 | 3 | 1 | 5.67 | 78.1 | 12.6 | 1 | 7 | 2 | 10 | 16 (117) | MISSING |
| Ja'Quan McMillian | CB | 10 | 64.9 (77.0 wk11) | 52 | 29 | 334 | 1 | 2 | 6.42 | 65.7 | 7.1 | 0 | 6 | 0 | 8 | 20 (193) | MISSING |
| Patrick Surtain II | CB | 7 | 92.0 (100.0 wk11) | 37 | 20 | 198 | 2 | 0 | 5.35 | 87.4 | 12.4 | 1 | 2 | 0 | 2 | 17 (172) | MISSING |
| Jahdae Barron | CB | 10 | 46.7 (19.0 wk11) | 35 | 22 | 252 | 2 | 0 | 7.20 | 103.5 | 8.2 | 1 | 2 | 4 | 6 | 20 (286) | MISSING |
| Kris Abrams-Draine | CB | 4 | 71.5 (58.0 wk7) | 23 | 14 | 112 | 1 | 1 | 4.87 | 69.5 | 10.1 | 0 | 4 | 1 | 6 | 11 (90) | MISSING |
| Devon Key | DB | 8 | 35.2 (53.0 wk11) | 13 | 9 | 111 | 1 | 0 | 8.54 | 121.0 | 13.6 | 0 | 2 | 0 | 3 | 11 (148) | MISSING |
| Brandon Jones | S | 8 | 90.8 (35.0 wk8) | 26 | 18 | 289 | 1 | 2 | 11.12 | 86.9 | 9.2 | 1 | 3 | 1 | 6 | 24 (320) | MISSING |
| Talanoa Hufanga | S | 6 | 93.7 (99.0 wk11) | 17 | 7 | 89 | 0 | 2 | 5.24 | 18.6 | 13.1 | 0 | 2 | 0 | 4 | 10 (173) | MISSING |
| Taylor Rapp | S | 5 | 67.2 (47.0 wk11) | 7 | 4 | 37 | 0 | 0 | 5.29 | 71.7 | 13.9 | 0 | 0 | 0 | 0 | 8 (129) | MISSING |
| JL Skinner | S | 4 | 26.8 (91.0 wk9) | 3 | 2 | 36 | 1 | 0 | 12.00 | 147.2 | 10.7 | 0 | 0 | 0 | 0 | 3 (50) | MISSING |
| Tycen Anderson | S | 1 | 1.0 (1.0 wk5) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Alex Singleton | 10 | 50 | 34 | 347 | 1 | 6.94 | 94.3 | 3 |
| Justin Strnad | 10 | 38 | 24 | 229 | 0 | 6.03 | 79.8 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | LV | T.Hufanga | PBU | T.Tucker | deep_middle |
| 11 | LV | J.Cooper | PBU | M.Mayer | short_middle |
| 11 | LV | Z.Allen | PBU | A.Jeanty | short_right |
| 11 | LV | J.McMillian | INT | T.Tucker | short_left |
| 11 | LV | Z.Allen | PBU | J.Bech | short_middle |
| 11 | LV | A.Singleton | PBU | M.Mayer | short_middle |
| 11 | LV | D.Jones | PBU | A.Jeanty | short_middle |
| 11 | LV | Z.Allen | PBU | T.Tucker | short_right |
| 9 | CAR | D.Key | INT | T.Tremble | short_left |
| 9 | CAR | J.Barron | DPI | D.Waller | short_left |
| 9 | CAR | R.Moss | PBU | J.Coker | deep_right |
| 8 | KC | R.Moss | PBU | X.Worthy | short_left |
| 8 | KC | P.Surtain | PBU | X.Worthy | deep_right |
| 8 | KC | D.Key | PBU | C.Allen | deep_middle |
| 8 | KC | Z.Allen | PBU | R.Rice | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
