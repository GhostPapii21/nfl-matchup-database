# Locked snapshot PHI @ DAL (2026_12_PHI_DAL)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T11:22:20+00:00  | kickoff (UTC): 2026-11-26T21:30:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `phi_dal_2026-11-26_data_only_nfl43`; code commit `25e0655ebea1d1b659eed1bab9ef766a5eb49e41`
- Trials: 100,000 in 4 chunks, seed 258085159, runtime 924.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| DAL points | 28.56 |
| PHI points | 16.99 |
| home margin | 11.57 (sd 13.24) |
| total | 45.55 (sd 11.42) |
| P(home win) / P(away win) / P(tie) | 0.807 / 0.188 / 0.0052 |
| P(OT) | 0.027 |
| penalties per game / yards home, away | 13.91 / 53.2, 45.8 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Philadelphia Eagles | 8.5 | 0.405 | 0.4958 |
| spread | pinnacle (ref) | Philadelphia Eagles | 9.0 | 0.405 | 0.5011 |
| spread | consensus (ref) | Philadelphia Eagles | 8.5 | 0.405 | 0.5 |
| spread | draftkings | Philadelphia Eagles | 8.5 | 0.405 | 0.4967 |
| spread | betrivers | Philadelphia Eagles | 8.5 | 0.405 | 0.4989 |
| spread | betmgm | Philadelphia Eagles | 8.5 | 0.405 | 0.5022 |
| spread | bet365 | Philadelphia Eagles | 8.5 | 0.405 | 0.4978 |
| spread | williamhill_us | Philadelphia Eagles | 8.5 | 0.405 | 0.4989 |
| spread | open (ref) | Philadelphia Eagles | 1.5 | 0.208 | 0.5108 |
| total | fanduel | Over | 48.5 | 0.390 | 0.4958 |
| total | pinnacle (ref) | Over | 49.0 | 0.364 | 0.5 |
| total | consensus (ref) | Over | 48.5 | 0.390 | 0.5011 |
| total | draftkings | Over | 48.5 | 0.390 | 0.512 |
| total | bet365 | Over | 48.5 | 0.390 | 0.5 |
| total | open (ref) | Over | 49.5 | 0.364 | 0.5108 |
| total | betrivers | Over | 48.0 | 0.390 | 0.4957 |
| total | betmgm | Over | 48.0 | 0.390 | 0.4978 |
| total | williamhill_us | Over | 48.0 | 0.390 | 0.5162 |
| moneyline | fanduel | Philadelphia Eagles |  | 0.189 | 0.2045 |
| moneyline | pinnacle (ref) | Philadelphia Eagles |  | 0.189 | 0.2166 |
| moneyline | consensus (ref) | Philadelphia Eagles |  | 0.189 | 0.2066 |
| moneyline | draftkings | Philadelphia Eagles |  | 0.189 | 0.218 |
| moneyline | betrivers | Philadelphia Eagles |  | 0.189 | 0.219 |
| moneyline | betmgm | Philadelphia Eagles |  | 0.189 | 0.2031 |
| moneyline | bet365 | Philadelphia Eagles |  | 0.189 | 0.2086 |
| moneyline | williamhill_us | Philadelphia Eagles |  | 0.189 | 0.2167 |

Market divergence: {'max_abs_moneyline_gap': 0.030204487424355136, 'flag': 'WITHIN_0.15'}

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
