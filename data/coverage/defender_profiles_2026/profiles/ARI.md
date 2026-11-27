# ARI defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 9.8 | 26.4 | — |
| Zone % | 81.9 | 73.3 | — |
| Single-high / MOFC % | 33.5 | 42.4 | — |
| Two-high / MOFO % | 60.1 | 57.6 | — |
| Blitz % | 29.3 | 35.3 | 33.6 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 30.7 / 35.8, 48.0 | — | — |

Sharp YPT allowed: WR 9.5, TE 7.5, RB 6.6, **outside 10.3 vs slot 9.4** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #30 vs StatRankings #24; blitz rank Sharp #13 vs SR #12 (raw gaps: man -16.6 pts, blitz -6.0 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 16.1 | 145.6 | 9.05 | 13 | 0.449 | 19 |
| TE | 7.3 | 54.4 | 7.48 | 10 | 0.348 | 14 |
| RB | 5.1 | 33.5 | 6.59 | 2 | 0.139 | 17 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 20 | 9 | 257 | 0 | 0 | 12.85 | 11.46 | 14 |  |
| deep middle | 11 | 6 | 125 | 2 | 0 | 11.36 | 14.39 | 24 |  |
| deep right | 25 | 9 | 355 | 4 | 2 | 14.2 | 12.14 | 9 |  |
| short left | 92 | 66 | 699 | 4 | 0 | 7.6 | 5.99 | 2 | **WEAK** |
| short middle | 66 | 45 | 475 | 8 | 2 | 7.2 | 7.32 | 19 |  |
| short right | 99 | 76 | 658 | 7 | 0 | 6.65 | 6.02 | 5 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs ARI: **2.99 yds** (league 2.93; rank 12/32 most allowed). WR 2.69, TE 3.68, cushion 6.05. Sample: 21 receiver-games, 150 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Denzel Burke | CB | 11 | 88.1 (100.0 wk11) | 46 | 25 | 305 | 4 | 1 | 6.63 | 94.9 | 11.5 | 1 | 8 | 5 | 14 | 19 (237) | MISSING |
| Kei'Trel Clark | CB | 11 | 49.3 (100.0 wk11) | 30 | 16 | 187 | 0 | 0 | 6.23 | 72.5 | 12.9 | 1 | 3 | 1 | 4 | 10 (109) | MISSING |
| Max Melton | CB | 9 | 61.1 (30.0 wk10) | 37 | 21 | 260 | 2 | 0 | 7.03 | 96.7 | 11.2 | 0 | 6 | 2 | 8 | 19 (214) | MISSING |
| Kalen King | CB | 8 | 35.1 (47.0 wk11) | 21 | 16 | 205 | 1 | 0 | 9.76 | 122.1 | 6.5 | 1 | 2 | 0 | 2 | 10 (140) | MISSING |
| Garrett Williams | CB | 8 | 35.4 (14.0 wk11) | 15 | 9 | 142 | 1 | 0 | 9.47 | 113.8 | 8.5 | 1 | 1 | 0 | 1 | 8 (98) | MISSING |
| Will Johnson | CB | 2 | 89.5 (83.0 wk2) | 14 | 7 | 105 | 1 | 0 | 7.50 | 98.8 | 13.2 | 1 | 1 | 0 | 1 | 4 (55) | MISSING |
| Budda Baker | S | 11 | 98.3 (96.0 wk11) | 40 | 21 | 335 | 5 | 1 | 8.38 | 109.9 | 9.8 | 1 | 3 | 0 | 4 | 24 (304) | MISSING |
| Andrew Wingard | S | 7 | 86.3 (100.0 wk10) | 13 | 10 | 156 | 1 | 1 | 12.00 | 109.8 | 11.2 | 0 | 1 | 0 | 2 | 16 (230) | MISSING |
| Wydett Williams | S | 5 | 51.2 (100.0 wk11) | 10 | 4 | 97 | 1 | 0 | 9.70 | 109.2 | 18.9 | 1 | 1 | 0 | 1 | 2 (51) | MISSING |
| Dadrion Taylor-Demerson | S | 5 | 32.0 (4.0 wk11) | 3 | 2 | 56 | 0 | 0 | 18.67 | 109.7 | 20.7 | 0 | 0 | 0 | 0 | 1 (18) | MISSING |
| Kitan Crawford | S | 5 | 8.0 (3.0 wk10) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 1 (11) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Mack Wilson | 11 | 39 | 26 | 345 | 3 | 8.85 | 120.1 | 2 |
| Jack Gibbens | 11 | 37 | 23 | 233 | 2 | 6.30 | 98.1 | 1 |
| Baron Browning | 11 | 10 | 5 | 93 | 2 | 9.30 | 122.1 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | KC | D.Burke | PBU | A.Armstrong | short_right |
| 11 | KC | R.Lopez | PBU | N.Gray | short_middle |
| 10 | LA | A.Wingard | PBU | T.Atwell | deep_middle |
| 10 | LA | C.Simon | INT | K.Mumpfield | short_middle |
| 9 | SEA | Ma.Wilson | PBU | A.Barner | short_middle |
| 9 | SEA | D.Burke | PBU | E.Saubert | short_right |
| 9 | SEA | D.Burke | DPI | T.Horton | deep_middle |
| 9 | SEA | M.Melton | PBU | J.Smith-Njigba | short_right |
| 9 | SEA | M.Melton | DPI | J.Smith-Njigba | deep_right |
| 9 | SEA | M.Melton | PBU | T.Horton | short_right |
| 9 | SEA | K.King | PBU | J.Smith-Njigba | deep_middle |
| 8 | DAL | L.Collier | PBU | C.Lamb | short_middle |
| 8 | DAL | D.Stills | PBU | B.Spann-Ford | short_middle |
| 8 | DAL | L.Collier | PBU | C.Lamb | short_middle |
| 8 | DAL | D.Burke | DPI | R.Flournoy | deep_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Denzel Burke | CB | 48.5 | 30.0 | 433.9 | 8.95 | 4.48 | 58 (12) |
| Mack Wilson | LB | 31.3 | 22.8 | 243.9 | 7.79 | 2.27 | 43 (1) |
| Budda Baker | S | 30.9 | 20.0 | 264.5 | 8.56 | 3.7 | 56 (8) |
| Max Melton | CB | 29.6 | 19.6 | 252.3 | 8.52 | 2.15 | 36 (10) |
| Kei'Trel Clark | CB | 28.2 | 18.2 | 257.6 | 9.13 | 1.57 | 38 (14) |
| Jack Gibbens | LB | 24.3 | 17.6 | 168.0 | 6.91 | 1.72 | 29 (0) |
| Josh Sweat | LB | 15.6 | 10.9 | 110.8 | 7.1 | 1.2 | 6 (0) |
| Andrew Wingard | S | 15.0 | 10.5 | 133.6 | 8.91 | 1.9 | 20 (5) |
| Kalen King | CB | 13.8 | 9.5 | 114.5 | 8.3 | 0.5 | 3 (0) |
| Zaven Collins | LB | 13.3 | 9.4 | 93.0 | 6.99 | 0.99 | 0 (0) |
| Baron Browning | LB | 13.3 | 9.4 | 92.9 | 6.98 | 1.1 | 0 (0) |
| Garrett Williams | CB | 12.5 | 8.2 | 98.4 | 7.87 | 0.92 | 5 (0) |

