# NYG defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 24.2 | 43.3 | — |
| Zone % | 70.2 | 56.2 | — |
| Single-high / MOFC % | 46.6 | 51.0 | — |
| Two-high / MOFO % | 50.3 | 49.0 | — |
| Blitz % | 36.3 | 40.3 | 38.7 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 43.1 / 29.3, 74.0 | — | — |

Sharp YPT allowed: WR 6.9, TE 5.6, RB 5.5, **outside 7.4 vs slot 6.6** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #6 vs StatRankings #6; blitz rank Sharp #4 vs SR #4 (raw gaps: man -19.1 pts, blitz -4.0 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.2 | 139.2 | 6.89 | 12 | 0.053 | 22 |
| TE | 8.0 | 44.5 | 5.56 | 3 | 0.03 | 25 |
| RB | 4.1 | 22.7 | 5.54 | 3 | 0.083 | 28 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 26 | 8 | 157 | 0 | 2 | 6.04 | 11.46 | 32 |  |
| deep middle | 14 | 7 | 174 | 1 | 0 | 12.43 | 14.39 | 21 |  |
| deep right | 22 | 8 | 228 | 1 | 1 | 10.36 | 12.14 | 23 |  |
| short left | 113 | 69 | 604 | 5 | 6 | 5.35 | 5.99 | 27 |  |
| short middle | 54 | 37 | 367 | 7 | 0 | 6.8 | 7.32 | 23 |  |
| short right | 94 | 75 | 534 | 4 | 0 | 5.68 | 6.02 | 22 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NYG: **2.59 yds** (league 2.93; rank 32/32 most allowed). WR 2.44, TE 3.14, cushion 4.8. Sample: 21 receiver-games, 175 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Deonte Banks | CB | 8 | 97.4 (97.0 wk11) | 51 | 23 | 210 | 4 | 2 | 4.12 | 66.6 | 9.3 | 0 | 12 | 3 | 17 | 16 (154) | MISSING |
| Greg Newsome II | CB | 9 | 83.2 (6.0 wk11) | 39 | 22 | 255 | 0 | 1 | 6.54 | 65.7 | 12.2 | 0 | 7 | 1 | 9 | 20 (251) | MISSING |
| Andru Phillips | CB | 10 | 73.9 (83.0 wk11) | 45 | 27 | 292 | 2 | 0 | 6.49 | 93.9 | 4.4 | 1 | 5 | 4 | 9 | 20 (204) | MISSING |
| Paulson Adebo | CB | 3 | 70.0 (93.0 wk11) | 11 | 4 | 47 | 0 | 1 | 4.27 | 12.3 | 22.8 | 0 | 3 | 0 | 4 | 4 (47) | MISSING |
| Colton Hood | CB | 4 | 52.2 (4.0 wk11) | 13 | 10 | 102 | 3 | 0 | 7.85 | 138.5 | 11.2 | 0 | 0 | 0 | 0 | 6 (49) | MISSING |
| Nic Jones | CB | 3 | 17.0 (43.0 wk6) | 2 | 2 | 25 | 1 | 0 | 12.50 | 158.3 | 9.5 | 0 | 0 | 0 | 0 | 1 (7) | MISSING |
| Jevon Holland | S | 9 | 100.0 (100.0 wk11) | 29 | 12 | 213 | 3 | 4 | 7.34 | 62.1 | 11.2 | 0 | 3 | 0 | 6 | 17 (254) | MISSING |
| Ar'Darius Washington | S | 9 | 51.4 (100.0 wk11) | 25 | 15 | 164 | 0 | 1 | 6.56 | 62.7 | 12.1 | 0 | 5 | 1 | 7 | 17 (171) | MISSING |
| Tyler Nubin | S | 7 | 49.4 (10.0 wk11) | 18 | 9 | 163 | 0 | 0 | 9.06 | 81.5 | 11.7 | 1 | 3 | 0 | 3 | 9 (102) | MISSING |
| Jason Pinnock | S | 6 | 54.8 (22.0 wk10) | 9 | 5 | 73 | 2 | 0 | 8.11 | 121.8 | 7.7 | 0 | 2 | 0 | 2 | 3 (41) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Arvell Reese | 10 | 41 | 35 | 178 | 1 | 4.34 | 82.7 | 2 |
| Micah McFadden | 5 | 23 | 14 | 121 | 1 | 5.26 | 89.2 | 0 |
| Tremaine Edmunds | 6 | 18 | 17 | 152 | 1 | 8.44 | 120.4 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | JAX | A.Phillips | PBU | J.Meyers | short_left |
| 11 | JAX | A.Washington | PBU | J.Meyers | short_middle |
| 11 | JAX | P.Adebo | PBU | P.Washington | deep_middle |
| 11 | JAX | P.Adebo | INT | J.Meyers | short_left |
| 11 | JAX | P.Adebo | PBU | P.Washington | deep_middle |
| 11 | JAX | A.Phillips | PBU | P.Washington | short_left |
| 11 | JAX | D.Banks | PBU | Bri.Thomas | short_middle |
| 11 | JAX | A.Phillips | PBU | J.Meyers | short_left |
| 11 | JAX | A.Washington | PBU | J.Cameron | short_middle |
| 11 | JAX | P.Adebo | PBU | J.Meyers | short_left |
| 11 | JAX | D.Banks | INT | P.Washington | short_left |
| 11 | JAX | D.Banks | PBU | P.Washington | deep_left |
| 11 | JAX | J.Holland | PBU | P.Washington | deep_middle |
| 11 | JAX | G.Newsome | PBU | P.Washington | deep_middle |
| 10 | WAS | D.Banks | DPI | T.Burks | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Deonte Banks | CB | 51.7 | 27.2 | 279.9 | 5.41 | 1.98 | 91 (64) |
| Greg Newsome II | CB | 43.8 | 27.6 | 348.8 | 7.96 | 2.27 | 52 (33) |
| Andru Phillips | CB | 39.2 | 23.2 | 246.6 | 6.29 | 1.79 | 21 (6) |
| Arvell Reese | LB | 30.0 | 23.0 | 170.8 | 5.69 | 2.24 | 34 (6) |
| Jevon Holland | S | 22.9 | 12.8 | 148.2 | 6.47 | 0.8 | 12 (2) |
| Tremaine Edmunds | LB | 17.0 | 13.3 | 100.4 | 5.91 | 1.33 | 20 (7) |
| Abdul Carter | LB | 16.6 | 12.2 | 95.5 | 5.75 | 1.25 | 4 (0) |
| Paulson Adebo | CB | 16.1 | 8.2 | 132.7 | 8.24 | 0.97 | 19 (16) |
| Kayvon Thibodeaux | LB | 15.8 | 10.4 | 96.0 | 6.08 | 1.2 | 6 (0) |
| Ar'Darius Washington | S | 14.3 | 8.3 | 96.6 | 6.76 | 0.85 | 14 (0) |
| Micah McFadden | LB | 13.2 | 9.8 | 74.4 | 5.64 | 0.64 | 18 (7) |
| Colton Hood | CB | 11.5 | 8.0 | 82.9 | 7.21 | 0.62 | 16 (8) |

