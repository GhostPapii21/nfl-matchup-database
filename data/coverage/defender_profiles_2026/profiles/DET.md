# DET defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 20.3 | 38.2 | — |
| Zone % | 74.8 | 59.2 | — |
| Single-high / MOFC % | 48.5 | 57.4 | — |
| Two-high / MOFO % | 49.0 | 42.6 | — |
| Blitz % | 22.1 | 29.8 | 27.3 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 47.8 / 26.6, 54.0 | — | — |

Sharp YPT allowed: WR 7.5, TE 7.9, RB 6.0, **outside 7.3 vs slot 8.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #13 vs StatRankings #10; blitz rank Sharp #27 vs SR #19 (raw gaps: man -17.9 pts, blitz -7.7 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.2 | 150.5 | 7.46 | 10 | 0.268 | 13 |
| TE | 9.5 | 73.3 | 7.75 | 11 | 0.326 | 3 |
| RB | 6.0 | 41.1 | 6.85 | 2 | 0.229 | 4 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 22 | 6 | 146 | 0 | 1 | 6.64 | 11.46 | 31 |  |
| deep middle | 18 | 10 | 296 | 2 | 2 | 16.44 | 14.39 | 11 |  |
| deep right | 38 | 18 | 473 | 5 | 1 | 12.45 | 12.14 | 16 |  |
| short left | 113 | 76 | 542 | 4 | 2 | 4.8 | 5.99 | 32 |  |
| short middle | 60 | 51 | 537 | 3 | 1 | 8.95 | 7.32 | 1 | **WEAK** |
| short right | 142 | 107 | 927 | 9 | 0 | 6.53 | 6.02 | 7 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs DET: **2.67 yds** (league 2.93; rank 27/32 most allowed). WR 2.52, TE 3.08, cushion 5.21. Sample: 33 receiver-games, 253 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Roger McCreary | CB | 11 | 83.8 (89.0 wk12) | 63 | 37 | 469 | 4 | 1 | 7.44 | 96.6 | 10.0 | 2 | 13 | 1 | 15 | 32 (452) | MISSING |
| D.J. Reed | CB | 8 | 87.1 (39.0 wk12) | 36 | 20 | 327 | 2 | 1 | 9.08 | 93.2 | 14.0 | 2 | 6 | 2 | 9 | 25 (349) | MISSING |
| Rock Ya-Sin | CB | 9 | 69.2 (92.0 wk12) | 42 | 25 | 208 | 2 | 0 | 4.95 | 88.2 | 10.0 | 1 | 1 | 1 | 2 | 24 (187) | MISSING |
| Keith Abney | CB | 5 | 44.8 (11.0 wk9) | 9 | 4 | 42 | 0 | 1 | 4.67 | 19.0 | 15.2 | 0 | 1 | 0 | 2 | 5 (51) | MISSING |
| Ennis Rakestraw | CB | 7 | 28.6 (8.0 wk10) | 22 | 13 | 169 | 0 | 0 | 7.68 | 83.3 | 9.7 | 1 | 2 | 1 | 3 | 8 (121) | MISSING |
| Khalil Dorsey | CB | 6 | 23.7 (12.0 wk11) | 11 | 5 | 88 | 0 | 0 | 8.00 | 73.3 | 20.3 | 0 | 1 | 0 | 1 | 6 (78) | MISSING |
| Nick Whiteside | CB | 4 | 12.0 (15.0 wk12) | 1 | 1 | 7 | 0 | 0 | 7.00 | 95.8 | 5.0 | 0 | 0 | 1 | 1 | 1 (7) | MISSING |
| Brian Branch | DB | 6 | 84.3 (97.0 wk12) | 12 | 4 | 38 | 0 | 1 | 3.17 | 8.3 | 11.1 | 0 | 4 | 1 | 6 | 8 (73) | MISSING |
| Christian Izien | DB | 7 | 36.3 (5.0 wk12) | 19 | 14 | 115 | 2 | 0 | 6.05 | 123.8 | 7.7 | 0 | 0 | 0 | 0 | 10 (71) | MISSING |
| Avonte Maddox | DB | 2 | 65.0 (36.0 wk2) | 11 | 6 | 158 | 2 | 0 | 14.36 | 139.2 | 15.6 | 1 | 2 | 0 | 2 | 4 (74) | MISSING |
| Jalen Mills | DB | 2 | 17.5 (30.0 wk5) | 2 | 2 | 12 | 0 | 0 | 6.00 | 91.7 | 4.5 | 0 | 0 | 0 | 0 | 2 (12) | MISSING |
| Chuck Clark | S | 10 | 91.0 (100.0 wk11) | 39 | 15 | 188 | 0 | 2 | 4.82 | 32.9 | 10.2 | 0 | 2 | 0 | 4 | 26 (303) | MISSING |
| Kerby Joseph | S | 2 | 73.5 (80.0 wk12) | — | — | — | — | — | — | — | — | — | 1 | 1 | 2 | 3 (20) | MISSING |
| Thomas Harper | S | 2 | 52.5 (45.0 wk2) | 8 | 5 | 128 | 1 | 0 | 16.00 | 145.8 | 13.9 | 1 | 2 | 0 | 2 | 4 (87) | MISSING |
| Andre Cisco | S | 3 | 20.0 (45.0 wk12) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 3 (29) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jack Campbell | 7 | 41 | 30 | 335 | 4 | 8.17 | 129.6 | 0 |
| Derrick Barnes | 11 | 39 | 23 | 301 | 1 | 7.72 | 81.2 | 2 |
| Malcolm Rodriguez | 10 | 12 | 10 | 51 | 3 | 4.25 | 124.0 | 2 |
| Trevor Nowaske | 11 | 10 | 3 | 29 | 0 | 2.90 | 39.6 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | CHI | D.Barnes | PBU | D.Swift | short_left |
| 12 | CHI | R.McCreary | PBU | S.Carlson | short_middle |
| 12 | CHI | K.Joseph | PBU | J.Walker | deep_right |
| 12 | CHI | R.McCreary | PBU | K.Raymond | short_left |
| 12 | CHI | R.McCreary | PBU | L.Burden | short_right |
| 11 | TB | K.Joseph | DPI | B.Sharp | deep_right |
| 11 | TB | B.Branch | DPI | T.Hurst | deep_right |
| 11 | TB | B.Branch | PBU | B.Irving | short_middle |
| 11 | TB | D.Wonnum | PBU | T.Johnson | short_left |
| 11 | TB | M.Rodriguez | PBU | K.Gainwell | short_right |
| 11 | TB | B.Branch | PBU | E.Egbuka | short_right |
| 11 | TB | R.McCreary | PBU | T.Hurst | short_right |
| 11 | TB | C.Clark | PBU | T.Hurst | short_left |
| 10 | NE | E.O'Neill | PBU | D.Douglas | short_right |
| 10 | NE | N.Whiteside | DPI | K.Williams | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Roger McCreary | CB | 67.4 | 41.2 | 466.0 | 6.91 | 3.16 | 85 (46) |
| D.J. Reed | CB | 54.1 | 34.2 | 462.4 | 8.55 | 3.15 | 67 (43) |
| Rock Ya-Sin | CB | 40.4 | 27.7 | 276.3 | 6.84 | 2.51 | 56 (22) |
| Derrick Barnes | LB | 35.2 | 26.1 | 239.5 | 6.8 | 2.08 | 35 (11) |
| Jack Campbell | LB | 30.8 | 24.4 | 222.0 | 7.21 | 2.49 | 37 (21) |
| Chuck Clark | S | 27.4 | 20.5 | 194.7 | 7.11 | 2.22 | 35 (4) |
| Brian Branch | CB | 26.2 | 16.1 | 171.5 | 6.55 | 0.96 | 22 (5) |
| Malcolm Rodriguez | LB | 18.3 | 14.2 | 147.4 | 8.05 | 0.67 | 20 (5) |
| Christian Izien | CB | 13.6 | 10.1 | 95.8 | 7.04 | 0.51 | 13 (1) |
| Keith Abney II | CB | 13.1 | 8.1 | 93.4 | 7.13 | 0.56 | 5 (0) |
| Ennis Rakestraw Jr. | CB | 11.9 | 8.3 | 107.8 | 9.06 | 1.04 | 0 (0) |
| Trevor Nowaske | LB | 11.6 | 8.9 | 79.4 | 6.84 | 0.52 | 1 (0) |

