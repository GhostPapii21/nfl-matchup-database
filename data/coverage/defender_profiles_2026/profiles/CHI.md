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

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Jaylon Johnson | CB | 50.5 | 31.0 | 465.5 | 9.22 | 1.72 | 66 (44) |
| Cam Lewis | CB | 45.2 | 31.0 | 435.3 | 9.63 | 1.68 | 43 (29) |
| Dillon Thieneman | CB | 45.1 | 29.1 | 379.9 | 8.42 | 2.08 | 22 (2) |
| Devin Bush | LB | 36.1 | 26.3 | 240.4 | 6.66 | 1.66 | 48 (22) |
| Tyrique Stevenson | CB | 34.5 | 18.6 | 263.1 | 7.63 | 1.9 | 61 (29) |
| Malik Muhammad | CB | 29.7 | 18.2 | 260.8 | 8.78 | 1.74 | 42 (5) |
| T.J. Edwards | LB | 27.2 | 19.2 | 136.7 | 5.03 | 1.04 | 28 (21) |
| D'Marco Jackson | LB | 12.0 | 9.2 | 120.5 | 10.04 | 1.19 | 5 (2) |
| Clark Phillips III | CB | 10.5 | 6.4 | 75.9 | 7.23 | 0.34 | 0 (0) |
| Kyler Gordon | CB | 10.3 | 5.8 | 85.1 | 8.26 | 0.42 | 5 (2) |
| Xavier Woods | CB | 7.8 | 5.1 | 56.5 | 7.24 | 0.2 | 0 (0) |
| Noah Sewell | LB | 7.3 | 4.9 | 44.3 | 6.07 | 0.32 | 6 (0) |

### Upcoming: opposing receivers vs likely CHI defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-06 | JAX | P.Washington (WR) | 33 | short_left 36%, deep_left 22% | Malik Muhammad (25%) | Cam Lewis (18%) |
| 13 | 2026-12-06 | JAX | J.Meyers (WR) | 22 | short_left 36%, short_middle 25% | Malik Muhammad (20%) | Cam Lewis (20%) |
| 13 | 2026-12-06 | JAX | J.Cameron (WR) | 11 | short_middle 29%, short_left 29% | Cam Lewis (20%) | Dillon Thieneman (19%) |
| 13 | 2026-12-06 | JAX | B.Strange (TE) | 8 | short_left 35%, short_middle 28% | Devin Bush (16%) | T.J. Edwards (15%) |

Defender pool = CHI players with defensive snaps in their most recent game (2026_12_CHI_DET); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Dillon Thieneman | S | 54.0 | 33.8 | 519.8 | 9.63 | 7.28 | 274.9 | 8 |
| Cam Lewis | S | 23.5 | 15.2 | 341.3 | 14.52 | 6.47 | 241.2 | 6 |
| Jaylon Johnson | CB | 36.1 | 23.6 | 331.5 | 9.18 | 4.92 | 161.9 | 6 |
| Malik Muhammad | CB | 30.1 | 18.2 | 242.4 | 8.05 | 3.24 | 108.4 | 4 |
| Tyrique Stevenson | CB | 38.2 | 21.9 | 295.6 | 7.74 | 3.04 | 112.9 | 4 |
| T.J. Edwards | LB | 44.7 | 31.5 | 255.2 | 5.71 | 2.06 | 67.0 | 2 |
| Clark Phillips III | CB | 21.9 | 13.3 | 142.1 | 6.49 | 1.68 | 51.1 | 1 |
| Devin Bush | LB | 43.6 | 29.8 | 251.3 | 5.76 | 1.4 | 43.4 | 0 |
| Kyler Gordon | CB | 15.9 | 9.1 | 126.2 | 7.94 | 1.03 | 43.6 | 0 |
| D'Marco Jackson | LB | 15.0 | 13.5 | 111.4 | 7.43 | 0.63 | 27.5 | 1 |
