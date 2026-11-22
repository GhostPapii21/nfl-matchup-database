# Locked snapshot MIN @ SF (2026_11_MIN_SF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T13:49:18+00:00  | kickoff (UTC): 2026-11-23T01:20:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `min_sf_2026-11-22_data_only_nfl43`; code commit `0b5052dee2b624b9a1b679f90e815e6073180518`
- Trials: 100,000 in 7 chunks, seed 434450187, runtime 522.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| SF points | 30.33 |
| MIN points | 16.96 |
| home margin | 13.38 (sd 13.80) |
| total | 47.29 (sd 12.85) |
| P(home win) / P(away win) / P(tie) | 0.834 / 0.160 / 0.0062 |
| P(OT) | 0.026 |
| penalties per game / yards home, away | 11.19 / 49.0, 38.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | SF | -3.5 | 0.775 | 0.4761 |
| spread | williamhill_us | SF | -3.5 | 0.775 | 0.4807 |
| total | fanduel | Over | 46.5 | 0.522 | 0.5188 |
| total | pinnacle (ref) | Over | 46.0 | 0.522 | 0.5068 |
| total | williamhill_us | Over | 46.5 | 0.522 | 0.4946 |
| moneyline | fanduel | SF |  | 0.839 | 0.5996 |
| moneyline | williamhill_us | SF |  | 0.839 | 0.6073 |

Market divergence: {'max_abs_moneyline_gap': 0.23959785073905993, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
