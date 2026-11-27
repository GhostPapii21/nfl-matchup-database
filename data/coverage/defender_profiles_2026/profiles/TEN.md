# TEN defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 17.3 | 29.2 | — |
| Zone % | 74.5 | 70.0 | — |
| Single-high / MOFC % | 48.4 | 46.5 | — |
| Two-high / MOFO % | 46.8 | 53.5 | — |
| Blitz % | 25.4 | 26.6 | 25.6 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 43.2 / 25.4, 71.0 | — | — |

Sharp YPT allowed: WR 9.9, TE 6.2, RB 7.0, **outside 9.4 vs slot 12.3** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #17 vs StatRankings #21; blitz rank Sharp #21 vs SR #23 (raw gaps: man -11.9 pts, blitz -1.2 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 21.2 | 210.2 | 9.92 | 11 | 0.452 | 1 |
| TE | 6.7 | 42.3 | 6.31 | 6 | 0.094 | 29 |
| RB | 4.8 | 33.4 | 6.96 | 1 | 0.183 | 18 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 23 | 13 | 338 | 1 | 1 | 14.7 | 11.46 | 4 | **WEAK** |
| deep middle | 7 | 4 | 120 | 1 | 0 | 17.14 | 14.39 | 7 |  |
| deep right | 36 | 18 | 443 | 4 | 3 | 12.31 | 12.14 | 17 |  |
| short left | 109 | 91 | 847 | 5 | 2 | 7.77 | 5.99 | 1 | **WEAK** |
| short middle | 53 | 37 | 454 | 5 | 1 | 8.57 | 7.32 | 3 | **WEAK** |
| short right | 99 | 83 | 657 | 2 | 2 | 6.64 | 6.02 | 6 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs TEN: **3.07 yds** (league 2.93; rank 7/32 most allowed). WR 3.05, TE 3.16, cushion 6.76. Sample: 25 receiver-games, 202 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cordale Flott | CB | 9 | 88.9 (54.0 wk11) | 43 | 28 | 364 | 3 | 2 | 8.47 | 95.5 | 11.5 | 1 | 2 | 0 | 4 | 21 (310) | MISSING |
| Alontae Taylor | CB | 8 | 90.0 (69.0 wk11) | 33 | 29 | 362 | 1 | 0 | 10.97 | 122.5 | 8.6 | 1 | 0 | 2 | 2 | 24 (337) | MISSING |
| Joshua Williams | CB | 5 | 100.0 (100.0 wk11) | 40 | 30 | 365 | 2 | 0 | 9.12 | 119.3 | 10.8 | 2 | 2 | 1 | 3 | 21 (269) | MISSING |
| Marcus Harris | CB | 8 | 56.0 (11.0 wk8) | 32 | 24 | 329 | 0 | 1 | 10.28 | 94.4 | 6.2 | 1 | 0 | 0 | 1 | 18 (172) | MISSING |
| Micah Robinson | CB | 6 | 33.8 (46.0 wk11) | 7 | 7 | 106 | 2 | 0 | 15.14 | 158.3 | 13.6 | 1 | 0 | 0 | 0 | 5 (93) | MISSING |
| Kevin Winston | S | 8 | 99.0 (100.0 wk11) | 20 | 13 | 148 | 2 | 0 | 7.40 | 120.4 | 5.5 | 0 | 0 | 0 | 0 | 18 (241) | MISSING |
| Amani Hooker | S | 7 | 99.3 (100.0 wk8) | 33 | 21 | 274 | 1 | 5 | 8.30 | 60.2 | 11.3 | 1 | 1 | 0 | 6 | 19 (252) | MISSING |
| Tony Adams | S | 8 | 43.8 (75.0 wk10) | 15 | 6 | 49 | 0 | 0 | 3.27 | 49.0 | 13.0 | 0 | 3 | 0 | 3 | 10 (146) | MISSING |
| Isaiah Oliver | S | 4 | 39.2 (69.0 wk11) | 4 | 2 | 13 | 0 | 0 | 3.25 | 57.3 | 2.8 | 0 | 1 | 0 | 1 | 4 (39) | MISSING |
| Terrell Burgess | S | 5 | 25.2 (31.0 wk11) | 8 | 7 | 97 | 2 | 0 | 12.12 | 156.8 | 13.6 | 0 | 1 | 0 | 1 | 6 (80) | MISSING |
| Erick Hallett | S | 1 | 14.0 (14.0 wk2) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Anthony Hill | 9 | 37 | 27 | 286 | 2 | 7.73 | 113.1 | 3 |
| Cody Barton | 9 | 26 | 19 | 273 | 1 | 10.50 | 119.6 | 1 |
| Cedric Gray | 9 | 18 | 14 | 98 | 2 | 5.44 | 103.2 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 10 | JAX | N.Stackhouse | PBU | P.Washington | short_middle |
| 10 | JAX | C.Flott | PBU | J.Meyers | deep_right |
| 10 | JAX | T.Adams | PBU | P.Washington | deep_left |
| 10 | JAX | C.Gray | PBU | B.Strange | deep_right |
| 10 | JAX | T.Adams | PBU | J.Meyers | deep_right |
| 10 | JAX | C.Gray | INT | J.Meyers | short_middle |
| 8 | CIN | C.Flott | PBU | J.Chase | deep_left |
| 8 | CIN | A.Hooker | INT | J.Chase | deep_right |
| 8 | CIN | A.Hooker | INT | M.Gesicki | deep_right |
| 8 | CIN | Jo.Williams | DPI | J.Chase | short_right |
| 8 | CIN | A.Hooker | INT | J.Chase | deep_right |
| 7 | CLE | J.Simmons | PBU | H.Fannin | short_middle |
| 7 | CLE | C.Flott | INT | D.Boston | short_left |
| 6 | IND | Jo.Williams | PBU | W.Mallory | deep_right |
| 6 | IND | A.Hill | PBU | L.Treadwell | deep_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Cordale Flott | CB | 52.1 | 38.0 | 497.7 | 9.55 | 2.25 | 43 (29) |
| Alontae Taylor | CB | 44.3 | 35.0 | 419.4 | 9.47 | 2.1 | 50 (32) |
| Joshua Williams | CB | 44.1 | 33.7 | 423.7 | 9.61 | 3.28 | 74 (41) |
| Anthony Hill Jr. | LB | 39.4 | 30.2 | 294.6 | 7.48 | 1.95 | 60 (31) |
| Marcus Harris | CB | 28.3 | 21.6 | 241.3 | 8.53 | 0.9 | 18 (3) |
| Amani Hooker | S | 22.7 | 15.4 | 199.3 | 8.78 | 1.4 | 20 (3) |
| Kevin Winston Jr. | S | 21.6 | 16.7 | 189.1 | 8.75 | 1.91 | 29 (2) |
| Cody Barton | LB | 20.0 | 15.9 | 141.4 | 7.07 | 0.63 | 10 (0) |
| Cedric Gray | LB | 17.3 | 13.4 | 128.7 | 7.44 | 1.12 | 5 (0) |
| Tony Adams | S | 13.1 | 7.8 | 105.5 | 8.05 | 0.96 | 7 (0) |
| Micah Robinson | CB | 12.1 | 9.3 | 123.3 | 10.19 | 0.7 | 5 (4) |

