# TB secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — TB defense vs ATL (ATL@TB)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 2** (1 rush, 1 rec)
- Q2 14:54 Bijan Robinson (RB) rush 26 — J.Parrish [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 4:35 Jahan Dotson (WR) rec 76 — Zyon McCollum [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L33/S23/R44)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 12 | 4 | 107 | -0.72 | M.Penix base 9.6 (QB n=68) |
| WR_mid | 1 | 0 | 0 | -10.15 | M.Penix base 10.2 (QB n=13) |
| TE | 7 | 2 | 14 | -5.06 | M.Penix base 7.1 (QB n=35) |
| RB | 2 | 1 | 3 | -3.45 | M.Penix base 5.0 (QB n=22) |
| RB rush | 16 car | — | 87 | 5.44 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| Z.McCollum | CB | 1 | 19 | 0 | 0 | 1 | 0 | J.Dotson×1 |
| J.Parrish | CB | 1 | 9 | 0 | 1 | 1 | 0 | A.Hooper×1 |
| K.Scott | CB | 1 | 8 | 0 | 1 | 0 | 0 | D.London×1 |
| A.Anzalone | MLB | 1 | 3 | 0 | 0 | 2 | 0 | K.Herbert×1 |
| A.Robinson | DT | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Zyon McCollum ← Jahan Dotson: 4 tgt, 2 rec, 95 yds
- Jacob Parrish ← Drake London: 4 tgt, 1 rec, 8 yds — limited his man
- Keionte Scott ← Olamide Zaccheaus: 2 tgt, 1 rec, 4 yds
