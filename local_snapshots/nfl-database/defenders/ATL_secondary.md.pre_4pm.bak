# ATL secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — ATL defense vs TB (ATL@TB)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (4 rush, 0 rec)
- Q1 9:55 Bucky Irving (RB) rush 24 — J.Bates; S.Ebukam [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q2 7:11 Kenny Gainwell (RB) rush 20 — A.Terrell [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 6:31 Bucky Irving (RB) rush 46 — C.Henderson [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 4:59 Kenny Gainwell (RB) rush 28 — K.Daniels; M.Smith [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 2 | 0 | 0 | -6.09 | B.Mayfield base 6.1 (QB n=46) |
| WR_mid | 0 | 0 | 0 | — |  |
| TE | 0 | 0 | 0 | — |  |
| RB | 1 | 0 | 0 | -3.35 | B.Mayfield base 3.3 (QB n=26) |
| RB rush | 39 car | — | 283 | 7.26 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| M.Hughes | CB | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Mike Hughes ← Chris Godwin Jr.: 1 tgt, 0 rec, 0 yds
