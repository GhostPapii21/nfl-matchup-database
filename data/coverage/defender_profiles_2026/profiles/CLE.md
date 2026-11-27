# CLE defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 44.4 | 54.8 | — |
| Zone % | 51.5 | 44.6 | — |
| Single-high / MOFC % | 72.3 | 68.6 | — |
| Two-high / MOFO % | 24.5 | 31.4 | — |
| Blitz % | 28.5 | 29.6 | 27.2 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 38.7 / 25.4, 95.0 | — | — |

Sharp YPT allowed: WR 7.4, TE 7.6, RB 4.0, **outside 6.6 vs slot 10.1** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #1 vs StatRankings #1; blitz rank Sharp #16 vs SR #20 (raw gaps: man -10.4 pts, blitz -1.1 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.8 | 147.3 | 7.44 | 9 | 0.155 | 17 |
| TE | 7.0 | 53.1 | 7.59 | 6 | 0.192 | 16 |
| RB | 4.7 | 18.9 | 4.02 | 0 | -0.171 | 30 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 26 | 10 | 259 | 1 | 1 | 9.96 | 11.46 | 22 |  |
| deep middle | 19 | 7 | 245 | 1 | 1 | 12.89 | 14.39 | 20 |  |
| deep right | 25 | 7 | 192 | 1 | 3 | 7.68 | 12.14 | 29 |  |
| short left | 88 | 57 | 490 | 2 | 2 | 5.57 | 5.99 | 21 |  |
| short middle | 47 | 36 | 339 | 6 | 0 | 7.21 | 7.32 | 18 |  |
| short right | 110 | 80 | 668 | 4 | 0 | 6.07 | 6.02 | 15 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs CLE: **2.78 yds** (league 2.93; rank 25/32 most allowed). WR 2.60, TE 3.59, cushion 4.77. Sample: 26 receiver-games, 183 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Denzel Ward | CB | 10 | 98.9 (100.0 wk10) | 56 | 23 | 239 | 3 | 3 | 4.27 | 49.6 | 11.9 | 0 | 10 | 0 | 13 | 21 (206) | MISSING |
| Tyson Campbell | CB | 9 | 93.2 (96.0 wk10) | 44 | 28 | 378 | 2 | 1 | 8.59 | 96.6 | 12.0 | 2 | 5 | 0 | 6 | 18 (295) | MISSING |
| Myles Harden | CB | 10 | 62.7 (79.0 wk10) | 60 | 36 | 495 | 2 | 1 | 8.25 | 90.6 | 9.6 | 1 | 7 | 1 | 9 | 23 (317) | MISSING |
| Mekhi Blackmon | CB | 8 | 21.2 (4.0 wk10) | 18 | 8 | 91 | 0 | 0 | 5.06 | 60.2 | 13.9 | 1 | 2 | 0 | 2 | 7 (84) | MISSING |
| Noah Igbinoghene | CB | 2 | 7.5 (3.0 wk3) | 2 | 2 | 37 | 0 | 0 | 18.50 | 118.8 | 15.0 | 0 | 0 | 0 | 0 | 2 (37) | MISSING |
| Grant Delpit | S | 10 | 90.0 (100.0 wk10) | 38 | 20 | 246 | 1 | 1 | 6.47 | 70.7 | 12.6 | 1 | 3 | 1 | 5 | 20 (157) | MISSING |
| Ronnie Hickman | S | 9 | 98.8 (99.0 wk9) | 26 | 18 | 277 | 4 | 1 | 10.65 | 127.7 | 9.8 | 1 | 3 | 0 | 4 | 19 (271) | MISSING |
| Emmanuel McNeil-Warren | S | 10 | 47.9 (100.0 wk10) | 19 | 6 | 70 | 1 | 0 | 3.68 | 61.3 | 11.6 | 0 | 3 | 1 | 4 | 7 (94) | MISSING |
| Daniel Thomas | S | 3 | 18.0 (16.0 wk10) | 1 | 1 | 11 | 1 | 0 | 11.00 | 152.1 | 11.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Donovan McMillon | S | 1 | 1.0 (1.0 wk10) | 1 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 52.0 | 0 | 1 | 0 | 1 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Carson Schwesinger | 10 | 38 | 26 | 364 | 2 | 9.58 | 116.6 | 1 |
| Quincy Williams | 10 | 36 | 23 | 118 | 0 | 3.28 | 69.0 | 4 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 10 | HOU | D.McMillon | PBU | X.Hutchinson | deep_left |
| 10 | HOU | T.Campbell | PBU | K.Boutte | deep_left |
| 10 | HOU | D.Ward | PBU | X.Hutchinson | short_right |
| 10 | HOU | M.Harden | DPI | — | deep_right |
| 10 | HOU | D.Ward | PBU | N.Collins | deep_left |
| 10 | HOU | T.Campbell | PBU | N.Collins | short_left |
| 10 | HOU | Q.Williams | PBU | X.Hutchinson | short_middle |
| 10 | HOU | T.Campbell | INT | N.Collins | short_left |
| 10 | HOU | D.Ward | PBU | N.Collins | short_right |
| 10 | HOU | M.Harden | PBU | T.Dell | short_left |
| 9 | NO | D.Ward | PBU | C.Olave | deep_right |
| 9 | NO | R.Hickman | PBU | D.Vele | deep_left |
| 9 | NO | R.Hickman | PBU | N.Fant | short_middle |
| 9 | NO | S.Williams | PBU | C.Olave | deep_middle |
| 9 | NO | M.Harden | PBU | C.Olave | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
