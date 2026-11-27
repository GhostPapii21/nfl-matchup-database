# BUF defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 18.1 | 28.3 | — |
| Zone % | 74.9 | 71.4 | — |
| Single-high / MOFC % | 46.0 | 48.1 | — |
| Two-high / MOFO % | 49.6 | 51.9 | — |
| Blitz % | 29.2 | 37.5 | 35.1 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 41.3 / 29.9, 65.0 | — | — |

Sharp YPT allowed: WR 7.0, TE 6.7, RB 5.4, **outside 7.4 vs slot 7.6** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #15 vs StatRankings #22; blitz rank Sharp #14 vs SR #8 (raw gaps: man -10.2 pts, blitz -8.3 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.1 | 136.4 | 6.79 | 11 | 0.071 | 24 |
| TE | 8.5 | 59.6 | 6.98 | 1 | 0.072 | 9 |
| RB | 7.2 | 38.8 | 5.41 | 3 | 0.023 | 8 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 29 | 12 | 294 | 0 | 0 | 10.14 | 11.46 | 20 |  |
| deep middle | 22 | 8 | 210 | 2 | 2 | 9.55 | 14.39 | 29 |  |
| deep right | 33 | 12 | 283 | 1 | 2 | 8.58 | 12.14 | 28 |  |
| short left | 111 | 68 | 602 | 4 | 2 | 5.42 | 5.99 | 26 |  |
| short middle | 69 | 47 | 467 | 4 | 2 | 6.77 | 7.32 | 25 |  |
| short right | 130 | 88 | 727 | 4 | 0 | 5.59 | 6.02 | 26 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs BUF: **2.81 yds** (league 2.93; rank 24/32 most allowed). WR 2.65, TE 3.17, cushion 5.56. Sample: 25 receiver-games, 193 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Davison Igbinosun | CB | 11 | 69.2 (100.0 wk12) | 52 | 23 | 275 | 2 | 2 | 5.29 | 57.8 | 12.6 | 1 | 12 | 3 | 17 | 21 (246) | MISSING |
| Christian Benford | CB | 8 | 85.6 (75.0 wk10) | 49 | 26 | 302 | 3 | 0 | 6.16 | 92.4 | 10.4 | 1 | 8 | 2 | 10 | 23 (270) | MISSING |
| Maxwell Hairston | CB | 11 | 63.5 (98.0 wk12) | 34 | 16 | 197 | 2 | 0 | 5.79 | 85.0 | 10.2 | 0 | 3 | 0 | 3 | 14 (155) | MISSING |
| Dee Alford | CB | 9 | 50.1 (57.0 wk12) | 30 | 16 | 207 | 1 | 1 | 6.90 | 72.5 | 8.2 | 1 | 4 | 1 | 6 | 7 (59) | MISSING |
| Anthony Kendall | CB | 1 | 38.0 (38.0 wk5) | 2 | 2 | 8 | 0 | 0 | 4.00 | 83.3 | -4.0 | 0 | 0 | 0 | 0 | 1 (3) | MISSING |
| Tre'Davious White | CB | 1 | 42.0 (42.0 wk11) | 2 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 19.5 | 0 | 1 | 0 | 1 | 0 (0) | MISSING |
| Jordan Hancock | DB | 4 | 36.8 (32.0 wk12) | 12 | 6 | 85 | 0 | 0 | 7.08 | 73.3 | 7.8 | 0 | 1 | 0 | 1 | 10 (137) | MISSING |
| Te'Cory Couch | DB | 1 | 71.0 (71.0 wk8) | 2 | 2 | 9 | 0 | 0 | 4.50 | 85.4 | -3.0 | 0 | 0 | 0 | 0 | 2 (7) | MISSING |
| Sam Franklin | DB | 2 | 11.5 (21.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Cole Bishop | S | 11 | 96.0 (100.0 wk12) | 43 | 24 | 279 | 1 | 0 | 6.49 | 83.4 | 8.2 | 1 | 3 | 1 | 4 | 31 (376) | MISSING |
| C.J. Gardner-Johnson | S | 6 | 89.3 (42.0 wk6) | 21 | 13 | 218 | 1 | 1 | 10.38 | 93.0 | 10.4 | 0 | 1 | 0 | 2 | 15 (250) | MISSING |
| Damar Hamlin | S | 11 | 41.3 (17.0 wk12) | 18 | 11 | 204 | 0 | 1 | 11.33 | 77.1 | 12.3 | 0 | 1 | 0 | 2 | 13 (192) | MISSING |
| Amani Hooker | S | 3 | 93.7 (100.0 wk12) | 8 | 4 | 45 | 0 | 0 | 5.62 | 67.2 | 6.9 | 0 | 3 | 0 | 3 | 5 (74) | MISSING |
| Geno Stone | S | 2 | 44.5 (52.0 wk9) | 3 | 3 | 9 | 0 | 0 | 3.00 | 79.2 | 0.7 | 0 | 0 | 0 | 0 | 2 (7) | MISSING |
| Jalon Kilgore | S | 2 | 18.0 (19.0 wk11) | 4 | 2 | 61 | 1 | 0 | 15.25 | 135.4 | 19.5 | 0 | 0 | 0 | 0 | 2 (24) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Terrel Bernard | 11 | 43 | 28 | 224 | 1 | 5.21 | 76.1 | 2 |
| Dorian Williams | 10 | 23 | 16 | 148 | 2 | 6.43 | 79.6 | 2 |
| Kaleb Elarms-Orr | 11 | 15 | 10 | 121 | 0 | 8.07 | 91.2 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | KC | A.Hooker | PBU | R.Rice | short_middle |
| 12 | KC | D.Igbinosun | PBU | R.Rice | short_left |
| 12 | KC | D.Walker | PBU | T.Kelce | deep_middle |
| 11 | MIA | S.Thompson | PBU | C.Douglas | deep_middle |
| 11 | MIA | T.White | PBU | K.Coleman | deep_left |
| 11 | MIA | J.Hancock | PBU | G.Dulcich | short_right |
| 11 | MIA | D.Alford | PBU | M.Washington | short_left |
| 11 | MIA | A.Hooker | PBU | G.Dulcich | short_right |
| 11 | MIA | D.Igbinosun | DPI | C.Douglas | short_right |
| 11 | MIA | C.Bishop | PBU | G.Dulcich | short_left |
| 11 | MIA | M.Hairston | PBU | C.Douglas | short_left |
| 11 | MIA | D.Hamlin | INT | C.Bell | deep_middle |
| 11 | MIA | D.Walker | PBU | M.Washington | short_right |
| 11 | MIA | D.Igbinosun | PBU | C.Douglas | short_right |
| 11 | MIA | D.Igbinosun | PBU | C.Douglas | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Davison Igbinosun | CB | 53.6 | 27.7 | 339.4 | 6.33 | 1.8 | 78 (22) |
| Christian Benford | CB | 53.4 | 32.4 | 381.1 | 7.14 | 2.71 | 96 (48) |
| Terrel Bernard | LB | 38.6 | 25.3 | 251.3 | 6.51 | 1.34 | 58 (13) |
| Maxwell Hairston | CB | 36.9 | 19.4 | 240.6 | 6.52 | 1.67 | 35 (20) |
| Cole Bishop | S | 33.3 | 21.1 | 258.1 | 7.75 | 1.14 | 45 (10) |
| Greg Rousseau | LB | 24.7 | 16.4 | 141.6 | 5.73 | 1.17 | 17 (2) |
| Dee Alford | CB | 22.0 | 11.6 | 138.9 | 6.31 | 0.81 | 6 (0) |
| Dorian Williams | LB | 21.7 | 14.9 | 144.4 | 6.65 | 1.07 | 11 (0) |
| Bradley Chubb | LB | 21.1 | 14.3 | 127.1 | 6.02 | 0.71 | 16 (0) |
| C.J. Gardner-Johnson | S | 15.8 | 10.1 | 138.1 | 8.74 | 0.98 | 8 (2) |
| Damar Hamlin | S | 12.4 | 6.3 | 81.4 | 6.56 | 0.27 | 1 (0) |
| TJ Parker | LB | 11.2 | 7.4 | 65.7 | 5.87 | 0.26 | 0 (0) |

### Upcoming: opposing receivers vs likely BUF defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-06 | NE | M.Hollins (WR) | 12 | short_right 34%, deep_right 25% | Davison Igbinosun (26%) | Maxwell Hairston (24%) |
| 13 | 2026-12-06 | NE | D.Douglas (WR) | 12 | short_right 35%, short_left 22% | Davison Igbinosun (25%) | Maxwell Hairston (21%) |
| 13 | 2026-12-06 | NE | E.Raridon (TE) | 7 | short_left 37%, short_middle 26% | Cole Bishop (15%) | Amani Hooker (13%) |
| 13 | 2026-12-06 | NE | H.Henry (TE) | 6 | short_right 40%, short_left 25% | Cole Bishop (15%) | Amani Hooker (14%) |

Defender pool = BUF players with defensive snaps in their most recent game (2026_12_KC_BUF); check inactives before use.
