# LAC defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 13.3 | 32.3 | — |
| Zone % | 74.5 | 67.4 | — |
| Single-high / MOFC % | 44.2 | 49.3 | — |
| Two-high / MOFO % | 50.6 | 50.7 | — |
| Blitz % | 23.5 | 25.9 | 23.8 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 47.8 / 27.0, 71.0 | — | — |

Sharp YPT allowed: WR 9.0, TE 9.4, RB 4.1, **outside 10.2 vs slot 8.3** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #27 vs StatRankings #16; blitz rank Sharp #23 vs SR #26 (raw gaps: man -19.0 pts, blitz -2.4 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.0 | 153.8 | 9.05 | 13 | 0.257 | 11 |
| TE | 6.2 | 58.3 | 9.4 | 1 | 0.281 | 10 |
| RB | 5.9 | 23.9 | 4.05 | 2 | -0.144 | 27 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 14 | 5 | 189 | 1 | 2 | 13.5 | 11.46 | 12 |  |
| deep middle | 10 | 5 | 157 | 1 | 0 | 15.7 | 14.39 | 12 |  |
| deep right | 23 | 14 | 382 | 2 | 0 | 16.61 | 12.14 | 5 | **WEAK** |
| short left | 81 | 61 | 544 | 5 | 2 | 6.72 | 5.99 | 6 | **WEAK** |
| short middle | 67 | 47 | 495 | 1 | 3 | 7.39 | 7.32 | 14 |  |
| short right | 97 | 71 | 594 | 6 | 1 | 6.12 | 6.02 | 14 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs LAC: **2.91 yds** (league 2.93; rank 19/32 most allowed). WR 2.77, TE 3.42, cushion 6.49. Sample: 17 receiver-games, 123 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cam Hart | CB | 10 | 87.2 (95.0 wk11) | 37 | 22 | 339 | 0 | 2 | 9.16 | 67.3 | 13.3 | 1 | 5 | 0 | 7 | 21 (298) | MISSING |
| Tarheeb Still | CB | 9 | 94.8 (99.0 wk10) | 39 | 25 | 305 | 3 | 1 | 7.82 | 103.0 | 8.1 | 1 | 4 | 1 | 6 | 21 (271) | MISSING |
| Donte Jackson | CB | 7 | 54.6 (82.0 wk11) | 19 | 13 | 215 | 4 | 0 | 11.32 | 145.8 | 10.3 | 0 | 4 | 1 | 5 | 8 (80) | MISSING |
| Isas Waxter | CB | 4 | 22.2 (12.0 wk11) | 10 | 5 | 9 | 0 | 0 | 0.90 | 56.2 | 3.8 | 0 | 0 | 0 | 0 | 5 (16) | MISSING |
| Rodney Shelley | CB | 6 | 12.2 (3.0 wk10) | 10 | 7 | 126 | 2 | 0 | 12.60 | 152.1 | 19.3 | 0 | 1 | 0 | 1 | 3 (73) | MISSING |
| Elijah Molden | DB | 8 | 81.0 (100.0 wk11) | 20 | 15 | 265 | 1 | 0 | 13.25 | 133.3 | 9.0 | 1 | 1 | 0 | 1 | 20 (264) | MISSING |
| Deane Leonard | DB | 5 | 39.0 (70.0 wk11) | 9 | 6 | 74 | 0 | 0 | 8.22 | 91.9 | 5.9 | 0 | 1 | 2 | 3 | 5 (61) | MISSING |
| Tony Jefferson | S | 10 | 66.1 (53.0 wk11) | 23 | 16 | 182 | 1 | 0 | 7.91 | 107.5 | 7.4 | 0 | 2 | 0 | 2 | 12 (118) | MISSING |
| Genesis Smith | S | 10 | 45.2 (25.0 wk11) | 26 | 14 | 211 | 3 | 2 | 8.12 | 87.2 | 12.6 | 0 | 3 | 0 | 5 | 9 (129) | MISSING |
| R.J. Mickens | S | 9 | 39.7 (30.0 wk11) | 10 | 6 | 73 | 0 | 0 | 7.30 | 82.5 | 12.8 | 0 | 1 | 0 | 1 | 10 (147) | MISSING |
| Derwin James | S | 3 | 94.3 (100.0 wk3) | 11 | 7 | 43 | 1 | 0 | 3.91 | 101.7 | 4.5 | 0 | 1 | 0 | 1 | 8 (65) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Daiyan Henley | 9 | 34 | 26 | 233 | 0 | 6.85 | 82.1 | 2 |
| Del'Shawn Phillips | 10 | 21 | 18 | 125 | 1 | 5.95 | 87.5 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | NYJ | D.Leonard | PBU | G.Wilson | short_middle |
| 10 | BAL | R.Mickens | PBU | J.Lane | deep_right |
| 10 | BAL | D.Henley | PBU | J.Lane | short_right |
| 10 | BAL | R.Shelley | PBU | J.Lane | deep_right |
| 10 | BAL | D.Phillips | INT | J.Lane | short_middle |
| 10 | BAL | T.Still | PBU | R.Bateman | short_right |
| 10 | BAL | E.Molden | PBU | R.Bateman | short_right |
| 10 | BAL | C.Hart | PBU | J.Lane | deep_left |
| 10 | BAL | D.Jackson | PBU | R.Bateman | short_middle |
| 10 | BAL | T.Tart | PBU | J.Lane | short_right |
| 9 | HOU | G.Smith | PBU | T.Dell | short_right |
| 9 | HOU | D.Jackson | PBU | T.Dell | short_middle |
| 9 | HOU | D.Henley | INT | K.Boutte | short_middle |
| 8 | LA | T.Still | INT | K.Mumpfield | short_left |
| 6 | KC | C.Hart | INT | A.Armstrong | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Cam Hart | CB | 44.6 | 29.3 | 415.8 | 9.32 | 2.73 | 67 (29) |
| Tarheeb Still | CB | 43.2 | 29.9 | 360.8 | 8.35 | 2.45 | 68 (24) |
| Elijah Molden | CB | 29.6 | 21.0 | 268.0 | 9.05 | 1.97 | 43 (2) |
| Daiyan Henley | LB | 24.5 | 17.9 | 155.9 | 6.36 | 0.65 | 35 (1) |
| Tuli Tuipulotu | LB | 19.1 | 13.7 | 122.2 | 6.4 | 0.9 | 9 (0) |
| Donte Jackson | CB | 17.9 | 12.2 | 163.1 | 9.11 | 1.57 | 5 (0) |
| Khalil Mack | LB | 15.9 | 11.5 | 105.4 | 6.63 | 0.69 | 3 (0) |
| Del'Shawn Phillips | LB | 15.0 | 10.8 | 92.9 | 6.19 | 0.45 | 15 (1) |
| Tony Jefferson | S | 13.4 | 9.4 | 121.6 | 9.07 | 0.62 | 14 (2) |
| Akheem Mesidor | LB | 12.7 | 9.1 | 79.4 | 6.25 | 0.46 | 4 (0) |
| Genesis Smith | S | 9.3 | 5.9 | 87.2 | 9.38 | 0.47 | 0 (0) |
| Derwin James | S | 8.9 | 6.0 | 62.6 | 7.03 | 0.55 | 14 (3) |

