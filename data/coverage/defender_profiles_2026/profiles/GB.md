# GB defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.5 | 24.1 | — |
| Zone % | 78.5 | 75.4 | — |
| Single-high / MOFC % | 34.7 | 36.5 | — |
| Two-high / MOFO % | 61.0 | 63.5 | — |
| Blitz % | 33.3 | 36.8 | 34.8 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 43.5 / 24.5, 72.0 | — | — |

Sharp YPT allowed: WR 7.2, TE 6.5, RB 5.9, **outside 7.6 vs slot 6.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #25 vs StatRankings #27; blitz rank Sharp #9 vs SR #9 (raw gaps: man -10.6 pts, blitz -3.5 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.3 | 148.3 | 7.31 | 10 | 0.096 | 15 |
| TE | 6.4 | 39.9 | 6.27 | 3 | 0.048 | 31 |
| RB | 5.6 | 32.5 | 5.76 | 2 | 0.1 | 19 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 30 | 15 | 432 | 3 | 4 | 14.4 | 11.46 | 5 | **WEAK** |
| deep middle | 11 | 5 | 99 | 1 | 0 | 9.0 | 14.39 | 30 |  |
| deep right | 21 | 9 | 229 | 1 | 2 | 10.9 | 12.14 | 19 |  |
| short left | 113 | 73 | 570 | 4 | 5 | 5.04 | 5.99 | 29 |  |
| short middle | 70 | 48 | 476 | 3 | 4 | 6.8 | 7.32 | 23 |  |
| short right | 110 | 90 | 621 | 3 | 0 | 5.65 | 6.02 | 23 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs GB: **2.93 yds** (league 2.93; rank 17/32 most allowed). WR 2.90, TE 3.14, cushion 5.91. Sample: 25 receiver-games, 205 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Keisean Nixon | CB | 11 | 96.9 (100.0 wk12) | 68 | 46 | 410 | 1 | 1 | 6.03 | 82.4 | 7.3 | 1 | 7 | 2 | 10 | 37 (356) | MISSING |
| Brandon Cisse | CB | 11 | 84.4 (100.0 wk12) | 45 | 25 | 362 | 3 | 1 | 8.04 | 94.9 | 11.2 | 1 | 7 | 2 | 10 | 20 (284) | MISSING |
| Carrington Valentine | CB | 9 | 22.1 (80.0 wk10) | 20 | 12 | 103 | 1 | 0 | 5.15 | 90.2 | 6.4 | 0 | 3 | 0 | 3 | 10 (78) | MISSING |
| Kamal Hadden | CB | 5 | 4.6 (1.0 wk12) | 4 | 3 | 37 | 0 | 0 | 9.25 | 103.1 | 10.5 | 0 | 0 | 0 | 0 | 2 (29) | MISSING |
| Benjamin St-Juste | CB | 2 | 10.5 (19.0 wk9) | 1 | 1 | 21 | 0 | 0 | 21.00 | 118.8 | 19.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Evan Williams | S | 11 | 99.7 (100.0 wk12) | 39 | 22 | 270 | 3 | 3 | 6.92 | 71.5 | 9.8 | 0 | 5 | 0 | 8 | 33 (430) | MISSING |
| Xavier McKinney | S | 11 | 97.2 (100.0 wk12) | 31 | 14 | 191 | 1 | 6 | 6.16 | 36.6 | 10.9 | 0 | 1 | 0 | 7 | 20 (221) | MISSING |
| Javon Bullard | S | 11 | 67.1 (31.0 wk12) | 46 | 27 | 219 | 3 | 0 | 4.76 | 92.6 | 7.2 | 0 | 6 | 0 | 6 | 20 (158) | MISSING |
| Kitan Oladapo | S | 3 | 11.7 (22.0 wk9) | 1 | 1 | 21 | 0 | 0 | 21.00 | 118.8 | 19.0 | 0 | 0 | 0 | 0 | 2 (42) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Isaiah McDuffie | 10 | 23 | 16 | 146 | 0 | 6.35 | 86.5 | 0 |
| Zaire Franklin | 6 | 16 | 12 | 129 | 1 | 8.06 | 119.0 | 1 |
| Ty'Ron Hopper | 9 | 16 | 12 | 91 | 1 | 5.69 | 69.5 | 4 |
| Edgerrin Cooper | 4 | 15 | 10 | 136 | 0 | 9.07 | 67.6 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | LA | T.Hopper | INT | T.Higbee | short_left |
| 12 | LA | B.Cisse | DPI | X.Smith | deep_middle |
| 10 | MIN | K.Nixon | PBU | J.Jefferson | short_middle |
| 10 | MIN | T.Hopper | PBU | J.Mason | short_right |
| 10 | MIN | K.Nixon | PBU | J.Jefferson | short_middle |
| 10 | MIN | X.McKinney | INT | T.Felton | deep_left |
| 10 | MIN | C.Valentine | PBU | J.Jefferson | short_left |
| 10 | MIN | E.Williams | PBU | T.Felton | short_left |
| 9 | NE | C.Valentine | PBU | M.Hollins | short_left |
| 9 | NE | N.Niemann | PBU | L.Larison | deep_right |
| 9 | NE | X.McKinney | INT | E.Raridon | short_left |
| 9 | NE | E.Williams | INT | K.Williams | deep_left |
| 9 | NE | X.McKinney | INT | M.Hollins | deep_left |
| 8 | CAR | D.Dennis-Sutton | PBU | T.McMillan | short_middle |
| 8 | CAR | X.McKinney | PBU | T.Tremble | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Keisean Nixon | CB | 77.9 | 58.1 | 506.0 | 6.5 | 3.71 | 103 (82) |
| Brandon Cisse | CB | 71.1 | 43.0 | 522.5 | 7.35 | 3.28 | 104 (78) |
| Evan Williams | S | 38.0 | 23.5 | 293.4 | 7.72 | 2.03 | 29 (4) |
| Xavier McKinney | S | 33.1 | 20.3 | 260.6 | 7.87 | 1.4 | 23 (1) |
| Isaiah McDuffie | LB | 26.7 | 19.7 | 164.4 | 6.16 | 1.14 | 8 (7) |
| Zaire Franklin | LB | 25.0 | 18.5 | 146.3 | 5.85 | 0.49 | 37 (20) |
| Ty'Ron Hopper | LB | 23.3 | 17.1 | 123.6 | 5.3 | 0.51 | 23 (22) |
| Javon Bullard | S | 22.9 | 14.3 | 160.6 | 7.01 | 0.94 | 4 (0) |
| Carrington Valentine | CB | 19.3 | 13.2 | 123.3 | 6.39 | 0.67 | 17 (16) |
| Edgerrin Cooper | LB | 9.6 | 7.7 | 66.2 | 6.9 | 0.37 | 4 (1) |

