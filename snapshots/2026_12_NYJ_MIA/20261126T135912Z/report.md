# Locked snapshot NYJ @ MIA (2026_12_NYJ_MIA)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:59:12+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `nyj_mia_2026-11-29_data_only_nfl43`; code commit `afde6cbd108ad2e72e8c49fd576c8bda311fd6fd`
- Trials: 100,000 in 4 chunks, seed 2122944308, runtime 733.6 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| MIA points | 16.79 |
| NYJ points | 22.96 |
| home margin | -6.16 (sd 12.98) |
| total | 39.75 (sd 11.67) |
| P(home win) / P(away win) / P(tie) | 0.314 / 0.677 / 0.0095 |
| P(OT) | 0.038 |
| penalties per game / yards home, away | 13.80 / 40.4, 55.4 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New York Jets | -4.5 | 0.553 | 0.5 |
| spread | pinnacle (ref) | New York Jets | -5.5 | 0.534 | 0.5034 |
| spread | consensus (ref) | New York Jets | -4.5 | 0.553 | 0.4989 |
| spread | draftkings | New York Jets | -4.5 | 0.553 | 0.4902 |
| spread | betmgm | New York Jets | -4.5 | 0.553 | 0.5022 |
| spread | bet365 | New York Jets | -4.5 | 0.553 | 0.4957 |
| spread | williamhill_us | New York Jets | -4.5 | 0.553 | 0.4989 |
| spread | open (ref) | New York Jets | 1.5 | 0.713 | 0.5 |
| spread | betrivers | New York Jets | -5.0 | 0.534 | 0.4957 |
| total | fanduel | Over | 40.5 | 0.453 | 0.5104 |
| total | pinnacle (ref) | Over | 40.5 | 0.453 | 0.4978 |
| total | consensus (ref) | Over | 40.5 | 0.453 | 0.4978 |
| total | open (ref) | Over | 40.5 | 0.453 | 0.5 |
| total | draftkings | Over | 40.5 | 0.453 | 0.488 |
| total | betrivers | Over | 40.5 | 0.453 | 0.5064 |
| total | betmgm | Over | 40.5 | 0.453 | 0.4978 |
| total | bet365 | Over | 40.5 | 0.453 | 0.4978 |
| total | williamhill_us | Over | 40.5 | 0.453 | 0.5 |
| moneyline | fanduel | New York Jets |  | 0.683 | 0.669 |
| moneyline | pinnacle (ref) | New York Jets |  | 0.683 | 0.6803 |
| moneyline | consensus (ref) | New York Jets |  | 0.683 | 0.6696 |
| moneyline | draftkings | New York Jets |  | 0.683 | 0.6571 |
| moneyline | betrivers | New York Jets |  | 0.683 | 0.6853 |
| moneyline | betmgm | New York Jets |  | 0.683 | 0.6704 |
| moneyline | bet365 | New York Jets |  | 0.683 | 0.6704 |
| moneyline | williamhill_us | New York Jets |  | 0.683 | 0.6629 |

Market divergence: {'max_abs_moneyline_gap': 0.02623753975064358, 'flag': 'WITHIN_0.15'}

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
