# Locked snapshot CHI @ DET (2026_12_CHI_DET)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T11:06:35+00:00  | kickoff (UTC): 2026-11-26T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `chi_det_2026-11-26_data_only_nfl43`; code commit `25e0655ebea1d1b659eed1bab9ef766a5eb49e41`
- Trials: 100,000 in 4 chunks, seed 537948638, runtime 875.9 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| DET points | 29.70 |
| CHI points | 21.66 |
| home margin | 8.04 (sd 14.26) |
| total | 51.35 (sd 12.73) |
| P(home win) / P(away win) / P(tie) | 0.711 / 0.282 / 0.0077 |
| P(OT) | 0.037 |
| penalties per game / yards home, away | 12.28 / 44.7, 47.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Chicago Bears | -1.5 | 0.261 | 0.5 |
| spread | pinnacle (ref) | Chicago Bears | -1.0 | 0.261 | 0.4977 |
| spread | consensus (ref) | Chicago Bears | -1.5 | 0.261 | 0.4978 |
| spread | draftkings | Chicago Bears | -1.5 | 0.261 | 0.4924 |
| spread | betrivers | Chicago Bears | -1.5 | 0.261 | 0.4968 |
| spread | bet365 | Chicago Bears | -1.5 | 0.261 | 0.4957 |
| spread | williamhill_us | Chicago Bears | -1.5 | 0.261 | 0.4989 |
| spread | open (ref) | Chicago Bears | 2.5 | 0.325 | 0.4892 |
| spread | betmgm | Chicago Bears | -1.0 | 0.261 | 0.5022 |
| total | fanduel | Over | 55.5 | 0.354 | 0.5042 |
| total | pinnacle (ref) | Over | 55.5 | 0.354 | 0.4977 |
| total | consensus (ref) | Over | 55.5 | 0.354 | 0.5033 |
| total | draftkings | Over | 55.5 | 0.354 | 0.5055 |
| total | betmgm | Over | 55.5 | 0.354 | 0.5022 |
| total | bet365 | Over | 55.5 | 0.354 | 0.5022 |
| total | williamhill_us | Over | 55.5 | 0.354 | 0.5043 |
| total | open (ref) | Over | 53.5 | 0.433 | 0.5 |
| total | betrivers | Over | 55.0 | 0.354 | 0.5054 |
| moneyline | fanduel | Chicago Bears |  | 0.284 | 0.5285 |
| moneyline | pinnacle (ref) | Chicago Bears |  | 0.284 | 0.5148 |
| moneyline | consensus (ref) | Chicago Bears |  | 0.284 | 0.5186 |
| moneyline | open (ref) | Chicago Bears |  | 0.284 | 0.4436 |
| moneyline | draftkings | Chicago Bears |  | 0.284 | 0.5166 |
| moneyline | betrivers | Chicago Bears |  | 0.284 | 0.5279 |
| moneyline | betmgm | Chicago Bears |  | 0.284 | 0.5198 |
| moneyline | bet365 | Chicago Bears |  | 0.284 | 0.5195 |
| moneyline | williamhill_us | Chicago Bears |  | 0.284 | 0.5174 |

Market divergence: {'max_abs_moneyline_gap': 0.24466296997974463, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
