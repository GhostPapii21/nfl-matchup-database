# Locked snapshot BAL @ HOU (2026_12_BAL_HOU)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:34:48+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `bal_hou_2026-11-29_data_only_nfl43`; code commit `c02809c6ddc0be63ecbde266d60f96171df07145`
- Trials: 100,000 in 3 chunks, seed 1293091237, runtime 663.4 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| HOU points | 25.83 |
| BAL points | 21.49 |
| home margin | 4.34 (sd 14.11) |
| total | 47.33 (sd 12.62) |
| P(home win) / P(away win) / P(tie) | 0.614 / 0.377 / 0.0089 |
| P(OT) | 0.042 |
| penalties per game / yards home, away | 15.31 / 51.4, 57.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Baltimore Ravens | 6.5 | 0.546 | 0.5 |
| spread | pinnacle (ref) | Baltimore Ravens | 6.5 | 0.546 | 0.4977 |
| spread | consensus (ref) | Baltimore Ravens | 6.5 | 0.546 | 0.4934 |
| spread | draftkings | Baltimore Ravens | 6.5 | 0.546 | 0.4945 |
| spread | betrivers | Baltimore Ravens | 6.5 | 0.546 | 0.4872 |
| spread | betmgm | Baltimore Ravens | 6.5 | 0.546 | 0.4923 |
| spread | bet365 | Baltimore Ravens | 6.5 | 0.546 | 0.4957 |
| spread | williamhill_us | Baltimore Ravens | 6.5 | 0.546 | 0.4892 |
| spread | open (ref) | Baltimore Ravens | 1.5 | 0.406 | 0.5 |
| total | fanduel | Over | 47.5 | 0.475 | 0.4958 |
| total | pinnacle (ref) | Over | 47.5 | 0.475 | 0.4977 |
| total | consensus (ref) | Over | 47.5 | 0.475 | 0.4912 |
| total | draftkings | Over | 47.5 | 0.475 | 0.4924 |
| total | bet365 | Over | 47.5 | 0.475 | 0.4913 |
| total | williamhill_us | Over | 47.5 | 0.475 | 0.4913 |
| total | open (ref) | Over | 45.5 | 0.541 | 0.5 |
| total | betrivers | Over | 46.5 | 0.525 | 0.4979 |
| total | betmgm | Over | 47.0 | 0.475 | 0.5077 |
| moneyline | fanduel | Baltimore Ravens |  | 0.380 | 0.2825 |
| moneyline | pinnacle (ref) | Baltimore Ravens |  | 0.380 | 0.2769 |
| moneyline | consensus (ref) | Baltimore Ravens |  | 0.380 | 0.2731 |
| moneyline | draftkings | Baltimore Ravens |  | 0.380 | 0.2631 |
| moneyline | betrivers | Baltimore Ravens |  | 0.380 | 0.2678 |
| moneyline | betmgm | Baltimore Ravens |  | 0.380 | 0.2759 |
| moneyline | bet365 | Baltimore Ravens |  | 0.380 | 0.2672 |
| moneyline | williamhill_us | Baltimore Ravens |  | 0.380 | 0.2742 |

Market divergence: {'max_abs_moneyline_gap': 0.11694621174666275, 'flag': 'WITHIN_0.15'}

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
