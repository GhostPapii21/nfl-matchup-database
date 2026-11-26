# Locked snapshot CAR @ TB (2026_12_CAR_TB)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:27:56+00:00  | kickoff (UTC): 2026-12-01T01:15:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `car_tb_2026-11-30_data_only_nfl43`; code commit `668ef51c74534c968bfa11294d59c6ede707a80e`
- Trials: 100,000 in 4 chunks, seed 1877844662, runtime 782.1 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| TB points | 18.29 |
| CAR points | 24.91 |
| home margin | -6.62 (sd 14.01) |
| total | 43.20 (sd 12.01) |
| P(home win) / P(away win) / P(tie) | 0.314 / 0.679 / 0.0069 |
| P(OT) | 0.032 |
| penalties per game / yards home, away | 13.57 / 44.7, 55.4 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Carolina Panthers | 3.0 | 0.729 | 0.513 |
| spread | pinnacle (ref) | Carolina Panthers | 3.0 | 0.729 | 0.5069 |
| spread | consensus (ref) | Carolina Panthers | 3.0 | 0.729 | 0.5022 |
| spread | draftkings | Carolina Panthers | 3.0 | 0.729 | 0.5055 |
| spread | betmgm | Carolina Panthers | 3.0 | 0.729 | 0.5022 |
| spread | williamhill_us | Carolina Panthers | 3.0 | 0.729 | 0.5065 |
| spread | open (ref) | Carolina Panthers | 3.5 | 0.757 | 0.5 |
| spread | betrivers | Carolina Panthers | 2.5 | 0.729 | 0.4819 |
| spread | bet365 | Carolina Panthers | 2.5 | 0.729 | 0.4613 |
| total | fanduel | Over | 43.5 | 0.477 | 0.5146 |
| total | pinnacle (ref) | Over | 44.0 | 0.439 | 0.4933 |
| total | consensus (ref) | Over | 43.5 | 0.477 | 0.5022 |
| total | draftkings | Over | 43.5 | 0.477 | 0.5011 |
| total | betrivers | Over | 43.5 | 0.477 | 0.5054 |
| total | betmgm | Over | 43.5 | 0.477 | 0.5022 |
| total | bet365 | Over | 43.5 | 0.477 | 0.5043 |
| total | williamhill_us | Over | 43.5 | 0.477 | 0.5065 |
| total | open (ref) | Over | 44.5 | 0.439 | 0.5 |
| moneyline | fanduel | Carolina Panthers |  | 0.683 | 0.4066 |
| moneyline | pinnacle (ref) | Carolina Panthers |  | 0.683 | 0.4012 |
| moneyline | consensus (ref) | Carolina Panthers |  | 0.683 | 0.4088 |
| moneyline | open (ref) | Carolina Panthers |  | 0.683 | 0.3631 |
| moneyline | draftkings | Carolina Panthers |  | 0.683 | 0.4137 |
| moneyline | betrivers | Carolina Panthers |  | 0.683 | 0.4324 |
| moneyline | betmgm | Carolina Panthers |  | 0.683 | 0.4088 |
| moneyline | bet365 | Carolina Panthers |  | 0.683 | 0.404 |
| moneyline | williamhill_us | Carolina Panthers |  | 0.683 | 0.4104 |

Market divergence: {'max_abs_moneyline_gap': 0.3203727970274597, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
