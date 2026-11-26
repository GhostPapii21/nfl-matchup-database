# Locked snapshot TEN @ JAX (2026_12_TEN_JAX)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T14:25:09+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `ten_jax_2026-11-29_data_only_nfl43`; code commit `afde6cbd108ad2e72e8c49fd576c8bda311fd6fd`
- Trials: 100,000 in 4 chunks, seed 1596433918, runtime 783.6 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| JAX points | 25.19 |
| TEN points | 18.13 |
| home margin | 7.06 (sd 12.93) |
| total | 43.32 (sd 11.49) |
| P(home win) / P(away win) / P(tie) | 0.707 / 0.286 / 0.0073 |
| P(OT) | 0.034 |
| penalties per game / yards home, away | 12.86 / 63.3, 36.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Tennessee Titans | 14.5 | 0.724 | 0.5146 |
| spread | pinnacle (ref) | Tennessee Titans | 14.5 | 0.724 | 0.4977 |
| spread | consensus (ref) | Tennessee Titans | 14.5 | 0.724 | 0.5098 |
| spread | draftkings | Tennessee Titans | 14.5 | 0.724 | 0.513 |
| spread | betrivers | Tennessee Titans | 14.5 | 0.724 | 0.5085 |
| spread | betmgm | Tennessee Titans | 14.5 | 0.724 | 0.5077 |
| spread | bet365 | Tennessee Titans | 14.5 | 0.724 | 0.5065 |
| spread | williamhill_us | Tennessee Titans | 14.5 | 0.724 | 0.5087 |
| spread | open (ref) | Tennessee Titans | 5.5 | 0.445 | 0.5 |
| total | fanduel | Over | 49.5 | 0.294 | 0.4958 |
| total | pinnacle (ref) | Over | 49.5 | 0.294 | 0.5 |
| total | consensus (ref) | Over | 49.5 | 0.294 | 0.4989 |
| total | draftkings | Over | 49.5 | 0.294 | 0.4924 |
| total | betrivers | Over | 49.5 | 0.294 | 0.5032 |
| total | bet365 | Over | 49.5 | 0.294 | 0.4935 |
| total | williamhill_us | Over | 49.5 | 0.294 | 0.4989 |
| total | open (ref) | Over | 45.5 | 0.417 | 0.5 |
| total | betmgm | Over | 49.0 | 0.294 | 0.5022 |
| moneyline | fanduel | Tennessee Titans |  | 0.288 | 0.113 |
| moneyline | pinnacle (ref) | Tennessee Titans |  | 0.288 | 0.1165 |
| moneyline | consensus (ref) | Tennessee Titans |  | 0.288 | 0.1132 |
| moneyline | draftkings | Tennessee Titans |  | 0.288 | 0.1157 |
| moneyline | betrivers | Tennessee Titans |  | 0.288 | 0.1189 |
| moneyline | betmgm | Tennessee Titans |  | 0.288 | 0.1137 |
| moneyline | bet365 | Tennessee Titans |  | 0.288 | 0.113 |
| moneyline | williamhill_us | Tennessee Titans |  | 0.288 | 0.1189 |

Market divergence: {'max_abs_moneyline_gap': 0.17510161774482746, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