### Upcoming: opposing receivers vs likely NYG defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | IND | T.Warren (TE) | 15 | short_left 36%, short_middle 30% | Ar'Darius Washington (13%) | Jevon Holland (12%) |
| 12 | 2026-11-29 | IND | J.Taylor (RB) | 14 | short_left 58%, short_right 31% | Arvell Reese (18%) | Micah McFadden (18%) |
| 12 | 2026-11-29 | IND | K.Allen (WR) | 8 | short_left 36%, short_right 32% | Deonte Banks (20%) | Andru Phillips (20%) |
| 12 | 2026-11-29 | IND | A.Dulin (WR) | 8 | short_right 53%, short_left 20% | Paulson Adebo (21%) | Andru Phillips (19%) |
| 13 | 2026-12-06 | SF | G.Kittle (TE) | 19 | short_left 37%, short_middle 25% | Jevon Holland (14%) | Ar'Darius Washington (14%) |
| 13 | 2026-12-06 | SF | K.Allen (WR) | 11 | short_left 36%, short_right 32% | Deonte Banks (20%) | Andru Phillips (20%) |
| 13 | 2026-12-06 | SF | C.McCaffrey (RB) | 10 | short_left 46%, short_right 37% | Arvell Reese (19%) | Micah McFadden (18%) |
| 13 | 2026-12-06 | SF | J.Watkins (WR) | 8 | deep_left 24%, deep_middle 24% | Paulson Adebo (26%) | Deonte Banks (19%) |

Defender pool = NYG players with defensive snaps in their most recent game (2026_11_JAX_NYG); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Andru Phillips | CB | 68.7 | 40.3 | 458.3 | 6.67 | 6.25 | 173.1 | 5 |
| Greg Newsome II | CB | 33.7 | 22.2 | 268.3 | 7.96 | 3.42 | 107.6 | 6 |
| Ar'Darius Washington | S | 20.7 | 12.8 | 145.9 | 7.05 | 2.69 | 66.2 | 2 |
| Jevon Holland | S | 16.8 | 6.8 | 121.4 | 7.23 | 2.53 | 73.6 | 2 |
| Tyler Nubin | S | 26.2 | 17.7 | 171.2 | 6.53 | 2.52 | 57.7 | 4 |
| Tremaine Edmunds | LB | 29.0 | 22.8 | 183.4 | 6.32 | 1.86 | 48.5 | 1 |
| Deonte Banks | CB | 38.8 | 19.1 | 197.2 | 5.08 | 1.55 | 32.8 | 3 |
| Arvell Reese | LB | 40.6 | 30.7 | 223.6 | 5.51 | 1.13 | 30.0 | 0 |
| Colton Hood | CB | 9.6 | 6.3 | 76.8 | 8.0 | 0.97 | 20.3 | 1 |
| Micah McFadden | LB | 21.4 | 15.4 | 130.7 | 6.11 | 0.83 | 28.2 | 0 |
| Jason Pinnock | S | 13.4 | 7.2 | 65.4 | 4.88 | 0.58 | 16.1 | 1 |

### Rest of Week 12: receivers vs likely NYG window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | IND | T.Warren (TE) | 15 | 2% | Ar'Darius Washington (52%, 2.69) | Arvell Reese (17%, 1.13) |
| 2026-11-29 | IND | J.Taylor (RB) | 14 | 0% | Arvell Reese (60%, 1.13) | Micah McFadden (17%, 0.83) |
| 2026-11-29 | IND | K.Allen (WR) | 8 | 7% | Andru Phillips (35%, 6.25) | Paulson Adebo (18%, 0.67) |
| 2026-11-29 | IND | A.Dulin (WR) | 8 | 20% | Andru Phillips (30%, 6.25) | Paulson Adebo (25%, 0.67) |
