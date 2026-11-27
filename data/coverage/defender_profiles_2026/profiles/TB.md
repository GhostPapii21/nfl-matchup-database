# TB defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 14.9 | 29.7 | — |
| Zone % | 80.1 | 69.8 | — |
| Single-high / MOFC % | 62.6 | 63.9 | — |
| Two-high / MOFO % | 36.0 | 36.1 | — |
| Blitz % | 41.8 | 44.7 | 43.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 34.6 / 34.6, 61.0 | — | — |

Sharp YPT allowed: WR 7.6, TE 7.9, RB 5.3, **outside 8.2 vs slot 7.0** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #21 vs StatRankings #20; blitz rank Sharp #2 vs SR #2 (raw gaps: man -14.8 pts, blitz -2.9 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 18.3 | 138.2 | 7.55 | 9 | -0.101 | 23 |
| TE | 8.2 | 64.8 | 7.9 | 5 | 0.104 | 5 |
| RB | 5.5 | 28.9 | 5.25 | 0 | 0.022 | 23 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 22 | 9 | 287 | 2 | 2 | 13.05 | 11.46 | 13 |  |
| deep middle | 13 | 6 | 216 | 2 | 0 | 16.62 | 14.39 | 9 |  |
| deep right | 15 | 4 | 130 | 0 | 2 | 8.67 | 12.14 | 27 |  |
| short left | 106 | 78 | 596 | 3 | 1 | 5.62 | 5.99 | 20 |  |
| short middle | 60 | 39 | 437 | 3 | 5 | 7.28 | 7.32 | 17 |  |
| short right | 104 | 74 | 653 | 4 | 6 | 6.28 | 6.02 | 13 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs TB: **3.16 yds** (league 2.93; rank 6/32 most allowed). WR 3.01, TE 3.55, cushion 5.44. Sample: 24 receiver-games, 176 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Zyon McCollum | CB | 10 | 99.8 (100.0 wk11) | 56 | 30 | 338 | 2 | 4 | 6.04 | 54.0 | 10.1 | 2 | 7 | 1 | 12 | 26 (296) | MISSING |
| Jacob Parrish | CB | 9 | 81.2 (10.0 wk11) | 54 | 27 | 371 | 1 | 2 | 6.87 | 63.1 | 9.8 | 3 | 11 | 2 | 15 | 23 (220) | MISSING |
| Benjamin Morrison | CB | 4 | 54.8 (50.0 wk11) | 23 | 16 | 219 | 2 | 0 | 9.52 | 128.7 | 8.4 | 1 | 2 | 0 | 2 | 13 (111) | MISSING |
| Kevin Knowles | CB | 1 | 34.0 (34.0 wk11) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 1 (10) | MISSING |
| Ayden Garnes | CB | 1 | 2.0 (2.0 wk5) | 1 | 1 | 18 | 1 | 0 | 18.00 | 158.3 | 18.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Keionte Scott | DB | 10 | 60.5 (34.0 wk11) | 42 | 29 | 257 | 3 | 0 | 6.12 | 108.9 | 6.2 | 0 | 4 | 0 | 4 | 20 (161) | MISSING |
| Tykee Smith | S | 10 | 95.2 (93.0 wk11) | 49 | 23 | 320 | 3 | 2 | 6.53 | 71.8 | 6.9 | 0 | 2 | 0 | 4 | 22 (236) | MISSING |
| Antoine Winfield Jr. | S | 6 | 88.8 (48.0 wk9) | 12 | 6 | 79 | 0 | 0 | 6.58 | 71.2 | 14.3 | 0 | 1 | 0 | 1 | 12 (223) | MISSING |
| Ifeatu Melifonwu | S | 7 | 64.4 (91.0 wk11) | 14 | 6 | 109 | 0 | 0 | 7.79 | 70.2 | 15.4 | 0 | 1 | 0 | 1 | 8 (150) | MISSING |
| Miles Killebrew | S | 7 | 3.4 (5.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| JJ Roberts | S | 1 | 2.0 (2.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Alex Anzalone | 10 | 52 | 35 | 398 | 2 | 7.65 | 70.8 | 0 |
| Josiah Trotter | 9 | 34 | 20 | 172 | 1 | 5.06 | 69.7 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | DET | T.Smith | PBU | S.LaPorta | short_left |
| 11 | DET | K.Scott | PBU | S.LaPorta | short_middle |
| 11 | DET | V.Vea | PBU | I.TeSlaa | short_middle |
| 11 | DET | Y.Diaby | PBU | J.Gibbs | short_middle |
| 9 | CHI | I.Melifonwu | PBU | C.Loveland | deep_right |
| 9 | CHI | A.Anzalone | INT | L.Burden | short_left |
| 9 | CHI | Z.McCollum | INT | K.Raymond | deep_right |
| 9 | CHI | Z.McCollum | INT | L.Burden | deep_right |
| 9 | CHI | T.Smith | INT | R.Odunze | deep_left |
| 9 | CHI | A.Winfield | PBU | C.Loveland | short_right |
| 8 | ATL | A.Robinson | PBU | K.Pitts | short_middle |
| 8 | ATL | J.Parrish | PBU | J.Dotson | short_left |
| 8 | ATL | Z.McCollum | INT | C.Woerner | short_right |
| 8 | ATL | J.Parrish | INT | D.London | short_middle |
| 8 | ATL | K.Scott | PBU | J.Dotson | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
