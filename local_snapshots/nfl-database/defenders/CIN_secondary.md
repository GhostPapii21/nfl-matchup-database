# CIN secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — CIN defense vs TEN (TEN@CIN)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 7** (2 rush, 5 rec)
- Q1 7:55 Tony Pollard (RB) rush 40 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q1 5:57 Elic Ayomanor (WR) rec 23 — DJ Ivey [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said DJ Turner)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S15/R40)
- Q2 11:06 Gunnar Helm (TE) rec 24 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 10:01 Chimere Dike (WR) rec 21 — defender unknown [unknown; no public source]; alignment: middle (this-play pass_location proxy)
- Q3 10:15 Chimere Dike (WR) rec 28 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)
- Q4 12:06 Tony Pollard (RB) rush 22 — M.Murphy [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 5:05 Gunnar Helm (TE) rec 25 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 14 | 11 | 118 | 1.69 | C.Ward base 6.7 (QB n=115) |
| WR_mid | 7 | 4 | 53 | -1.49 | C.Ward base 9.1 (QB n=17) |
| TE | 13 | 8 | 112 | 4.68 | C.Ward base 3.9 (QB n=30) |
| RB | 5 | 3 | 20 | 0.12 | C.Ward base 3.9 (QB n=34) |
| RB rush | 14 car | — | 113 | 8.07 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| J.Battle | SAF | 8 | 104 | 2 | 2 | 0 | 0 | G.Helm×1, E.Ayomanor×1, W.Robinson×3, C.Dike×2, D.Bellinger×1 |
| D.Hill | DB | 3 | 57 | 1 | 0 | 0 | 0 | W.Robinson×1, C.Dike×1, E.Ayomanor×1 |
| J.Newton | CB | 1 | 25 | 1 | 1 | 0 | 0 | G.Helm×1 |
| D.Knight | LB | 3 | 19 | 0 | 0 | 0 | 0 | G.Helm×2, C.Dike×1 |
| B.Carter | LB | 2 | 17 | 0 | 0 | 0 | 0 | C.Ridley×1, T.Pollard×1 |
| D.Ivey | CB | 1 | 8 | 0 | 0 | 0 | 0 | T.Pollard×1 |
| B.Hill | DT | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Daxton Hill ← Wan'Dale Robinson: 7 tgt, 6 rec, 56 yds
- DJ Ivey ← Elic Ayomanor: 5 tgt, 3 rec, 34 yds
