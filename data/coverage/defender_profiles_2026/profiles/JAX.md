# JAX defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 17.2 | 24.9 | — |
| Zone % | 76.9 | 75.1 | — |
| Single-high / MOFC % | 44.3 | 46.5 | — |
| Two-high / MOFO % | 52.8 | 53.5 | — |
| Blitz % | 28.8 | 33.4 | 31.6 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 45.0 / 22.4, 70.0 | — | — |

Sharp YPT allowed: WR 8.3, TE 5.4, RB 5.2, **outside 9.1 vs slot 8.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #18 vs StatRankings #25; blitz rank Sharp #15 vs SR #14 (raw gaps: man -7.7 pts, blitz -4.6 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.5 | 162.2 | 8.32 | 5 | 0.066 | 9 |
| TE | 6.3 | 34.3 | 5.44 | 5 | -0.121 | 32 |
| RB | 6.6 | 34.6 | 5.24 | 1 | -0.14 | 15 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 22 | 9 | 227 | 0 | 1 | 10.32 | 11.46 | 19 |  |
| deep middle | 11 | 5 | 183 | 1 | 0 | 16.64 | 14.39 | 8 |  |
| deep right | 26 | 11 | 327 | 1 | 0 | 12.58 | 12.14 | 15 |  |
| short left | 107 | 78 | 590 | 3 | 6 | 5.51 | 5.99 | 22 |  |
| short middle | 52 | 36 | 385 | 1 | 2 | 7.4 | 7.32 | 13 |  |
| short right | 106 | 79 | 599 | 5 | 3 | 5.65 | 6.02 | 23 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs JAX: **3.05 yds** (league 2.93; rank 9/32 most allowed). WR 3.13, TE 2.68, cushion 6.11. Sample: 21 receiver-games, 162 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jarrian Jones | CB | 9 | 71.2 (61.0 wk10) | 54 | 29 | 395 | 0 | 1 | 7.31 | 69.6 | 12.7 | 2 | 7 | 2 | 10 | 21 (230) | MISSING |
| Jourdan Lewis | CB | 10 | 58.1 (63.0 wk11) | 35 | 18 | 162 | 2 | 3 | 4.63 | 47.6 | 6.9 | 0 | 0 | 1 | 4 | 17 (193) | MISSING |
| Montaric Brown | CB | 8 | 68.1 (94.0 wk11) | 32 | 20 | 304 | 2 | 1 | 9.50 | 101.6 | 11.2 | 1 | 3 | 1 | 5 | 18 (178) | MISSING |
| Jaylon Jones | CB | 2 | 19.0 (18.0 wk9) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Christian Braswell | CB | 2 | 13.0 (14.0 wk3) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Jabbar Muhammad | CB | 1 | 3.0 (3.0 wk4) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Antonio Johnson | S | 9 | 88.4 (100.0 wk11) | 32 | 17 | 173 | 1 | 0 | 5.41 | 79.3 | 11.4 | 0 | 3 | 0 | 3 | 18 (205) | MISSING |
| Rayuan Lane | S | 7 | 61.9 (98.0 wk10) | 18 | 11 | 138 | 1 | 1 | 7.67 | 80.3 | 9.0 | 1 | 3 | 0 | 4 | 11 (159) | MISSING |
| Eric Murray | S | 5 | 80.6 (98.0 wk6) | 7 | 5 | 56 | 2 | 0 | 8.00 | 134.5 | 6.6 | 0 | 0 | 0 | 0 | 7 (91) | MISSING |
| Kaevon Merriweather | S | 6 | 46.8 (29.0 wk11) | 5 | 4 | 71 | 0 | 0 | 14.20 | 118.8 | 6.8 | 0 | 1 | 0 | 1 | 3 (69) | MISSING |
| Jessie Bates III | S | 1 | 94.0 (94.0 wk11) | 4 | 2 | 34 | 0 | 0 | 8.50 | 79.2 | 15.3 | 0 | 0 | 0 | 0 | 3 (48) | MISSING |
| Caleb Ransaw | S | 3 | 35.3 (30.0 wk3) | 2 | 0 | 21 | 0 | 0 | 10.50 | 70.8 | 4.0 | 0 | 0 | 0 | 0 | 3 (49) | MISSING |
| Jalen Huskey | S | 2 | 24.0 (18.0 wk9) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Foyesade Oluokun | 10 | 50 | 41 | 333 | 2 | 6.66 | 91.1 | 1 |
| Ventrell Miller | 10 | 34 | 22 | 163 | 0 | 4.79 | 76.0 | 4 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | NYG | T.Walker | PBU | M.Nabers | short_middle |
| 11 | NYG | K.Merriweather | PBU | C.Skattebo | short_left |
| 11 | NYG | A.Armstead | PBU | D.Mooney | deep_middle |
| 11 | NYG | J.Hines-Allen | PBU | C.Skattebo | short_left |
| 11 | NYG | M.Brown | PBU | J.Hyatt | deep_left |
| 11 | NYG | T.Walker | PBU | M.Nabers | short_right |
| 11 | NYG | A.Johnson | PBU | M.Fields | deep_left |
| 11 | NYG | A.Johnson | PBU | I.Likely | short_middle |
| 11 | NYG | M.Brown | DPI | M.Fields | deep_left |
| 11 | NYG | F.Oluokun | PBU | C.Skattebo | short_left |
| 10 | TEN | Jar.Jones | PBU | E.Ayomanor | short_right |
| 10 | TEN | D.Gardeck | PBU | W.Robinson | deep_middle |
| 10 | TEN | T.Hunter | INT | E.Ayomanor | short_left |
| 10 | TEN | T.Walker | PBU | D.Bellinger | short_right |
| 10 | TEN | M.Dickerson | PBU | E.Ayomanor | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Jarrian Jones | CB | 58.8 | 39.1 | 503.8 | 8.57 | 1.96 | 80 (62) |
| Jourdan Lewis | CB | 46.1 | 30.2 | 352.5 | 7.65 | 1.28 | 24 (15) |
| Foyesade Oluokun | LB | 44.2 | 32.8 | 252.2 | 5.71 | 1.36 | 62 (40) |
| Montaric Brown | CB | 43.6 | 28.6 | 306.7 | 7.03 | 1.33 | 76 (43) |
| Ventrell Miller | LB | 31.0 | 22.8 | 187.9 | 6.06 | 1.05 | 22 (8) |
| Antonio Johnson | S | 26.7 | 16.5 | 197.4 | 7.39 | 1.1 | 11 (1) |
| Rayuan Lane III | S | 17.4 | 10.7 | 102.6 | 5.9 | 0.57 | 28 (0) |
| Dennis Gardeck | LB | 16.7 | 10.9 | 105.5 | 6.32 | 0.6 | 0 (0) |
| Eric Murray | S | 11.5 | 8.3 | 111.1 | 9.66 | 0.82 | 9 (0) |
| Kaevon Merriweather | S | 8.1 | 5.2 | 47.7 | 5.89 | 0.44 | 3 (0) |
| Branson Combs | LB | 5.5 | 4.0 | 39.1 | 7.11 | 0.14 | 0 (0) |

