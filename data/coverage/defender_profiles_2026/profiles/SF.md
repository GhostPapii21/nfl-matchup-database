# SF defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 10.3 | 26.5 | — |
| Zone % | 84.0 | 72.4 | — |
| Single-high / MOFC % | 54.3 | 57.7 | — |
| Two-high / MOFO % | 41.7 | 42.3 | — |
| Blitz % | 26.9 | 31.6 | 28.8 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 49.4 / 21.9, 64.0 | — | — |

Sharp YPT allowed: WR 7.1, TE 6.8, RB 5.4, **outside 7.4 vs slot 7.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #28 vs StatRankings #23; blitz rank Sharp #18 vs SR #16 (raw gaps: man -16.2 pts, blitz -4.7 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.7 | 146.1 | 7.06 | 11 | 0.106 | 18 |
| TE | 8.1 | 55.1 | 6.8 | 3 | 0.035 | 12 |
| RB | 6.8 | 36.9 | 5.43 | 2 | 0.054 | 11 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 24 | 9 | 219 | 1 | 1 | 9.12 | 11.46 | 23 |  |
| deep middle | 15 | 8 | 164 | 1 | 1 | 10.93 | 14.39 | 26 |  |
| deep right | 33 | 11 | 358 | 2 | 3 | 10.85 | 12.14 | 20 |  |
| short left | 125 | 108 | 812 | 8 | 0 | 6.5 | 5.99 | 9 |  |
| short middle | 39 | 22 | 216 | 0 | 1 | 5.54 | 7.32 | 32 |  |
| short right | 119 | 89 | 612 | 4 | 1 | 5.14 | 6.02 | 29 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs SF: **2.98 yds** (league 2.93; rank 14/32 most allowed). WR 2.82, TE 3.46, cushion 7.18. Sample: 23 receiver-games, 191 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Renardo Green | CB | 10 | 92.7 (90.0 wk11) | 53 | 36 | 365 | 2 | 4 | 6.89 | 68.5 | 11.2 | 1 | 3 | 1 | 8 | 32 (255) | MISSING |
| Upton Stout | CB | 9 | 60.8 (64.0 wk11) | 38 | 28 | 372 | 3 | 0 | 9.79 | 130.6 | 6.7 | 2 | 2 | 0 | 2 | 14 (163) | MISSING |
| Jack Jones | CB | 7 | 18.9 (34.0 wk7) | 21 | 12 | 126 | 2 | 0 | 6.00 | 106.4 | 10.8 | 0 | 3 | 1 | 4 | 7 (85) | MISSING |
| Ephesians Prysock | CB | 4 | 18.0 (19.0 wk11) | 10 | 7 | 49 | 1 | 0 | 4.90 | 114.2 | 9.5 | 0 | 1 | 1 | 2 | 6 (54) | MISSING |
| Deommodore Lenoir | DB | 10 | 94.2 (81.0 wk11) | 59 | 37 | 385 | 5 | 0 | 6.53 | 109.8 | 12.2 | 1 | 7 | 2 | 9 | 25 (225) | MISSING |
| Siran Neal | DB | 2 | 12.0 (10.0 wk11) | 3 | 2 | 13 | 0 | 0 | 4.33 | 75.7 | 10.0 | 0 | 0 | 0 | 0 | 1 (8) | MISSING |
| Ji'Ayir Brown | S | 10 | 87.5 (61.0 wk11) | 29 | 19 | 220 | 1 | 1 | 7.59 | 85.4 | 9.5 | 0 | 3 | 0 | 4 | 20 (240) | MISSING |
| Malik Mustapha | S | 10 | 60.0 (73.0 wk11) | 29 | 11 | 169 | 1 | 2 | 5.83 | 40.7 | 15.4 | 0 | 4 | 0 | 6 | 19 (248) | MISSING |
| Marques Sigle | S | 7 | 75.9 (70.0 wk11) | 12 | 4 | 51 | 0 | 0 | 4.25 | 47.6 | 7.8 | 0 | 2 | 0 | 2 | 10 (175) | MISSING |
| Ashtyn Davis | S | 2 | 15.5 (10.0 wk7) | 4 | 3 | 38 | 0 | 0 | 9.50 | 104.2 | 9.5 | 0 | 0 | 0 | 0 | 2 (36) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Fred Warner | 10 | 39 | 28 | 254 | 0 | 6.51 | 89.0 | 4 |
| Dre Greenlaw | 8 | 35 | 26 | 151 | 0 | 4.31 | 82.0 | 0 |
| Jaden Dugger | 10 | 24 | 21 | 129 | 1 | 5.38 | 85.6 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | MIN | M.Sigle | PBU | T.Felton | short_left |
| 11 | MIN | J.Brown | INT | T.Felton | short_middle |
| 11 | MIN | D.Lenoir | PBU | J.Jennings | deep_right |
| 11 | MIN | D.Lenoir | PBU | J.Jennings | short_middle |
| 11 | MIN | F.Warner | PBU | T.Felton | short_middle |
| 10 | DAL | E.Prysock | DPI | R.Flournoy | short_middle |
| 10 | DAL | M.Mustapha | PBU | K.Turpin | deep_right |
| 10 | DAL | M.Mustapha | INT | C.Lamb | deep_right |
| 10 | DAL | J.Brown | PBU | G.Pickens | short_right |
| 10 | DAL | D.Lenoir | PBU | G.Pickens | deep_right |
| 10 | DAL | D.Lenoir | PBU | G.Pickens | deep_middle |
| 10 | DAL | M.Sigle | PBU | C.Lamb | short_middle |
| 10 | DAL | D.Lenoir | PBU | G.Pickens | short_right |
| 10 | DAL | D.Lenoir | PBU | C.Lamb | short_right |
| 10 | DAL | R.Green | PBU | G.Pickens | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
