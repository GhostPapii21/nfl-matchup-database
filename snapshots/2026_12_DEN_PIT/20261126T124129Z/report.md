# Locked snapshot DEN @ PIT (2026_12_DEN_PIT)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:41:29+00:00  | kickoff (UTC): 2026-11-27T20:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `den_pit_2026-11-27_data_only_nfl43`; code commit `668ef51c74534c968bfa11294d59c6ede707a80e`
- Trials: 100,000 in 4 chunks, seed 1969908846, runtime 812.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| PIT points | 20.01 |
| DEN points | 20.23 |
| home margin | -0.22 (sd 13.11) |
| total | 40.23 (sd 11.76) |
| P(home win) / P(away win) / P(tie) | 0.486 / 0.503 / 0.0117 |
| P(OT) | 0.045 |
| penalties per game / yards home, away | 12.71 / 46.8, 48.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Denver Broncos | -3.5 | 0.414 | 0.5042 |
| spread | pinnacle (ref) | Denver Broncos | -4.0 | 0.370 | 0.5092 |
| spread | consensus (ref) | Denver Broncos | -3.5 | 0.414 | 0.5076 |
| spread | draftkings | Denver Broncos | -3.5 | 0.414 | 0.5076 |
| spread | bet365 | Denver Broncos | -3.5 | 0.414 | 0.5108 |
| spread | open (ref) | Denver Broncos | -1.5 | 0.469 | 0.5 |
| spread | betrivers | Denver Broncos | -4.0 | 0.370 | 0.4946 |
| spread | betmgm | Denver Broncos | -4.0 | 0.370 | 0.4978 |
| spread | williamhill_us | Denver Broncos | -4.0 | 0.370 | 0.4957 |
| total | fanduel | Over | 36.5 | 0.616 | 0.5104 |
| total | pinnacle (ref) | Over | 37.0 | 0.561 | 0.4955 |
| total | consensus (ref) | Over | 36.5 | 0.616 | 0.5098 |
| total | draftkings | Over | 36.5 | 0.616 | 0.5098 |
| total | betrivers | Over | 36.5 | 0.616 | 0.5054 |
| total | betmgm | Over | 36.5 | 0.616 | 0.5108 |
| total | bet365 | Over | 36.5 | 0.616 | 0.5087 |
| total | williamhill_us | Over | 36.5 | 0.616 | 0.5065 |
| total | open (ref) | Over | 39.5 | 0.518 | 0.5 |
| moneyline | fanduel | Denver Broncos |  | 0.508 | 0.6411 |
| moneyline | pinnacle (ref) | Denver Broncos |  | 0.508 | 0.6587 |
| moneyline | consensus (ref) | Denver Broncos |  | 0.508 | 0.6479 |
| moneyline | draftkings | Denver Broncos |  | 0.508 | 0.644 |
| moneyline | betrivers | Denver Broncos |  | 0.508 | 0.6368 |
| moneyline | betmgm | Denver Broncos |  | 0.508 | 0.6507 |
| moneyline | bet365 | Denver Broncos |  | 0.508 | 0.6507 |
| moneyline | williamhill_us | Denver Broncos |  | 0.508 | 0.6411 |

Market divergence: {'max_abs_moneyline_gap': 0.15021616330247378, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
