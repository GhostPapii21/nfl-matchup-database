# CIN defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 25.7 | 43.4 | — |
| Zone % | 67.4 | 55.0 | — |
| Single-high / MOFC % | 52.8 | 56.5 | — |
| Two-high / MOFO % | 42.8 | 43.5 | — |
| Blitz % | 16.5 | 18.1 | 16.8 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 57.4 / 15.5, 82.0 | — | — |

Sharp YPT allowed: WR 7.7, TE 8.8, RB 5.5, **outside 7.4 vs slot 9.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #3 vs StatRankings #5; blitz rank Sharp #32 vs SR #32 (raw gaps: man -17.7 pts, blitz -1.6 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.5 | 135.2 | 7.73 | 9 | 0.194 | 25 |
| TE | 8.5 | 75.1 | 8.84 | 2 | 0.288 | 2 |
| RB | 5.8 | 32.0 | 5.52 | 0 | -0.058 | 20 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 23 | 7 | 173 | 2 | 0 | 7.52 | 11.46 | 28 |  |
| deep middle | 17 | 10 | 250 | 0 | 0 | 14.71 | 14.39 | 15 |  |
| deep right | 19 | 4 | 104 | 2 | 0 | 5.47 | 12.14 | 30 |  |
| short left | 86 | 65 | 570 | 1 | 1 | 6.63 | 5.99 | 7 | **WEAK** |
| short middle | 61 | 38 | 513 | 2 | 2 | 8.41 | 7.32 | 4 | **WEAK** |
| short right | 112 | 89 | 813 | 4 | 2 | 7.26 | 6.02 | 2 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs CIN: **2.93 yds** (league 2.93; rank 17/32 most allowed). WR 2.58, TE 3.79, cushion 6.19. Sample: 26 receiver-games, 176 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DJ Turner | CB | 10 | 94.7 (99.0 wk11) | 38 | 24 | 291 | 2 | 0 | 7.66 | 104.2 | 9.6 | 1 | 6 | 3 | 9 | 22 (217) | MISSING |
| Daxton Hill | CB | 10 | 93.3 (76.0 wk11) | 48 | 28 | 380 | 1 | 0 | 7.92 | 90.6 | 10.3 | 3 | 6 | 1 | 7 | 27 (315) | MISSING |
| DJ Ivey | CB | 10 | 34.4 (24.0 wk11) | 30 | 15 | 174 | 3 | 0 | 5.80 | 101.2 | 11.5 | 0 | 3 | 0 | 3 | 11 (105) | MISSING |
| Josh Newton | CB | 5 | 68.2 (75.0 wk11) | 21 | 9 | 107 | 1 | 0 | 5.10 | 74.9 | 9.5 | 0 | 4 | 1 | 5 | 9 (143) | MISSING |
| Jalen Davis | CB | 3 | 61.3 (31.0 wk3) | 15 | 8 | 126 | 1 | 0 | 8.40 | 103.7 | 11.3 | 0 | 2 | 0 | 2 | 7 (67) | MISSING |
| Tacario Davis | CB | 7 | 17.6 (13.0 wk10) | 12 | 6 | 57 | 0 | 0 | 4.75 | 63.5 | 7.4 | 0 | 1 | 1 | 2 | 5 (46) | MISSING |
| Jordan Battle | S | 10 | 98.5 (100.0 wk11) | 46 | 27 | 370 | 1 | 3 | 8.04 | 64.6 | 10.0 | 1 | 5 | 0 | 8 | 30 (362) | MISSING |
| Bryan Cook | S | 9 | 90.7 (94.0 wk11) | 21 | 10 | 156 | 0 | 0 | 7.43 | 72.7 | 11.2 | 0 | 0 | 1 | 1 | 20 (298) | MISSING |
| PJ Jules | S | 3 | 27.3 (4.0 wk11) | 3 | 3 | 66 | 0 | 0 | 22.00 | 118.8 | 13.7 | 0 | 0 | 0 | 0 | 1 (12) | MISSING |
| Kyle Dugger | S | 1 | 66.0 (66.0 wk3) | 4 | 0 | 22 | 0 | 0 | 5.50 | 50.0 | 20.0 | 0 | 0 | 0 | 0 | 5 (88) | MISSING |
| Russ Yeast | S | 1 | 34.0 (34.0 wk4) | 1 | 1 | 15 | 0 | 0 | 15.00 | 118.8 | 6.0 | 0 | 0 | 0 | 0 | 2 (38) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Barrett Carter | 10 | 49 | 31 | 347 | 0 | 7.08 | 75.8 | 3 |
| Demetrius Knight | 10 | 40 | 32 | 312 | 1 | 7.80 | 97.1 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | WAS | D.Hill | DPI | T.Burks | short_left |
| 11 | WAS | J.Newton | PBU | S.Diggs | short_right |
| 10 | PIT | B.Carter | PBU | D.Washington | short_right |
| 10 | PIT | J.Newton | PBU | G.Bernard | short_right |
| 10 | PIT | D.Knight | PBU | P.Freiermuth | short_middle |
| 10 | PIT | J.Battle | PBU | D.Metcalf | deep_right |
| 10 | PIT | D.Hill | PBU | G.Bernard | deep_left |
| 10 | PIT | D.Turner | PBU | D.Metcalf | deep_middle |
| 9 | ATL | B.Carter | INT | B.Robinson | short_middle |
| 9 | ATL | J.Battle | PBU | O.Zaccheaus | short_right |
| 9 | ATL | J.Newton | PBU | C.Blair | deep_left |
| 9 | ATL | D.Turner | DPI | D.London | deep_left |
| 9 | ATL | D.Turner | DPI | D.London | short_right |
| 8 | TEN | J.Battle | PBU | G.Helm | short_left |
| 8 | TEN | B.Cook | DPI | G.Helm | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
