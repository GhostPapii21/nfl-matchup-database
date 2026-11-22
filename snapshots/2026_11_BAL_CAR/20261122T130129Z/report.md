# Locked snapshot BAL @ CAR (2026_11_BAL_CAR)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T13:01:29+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `bal_car_2026-11-22_data_only_nfl43`; code commit `02316aa796743b6caf60fe227b0a04b02268c0f3`
- Trials: 100,000 in 4 chunks, seed 1652207772, runtime 1236.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| CAR points | 23.60 |
| BAL points | 24.18 |
| home margin | -0.58 (sd 14.64) |
| total | 47.78 (sd 12.70) |
| P(home win) / P(away win) / P(tie) | 0.479 / 0.514 / 0.0068 |
| P(OT) | 0.033 |
| penalties per game / yards home, away | 15.58 / 55.3, 58.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | CAR | -2.5 | 0.435 | 0.5188 |
| spread | williamhill_us | CAR | -3.0 | 0.396 | 0.4838 |
| total | fanduel | Over | 43.5 | 0.623 | 0.5104 |
| total | pinnacle (ref) | Over | 43.5 | 0.623 | 0.5068 |
| total | williamhill_us | Over | 43.5 | 0.623 | 0.5087 |
| moneyline | fanduel | CAR |  | 0.482 | 0.5707 |
| moneyline | williamhill_us | CAR |  | 0.482 | 0.5766 |

Market divergence: {'max_abs_moneyline_gap': 0.09415905036145067, 'flag': 'WITHIN_0.15'}

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
