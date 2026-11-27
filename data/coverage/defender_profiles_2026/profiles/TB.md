# TB defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 14.9 | 29.7 | — |
| Zone % | 80.1 | 69.8 | — |
| Single-high / MOFC % | 62.6 | 63.9 | — |
| Two-high / MOFO % | 36.0 | 36.1 | — |
| Blitz % | 41.8 | 44.7 | 43.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 34.6 / 34.6, 61.0 | — | — |

Sharp YPT allowed: WR 7.6, TE 7.9, RB 5.3, **outside 8.2 vs slot 7.0** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #21 vs StatRankings #20; blitz rank Sharp #2 vs SR #2 (raw gaps: man -14.8 pts, blitz -2.9 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 18.3 | 138.2 | 7.55 | 9 | -0.101 | 23 |
| TE | 8.2 | 64.8 | 7.9 | 5 | 0.104 | 5 |
| RB | 5.5 | 28.9 | 5.25 | 0 | 0.022 | 23 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 22 | 9 | 287 | 2 | 2 | 13.05 | 11.46 | 13 |  |
| deep middle | 13 | 6 | 216 | 2 | 0 | 16.62 | 14.39 | 9 |  |
| deep right | 15 | 4 | 130 | 0 | 2 | 8.67 | 12.14 | 27 |  |
| short left | 106 | 78 | 596 | 3 | 1 | 5.62 | 5.99 | 20 |  |
| short middle | 60 | 39 | 437 | 3 | 5 | 7.28 | 7.32 | 17 |  |
| short right | 104 | 74 | 653 | 4 | 6 | 6.28 | 6.02 | 13 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs TB: **3.16 yds** (league 2.93; rank 6/32 most allowed). WR 3.01, TE 3.55, cushion 5.44. Sample: 24 receiver-games, 176 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Zyon McCollum | CB | 10 | 99.8 (100.0 wk11) | 56 | 30 | 338 | 2 | 4 | 6.04 | 54.0 | 10.1 | 2 | 7 | 1 | 12 | 26 (296) | MISSING |
| Jacob Parrish | CB | 9 | 81.2 (10.0 wk11) | 54 | 27 | 371 | 1 | 2 | 6.87 | 63.1 | 9.8 | 3 | 11 | 2 | 15 | 23 (220) | MISSING |
| Benjamin Morrison | CB | 4 | 54.8 (50.0 wk11) | 23 | 16 | 219 | 2 | 0 | 9.52 | 128.7 | 8.4 | 1 | 2 | 0 | 2 | 13 (111) | MISSING |
| Kevin Knowles | CB | 1 | 34.0 (34.0 wk11) | 0 | 0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | 1 (10) | MISSING |
| Ayden Garnes | CB | 1 | 2.0 (2.0 wk5) | 1 | 1 | 18 | 1 | 0 | 18.00 | 158.3 | 18.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Keionte Scott | DB | 10 | 60.5 (34.0 wk11) | 42 | 29 | 257 | 3 | 0 | 6.12 | 108.9 | 6.2 | 0 | 4 | 0 | 4 | 20 (161) | MISSING |
| Tykee Smith | S | 10 | 95.2 (93.0 wk11) | 49 | 23 | 320 | 3 | 2 | 6.53 | 71.8 | 6.9 | 0 | 2 | 0 | 4 | 22 (236) | MISSING |
| Antoine Winfield Jr. | S | 6 | 88.8 (48.0 wk9) | 12 | 6 | 79 | 0 | 0 | 6.58 | 71.2 | 14.3 | 0 | 1 | 0 | 1 | 12 (223) | MISSING |
| Ifeatu Melifonwu | S | 7 | 64.4 (91.0 wk11) | 14 | 6 | 109 | 0 | 0 | 7.79 | 70.2 | 15.4 | 0 | 1 | 0 | 1 | 8 (150) | MISSING |
| Miles Killebrew | S | 7 | 3.4 (5.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| JJ Roberts | S | 1 | 2.0 (2.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Alex Anzalone | 10 | 52 | 35 | 398 | 2 | 7.65 | 70.8 | 0 |
| Josiah Trotter | 9 | 34 | 20 | 172 | 1 | 5.06 | 69.7 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | DET | T.Smith | PBU | S.LaPorta | short_left |
| 11 | DET | K.Scott | PBU | S.LaPorta | short_middle |
| 11 | DET | V.Vea | PBU | I.TeSlaa | short_middle |
| 11 | DET | Y.Diaby | PBU | J.Gibbs | short_middle |
| 9 | CHI | I.Melifonwu | PBU | C.Loveland | deep_right |
| 9 | CHI | A.Anzalone | INT | L.Burden | short_left |
| 9 | CHI | Z.McCollum | INT | K.Raymond | deep_right |
| 9 | CHI | Z.McCollum | INT | L.Burden | deep_right |
| 9 | CHI | T.Smith | INT | R.Odunze | deep_left |
| 9 | CHI | A.Winfield | PBU | C.Loveland | short_right |
| 8 | ATL | A.Robinson | PBU | K.Pitts | short_middle |
| 8 | ATL | J.Parrish | PBU | J.Dotson | short_left |
| 8 | ATL | Z.McCollum | INT | C.Woerner | short_right |
| 8 | ATL | J.Parrish | INT | D.London | short_middle |
| 8 | ATL | K.Scott | PBU | J.Dotson | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Zyon McCollum | CB | 59.5 | 37.3 | 430.5 | 7.24 | 2.85 | 84 (73) |
| Jacob Parrish | CB | 54.4 | 32.5 | 414.5 | 7.62 | 2.23 | 77 (66) |
| Keionte Scott | CB | 31.1 | 19.9 | 219.1 | 7.05 | 1.2 | 0 (0) |
| Alex Anzalone | LB | 30.6 | 21.4 | 217.5 | 7.11 | 1.52 | 57 (6) |
| Josiah Trotter | LB | 28.4 | 20.4 | 183.5 | 6.46 | 0.92 | 38 (12) |
| Tykee Smith | S | 24.5 | 15.8 | 174.3 | 7.11 | 1.52 | 28 (4) |
| Benjamin Morrison | CB | 15.3 | 12.0 | 121.9 | 7.97 | 0.61 | 24 (15) |
| Antoine Winfield Jr. | S | 12.7 | 8.0 | 106.9 | 8.42 | 0.78 | 7 (1) |
| Yaya Diaby | LB | 12.2 | 8.7 | 77.6 | 6.36 | 0.37 | 0 (0) |
| Ifeatu Melifonwu | S | 10.5 | 6.0 | 98.4 | 9.37 | 0.59 | 5 (1) |
| Rueben Bain Jr. | nan | 10.4 | 6.9 | 70.1 | 6.74 | 0.34 | 0 (0) |
| Al-Quadin Muhammad | LB | 9.6 | 6.6 | 61.9 | 6.45 | 0.31 | 0 (0) |

### Upcoming: opposing receivers vs likely TB defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-30 | CAR | T.McMillan (WR) | 22 | short_right 25%, short_middle 24% | Zyon McCollum (24%) | Benjamin Morrison (14%) |
| 12 | 2026-11-30 | CAR | D.Waller (TE) | 17 | short_right 38%, short_left 26% | Tykee Smith (15%) | Ifeatu Melifonwu (14%) |
| 12 | 2026-11-30 | CAR | J.Coker (WR) | 16 | short_left 38%, short_middle 22% | Zyon McCollum (20%) | Benjamin Morrison (16%) |
| 12 | 2026-11-30 | CAR | T.Tremble (TE) | 12 | short_left 44%, short_right 39% | Tykee Smith (16%) | Ifeatu Melifonwu (14%) |
| 13 | 2026-12-06 | LAC | T.Harris (WR) | 14 | short_right 31%, short_left 29% | Zyon McCollum (29%) | Benjamin Morrison (14%) |
| 13 | 2026-12-06 | LAC | L.McConkey (WR) | 8 | short_right 31%, short_middle 22% | Zyon McCollum (27%) | Benjamin Morrison (12%) |
| 13 | 2026-12-06 | LAC | C.Kolar (TE) | 7 | short_right 62%, short_middle 21% | Tykee Smith (14%) | Zyon McCollum (14%) |
| 13 | 2026-12-06 | LAC | Q.Johnston (WR) | 7 | short_right 30%, short_left 21% | Zyon McCollum (28%) | Benjamin Morrison (15%) |

Defender pool = TB players with defensive snaps in their most recent game (2026_11_TB_DET); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Tykee Smith | S | 59.2 | 37.5 | 427.0 | 7.21 | 5.21 | 169.9 | 4 |
| Keionte Scott | CB | 56.2 | 34.7 | 369.7 | 6.58 | 3.61 | 126.0 | 5 |
| Jacob Parrish | CB | 30.0 | 18.0 | 252.9 | 8.43 | 3.31 | 126.8 | 3 |
| Ifeatu Melifonwu | S | 8.1 | 4.8 | 151.0 | 18.64 | 3.05 | 130.3 | 5 |
| Zyon McCollum | CB | 32.6 | 21.0 | 247.6 | 7.6 | 2.43 | 74.4 | 2 |
| Alex Anzalone | LB | 65.7 | 45.5 | 399.9 | 6.09 | 2.12 | 82.5 | 1 |
| Antoine Winfield Jr. | S | 8.3 | 3.2 | 83.5 | 10.06 | 2.01 | 70.6 | 2 |
| Benjamin Morrison | CB | 14.1 | 11.0 | 118.4 | 8.4 | 1.35 | 38.2 | 2 |
| Josiah Trotter | LB | 43.2 | 32.3 | 257.6 | 5.96 | 0.92 | 27.3 | 0 |

### Rest of Week 12: receivers vs likely TB window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-30 | CAR | T.McMillan (WR) | 22 | 16% | Tykee Smith (40%, 5.21) | Alex Anzalone (16%, 2.12) |
| 2026-11-30 | CAR | D.Waller (TE) | 17 | 14% | Tykee Smith (50%, 5.21) | Alex Anzalone (20%, 2.12) |
| 2026-11-30 | CAR | J.Coker (WR) | 16 | 17% | Tykee Smith (40%, 5.21) | Benjamin Morrison (18%, 1.35) |
| 2026-11-30 | CAR | T.Tremble (TE) | 12 | 0% | Tykee Smith (50%, 5.21) | Josiah Trotter (24%, 0.92) |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Benjamin Morrison (CB) 23 tgt, 69.6% catch, 9.52 ypt, rating 128.7 [TARGET MAGNET, WEAK LINK]
**Best / lockdown:** Zyon McCollum (CB) 56 tgt, 53.6% catch, 6.04 ypt, rating 54.0 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS]
**Weak zones:** none flagged

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Zyon McCollum | CB | 9 | 56 | 24% | 53.6 | 6.04 | 11.27 | 0.557 | 54.0 | 2 | 4 | 7 | 70.8 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS |  |
| Jacob Parrish | CB | 9 | 54 | 24% | 50.0 | 6.87 | 13.74 | 0.828 | 63.1 | 1 | 2 | 11 | 62.8 | LIMITS CATCHES, TARGET MAGNET |  |
| Keionte Scott | CB | 10 | 42 | 17% | 69.0 | 6.12 | 8.86 | 0.696 | 108.9 | 3 | 0 | 4 | 46.0 | LIMITS YARDS |  |
| Benjamin Morrison | CB | 3 | 23 | 33% | 69.6 | 9.52 | 13.69 | 1.672 | 128.7 | 2 | 0 | 2 | 5.2 | TARGET MAGNET, WEAK LINK | small sample (<35 tgts) |
| Tykee Smith | S | 10 | 49 | 20% | 46.9 | 6.53 | 13.91 | 0.551 | 71.8 | 3 | 2 | 2 | 66.0 | LIMITS CATCHES, LIMITS YARDS |  |