### Upcoming: opposing receivers vs likely LAC defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | NE | M.Hollins (WR) | 12 | short_right 34%, deep_right 25% | Elijah Molden (22%) | Cam Hart (21%) |
| 12 | 2026-11-29 | NE | D.Douglas (WR) | 12 | short_right 35%, short_left 22% | Cam Hart (23%) | Elijah Molden (20%) |
| 12 | 2026-11-29 | NE | E.Raridon (TE) | 7 | short_left 37%, short_middle 26% | Cam Hart (13%) | Elijah Molden (11%) |
| 12 | 2026-11-29 | NE | H.Henry (TE) | 6 | short_right 40%, short_left 25% | Cam Hart (11%) | Elijah Molden (10%) |
| 13 | 2026-12-06 | TB | C.Otton (TE) | 11 | short_right 46%, short_middle 22% | Elijah Molden (11%) | Cam Hart (10%) |
| 13 | 2026-12-06 | TB | E.Egbuka (WR) | 10 | short_right 34%, short_left 29% | Cam Hart (21%) | Elijah Molden (19%) |
| 13 | 2026-12-06 | TB | B.Irving (RB) | 9 | short_left 47%, short_right 44% | Tuli Tuipulotu (19%) | Khalil Mack (14%) |
| 13 | 2026-12-06 | TB | K.Gainwell (RB) | 8 | short_right 58%, short_left 35% | Tuli Tuipulotu (18%) | Khalil Mack (15%) |

Defender pool = LAC players with defensive snaps in their most recent game (2026_11_NYJ_LAC); check inactives before use.
