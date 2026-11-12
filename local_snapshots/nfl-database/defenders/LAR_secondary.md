# LAR secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — FILLS STUB ABOVE — LAR defense vs LAC (LAC@LAR)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (0 rush, 4 rec)
- Q1 3:55 Ladd McConkey (WR) rec 30 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)
- Q2 12:32 Charlie Kolar (TE) rec 20 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 8:26 Quentin Johnston (WR) rec 21 — defender unknown [unknown; no public source]; alignment: middle (this-play pass_location proxy)
- Q2 0:04 Ladd McConkey (WR) rec 54 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 7 | 6 | 101 | 6.94 | J.Herbert base 7.5 (QB n=71) |
| WR_mid | 2 | 1 | 21 | 1.17 | J.Herbert base 9.3 (QB n=18) |
| TE | 9 | 6 | 72 | 2.07 | J.Herbert base 5.9 (QB n=43) |
| RB | 7 | 6 | 30 | -0.25 | J.Herbert base 4.5 (QB n=41) |
| RB rush | 13 car | — | 43 | 3.31 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| J.Watson | CB | 2 | 64 | 1 | 0 | 0 | 0 | L.McConkey×1, T.Harris×1 |
| Q.Lake | SAF | 3 | 48 | 1 | 1 | 1 | 0 | L.McConkey×1, O.Gadsden×2 |
| J.Wallace | DB | 4 | 32 | 0 | 0 | 0 | 0 | T.Harris×2, K.Mitchell×1, O.Gadsden×1 |
| O.Speights | LB | 3 | 23 | 1 | 1 | 0 | 0 | L.McConkey×1, Q.Johnston×1, O.Hampton×1 |
| N.Landman | LB | 1 | 12 | 0 | 0 | 0 | 0 | O.Gadsden×1 |
| T.McDuffie | CB | 4 | 10 | 0 | 0 | 1 | 0 | L.McConkey×1, K.Vidal×1, O.Hampton×1, Q.Johnston×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
