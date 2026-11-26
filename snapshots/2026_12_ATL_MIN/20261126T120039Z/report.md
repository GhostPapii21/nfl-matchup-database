# Locked snapshot ATL @ MIN (2026_12_ATL_MIN)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:00:39+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `atl_min_2026-11-29_data_only_nfl43`; code commit `668ef51c74534c968bfa11294d59c6ede707a80e`
- Trials: 100,000 in 4 chunks, seed 1903508734, runtime 765.1 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| MIN points | 20.82 |
| ATL points | 21.64 |
| home margin | -0.82 (sd 13.72) |
| total | 42.45 (sd 12.21) |
| P(home win) / P(away win) / P(tie) | 0.469 / 0.520 / 0.0111 |
| P(OT) | 0.044 |
| penalties per game / yards home, away | 10.28 / 40.1, 41.2 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Atlanta Falcons | 7.0 | 0.692 | 0.5108 |
| spread | pinnacle (ref) | Atlanta Falcons | 7.0 | 0.692 | 0.5092 |
| spread | consensus (ref) | Atlanta Falcons | 7.0 | 0.692 | 0.5142 |
| spread | draftkings | Atlanta Falcons | 7.0 | 0.692 | 0.5217 |
| spread | betmgm | Atlanta Falcons | 7.0 | 0.692 | 0.5174 |
| spread | williamhill_us | Atlanta Falcons | 7.0 | 0.692 | 0.5152 |
| spread | betrivers | Atlanta Falcons | 6.5 | 0.692 | 0.4872 |
| spread | bet365 | Atlanta Falcons | 6.5 | 0.692 | 0.4805 |
| spread | open (ref) | Atlanta Falcons | 4.5 | 0.652 | 0.5 |
| total | fanduel | Over | 41.5 | 0.509 | 0.5 |
| total | pinnacle (ref) | Over | 41.5 | 0.509 | 0.5 |
| total | consensus (ref) | Over | 41.5 | 0.509 | 0.5022 |
| total | draftkings | Over | 41.5 | 0.509 | 0.5065 |
| total | betrivers | Over | 41.5 | 0.509 | 0.5022 |
| total | betmgm | Over | 41.5 | 0.509 | 0.5022 |
| total | bet365 | Over | 41.5 | 0.509 | 0.5043 |
| total | williamhill_us | Over | 41.5 | 0.509 | 0.5108 |
| total | open (ref) | Over | 43.5 | 0.455 | 0.5 |
| moneyline | fanduel | Atlanta Falcons |  | 0.525 | 0.2631 |
| moneyline | pinnacle (ref) | Atlanta Falcons |  | 0.525 | 0.2646 |
| moneyline | consensus (ref) | Atlanta Falcons |  | 0.525 | 0.2665 |
| moneyline | open (ref) | Atlanta Falcons |  | 0.525 | 0.3425 |
| moneyline | draftkings | Atlanta Falcons |  | 0.525 | 0.2731 |
| moneyline | betrivers | Atlanta Falcons |  | 0.525 | 0.2735 |
| moneyline | betmgm | Atlanta Falcons |  | 0.525 | 0.2665 |
| moneyline | bet365 | Atlanta Falcons |  | 0.525 | 0.2631 |
| moneyline | williamhill_us | Atlanta Falcons |  | 0.525 | 0.2665 |

Market divergence: {'max_abs_moneyline_gap': 0.2622450629455483, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
