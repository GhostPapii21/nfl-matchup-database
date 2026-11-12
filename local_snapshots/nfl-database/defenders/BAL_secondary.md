# BAL secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — BAL defense vs BUF (BAL@BUF)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 5** (1 rush, 4 rec)
- Q1 13:43 Khalil Shakir (WR) rec 26 — Keyon Martin [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Kyle Hamilton)]; alignment: slot (middle-target proxy) (pregame target-side proxy; ESPN season split L18/S67/R15)
- Q2 4:22 James Cook (RB) rush 16 — T.Tampa [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 9:44 Denarius Moore (WR) rec 49 — Marlon Humphrey [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L36/S26/R39)
- Q4 13:45 Dalton Kincaid (TE) rec 40 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 5:58 Dalton Kincaid (TE) rec 23 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 10 | 5 | 49 | -2.81 | J.Allen base 7.7 (QB n=66) |
| WR_mid | 6 | 4 | 92 | 0.79 | J.Allen base 14.5 (QB n=24) |
| TE | 10 | 6 | 99 | 1.34 | J.Allen base 8.6 (QB n=41) |
| RB | 6 | 5 | 40 | -3.13 | J.Allen base 9.8 (QB n=29) |
| RB rush | 26 car | — | 106 | 4.08 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| M.Humphrey | CB | 3 | 79 | 2 | 1 | 0 | 0 | K.Shakir×1, K.Coleman×1, D.Moore×1 |
| T.Simpson | LB | 2 | 28 | 0 | 0 | 0 | 0 | D.Kincaid×1, J.Cook×1 |
| R.Smith | ILB | 2 | 28 | 0 | 2 | 0 | 0 | D.Moore×1, K.Shakir×1 |
| T.Buchanan | LB | 3 | 19 | 0 | 0 | 0 | 0 | K.Shakir×1, J.Hawes×1, D.Knox×1 |
| T.Hendrickson | LB | 1 | 18 | 0 | 0 | 0 | 0 | K.Shakir×1 |
| K.Martin | CB | 1 | 6 | 0 | 0 | 0 | 0 | K.Shakir×1 |
| T.Tampa | CB | 1 | 4 | 0 | 0 | 0 | 0 | D.Moore×1 |
| B.Washington | DT | 0 | 0 | 0 | 0 | 1 | 0 |  |
| C.Awuzie | CB | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Marlon Humphrey ← Denarius Moore: 6 tgt, 3 rec, 72 yds
- Keyon Martin ← Khalil Shakir: 6 tgt, 5 rec, 65 yds
- Nate Wiggins ← Keon Coleman: 3 tgt, 1 rec, 4 yds — limited his man
