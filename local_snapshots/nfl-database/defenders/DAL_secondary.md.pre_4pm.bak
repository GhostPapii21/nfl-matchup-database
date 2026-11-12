# DAL secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — DAL defense vs ARI (ARI@DAL)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 7** (3 rush, 4 rec)
- Q1 1:49 Michael Wilson (WR) rec 22 — Joey Porter Jr. [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Q2 5:11 Kendrick Bourne (WR) rec 29 — Caleb Downs [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said DaRon Bland)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L18/S69/R13)
- Q3 0:57 Tyler Allgeier (RB) rush 63 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q4 14:20 Tyler Allgeier (RB) rush 52 — D.Bland [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 0:50 Michael Wilson (WR) rec 21 — Joey Porter Jr. [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Q4 0:27 Michael Wilson (WR) rec 27 — Joey Porter Jr. [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Q5 5:43 Michael Wilson (WR) rush 17 — S.James [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 19 | 10 | 129 | 1.3 | J.Brissett base 5.5 (QB n=108) |
| WR_mid | 3 | 2 | 42 | 6.72 | J.Brissett base 7.3 (QB n=29) |
| TE | 12 | 9 | 82 | 0.14 | J.Brissett base 6.7 (QB n=96) |
| RB | 7 | 6 | 54 | 3.85 | J.Brissett base 3.9 (QB n=38) |
| RB rush | 18 car | — | 165 | 9.17 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| P.Locke | DB | 4 | 61 | 1 | 0 | 0 | 0 | K.Bourne×1, D.Duvernay×1, T.McBride×2 |
| D.Bland | CB | 2 | 48 | 2 | 2 | 0 | 0 | Mi.Wilson×2 |
| D.Overshown | LB | 4 | 35 | 0 | 0 | 0 | 0 | Z.Knight×1, E.Higgins×1, T.Allgeier×1, D.Duvernay×1 |
| M.Hooker | FS | 2 | 22 | 0 | 1 | 0 | 0 | T.McBride×1, T.Allgeier×1 |
| C.Durant | CB | 3 | 16 | 0 | 0 | 0 | 0 | Mi.Wilson×1, T.McBride×2 |
| J.Porter | CB | 1 | 9 | 0 | 0 | 0 | 0 | Mi.Wilson×1 |
| A.Speed | CB | 1 | 9 | 0 | 1 | 0 | 0 | Mi.Wilson×1 |
| S.James | LB | 2 | 8 | 0 | 0 | 1 | 0 | T.Allgeier×2 |
| J.Barham | LB | 1 | 6 | 0 | 0 | 0 | 0 | E.Higgins×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Joey Porter Jr. ← Michael Wilson: 15 tgt, 8 rec, 111 yds
- Caleb Downs ← Kendrick Bourne: 2 tgt, 1 rec, 29 yds
