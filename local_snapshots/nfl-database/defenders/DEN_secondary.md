# DEN secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — FILLS STUB ABOVE — DEN defense vs KC (KC@DEN)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (1 rush, 3 rec)
- Q2 7:40 Emmett Johnson (RB) rec 73 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q2 1:02 Emmett Johnson (RB) rec 38 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 5:19 Emmett Johnson (RB) rush 15 — T.Rapp [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 1:32 Travis Kelce (TE) rec 32 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 12 | 9 | 50 | -3.72 | P.Mahomes base 7.9 (QB n=70) |
| WR_mid | 6 | 4 | 40 | -2.96 | P.Mahomes base 9.6 (QB n=19) |
| TE | 10 | 8 | 88 | -1.2 | P.Mahomes base 10.0 (QB n=51) |
| RB | 10 | 9 | 143 | 8.58 | P.Mahomes base 5.7 (QB n=40) |
| RB rush | 16 car | — | 88 | 5.5 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| D.Key | SAF | 5 | 63 | 1 | 1 | 0 | 0 | T.Kelce×2, K.Walker×2, C.Allen×1 |
| A.Singleton | LB | 5 | 35 | 0 | 1 | 0 | 0 | E.Johnson×1, R.Rice×2, T.Kelce×1, J.Briningstool×1 |
| P.Surtain | CB | 3 | 23 | 0 | 1 | 0 | 0 | R.Rice×1, T.Kelce×1, N.Gray×1 |
| R.Moss | CB | 4 | 17 | 0 | 1 | 0 | 0 | K.Walker×1, X.Worthy×1, C.Allen×1, J.Royals×1 |
| J.Strnad | LB | 2 | 12 | 0 | 0 | 0 | 0 | T.Kelce×1, E.Johnson×1 |
| D.Tillman | LB | 1 | 7 | 0 | 1 | 0 | 0 | R.Rice×1 |
| J.McMillian | CB | 1 | 7 | 0 | 0 | 0 | 0 | X.Worthy×1 |
| J.Cooper | LB | 2 | 7 | 0 | 0 | 0 | 0 | E.Johnson×1, R.Rice×1 |
| Z.Allen | DE | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Ja'Quan McMillian ← Rashee Rice: 8 tgt, 7 rec, 53 yds
- Riley Moss ← Xavier Worthy: 6 tgt, 3 rec, 13 yds — limited his man
