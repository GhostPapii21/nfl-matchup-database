# Locked snapshot DEN @ PIT (2026_12_DEN_PIT)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-27T11:16:48+00:00  | kickoff (UTC): 2026-11-27T20:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `den_pit_2026-11-27_data_only_nfl43`; code commit `aa60efa49fce9f309f2d7ab6559912d9de2b9896`
- Trials: 100,000 in 7 chunks, seed 1969908846, runtime 819.2 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `e0f532a73338bbd4...`

| | mean |
|---|---|
| PIT points | 20.01 |
| DEN points | 20.22 |
| home margin | -0.21 (sd 13.11) |
| total | 40.22 (sd 11.74) |
| P(home win) / P(away win) / P(tie) | 0.487 / 0.502 / 0.0117 |
| P(OT) | 0.045 |
| penalties per game / yards home, away | 12.69 / 46.8, 48.4 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | PIT | 4.5 | 0.631 | 0.5 |
| spread | pinnacle (ref) | PIT | 4.5 | 0.631 | 0.4954 |
| spread | consensus | PIT | 4.5 | 0.631 | 0.5 |
| spread | draftkings | PIT | 4.5 | 0.631 | 0.4826 |
| spread | bet365 | PIT | 4.5 | 0.631 | 0.4935 |
| spread | williamhill_us | PIT | 4.5 | 0.631 | 0.4913 |
| spread | open | PIT | 1.5 | 0.532 | 0.5 |
| spread | betrivers | PIT | 5.5 | 0.649 | 0.5054 |
| spread | betmgm | PIT | 5.0 | 0.631 | 0.5022 |
| total | fanduel | Over | 36.5 | 0.616 | 0.5146 |
| total | pinnacle (ref) | Over | 37.0 | 0.562 | 0.4955 |
| total | draftkings | Over | 36.5 | 0.616 | 0.5195 |
| total | betrivers | Over | 36.5 | 0.616 | 0.5065 |
| total | bet365 | Over | 36.5 | 0.616 | 0.5152 |
| total | open | Over | 39.5 | 0.519 | 0.5 |
| total | consensus | Over | 37.0 | 0.562 | 0.5054 |
| total | betmgm | Over | 37.0 | 0.562 | 0.4978 |
| total | williamhill_us | Over | 37.0 | 0.562 | 0.4957 |
| moneyline | fanduel | PIT |  | 0.492 | 0.3265 |
| moneyline | pinnacle (ref) | PIT |  | 0.492 | 0.3384 |
| moneyline | consensus | PIT |  | 0.492 | 0.326 |
| moneyline | draftkings | PIT |  | 0.492 | 0.3151 |
| moneyline | betrivers | PIT |  | 0.492 | 0.3076 |
| moneyline | betmgm | PIT |  | 0.492 | 0.3296 |
| moneyline | bet365 | PIT |  | 0.492 | 0.3244 |
| moneyline | williamhill_us | PIT |  | 0.492 | 0.3273 |

Market divergence: {'max_abs_moneyline_gap': 0.18473571103354075, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
