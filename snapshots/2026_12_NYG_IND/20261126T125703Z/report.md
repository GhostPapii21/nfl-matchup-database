# Locked snapshot NYG @ IND (2026_12_NYG_IND)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:57:03+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `nyg_ind_2026-11-29_data_only_nfl43`; code commit `c0b0c8c8841586459b0bb9444cc3cf9d78f87769`
- Trials: 100,000 in 3 chunks, seed 1447767749, runtime 650.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| IND points | 17.88 |
| NYG points | 22.33 |
| home margin | -4.45 (sd 13.53) |
| total | 40.21 (sd 11.61) |
| P(home win) / P(away win) / P(tie) | 0.368 / 0.622 / 0.0108 |
| P(OT) | 0.043 |
| penalties per game / yards home, away | 11.02 / 29.6, 51.1 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New York Giants | -6.5 | 0.454 | 0.4958 |
| spread | pinnacle (ref) | New York Giants | -6.0 | 0.454 | 0.5057 |
| spread | consensus (ref) | New York Giants | -6.5 | 0.454 | 0.4989 |
| spread | draftkings | New York Giants | -6.5 | 0.454 | 0.5087 |
| spread | betmgm | New York Giants | -6.5 | 0.454 | 0.4978 |
| spread | bet365 | New York Giants | -6.5 | 0.454 | 0.5 |
| spread | williamhill_us | New York Giants | -6.5 | 0.454 | 0.5065 |
| spread | open (ref) | New York Giants | 2.5 | 0.670 | 0.5 |
| total | fanduel | Over | 41.5 | 0.434 | 0.5 |
| total | pinnacle (ref) | Over | 42.0 | 0.419 | 0.4932 |
| total | betrivers | Over | 40.5 | 0.477 | 0.5085 |
| total | consensus (ref) | Over | 41.5 | 0.434 | 0.5 |
| total | draftkings | Over | 41.5 | 0.434 | 0.5033 |
| total | betmgm | Over | 41.5 | 0.434 | 0.4978 |
| total | bet365 | Over | 41.5 | 0.434 | 0.5 |
| total | williamhill_us | Over | 41.5 | 0.434 | 0.5032 |
| total | open (ref) | Over | 47.5 | 0.256 | 0.5 |
| moneyline | fanduel | New York Giants |  | 0.628 | 0.7175 |
| moneyline | pinnacle (ref) | New York Giants |  | 0.628 | 0.7149 |
| moneyline | consensus (ref) | New York Giants |  | 0.628 | 0.725 |
| moneyline | draftkings | New York Giants |  | 0.628 | 0.7337 |
| moneyline | betrivers | New York Giants |  | 0.628 | 0.7161 |
| moneyline | betmgm | New York Giants |  | 0.628 | 0.7241 |
| moneyline | bet365 | New York Giants |  | 0.628 | 0.7258 |
| moneyline | williamhill_us | New York Giants |  | 0.628 | 0.7273 |

Market divergence: {'max_abs_moneyline_gap': 0.10529204633907185, 'flag': 'WITHIN_0.15'}

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
