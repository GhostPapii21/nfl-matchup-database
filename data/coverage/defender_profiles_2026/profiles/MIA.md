# MIA defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.8 | 22.2 | — |
| Zone % | 77.2 | 77.5 | — |
| Single-high / MOFC % | 42.1 | 47.3 | — |
| Two-high / MOFO % | 51.9 | 52.7 | — |
| Blitz % | 18.9 | 23.1 | 21.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 38.5 / 26.6, 56.0 | — | — |

Sharp YPT allowed: WR 9.2, TE 8.0, RB 6.0, **outside 9.6 vs slot 9.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #23 vs StatRankings #29; blitz rank Sharp #31 vs SR #30 (raw gaps: man -8.4 pts, blitz -4.2 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 14.0 | 128.2 | 9.16 | 7 | 0.299 | 28 |
| TE | 7.3 | 58.2 | 7.97 | 6 | 0.261 | 11 |
| RB | 6.2 | 37.5 | 6.05 | 5 | 0.199 | 9 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 15 | 9 | 209 | 0 | 1 | 13.93 | 11.46 | 10 |  |
| deep middle | 15 | 9 | 305 | 1 | 2 | 20.33 | 14.39 | 3 | **WEAK** |
| deep right | 22 | 13 | 383 | 2 | 0 | 17.41 | 12.14 | 4 | **WEAK** |
| short left | 82 | 67 | 527 | 6 | 0 | 6.43 | 5.99 | 10 |  |
| short middle | 46 | 32 | 279 | 5 | 4 | 6.07 | 7.32 | 30 |  |
| short right | 95 | 77 | 536 | 4 | 2 | 5.64 | 6.02 | 25 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs MIA: **3.44 yds** (league 2.93; rank 1/32 most allowed). WR 3.56, TE 3.19, cushion 6.04. Sample: 13 receiver-games, 100 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chris Johnson | CB | 10 | 97.8 (99.0 wk11) | 45 | 32 | 408 | 3 | 2 | 9.07 | 102.8 | 7.1 | 2 | 3 | 0 | 5 | 29 (339) | MISSING |
| Jason Marshall | CB | 10 | 71.6 (71.0 wk11) | 37 | 25 | 347 | 2 | 0 | 9.38 | 115.5 | 8.3 | 1 | 1 | 1 | 2 | 15 (188) | MISSING |
| Julius Brents | CB | 10 | 69.9 (72.0 wk11) | 33 | 23 | 258 | 1 | 0 | 7.82 | 102.8 | 9.5 | 1 | 2 | 1 | 3 | 17 (145) | MISSING |
| Darrell Baker | CB | 1 | 23.0 (23.0 wk11) | 1 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 12.0 | 0 | 0 | 0 | 0 | 1 (12) | MISSING |
| Jaylin Simpson | CB | 3 | 4.3 (3.0 wk9) | 1 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 6.0 | 0 | 1 | 0 | 1 | 0 (0) | MISSING |
| Marcellas Dial | CB | 1 | 1.0 (1.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Michael Taaffe | S | 10 | 95.4 (99.0 wk11) | 33 | 19 | 341 | 3 | 3 | 10.33 | 85.5 | 11.8 | 0 | 0 | 0 | 3 | 20 (263) | MISSING |
| Dante Trader | S | 9 | 85.2 (100.0 wk10) | 16 | 9 | 122 | 0 | 1 | 7.62 | 54.7 | 12.7 | 0 | 1 | 0 | 2 | 13 (237) | MISSING |
| Zayne Anderson | S | 8 | 33.9 (100.0 wk11) | 17 | 6 | 55 | 3 | 1 | 3.24 | 60.0 | 13.5 | 0 | 3 | 0 | 4 | 10 (166) | MISSING |
| Kyle Louis | S | 5 | 20.0 (17.0 wk11) | 3 | 2 | 11 | 0 | 0 | 3.67 | 72.9 | 8.7 | 0 | 0 | 0 | 0 | 1 (7) | MISSING |
| Julius Wood | S | 4 | 9.5 (4.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jacob Rodriguez | 10 | 51 | 34 | 299 | 3 | 5.86 | 85.3 | 0 |
| Jordyn Brooks | 10 | 45 | 29 | 249 | 1 | 5.53 | 86.3 | 2 |
| Willie Gay Jr. | 9 | 13 | 11 | 128 | 2 | 9.85 | 147.3 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | BUF | Z.Anderson | INT | K.Shakir | short_middle |
| 11 | BUF | J.Rodriguez | INT | K.Latu | short_middle |
| 11 | BUF | Z.Anderson | PBU | K.Latu | deep_right |
| 11 | BUF | Z.Anderson | PBU | K.Shakir | deep_right |
| 11 | BUF | J.Brents | PBU | K.Coleman | deep_right |
| 11 | BUF | C.Johnson | PBU | K.Shakir | short_right |
| 10 | IND | C.Johnson | INT | A.Ogletree | short_right |
| 10 | IND | M.Taaffe | INT | D.Burks | short_middle |
| 10 | IND | J.Brooks | PBU | A.Gould | short_right |
| 9 | DET | J.Marshall | DPI | — | deep_right |
| 9 | DET | J.Marshall | PBU | J.Williams | deep_left |
| 9 | DET | C.Johnson | INT | A.St. Brown | short_right |
| 9 | DET | C.Robinson | PBU | I.TeSlaa | short_middle |
| 7 | NYJ | J.Brents | DPI | — | unk_unk |
| 7 | NYJ | Z.Biggers | PBU | B.Allen | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
