# NYJ defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 25.7 | 37.0 | — |
| Zone % | 64.5 | 63.0 | — |
| Single-high / MOFC % | 44.3 | 44.7 | — |
| Two-high / MOFO % | 49.7 | 55.3 | — |
| Blitz % | 36.1 | 39.1 | 36.6 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 40.1 / 29.1, 65.0 | — | — |

Sharp YPT allowed: WR 7.7, TE 8.1, RB 6.0, **outside 8.4 vs slot 7.5** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #3 vs StatRankings #13; blitz rank Sharp #5 vs SR #6 (raw gaps: man -11.3 pts, blitz -3.0 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 15.3 | 117.0 | 7.66 | 12 | 0.273 | 29 |
| TE | 7.5 | 60.1 | 8.06 | 3 | 0.275 | 7 |
| RB | 4.4 | 26.2 | 6.0 | 4 | 0.256 | 26 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 15 | 5 | 118 | 1 | 1 | 7.87 | 11.46 | 27 |  |
| deep middle | 12 | 6 | 198 | 1 | 1 | 16.5 | 14.39 | 10 |  |
| deep right | 19 | 9 | 290 | 1 | 0 | 15.26 | 12.14 | 7 | **WEAK** |
| short left | 93 | 62 | 563 | 4 | 0 | 6.05 | 5.99 | 14 |  |
| short middle | 53 | 40 | 387 | 2 | 0 | 7.3 | 7.32 | 16 |  |
| short right | 106 | 78 | 680 | 10 | 0 | 6.42 | 6.02 | 10 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NYJ: **3.21 yds** (league 2.93; rank 5/32 most allowed). WR 2.91, TE 3.98, cushion 5.23. Sample: 23 receiver-games, 162 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Azareye'h Thomas | CB | 11 | 100.0 (100.0 wk11) | 57 | 33 | 355 | 4 | 1 | 6.23 | 92.4 | 8.3 | 0 | 6 | 1 | 8 | 27 (247) | MISSING |
| Brandon Stephens | CB | 11 | 97.0 (100.0 wk11) | 56 | 29 | 403 | 4 | 0 | 7.20 | 99.0 | 9.3 | 0 | 5 | 2 | 7 | 19 (221) | MISSING |
| D'Angelo Ponds | CB | 9 | 21.3 (58.0 wk11) | 8 | 5 | 77 | 1 | 0 | 9.62 | 133.9 | 5.9 | 0 | 1 | 1 | 2 | 2 (8) | MISSING |
| Qwan'tez Stiggers | CB | 1 | 2.0 (2.0 wk7) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Jarvis Brownlee | DB | 8 | 53.1 (3.0 wk9) | 29 | 18 | 185 | 3 | 0 | 6.38 | 114.9 | 8.4 | 0 | 0 | 1 | 1 | 10 (92) | MISSING |
| Malachi Moore | DB | 5 | 21.6 (17.0 wk11) | 1 | 1 | 45 | 1 | 0 | 45.00 | 158.3 | 40.0 | 0 | 0 | 1 | 1 | 0 (0) | MISSING |
| Nahshon Wright | DB | 2 | 4.5 (5.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Dane Belton | S | 11 | 100.0 (100.0 wk11) | 37 | 18 | 211 | 0 | 0 | 5.70 | 66.4 | 8.4 | 0 | 5 | 0 | 5 | 31 (423) | MISSING |
| Minkah Fitzpatrick | S | 9 | 90.0 (100.0 wk11) | 22 | 12 | 232 | 2 | 1 | 10.55 | 102.8 | 10.8 | 1 | 2 | 0 | 3 | 13 (185) | MISSING |
| Andre Cisco | S | 7 | 45.9 (13.0 wk8) | 13 | 7 | 85 | 0 | 0 | 6.54 | 74.2 | 8.9 | 0 | 1 | 0 | 1 | 10 (130) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jamien Sherwood | 11 | 46 | 33 | 332 | 3 | 7.22 | 113.7 | 5 |
| Demario Davis | 11 | 37 | 28 | 254 | 1 | 6.86 | 102.8 | 4 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | LAC | A.Thomas | PBU | D.Njoku | short_right |
| 11 | LAC | D.Bailey | PBU | L.McConkey | short_left |
| 10 | BUF | A.Thomas | INT | G.Dortch | deep_left |
| 10 | BUF | D.Ponds | PBU | D.Knox | short_left |
| 10 | BUF | D.Belton | PBU | D.Kincaid | short_right |
| 10 | BUF | M.Moore | DPI | D.Kincaid | deep_left |
| 10 | BUF | D.Bailey | PBU | D.Knox | short_right |
| 10 | BUF | D.Bailey | PBU | K.Shakir | short_right |
| 8 | LV | J.Brownlee | DPI | T.Tucker | deep_middle |
| 8 | LV | M.Fitzpatrick | PBU | B.Bowers | deep_left |
| 8 | LV | D.Belton | PBU | M.Mayer | short_middle |
| 8 | LV | A.Thomas | PBU | B.Bowers | short_right |
| 7 | MIA | B.Stephens | PBU | C.Douglas | short_left |
| 7 | MIA | J.Sherwood | PBU | S.Traore | short_right |
| 7 | MIA | D.Davis | PBU | O.Gordon | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
