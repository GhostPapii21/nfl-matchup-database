# Locked snapshot NE @ LAC (2026_12_NE_LAC)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:39:21+00:00  | kickoff (UTC): 2026-11-29T21:05:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `ne_lac_2026-11-29_data_only_nfl43`; code commit `fd257857069057a3bc5963766f0cd3198d0a174f`
- Trials: 100,000 in 3 chunks, seed 1372166181, runtime 631.2 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| LAC points | 18.86 |
| NE points | 25.52 |
| home margin | -6.66 (sd 14.55) |
| total | 44.38 (sd 12.76) |
| P(home win) / P(away win) / P(tie) | 0.318 / 0.674 / 0.0079 |
| P(OT) | 0.035 |
| penalties per game / yards home, away | 14.92 / 56.3, 50.2 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New England Patriots | -1.5 | 0.647 | 0.4896 |
| spread | pinnacle (ref) | New England Patriots | -1.0 | 0.647 | 0.4966 |
| spread | consensus (ref) | New England Patriots | -1.5 | 0.647 | 0.4892 |
| spread | draftkings | New England Patriots | -1.5 | 0.647 | 0.473 |
| spread | bet365 | New England Patriots | -1.5 | 0.647 | 0.4826 |
| spread | open (ref) | New England Patriots | 1.5 | 0.699 | 0.5 |
| spread | betmgm | New England Patriots | -1.0 | 0.647 | 0.4892 |
| spread | williamhill_us | New England Patriots | -1.0 | 0.647 | 0.4892 |
| spread | betrivers | New England Patriots | 0.5 | 0.682 | 0.5043 |
| total | fanduel | Over | 35.5 | 0.756 | 0.5 |
| total | pinnacle (ref) | Over | 35.0 | 0.756 | 0.5077 |
| total | consensus (ref) | Over | 35.5 | 0.756 | 0.4989 |
| total | draftkings | Over | 35.5 | 0.756 | 0.4989 |
| total | betmgm | Over | 35.5 | 0.756 | 0.4978 |
| total | bet365 | Over | 35.5 | 0.756 | 0.5 |
| total | williamhill_us | Over | 35.5 | 0.756 | 0.5032 |
| total | betrivers | Over | 36.5 | 0.730 | 0.4915 |
| total | open (ref) | Over | 45.5 | 0.448 | 0.5 |
| moneyline | fanduel | New England Patriots |  | 0.680 | 0.5154 |
| moneyline | pinnacle (ref) | New England Patriots |  | 0.680 | 0.5148 |
| moneyline | consensus (ref) | New England Patriots |  | 0.680 | 0.5044 |
| moneyline | open (ref) | New England Patriots |  | 0.680 | 0.4675 |
| moneyline | draftkings | New England Patriots |  | 0.680 | 0.5066 |
| moneyline | betrivers | New England Patriots |  | 0.680 | 0.4946 |
| moneyline | betmgm | New England Patriots |  | 0.680 | 0.5022 |
| moneyline | bet365 | New England Patriots |  | 0.680 | 0.5152 |
| moneyline | williamhill_us | New England Patriots |  | 0.680 | 0.5088 |

Market divergence: {'max_abs_moneyline_gap': 0.21216655242626448, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
