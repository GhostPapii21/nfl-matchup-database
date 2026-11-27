# NO defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 16.9 | 38.0 | — |
| Zone % | 74.2 | 59.9 | — |
| Single-high / MOFC % | 64.2 | 66.2 | — |
| Two-high / MOFO % | 32.2 | 33.8 | — |
| Blitz % | 34.4 | 39.7 | 37.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 43.5 / 23.0, 70.0 | — | — |

Sharp YPT allowed: WR 8.5, TE 8.0, RB 7.4, **outside 8.6 vs slot 8.9** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #19 vs StatRankings #11; blitz rank Sharp #8 vs SR #5 (raw gaps: man -21.1 pts, blitz -5.3 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 16.5 | 139.5 | 8.45 | 7 | 0.123 | 21 |
| TE | 7.9 | 64.1 | 8.11 | 6 | 0.381 | 6 |
| RB | 5.3 | 39.0 | 7.36 | 2 | 0.105 | 7 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 25 | 15 | 431 | 1 | 1 | 17.24 | 11.46 | 2 | **WEAK** |
| deep middle | 12 | 6 | 183 | 2 | 1 | 15.25 | 14.39 | 14 |  |
| deep right | 24 | 10 | 285 | 2 | 0 | 11.88 | 12.14 | 18 |  |
| short left | 97 | 69 | 587 | 5 | 1 | 6.05 | 5.99 | 14 |  |
| short middle | 58 | 43 | 371 | 1 | 1 | 6.4 | 7.32 | 29 |  |
| short right | 81 | 60 | 569 | 4 | 1 | 7.02 | 6.02 | 3 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NO: **2.97 yds** (league 2.93; rank 15/32 most allowed). WR 2.94, TE 3.03, cushion 6.63. Sample: 18 receiver-games, 150 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kool-Aid McKinstry | CB | 10 | 94.0 (100.0 wk11) | 47 | 28 | 392 | 2 | 0 | 8.34 | 100.7 | 11.3 | 1 | 7 | 1 | 8 | 23 (314) | MISSING |
| Quincy Riley | CB | 10 | 68.3 (100.0 wk11) | 36 | 21 | 275 | 4 | 0 | 7.64 | 119.6 | 10.3 | 2 | 5 | 0 | 5 | 15 (171) | MISSING |
| Martin Emerson | CB | 7 | 52.9 (57.0 wk10) | 27 | 14 | 247 | 1 | 2 | 9.15 | 64.9 | 11.6 | 1 | 2 | 2 | 6 | 16 (194) | MISSING |
| Jordan Howden | DB | 8 | 29.1 (100.0 wk11) | 6 | 2 | 32 | 0 | 0 | 5.33 | 52.1 | 20.0 | 0 | 1 | 0 | 1 | 3 (70) | MISSING |
| Lorenzo Styles Jr. | DB | 1 | 3.0 (3.0 wk6) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Julian Blackmon | S | 10 | 97.6 (100.0 wk11) | 26 | 16 | 268 | 4 | 2 | 10.31 | 103.8 | 16.4 | 1 | 0 | 0 | 2 | 17 (251) | MISSING |
| Justin Reid | S | 9 | 89.9 (79.0 wk10) | 35 | 24 | 328 | 3 | 0 | 9.37 | 126.8 | 7.1 | 1 | 0 | 0 | 0 | 21 (241) | MISSING |
| Jonas Sanker | S | 10 | 69.6 (64.0 wk11) | 50 | 32 | 336 | 1 | 0 | 6.72 | 90.1 | 6.2 | 1 | 4 | 1 | 5 | 26 (305) | MISSING |
| Michael Reid | S | 1 | 2.0 (2.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Kaden Elliss | 7 | 33 | 26 | 280 | 0 | 8.48 | 102.0 | 2 |
| Pete Werner | 9 | 32 | 22 | 201 | 1 | 6.28 | 96.0 | 2 |
| Danny Stutsman | 9 | 13 | 9 | 80 | 0 | 6.15 | 53.4 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | CHI | K.McKinstry | PBU | K.Raymond | short_right |
| 11 | CHI | D.Stutsman | INT | L.Burden | short_middle |
| 11 | CHI | J.Howden | PBU | K.Raymond | deep_middle |
| 10 | CAR | K.McKinstry | DPI | J.Coker | short_middle |
| 10 | CAR | J.Sanker | PBU | J.Coker | short_middle |
| 10 | CAR | K.Elliss | PBU | T.McMillan | short_left |
| 10 | CAR | M.Emerson | DPI | T.McMillan | short_left |
| 10 | CAR | Q.Riley | PBU | T.McMillan | short_middle |
| 10 | CAR | Q.Riley | PBU | T.McMillan | deep_right |
| 10 | CAR | J.Sanker | PBU | J.Coker | short_left |
| 9 | CLE | C.Granderson | PBU | D.Sampson | short_left |
| 9 | CLE | C.Young | PBU | D.Sampson | short_left |
| 9 | CLE | K.Boyd | PBU | D.Sampson | short_right |
| 9 | CLE | A.Jennings | PBU | M.Corley | short_left |
| 9 | CLE | J.Sanker | PBU | B.Whiteheart | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Kool-Aid McKinstry | CB | 61.0 | 39.9 | 501.8 | 8.23 | 3.52 | 74 (43) |
| Quincy Riley | CB | 46.2 | 30.1 | 370.6 | 8.02 | 2.27 | 54 (40) |
| Kaden Elliss | LB | 33.3 | 25.7 | 249.4 | 7.49 | 1.3 | 49 (30) |
| Martin Emerson | CB | 27.8 | 16.2 | 213.8 | 7.69 | 0.81 | 32 (24) |
| Julian Blackmon | S | 27.2 | 18.0 | 263.3 | 9.68 | 1.91 | 22 (4) |
| Pete Werner | LB | 26.8 | 20.6 | 190.9 | 7.12 | 0.85 | 24 (13) |
| Justin Reid | S | 23.7 | 16.7 | 205.5 | 8.67 | 1.29 | 16 (2) |
| Jonas Sanker | S | 21.1 | 14.8 | 180.7 | 8.56 | 1.32 | 9 (0) |
| Danny Stutsman | LB | 17.3 | 13.1 | 137.7 | 7.96 | 1.24 | 10 (4) |
| Jordan Howden | CB | 10.9 | 6.7 | 99.6 | 9.14 | 0.37 | 7 (6) |

### Upcoming: opposing receivers vs likely NO defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | CIN | J.Chase (WR) | 35 | short_right 33%, short_left 32% | Quincy Riley (29%) | Kool-Aid McKinstry (26%) |
| 12 | 2026-11-29 | CIN | C.Brown (RB) | 20 | short_right 42%, short_left 39% | Kaden Elliss (35%) | Danny Stutsman (32%) |
| 12 | 2026-11-29 | CIN | T.Higgins (WR) | 15 | short_right 32%, short_left 28% | Quincy Riley (27%) | Kool-Aid McKinstry (26%) |
| 12 | 2026-11-29 | CIN | M.Gesicki (TE) | 10 | short_left 29%, short_middle 21% | Julian Blackmon (20%) | Quincy Riley (15%) |
| 13 | 2026-12-06 | GB | M.Golden (WR) | 24 | short_left 28%, short_right 24% | Quincy Riley (29%) | Kool-Aid McKinstry (25%) |
| 13 | 2026-12-06 | GB | C.Watson (WR) | 17 | short_right 30%, short_left 27% | Jordan Howden (28%) | Kool-Aid McKinstry (24%) |
| 13 | 2026-12-06 | GB | T.Kraft (TE) | 12 | short_right 41%, short_middle 28% | Julian Blackmon (20%) | Kaden Elliss (15%) |
| 13 | 2026-12-06 | GB | S.Williams (WR) | 9 | short_left 33%, short_middle 28% | Jordan Howden (26%) | Kool-Aid McKinstry (25%) |

Defender pool = NO players with defensive snaps in their most recent game (2026_11_NO_CHI); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Justin Reid | S | 71.6 | 48.7 | 576.4 | 8.05 | 8.08 | 225.1 | 8 |
| Quincy Riley | CB | 31.1 | 21.0 | 290.1 | 9.33 | 4.44 | 141.1 | 5 |
| Julian Blackmon | S | 19.3 | 13.3 | 247.0 | 12.8 | 4.3 | 146.0 | 5 |
| Kaden Elliss | LB | 50.1 | 39.8 | 350.6 | 7.0 | 4.27 | 108.6 | 6 |
| Kool-Aid McKinstry | CB | 37.7 | 20.5 | 298.0 | 7.9 | 3.75 | 136.4 | 4 |
| Jonas Sanker | S | 19.2 | 12.2 | 162.6 | 8.47 | 2.95 | 104.2 | 3 |
| Martin Emerson | CB | 14.5 | 7.4 | 112.9 | 7.79 | 2.07 | 75.7 | 2 |
| Danny Stutsman | LB | 19.8 | 15.4 | 160.1 | 8.09 | 1.82 | 54.4 | 0 |
| Pete Werner | LB | 31.9 | 23.9 | 207.5 | 6.5 | 1.06 | 29.6 | 0 |

### Rest of Week 12: receivers vs likely NO window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | CIN | J.Chase (WR) | 35 | 16% | Julian Blackmon (43%, 4.3) | Kool-Aid McKinstry (21%, 3.75) |
| 2026-11-29 | CIN | C.Brown (RB) | 20 | 0% | Kaden Elliss (62%, 4.27) | Danny Stutsman (18%, 1.82) |
| 2026-11-29 | CIN | T.Higgins (WR) | 15 | 12% | Julian Blackmon (44%, 4.3) | Kool-Aid McKinstry (20%, 3.75) |
| 2026-11-29 | CIN | M.Gesicki (TE) | 10 | 12% | Julian Blackmon (59%, 4.3) | Kaden Elliss (18%, 4.27) |