### Upcoming: opposing receivers vs likely JAX defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | TEN | E.Ayomanor (WR) | 13 | short_left 33%, short_right 33% | Montaric Brown (35%) | Jourdan Lewis (25%) |
| 12 | 2026-11-29 | TEN | T.Pollard (RB) | 10 | short_left 35%, short_right 32% | Foyesade Oluokun (33%) | Ventrell Miller (25%) |
| 12 | 2026-11-29 | TEN | C.Dike (WR) | 10 | short_left 39%, short_right 30% | Montaric Brown (36%) | Jourdan Lewis (26%) |
| 12 | 2026-11-29 | TEN | G.Helm (TE) | 7 | short_left 52%, short_middle 24% | Antonio Johnson (19%) | Jessie Bates (18%) |
| 13 | 2026-12-06 | CHI | R.Odunze (WR) | 20 | short_right 25%, short_middle 20% | Montaric Brown (30%) | Jourdan Lewis (23%) |
| 13 | 2026-12-06 | CHI | L.Burden (WR) | 20 | short_middle 26%, short_left 26% | Montaric Brown (31%) | Jourdan Lewis (23%) |
| 13 | 2026-12-06 | CHI | K.Raymond (WR) | 16 | short_right 38%, short_middle 24% | Montaric Brown (32%) | Jourdan Lewis (24%) |
| 13 | 2026-12-06 | CHI | D.Swift (RB) | 11 | short_right 54%, short_left 36% | Foyesade Oluokun (31%) | Ventrell Miller (26%) |

Defender pool = JAX players with defensive snaps in their most recent game (2026_11_JAX_NYG); check inactives before use.