### Upcoming: opposing receivers vs likely DET defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-06 | ATL | D.London (WR) | 17 | short_right 29%, short_left 27% | Roger McCreary (22%) | Brian Branch (22%) |
| 13 | 2026-12-06 | ATL | B.Robinson (RB) | 12 | short_left 51%, short_right 36% | Malcolm Rodriguez (23%) | Trevor Nowaske (18%) |
| 13 | 2026-12-06 | ATL | K.Pitts (TE) | 10 | short_right 40%, short_left 33% | Kerby Joseph (15%) | Rock Ya-Sin (13%) |
| 13 | 2026-12-06 | ATL | J.Dotson (WR) | 8 | short_left 29%, deep_left 18% | Roger McCreary (23%) | Brian Branch (22%) |

Defender pool = DET players with defensive snaps in their most recent game (2026_12_CHI_DET); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Chuck Clark | S | 67.9 | 46.5 | 524.1 | 7.72 | 7.53 | 202.4 | 6 |
| Roger McCreary | CB | 50.1 | 30.5 | 358.1 | 7.15 | 7.08 | 179.3 | 9 |
| D.J. Reed | CB | 42.4 | 28.0 | 377.8 | 8.91 | 6.09 | 185.3 | 7 |
| Derrick Barnes | LB | 48.2 | 36.8 | 320.4 | 6.65 | 2.96 | 85.6 | 3 |
| Brian Branch | S | 17.2 | 9.2 | 146.7 | 8.53 | 2.81 | 91.9 | 2 |
| Keith Abney II | CB | 23.1 | 14.6 | 145.9 | 6.32 | 2.13 | 53.9 | 2 |
| Jack Campbell | LB | 45.4 | 36.6 | 291.4 | 6.42 | 2.1 | 47.8 | 1 |
| Ennis Rakestraw Jr. | CB | 18.9 | 13.6 | 152.4 | 8.06 | 2.03 | 49.2 | 1 |
| Thomas Harper | S | 11.6 | 6.1 | 97.1 | 8.37 | 1.81 | 60.3 | 2 |
| Malcolm Rodriguez | LB | 23.5 | 18.0 | 183.5 | 7.81 | 0.75 | 23.1 | 1 |
| Rock Ya-Sin | CB | 22.0 | 14.0 | 115.8 | 5.26 | 0.69 | 19.0 | 1 |
| Khalil Dorsey | CB | 5.7 | 3.1 | 28.4 | 4.98 | 0.57 | 13.3 | 0 |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** D.J. Reed (CB) 36 tgt, 55.6% catch, 9.08 ypt, rating 93.2 [GIVES UP EXPLOSIVES]
**Best / lockdown:** Chuck Clark (S) 39 tgt, 38.5% catch, 4.82 ypt, rating 32.9 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS]
**Weak zones:** short middle 8.9 ypt; short right 6.5 ypt

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rock Ya-Sin | CB | 8 | 42 | 21% | 59.5 | 4.95 | 8.32 | 0.568 | 88.2 | 2 | 0 | 1 | 67.5 | LIMITS YARDS |  |
| Ennis Rakestraw | CB | 6 | 22 | 13% | 59.1 | 7.68 | 13.0 | 1.243 | 83.3 | 0 | 0 | 2 | 55.5 |  | small sample (<35 tgts) |
| Roger McCreary | CB | 10 | 63 | 23% | 58.7 | 7.44 | 12.68 | 0.842 | 96.6 | 4 | 1 | 10 | 35.5 |  |  |
| D.J. Reed | CB | 7 | 36 | 17% | 55.6 | 9.08 | 16.35 | 0.693 | 93.2 | 2 | 1 | 6 | 35.2 | GIVES UP EXPLOSIVES |  |
| Chuck Clark | S | 10 | 39 | 14% | 38.5 | 4.82 | 12.53 | 0.309 | 32.9 | 0 | 2 | 2 | 93.8 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS |  |
