# DAL defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 22.3 | 46.6 | — |
| Zone % | 69.3 | 51.8 | — |
| Single-high / MOFC % | 55.7 | 58.1 | — |
| Two-high / MOFO % | 39.3 | 41.9 | — |
| Blitz % | 20.1 | 25.1 | 21.9 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 50.6 / 18.8, 69.0 | — | — |

Sharp YPT allowed: WR 8.9, TE 7.3, RB 7.2, **outside 8.2 vs slot 10.3** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #10 vs StatRankings #2; blitz rank Sharp #30 vs SR #27 (raw gaps: man -24.3 pts, blitz -5.0 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.2 | 177.0 | 9.23 | 15 | 0.39 | 3 |
| TE | 6.6 | 46.2 | 7.01 | 4 | 0.222 | 21 |
| RB | 4.8 | 33.7 | 7.09 | 5 | 0.255 | 16 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 29 | 10 | 264 | 0 | 0 | 9.1 | 11.46 | 24 |  |
| deep middle | 13 | 7 | 188 | 0 | 1 | 14.46 | 14.39 | 16 |  |
| deep right | 38 | 18 | 493 | 5 | 1 | 12.97 | 12.14 | 13 |  |
| short left | 111 | 86 | 784 | 6 | 1 | 7.06 | 5.99 | 3 | **WEAK** |
| short middle | 54 | 39 | 427 | 4 | 1 | 7.91 | 7.32 | 7 | **WEAK** |
| short right | 121 | 98 | 926 | 9 | 1 | 7.65 | 6.02 | 1 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs DAL: **2.97 yds** (league 2.93; rank 15/32 most allowed). WR 2.86, TE 3.36, cushion 5.95. Sample: 29 receiver-games, 223 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DaRon Bland | CB | 10 | 89.3 (14.0 wk10) | 57 | 36 | 495 | 5 | 0 | 8.68 | 120.1 | 11.8 | 4 | 7 | 4 | 11 | 21 (250) | MISSING |
| Cobie Durant | CB | 8 | 72.0 (100.0 wk12) | 24 | 15 | 223 | 1 | 0 | 9.29 | 106.8 | 12.6 | 1 | 2 | 0 | 3 | 18 (224) | MISSING |
| Joey Porter Jr. | CB | 7 | 66.6 (87.0 wk12) | 15 | 4 | 23 | 0 | 0 | 1.53 | 39.6 | 12.9 | 0 | 5 | 1 | 6 | 8 (50) | MISSING |
| Ameer Speed | CB | 11 | 24.9 (13.0 wk12) | 14 | 6 | 68 | 1 | 0 | 4.86 | 81.8 | 18.2 | 0 | 3 | 0 | 3 | 6 (73) | MISSING |
| Shavon Revel | CB | 9 | 28.7 (20.0 wk11) | 22 | 14 | 163 | 1 | 0 | 7.41 | 101.1 | 9.6 | 0 | 1 | 1 | 2 | 11 (136) | MISSING |
| Reddy Steward | CB | 3 | 46.0 (64.0 wk5) | 13 | 12 | 186 | 2 | 0 | 14.31 | 158.3 | 8.7 | 1 | 0 | 0 | 0 | 9 (92) | MISSING |
| Caelen Carson | CB | 1 | 27.0 (27.0 wk3) | 2 | 1 | 2 | 1 | 0 | 1.00 | 95.8 | 2.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Derion Kendrick | CB | 1 | 20.0 (20.0 wk11) | 2 | 2 | 26 | 0 | 0 | 13.00 | 118.8 | 11.5 | 0 | 0 | 0 | 0 | 1 (5) | MISSING |
| Caleb Downs | DB | 12 | 93.2 (98.0 wk12) | 37 | 29 | 319 | 2 | 1 | 8.62 | 109.3 | 8.6 | 2 | 3 | 2 | 6 | 25 (305) | MISSING |
| Malik Hooker | S | 10 | 69.6 (98.0 wk12) | 16 | 9 | 123 | 0 | 0 | 7.69 | 81.0 | 9.8 | 0 | 5 | 1 | 6 | 17 (279) | MISSING |
| Markquese Bell | S | 11 | 43.0 (10.0 wk12) | 16 | 13 | 188 | 1 | 0 | 11.75 | 136.5 | 8.1 | 0 | 1 | 3 | 4 | 17 (238) | MISSING |
| Jalen Thompson | S | 4 | 81.2 (83.0 wk12) | 4 | 3 | 32 | 0 | 0 | 8.00 | 97.9 | 6.0 | 0 | 0 | 0 | 0 | 8 (90) | MISSING |
| P.J. Locke | S | 4 | 49.0 (67.0 wk9) | 7 | 4 | 41 | 2 | 0 | 5.86 | 113.7 | 7.6 | 0 | 2 | 0 | 2 | 8 (90) | MISSING |
| Alijah Clark | S | 7 | 21.9 (19.0 wk11) | 3 | 1 | 31 | 0 | 0 | 10.33 | 72.9 | 26.3 | 0 | 2 | 0 | 2 | 2 (45) | MISSING |
| Juanyeh Thomas | S | 4 | 13.2 (25.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Dee Winters | 10 | 31 | 22 | 242 | 1 | 7.81 | 91.1 | 0 |
| Shemar James | 12 | 22 | 18 | 138 | 0 | 6.27 | 73.9 | 0 |
| Jaishawn Barham | 10 | 20 | 16 | 132 | 1 | 6.60 | 110.8 | 0 |
| DeMarvion Overshown | 6 | 16 | 14 | 125 | 2 | 7.81 | 112.8 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | PHI | M.Bell | DPI | Z.Ertz | short_left |
| 12 | PHI | C.Durant | INT | M.Lemon | deep_right |
| 12 | PHI | M.Hooker | PBU | D.Smith | deep_left |
| 12 | PHI | C.Downs | PBU | E.Moore | deep_right |
| 12 | PHI | M.Hooker | DPI | Z.Ertz | deep_right |
| 11 | TEN | A.Speed | PBU | C.Dike | deep_right |
| 11 | TEN | M.Hooker | PBU | C.Ridley | short_middle |
| 11 | TEN | J.Porter | PBU | C.Tate | short_middle |
| 11 | TEN | C.Downs | DPI | C.Tate | deep_left |
| 11 | TEN | Q.Williams | PBU | G.Helm | short_left |
| 10 | SF | M.Hooker | PBU | G.Kittle | deep_left |
| 10 | SF | J.Porter | PBU | J.Watkins | short_left |
| 10 | SF | L.Overton | PBU | G.Kittle | short_middle |
| 9 | IND | C.Downs | INT | K.Allen | deep_middle |
| 9 | IND | P.Locke | PBU | J.Downs | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Caleb Downs | CB | 58.7 | 37.2 | 515.2 | 8.78 | 3.17 | 81 (20) |
| DaRon Bland | CB | 51.6 | 31.9 | 410.7 | 7.96 | 2.72 | 82 (44) |
| Cobie Durant | CB | 36.5 | 25.6 | 357.5 | 9.79 | 3.06 | 39 (25) |
| Joey Porter Jr. | CB | 24.9 | 17.9 | 240.4 | 9.65 | 1.98 | 33 (0) |
| Shemar James | LB | 23.5 | 18.5 | 201.6 | 8.58 | 1.74 | 30 (6) |
| Malik Hooker | S | 16.3 | 10.7 | 140.6 | 8.63 | 0.82 | 6 (0) |
| Dee Winters | LB | 16.0 | 13.1 | 120.4 | 7.52 | 1.01 | 18 (1) |
| Rashan Gary | LB | 15.9 | 12.3 | 115.9 | 7.29 | 1.17 | 4 (0) |
| Donovan Ezeiruaku | LB | 15.3 | 11.7 | 98.6 | 6.44 | 1.1 | 15 (0) |
| Ameer Speed | CB | 12.7 | 8.6 | 126.9 | 9.99 | 0.87 | 0 (0) |
| Shavon Revel Jr. | CB | 12.4 | 8.7 | 107.8 | 8.69 | 0.73 | 4 (0) |
| Jaishawn Barham | LB | 11.8 | 9.5 | 80.7 | 6.84 | 0.87 | 7 (0) |

### Upcoming: opposing receivers vs likely DAL defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-07 | SEA | J.Smith-Njigba (WR) | 20 | short_right 31%, short_left 25% | Caleb Downs (23%) | Cobie Durant (20%) |
| 13 | 2026-12-07 | SEA | A.Barner (TE) | 7 | short_right 49%, short_left 29% | Malik Hooker (13%) | Shemar James (12%) |
| 13 | 2026-12-07 | SEA | C.Kupp (WR) | 5 | short_left 31%, short_right 29% | Caleb Downs (23%) | Cobie Durant (20%) |
| 13 | 2026-12-07 | SEA | J.Price (RB) | 5 | short_right 38%, short_left 38% | Shemar James (18%) | Dee Winters (13%) |

Defender pool = DAL players with defensive snaps in their most recent game (2026_12_PHI_DAL); check inactives before use.