### Upcoming: opposing receivers vs likely TEN defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | JAX | P.Washington (WR) | 33 | short_left 36%, deep_left 22% | Joshua Williams (24%) | Alontae Taylor (18%) |
| 12 | 2026-11-29 | JAX | J.Meyers (WR) | 22 | short_left 36%, short_middle 25% | Joshua Williams (25%) | Alontae Taylor (17%) |
| 12 | 2026-11-29 | JAX | J.Cameron (WR) | 11 | short_middle 29%, short_left 29% | Joshua Williams (25%) | Alontae Taylor (17%) |
| 12 | 2026-11-29 | JAX | B.Strange (TE) | 8 | short_left 35%, short_middle 28% | Kevin Winston Jr. (20%) | Anthony Hill Jr. (16%) |
| 13 | 2026-12-06 | WAS | S.Diggs (WR) | 21 | short_right 32%, short_left 31% | Joshua Williams (27%) | Alontae Taylor (17%) |
| 13 | 2026-12-06 | WAS | C.Okonkwo (TE) | 20 | short_right 36%, short_left 27% | Kevin Winston Jr. (17%) | Anthony Hill Jr. (14%) |
| 13 | 2026-12-06 | WAS | A.Williams (WR) | 19 | short_right 31%, short_left 27% | Joshua Williams (26%) | Alontae Taylor (17%) |
| 13 | 2026-12-06 | WAS | A.Ekeler (RB) | 10 | short_middle 40%, short_right 33% | Anthony Hill Jr. (35%) | Cedric Gray (30%) |

Defender pool = TEN players with defensive snaps in their most recent game (2026_11_TEN_DAL); check inactives before use.
