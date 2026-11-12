# CLE secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — CLE defense vs PIT (CLE@PIT)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 7** (4 rush, 3 rec)
- Q1 9:19 Rico Dowdle (RB) rush 15 — R.Hickman [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q1 6:17 Jaylen Warren (RB) rush 15 — R.Hickman; E.McNeil-Warren [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q1 4:17 Jaylen Warren (RB) rush 51 — C.Schwesinger [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q2 7:54 Darnell Washington (TE) rec 24 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 0:40 Jaylen Warren (RB) rush 23 — G.Delpit [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q2 0:25 Pat Freiermuth (TE) rec 28 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 10:23 Darnell Washington (TE) rec 58 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 11 | 6 | 34 | -3.36 | A.Rodgers base 6.4 (QB n=105) |
| WR_mid | 0 | 0 | 0 | — |  |
| TE | 7 | 5 | 129 | 12.08 | A.Rodgers base 6.4 (QB n=57) |
| RB | 2 | 0 | 0 | -7.23 | A.Rodgers base 7.2 (QB n=52) |
| RB rush | 24 car | — | 165 | 6.88 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| C.Schwesinger | LB | 3 | 89 | 2 | 0 | 0 | 0 | P.Freiermuth×1, D.Washington×2 |
| M.Harden | CB | 2 | 18 | 0 | 0 | 0 | 0 | G.Bernard×1, B.Johnson×1 |
| Q.Williams | LB | 1 | 15 | 0 | 1 | 0 | 0 | G.Bernard×1 |
| D.Ward | CB | 2 | 11 | 0 | 1 | 1 | 0 | D.Metcalf×1, G.Bernard×1 |
| T.Campbell | CB | 1 | 2 | 0 | 1 | 0 | 0 | G.Bernard×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Myles Harden ← Germie Bernard: 5 tgt, 5 rec, 30 yds
- Tyson Campbell ← DK Metcalf: 5 tgt, 1 rec, 4 yds — limited his man
