# Locked snapshot MIN @ SF (2026_11_MIN_SF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T16:05:35+00:00  | kickoff (UTC): 2026-11-23T01:20:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `min_sf_2026-11-22_data_only_nfl43`; code commit `c13b9929a4965a684846ff0edbca49e8e0ea9eb2`
- Trials: 100,000 in 4 chunks, seed 434450187, runtime 1157.4 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| SF points | 30.34 |
| MIN points | 16.94 |
| home margin | 13.40 (sd 13.77) |
| total | 47.28 (sd 12.84) |
| P(home win) / P(away win) / P(tie) | 0.834 / 0.160 / 0.0062 |
| P(OT) | 0.026 |
| penalties per game / yards home, away | 11.17 / 48.9, 38.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | SF | -3.5 | 0.775 | 0.4761 |
| spread | williamhill_us | SF | -3.5 | 0.775 | 0.4807 |
| total | fanduel | Over | 46.5 | 0.523 | 0.5188 |
| total | pinnacle (ref) | Over | 46.0 | 0.523 | 0.5068 |
| total | williamhill_us | Over | 46.5 | 0.523 | 0.4946 |
| moneyline | fanduel | SF |  | 0.839 | 0.5996 |
| moneyline | williamhill_us | SF |  | 0.839 | 0.6073 |

Market divergence: {'max_abs_moneyline_gap': 0.23976046043628751, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
