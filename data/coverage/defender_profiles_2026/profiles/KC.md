# KC defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 18.8 | 43.0 | — |
| Zone % | 77.3 | 55.9 | — |
| Single-high / MOFC % | 39.5 | 47.5 | — |
| Two-high / MOFO % | 57.1 | 52.5 | — |
| Blitz % | 26.4 | 28.3 | 26.5 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 42.0 / 23.5, 70.0 | — | — |

Sharp YPT allowed: WR 6.6, TE 6.6, RB 6.5, **outside 6.7 vs slot 7.8** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #14 vs StatRankings #7; blitz rank Sharp #20 vs SR #22 (raw gaps: man -24.2 pts, blitz -1.9 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 17.6 | 113.1 | 6.41 | 3 | -0.133 | 30 |
| TE | 9.2 | 59.9 | 6.52 | 5 | 0.06 | 8 |
| RB | 5.5 | 34.8 | 6.38 | 0 | 0.102 | 13 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 27 | 11 | 329 | 3 | 0 | 12.19 | 11.46 | 16 |  |
| deep middle | 17 | 6 | 192 | 0 | 2 | 11.29 | 14.39 | 25 |  |
| deep right | 12 | 2 | 37 | 1 | 0 | 3.08 | 12.14 | 32 |  |
| short left | 103 | 68 | 563 | 0 | 3 | 5.47 | 5.99 | 24 |  |
| short middle | 72 | 49 | 509 | 1 | 1 | 7.07 | 7.32 | 20 |  |
| short right | 124 | 85 | 656 | 3 | 3 | 5.29 | 6.02 | 28 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs KC: **2.9 yds** (league 2.93; rank 20/32 most allowed). WR 2.74, TE 3.19, cushion 5.4. Sample: 28 receiver-games, 213 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mansoor Delane | CB | 8 | 74.2 (67.0 wk12) | 31 | 18 | 255 | 2 | 1 | 8.23 | 92.8 | 13.3 | 2 | 6 | 0 | 7 | 15 (197) | MISSING |
| Christian Roland-Wallace | CB | 11 | 46.7 (64.0 wk12) | 21 | 18 | 134 | 1 | 0 | 6.38 | 109.1 | 3.1 | 0 | 2 | 0 | 2 | 14 (111) | MISSING |
| Kristian Fulton | CB | 10 | 54.0 (32.0 wk12) | 27 | 12 | 123 | 0 | 1 | 4.56 | 42.7 | 7.0 | 0 | 2 | 4 | 7 | 10 (86) | MISSING |
| L'Jarius Sneed | CB | 6 | 63.7 (20.0 wk7) | 43 | 34 | 341 | 1 | 0 | 7.93 | 107.5 | 6.4 | 3 | 3 | 0 | 3 | 24 (213) | MISSING |
| Nohl Williams | DB | 11 | 92.9 (100.0 wk12) | 56 | 25 | 254 | 2 | 2 | 4.54 | 55.2 | 9.5 | 1 | 11 | 0 | 14 | 22 (258) | MISSING |
| Chamarri Conner | DB | 8 | 92.6 (100.0 wk12) | 20 | 13 | 202 | 0 | 0 | 10.10 | 98.3 | 4.9 | 1 | 2 | 1 | 3 | 14 (188) | MISSING |
| Jaden Hicks | DB | 11 | 49.8 (16.0 wk12) | 18 | 10 | 172 | 1 | 0 | 9.56 | 106.7 | 16.8 | 0 | 1 | 0 | 1 | 12 (128) | MISSING |
| Jadon Canady | DB | 6 | 14.5 (13.0 wk12) | 12 | 8 | 108 | 0 | 0 | 9.00 | 95.1 | 10.2 | 0 | 1 | 0 | 1 | 7 (111) | MISSING |
| Alohi Gilman | S | 11 | 81.7 (84.0 wk12) | 15 | 8 | 93 | 1 | 0 | 6.20 | 94.6 | 11.6 | 0 | 1 | 1 | 3 | 14 (212) | MISSING |
| Xavier Nwankpa | S | 6 | 4.2 (7.0 wk12) | 2 | 1 | 8 | 0 | 1 | 4.00 | 20.8 | 8.5 | 0 | 0 | 0 | 1 | 2 (18) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Drue Tranquill | 11 | 33 | 20 | 191 | 0 | 5.79 | 76.7 | 2 |
| Nick Bolton | 11 | 31 | 21 | 183 | 0 | 5.90 | 83.1 | 3 |
| Jack Cochrane | 11 | 11 | 5 | 58 | 0 | 5.27 | 24.1 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | BUF | N.Williams | INT | K.Shakir | short_right |
| 12 | BUF | A.Gilman | INT | D.Knox | short_left |
| 11 | ARI | K.Fulton | PBU | S.Fehoko | short_right |
| 11 | ARI | C.Jones | PBU | T.McBride | short_right |
| 11 | ARI | N.Williams | PBU | H.Wallace | deep_right |
| 11 | ARI | N.Williams | PBU | S.Fehoko | deep_right |
| 11 | ARI | N.Bolton | PBU | H.Wallace | short_left |
| 10 | ATL | K.Fulton | PBU | C.Blair | short_left |
| 10 | ATL | N.Williams | INT | C.Blair | deep_middle |
| 10 | ATL | J.Canady | PBU | D.London | short_middle |
| 10 | ATL | A.Gillotte | PBU | D.London | short_middle |
| 10 | ATL | M.Delane | PBU | J.Dotson | short_left |
| 10 | ATL | C.Conner | DPI | D.London | deep_right |
| 10 | ATL | N.Williams | PBU | D.London | short_left |
| 10 | ATL | G.Karlaftis | PBU | D.London | short_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Nohl Williams | CB | 60.0 | 34.0 | 346.3 | 5.77 | 1.5 | 99 (48) |
| Nick Bolton | LB | 43.2 | 32.0 | 274.6 | 6.36 | 0.87 | 57 (26) |
| Mansoor Delane | CB | 36.8 | 20.3 | 288.1 | 7.83 | 0.91 | 57 (24) |
| Drue Tranquill | LB | 36.0 | 26.4 | 214.8 | 5.97 | 0.38 | 42 (18) |
| Chamarri Conner | CB | 36.0 | 20.5 | 252.8 | 7.02 | 0.93 | 30 (3) |
| Kristian Fulton | CB | 27.1 | 14.8 | 157.9 | 5.83 | 0.94 | 20 (12) |
| L'Jarius Sneed | CB | 25.5 | 17.3 | 167.4 | 6.56 | 0.32 | 23 (13) |
| Jaden Hicks | CB | 25.5 | 14.8 | 169.9 | 6.66 | 0.62 | 9 (4) |
| Christian Roland-Wallace | CB | 24.0 | 14.3 | 139.0 | 5.79 | 0.52 | 9 (1) |
| Alohi Gilman | S | 23.7 | 15.3 | 162.1 | 6.84 | 0.78 | 9 (2) |
| Jack Cochrane | LB | 8.4 | 6.0 | 53.0 | 6.31 | 0.12 | 0 (0) |
| Jadon Canady | CB | 5.0 | 2.6 | 37.7 | 7.54 | 0.06 | 0 (0) |

