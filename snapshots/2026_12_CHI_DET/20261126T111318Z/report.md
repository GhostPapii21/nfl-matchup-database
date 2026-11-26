# Locked snapshot CHI @ DET (2026_12_CHI_DET)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T11:13:18+00:00  | kickoff (UTC): 2026-11-26T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `chi_det_2026-11-26_data_only_nfl43`; code commit `2b33647ccd84ef8515e122c291705fdfe7b1d2cd`
- Trials: 100,000 in 7 chunks, seed 537948638, runtime 639.7 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| DET points | 29.70 |
| CHI points | 21.63 |
| home margin | 8.07 (sd 14.24) |
| total | 51.33 (sd 12.72) |
| P(home win) / P(away win) / P(tie) | 0.711 / 0.282 / 0.0072 |
| P(OT) | 0.037 |
| penalties per game / yards home, away | 12.28 / 44.8, 47.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | DET | 1.5 | 0.739 | 0.5 |
| spread | pinnacle (ref) | DET | 1.5 | 0.739 | 0.5034 |
| spread | consensus | DET | 1.5 | 0.739 | 0.5011 |
| spread | draftkings | DET | 1.5 | 0.739 | 0.5076 |
| spread | betrivers | DET | 1.5 | 0.739 | 0.4946 |
| spread | bet365 | DET | 1.5 | 0.739 | 0.5043 |
| spread | williamhill_us | DET | 1.5 | 0.739 | 0.5011 |
| spread | open | DET | -2.5 | 0.676 | 0.5108 |
| spread | betmgm | DET | 1.0 | 0.718 | 0.4978 |
| total | fanduel | Over | 55.5 | 0.353 | 0.5042 |
| total | pinnacle (ref) | Over | 55.5 | 0.353 | 0.4955 |
| total | consensus | Over | 55.5 | 0.353 | 0.4956 |
| total | draftkings | Over | 55.5 | 0.353 | 0.488 |
| total | betrivers | Over | 55.5 | 0.353 | 0.4925 |
| total | betmgm | Over | 55.5 | 0.353 | 0.4978 |
| total | bet365 | Over | 55.5 | 0.353 | 0.4935 |
| total | williamhill_us | Over | 55.5 | 0.353 | 0.4935 |
| total | open | Over | 53.5 | 0.433 | 0.5 |
| moneyline | fanduel | DET |  | 0.716 | 0.4715 |
| moneyline | pinnacle (ref) | DET |  | 0.716 | 0.474 |
| moneyline | consensus | DET |  | 0.716 | 0.4773 |
| moneyline | open | DET |  | 0.716 | 0.5564 |
| moneyline | draftkings | DET |  | 0.716 | 0.477 |
| moneyline | betrivers | DET |  | 0.716 | 0.4658 |
| moneyline | betmgm | DET |  | 0.716 | 0.4783 |
| moneyline | bet365 | DET |  | 0.716 | 0.4718 |
| moneyline | williamhill_us | DET |  | 0.716 | 0.4634 |

Market divergence: {'max_abs_moneyline_gap': 0.2525937950763529, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