### Upcoming: opposing receivers vs likely GB defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-06 | NO | C.Olave (WR) | 31 | short_right 33%, short_left 29% | Brandon Cisse (35%) | Keisean Nixon (31%) |
| 13 | 2026-12-06 | NO | J.Tyson (WR) | 20 | short_left 35%, short_right 35% | Keisean Nixon (34%) | Brandon Cisse (32%) |
| 13 | 2026-12-06 | NO | D.Vele (WR) | 13 | short_left 46%, short_right 18% | Brandon Cisse (44%) | Keisean Nixon (23%) |
| 13 | 2026-12-06 | NO | A.Kamara (RB) | 10 | short_left 43%, short_right 41% | Isaiah McDuffie (34%) | Ty'Ron Hopper (33%) |

Defender pool = GB players with defensive snaps in their most recent game (2026_12_GB_LA); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Evan Williams | S | 126.3 | 80.9 | 885.9 | 7.01 | 10.47 | 317.1 | 12 |
| Brandon Cisse | CB | 41.1 | 24.2 | 312.1 | 7.59 | 3.99 | 129.2 | 4 |
| Keisean Nixon | CB | 40.3 | 31.4 | 283.3 | 7.03 | 3.74 | 99.2 | 3 |
| Xavier McKinney | S | 16.0 | 9.2 | 148.1 | 9.26 | 3.53 | 89.5 | 5 |
| Isaiah McDuffie | LB | 41.1 | 29.7 | 255.0 | 6.2 | 2.28 | 55.5 | 2 |
| Zaire Franklin | LB | 41.3 | 28.9 | 243.1 | 5.89 | 0.97 | 29.5 | 1 |
| Carrington Valentine | CB | 6.6 | 5.2 | 57.7 | 8.74 | 0.84 | 26.1 | 0 |
| Ty'Ron Hopper | LB | 22.3 | 15.2 | 119.0 | 5.34 | 0.5 | 12.8 | 0 |
| Edgerrin Cooper | LB | 15.8 | 12.7 | 100.4 | 6.35 | 0.41 | 15.6 | 0 |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Keisean Nixon (CB) 68 tgt, 67.6% catch, 6.03 ypt, rating 82.4 [LIMITS YARDS]
**Best / lockdown:** Xavier McKinney (S) 31 tgt, 45.2% catch, 6.16 ypt, rating 36.6 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS]
**Weak zones:** deep left 14.4 ypt

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Carrington Valentine | CB | 7 | 20 | 10% | 60.0 | 5.15 | 8.58 | 0.752 | 90.2 | 1 | 0 | 3 | 69.8 | LIMITS YARDS | small sample (<35 tgts) |
| Brandon Cisse | CB | 10 | 45 | 18% | 55.6 | 8.04 | 14.48 | 0.631 | 94.9 | 3 | 1 | 7 | 47.2 | GIVES UP EXPLOSIVES |  |
| Keisean Nixon | CB | 10 | 68 | 27% | 67.6 | 6.03 | 8.91 | 0.612 | 82.4 | 1 | 1 | 7 | 45.8 | LIMITS YARDS |  |
| Xavier McKinney | S | 10 | 31 | 12% | 45.2 | 6.16 | 13.64 | 0.284 | 36.6 | 1 | 6 | 1 | 88.2 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS | small sample (<35 tgts) |
| Javon Bullard | S | 10 | 46 | 18% | 58.7 | 4.76 | 8.11 | 0.446 | 92.6 | 3 | 0 | 6 | 66.8 | LIMITS YARDS |  |
| Evan Williams | S | 9 | 39 | 16% | 56.4 | 6.92 | 12.27 | 0.391 | 71.5 | 3 | 3 | 5 | 60.8 |  |  |
