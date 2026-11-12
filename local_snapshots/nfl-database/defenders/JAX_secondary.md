# JAX secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — JAX defense vs IND (IND@JAX)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 2** (2 rush, 0 rec)
- Q1 14:56 Jonathan Taylor (RB) rush 19 — M.Brown [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 6:04 Seth McGowan (RB) rush 16 — K.Merriweather; R.Lane [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 14 | 12 | 92 | 0.42 | D.Jones base 6.1 (QB n=102) |
| WR_mid | 1 | 1 | 18 | 9.6 | D.Jones base 8.4 (QB n=35) |
| TE | 9 | 3 | 17 | -3.15 | D.Jones base 5.0 (QB n=57) |
| RB | 5 | 4 | 24 | -1.33 | D.Jones base 6.1 (QB n=31) |
| RB rush | 14 car | — | 92 | 6.57 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| M.Brown | CB | 3 | 27 | 0 | 0 | 0 | 0 | K.Allen×2, J.Downs×1 |
| F.Oluokun | LB | 5 | 23 | 0 | 0 | 0 | 0 | J.Taylor×3, J.Downs×1, K.Allen×1 |
| T.Hunter | CB | 2 | 22 | 0 | 0 | 0 | 0 | K.Allen×1, L.Treadwell×1 |
| V.Miller | LB | 1 | 10 | 0 | 0 | 0 | 0 | T.Warren×1 |
| R.Lane | SAF | 1 | 5 | 0 | 1 | 1 | 0 | K.Allen×1 |
| J.Mcleod | LB | 1 | 3 | 0 | 0 | 0 | 0 | T.Warren×1 |
| B.Combs | LB | 0 | 0 | 0 | 1 | 1 | 0 |  |
| D.Gardeck | LB | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Jarrian Jones ← Keenan Allen: 7 tgt, 7 rec, 67 yds
- Jourdan Lewis ← Josh Downs: 5 tgt, 4 rec, 23 yds — limited his man
- Travis Hunter ← Laquon Treadwell: 2 tgt, 1 rec, 18 yds
