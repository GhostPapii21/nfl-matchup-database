# NYJ defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 25.7 | 37.0 | — |
| Zone % | 64.5 | 63.0 | — |
| Single-high / MOFC % | 44.3 | 44.7 | — |
| Two-high / MOFO % | 49.7 | 55.3 | — |
| Blitz % | 36.1 | 39.1 | 36.6 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 40.1 / 29.1, 65.0 | — | — |

Sharp YPT allowed: WR 7.7, TE 8.1, RB 6.0, **outside 8.4 vs slot 7.5** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #3 vs StatRankings #13; blitz rank Sharp #5 vs SR #6 (raw gaps: man -11.3 pts, blitz -3.0 pts; Sharp man % runs lower than SR league-wide) → **CONFLICT FLAG (rank gap ≥8)**

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 15.3 | 117.0 | 7.66 | 12 | 0.273 | 29 |
| TE | 7.5 | 60.1 | 8.06 | 3 | 0.275 | 7 |
| RB | 4.4 | 26.2 | 6.0 | 4 | 0.256 | 26 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 15 | 5 | 118 | 1 | 1 | 7.87 | 11.46 | 27 |  |
| deep middle | 12 | 6 | 198 | 1 | 1 | 16.5 | 14.39 | 10 |  |
| deep right | 19 | 9 | 290 | 1 | 0 | 15.26 | 12.14 | 7 | **WEAK** |
| short left | 93 | 62 | 563 | 4 | 0 | 6.05 | 5.99 | 14 |  |
| short middle | 53 | 40 | 387 | 2 | 0 | 7.3 | 7.32 | 16 |  |
| short right | 106 | 78 | 680 | 10 | 0 | 6.42 | 6.02 | 10 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs NYJ: **3.21 yds** (league 2.93; rank 5/32 most allowed). WR 2.91, TE 3.98, cushion 5.23. Sample: 23 receiver-games, 162 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Azareye'h Thomas | CB | 11 | 100.0 (100.0 wk11) | 57 | 33 | 355 | 4 | 1 | 6.23 | 92.4 | 8.3 | 0 | 6 | 1 | 8 | 27 (247) | MISSING |
| Brandon Stephens | CB | 11 | 97.0 (100.0 wk11) | 56 | 29 | 403 | 4 | 0 | 7.20 | 99.0 | 9.3 | 0 | 5 | 2 | 7 | 19 (221) | MISSING |
| D'Angelo Ponds | CB | 9 | 21.3 (58.0 wk11) | 8 | 5 | 77 | 1 | 0 | 9.62 | 133.9 | 5.9 | 0 | 1 | 1 | 2 | 2 (8) | MISSING |
| Qwan'tez Stiggers | CB | 1 | 2.0 (2.0 wk7) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Jarvis Brownlee | DB | 8 | 53.1 (3.0 wk9) | 29 | 18 | 185 | 3 | 0 | 6.38 | 114.9 | 8.4 | 0 | 0 | 1 | 1 | 10 (92) | MISSING |
| Malachi Moore | DB | 5 | 21.6 (17.0 wk11) | 1 | 1 | 45 | 1 | 0 | 45.00 | 158.3 | 40.0 | 0 | 0 | 1 | 1 | 0 (0) | MISSING |
| Nahshon Wright | DB | 2 | 4.5 (5.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Dane Belton | S | 11 | 100.0 (100.0 wk11) | 37 | 18 | 211 | 0 | 0 | 5.70 | 66.4 | 8.4 | 0 | 5 | 0 | 5 | 31 (423) | MISSING |
| Minkah Fitzpatrick | S | 9 | 90.0 (100.0 wk11) | 22 | 12 | 232 | 2 | 1 | 10.55 | 102.8 | 10.8 | 1 | 2 | 0 | 3 | 13 (185) | MISSING |
| Andre Cisco | S | 7 | 45.9 (13.0 wk8) | 13 | 7 | 85 | 0 | 0 | 6.54 | 74.2 | 8.9 | 0 | 1 | 0 | 1 | 10 (130) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jamien Sherwood | 11 | 46 | 33 | 332 | 3 | 7.22 | 113.7 | 5 |
| Demario Davis | 11 | 37 | 28 | 254 | 1 | 6.86 | 102.8 | 4 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | LAC | A.Thomas | PBU | D.Njoku | short_right |
| 11 | LAC | D.Bailey | PBU | L.McConkey | short_left |
| 10 | BUF | A.Thomas | INT | G.Dortch | deep_left |
| 10 | BUF | D.Ponds | PBU | D.Knox | short_left |
| 10 | BUF | D.Belton | PBU | D.Kincaid | short_right |
| 10 | BUF | M.Moore | DPI | D.Kincaid | deep_left |
| 10 | BUF | D.Bailey | PBU | D.Knox | short_right |
| 10 | BUF | D.Bailey | PBU | K.Shakir | short_right |
| 8 | LV | J.Brownlee | DPI | T.Tucker | deep_middle |
| 8 | LV | M.Fitzpatrick | PBU | B.Bowers | deep_left |
| 8 | LV | D.Belton | PBU | M.Mayer | short_middle |
| 8 | LV | A.Thomas | PBU | B.Bowers | short_right |
| 7 | MIA | B.Stephens | PBU | C.Douglas | short_left |
| 7 | MIA | J.Sherwood | PBU | S.Traore | short_right |
| 7 | MIA | D.Davis | PBU | O.Gordon | short_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Azareye'h Thomas | CB | 62.9 | 43.8 | 446.4 | 7.1 | 4.84 | 96 (77) |
| Brandon Stephens | CB | 58.2 | 35.0 | 415.1 | 7.13 | 3.66 | 79 (68) |
| Jamien Sherwood | LB | 38.0 | 27.7 | 271.8 | 7.15 | 2.22 | 26 (25) |
| Demario Davis | LB | 36.4 | 26.5 | 252.0 | 6.92 | 2.66 | 28 (18) |
| Dane Belton | S | 33.9 | 23.6 | 292.5 | 8.63 | 1.91 | 35 (22) |
| Jarvis Brownlee Jr. | CB | 23.4 | 13.6 | 172.5 | 7.37 | 0.99 | 12 (7) |
| Minkah Fitzpatrick | S | 22.6 | 14.5 | 206.4 | 9.13 | 1.44 | 17 (9) |
| Andre Cisco | S | 9.4 | 6.8 | 78.7 | 8.37 | 0.22 | 5 (5) |
| D'Angelo Ponds | CB | 7.9 | 5.5 | 62.8 | 7.95 | 0.75 | 0 (0) |

### Upcoming: opposing receivers vs likely NYJ defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | MIA | C.Douglas (WR) | 26 | short_right 31%, short_left 22% | Brandon Stephens (25%) | Azareye'h Thomas (24%) |
| 12 | 2026-11-29 | MIA | G.Dulcich (TE) | 13 | short_right 41%, short_left 27% | Dane Belton (18%) | Minkah Fitzpatrick (18%) |
| 12 | 2026-11-29 | MIA | M.Washington (WR) | 12 | short_right 28%, short_left 28% | Brandon Stephens (29%) | Azareye'h Thomas (24%) |
| 12 | 2026-11-29 | MIA | O.Gordon (RB) | 9 | short_left 56%, short_right 28% | Demario Davis (34%) | Jamien Sherwood (33%) |

Defender pool = NYJ players with defensive snaps in their most recent game (2026_11_NYJ_LAC); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Dane Belton | S | 66.5 | 43.8 | 583.9 | 8.78 | 7.88 | 260.7 | 8 |
| Azareye'h Thomas | CB | 38.0 | 26.5 | 282.7 | 7.44 | 3.75 | 110.3 | 5 |
| Jarvis Brownlee Jr. | CB | 41.9 | 26.4 | 280.7 | 6.7 | 3.7 | 107.9 | 3 |
| Minkah Fitzpatrick | S | 9.5 | 5.6 | 124.0 | 13.05 | 3.23 | 99.1 | 4 |
| Brandon Stephens | CB | 33.8 | 20.1 | 231.5 | 6.85 | 2.74 | 86.3 | 3 |
| Demario Davis | LB | 52.9 | 37.7 | 345.6 | 6.53 | 2.52 | 80.1 | 1 |
| Jamien Sherwood | LB | 41.7 | 31.1 | 287.3 | 6.89 | 2.1 | 67.3 | 2 |
| D'Angelo Ponds | CB | 9.2 | 6.4 | 71.1 | 7.73 | 0.49 | 23.5 | 0 |

### Rest of Week 12: receivers vs likely NYJ window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | MIA | C.Douglas (WR) | 26 | 22% | D'Angelo Ponds (28%, 0.49) | Azareye'h Thomas (21%, 3.75) |
| 2026-11-29 | MIA | G.Dulcich (TE) | 13 | 10% | Dane Belton (45%, 7.88) | Demario Davis (17%, 2.52) |
| 2026-11-29 | MIA | M.Washington (WR) | 12 | 28% | D'Angelo Ponds (28%, 0.49) | Brandon Stephens (18%, 2.74) |
| 2026-11-29 | MIA | O.Gordon (RB) | 9 | 0% | Jamien Sherwood (56%, 2.1) | Demario Davis (19%, 2.52) |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Minkah Fitzpatrick (S) 22 tgt, 54.5% catch, 10.55 ypt, rating 102.8 [LIMITS CATCHES, GIVES UP EXPLOSIVES]
**Best / lockdown:** Dane Belton (S) 37 tgt, 48.6% catch, 5.7 ypt, rating 66.4 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS]
**Weak zones:** deep right 15.3 ypt

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Azareye'h Thomas | CB | 11 | 57 | 26% | 57.9 | 6.23 | 10.76 | 0.497 | 92.4 | 4 | 1 | 6 | 57.5 | LIMITS YARDS |  |
| Brandon Stephens | CB | 11 | 56 | 25% | 51.8 | 7.2 | 13.9 | 0.582 | 99.0 | 4 | 0 | 5 | 52.0 | LIMITS CATCHES, GIVES UP EXPLOSIVES |  |
| Jarvis Brownlee | CB | 8 | 29 | 16% | 62.1 | 6.38 | 10.28 | 0.67 | 114.9 | 3 | 0 | 0 | 49.5 |  | small sample (<35 tgts) |
| Dane Belton | S | 10 | 37 | 18% | 48.6 | 5.7 | 11.72 | 0.296 | 66.4 | 0 | 0 | 5 | 81.5 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS |  |
| Minkah Fitzpatrick | S | 8 | 22 | 14% | 54.5 | 10.55 | 19.33 | 0.426 | 102.8 | 2 | 1 | 2 | 39.5 | LIMITS CATCHES, GIVES UP EXPLOSIVES | small sample (<35 tgts) |
