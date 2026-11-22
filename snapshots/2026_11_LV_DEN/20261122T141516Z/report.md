# Locked snapshot LV @ DEN (2026_11_LV_DEN)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T14:15:16+00:00  | kickoff (UTC): 2026-11-22T21:25:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `lv_den_2026-11-22_data_only_nfl43`; code commit `0b5052dee2b624b9a1b679f90e815e6073180518`
- Trials: 100,000 in 7 chunks, seed 1476728154, runtime 585.1 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| DEN points | 19.86 |
| LV points | 22.09 |
| home margin | -2.23 (sd 13.25) |
| total | 41.95 (sd 12.11) |
| P(home win) / P(away win) / P(tie) | 0.423 / 0.565 / 0.0119 |
| P(OT) | 0.048 |
| penalties per game / yards home, away | 13.51 / 48.6, 43.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | DEN | -10.5 | 0.168 | 0.4854 |
| spread | williamhill_us | DEN | -10.5 | 0.168 | 0.488 |
| total | fanduel | Over | 40.5 | 0.535 | 0.5 |
| total | pinnacle (ref) | Over | 41.0 | 0.488 | 0.5068 |
| total | williamhill_us | Over | 40.5 | 0.535 | 0.4913 |
| moneyline | fanduel | DEN |  | 0.428 | 0.825 |
| moneyline | williamhill_us | DEN |  | 0.428 | 0.8167 |

Market divergence: {'max_abs_moneyline_gap': 0.39696206823265084, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

## Known limits
- Vertical slice: empirical team-only snap resampling + explicit same-team coarser fallbacks
- Clock costs use empirical median deltas when available else fixed means — not a situational clock model
- OT rule: official 2025 regular-season (both possess, then sudden death, ties allowed)
- No league silent pool; proposed pooling config default false
- W1-8 development set; no betting edge claim
- Inspired conceptually by NFLSimulatoR/nflfastR (MIT); no R source copied
- See FEATURE_MATRIX.md for unimplemented coverage/route/pressure fields
- NFL-43 still_unsupported (not invented): kick-play fouls, joint_producer penalties/return yards, blocked kicks/onside/fakes
- data_only config: no injury/inactive adjustment; Phase 15 inactives not applied to the sim
- team scores only; player yards are bootstrap credits, not a player projection model
