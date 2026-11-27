# LV defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 22.4 | 33.2 | — |
| Zone % | 68.8 | 66.8 | — |
| Single-high / MOFC % | 47.6 | 49.4 | — |
| Two-high / MOFO % | 47.1 | 50.6 | — |
| Blitz % | 25.4 | 30.4 | 28.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 42.6 / 34.2, 73.0 | — | — |

Sharp YPT allowed: WR 10.0, TE 6.6, RB 7.3, **outside 9.7 vs slot 11.6** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #9 vs StatRankings #15; blitz rank Sharp #21 vs SR #17 (raw gaps: man -10.8 pts, blitz -5.0 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 16.5 | 162.6 | 9.88 | 13 | 0.413 | 7 |
| TE | 8.3 | 54.6 | 6.6 | 9 | 0.151 | 13 |
| RB | 3.7 | 27.4 | 7.34 | 1 | 0.399 | 24 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 32 | 14 | 458 | 1 | 2 | 14.31 | 11.46 | 7 | **WEAK** |
| deep middle | 22 | 12 | 385 | 4 | 1 | 17.5 | 14.39 | 6 | **WEAK** |
| deep right | 31 | 12 | 303 | 1 | 1 | 9.77 | 12.14 | 25 |  |
| short left | 97 | 74 | 671 | 9 | 2 | 6.92 | 5.99 | 5 | **WEAK** |
| short middle | 38 | 28 | 253 | 2 | 1 | 6.66 | 7.32 | 26 |  |
| short right | 93 | 76 | 621 | 6 | 0 | 6.68 | 6.02 | 4 | **WEAK** |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs LV: **3.06 yds** (league 2.93; rank 8/32 most allowed). WR 2.80, TE 3.80, cushion 4.99. Sample: 21 receiver-games, 155 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Eric Stokes | CB | 11 | 97.4 (97.0 wk11) | 54 | 33 | 451 | 4 | 0 | 8.35 | 112.5 | 13.2 | 0 | 4 | 4 | 8 | 24 (294) | MISSING |
| Taron Johnson | CB | 11 | 74.0 (81.0 wk11) | 38 | 25 | 233 | 2 | 0 | 6.13 | 100.0 | 5.8 | 0 | 2 | 1 | 3 | 17 (169) | MISSING |
| Hezekiah Masses | CB | 11 | 45.4 (8.0 wk11) | 33 | 18 | 301 | 4 | 3 | 9.12 | 87.2 | 15.8 | 0 | 4 | 3 | 10 | 15 (206) | MISSING |
| Darien Porter | CB | 8 | 50.0 (53.0 wk10) | 25 | 14 | 217 | 1 | 0 | 8.68 | 98.2 | 14.5 | 0 | 5 | 0 | 5 | 11 (160) | MISSING |
| Jermod McCoy | CB | 6 | 40.7 (97.0 wk11) | 12 | 7 | 141 | 1 | 0 | 11.75 | 127.4 | 18.7 | 0 | 3 | 0 | 3 | 6 (85) | MISSING |
| Jeremy Chinn | S | 11 | 100.0 (100.0 wk11) | 28 | 22 | 243 | 1 | 1 | 8.68 | 99.9 | 10.8 | 0 | 1 | 0 | 2 | 31 (446) | MISSING |
| Treydan Stukes | S | 10 | 94.6 (100.0 wk11) | 35 | 21 | 331 | 3 | 2 | 9.46 | 96.2 | 13.9 | 2 | 3 | 0 | 5 | 21 (348) | MISSING |
| Isaiah Pola-Mao | S | 4 | 41.0 (3.0 wk11) | 7 | 6 | 89 | 2 | 0 | 12.71 | 158.3 | 8.2 | 0 | 0 | 0 | 0 | 5 (64) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Quay Walker | 11 | 36 | 27 | 294 | 1 | 8.17 | 107.9 | 0 |
| Nakobe Dean | 11 | 30 | 24 | 241 | 2 | 8.03 | 108.5 | 2 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | DEN | M.Crosby | PBU | M.Mims | short_right |
| 11 | DEN | N.Dean | PBU | J.Waddle | deep_left |
| 11 | DEN | T.Stukes | PBU | J.Waddle | deep_left |
| 11 | DEN | E.Stokes | DPI | J.Waddle | short_right |
| 11 | DEN | M.Crosby | PBU | C.Sutton | short_middle |
| 11 | DEN | J.McCoy | PBU | J.Waddle | deep_left |
| 10 | SEA | E.Stokes | PBU | R.Shaheed | short_right |
| 9 | SF | J.McCoy | PBU | D.Robinson | deep_left |
| 9 | SF | J.McCoy | PBU | L.Farrell | short_left |
| 9 | SF | T.Stukes | INT | G.Kittle | deep_right |
| 9 | SF | E.Stokes | DPI | J.Cowing | short_left |
| 8 | NYJ | J.Chinn | INT | G.Wilson | deep_left |
| 8 | NYJ | H.Masses | PBU | M.Taylor | short_left |
| 8 | NYJ | E.Stokes | PBU | G.Wilson | deep_right |
| 8 | NYJ | T.Eichenberg | PBU | G.Wilson | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Eric Stokes | CB | 56.6 | 37.9 | 495.7 | 8.76 | 4.67 | 80 (51) |
| Taron Johnson | CB | 42.7 | 27.9 | 371.0 | 8.69 | 3.19 | 33 (13) |
| Nakobe Dean | LB | 35.1 | 27.9 | 253.2 | 7.21 | 1.95 | 38 (23) |
| Quay Walker | LB | 34.8 | 27.4 | 251.9 | 7.24 | 1.95 | 40 (21) |
| Jeremy Chinn | S | 34.2 | 24.6 | 284.3 | 8.31 | 2.97 | 32 (15) |
| Hezekiah Masses | CB | 30.1 | 18.1 | 295.2 | 9.81 | 2.47 | 34 (18) |
| Treydan Stukes | S | 29.8 | 18.8 | 279.4 | 9.38 | 1.76 | 12 (4) |
| Darien Porter | CB | 22.0 | 14.9 | 201.7 | 9.17 | 1.99 | 26 (12) |
| Jermod McCoy | CB | 14.6 | 8.8 | 160.3 | 10.98 | 0.79 | 18 (9) |
| Tommy Eichenberg | LB | 6.6 | 4.7 | 51.1 | 7.74 | 0.41 | 0 (0) |
| Isaiah Pola-Mao | S | 6.3 | 5.0 | 46.3 | 7.35 | 0.84 | 0 (0) |

