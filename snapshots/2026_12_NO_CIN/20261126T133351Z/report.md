# Locked snapshot NO @ CIN (2026_12_NO_CIN)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:33:51+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `no_cin_2026-11-29_data_only_nfl43`; code commit `46b799460a56ad1d76a8e794fce8d25dd1d28530`
- Trials: 100,000 in 4 chunks, seed 156793436, runtime 816.8 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| CIN points | 32.74 |
| NO points | 18.61 |
| home margin | 14.13 (sd 14.63) |
| total | 51.36 (sd 12.47) |
| P(home win) / P(away win) / P(tie) | 0.833 / 0.162 / 0.0047 |
| P(OT) | 0.025 |
| penalties per game / yards home, away | 12.59 / 46.7, 38.6 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New Orleans Saints | 10.5 | 0.403 | 0.5188 |
| spread | pinnacle (ref) | New Orleans Saints | 10.0 | 0.371 | 0.4966 |
| spread | bet365 | New Orleans Saints | 9.5 | 0.371 | 0.4783 |
| spread | open (ref) | New Orleans Saints | 6.5 | 0.288 | 0.5 |
| spread | consensus (ref) | New Orleans Saints | 10.0 | 0.371 | 0.4912 |
| spread | draftkings | New Orleans Saints | 10.0 | 0.371 | 0.5076 |
| spread | betrivers | New Orleans Saints | 10.0 | 0.371 | 0.5054 |
| spread | betmgm | New Orleans Saints | 10.0 | 0.371 | 0.5077 |
| spread | williamhill_us | New Orleans Saints | 10.0 | 0.371 | 0.4989 |
| total | fanduel | Over | 49.5 | 0.560 | 0.5042 |
| total | pinnacle (ref) | Over | 49.5 | 0.560 | 0.4978 |
| total | consensus (ref) | Over | 49.5 | 0.560 | 0.5 |
| total | draftkings | Over | 49.5 | 0.560 | 0.5033 |
| total | betmgm | Over | 49.5 | 0.560 | 0.4978 |
| total | bet365 | Over | 49.5 | 0.560 | 0.5 |
| total | williamhill_us | Over | 49.5 | 0.560 | 0.5085 |
| total | open (ref) | Over | 48.5 | 0.574 | 0.5 |
| total | betrivers | Over | 50.0 | 0.526 | 0.4935 |
| moneyline | fanduel | New Orleans Saints |  | 0.163 | 0.1848 |
| moneyline | pinnacle (ref) | New Orleans Saints |  | 0.163 | 0.1804 |
| moneyline | consensus (ref) | New Orleans Saints |  | 0.163 | 0.1835 |
| moneyline | open (ref) | New Orleans Saints |  | 0.163 | 0.2905 |
| moneyline | draftkings | New Orleans Saints |  | 0.163 | 0.1835 |
| moneyline | betrivers | New Orleans Saints |  | 0.163 | 0.1819 |
| moneyline | betmgm | New Orleans Saints |  | 0.163 | 0.1837 |
| moneyline | bet365 | New Orleans Saints |  | 0.163 | 0.1827 |
| moneyline | williamhill_us | New Orleans Saints |  | 0.163 | 0.1822 |

Market divergence: {'max_abs_moneyline_gap': 0.12761934735213448, 'flag': 'WITHIN_0.15'}

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
