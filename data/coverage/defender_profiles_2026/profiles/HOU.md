# HOU defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 14.3 | 31.9 | — |
| Zone % | 81.7 | 67.8 | — |
| Single-high / MOFC % | 56.2 | 52.1 | — |
| Two-high / MOFO % | 42.6 | 47.9 | — |
| Blitz % | 22.3 | 24.5 | 23.7 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 45.6 / 23.8, 81.0 | — | — |

Sharp YPT allowed: WR 8.5, TE 7.4, RB 4.1, **outside 10.1 vs slot 7.1** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #22 vs StatRankings #17; blitz rank Sharp #25 vs SR #29 (raw gaps: man -17.6 pts, blitz -2.2 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 20.6 | 175.1 | 8.5 | 9 | 0.267 | 4 |
| TE | 6.5 | 48.3 | 7.43 | 1 | 0.182 | 19 |
| RB | 6.5 | 26.8 | 4.12 | 2 | -0.18 | 25 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 29 | 11 | 291 | 0 | 1 | 10.03 | 11.46 | 21 |  |
| deep middle | 20 | 10 | 288 | 1 | 2 | 14.4 | 14.39 | 17 |  |
| deep right | 25 | 12 | 347 | 3 | 0 | 13.88 | 12.14 | 11 |  |
| short left | 92 | 69 | 487 | 1 | 1 | 5.29 | 5.99 | 28 |  |
| short middle | 63 | 40 | 462 | 2 | 2 | 7.33 | 7.32 | 15 |  |
| short right | 107 | 73 | 627 | 5 | 0 | 5.86 | 6.02 | 20 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs HOU: **2.99 yds** (league 2.93; rank 12/32 most allowed). WR 2.88, TE 3.42, cushion 7.89. Sample: 21 receiver-games, 178 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kamari Lassiter | CB | 10 | 99.6 (100.0 wk11) | 67 | 37 | 435 | 2 | 1 | 6.49 | 78.9 | 12.1 | 2 | 11 | 3 | 15 | 34 (391) | MISSING |
| Derek Stingley Jr. | CB | 10 | 98.6 (100.0 wk11) | 50 | 25 | 422 | 2 | 1 | 8.44 | 83.9 | 11.2 | 0 | 6 | 0 | 7 | 14 (194) | MISSING |
| Tremon Smith | CB | 4 | 22.8 (8.0 wk9) | 7 | 3 | 80 | 0 | 0 | 11.43 | 85.4 | 14.7 | 0 | 2 | 0 | 2 | 3 (40) | MISSING |
| Jaylin Smith | CB | 1 | 12.0 (12.0 wk2) | 1 | 1 | 16 | 0 | 0 | 16.00 | 118.8 | 7.0 | 0 | 0 | 0 | 0 | 1 (16) | MISSING |
| Calen Bullock | S | 10 | 97.7 (100.0 wk11) | 40 | 22 | 368 | 1 | 2 | 9.20 | 73.8 | 16.6 | 2 | 6 | 0 | 8 | 24 (409) | MISSING |
| Jalen Pitre | S | 8 | 94.5 (100.0 wk11) | 31 | 17 | 139 | 1 | 0 | 4.48 | 77.2 | 5.3 | 0 | 5 | 0 | 5 | 14 (117) | MISSING |
| Reed Blankenship | S | 8 | 76.8 (98.0 wk11) | 38 | 27 | 322 | 2 | 1 | 8.47 | 103.2 | 8.9 | 1 | 2 | 0 | 3 | 28 (271) | MISSING |
| M.J. Stewart | S | 4 | 78.5 (96.0 wk10) | 25 | 16 | 193 | 1 | 0 | 7.72 | 100.9 | 9.5 | 1 | 1 | 0 | 1 | 18 (218) | MISSING |
| Kamari Ramsey | S | 7 | 12.7 (4.0 wk11) | 7 | 4 | 31 | 0 | 0 | 4.43 | 68.2 | 6.6 | 0 | 0 | 0 | 0 | 3 (14) | MISSING |
| Ja'Marcus Ingram | S | 3 | 2.3 (2.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jake Hansen | 10 | 33 | 21 | 219 | 0 | 6.64 | 70.1 | 3 |
| Azeez Al-Shaair | 7 | 27 | 19 | 153 | 1 | 5.67 | 96.7 | 3 |
| Henry To'oTo'o | 6 | 14 | 9 | 108 | 1 | 7.71 | 111.6 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | IND | J.Hansen | PBU | T.Warren | short_middle |
| 11 | IND | C.Bullock | PBU | A.Dulin | deep_middle |
| 11 | IND | T.Togiai | PBU | T.Warren | short_middle |
| 11 | IND | K.Lassiter | INT | D.Burks | deep_middle |
| 11 | IND | J.Hansen | PBU | T.Warren | short_right |
| 11 | IND | K.Lassiter | PBU | D.Burks | short_left |
| 10 | CLE | C.Bullock | INT | B.Whiteheart | short_middle |
| 10 | CLE | D.Robinson | PBU | D.Boston | short_left |
| 10 | CLE | K.Lassiter | PBU | K.Concepcion | deep_middle |
| 10 | CLE | J.Clowney | PBU | Q.Judkins | short_right |
| 10 | CLE | J.Pitre | PBU | H.Fannin | short_middle |
| 10 | CLE | C.Bullock | PBU | K.Concepcion | deep_left |
| 9 | LAC | D.Robinson | PBU | D.Davis | short_middle |
| 9 | LAC | D.Stingley | PBU | K.Lambert-Smith | short_right |
| 9 | LAC | A.Al-Shaair | PBU | K.Mitchell | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Kamari Lassiter | CB | 82.4 | 51.7 | 600.3 | 7.29 | 2.5 | 106 (82) |
| Derek Stingley Jr. | CB | 65.5 | 38.5 | 527.9 | 8.06 | 3.14 | 89 (60) |
| Calen Bullock | S | 34.0 | 19.2 | 331.1 | 9.74 | 1.14 | 27 (12) |
| Jake Hansen | LB | 31.1 | 22.3 | 175.5 | 5.64 | 0.72 | 30 (21) |
| Azeez Al-Shaair | LB | 29.8 | 20.8 | 191.3 | 6.42 | 1.24 | 27 (11) |
| Henry To'oTo'o | LB | 23.5 | 15.5 | 160.2 | 6.82 | 1.13 | 24 (9) |
| Jalen Pitre | S | 21.6 | 13.9 | 169.6 | 7.85 | 0.76 | 7 (0) |
| Reed Blankenship | S | 21.2 | 14.3 | 140.1 | 6.61 | 0.43 | 14 (1) |
| M.J. Stewart | S | 11.8 | 8.6 | 104.7 | 8.87 | 0.31 | 10 (6) |
| Tremon Smith | CB | 6.2 | 4.1 | 56.6 | 9.13 | 0.42 | 0 (0) |

