# LAC secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — FILLS STUB ABOVE — LAC defense vs LAR (LAC@LAR)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 2** (1 rush, 1 rec)
- Q2 1:29 Tutu Atwell (WR) rec 40 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)
- Q3 10:42 Blake Corum (RB) rush 23 — defender unknown [unknown; no public source]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 15 | 11 | 107 | -0.86 | M.Stafford base 8.0 (QB n=109) |
| WR_mid | 4 | 2 | 25 | -3.79 | M.Stafford base 10.0 (QB n=27) |
| TE | 4 | 3 | 22 | -1.11 | M.Stafford base 6.6 (QB n=77) |
| RB | 2 | 1 | 3 | -4.65 | M.Stafford base 6.1 (QB n=55) |
| RB rush | 23 car | — | 125 | 5.43 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| T.Still | CB | 1 | 40 | 1 | 0 | 1 | 0 | T.Atwell×1 |
| T.Jefferson | S | 3 | 37 | 0 | 0 | 0 | 0 | P.Nacua×3 |
| I.Waxter | DB | 5 | 16 | 0 | 0 | 0 | 0 | P.Nacua×3, D.Allen×1, T.Atwell×1 |
| D.Henley | LB | 2 | 15 | 0 | 0 | 0 | 0 | P.Nacua×2 |
| E.Molden | CB | 1 | 6 | 0 | 0 | 0 | 0 | D.Allen×1 |
| C.Hart | CB | 1 | 5 | 0 | 0 | 0 | 0 | P.Nacua×1 |
| T.Tuipulotu | LB | 1 | 3 | 0 | 0 | 0 | 0 | P.Nacua×1 |
| D.Phillips | LB | 1 | 3 | 0 | 0 | 0 | 0 | K.Williams×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Donte Jackson ← Puka Nacua: 12 tgt, 11 rec, 80 yds
