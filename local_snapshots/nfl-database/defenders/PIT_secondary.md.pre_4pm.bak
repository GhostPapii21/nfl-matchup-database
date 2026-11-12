# PIT secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — PIT defense vs CLE (CLE@PIT)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (0 rush, 4 rec)
- Q2 11:21 Harold Fannin Jr. (TE) rec 25 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 2:00 KC Concepcion (WR) rec 24 — Jalen Ramsey [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Jamel Dean)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L20/S59/R21)
- Q4 14:22 Harold Fannin Jr. (TE) rec 37 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 6:51 Harold Fannin Jr. (TE) rec 27 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 16 | 9 | 77 | -2.17 | D.Watson base 7.0 (QB n=93) |
| WR_mid | 0 | 0 | 0 | — |  |
| TE | 13 | 11 | 163 | 5.51 | S.Sanders base 7.0 (league fallback) |
| RB | 10 | 8 | 86 | 3.25 | D.Watson base 5.3 (QB n=43) |
| RB rush | 9 car | — | 31 | 3.44 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| P.Queen | LB | 7 | 70 | 0 | 1 | 0 | 0 | H.Fannin×2, D.Sampson×5 |
| J.Ramsey | CB | 2 | 28 | 1 | 0 | 0 | 0 | T.Wallace×1, H.Fannin×1 |
| D.Everette | CB | 2 | 26 | 1 | 0 | 0 | 0 | H.Fannin×1, K.Concepcion×1 |
| J.Dean | CB | 3 | 19 | 0 | 0 | 0 | 0 | D.Boston×3 |
| P.Wilson | LB | 2 | 15 | 0 | 0 | 0 | 0 | H.Fannin×1, D.Boston×1 |
| A.Highsmith | LB | 1 | 8 | 0 | 0 | 0 | 0 | H.Fannin×1 |
| C.Heyward | DE | 1 | 7 | 0 | 1 | 0 | 0 | K.Concepcion×1 |
| A.Samuel | CB | 0 | 0 | 0 | 1 | 0 | 0 |  |
| K.Benton | DT | 0 | 0 | 0 | 1 | 0 | 0 |  |
| T.Watt | OLB | 0 | 0 | 0 | 1 | 0 | 0 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Jamel Dean ← Denzel Boston: 10 tgt, 5 rec, 37 yds — limited his man
- Jalen Ramsey ← KC Concepcion: 4 tgt, 3 rec, 37 yds
- Asante Samuel Jr. ← Jerry Jeudy: 1 tgt, 0 rec, 0 yds
