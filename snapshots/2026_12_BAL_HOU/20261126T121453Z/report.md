# Locked snapshot BAL @ HOU (2026_12_BAL_HOU)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:14:53+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `bal_hou_2026-11-29_data_only_nfl43`; code commit `668ef51c74534c968bfa11294d59c6ede707a80e`
- Trials: 100,000 in 4 chunks, seed 1293091237, runtime 853.4 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| HOU points | 25.86 |
| BAL points | 21.49 |
| home margin | 4.37 (sd 14.09) |
| total | 47.35 (sd 12.63) |
| P(home win) / P(away win) / P(tie) | 0.616 / 0.375 / 0.0089 |
| P(OT) | 0.042 |
| penalties per game / yards home, away | 15.31 / 51.4, 57.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Baltimore Ravens | 6.5 | 0.545 | 0.5 |
| spread | pinnacle (ref) | Baltimore Ravens | 6.5 | 0.545 | 0.4931 |
| spread | consensus (ref) | Baltimore Ravens | 6.5 | 0.545 | 0.4945 |
| spread | draftkings | Baltimore Ravens | 6.5 | 0.545 | 0.4945 |
| spread | betmgm | Baltimore Ravens | 6.5 | 0.545 | 0.4923 |
| spread | bet365 | Baltimore Ravens | 6.5 | 0.545 | 0.4957 |
| spread | williamhill_us | Baltimore Ravens | 6.5 | 0.545 | 0.4892 |
| spread | open (ref) | Baltimore Ravens | 1.5 | 0.405 | 0.5 |
| spread | betrivers | Baltimore Ravens | 7.0 | 0.545 | 0.5117 |
| total | fanduel | Over | 47.5 | 0.475 | 0.4958 |
| total | pinnacle (ref) | Over | 47.5 | 0.475 | 0.4977 |
| total | consensus (ref) | Over | 47.5 | 0.475 | 0.4912 |
| total | draftkings | Over | 47.5 | 0.475 | 0.4924 |
| total | bet365 | Over | 47.5 | 0.475 | 0.4913 |
| total | williamhill_us | Over | 47.5 | 0.475 | 0.4913 |
| total | open (ref) | Over | 45.5 | 0.541 | 0.5 |
| total | betrivers | Over | 46.5 | 0.524 | 0.5097 |
| total | betmgm | Over | 47.0 | 0.475 | 0.5077 |
| moneyline | fanduel | Baltimore Ravens |  | 0.378 | 0.2825 |
| moneyline | pinnacle (ref) | Baltimore Ravens |  | 0.378 | 0.2753 |
| moneyline | consensus (ref) | Baltimore Ravens |  | 0.378 | 0.2731 |
| moneyline | draftkings | Baltimore Ravens |  | 0.378 | 0.2617 |
| moneyline | betrivers | Baltimore Ravens |  | 0.378 | 0.2638 |
| moneyline | betmgm | Baltimore Ravens |  | 0.378 | 0.2759 |
| moneyline | bet365 | Baltimore Ravens |  | 0.378 | 0.2672 |
| moneyline | williamhill_us | Baltimore Ravens |  | 0.378 | 0.2742 |

Market divergence: {'max_abs_moneyline_gap': 0.11664729088891129, 'flag': 'WITHIN_0.15'}

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
