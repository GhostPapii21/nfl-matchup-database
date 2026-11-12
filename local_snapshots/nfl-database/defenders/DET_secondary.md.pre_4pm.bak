# DET secondary / defense coverage ledger
Created 2026-11-01 by wk8 dissection. Method: see defenders/CAR_secondary.md and postmortems/WEEK8_DEFENSE_DISSECTION_2026-11-01.md.


## Week 8 (2026-11-01) — DET defense vs MIN (MIN@DET)
Appended 2026-11-01; season numbers above are untouched. Sources: ESPN summary API play-by-play (single source), pregame matchups week8/breakdown/coverage/coverage.json + ESPN cheat sheet, nflverse pbp wk1–7 for QB baselines. Freshness: coverage tendencies are from 10/27–10/29 pulls, older than 48h → STALE for shell; Week 8 FTN not released.
**Explosives allowed (rush 15+/rec 20+): 4** (1 rush, 3 rec)
- Q1 15:00 Ben Yurosek (TE) rec 24 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q1 0:51 T.J. Hockenson (TE) rec 22 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 2:00 Kyler Murray (QB) rush 22 — R.Ya-Sin [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: ?
- Q4 10:16 Jordan Addison (WR) rec 51 — D.J. Reed [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Ennis Rakestraw)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L35/S32/R33)

**Yards allowed by position (QB-adjusted, features.py residual method):** YPT vs this D minus the passer's own wk1–7 YPT to that group (fallback: league YPT when <8 tgts). Positive = worse than that QB normally gets.

| Group | Tgt | Rec | Yds | QB-adj YPT resid | QB baseline |
|---|---|---|---|---|---|
| WR_out | 16 | 7 | 53 | -4.79 | K.Murray base 8.1 (QB n=51) |
| WR_mid | 2 | 2 | 56 | 17.77 | K.Murray base 10.2 (league fallback) |
| TE | 7 | 5 | 82 | 4.35 | K.Murray base 7.4 (QB n=33) |
| RB | 0 | 0 | 0 | — |  |
| RB rush | 7 car | — | 22 | 3.14 ypc | — |

WR_out/WR_mid split uses ESPN pass_location (left/right=outside proxy, middle=slot/middle proxy), the same proxy as the season WR_outside/WR_middle numbers.

**Defenders (ESPN-text proxy; per-defender targets are NOT public free — PFF/FTN-premium only):** catches/yards = first tackler after the catch (CAR_secondary.md method), PBU = named on an incompletion.

| Defender | Pos | Rec charged | Yds | 20+ | PBU | INT | Pen (DPI/hold/IC) | Receivers |
|---|---|---|---|---|---|---|---|---|
| K.Dorsey | CB | 1 | 51 | 1 | 0 | 0 | 0 | J.Addison×1 |
| R.McCreary | CB | 4 | 42 | 1 | 0 | 0 | 0 | B.Yurosek×1, J.Jennings×1, J.Jefferson×1, J.Addison×1 |
| B.Branch | CB | 1 | 22 | 1 | 0 | 0 | 0 | T.Hockenson×1 |
| J.Rolder | LB | 2 | 20 | 0 | 0 | 0 | 0 | A.Jones×1, J.Jennings×1 |
| R.Ya-Sin | CB | 1 | 18 | 0 | 0 | 0 | 0 | T.Hockenson×1 |
| D.Reed | CB | 1 | 11 | 0 | 2 | 1 | 0 | J.Addison×1 |
| M.Rodriguez | LB | 1 | 3 | 0 | 0 | 0 | 0 | A.Jones×1 |

**Inferred matchups (labeled INFERRED: receiver's line when targeted vs his pregame primary defender):**
- D.J. Reed ← Jordan Addison: 7 tgt, 3 rec, 66 yds
- Ennis Rakestraw Jr. ← Justin Jefferson: 8 tgt, 4 rec, 32 yds — limited his man
- Roger McCreary ← Jauan Jennings: 2 tgt, 2 rec, 11 yds
