# ATL defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 21.9 | 37.6 | — |
| Zone % | 70.8 | 62.1 | — |
| Single-high / MOFC % | 60.7 | 60.2 | — |
| Two-high / MOFO % | 33.5 | 39.8 | — |
| Blitz % | 23.3 | 26.6 | 25.6 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 41.1 / 30.0, 73.0 | — | — |

Sharp YPT allowed: WR 8.7, TE 7.2, RB 4.9, **outside 9.8 vs slot 7.9** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #12 vs StatRankings #12; blitz rank Sharp #24 vs SR #23 (raw gaps: man -15.7 pts, blitz -3.3 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 19.2 | 164.9 | 8.59 | 10 | 0.302 | 6 |
| TE | 7.1 | 51.0 | 7.18 | 4 | 0.067 | 18 |
| RB | 7.1 | 34.8 | 4.9 | 5 | 0.045 | 13 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 34 | 10 | 301 | 2 | 0 | 8.85 | 11.46 | 25 |  |
| deep middle | 11 | 8 | 244 | 0 | 0 | 22.18 | 14.39 | 2 |  |
| deep right | 22 | 10 | 286 | 2 | 0 | 13.0 | 12.14 | 12 |  |
| short left | 98 | 81 | 629 | 6 | 0 | 6.42 | 5.99 | 11 |  |
| short middle | 43 | 30 | 294 | 3 | 2 | 6.84 | 7.32 | 22 |  |
| short right | 126 | 93 | 753 | 6 | 1 | 5.98 | 6.02 | 17 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs ATL: **2.88 yds** (league 2.93; rank 22/32 most allowed). WR 2.77, TE 3.29, cushion 6.22. Sample: 25 receiver-games, 197 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C.J. Henderson | CB | 9 | 78.6 (100.0 wk10) | 51 | 28 | 360 | 3 | 0 | 7.06 | 96.9 | 12.0 | 3 | 9 | 1 | 10 | 26 (321) | MISSING |
| Mike Hughes | CB | 10 | 62.0 (5.0 wk10) | 47 | 29 | 447 | 4 | 0 | 9.51 | 121.5 | 11.8 | 3 | 5 | 1 | 6 | 18 (252) | MISSING |
| AJ Terrell | CB | 6 | 83.3 (100.0 wk10) | 25 | 14 | 256 | 4 | 0 | 10.24 | 131.0 | 14.0 | 1 | 4 | 1 | 5 | 8 (101) | MISSING |
| Avieon Terrell | CB | 7 | 45.1 (18.0 wk9) | 15 | 7 | 73 | 0 | 0 | 4.87 | 61.2 | 10.8 | 0 | 0 | 1 | 1 | 6 (47) | MISSING |
| Billy Bowman | CB | 5 | 46.0 (42.0 wk10) | 24 | 14 | 151 | 1 | 0 | 6.29 | 90.8 | 8.7 | 0 | 3 | 1 | 4 | 7 (89) | MISSING |
| Mike Ford | CB | 2 | 1.0 (1.0 wk6) | 1 | 1 | 7 | 1 | 0 | 7.00 | 135.4 | 7.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Sydney Brown | DB | 10 | 36.1 (40.0 wk10) | 14 | 11 | 77 | 1 | 0 | 5.50 | 113.4 | 2.9 | 0 | 1 | 1 | 2 | 12 (121) | MISSING |
| Xavier Watts | S | 10 | 98.6 (100.0 wk10) | 31 | 22 | 270 | 1 | 1 | 8.71 | 94.8 | 9.9 | 1 | 1 | 1 | 3 | 27 (374) | MISSING |
| Jessie Bates III | S | 9 | 96.8 (100.0 wk9) | 30 | 20 | 240 | 5 | 1 | 8.00 | 116.7 | 9.2 | 0 | 3 | 0 | 4 | 27 (284) | MISSING |
| DeMarcco Hellams | S | 6 | 21.8 (95.0 wk10) | 8 | 6 | 42 | 0 | 0 | 5.25 | 86.5 | 10.6 | 0 | 1 | 0 | 1 | 8 (105) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Harold Perkins | 10 | 39 | 23 | 177 | 1 | 4.54 | 78.7 | 1 |
| Kendal Daniels | 10 | 37 | 27 | 186 | 0 | 5.03 | 72.6 | 1 |
| Divine Deablo | 7 | 19 | 17 | 199 | 0 | 10.47 | 110.3 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 10 | KC | J.Pearce | PBU | E.Johnson | short_right |
| 10 | KC | B.Bowman | PBU | C.Allen | deep_left |
| 9 | CIN | C.Henderson | DPI | J.Chase | short_right |
| 9 | CIN | A.Terrell | PBU | T.Higgins | short_right |
| 9 | CIN | C.Henderson | PBU | J.Chase | short_right |
| 8 | TB | M.Hughes | PBU | T.Hurst | deep_right |
| 7 | SF | C.Henderson | PBU | J.Cowing | short_left |
| 7 | SF | M.Hughes | PBU | G.Kittle | short_left |
| 7 | SF | K.Daniels | INT | J.Watkins | short_middle |
| 7 | SF | J.Bates | PBU | G.Kittle | short_right |
| 7 | SF | C.Henderson | PBU | J.Watkins | deep_left |
| 7 | SF | A.Terrell | PBU | J.Watkins | deep_left |
| 7 | SF | J.Bates | INT | J.Cowing | short_right |
| 6 | CHI | B.Dorlus | PBU | R.Odunze | short_right |
| 5 | BAL | X.Watts | DPI | — | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| C.J. Henderson | CB | 54.3 | 34.5 | 472.3 | 8.7 | 2.97 | 78 (52) |
| Mike Hughes | CB | 44.2 | 27.8 | 350.8 | 7.94 | 1.52 | 42 (29) |
| Xavier Watts | S | 30.3 | 20.7 | 233.4 | 7.7 | 1.43 | 30 (9) |
| Kendal Daniels | LB | 29.2 | 22.2 | 188.2 | 6.45 | 1.99 | 30 (12) |
| Jessie Bates | S | 28.9 | 21.9 | 201.5 | 6.97 | 1.58 | 37 (16) |
| A.J. Terrell | CB | 25.4 | 15.8 | 204.3 | 8.04 | 2.18 | 34 (22) |
| Harold Perkins Jr. | LB | 24.5 | 18.6 | 145.0 | 5.92 | 1.64 | 19 (14) |
| Divine Deablo | LB | 22.3 | 16.4 | 128.7 | 5.77 | 1.22 | 33 (8) |
| Sydney Brown | CB | 18.8 | 13.9 | 152.7 | 8.12 | 0.93 | 2 (0) |
| Avieon Terrell | CB | 18.2 | 14.6 | 146.3 | 8.04 | 0.67 | 10 (8) |
| Billy Bowman Jr. | CB | 16.9 | 9.7 | 122.4 | 7.24 | 1.16 | 13 (0) |
| Jared Ivey | LB | 5.4 | 4.0 | 32.5 | 6.02 | 0.38 | 0 (0) |

