# LA defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 22.3 | 40.1 | — |
| Zone % | 70.8 | 59.3 | — |
| Single-high / MOFC % | 37.8 | 45.7 | — |
| Two-high / MOFO % | 57.9 | 54.3 | — |
| Blitz % | 26.6 | 30.4 | 28.2 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 50.6 / 19.0, 63.0 | — | — |

Sharp YPT allowed: WR 7.4, TE 5.7, RB 6.3, **outside 7.1 vs slot 8.5** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #10 vs StatRankings #8; blitz rank Sharp #19 vs SR #17 (raw gaps: man -17.8 pts, blitz -3.8 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 15.2 | 112.7 | 7.43 | 10 | 0.063 | 31 |
| TE | 7.9 | 45.0 | 5.69 | 1 | -0.241 | 23 |
| RB | 6.5 | 41.1 | 6.28 | 1 | -0.066 | 4 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 14 | 5 | 149 | 1 | 0 | 10.64 | 11.46 | 17 |  |
| deep middle | 16 | 6 | 140 | 1 | 2 | 8.75 | 14.39 | 31 |  |
| deep right | 20 | 5 | 175 | 1 | 2 | 8.75 | 12.14 | 26 |  |
| short left | 111 | 73 | 641 | 1 | 2 | 5.77 | 5.99 | 19 |  |
| short middle | 65 | 40 | 424 | 2 | 2 | 6.52 | 7.32 | 27 |  |
| short right | 102 | 78 | 659 | 6 | 3 | 6.46 | 6.02 | 8 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs LA: **2.6 yds** (league 2.93; rank 31/32 most allowed). WR 2.65, TE 2.51, cushion 5.12. Sample: 25 receiver-games, 167 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Josh Wallace | CB | 11 | 78.1 (93.0 wk12) | 40 | 24 | 207 | 0 | 1 | 5.18 | 63.2 | 7.2 | 0 | 4 | 3 | 8 | 25 (255) | MISSING |
| Trent McDuffie | CB | 8 | 95.6 (100.0 wk12) | 30 | 13 | 86 | 0 | 2 | 2.87 | 22.9 | 7.6 | 0 | 7 | 1 | 10 | 15 (100) | MISSING |
| Jaylen Watson | CB | 7 | 84.0 (67.0 wk8) | 38 | 19 | 261 | 2 | 1 | 6.87 | 78.9 | 11.9 | 0 | 8 | 0 | 9 | 14 (162) | MISSING |
| Emmanuel Forbes | CB | 9 | 48.1 (76.0 wk12) | 26 | 13 | 66 | 2 | 0 | 2.54 | 81.9 | 9.3 | 0 | 5 | 1 | 7 | 12 (59) | MISSING |
| Cam Lampkin | CB | 2 | 4.5 (3.0 wk10) | 1 | 1 | 12 | 0 | 0 | 12.00 | 116.7 | 11.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Quentin Lake | S | 11 | 100.0 (100.0 wk12) | 56 | 33 | 404 | 2 | 3 | 7.21 | 70.8 | 8.5 | 1 | 10 | 2 | 15 | 30 (308) | MISSING |
| Kamren Curl | S | 11 | 93.6 (100.0 wk12) | 21 | 16 | 178 | 1 | 0 | 8.48 | 116.8 | 9.3 | 0 | 3 | 0 | 3 | 25 (424) | MISSING |
| Kamren Kinchens | S | 9 | 67.2 (54.0 wk12) | 15 | 12 | 153 | 2 | 1 | 10.20 | 121.0 | 13.1 | 0 | 4 | 0 | 5 | 12 (191) | MISSING |
| Jaylen McCollough | S | 11 | 37.2 (37.0 wk12) | 9 | 9 | 141 | 1 | 0 | 15.67 | 155.8 | 4.9 | 0 | 0 | 0 | 1 | 6 (53) | MISSING |
| Maximus Pulley | S | 1 | 2.0 (2.0 wk12) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Nathan Landman | 10 | 24 | 15 | 79 | 1 | 3.29 | 81.8 | 2 |
| Omar Speights | 11 | 19 | 13 | 109 | 0 | 5.74 | 83.0 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | GB | E.Forbes | INT | B.Melton | deep_right |
| 12 | GB | J.McCollough | INT | M.Golden | deep_middle |
| 12 | GB | Q.Lake | PBU | S.Williams | short_right |
| 12 | GB | A.Donald | PBU | K.Johnson | short_middle |
| 12 | GB | Q.Lake | PBU | M.Golden | deep_middle |
| 12 | GB | T.McDuffie | PBU | M.Golden | short_right |
| 12 | GB | K.Kinchens | PBU | T.Kraft | short_middle |
| 12 | GB | K.Kinchens | PBU | J.Sturdivant | short_middle |
| 10 | ARI | W.Bailey | INT | T.Allgeier | short_middle |
| 10 | ARI | K.Kinchens | INT | D.Duvernay | short_middle |
| 10 | ARI | K.Curl | PBU | Z.Jones | deep_right |
| 9 | WAS | E.Forbes | PBU | V.Jefferson | deep_left |
| 9 | WAS | B.Young | PBU | A.Ekeler | short_middle |
| 9 | WAS | E.Forbes | PBU | V.Jefferson | short_left |
| 9 | WAS | E.Forbes | PBU | C.Okonkwo | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Josh Wallace | CB | 45.3 | 27.9 | 301.7 | 6.66 | 1.65 | 56 (19) |
| Trent McDuffie | CB | 39.5 | 22.7 | 260.9 | 6.61 | 2.81 | 53 (29) |
| Jaylen Watson | CB | 34.5 | 19.2 | 244.1 | 7.08 | 1.73 | 41 (28) |
| Quentin Lake | S | 33.3 | 21.1 | 210.7 | 6.33 | 0.82 | 57 (5) |
| Kam Curl | S | 26.0 | 15.6 | 180.4 | 6.94 | 0.82 | 23 (3) |
| Emmanuel Forbes | CB | 24.4 | 13.9 | 176.4 | 7.23 | 0.76 | 15 (13) |
| Byron Young | LB | 23.9 | 16.9 | 157.7 | 6.6 | 0.74 | 30 (4) |
| Nate Landman | LB | 23.2 | 16.4 | 143.2 | 6.17 | 0.43 | 31 (4) |
| Josaiah Stewart | LB | 17.9 | 12.3 | 114.2 | 6.38 | 0.44 | 3 (0) |
| Kamren Kinchens | S | 14.8 | 10.1 | 109.9 | 7.43 | 0.34 | 9 (2) |
| Omar Speights | LB | 14.1 | 10.0 | 93.8 | 6.65 | 0.68 | 9 (0) |
| Jaylen McCollough | S | 9.2 | 5.8 | 62.8 | 6.83 | 0.27 | 0 (0) |

