# MIN secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — MIN defense vs DET (MIN@DET)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (3 rush, 1 rec)
- Q1 4:55 Jameson Williams (WR) rec 46 — Isaiah Rodgers [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said James Pierre)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L35/S22/R42)
- Q2 0:12 Jahmyr Gibbs (RB) rush 19 — B.Murphy [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 4:40 Jahmyr Gibbs (RB) rush 30 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q4 8:39 Jahmyr Gibbs (RB) rush 17 — J.Metellus [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 5 | 3 | 24 | -3.85 | J.Goff base 8.6 (QB n=96) |
| WR_mid | 2 | 1 | 46 | 14.65 | J.Goff base 8.4 (QB n=31) |
| TE | 6 | 4 | 40 | -1.35 | J.Goff base 8.0 (QB n=47) |
| RB | 5 | 3 | 20 | -2.96 | J.Goff base 7.0 (QB n=45) |
| RB rush | 32 car | — | 217 | 6.78 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| B.Murphy | CB | 4 | 68 | 1 | 0 | 0 | 0 | J.Williams×2, J.Gibbs×1, S.LaPorta×1 |
| B.Cashman | LB | 1 | 19 | 0 | 0 | 0 | 0 | S.LaPorta×1 |
| J.Metellus | SAF | 2 | 10 | 0 | 1 | 0 | 0 | T.Conklin×1, J.Williams×1 |
| H.Smith | FS | 1 | 8 | 0 | 0 | 0 | 0 | S.LaPorta×1 |
| E.Wilson | LB | 1 | 5 | 0 | 0 | 0 | 0 | S.Vaki×1 |
| J.Redmond | DL | 0 | 0 | 0 | 1 | 0 | 0 |  |
| J.Pierre | CB | 0 | 0 | 0 | 0 | 1 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Isaiah Rodgers ← Jameson Williams: 5 tgt, 4 rec, 70 yds
