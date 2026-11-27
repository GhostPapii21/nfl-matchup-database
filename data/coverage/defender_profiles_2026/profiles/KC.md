# KC defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 18.8 | 43.0 | — |
| Zone % | 77.3 | 55.9 | — |
| Single-high / MOFC % | 39.5 | 47.5 | — |
| Two-high / MOFO % | 57.1 | 52.5 | — |
| Blitz % | 26.4 | 28.3 | 26.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 42.0 / 23.5, 70.0 | — | — |

Sharp YPT allowed: WR 6.6, TE 6.6, RB 6.5, **outside 6.7 vs slot 7.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #14 vs StatRankings #7; blitz rank Sharp #20 vs SR #22 (raw gaps: man -24.2 pts, blitz -1.9 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.6 | 113.1 | 6.41 | 3 | -0.133 | 30 |
| TE | 9.2 | 59.9 | 6.52 | 5 | 0.06 | 8 |
| RB | 5.5 | 34.8 | 6.38 | 0 | 0.102 | 13 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 27 | 11 | 329 | 3 | 0 | 12.19 | 11.46 | 16 |  |
| deep middle | 17 | 6 | 192 | 0 | 2 | 11.29 | 14.39 | 25 |  |
| deep right | 12 | 2 | 37 | 1 | 0 | 3.08 | 12.14 | 32 |  |
| short left | 103 | 68 | 563 | 0 | 3 | 5.47 | 5.99 | 24 |  |
| short middle | 72 | 49 | 509 | 1 | 1 | 7.07 | 7.32 | 20 |  |
| short right | 124 | 85 | 656 | 3 | 3 | 5.29 | 6.02 | 28 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs KC: **2.9 yds** (league 2.93; rank 20/32 most allowed). WR 2.74, TE 3.19, cushion 5.4. Sample: 28 receiver-games, 213 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mansoor Delane | CB | 8 | 74.2 (67.0 wk12) | 31 | 18 | 255 | 2 | 1 | 8.23 | 92.8 | 13.3 | 2 | 6 | 0 | 7 | 15 (197) | MISSING |
| Christian Roland-Wallace | CB | 11 | 46.7 (64.0 wk12) | 21 | 18 | 134 | 1 | 0 | 6.38 | 109.1 | 3.1 | 0 | 2 | 0 | 2 | 14 (111) | MISSING |
| Kristian Fulton | CB | 10 | 54.0 (32.0 wk12) | 27 | 12 | 123 | 0 | 1 | 4.56 | 42.7 | 7.0 | 0 | 2 | 4 | 7 | 10 (86) | MISSING |
| L'Jarius Sneed | CB | 6 | 63.7 (20.0 wk7) | 43 | 34 | 341 | 1 | 0 | 7.93 | 107.5 | 6.4 | 3 | 3 | 0 | 3 | 24 (213) | MISSING |
| Nohl Williams | DB | 11 | 92.9 (100.0 wk12) | 56 | 25 | 254 | 2 | 2 | 4.54 | 55.2 | 9.5 | 1 | 11 | 0 | 14 | 22 (258) | MISSING |
| Chamarri Conner | DB | 8 | 92.6 (100.0 wk12) | 20 | 13 | 202 | 0 | 0 | 10.10 | 98.3 | 4.9 | 1 | 2 | 1 | 3 | 14 (188) | MISSING |
| Jaden Hicks | DB | 11 | 49.8 (16.0 wk12) | 18 | 10 | 172 | 1 | 0 | 9.56 | 106.7 | 16.8 | 0 | 1 | 0 | 1 | 12 (128) | MISSING |
| Jadon Canady | DB | 6 | 14.5 (13.0 wk12) | 12 | 8 | 108 | 0 | 0 | 9.00 | 95.1 | 10.2 | 0 | 1 | 0 | 1 | 7 (111) | MISSING |
| Alohi Gilman | S | 11 | 81.7 (84.0 wk12) | 15 | 8 | 93 | 1 | 0 | 6.20 | 94.6 | 11.6 | 0 | 1 | 1 | 3 | 14 (212) | MISSING |
| Xavier Nwankpa | S | 6 | 4.2 (7.0 wk12) | 2 | 1 | 8 | 0 | 1 | 4.00 | 20.8 | 8.5 | 0 | 0 | 0 | 1 | 2 (18) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Drue Tranquill | 11 | 33 | 20 | 191 | 0 | 5.79 | 76.7 | 2 |
| Nick Bolton | 11 | 31 | 21 | 183 | 0 | 5.90 | 83.1 | 3 |
| Jack Cochrane | 11 | 11 | 5 | 58 | 0 | 5.27 | 24.1 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | BUF | N.Williams | INT | K.Shakir | short_right |
| 12 | BUF | A.Gilman | INT | D.Knox | short_left |
| 11 | ARI | K.Fulton | PBU | S.Fehoko | short_right |
| 11 | ARI | C.Jones | PBU | T.McBride | short_right |
| 11 | ARI | N.Williams | PBU | H.Wallace | deep_right |
| 11 | ARI | N.Williams | PBU | S.Fehoko | deep_right |
| 11 | ARI | N.Bolton | PBU | H.Wallace | short_left |
| 10 | ATL | K.Fulton | PBU | C.Blair | short_left |
| 10 | ATL | N.Williams | INT | C.Blair | deep_middle |
| 10 | ATL | J.Canady | PBU | D.London | short_middle |
| 10 | ATL | A.Gillotte | PBU | D.London | short_middle |
| 10 | ATL | M.Delane | PBU | J.Dotson | short_left |
| 10 | ATL | C.Conner | DPI | D.London | deep_right |
| 10 | ATL | N.Williams | PBU | D.London | short_left |
| 10 | ATL | G.Karlaftis | PBU | D.London | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.
