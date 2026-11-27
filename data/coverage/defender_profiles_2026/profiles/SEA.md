# SEA defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 9.8 | 20.7 | — |
| Zone % | 85.4 | 79.3 | — |
| Single-high / MOFC % | 41.2 | 43.0 | — |
| Two-high / MOFO % | 56.9 | 57.0 | — |
| Blitz % | 22.1 | 24.9 | 24.0 (dropbacks with 1+ blitzer, thru wk 10) |
| Light / heavy box %, sub package % | 48.8 / 17.8, 89.0 | — | — |

Sharp YPT allowed: WR 5.9, TE 5.9, RB 5.1, **outside 7.3 vs slot 4.2** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #30 vs StatRankings #30; blitz rank Sharp #27 vs SR #28 (raw gaps: man -10.9 pts, blitz -2.8 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 15.9 | 93.6 | 5.89 | 5 | -0.002 | 32 |
| TE | 7.2 | 42.6 | 5.92 | 2 | 0.09 | 28 |
| RB | 5.9 | 30.0 | 5.08 | 2 | 0.095 | 21 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 19 | 6 | 140 | 1 | 2 | 7.37 | 11.46 | 29 |  |
| deep middle | 12 | 7 | 148 | 0 | 1 | 12.33 | 14.39 | 22 |  |
| deep right | 25 | 5 | 134 | 0 | 1 | 5.36 | 12.14 | 31 |  |
| short left | 80 | 63 | 439 | 4 | 2 | 5.49 | 5.99 | 23 |  |
| short middle | 50 | 37 | 321 | 3 | 1 | 6.42 | 7.32 | 28 |  |
| short right | 105 | 77 | 480 | 1 | 1 | 4.57 | 6.02 | 32 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs SEA: **3.24 yds** (league 2.93; rank 4/32 most allowed). WR 3.21, TE 3.29, cushion 5.23. Sample: 19 receiver-games, 141 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Devon Witherspoon | CB | 10 | 98.9 (100.0 wk10) | 54 | 34 | 254 | 0 | 0 | 4.70 | 74.2 | 6.7 | 0 | 3 | 1 | 4 | 33 (245) | MISSING |
| Josh Jobe | CB | 10 | 98.8 (98.0 wk10) | 46 | 33 | 286 | 2 | 1 | 6.22 | 93.2 | 8.5 | 1 | 1 | 4 | 6 | 22 (169) | MISSING |
| Nehemiah Pritchett | CB | 10 | 33.4 (20.0 wk10) | 21 | 9 | 124 | 0 | 2 | 5.90 | 22.8 | 14.3 | 0 | 3 | 1 | 6 | 6 (60) | MISSING |
| Trevon Diggs | CB | 5 | 11.8 (15.0 wk10) | 1 | 1 | 6 | 0 | 0 | 6.00 | 91.7 | 6.0 | 0 | 0 | 0 | 0 | 1 (6) | MISSING |
| Julian Neal | CB | 1 | 4.0 (4.0 wk2) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Julian Love | S | 9 | 98.6 (100.0 wk10) | 26 | 14 | 169 | 0 | 2 | 6.50 | 42.0 | 11.2 | 0 | 5 | 0 | 7 | 20 (231) | MISSING |
| Nick Emmanwori | S | 9 | 80.8 (97.0 wk10) | 30 | 18 | 163 | 1 | 0 | 5.43 | 85.8 | 4.7 | 0 | 3 | 0 | 3 | 9 (70) | MISSING |
| Ty Okada | S | 6 | 98.5 (100.0 wk10) | 13 | 6 | 60 | 1 | 1 | 4.62 | 53.4 | 12.9 | 0 | 1 | 0 | 2 | 12 (128) | MISSING |
| Rodney Thomas II | S | 7 | 58.4 (2.0 wk9) | 14 | 7 | 62 | 0 | 0 | 4.43 | 62.2 | 13.0 | 0 | 2 | 1 | 3 | 6 (97) | MISSING |
| AJ Finley | S | 2 | 52.0 (100.0 wk3) | 4 | 3 | 31 | 1 | 0 | 7.75 | 136.5 | 12.3 | 0 | 0 | 0 | 0 | 2 (23) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Ernest Jones | 10 | 54 | 36 | 307 | 0 | 5.69 | 73.6 | 4 |
| Drake Thomas | 8 | 26 | 17 | 127 | 1 | 4.88 | 73.7 | 0 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 10 | LV | N.Emmanwori | PBU | J.Bech | short_left |
| 10 | LV | J.Love | PBU | J.Bech | short_middle |
| 9 | ARI | N.Emmanwori | PBU | T.McBride | short_right |
| 9 | ARI | J.Jobe | DPI | — | deep_right |
| 9 | ARI | T.Okada | PBU | R.Virgil | deep_middle |
| 9 | ARI | J.Jobe | PBU | E.Hull | short_right |
| 9 | ARI | E.Jones | PBU | R.Virgil | deep_right |
| 8 | CHI | E.Jones | PBU | L.Burden | short_middle |
| 8 | CHI | D.Lawrence | PBU | Z.Thomas | deep_right |
| 8 | CHI | N.Pritchett | PBU | R.Odunze | deep_middle |
| 7 | KC | L.Williams | PBU | C.Allen | short_middle |
| 7 | KC | T.Okada | INT | J.Royals | short_left |
| 6 | DEN | U.Nwosu | PBU | R.Harvey | short_right |
| 6 | DEN | D.Witherspoon | DPI | C.Sutton | deep_left |
| 6 | DEN | D.Witherspoon | PBU | J.Waddle | deep_right |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Devon Witherspoon | CB | 52.5 | 32.8 | 284.9 | 5.43 | 1.3 | 72 (28) |
| Josh Jobe | CB | 52.0 | 31.3 | 317.1 | 6.1 | 1.91 | 83 (41) |
| Ernest Jones | LB | 34.5 | 25.9 | 190.9 | 5.53 | 1.22 | 62 (14) |
| Julian Love | S | 23.5 | 15.5 | 148.9 | 6.34 | 0.58 | 18 (0) |
| Drake Thomas | LB | 19.2 | 15.2 | 105.3 | 5.48 | 0.79 | 14 (1) |
| DeMarcus Lawrence | LB | 16.4 | 10.8 | 87.8 | 5.35 | 0.49 | 8 (0) |
| Nehemiah Pritchett | CB | 15.9 | 10.2 | 89.5 | 5.63 | 0.57 | 9 (7) |
| Nick Emmanwori | S | 14.6 | 10.3 | 85.5 | 5.86 | 0.26 | 5 (0) |
| Derick Hall | LB | 13.8 | 10.5 | 68.2 | 4.94 | 0.37 | 6 (0) |
| Ty Okada | S | 13.4 | 9.0 | 93.4 | 6.97 | 0.15 | 2 (1) |
| Uchenna Nwosu | LB | 10.0 | 7.6 | 51.7 | 5.17 | 0.35 | 0 (0) |
| Rodney Thomas | S | 9.3 | 4.9 | 58.6 | 6.3 | 0.56 | 3 (2) |

