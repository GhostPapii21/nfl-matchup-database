# MIN defense — coverage profile (2026, research only)

Built from free/public sources. nflverse pbp through week 12 (last game 2026-11-26); PFR charted coverage through week 11; NGS through week 12; FTN charting through week 11. nflverse pulled 2026-11-27T12:26:11Z.

Labels: **PFR_charted** = targets charged by PFR charters to nearest defender (not an assignment). **verified** = named in pbp on a PBU, INT or DPI. **inferred** = tackler after the catch only. Slot vs outside alignment per defender = **MISSING** (no free source).

## Scheme rates (two charting sources; do not mix on one slip)

| Metric | Sharp | StatRankings | FTN via nflverse |
|---|---|---|---|
| Man % | 4.9 | 24.4 | — |
| Zone % | 86.7 | 75.3 | — |
| Single-high / MOFC % | 28.0 | 40.3 | — |
| Two-high / MOFO % | 65.8 | 59.7 | — |
| Blitz % | 69.6 | 74.7 | 72.3 (dropbacks with 1+ blitzer, thru wk 11) |
| Light / heavy box %, sub package % | 22.2 / 41.4, 31.0 | — | — |

Sharp YPT allowed: WR 7.9, TE 6.9, RB 4.8, **outside 7.8 vs slot 9.0** (team-level alignment split; the only free slot/outside number).
Sharp as of Sharp pages 'Updated: November 24' 2026 (pulled 2026-11-27T12:26:33Z); StatRankings as of ranking pages last updated 2026-11-26T00:02:20Z (pulled 2026-11-27T12:27:16Z).
Source check: man rank Sharp #32 vs StatRankings #26; blitz rank Sharp #1 vs SR #1 (raw gaps: man -19.5 pts, blitz -5.1 pts; Sharp man % runs lower than SR league-wide) → ranks agree (gap <8)

## Allowed by receiver position (nflverse pbp)

| Pos | Tgt/g | Yds/g | YPT | TD | EPA/tgt | Yds/g rank (1=most) |
|---|---|---|---|---|---|---|
| WR | 16.7 | 131.1 | 7.85 | 6 | 0.174 | 27 |
| TE | 6.3 | 43.6 | 6.92 | 3 | 0.04 | 27 |
| RB | 4.6 | 22.6 | 4.91 | 0 | -0.088 | 29 |

## Zones: depth × direction (nflverse pbp; direction is offense's left/middle/right)

| Zone | Tgt | Cmp | Yds | TD | INT | YPT | Lg YPT | YPT rank (1=most) | Weak? |
|---|---|---|---|---|---|---|---|---|---|
| deep left | 13 | 4 | 115 | 0 | 1 | 8.85 | 11.46 | 25 |  |
| deep middle | 17 | 8 | 307 | 2 | 3 | 18.06 | 14.39 | 4 | **WEAK** |
| deep right | 15 | 6 | 158 | 2 | 0 | 10.53 | 12.14 | 21 |  |
| short left | 80 | 58 | 503 | 1 | 1 | 6.29 | 5.99 | 12 |  |
| short middle | 53 | 30 | 308 | 2 | 1 | 5.81 | 7.32 | 31 |  |
| short right | 98 | 69 | 582 | 2 | 3 | 5.94 | 6.02 | 19 |  |

Weak = top-8 most YPT allowed in that zone league-wide with 12+ targets.

## NGS separation allowed (proxy)

Target-weighted avg separation of NGS-qualified receivers vs MIN: **3.3 yds** (league 2.93; rank 3/32 most allowed). WR 3.23, TE 3.55, cushion 6.65. Sample: 21 receiver-games, 138 targets. NGS publishes separation per receiver, not per defender; this is a receiver-side proxy.

## Every CB and S (PFR charted + pbp verified/inferred)

