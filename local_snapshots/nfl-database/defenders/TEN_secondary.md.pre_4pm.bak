# TEN secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — TEN defense vs CIN (TEN@CIN)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 5** (0 rush, 5 rec)
- Q2 13:20 Ja'Marr Chase (WR) rec 30 — Joshua Williams [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Cordale Flott)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L40/S24/R35)
- Q2 6:51 Tee Higgins (WR) rec 32 — Cordale Flott [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L43/S14/R43)
- Q2 2:12 Mike Gesicki (TE) rec 28 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 8:02 Ja'Marr Chase (WR) rec 23 — Joshua Williams [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Cordale Flott)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L40/S24/R35)
- Q5 8:32 Tee Higgins (WR) rec 21 — Cordale Flott [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L43/S14/R43)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 27 | 22 | 268 | 2.07 | J.Burrow base 7.9 (QB n=98) |
| WR_mid | 3 | 2 | 62 | 8.51 | J.Burrow base 12.2 (QB n=31) |
| TE | 5 | 3 | 51 | 3.01 | J.Burrow base 7.2 (QB n=42) |
| RB | 9 | 8 | 55 | 1.37 | J.Burrow base 4.7 (QB n=43) |
| RB rush | 13 car | — | 64 | 4.92 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| A.Hill | LB | 7 | 94 | 1 | 0 | 0 | 0 | M.Gesicki×1, C.Brown×3, T.Higgins×2, J.Chase×1 |
| C.Flott | CB | 4 | 50 | 0 | 1 | 0 | 0 | T.Higgins×1, C.Brown×1, D.Meyers×1, J.Chase×1 |
| Jo.Williams | CB | 4 | 38 | 0 | 0 | 0 | 0 | J.Chase×2, T.Higgins×2 |
| M.Harris | CB | 1 | 32 | 1 | 0 | 0 | 0 | T.Higgins×1 |
| A.Taylor | CB | 2 | 23 | 0 | 0 | 0 | 0 | J.Chase×2 |
| A.Hooker | SAF | 3 | 21 | 0 | 0 | 3 | 0 | C.Brown×2, D.Meyers×1 |
| C.Gray | LB | 2 | 20 | 0 | 0 | 0 | 0 | T.Higgins×1, J.Chase×1 |
| C.Barton | LB | 1 | 4 | 0 | 0 | 0 | 0 | J.Chase×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Cordale Flott ← Tee Higgins: 11 tgt, 10 rec, 155 yds
- Joshua Williams ← Ja'Marr Chase: 14 tgt, 11 rec, 141 yds
- Marcus X. Harris ← Dohnte Meyers: 3 tgt, 3 rec, 34 yds
