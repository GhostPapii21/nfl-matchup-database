# SEA defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 9.8 | 20.7 | — |
| Zone % | 85.4 | 79.3 | — |
| Single-high / MOFC % | 41.2 | 43.0 | — |
| Two-high / MOFO % | 56.9 | 57.0 | — |
| Blitz % | 22.1 | 24.9 | 24.0 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 48.8 / 17.8, 89.0 | — | — |

Sharp YPT allowed: WR 5.9, TE 5.9, RB 5.1, **outside 7.3 vs slot 4.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #30 vs StatRankings #30; blitz rank Sharp #27 vs SR #28 (raw gaps: man -10.9 pts, blitz -2.8 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 15.9 | 93.6 | 5.89 | 5 | -0.002 | 32 |
| TE | 7.2 | 42.6 | 5.92 | 2 | 0.09 | 28 |
| RB | 5.9 | 30.0 | 5.08 | 2 | 0.095 | 21 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 19 | 6 | 140 | 1 | 2 | 7.37 | 11.46 | 29 |  |
| deep middle | 12 | 7 | 148 | 0 | 1 | 12.33 | 14.39 | 22 |  |
| deep right | 25 | 5 | 134 | 0 | 1 | 5.36 | 12.14 | 31 |  |
| short left | 80 | 63 | 439 | 4 | 2 | 5.49 | 5.99 | 23 |  |
| short middle | 50 | 37 | 321 | 3 | 1 | 6.42 | 7.32 | 28 |  |
| short right | 105 | 77 | 480 | 1 | 1 | 4.57 | 6.02 | 32 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs SEA: **3.24 yds** (league 2.93; rank 4/32 most allowed). WR 3.21, TE 3.29, cushion 5.23. Sample: 19 receiver-games, 141 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Devon Witherspoon | CB | 10 | 98.9 (100.0 wk10) | 54 | 34 | 254 | 0 | 0 | 4.70 | 74.2 | 6.7 | 0 | 3 | 1 | 4 | 33 (245) | MISSING |
| Josh Jobe | CB | 10 | 98.8 (98.0 wk10) | 46 | 33 | 286 | 2 | 1 | 6.22 | 93.2 | 8.5 | 1 | 1 | 4 | 6 | 22 (169) | MISSING |
| Nehemiah Pritchett | CB | 10 | 33.4 (20.0 wk10) | 21 | 9 | 124 | 0 | 2 | 5.90 | 22.8 | 14.3 | 0 | 3 | 1 | 6 | 6 (60) | MISSING |
| Trevon Diggs | CB | 5 | 11.8 (15.0 wk10) | 1 | 1 | 6 | 0 | 0 | 6.00 | 91.7 | 6.0 | 0 | 0 | 0 | 0 | 1 (6) | MISSING |
| Julian Neal | CB | 1 | 4.0 (4.0 wk2) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Julian Love | S | 9 | 98.6 (100.0 wk10) | 26 | 14 | 169 | 0 | 2 | 6.50 | 42.0 | 11.2 | 0 | 5 | 0 | 7 | 20 (231) | MISSING |
| Nick Emmanwori | S | 9 | 80.8 (97.0 wk10) | 30 | 18 | 163 | 1 | 0 | 5.43 | 85.8 | 4.7 | 0 | 3 | 0 | 3 | 9 (70) | MISSING |
| Ty Okada | S | 6 | 98.5 (100.0 wk10) | 13 | 6 | 60 | 1 | 1 | 4.62 | 53.4 | 12.9 | 0 | 1 | 0 | 2 | 12 (128) | MISSING |
| Rodney Thomas II | S | 7 | 58.4 (2.0 wk9) | 14 | 7 | 62 | 0 | 0 | 4.43 | 62.2 | 13.0 | 0 | 2 | 1 | 3 | 6 (97) | MISSING |
| AJ Finley | S | 2 | 52.0 (100.0 wk3) | 4 | 3 | 31 | 1 | 0 | 7.75 | 136.5 | 12.3 | 0 | 0 | 0 | 0 | 2 (23) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Ernest Jones | 10 | 54 | 36 | 307 | 0 | 5.69 | 73.6 | 4 |
| Drake Thomas | 8 | 26 | 17 | 127 | 1 | 4.88 | 73.7 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 10 | LV | N.Emmanwori | PBU | J.Bech | short_left |
| 10 | LV | J.Love | PBU | J.Bech | short_middle |
| 9 | ARI | N.Emmanwori | PBU | T.McBride | short_right |
| 9 | ARI | J.Jobe | DPI | — | deep_right |
| 9 | ARI | T.Okada | PBU | R.Virgil | deep_middle |
| 9 | ARI | J.Jobe | PBU | E.Hull | short_right |
| 9 | ARI | E.Jones | PBU | R.Virgil | deep_right |
| 8 | CHI | E.Jones | PBU | L.Burden | short_middle |
| 8 | CHI | D.Lawrence | PBU | Z.Thomas | deep_right |
| 8 | CHI | N.Pritchett | PBU | R.Odunze | deep_middle |
| 7 | KC | L.Williams | PBU | C.Allen | short_middle |
| 7 | KC | T.Okada | INT | J.Royals | short_left |
| 6 | DEN | U.Nwosu | PBU | R.Harvey | short_right |
| 6 | DEN | D.Witherspoon | DPI | C.Sutton | deep_left |
| 6 | DEN | D.Witherspoon | PBU | J.Waddle | deep_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