### Upcoming: opposing receivers vs likely SEA defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | SF | G.Kittle (TE) | 19 | short_left 37%, short_middle 25% | Nick Emmanwori (14%) | Ty Okada (14%) |
| 12 | 2026-11-29 | SF | K.Allen (WR) | 11 | short_left 36%, short_right 32% | Devon Witherspoon (25%) | Josh Jobe (24%) |
| 12 | 2026-11-29 | SF | C.McCaffrey (RB) | 10 | short_left 46%, short_right 37% | Ernest Jones (20%) | Drake Thomas (15%) |
| 12 | 2026-11-29 | SF | J.Watkins (WR) | 8 | deep_left 24%, deep_middle 24% | Josh Jobe (26%) | Devon Witherspoon (22%) |
| 13 | 2026-12-07 | DAL | C.Lamb (WR) | 51 | short_right 36%, short_left 24% | Devon Witherspoon (26%) | Josh Jobe (25%) |
| 13 | 2026-12-07 | DAL | G.Pickens (WR) | 37 | short_left 35%, short_right 28% | Josh Jobe (28%) | Devon Witherspoon (25%) |
| 13 | 2026-12-07 | DAL | J.Williams (RB) | 12 | short_right 44%, short_left 33% | Ernest Jones (21%) | Drake Thomas (14%) |
| 13 | 2026-12-07 | DAL | R.Flournoy (WR) | 11 | short_left 42%, short_middle 22% | Josh Jobe (25%) | Devon Witherspoon (23%) |