### Upcoming: opposing receivers vs likely LV defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | CLE | K.Concepcion (WR) | 14 | short_left 40%, short_right 21% | Jermod McCoy (29%) | Taron Johnson (20%) |
| 12 | 2026-11-29 | CLE | D.Sampson (RB) | 12 | short_left 43%, short_right 30% | Nakobe Dean (34%) | Quay Walker (33%) |
| 12 | 2026-11-29 | CLE | H.Fannin (TE) | 11 | short_left 37%, short_right 34% | Jeremy Chinn (20%) | Treydan Stukes (18%) |
| 12 | 2026-11-29 | CLE | D.Boston (WR) | 9 | short_left 29%, short_right 23% | Jermod McCoy (28%) | Eric Stokes (21%) |

Defender pool = LV players with defensive snaps in their most recent game (2026_11_LV_DEN); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Jeremy Chinn | S | 63.2 | 43.0 | 581.3 | 9.2 | 9.02 | 300.5 | 8 |
| Treydan Stukes | S | 21.7 | 11.3 | 280.1 | 12.91 | 6.43 | 232.1 | 7 |
| Darien Porter | CB | 30.3 | 22.3 | 299.4 | 9.88 | 4.25 | 132.4 | 4 |
| Eric Stokes | CB | 36.4 | 23.2 | 304.7 | 8.37 | 3.96 | 119.0 | 5 |
| Taron Johnson | CB | 46.1 | 29.1 | 355.1 | 7.7 | 3.94 | 123.7 | 5 |
| Quay Walker | LB | 47.8 | 38.8 | 341.9 | 7.15 | 2.82 | 70.9 | 2 |
| Nakobe Dean | LB | 40.8 | 33.3 | 287.1 | 7.04 | 1.81 | 43.0 | 0 |
| Hezekiah Masses | CB | 13.5 | 7.9 | 140.8 | 10.43 | 1.45 | 71.2 | 3 |
| Jermod McCoy | CB | 9.4 | 5.8 | 85.8 | 9.13 | 1.32 | 35.1 | 1 |

### Rest of Week 12: receivers vs likely LV window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | CLE | K.Concepcion (WR) | 14 | 14% | Taron Johnson (29%, 3.94) | Jermod McCoy (22%, 1.32) |
| 2026-11-29 | CLE | D.Sampson (RB) | 12 | 0% | Quay Walker (56%, 2.82) | Nakobe Dean (19%, 1.81) |
| 2026-11-29 | CLE | H.Fannin (TE) | 11 | 6% | Jeremy Chinn (39%, 9.02) | Nakobe Dean (20%, 1.81) |
| 2026-11-29 | CLE | D.Boston (WR) | 9 | 24% | Taron Johnson (27%, 3.94) | Jermod McCoy (19%, 1.32) |
