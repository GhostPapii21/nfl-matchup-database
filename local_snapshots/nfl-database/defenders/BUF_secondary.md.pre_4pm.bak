# BUF secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — BUF defense vs BAL (BAL@BUF)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 1** (0 rush, 1 rec)
- Q3 14:06 Rashod Bateman (WR) rec 22 — Davison Igbinosun [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Maxwell Hairston)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L31/S32/R37)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 7 | 2 | 35 | -7.14 | L.Jackson base 12.1 (QB n=35) |
| WR_mid | 2 | 0 | 0 | -10.23 | J.Fagnano base 10.2 (league fallback) |
| TE | 6 | 3 | 29 | -1.9 | T.Huntley base 6.7 (QB n=26) |
| RB | 9 | 5 | 26 | -2.11 | T.Huntley base 5.0 (QB n=19) |
| RB rush | 13 car | — | 74 | 5.69 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| D.Hamlin | SAF | 3 | 36 | 1 | 1 | 0 | 0 | J.Hill×2, R.Bateman×1 |
| M.Hairston | CB | 1 | 13 | 0 | 0 | 0 | 0 | J.Lane×1 |
| T.Bernard | LB | 2 | 12 | 0 | 0 | 0 | 0 | D.Henry×1, M.Andrews×1 |
| T.Couch | DB | 1 | 7 | 0 | 0 | 0 | 0 | J.Hill×1 |
| G.Rousseau | LB | 0 | 0 | 0 | 2 | 0 | 0 |  |
| D.Igbinosun | CB | 0 | 0 | 0 | 0 | 1 | 0 |  |
| D.Walker | DT | 0 | 0 | 0 | 1 | 0 | 0 |  |
| C.Benford | CB | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Davison Igbinosun ← Rashod Bateman: 3 tgt, 1 rec, 22 yds
- Christian Benford ← Ja'Kobi Lane: 1 tgt, 1 rec, 13 yds
- Dee Alford ← Zay Flowers: 4 tgt, 0 rec, 0 yds — limited his man
