# SF defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 10.3 | 26.5 | — |
| Zone % | 84.0 | 72.4 | — |
| Single-high / MOFC % | 54.3 | 57.7 | — |
| Two-high / MOFO % | 41.7 | 42.3 | — |
| Blitz % | 26.9 | 31.6 | 28.8 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 49.4 / 21.9, 64.0 | — | — |

Sharp YPT allowed: WR 7.1, TE 6.8, RB 5.4, **outside 7.4 vs slot 7.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #28 vs StatRankings #23; blitz rank Sharp #18 vs SR #16 (raw gaps: man -16.2 pts, blitz -4.7 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.7 | 146.1 | 7.06 | 11 | 0.106 | 18 |
| TE | 8.1 | 55.1 | 6.8 | 3 | 0.035 | 12 |
| RB | 6.8 | 36.9 | 5.43 | 2 | 0.054 | 11 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 24 | 9 | 219 | 1 | 1 | 9.12 | 11.46 | 23 |  |
| deep middle | 15 | 8 | 164 | 1 | 1 | 10.93 | 14.39 | 26 |  |
| deep right | 33 | 11 | 358 | 2 | 3 | 10.85 | 12.14 | 20 |  |
| short left | 125 | 108 | 812 | 8 | 0 | 6.5 | 5.99 | 9 |  |
| short middle | 39 | 22 | 216 | 0 | 1 | 5.54 | 7.32 | 32 |  |
| short right | 119 | 89 | 612 | 4 | 1 | 5.14 | 6.02 | 29 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs SF: **2.98 yds** (league 2.93; rank 14/32 most allowed). WR 2.82, TE 3.46, cushion 7.18. Sample: 23 receiver-games, 191 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Renardo Green | CB | 10 | 92.7 (90.0 wk11) | 53 | 36 | 365 | 2 | 4 | 6.89 | 68.5 | 11.2 | 1 | 3 | 1 | 8 | 32 (255) | MISSING |
| Upton Stout | CB | 9 | 60.8 (64.0 wk11) | 38 | 28 | 372 | 3 | 0 | 9.79 | 130.6 | 6.7 | 2 | 2 | 0 | 2 | 14 (163) | MISSING |
| Jack Jones | CB | 7 | 18.9 (34.0 wk7) | 21 | 12 | 126 | 2 | 0 | 6.00 | 106.4 | 10.8 | 0 | 3 | 1 | 4 | 7 (85) | MISSING |
| Ephesians Prysock | CB | 4 | 18.0 (19.0 wk11) | 10 | 7 | 49 | 1 | 0 | 4.90 | 114.2 | 9.5 | 0 | 1 | 1 | 2 | 6 (54) | MISSING |
| Deommodore Lenoir | DB | 10 | 94.2 (81.0 wk11) | 59 | 37 | 385 | 5 | 0 | 6.53 | 109.8 | 12.2 | 1 | 7 | 2 | 9 | 25 (225) | MISSING |
| Siran Neal | DB | 2 | 12.0 (10.0 wk11) | 3 | 2 | 13 | 0 | 0 | 4.33 | 75.7 | 10.0 | 0 | 0 | 0 | 0 | 1 (8) | MISSING |
| Ji'Ayir Brown | S | 10 | 87.5 (61.0 wk11) | 29 | 19 | 220 | 1 | 1 | 7.59 | 85.4 | 9.5 | 0 | 3 | 0 | 4 | 20 (240) | MISSING |
| Malik Mustapha | S | 10 | 60.0 (73.0 wk11) | 29 | 11 | 169 | 1 | 2 | 5.83 | 40.7 | 15.4 | 0 | 4 | 0 | 6 | 19 (248) | MISSING |
| Marques Sigle | S | 7 | 75.9 (70.0 wk11) | 12 | 4 | 51 | 0 | 0 | 4.25 | 47.6 | 7.8 | 0 | 2 | 0 | 2 | 10 (175) | MISSING |
| Ashtyn Davis | S | 2 | 15.5 (10.0 wk7) | 4 | 3 | 38 | 0 | 0 | 9.50 | 104.2 | 9.5 | 0 | 0 | 0 | 0 | 2 (36) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Fred Warner | 10 | 39 | 28 | 254 | 0 | 6.51 | 89.0 | 4 |
| Dre Greenlaw | 8 | 35 | 26 | 151 | 0 | 4.31 | 82.0 | 0 |
| Jaden Dugger | 10 | 24 | 21 | 129 | 1 | 5.38 | 85.6 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | MIN | M.Sigle | PBU | T.Felton | short_left |
| 11 | MIN | J.Brown | INT | T.Felton | short_middle |
| 11 | MIN | D.Lenoir | PBU | J.Jennings | deep_right |
| 11 | MIN | D.Lenoir | PBU | J.Jennings | short_middle |
| 11 | MIN | F.Warner | PBU | T.Felton | short_middle |
| 10 | DAL | E.Prysock | DPI | R.Flournoy | short_middle |
| 10 | DAL | M.Mustapha | PBU | K.Turpin | deep_right |
| 10 | DAL | M.Mustapha | INT | C.Lamb | deep_right |
| 10 | DAL | J.Brown | PBU | G.Pickens | short_right |
| 10 | DAL | D.Lenoir | PBU | G.Pickens | deep_right |
| 10 | DAL | D.Lenoir | PBU | G.Pickens | deep_middle |
| 10 | DAL | M.Sigle | PBU | C.Lamb | short_middle |
| 10 | DAL | D.Lenoir | PBU | G.Pickens | short_right |
| 10 | DAL | D.Lenoir | PBU | C.Lamb | short_right |
| 10 | DAL | R.Green | PBU | G.Pickens | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Renardo Green | CB | 71.4 | 49.6 | 502.3 | 7.04 | 3.74 | 110 (64) |
| Deommodore Lenoir | CB | 69.7 | 43.3 | 504.0 | 7.23 | 4.15 | 76 (43) |
| Fred Warner | LB | 42.6 | 33.3 | 243.0 | 5.7 | 1.32 | 46 (15) |
| Dre Greenlaw | LB | 31.7 | 25.8 | 161.0 | 5.08 | 0.88 | 49 (28) |
| Upton Stout | CB | 31.6 | 21.4 | 223.3 | 7.07 | 1.46 | 6 (0) |
| Ji'Ayir Brown | S | 26.9 | 18.3 | 181.2 | 6.74 | 1.08 | 21 (1) |
| Malik Mustapha | S | 22.1 | 14.2 | 171.8 | 7.77 | 1.4 | 17 (3) |
| Jaden Dugger | LB | 17.8 | 14.1 | 116.7 | 6.56 | 0.56 | 12 (3) |
| Marques Sigle | S | 15.4 | 9.7 | 106.4 | 6.91 | 0.33 | 4 (0) |
| Jack Jones | CB | 10.2 | 5.9 | 70.1 | 6.87 | 0.54 | 9 (0) |
| Garret Wallow | LB | 6.0 | 4.7 | 35.8 | 5.97 | 0.05 | 2 (1) |
| Ephesians Prysock | CB | 5.8 | 3.8 | 40.6 | 7.0 | 0.36 | 3 (0) |

