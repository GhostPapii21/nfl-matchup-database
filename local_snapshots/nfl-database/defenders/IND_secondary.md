# IND secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — IND defense vs JAX (IND@JAX)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 6** (2 rush, 4 rec)
- Q1 10:33 Brenton Strange (TE) rec 46 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 7:14 Nate Boerkircher (TE) rec 31 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 1:51 Bhayshul Tuten (RB) rush 39 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 9:08 Chris Rodriguez Jr. (RB) rush 28 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 3:50 Bhayshul Tuten (RB) rec 30 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 0:00 Bhayshul Tuten (RB) rec 25 — defender unknown [unknown; no public source]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 2 | 1 | 10 | -3.14 | T.Lawrence base 8.1 (QB n=86) |
| WR_mid | 2 | 1 | 14 | -4.74 | T.Lawrence base 11.7 (QB n=19) |
| TE | 4 | 4 | 94 | 15.64 | T.Lawrence base 7.9 (QB n=43) |
| RB | 6 | 4 | 88 | 8.71 | T.Lawrence base 6.0 (QB n=24) |
| RB rush | 22 car | — | 163 | 7.41 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| A.Davis-Gaither | LB | 1 | 17 | 0 | 0 | 0 | 0 | C.Rodriguez×1 |
| C.Ward | CB | 1 | 16 | 0 | 0 | 0 | 0 | P.Washington×1 |
| K.Gushiken | CB | 1 | 14 | 0 | 0 | 0 | 0 | J.Meyers×1 |
| A.Gardner | CB | 1 | 10 | 0 | 2 | 0 | 0 | J.Meyers×1 |
| J.Carlies | LB | 1 | 9 | 0 | 0 | 0 | 0 | B.Strange×1 |
| A.Adebawore | DT | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Charvarius Ward ← Jakobi Meyers: 3 tgt, 2 rec, 24 yds