| Player | Pos | G | Snap% (last) | Tgt | Cmp | Yds | TD | INT | YPT | Rtg (computed) | aDOT | 70+ yd games | PBU | DPI | Verified plays | Tackle-after-catch (yds) | Align |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Byron Murphy | CB | 10 | 87.3 (83.0 wk11) | 51 | 34 | 385 | 1 | 4 | 7.55 | 62.9 | 9.7 | 2 | 4 | 0 | 8 | 27 (303) | MISSING |
| Isaiah Rodgers | CB | 9 | 83.2 (80.0 wk10) | 35 | 16 | 211 | 0 | 1 | 6.03 | 53.4 | 11.9 | 0 | 4 | 0 | 4 | 17 (185) | MISSING |
| James Pierre | CB | 10 | 47.7 (81.0 wk11) | 29 | 14 | 133 | 0 | 2 | 4.59 | 32.7 | 9.5 | 0 | 3 | 0 | 5 | 19 (180) | MISSING |
| Charles Demmings | CB | 2 | 14.5 (26.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Zemaiah Vaughn | CB | 3 | 7.7 (11.0 wk11) | 1 | 1 | 5 | 0 | 0 | 5.00 | 87.5 | -3.0 | 0 | 0 | 0 | 0 | 0 (0) | MISSING |
| Josh Metellus | S | 10 | 97.6 (83.0 wk11) | 45 | 29 | 375 | 1 | 0 | 8.33 | 97.9 | 9.1 | 2 | 4 | 0 | 4 | 20 (247) | MISSING |
| Harrison Smith | S | 10 | 54.6 (48.0 wk11) | 22 | 12 | 117 | 3 | 2 | 5.32 | 71.4 | 9.0 | 0 | 2 | 0 | 4 | 10 (116) | MISSING |
| Theo Jackson | S | 9 | 60.0 (54.0 wk11) | 10 | 10 | 222 | 2 | 0 | 22.20 | 158.3 | 10.2 | 1 | 1 | 0 | 1 | 9 (147) | MISSING |
| Jacob Thomas | S | 8 | 15.5 (22.0 wk11) | 4 | 3 | 48 | 0 | 0 | 12.00 | 114.6 | 17.2 | 0 | 0 | 0 | 0 | 2 (47) | MISSING |
| Jay Ward | S | 3 | 7.3 (16.0 wk9) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 0 (0) | MISSING |
| Jakobe Thomas | S | 1 | 17.0 (17.0 wk11) | — | — | — | — | — | — | — | — | — | 0 | 0 | 0 | 1 (5) | MISSING |

## Linebackers in coverage (PFR charted)

| Player | G | Tgt | Cmp | Yds | TD | YPT | Rtg | PBU |
|---|---|---|---|---|---|---|---|---|
| Blake Cashman | 9 | 27 | 19 | 197 | 0 | 7.30 | 91.1 | 7 |
| Andrew Van Ginkel | 10 | 24 | 11 | 100 | 1 | 4.17 | 54.2 | 0 |
| Eric Wilson | 10 | 22 | 18 | 134 | 1 | 6.09 | 107.2 | 1 |

## Most recent verified defender plays (pbp: PBU / INT / DPI)

| Wk | Opp | Defender | Type | Receiver | Zone |
|---|---|---|---|---|---|
| 11 | SF | B.Murphy | PBU | K.Allen | short_right |
| 11 | SF | K.Van Noy | PBU | C.McCaffrey | short_right |
| 10 | GB | D.Turner | PBU | J.Sturdivant | short_middle |
| 10 | GB | I.Rodgers | PBU | M.Golden | short_right |
| 10 | GB | J.Redmond | PBU | C.Watson | short_left |
| 10 | GB | D.Turner | PBU | T.Kraft | short_middle |
| 10 | GB | J.Pierre | PBU | M.Golden | short_left |
| 10 | GB | I.Pace | PBU | T.Kraft | short_right |
| 10 | GB | H.Smith | INT | T.Kraft | deep_middle |
| 9 | BUF | B.Cashman | PBU | D.Knox | short_middle |
| 9 | BUF | D.Turner | PBU | R.Davis | short_right |
| 9 | BUF | B.Murphy | INT | D.Moore | deep_middle |
| 9 | BUF | B.Cashman | PBU | K.Coleman | short_middle |
| 8 | DET | J.Pierre | INT | J.Williams | short_left |
| 8 | DET | J.Redmond | PBU | J.Gibbs | short_middle |

Full per-play log: `defender_target_log_pbp.csv`; per-week: `defender_weekly_log.csv`.

<!-- INFERRED-ATTRIBUTION -->
## INFERRED coverage attribution (not verified)

Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: high 36% (n=45), med 31% (n=102), low 20% (n=217), ALL 25% (n=364).

| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |
|---|---|---|---|---|---|---|---|
| Byron Murphy | CB | 53.6 | 33.3 | 468.1 | 8.73 | 2.49 | 82 (50) |
| Isaiah Rodgers | CB | 41.6 | 25.9 | 309.5 | 7.44 | 1.37 | 51 (38) |
| James Pierre | CB | 27.8 | 18.2 | 189.9 | 6.83 | 0.78 | 29 (11) |
| Blake Cashman | LB | 24.4 | 16.3 | 146.3 | 6.0 | 0.6 | 27 (0) |
| Josh Metellus | S | 24.4 | 14.2 | 175.7 | 7.2 | 0.81 | 41 (3) |
| Eric Wilson | LB | 22.4 | 15.1 | 134.2 | 5.99 | 0.37 | 20 (0) |
| Dallas Turner | LB | 18.5 | 12.0 | 107.9 | 5.83 | 0.4 | 8 (0) |
| Andrew Van Ginkel | LB | 18.1 | 12.2 | 100.8 | 5.57 | 0.31 | 9 (2) |
| Harrison Smith | S | 11.7 | 6.7 | 85.9 | 7.34 | 0.43 | 0 (0) |
| Theo Jackson | S | 11.7 | 6.3 | 91.1 | 7.79 | 0.44 | 6 (1) |
| Kyle Van Noy | LB | 8.0 | 5.3 | 50.6 | 6.32 | 0.24 | 0 (0) |
| Ivan Pace Jr. | LB | 5.4 | 3.5 | 35.9 | 6.65 | 0.19 | 2 (0) |

### Upcoming: opposing receivers vs likely MIN defender (INFERRED)

| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |
|---|---|---|---|---|---|---|---|
| 12 | 2026-11-29 | ATL | D.London (WR) | 17 | short_right 29%, short_left 27% | Byron Murphy (24%) | James Pierre (23%) |
| 12 | 2026-11-29 | ATL | B.Robinson (RB) | 12 | short_left 51%, short_right 36% | Blake Cashman (19%) | Dallas Turner (14%) |
| 12 | 2026-11-29 | ATL | K.Pitts (TE) | 10 | short_right 40%, short_left 33% | Josh Metellus (12%) | Blake Cashman (10%) |
| 12 | 2026-11-29 | ATL | J.Dotson (WR) | 8 | short_left 29%, deep_left 18% | Byron Murphy (25%) | James Pierre (23%) |
| 13 | 2026-12-06 | CAR | T.McMillan (WR) | 22 | short_right 25%, short_middle 24% | James Pierre (23%) | Byron Murphy (22%) |
| 13 | 2026-12-06 | CAR | D.Waller (TE) | 17 | short_right 38%, short_left 26% | Josh Metellus (12%) | Blake Cashman (10%) |
| 13 | 2026-12-06 | CAR | J.Coker (WR) | 16 | short_left 38%, short_middle 22% | James Pierre (25%) | Byron Murphy (21%) |
| 13 | 2026-12-06 | CAR | T.Tremble (TE) | 12 | short_left 44%, short_right 39% | Josh Metellus (12%) | James Pierre (10%) |

Defender pool = MIN players with defensive snaps in their most recent game (2026_11_MIN_SF); check inactives before use.

<!-- V2-WINDOW-CREDIT -->
## v2 INFERRED window credit (zone of responsibility)

Who owned the window where the ball was caught, from the team's shell mix + defender roles + catch spot (pbp direction + air yards), blended with the tackler. **INFERRED only.** Held-out wk 9–12 verified PBU/INT (n=364): exact defender 24% (top-2 39%); window class (CB-left/CB-right/nickel/S/LB) 32%; position group 50%.

| Defender | Pos | Window tgts | Window rec | Window yds | YPT | 20+ catches credited (prob-weighted) | 20+ yds credited | 20+ as top credit |
|---|---|---|---|---|---|---|---|---|
| Josh Metellus | S | 62.4 | 36.5 | 501.2 | 8.03 | 6.82 | 235.4 | 8 |
| Theo Jackson | S | 10.5 | 5.8 | 139.7 | 13.3 | 3.04 | 103.1 | 4 |
| Byron Murphy | CB | 35.9 | 23.8 | 263.0 | 7.33 | 2.48 | 69.1 | 2 |
| Isaiah Rodgers | CB | 28.6 | 18.4 | 184.2 | 6.44 | 2.44 | 62.3 | 4 |
| James Pierre | CB | 37.8 | 25.8 | 251.1 | 6.64 | 1.74 | 52.4 | 0 |
| Eric Wilson | LB | 39.7 | 23.2 | 242.7 | 6.11 | 1.54 | 66.6 | 1 |
| Blake Cashman | LB | 45.4 | 31.6 | 273.2 | 6.02 | 1.39 | 43.9 | 0 |
| Harrison Smith | S | 5.5 | 2.2 | 58.5 | 10.64 | 1.15 | 46.5 | 2 |
| Dallas Turner | LB | 6.8 | 5.1 | 50.1 | 7.37 | 0.4 | 10.7 | 0 |

### Rest of Week 12: receivers vs likely MIN window defender (INFERRED)

| Date | Offense | Receiver | Tgts last 4 | 20+ air tgt share | Window defender (share, his 20+ credit) | Next |
|---|---|---|---|---|---|---|
| 2026-11-29 | ATL | D.London (WR) | 17 | 13% | Josh Metellus (38%, 6.82) | James Pierre (18%, 1.74) |
| 2026-11-29 | ATL | B.Robinson (RB) | 12 | 0% | Blake Cashman (46%, 1.39) | Dallas Turner (23%, 0.4) |
| 2026-11-29 | ATL | K.Pitts (TE) | 10 | 7% | Josh Metellus (48%, 6.82) | Dallas Turner (23%, 0.4) |
| 2026-11-29 | ATL | J.Dotson (WR) | 8 | 26% | Josh Metellus (35%, 6.82) | James Pierre (21%, 1.74) |
