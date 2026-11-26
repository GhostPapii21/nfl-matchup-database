# Locked snapshot NE @ LAC (2026_12_NE_LAC)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:20:14+00:00  | kickoff (UTC): 2026-11-29T21:05:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `ne_lac_2026-11-29_data_only_nfl43`; code commit `46b799460a56ad1d76a8e794fce8d25dd1d28530`
- Trials: 100,000 in 4 chunks, seed 1372166181, runtime 780.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| LAC points | 18.82 |
| NE points | 25.51 |
| home margin | -6.69 (sd 14.52) |
| total | 44.33 (sd 12.76) |
| P(home win) / P(away win) / P(tie) | 0.317 / 0.676 / 0.0078 |
| P(OT) | 0.035 |
| penalties per game / yards home, away | 14.92 / 56.3, 50.2 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New England Patriots | -1.5 | 0.649 | 0.4812 |
| spread | pinnacle (ref) | New England Patriots | -1.0 | 0.649 | 0.4989 |
| spread | consensus (ref) | New England Patriots | -1.5 | 0.649 | 0.4934 |
| spread | draftkings | New England Patriots | -1.5 | 0.649 | 0.4814 |
| spread | bet365 | New England Patriots | -1.5 | 0.649 | 0.4826 |
| spread | open (ref) | New England Patriots | 1.5 | 0.700 | 0.5 |
| spread | betrivers | New England Patriots | -1.0 | 0.649 | 0.4968 |
| spread | betmgm | New England Patriots | -1.0 | 0.649 | 0.4978 |
| spread | williamhill_us | New England Patriots | -1.0 | 0.649 | 0.4989 |
| total | fanduel | Over | 35.5 | 0.754 | 0.5 |
| total | pinnacle (ref) | Over | 35.5 | 0.754 | 0.4977 |
| total | consensus (ref) | Over | 35.5 | 0.754 | 0.5 |
| total | draftkings | Over | 35.5 | 0.754 | 0.4989 |
| total | betmgm | Over | 35.5 | 0.754 | 0.5 |
| total | bet365 | Over | 35.5 | 0.754 | 0.5 |
| total | williamhill_us | Over | 35.5 | 0.754 | 0.5032 |
| total | betrivers | Over | 36.5 | 0.728 | 0.4903 |
| total | open (ref) | Over | 45.5 | 0.446 | 0.5 |
| moneyline | fanduel | New England Patriots |  | 0.681 | 0.5154 |
| moneyline | pinnacle (ref) | New England Patriots |  | 0.681 | 0.5183 |
| moneyline | consensus (ref) | New England Patriots |  | 0.681 | 0.5174 |
| moneyline | open (ref) | New England Patriots |  | 0.681 | 0.4675 |
| moneyline | draftkings | New England Patriots |  | 0.681 | 0.5208 |
| moneyline | betrivers | New England Patriots |  | 0.681 | 0.5138 |
| moneyline | betmgm | New England Patriots |  | 0.681 | 0.5174 |
| moneyline | bet365 | New England Patriots |  | 0.681 | 0.5152 |
| moneyline | williamhill_us | New England Patriots |  | 0.681 | 0.5088 |

Market divergence: {'max_abs_moneyline_gap': 0.2135045956623397, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