### Upcoming: opposing receivers vs likely ARI defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | WAS | S.Diggs (WR) | 21 | short_right 32%, short_left 31% | Kei'Trel Clark (24%) | Denzel Burke (24%) |
| 12 | 2026-11-29 | WAS | C.Okonkwo (TE) | 20 | short_right 36%, short_left 27% | Wydett Williams Jr. (16%) | Budda Baker (14%) |
| 12 | 2026-11-29 | WAS | A.Williams (WR) | 19 | short_right 31%, short_left 27% | Denzel Burke (24%) | Kei'Trel Clark (22%) |
| 12 | 2026-11-29 | WAS | A.Ekeler (RB) | 10 | short_middle 40%, short_right 33% | Mack Wilson (21%) | Jack Gibbens (16%) |
| 13 | 2026-12-06 | PHI | D.Smith (WR) | 26 | short_right 31%, short_left 30% | Kei'Trel Clark (28%) | Denzel Burke (25%) |
| 13 | 2026-12-06 | PHI | M.Lemon (WR) | 18 | short_left 41%, short_right 29% | Kei'Trel Clark (24%) | Denzel Burke (22%) |
| 13 | 2026-12-06 | PHI | D.Cooper (WR) | 15 | short_middle 31%, short_left 26% | Kei'Trel Clark (22%) | Denzel Burke (21%) |
| 13 | 2026-12-06 | PHI | D.Goedert (TE) | 9 | short_right 36%, short_left 32% | Wydett Williams Jr. (15%) | Budda Baker (13%) |

Defender pool = ARI players with defensive snaps in their most recent game (2026_11_ARI_KC); check inactives before use.
