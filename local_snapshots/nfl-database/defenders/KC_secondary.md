# KC secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — FILLS STUB ABOVE — KC defense vs DEN (KC@DEN)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (0 rush, 4 rec)
- Q1 0:05 Courtland Sutton (WR) rec 23 — Mansoor Delane [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L39/S29/R33)
- Q2 13:04 Jaylen Waddle (WR) rec 35 — Nohl Williams [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Mansoor Delane)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L27/S38/R35)
- Q4 11:23 Adam Trautman (TE) rec 22 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 2:31 Jonah Coleman (RB) rec 51 — defender unknown [unknown; no public source]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 14 | 9 | 79 | -0.3 | B.Nix base 5.9 (QB n=107) |
| WR_mid | 1 | 1 | 35 | 24.77 | B.Nix base 10.2 (league fallback) |
| TE | 7 | 4 | 34 | -0.96 | B.Nix base 5.8 (QB n=32) |
| RB | 5 | 4 | 72 | 7.46 | B.Nix base 6.9 (QB n=50) |
| RB rush | 12 car | — | 50 | 4.17 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| C.Conner | DB | 3 | 55 | 2 | 0 | 0 | 0 | C.Sutton×1, L.Humphrey×1, A.Trautman×1 |
| N.Williams | CB | 1 | 51 | 1 | 0 | 0 | 0 | J.Coleman×1 |
| N.Bolton | LB | 4 | 21 | 0 | 0 | 0 | 0 | J.Coleman×2, N.Adkins×1, A.Trautman×1 |
| J.Cochrane | LB | 1 | 10 | 0 | 0 | 0 | 0 | A.Prentice×1 |
| K.Fulton | CB | 2 | 10 | 0 | 0 | 0 | 0 | T.Franklin×1, M.Mims×1 |
| D.Tranquill | LB | 1 | 8 | 0 | 0 | 0 | 0 | C.Sutton×1 |
| J.Canady | CB | 2 | 7 | 0 | 0 | 0 | 0 | M.Mims×1, C.Sutton×1 |
| C.Roland-Wallace | CB | 1 | 3 | 0 | 0 | 0 | 0 | J.Waddle×1 |
| C.Roland-Wallace, G.Karlaftis | ? | 0 | 0 | 0 | 1 | 0 | 0 |  |
| R.Thomas | DE | 0 | 0 | 0 | 1 | 0 | 0 |  |
| G.Karlaftis | DE | 0 | 0 | 0 | 2 | 0 | 0 |  |
| K.Tonga | DT | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Mansoor Delane ← Courtland Sutton: 4 tgt, 4 rec, 53 yds
- Nohl Williams ← Jaylen Waddle: 5 tgt, 2 rec, 38 yds
- Nohl Williams ← Marvin Mims Jr.: 3 tgt, 2 rec, 10 yds — limited his man