### Upcoming: opposing receivers vs likely LA defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-03 | KC | R.Rice (WR) | 24 | short_right 35%, short_left 31% | Josh Wallace (24%) | Trent McDuffie (23%) |
| 13 | 2026-12-03 | KC | T.Kelce (TE) | 22 | short_right 44%, short_middle 23% | Quentin Lake (14%) | Kam Curl (14%) |
| 13 | 2026-12-03 | KC | X.Worthy (WR) | 16 | short_right 44%, short_left 21% | Trent McDuffie (26%) | Josh Wallace (22%) |
| 13 | 2026-12-03 | KC | E.Johnson (RB) | 15 | short_right 48%, short_left 42% | Byron Young (18%) | Myles Garrett (16%) |

Defender pool = LA players with defensive snaps in their most recent game (2026_12_GB_LA); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Quentin Lake | S | 79.0 | 48.0 | 527.2 | 6.67 | 5.53 | 175.2 | 8 |
| Josh Wallace | CB | 40.4 | 24.8 | 311.0 | 7.7 | 4.83 | 161.6 | 2 |
| Kam Curl | S | 19.6 | 9.0 | 146.9 | 7.49 | 3.63 | 89.9 | 5 |
| Nate Landman | LB | 45.4 | 31.7 | 285.5 | 6.29 | 2.78 | 99.3 | 4 |
| Byron Young | LB | 51.2 | 34.8 | 312.0 | 6.09 | 2.36 | 74.9 | 1 |
| Emmanuel Forbes | CB | 29.3 | 16.9 | 171.9 | 5.87 | 2.35 | 71.3 | 1 |
| Jaylen Watson | CB | 19.6 | 13.1 | 163.0 | 8.32 | 2.02 | 72.4 | 3 |
| Trent McDuffie | CB | 22.2 | 14.6 | 145.7 | 6.56 | 1.82 | 66.6 | 2 |
| Kamren Kinchens | S | 11.0 | 7.5 | 67.6 | 6.15 | 0.39 | 15.2 | 0 |
| Josaiah Stewart | LB | 7.7 | 4.4 | 41.1 | 5.34 | 0.23 | 8.7 | 0 |
