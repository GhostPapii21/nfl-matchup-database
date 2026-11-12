# LV secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — LV defense vs NYJ (LV@NYJ)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 9** (4 rush, 5 rec)
- Q1 15:00 Garrett Wilson (WR) rec 31 — Eric Stokes [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L42/S22/R36)
- Q1 14:28 Braelon Allen (RB) rush 15 — Q.Walker; T.Stukes [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q1 13:56 Braelon Allen (RB) rush 15 — A.Butler [confirmed; ESPN play text: Defensive Holding on play (single-source)]; alignment: backfield (position default)
- Q2 14:01 Adonai Mitchell (WR) rec 20 — Darien Porter [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Hezekiah Masses)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S16/R39)
- Q2 11:32 Adonai Mitchell (WR) rec 22 — Darien Porter [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Hezekiah Masses)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S16/R39)
- Q2 8:42 Braelon Allen (RB) rush 24 — T.Johnson; E.Stokes [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 9:09 Kenyon Sadiq (TE) rec 22 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 8:20 Braelon Allen (RB) rush 21 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q4 6:11 Adonai Mitchell (WR) rec 47 — Darien Porter [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Hezekiah Masses)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S16/R39)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 19 | 13 | 225 | 3.16 | G.Smith base 8.7 (QB n=89) |
| WR_mid | 3 | 1 | 18 | -8.81 | G.Smith base 14.8 (QB n=16) |
| TE | 7 | 4 | 41 | -0.6 | G.Smith base 6.5 (QB n=57) |
| RB | 2 | 2 | 6 | -3.81 | G.Smith base 6.8 (QB n=36) |
| RB rush | 23 car | — | 161 | 7.0 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| T.Stukes | SAF | 4 | 102 | 2 | 1 | 0 | 0 | G.Wilson×2, M.Taylor×1, A.Mitchell×1 |
| J.Chinn | SAF | 3 | 37 | 0 | 0 | 1 | 0 | M.Taylor×1, G.Wilson×2 |
| E.Stokes | CB | 4 | 30 | 1 | 2 | 0 | 0 | G.Wilson×2, A.Mitchell×1, M.Taylor×1 |
| N.Dean | LB | 2 | 28 | 0 | 0 | 0 | 0 | A.Mitchell×1, B.Allen×1 |
| T.Eichenberg | LB | 1 | 22 | 1 | 1 | 0 | 0 | K.Sadiq×1 |
| J.McCoy | CB | 1 | 22 | 1 | 0 | 0 | 1 | A.Mitchell×1 |
| H.Masses | CB | 0 | 0 | 0 | 1 | 0 | 0 |  |
| Q.Walker | LB | 1 | -5 | 0 | 0 | 0 | 0 | B.Allen×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Darien Porter ← Adonai Mitchell: 9 tgt, 7 rec, 142 yds
- Eric Stokes ← Garrett Wilson: 11 tgt, 6 rec, 83 yds
