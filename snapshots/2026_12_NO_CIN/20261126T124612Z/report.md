# Locked snapshot NO @ CIN (2026_12_NO_CIN)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T12:46:12+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `no_cin_2026-11-29_data_only_nfl43`; code commit `9e3bcea051c569adc647cc2dbea8b5b4b43be6f7`
- Trials: 100,000 in 3 chunks, seed 156793436, runtime 683.4 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| CIN points | 32.79 |
| NO points | 18.58 |
| home margin | 14.22 (sd 14.61) |
| total | 51.37 (sd 12.48) |
| P(home win) / P(away win) / P(tie) | 0.834 / 0.161 / 0.0047 |
| P(OT) | 0.025 |
| penalties per game / yards home, away | 12.60 / 46.8, 38.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New Orleans Saints | 10.5 | 0.399 | 0.5146 |
| spread | pinnacle (ref) | New Orleans Saints | 9.5 | 0.368 | 0.492 |
| spread | bet365 | New Orleans Saints | 9.5 | 0.368 | 0.4848 |
| spread | open (ref) | New Orleans Saints | 6.5 | 0.286 | 0.5 |
| spread | consensus (ref) | New Orleans Saints | 10.0 | 0.368 | 0.4945 |
| spread | draftkings | New Orleans Saints | 10.0 | 0.368 | 0.5055 |
| spread | betrivers | New Orleans Saints | 10.0 | 0.368 | 0.5054 |
| spread | betmgm | New Orleans Saints | 10.0 | 0.368 | 0.5022 |
| spread | williamhill_us | New Orleans Saints | 10.0 | 0.368 | 0.4989 |
| total | fanduel | Over | 49.5 | 0.559 | 0.5042 |
| total | pinnacle (ref) | Over | 49.5 | 0.559 | 0.5 |
| total | consensus (ref) | Over | 49.5 | 0.559 | 0.5011 |
| total | draftkings | Over | 49.5 | 0.559 | 0.5033 |
| total | betmgm | Over | 49.5 | 0.559 | 0.5022 |
| total | bet365 | Over | 49.5 | 0.559 | 0.5 |
| total | williamhill_us | Over | 49.5 | 0.559 | 0.5085 |
| total | open (ref) | Over | 48.5 | 0.574 | 0.5 |
| total | betrivers | Over | 50.0 | 0.526 | 0.4935 |
| moneyline | fanduel | New Orleans Saints |  | 0.162 | 0.1848 |
| moneyline | pinnacle (ref) | New Orleans Saints |  | 0.162 | 0.1863 |
| moneyline | consensus (ref) | New Orleans Saints |  | 0.162 | 0.1845 |
| moneyline | open (ref) | New Orleans Saints |  | 0.162 | 0.2905 |
| moneyline | draftkings | New Orleans Saints |  | 0.162 | 0.1889 |
| moneyline | betrivers | New Orleans Saints |  | 0.162 | 0.1819 |
| moneyline | betmgm | New Orleans Saints |  | 0.162 | 0.1837 |
| moneyline | bet365 | New Orleans Saints |  | 0.162 | 0.1827 |
| moneyline | williamhill_us | New Orleans Saints |  | 0.162 | 0.1822 |

Market divergence: {'max_abs_moneyline_gap': 0.12866097497262158, 'flag': 'WITHIN_0.15'}

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
