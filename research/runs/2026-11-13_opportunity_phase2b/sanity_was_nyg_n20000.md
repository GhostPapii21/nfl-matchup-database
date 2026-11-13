# WAS@NYG 2026-11-12 sanity table, Phase 2b (projection only, Week 10 never graded)

Same engine run for both columns: n=20000, seed=20261112, runtime 801s. Model `model_2026_w10_WAS_NYG.json` sha256 1f9783165a421ee3 (fit on 2024-2025 + 2026 Weeks 1-9). Reconciliation failures: name-locked 0/20000, opportunity 0/20000. The engine runs WITH opt-in INT pooling (league rate 0.0221, m 1200), so 'main' here is the name-locked recorder on the INT-pooled engine; see ../2026-11-13_opportunity_phase2/sanity_was_nyg_n20000.md for main without pooling and the Phase 2 model.

## NYG

Team totals per game (identical in both recorders): pass_att 33.3, targets 33.0, carries 27.0.

| player | pos | report status | pass_att main | pass_att opp | P(INT>=1) main | P(INT>=1) opp | carries main | carries opp | targets main | targets opp | rz targets opp | i5 carries opp | P(any TD) opp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J.McCarthy | QB | - | 8.3 | 28.8 | 0.087 | 0.489 | 1.1 | 3.2 | 0.0 | 0.0 | 0.00 | 0.12 | 0.062 |
| C.Skattebo | RB | - | 0.0 | 0.0 | 0.000 | 0.000 | 11.8 | 13.5 | 1.9 | 2.0 | 0.25 | 0.41 | 0.389 |
| UNLISTED | UNLISTED | - | 0.0 | 2.1 | 0.000 | 0.037 | 0.0 | 1.9 | 0.0 | 3.1 | 0.33 | 0.06 | 0.185 |
| M.Nabers | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 10.2 | 9.1 | 0.82 | 0.00 | 0.282 |
| D.Singletary | RB | - | 0.0 | 0.0 | 0.000 | 0.000 | 4.7 | 6.7 | 1.4 | 1.9 | 0.22 | 0.20 | 0.231 |
| J.Winston | QB | - | 21.1 | 2.4 | 0.516 | 0.047 | 1.5 | 0.3 | 0.0 | 0.0 | 0.00 | 0.01 | 0.005 |
| I.Likely | TE | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 9.0 | 7.5 | 0.98 | 0.00 | 0.419 |
| M.Fields | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 4.0 | 4.7 | 0.47 | 0.00 | 0.212 |
| D.Mooney | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.5 | 0.8 | 3.3 | 3.4 | 0.23 | 0.01 | 0.139 |
| J.Hyatt | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 0.1 | 1.2 | 0.12 | 0.00 | 0.055 |
| G.Desrosiers | RB | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.4 | 0.6 | 0.0 | 0.0 | 0.00 | 0.02 | 0.015 |
| J.Dart | not a candidate | n/a | 4.0 | 0.0 | 0.000 | 0.000 | 1.1 | 0.0 | 0.0 | 0.0 | 0.00 | 0.00 | 0.000 |
| N.Harris | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 3.9 | 0.0 | 0.1 | 0.0 | 0.00 | 0.00 | 0.000 |
| T.Johnson | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 1.0 | 0.0 | 0.00 | 0.00 | 0.000 |
| T.Tracy | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 2.1 | 0.0 | 0.8 | 0.0 | 0.00 | 0.00 | 0.000 |

## WAS

Team totals per game (identical in both recorders): pass_att 34.6, targets 32.6, carries 27.0.

| player | pos | report status | pass_att main | pass_att opp | P(INT>=1) main | P(INT>=1) opp | carries main | carries opp | targets main | targets opp | rz targets opp | i5 carries opp | P(any TD) opp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J.Daniels | QB | - | 22.3 | 31.7 | 0.280 | 0.482 | 3.6 | 4.2 | 0.0 | 0.0 | 0.00 | 0.09 | 0.136 |
| R.White | RB | - | 0.0 | 0.0 | 0.000 | 0.000 | 7.2 | 12.9 | 2.5 | 2.8 | 0.32 | 0.38 | 0.294 |
| UNLISTED | UNLISTED | - | 0.0 | 2.9 | 0.000 | 0.055 | 0.0 | 2.0 | 0.0 | 3.1 | 0.32 | 0.06 | 0.176 |
| A.Ekeler | RB | - | 0.0 | 0.0 | 0.000 | 0.000 | 3.1 | 8.0 | 1.1 | 1.7 | 0.16 | 0.23 | 0.191 |
| S.Diggs | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 6.3 | 6.3 | 0.79 | 0.00 | 0.420 |
| C.Okonkwo | TE | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 4.1 | 5.8 | 0.45 | 0.00 | 0.167 |
| A.Williams | WR | - | 0.1 | 0.0 | 0.002 | 0.000 | 0.0 | 0.0 | 5.7 | 4.8 | 0.44 | 0.00 | 0.205 |
| T.Burks | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 2.6 | 3.7 | 0.36 | 0.00 | 0.181 |
| V.Jefferson | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 0.9 | 3.4 | 0.31 | 0.00 | 0.146 |
| L.McCaffrey | WR | - | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 0.3 | 0.7 | 0.07 | 0.00 | 0.037 |
| A.Kaliakmanis | not a candidate | n/a | 4.6 | 0.0 | 0.253 | 0.000 | 0.3 | 0.0 | 0.0 | 0.0 | 0.00 | 0.00 | 0.000 |
| C.Yankoff | TE | Out | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 0.9 | 0.0 | 0.00 | 0.00 | 0.000 |
| D.Brown | not a candidate | n/a | 0.1 | 0.0 | 0.002 | 0.000 | 0.0 | 0.0 | 2.2 | 0.0 | 0.00 | 0.00 | 0.000 |
| J.Bates | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 0.9 | 0.0 | 0.00 | 0.00 | 0.000 |
| J.Croskey-Merritt | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 9.1 | 0.0 | 0.8 | 0.0 | 0.00 | 0.00 | 0.000 |
| J.McNichols | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 1.2 | 0.0 | 0.2 | 0.0 | 0.00 | 0.00 | 0.000 |
| K.Allen | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 1.6 | 0.0 | 0.0 | 0.0 | 0.00 | 0.00 | 0.000 |
| M.Mariota | not a candidate | n/a | 7.5 | 0.0 | 0.107 | 0.000 | 0.6 | 0.0 | 0.0 | 0.0 | 0.00 | 0.00 | 0.000 |
| T.McLaurin | not a candidate | n/a | 0.0 | 0.0 | 0.000 | 0.000 | 0.0 | 0.0 | 3.6 | 0.0 | 0.00 | 0.00 | 0.000 |

UNASSIGNED (main) = rows whose names the engine nulled (foreign rows) or that had no name; UNLISTED (opp) = the fitted share for players outside the candidate list. Snaps: unknown (no snap model; nflverse snap counts in the repo stop at Week 7).
