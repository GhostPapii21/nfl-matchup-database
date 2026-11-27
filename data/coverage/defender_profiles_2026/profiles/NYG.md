# NYG defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 24.2 | 43.3 | — |
| Zone % | 70.2 | 56.2 | — |
| Single-high / MOFC % | 46.6 | 51.0 | — |
| Two-high / MOFO % | 50.3 | 49.0 | — |
| Blitz % | 36.3 | 40.3 | 38.7 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 43.1 / 29.3, 74.0 | — | — |

Sharp YPT allowed: WR 6.9, TE 5.6, RB 5.5, **outside 7.4 vs slot 6.6** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #6 vs StatRankings #6; blitz rank Sharp #4 vs SR #4 (raw gaps: man -19.1 pts, blitz -4.0 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.2 | 139.2 | 6.89 | 12 | 0.053 | 22 |
| TE | 8.0 | 44.5 | 5.56 | 3 | 0.03 | 25 |
| RB | 4.1 | 22.7 | 5.54 | 3 | 0.083 | 28 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 26 | 8 | 157 | 0 | 2 | 6.04 | 11.46 | 32 |  |
| deep middle | 14 | 7 | 174 | 1 | 0 | 12.43 | 14.39 | 21 |  |
| deep right | 22 | 8 | 228 | 1 | 1 | 10.36 | 12.14 | 23 |  |
| short left | 113 | 69 | 604 | 5 | 6 | 5.35 | 5.99 | 27 |  |
| short middle | 54 | 37 | 367 | 7 | 0 | 6.8 | 7.32 | 23 |  |
| short right | 94 | 75 | 534 | 4 | 0 | 5.68 | 6.02 | 22 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NYG: **2.59 yds** (league 2.93; rank 32/32 most allowed). WR 2.44, TE 3.14, cushion 4.8. Sample: 21 receiver-games, 175 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Deonte Banks | CB | 8 | 97.4 (97.0 wk11) | 51 | 23 | 210 | 4 | 2 | 4.12 | 66.6 | 9.3 | 0 | 12 | 3 | 17 | 16 (154) | MISSING |
| Greg Newsome II | CB | 9 | 83.2 (6.0 wk11) | 39 | 22 | 255 | 0 | 1 | 6.54 | 65.7 | 12.2 | 0 | 7 | 1 | 9 | 20 (251) | MISSING |
| Andru Phillips | CB | 10 | 73.9 (83.0 wk11) | 45 | 27 | 292 | 2 | 0 | 6.49 | 93.9 | 4.4 | 1 | 5 | 4 | 9 | 20 (204) | MISSING |
| Paulson Adebo | CB | 3 | 70.0 (93.0 wk11) | 11 | 4 | 47 | 0 | 1 | 4.27 | 12.3 | 22.8 | 0 | 3 | 0 | 4 | 4 (47) | MISSING |
| Colton Hood | CB | 4 | 52.2 (4.0 wk11) | 13 | 10 | 102 | 3 | 0 | 7.85 | 138.5 | 11.2 | 0 | 0 | 0 | 0 | 6 (49) | MISSING |
| Nic Jones | CB | 3 | 17.0 (43.0 wk6) | 2 | 2 | 25 | 1 | 0 | 12.50 | 158.3 | 9.5 | 0 | 0 | 0 | 0 | 1 (7) | MISSING |
| Jevon Holland | S | 9 | 100.0 (100.0 wk11) | 29 | 12 | 213 | 3 | 4 | 7.34 | 62.1 | 11.2 | 0 | 3 | 0 | 6 | 17 (254) | MISSING |
| Ar'Darius Washington | S | 9 | 51.4 (100.0 wk11) | 25 | 15 | 164 | 0 | 1 | 6.56 | 62.7 | 12.1 | 0 | 5 | 1 | 7 | 17 (171) | MISSING |
| Tyler Nubin | S | 7 | 49.4 (10.0 wk11) | 18 | 9 | 163 | 0 | 0 | 9.06 | 81.5 | 11.7 | 1 | 3 | 0 | 3 | 9 (102) | MISSING |
| Jason Pinnock | S | 6 | 54.8 (22.0 wk10) | 9 | 5 | 73 | 2 | 0 | 8.11 | 121.8 | 7.7 | 0 | 2 | 0 | 2 | 3 (41) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Arvell Reese | 10 | 41 | 35 | 178 | 1 | 4.34 | 82.7 | 2 |
| Micah McFadden | 5 | 23 | 14 | 121 | 1 | 5.26 | 89.2 | 0 |
| Tremaine Edmunds | 6 | 18 | 17 | 152 | 1 | 8.44 | 120.4 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | JAX | A.Phillips | PBU | J.Meyers | short_left |
| 11 | JAX | A.Washington | PBU | J.Meyers | short_middle |
| 11 | JAX | P.Adebo | PBU | P.Washington | deep_middle |
| 11 | JAX | P.Adebo | INT | J.Meyers | short_left |
| 11 | JAX | P.Adebo | PBU | P.Washington | deep_middle |
| 11 | JAX | A.Phillips | PBU | P.Washington | short_left |
| 11 | JAX | D.Banks | PBU | Bri.Thomas | short_middle |
| 11 | JAX | A.Phillips | PBU | J.Meyers | short_left |
| 11 | JAX | A.Washington | PBU | J.Cameron | short_middle |
| 11 | JAX | P.Adebo | PBU | J.Meyers | short_left |
| 11 | JAX | D.Banks | INT | P.Washington | short_left |
| 11 | JAX | D.Banks | PBU | P.Washington | deep_left |
| 11 | JAX | J.Holland | PBU | P.Washington | deep_middle |
| 11 | JAX | G.Newsome | PBU | P.Washington | deep_middle |
| 10 | WAS | D.Banks | DPI | T.Burks | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