### Upcoming: opposing receivers vs likely SF defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | SEA | J.Smith-Njigba (WR) | 20 | short_right 31%, short_left 25% | Deommodore Lenoir (22%) | Renardo Green (21%) |
| 12 | 2026-11-29 | SEA | A.Barner (TE) | 7 | short_right 49%, short_left 29% | Fred Warner (14%) | Ji'Ayir Brown (13%) |
| 12 | 2026-11-29 | SEA | C.Kupp (WR) | 5 | short_left 31%, short_right 29% | Renardo Green (22%) | Deommodore Lenoir (21%) |
| 12 | 2026-11-29 | SEA | J.Price (RB) | 5 | short_right 38%, short_left 38% | Fred Warner (27%) | Garret Wallow (22%) |
| 13 | 2026-12-06 | NYG | M.Nabers (WR) | 27 | short_right 31%, short_left 28% | Renardo Green (23%) | Deommodore Lenoir (22%) |
| 13 | 2026-12-06 | NYG | I.Likely (TE) | 20 | short_middle 33%, short_left 30% | Malik Mustapha (14%) | Marques Sigle (14%) |
| 13 | 2026-12-06 | NYG | D.Mooney (WR) | 14 | short_left 33%, short_middle 17% | Renardo Green (23%) | Deommodore Lenoir (23%) |
| 13 | 2026-12-06 | NYG | M.Fields (WR) | 14 | short_left 23%, short_middle 23% | Deommodore Lenoir (23%) | Renardo Green (21%) |

Defender pool = SF players with defensive snaps in their most recent game (2026_11_MIN_SF); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Ji'Ayir Brown | S | 59.3 | 40.4 | 429.7 | 7.25 | 5.55 | 167.7 | 5 |
| Deommodore Lenoir | CB | 38.4 | 23.2 | 319.8 | 8.33 | 5.11 | 177.6 | 6 |
| Upton Stout | CB | 59.3 | 38.7 | 395.0 | 6.66 | 4.99 | 139.7 | 5 |
| Renardo Green | CB | 49.7 | 33.4 | 355.6 | 7.15 | 4.18 | 115.4 | 8 |
| Malik Mustapha | S | 13.4 | 6.4 | 106.4 | 7.94 | 2.7 | 75.5 | 2 |
| Fred Warner | LB | 73.8 | 57.9 | 438.0 | 5.93 | 2.56 | 64.0 | 1 |
| Marques Sigle | S | 11.1 | 6.0 | 57.0 | 5.14 | 0.95 | 22.4 | 0 |
| Dre Greenlaw | LB | 34.3 | 27.7 | 186.2 | 5.43 | 0.73 | 20.3 | 0 |
| Jaden Dugger | LB | 10.3 | 8.7 | 59.5 | 5.78 | 0.17 | 3.7 | 0 |
| Garret Wallow | LB | 5.5 | 4.8 | 33.9 | 6.16 | 0.07 | 1.6 | 0 |

### Rest of Week 12: receivers vs likely SF window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | SEA | J.Smith-Njigba (WR) | 20 | 17% | Upton Stout (30%, 4.99) | Fred Warner (15%, 2.56) |
| 2026-11-29 | SEA | A.Barner (TE) | 7 | 0% | Marques Sigle (38%, 0.95) | Fred Warner (27%, 2.56) |
| 2026-11-29 | SEA | C.Kupp (WR) | 5 | 6% | Upton Stout (31%, 4.99) | Fred Warner (17%, 2.56) |
| 2026-11-29 | SEA | J.Price (RB) | 5 | 12% | Fred Warner (52%, 2.56) | Garret Wallow (17%, 0.07) |