### Upcoming: opposing receivers vs likely KC defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-03 | LA | P.Nacua (WR) | 19 | short_left 32%, short_right 29% | Nohl Williams (22%) | Chamarri Conner (22%) |
| 13 | 2026-12-03 | LA | K.Williams (RB) | 14 | short_right 45%, short_left 39% | Nick Bolton (29%) | Drue Tranquill (27%) |
| 13 | 2026-12-03 | LA | T.Higbee (TE) | 12 | short_right 52%, short_left 20% | Nohl Williams (17%) | Alohi Gilman (16%) |
| 13 | 2026-12-03 | LA | K.Mumpfield (WR) | 11 | short_middle 25%, deep_right 25% | Chamarri Conner (23%) | Nohl Williams (22%) |

Defender pool = KC players with defensive snaps in their most recent game (2026_12_KC_BUF); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Alohi Gilman | S | 68.2 | 42.2 | 492.9 | 7.23 | 7.45 | 211.2 | 5 |
| Mansoor Delane | CB | 28.2 | 15.4 | 222.3 | 7.88 | 4.96 | 150.9 | 7 |
| Christian Roland-Wallace | CB | 36.6 | 20.2 | 234.9 | 6.42 | 3.52 | 105.9 | 6 |
| Chamarri Conner | S | 18.3 | 9.3 | 138.5 | 7.57 | 3.4 | 95.1 | 3 |
| L'Jarius Sneed | CB | 35.7 | 22.3 | 224.9 | 6.3 | 1.92 | 70.7 | 2 |
| Nick Bolton | LB | 72.7 | 51.9 | 414.4 | 5.7 | 1.87 | 58.6 | 1 |
| Drue Tranquill | LB | 40.7 | 28.9 | 266.5 | 6.55 | 1.6 | 55.4 | 1 |
| Jaden Hicks | S | 6.6 | 4.0 | 66.3 | 10.05 | 0.86 | 38.8 | 1 |
| Kristian Fulton | CB | 11.8 | 6.3 | 56.1 | 4.75 | 0.73 | 16.5 | 1 |
| Nohl Williams | CB | 36.0 | 20.6 | 169.2 | 4.7 | 0.67 | 22.9 | 0 |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** L'Jarius Sneed (CB) 43 tgt, 79.1% catch, 7.93 ypt, rating 107.5 [TARGET MAGNET]
**Best / lockdown:** Kristian Fulton (CB) 27 tgt, 44.4% catch, 4.56 ypt, rating 42.7 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS]
**Weak zones:** none flagged

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kristian Fulton | CB | 8 | 27 | 14% | 44.4 | 4.56 | 10.25 | 0.389 | 42.7 | 0 | 1 | 2 | 94.8 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS | small sample (<35 tgts) |
| Nohl Williams | CB | 10 | 56 | 23% | 44.6 | 4.54 | 10.16 | 0.416 | 55.2 | 2 | 2 | 11 | 90.0 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS |  |
| Mansoor Delane | CB | 7 | 31 | 17% | 58.1 | 8.23 | 14.17 | 0.689 | 92.8 | 2 | 1 | 6 | 45.2 | GIVES UP EXPLOSIVES | small sample (<35 tgts) |
| Christian Roland-Wallace | CB | 10 | 21 | 9% | 85.7 | 6.38 | 7.44 | 0.451 | 109.1 | 1 | 0 | 2 | 44.2 |  | small sample (<35 tgts) |
| L'Jarius Sneed | CB | 6 | 43 | 30% | 79.1 | 7.93 | 10.03 | 1.322 | 107.5 | 1 | 0 | 3 | 15.0 | TARGET MAGNET |  |
| Chamarri Conner | S | 7 | 20 | 11% | 65.0 | 10.1 | 15.54 | 0.467 | 98.3 | 0 | 0 | 2 | 32.2 |  | small sample (<35 tgts) |
