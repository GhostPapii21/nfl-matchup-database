# PHI defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 17.5 | 39.5 | — |
| Zone % | 74.3 | 60.5 | — |
| Single-high / MOFC % | 52.2 | 57.7 | — |
| Two-high / MOFO % | 41.9 | 42.3 | — |
| Blitz % | 22.2 | 26.5 | 24.0 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 55.8 / 18.6, 73.0 | — | — |

Sharp YPT allowed: WR 8.1, TE 7.2, RB 3.8, **outside 8.3 vs slot 8.6** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #16 vs StatRankings #9; blitz rank Sharp #26 vs SR #25 (raw gaps: man -22.0 pts, blitz -4.3 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 21.9 | 182.2 | 8.32 | 12 | 0.254 | 2 |
| TE | 5.6 | 42.0 | 7.45 | 3 | 0.287 | 30 |
| RB | 4.6 | 18.4 | 3.96 | 1 | -0.007 | 31 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 25 | 11 | 266 | 2 | 1 | 10.64 | 11.46 | 17 |  |
| deep middle | 10 | 2 | 47 | 1 | 0 | 4.7 | 14.39 | 32 |  |
| deep right | 39 | 18 | 504 | 2 | 3 | 12.92 | 12.14 | 14 |  |
| short left | 99 | 72 | 598 | 1 | 0 | 6.04 | 5.99 | 16 |  |
| short middle | 73 | 55 | 605 | 4 | 0 | 8.29 | 7.32 | 6 | **WEAK** |
| short right | 108 | 71 | 648 | 6 | 0 | 6.0 | 6.02 | 16 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs PHI: **2.65 yds** (league 2.93; rank 28/32 most allowed). WR 2.58, TE 3.26, cushion 6.58. Sample: 24 receiver-games, 185 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Quinyon Mitchell | CB | 11 | 92.4 (100.0 wk12) | 59 | 31 | 337 | 1 | 1 | 5.71 | 68.3 | 10.1 | 0 | 10 | 2 | 13 | 28 (279) | MISSING |
| Riq Woolen | CB | 10 | 94.7 (100.0 wk12) | 55 | 33 | 464 | 3 | 0 | 8.44 | 105.4 | 14.2 | 2 | 8 | 2 | 10 | 27 (351) | MISSING |
| Jonathan Jones | CB | 6 | 20.5 (49.0 wk11) | 16 | 8 | 69 | 0 | 0 | 4.31 | 61.7 | 10.3 | 0 | 4 | 0 | 4 | 8 (69) | MISSING |
| Kelee Ringo | CB | 2 | 6.5 (10.0 wk11) | 1 | 1 | 20 | 1 | 0 | 20.00 | 158.3 | 20.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Mac McWilliams | CB | 2 | 4.5 (5.0 wk12) | 1 | 0 | 0 | 0 | 0 | 0.00 | 39.6 | 1.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Cooper DeJean | DB | 11 | 90.9 (5.0 wk12) | 51 | 29 | 323 | 4 | 1 | 6.33 | 93.8 | 7.1 | 0 | 5 | 1 | 7 | 24 (226) | MISSING |
| Kenny Moore | DB | 7 | 40.3 (36.0 wk12) | 9 | 7 | 130 | 1 | 0 | 14.44 | 155.8 | 13.3 | 0 | 0 | 0 | 0 | 10 (207) | MISSING |
| Michael Carter II | DB | 8 | 29.6 (51.0 wk12) | 9 | 4 | 22 | 0 | 0 | 2.44 | 51.6 | 11.6 | 0 | 2 | 0 | 2 | 5 (49) | MISSING |
| Andrew Mukuba | S | 11 | 99.6 (100.0 wk12) | 33 | 20 | 329 | 4 | 1 | 9.97 | 121.1 | 14.7 | 1 | 2 | 0 | 4 | 23 (323) | MISSING |
| Marcus Epps | S | 7 | 58.9 (55.0 wk12) | 18 | 13 | 159 | 0 | 0 | 8.83 | 99.1 | 5.6 | 0 | 1 | 0 | 1 | 16 (192) | MISSING |
| Cole Wisniewski | S | 1 | 10.0 (10.0 wk12) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 1 (15) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Jihaad Campbell | 9 | 31 | 19 | 216 | 0 | 6.97 | 82.2 | 1 |
| Zack Baun | 8 | 31 | 19 | 182 | 0 | 5.87 | 77.6 | 5 |
| Jeremiah Trotter Jr. | 8 | 22 | 17 | 134 | 0 | 6.09 | 91.9 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 12 | DAL | A.Mukuba | INT | G.Pickens | deep_left |
| 12 | DAL | Q.Mitchell | DPI | C.Lamb | deep_right |
| 12 | DAL | T.Woolen | DPI | G.Pickens | short_left |
| 12 | DAL | J.Campbell | PBU | C.Lamb | deep_left |
| 12 | DAL | Q.Mitchell | DPI | G.Pickens | deep_middle |
| 11 | PIT | A.Mukuba | PBU | G.Bernard | deep_right |
| 11 | PIT | J.Jones | PBU | M.Hurleman | deep_right |
| 11 | PIT | J.Jones | PBU | R.Wilson | short_left |
| 11 | PIT | Q.Mitchell | PBU | D.Metcalf | deep_left |
| 11 | PIT | Q.Mitchell | PBU | D.Metcalf | deep_left |
| 11 | PIT | J.Jones | PBU | R.Wilson | short_right |
| 11 | PIT | C.DeJean | PBU | G.Bernard | short_middle |
| 9 | NYG | Q.Mitchell | PBU | M.Nabers | deep_left |
| 9 | NYG | T.Woolen | PBU | M.Fields | short_right |
| 9 | NYG | T.Woolen | PBU | M.Fields | deep_left |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Quinyon Mitchell | CB | 62.7 | 38.4 | 492.5 | 7.85 | 2.78 | 88 (44) |
| Riq Woolen | CB | 57.5 | 34.9 | 528.1 | 9.18 | 3.19 | 83 (57) |
| Cooper DeJean | CB | 54.5 | 34.0 | 401.7 | 7.37 | 2.61 | 57 (31) |
| Andrew Mukuba | S | 26.8 | 17.2 | 227.3 | 8.48 | 1.6 | 15 (4) |
| Jihaad Campbell | LB | 22.6 | 15.9 | 161.8 | 7.16 | 0.8 | 14 (1) |
| Jeremiah Trotter Jr. | LB | 19.8 | 15.4 | 124.3 | 6.28 | 0.64 | 35 (6) |
| Zack Baun | LB | 17.3 | 11.9 | 105.6 | 6.1 | 0.66 | 15 (4) |
| Nolan Smith | LB | 14.6 | 9.8 | 84.0 | 5.75 | 0.58 | 5 (0) |
| Kenny Moore II | CB | 14.3 | 8.7 | 131.9 | 9.22 | 0.79 | 9 (0) |
| Michael Carter II | CB | 13.0 | 7.3 | 94.4 | 7.26 | 0.45 | 9 (2) |
| Jalyx Hunt | LB | 12.2 | 9.0 | 72.0 | 5.9 | 0.36 | 2 (0) |
| Marcus Epps | S | 9.8 | 6.7 | 69.0 | 7.04 | 0.44 | 10 (0) |

