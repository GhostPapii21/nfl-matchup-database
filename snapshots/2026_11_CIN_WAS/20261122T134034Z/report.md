# Locked snapshot CIN @ WAS (2026_11_CIN_WAS)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T13:40:34+00:00  | kickoff (UTC): 2026-11-24T01:15:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `cin_was_2026-11-23_data_only_nfl43`; code commit `0b5052dee2b624b9a1b679f90e815e6073180518`
- Trials: 100,000 in 7 chunks, seed 1482608122, runtime 547.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| WAS points | 22.06 |
| CIN points | 30.75 |
| home margin | -8.70 (sd 14.22) |
| total | 52.81 (sd 12.71) |
| P(home win) / P(away win) / P(tie) | 0.263 / 0.732 / 0.0052 |
| P(OT) | 0.028 |
| penalties per game / yards home, away | 13.31 / 50.4, 45.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | WAS | 6.5 | 0.422 | 0.5188 |
| spread | williamhill_us | WAS | 6.0 | 0.405 | 0.4957 |
| total | fanduel | Over | 54.5 | 0.435 | 0.5 |
| total | pinnacle (ref) | Over | 55.0 | 0.401 | 0.4977 |
| total | williamhill_us | Over | 54.0 | 0.435 | 0.5011 |
| moneyline | fanduel | WAS |  | 0.265 | 0.2864 |
| moneyline | williamhill_us | WAS |  | 0.265 | 0.2895 |

Market divergence: {'max_abs_moneyline_gap': 0.024806830175403305, 'flag': 'WITHIN_0.15'}

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