### Upcoming: opposing receivers vs likely ATL defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | MIN | J.Jefferson (WR) | 33 | short_left 36%, short_right 29% | C.J. Henderson (27%) | A.J. Terrell (25%) |
| 12 | 2026-11-29 | MIN | T.Felton (WR) | 17 | short_left 38%, short_right 25% | C.J. Henderson (26%) | A.J. Terrell (23%) |
| 12 | 2026-11-29 | MIN | T.Hockenson (TE) | 14 | short_left 33%, short_right 25% | Xavier Watts (18%) | DeMarcco Hellams (16%) |
| 12 | 2026-11-29 | MIN | M.Price (WR) | 10 | short_left 41%, short_right 24% | C.J. Henderson (28%) | A.J. Terrell (24%) |
| 13 | 2026-12-06 | DET | A.St. Brown (WR) | 31 | short_left 31%, short_right 26% | C.J. Henderson (27%) | A.J. Terrell (23%) |
| 13 | 2026-12-06 | DET | J.Williams (WR) | 22 | short_left 33%, deep_left 17% | C.J. Henderson (29%) | A.J. Terrell (24%) |
| 13 | 2026-12-06 | DET | S.LaPorta (TE) | 20 | short_right 33%, short_middle 28% | Xavier Watts (18%) | DeMarcco Hellams (18%) |
| 13 | 2026-12-06 | DET | J.Gibbs (RB) | 19 | short_left 40%, short_middle 30% | Kendal Daniels (35%) | Harold Perkins Jr. (20%) |

Defender pool = ATL players with defensive snaps in their most recent game (2026_10_KC_ATL); check inactives before use.