### Upcoming: opposing receivers vs likely PHI defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 13 | 2026-12-06 | ARI | T.McBride (TE) | 27 | short_right 50%, short_left 24% | Andrew Mukuba (13%) | Riq Woolen (12%) |
| 13 | 2026-12-06 | ARI | S.Fehoko (WR) | 8 | short_right 44%, deep_right 33% | Riq Woolen (37%) | Quinyon Mitchell (15%) |
| 13 | 2026-12-06 | ARI | H.Wallace (WR) | 8 | short_left 38%, short_right 25% | Quinyon Mitchell (26%) | Riq Woolen (22%) |
| 13 | 2026-12-06 | ARI | Mi.Wilson (WR) | 7 | short_right 41%, deep_right 19% | Riq Woolen (28%) | Quinyon Mitchell (21%) |

Defender pool = PHI players with defensive snaps in their most recent game (2026_12_PHI_DAL); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Riq Woolen | CB | 62.1 | 40.3 | 567.4 | 9.14 | 10.32 | 302.8 | 13 |
| Andrew Mukuba | S | 43.4 | 25.4 | 378.7 | 8.73 | 6.63 | 176.7 | 4 |
| Quinyon Mitchell | CB | 43.6 | 26.4 | 339.5 | 7.79 | 5.78 | 165.4 | 8 |
| Cooper DeJean | CB | 39.9 | 22.6 | 317.7 | 7.96 | 5.39 | 160.1 | 7 |
| Marcus Epps | S | 40.1 | 26.4 | 310.1 | 7.73 | 4.65 | 138.3 | 3 |
| Zack Baun | LB | 35.0 | 22.8 | 202.5 | 5.79 | 1.77 | 49.1 | 3 |
| Jihaad Campbell | LB | 30.6 | 22.4 | 186.7 | 6.1 | 1.55 | 49.4 | 0 |
| Michael Carter II | CB | 15.6 | 10.0 | 122.3 | 7.84 | 1.31 | 39.1 | 0 |
| Arnold Ebiketie | LB | 5.4 | 3.0 | 29.5 | 5.46 | 0.29 | 8.2 | 0 |
| Jeremiah Trotter Jr. | LB | 35.9 | 27.9 | 200.6 | 5.59 | 0.25 | 6.0 | 0 |