Defender pool = SEA players with defensive snaps in their most recent game (2026_10_SEA_LV); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Ty Okada | S | 56.5 | 36.8 | 345.5 | 6.12 | 3.56 | 83.6 | 4 |
| Josh Jobe | CB | 31.5 | 20.5 | 194.0 | 6.16 | 3.25 | 79.5 | 1 |
| Julian Love | S | 28.9 | 15.4 | 163.3 | 5.65 | 2.6 | 62.8 | 5 |
| Ernest Jones | LB | 65.1 | 50.6 | 391.8 | 6.02 | 2.08 | 59.9 | 2 |
| Devon Witherspoon | CB | 37.1 | 22.2 | 172.0 | 4.64 | 1.62 | 45.5 | 1 |
| Rodney Thomas | S | 6.1 | 2.5 | 55.5 | 9.1 | 1.31 | 44.4 | 2 |
| Drake Thomas | LB | 34.7 | 25.9 | 169.3 | 4.88 | 0.6 | 14.9 | 0 |
| Nehemiah Pritchett | CB | 16.7 | 11.4 | 90.4 | 5.41 | 0.37 | 8.3 | 0 |
| Tyrice Knight | LB | 9.7 | 7.1 | 48.9 | 5.04 | 0.0 | 0.0 | 0 |

### Rest of Week 12: receivers vs likely SEA window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | SF | G.Kittle (TE) | 19 | 6% | Ty Okada (48%, 3.56) | Ernest Jones (22%, 2.08) |
| 2026-11-29 | SF | K.Allen (WR) | 11 | 7% | Ty Okada (37%, 3.56) | Devon Witherspoon (15%, 1.62) |
| 2026-11-29 | SF | C.McCaffrey (RB) | 10 | 0% | Ernest Jones (44%, 2.08) | Drake Thomas (24%, 0.6) |
| 2026-11-29 | SF | J.Watkins (WR) | 8 | 29% | Ty Okada (37%, 3.56) | Josh Jobe (17%, 3.25) |

<!-- DEFENDER-GRADES -->
## Defender quality grades (CB/S with 20+ charted targets)

PFR charted (weekly via nflverse) + pbp PBU. Percentiles vs his position league-wide (100 = best). Labels: see GRADES.md.

**Weakest link:** Josh Jobe (CB) 46 tgt, 71.7% catch, 6.22 ypt, rating 93.2 [LIMITS YARDS]
**Best / lockdown:** Nehemiah Pritchett (CB) 21 tgt, 42.9% catch, 5.9 ypt, rating 22.8 [LOCKDOWN, LIMITS CATCHES, LIMITS YARDS, GIVES UP EXPLOSIVES]
**Weak zones:** none flagged

| Player | Pos | G | Tgt | Tgt share | Catch % | YPT | Yds/cmp | Yds/snap | Rating | TD | INT | PBU | Composite | Labels | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nehemiah Pritchett | CB | 9 | 21 | 11% | 42.9 | 5.9 | 13.78 | 0.599 | 22.8 | 0 | 2 | 3 | 92.2 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS, GIVES UP EXPLOSIVES | small sample (<35 tgts) |
| Devon Witherspoon | CB | 10 | 54 | 26% | 63.0 | 4.7 | 7.47 | 0.416 | 74.2 | 0 | 0 | 3 | 69.2 | LIMITS YARDS |  |
| Josh Jobe | CB | 10 | 46 | 22% | 71.7 | 6.22 | 8.67 | 0.47 | 93.2 | 2 | 1 | 1 | 48.8 | LIMITS YARDS |  |
| Julian Love | S | 9 | 26 | 14% | 53.8 | 6.5 | 12.07 | 0.314 | 42.0 | 0 | 2 | 5 | 82.5 | LOCKDOWN, LIMITS CATCHES, LIMITS YARDS | small sample (<35 tgts) |
| Nick Emmanwori | S | 9 | 30 | 16% | 60.0 | 5.43 | 9.06 | 0.369 | 85.8 | 1 | 0 | 3 | 71.2 | LIMITS YARDS | small sample (<35 tgts) |
