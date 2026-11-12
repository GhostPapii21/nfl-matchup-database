# MIA secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — FILLS STUB ABOVE — MIA defense vs NE (NE@MIA)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (1 rush, 3 rec)
- Q1 10:49 Hunter Henry (TE) rec 20 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q1 3:39 Corey Kiner (RB) rush 20 — M.Taaffe; J.Marshall [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 7:17 DeMario Douglas (WR) rec 26 — Chris A. Johnson [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Jason Marshall)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L9/S82/R9)
- Q4 12:39 DeMario Douglas (WR) rec 48 — Chris A. Johnson [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Jason Marshall)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L9/S82/R9)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 7 | 7 | 101 | 5.42 | D.Maye base 9.0 (QB n=104) |
| WR_mid | 1 | 1 | 12 | 4.88 | D.Maye base 7.1 (QB n=16) |
| TE | 7 | 4 | 35 | -4.87 | D.Maye base 9.9 (QB n=47) |
| RB | 3 | 3 | 8 | -4.28 | D.Maye base 6.9 (QB n=37) |
| RB rush | 27 car | — | 123 | 4.56 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| J.Rodriguez | LB | 3 | 17 | 0 | 0 | 0 | 0 | H.Henry×1, E.Chism×2 |
| J.Brents | CB | 3 | 13 | 0 | 0 | 0 | 0 | E.Raridon×1, R.Stevenson×1, E.Chism×1 |
| J.Brooks | LB | 3 | 10 | 0 | 0 | 0 | 0 | H.Henry×1, R.Stevenson×2 |
| C.Johnson | CB | 2 | 10 | 0 | 0 | 0 | 0 | D.Douglas×1, E.Chism×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Chris A. Johnson ← DeMario Douglas: 3 tgt, 3 rec, 76 yds
