# ARI secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — ARI defense vs DAL (ARI@DAL)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 2** (0 rush, 2 rec)
- Q2 10:03 CeeDee Lamb (WR) rec 27 — Denzel Burke [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Garrett Williams)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L28/S38/R34)
- Q3 0:51 George Pickens (WR) rec 37 — Max Melton [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Denzel Burke)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L57/S10/R32)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 14 | 9 | 115 | 0.82 | D.Prescott base 7.4 (QB n=166) |
| WR_mid | 5 | 3 | 29 | -4.27 | D.Prescott base 10.1 (QB n=28) |
| TE | 4 | 3 | 30 | 2.04 | D.Prescott base 5.5 (QB n=41) |
| RB | 3 | 2 | 19 | 2.53 | D.Prescott base 3.8 (QB n=31) |
| RB rush | 23 car | — | 64 | 2.78 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| D.Burke | CB | 3 | 66 | 1 | 2 | 0 | 0 | R.Flournoy×2, G.Pickens×1 |
| M.Melton | CB | 1 | 27 | 1 | 0 | 0 | 0 | C.Lamb×1 |
| J.Gibbens | LB | 3 | 14 | 0 | 0 | 0 | 0 | T.Goodson×1, C.Lamb×2 |
| J.Burch | LB | 1 | 11 | 0 | 0 | 0 | 0 | T.Goodson×1 |
| D.Stills | DT | 1 | 5 | 0 | 1 | 0 | 0 | C.Lamb×1 |
| L.Collier | DE | 0 | 0 | 0 | 2 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Denzel Burke ← CeeDee Lamb: 11 tgt, 7 rec, 58 yds — limited his man
- Max Melton ← George Pickens: 4 tgt, 2 rec, 48 yds
- Garrett Williams ← Ryan Flournoy: 4 tgt, 3 rec, 38 yds