### Upcoming: opposing receivers vs likely HOU defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | BAL | Z.Flowers (WR) | 24 | short_right 35%, short_middle 30% | Derek Stingley Jr. (32%) | Kamari Lassiter (26%) |
| 12 | 2026-11-29 | BAL | J.Hill (RB) | 15 | short_right 57%, short_left 25% | Henry To'oTo'o (34%) | Jake Hansen (22%) |
| 12 | 2026-11-29 | BAL | M.Andrews (TE) | 13 | short_middle 41%, short_left 30% | Reed Blankenship (18%) | Jalen Pitre (17%) |
| 12 | 2026-11-29 | BAL | R.Bateman (WR) | 13 | short_left 26%, short_right 24% | Kamari Lassiter (32%) | Derek Stingley Jr. (29%) |
| 13 | 2026-12-06 | PIT | G.Bernard (WR) | 13 | short_left 31%, short_right 31% | Derek Stingley Jr. (31%) | Kamari Lassiter (30%) |
| 13 | 2026-12-06 | PIT | D.Metcalf (WR) | 10 | short_right 27%, short_left 26% | Kamari Lassiter (32%) | Derek Stingley Jr. (30%) |
| 13 | 2026-12-06 | PIT | J.Warren (RB) | 9 | short_right 51%, short_left 31% | Henry To'oTo'o (34%) | Jake Hansen (22%) |
| 13 | 2026-12-06 | PIT | P.Freiermuth (TE) | 8 | short_left 30%, short_middle 26% | Reed Blankenship (17%) | Jalen Pitre (17%) |

Defender pool = HOU players with defensive snaps in their most recent game (2026_11_IND_HOU); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Jalen Pitre | S | 83.8 | 53.2 | 689.3 | 8.23 | 10.92 | 344.1 | 10 |
| Derek Stingley Jr. | CB | 36.9 | 20.1 | 328.1 | 8.89 | 6.04 | 206.4 | 9 |
| Calen Bullock | S | 23.6 | 11.3 | 264.6 | 11.21 | 5.6 | 191.5 | 6 |
| Kamari Lassiter | CB | 41.4 | 26.2 | 295.3 | 7.13 | 4.37 | 138.1 | 5 |
| Henry To'oTo'o | LB | 33.3 | 22.4 | 218.2 | 6.55 | 3.39 | 89.0 | 5 |
| Azeez Al-Shaair | LB | 42.6 | 32.2 | 258.2 | 6.06 | 2.32 | 57.9 | 2 |
| Tremon Smith | CB | 13.0 | 8.2 | 110.0 | 8.46 | 1.75 | 51.4 | 0 |
| M.J. Stewart | S | 12.1 | 7.1 | 80.3 | 6.64 | 1.52 | 49.9 | 1 |
| Jake Hansen | LB | 32.2 | 23.1 | 169.5 | 5.26 | 1.49 | 33.0 | 0 |
| Reed Blankenship | S | 12.2 | 7.6 | 61.0 | 5.0 | 0.37 | 8.4 | 0 |

### Rest of Week 12: receivers vs likely HOU window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | BAL | Z.Flowers (WR) | 24 | 10% | Jalen Pitre (40%, 10.92) | Henry To'oTo'o (20%, 3.39) |
| 2026-11-29 | BAL | J.Hill (RB) | 15 | 0% | Henry To'oTo'o (53%, 3.39) | Jake Hansen (21%, 1.49) |
| 2026-11-29 | BAL | M.Andrews (TE) | 13 | 4% | Jalen Pitre (46%, 10.92) | Henry To'oTo'o (31%, 3.39) |
| 2026-11-29 | BAL | R.Bateman (WR) | 13 | 17% | Jalen Pitre (39%, 10.92) | Kamari Lassiter (19%, 4.37) |
