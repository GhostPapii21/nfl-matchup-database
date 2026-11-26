# Locked snapshot PHI @ DAL (2026_12_PHI_DAL)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T11:29:26+00:00  | kickoff (UTC): 2026-11-26T21:30:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `phi_dal_2026-11-26_data_only_nfl43`; code commit `88f8beef5a25012c553eb094c252965ce07ceb38`
- Trials: 100,000 in 3 chunks, seed 258085159, runtime 1175.8 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| DAL points | 28.58 |
| PHI points | 17.00 |
| home margin | 11.58 (sd 13.23) |
| total | 45.58 (sd 11.41) |
| P(home win) / P(away win) / P(tie) | 0.807 / 0.188 / 0.0052 |
| P(OT) | 0.027 |
| penalties per game / yards home, away | 13.90 / 53.2, 45.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Philadelphia Eagles | 8.5 | 0.404 | 0.5 |
| spread | pinnacle (ref) | Philadelphia Eagles | 9.0 | 0.404 | 0.5034 |
| spread | consensus (ref) | Philadelphia Eagles | 8.5 | 0.404 | 0.5 |
| spread | draftkings | Philadelphia Eagles | 8.5 | 0.404 | 0.4967 |
| spread | betrivers | Philadelphia Eagles | 8.5 | 0.404 | 0.4989 |
| spread | betmgm | Philadelphia Eagles | 8.5 | 0.404 | 0.5022 |
| spread | bet365 | Philadelphia Eagles | 8.5 | 0.404 | 0.4978 |
| spread | williamhill_us | Philadelphia Eagles | 8.5 | 0.404 | 0.4989 |
| spread | open (ref) | Philadelphia Eagles | 1.5 | 0.208 | 0.5108 |
| total | fanduel | Over | 48.5 | 0.390 | 0.4854 |
| total | pinnacle (ref) | Over | 48.0 | 0.390 | 0.4978 |
| total | consensus (ref) | Over | 47.5 | 0.413 | 0.5183 |
| total | draftkings | Over | 47.5 | 0.413 | 0.5142 |
| total | bet365 | Over | 47.5 | 0.413 | 0.5195 |
| total | open (ref) | Over | 49.5 | 0.365 | 0.5108 |
| total | betrivers | Over | 48.0 | 0.390 | 0.4957 |
| total | betmgm | Over | 48.0 | 0.390 | 0.4978 |
| total | williamhill_us | Over | 48.0 | 0.390 | 0.4935 |
| moneyline | fanduel | Philadelphia Eagles |  | 0.189 | 0.2045 |
| moneyline | pinnacle (ref) | Philadelphia Eagles |  | 0.189 | 0.2177 |
| moneyline | consensus (ref) | Philadelphia Eagles |  | 0.189 | 0.2045 |
| moneyline | draftkings | Philadelphia Eagles |  | 0.189 | 0.2045 |
| moneyline | betrivers | Philadelphia Eagles |  | 0.189 | 0.219 |
| moneyline | betmgm | Philadelphia Eagles |  | 0.189 | 0.2031 |
| moneyline | bet365 | Philadelphia Eagles |  | 0.189 | 0.2063 |
| moneyline | williamhill_us | Philadelphia Eagles |  | 0.189 | 0.2167 |

Market divergence: {'max_abs_moneyline_gap': 0.03047969441093687, 'flag': 'WITHIN_0.15'}

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
