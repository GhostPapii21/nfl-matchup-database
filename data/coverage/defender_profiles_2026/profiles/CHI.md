# CHI defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 25.6 | 35.1 | — |
| Zone % | 69.9 | 64.3 | — |
| Single-high / MOFC % | 48.3 | 50.8 | — |
| Two-high / MOFO % | 47.7 | 49.2 | — |
| Blitz % | 31.1 | 35.9 | 34.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 35.8 / 24.5, 65.0 | — | — |

Sharp YPT allowed: WR 8.9, TE 7.1, RB 6.6, **outside 10.7 vs slot 7.1** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #5 vs StatRankings #14; blitz rank Sharp #12 vs SR #11 (raw gaps: man -9.5 pts, blitz -4.8 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.2 | 156.0 | 9.08 | 8 | 0.123 | 10 |
| TE | 6.6 | 47.5 | 7.15 | 4 | 0.053 | 20 |
| RB | 5.7 | 36.4 | 6.35 | 3 | -0.076 | 12 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 34 | 16 | 475 | 3 | 1 | 13.97 | 11.46 | 9 |  |
| deep middle | 12 | 10 | 350 | 2 | 0 | 29.17 | 14.39 | 1 | **WEAK** |
| deep right | 21 | 9 | 292 | 1 | 1 | 13.9 | 12.14 | 10 |  |
| short left | 106 | 65 | 512 | 5 | 3 | 4.83 | 5.99 | 31 |  |
| short middle | 53 | 42 | 363 | 1 | 2 | 6.85 | 7.32 | 21 |  |
| short right | 100 | 69 | 646 | 3 | 2 | 6.46 | 6.02 | 8 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs CHI: **2.65 yds** (league 2.93; rank 28/32 most allowed). WR 2.50, TE 3.13, cushion 6.78. Sample: 27 receiver-games, 192 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dillon Thieneman | DB | 11 | 98.5 (100.0 wk12) | 28 | 13 | 167 | 1 | 2 | 5.96 | 47.8 | 10.0 | 0 | 4 | 0 | 7 | 16 (251) | MISSING |
| Jaylon Johnson | DB | 11 | 97.3 (96.0 wk12) | 49 | 34 | 549 | 1 | 1 | 11.20 | 104.9 | 11.3 | 2 | 2 | 3 | 6 | 28 (418) | MISSING |
| Cameron Lewis | DB | 10 | 87.2 (96.0 wk12) | 20 | 16 | 191 | 3 | 1 | 9.55 | 125.2 | 7.2 | 1 | 1 | 1 | 3 | 28 (346) | MISSING |
| Tyrique Stevenson | DB | 9 | 69.9 (90.0 wk11) | 43 | 24 | 383 | 4 | 0 | 8.91 | 116.7 | 13.7 | 3 | 5 | 0 | 5 | 19 (246) | MISSING |
| Malik Muhammad | DB | 9 | 69.8 (94.0 wk12) | 31 | 17 | 273 | 1 | 1 | 8.81 | 81.8 | 11.0 | 1 | 4 | 1 | 6 | 14 (188) | MISSING |
| Clark Phillips | DB | 6 | 37.8 (56.0 wk12) | 8 | 3 | 13 | 0 | 0 | 1.62 | 45.8 | 13.9 | 0 | 2 | 0 | 2 | 6 (83) | MISSING |
| Kyler Gordon | DB | 4 | 56.5 (76.0 wk9) | 14 | 8 | 124 | 0 | 0 | 8.86 | 86.6 | 10.3 | 1 | 1 | 0 | 1 | 5 (90) | MISSING |
| Xavier Woods | DB | 4 | 63.5 (57.0 wk5) | 6 | 5 | 68 | 1 | 0 | 11.33 | 153.5 | 13.7 | 0 | 0 | 0 | 0 | 4 (26) | MISSING |
| Elijah Hicks | DB | 9 | 13.6 (4.0 wk11) | 5 | 4 | 49 | 1 | 0 | 9.80 | 147.1 | 5.2 | 0 | 0 | 0 | 0 | 3 (23) | MISSING |
| Skyler Thomas | DB | 5 | 6.6 (6.0 wk12) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Josh Blackwell | DB | 2 | 8.5 (1.0 wk12) | 2 | 2 | 4 | 0 | 0 | 2.00 | 79.2 | 7.0 | 0 | 1 | 0 | 1 | 2 (33) | MISSING |
| Nick McCloud | DB | 1 | 16.0 (16.0 wk6) | 1 | 1 | 33 | 0 | 0 | 33.00 | 118.8 | 13.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Devin Bush Jr. | 11 | 41 | 24 | 228 | 2 | 5.56 | 90.3 | 3 |
| T.J. Edwards | 9 | 26 | 18 | 166 | 0 | 6.38 | 70.4 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | DET | D.Thieneman | INT | J.Williams | short_left |
| 12 | DET | J.Johnson | DPI | — | short_right |
| 12 | DET | C.Phillips | PBU | I.TeSlaa | short_right |
| 11 | NO | T.Stevenson | PBU | C.Olave | deep_left |
| 11 | NO | A.Booker | PBU | T.Etienne | short_right |
| 11 | NO | A.Booker | PBU | J.Johnson | short_left |
| 11 | NO | C.Phillips | PBU | J.Tyson | short_left |
| 11 | NO | D.Thieneman | INT | C.Olave | short_right |
| 9 | TB | D.Bush | PBU | T.Johnson | short_left |
| 9 | TB | J.Johnson | INT | C.Otton | short_right |
| 9 | TB | J.Simmons | PBU | B.Irving | short_right |
| 9 | TB | C.Lewis | INT | T.Johnson | short_left |
| 9 | TB | D.Bush | PBU | C.Otton | deep_right |
| 8 | SEA | J.Simmons | PBU | J.Smith-Njigba | short_right |
| 8 | SEA | J.Lynch | INT | A.Barner | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
