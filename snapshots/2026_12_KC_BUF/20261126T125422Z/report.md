# Locked snapshot KC @ BUF (2026_12_KC_BUF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:54:22+00:00  | kickoff (UTC): 2026-11-27T01:20:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `kc_buf_2026-11-26_data_only_nfl43`; code commit `46b799460a56ad1d76a8e794fce8d25dd1d28530`
- Trials: 100,000 in 4 chunks, seed 1700585865, runtime 772.3 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| BUF points | 29.79 |
| KC points | 33.02 |
| home margin | -3.23 (sd 14.64) |
| total | 62.81 (sd 13.49) |
| P(home win) / P(away win) / P(tie) | 0.409 / 0.585 / 0.0059 |
| P(OT) | 0.035 |
| penalties per game / yards home, away | 14.83 / 62.6, 57.6 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Kansas City Chiefs | 2.5 | 0.631 | 0.4812 |
| spread | pinnacle (ref) | Kansas City Chiefs | 3.0 | 0.631 | 0.5171 |
| spread | open (ref) | Kansas City Chiefs | 2.5 | 0.631 | 0.4892 |
| spread | betrivers | Kansas City Chiefs | 2.5 | 0.631 | 0.4819 |
| spread | bet365 | Kansas City Chiefs | 2.5 | 0.631 | 0.4739 |
| spread | consensus (ref) | Kansas City Chiefs | 3.0 | 0.631 | 0.5164 |
| spread | draftkings | Kansas City Chiefs | 3.0 | 0.631 | 0.5142 |
| spread | betmgm | Kansas City Chiefs | 3.0 | 0.631 | 0.5174 |
| spread | williamhill_us | Kansas City Chiefs | 3.0 | 0.631 | 0.5174 |
| total | fanduel | Over | 45.5 | 0.903 | 0.5 |
| total | pinnacle (ref) | Over | 45.5 | 0.903 | 0.5067 |
| total | consensus (ref) | Over | 45.5 | 0.903 | 0.5 |
| total | draftkings | Over | 45.5 | 0.903 | 0.4989 |
| total | betmgm | Over | 45.5 | 0.903 | 0.5 |
| total | bet365 | Over | 45.5 | 0.903 | 0.5 |
| total | williamhill_us | Over | 45.5 | 0.903 | 0.5065 |
| total | betrivers | Over | 46.5 | 0.893 | 0.4946 |
| total | open (ref) | Over | 50.5 | 0.820 | 0.5 |
| moneyline | fanduel | Kansas City Chiefs |  | 0.589 | 0.421 |
| moneyline | pinnacle (ref) | Kansas City Chiefs |  | 0.589 | 0.417 |
| moneyline | consensus (ref) | Kansas City Chiefs |  | 0.589 | 0.417 |
| moneyline | open (ref) | Kansas City Chiefs |  | 0.589 | 0.4255 |
| moneyline | draftkings | Kansas City Chiefs |  | 0.589 | 0.4176 |
| moneyline | betrivers | Kansas City Chiefs |  | 0.589 | 0.429 |
| moneyline | betmgm | Kansas City Chiefs |  | 0.589 | 0.417 |
| moneyline | bet365 | Kansas City Chiefs |  | 0.589 | 0.417 |
| moneyline | williamhill_us | Kansas City Chiefs |  | 0.589 | 0.417 |

Market divergence: {'max_abs_moneyline_gap': 0.17174123552667325, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
