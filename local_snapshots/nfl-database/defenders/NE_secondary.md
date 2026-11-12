# NE secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — FILLS STUB ABOVE — NE defense vs MIA (NE@MIA)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 3** (2 rush, 1 rec)
- Q2 14:18 Malik Washington (WR) rec 23 — Marcus Jones [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Christian Gonzalez)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L25/S56/R18)
- Q2 0:34 Ollie Gordon II (RB) rush 15 — K.Byard [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 11:46 Ollie Gordon II (RB) rush 16 — C.Woodson [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 15 | 11 | 99 | -0.24 | M.Willis base 6.8 (QB n=76) |
| WR_mid | 4 | 4 | 33 | -2.7 | M.Willis base 10.9 (QB n=20) |
| TE | 7 | 4 | 43 | -1.76 | M.Willis base 7.9 (QB n=30) |
| RB | 2 | 0 | 0 | -3.38 | M.Willis base 3.4 (QB n=24) |
| RB rush | 16 car | — | 80 | 5.0 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| C.Davis | CB | 6 | 59 | 0 | 0 | 0 | 0 | M.Washington×1, K.Coleman×1, G.Dulcich×3, J.Tolbert×1 |
| C.Gonzalez | CB | 3 | 46 | 1 | 0 | 0 | 0 | M.Washington×2, C.Douglas×1 |
| M.Jones | CB | 4 | 28 | 0 | 1 | 0 | 0 | C.Bell×2, C.Douglas×1, G.Dulcich×1 |
| K.Byard | FS | 2 | 18 | 0 | 0 | 1 | 0 | C.Douglas×2 |
| C.Elliss | LB | 1 | 9 | 0 | 0 | 0 | 0 | C.Bell×1 |
| E.Ponder | LB | 0 | 0 | 0 | 1 | 0 | 0 |  |
| R.Spillane | LB | 0 | 0 | 0 | 2 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Christian Gonzalez ← Caleb Douglas: 5 tgt, 4 rec, 43 yds
- Marcus Jones ← Malik Washington: 5 tgt, 4 rec, 39 yds
- Carlton Davis ← Kevin Coleman Jr.: 2 tgt, 2 rec, 11 yds
