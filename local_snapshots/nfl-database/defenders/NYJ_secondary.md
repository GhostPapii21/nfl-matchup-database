# NYJ secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — NYJ defense vs LV (LV@NYJ)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (1 rush, 3 rec)
- Q1 8:59 Brock Bowers (TE) rec 23 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 15:00 Brock Bowers (TE) rec 27 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 13:39 Mike Washington Jr. (RB) rush 15 — J.Sherwood [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 15:00 Ashton Jeanty (RB) rec 45 — defender unknown [unknown; no public source]; alignment: backfield (position default)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 2 | 1 | 2 | -6.15 | K.Cousins base 7.2 (QB n=78) |
| WR_mid | 3 | 3 | 36 | 3.95 | K.Cousins base 8.0 (QB n=22) |
| TE | 16 | 12 | 145 | 0.42 | K.Cousins base 8.6 (QB n=93) |
| RB | 4 | 3 | 64 | 9.74 | K.Cousins base 6.3 (QB n=54) |
| RB rush | 21 car | — | 90 | 4.29 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| D.Belton | SAF | 5 | 96 | 2 | 1 | 0 | 0 | B.Bowers×3, M.Mayer×2 |
| J.Sherwood | LB | 2 | 49 | 1 | 0 | 0 | 0 | A.Jeanty×2 |
| M.Fitzpatrick | FS | 3 | 24 | 0 | 1 | 0 | 0 | B.Bowers×1, J.Nailor×1, M.Mayer×1 |
| D.Davis | OLB | 2 | 21 | 0 | 0 | 0 | 0 | A.Jeanty×1, M.Mayer×1 |
| A.Thomas | CB | 1 | 12 | 0 | 1 | 0 | 0 | J.Nailor×1 |
| J.Brownlee | DB | 0 | 0 | 0 | 0 | 0 | 1 |  |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- Brandon Stephens ← Jalen Nailor: 4 tgt, 4 rec, 38 yds
- Azareye'h Thomas ← Tre Tucker: 1 tgt, 0 rec, 0 yds
