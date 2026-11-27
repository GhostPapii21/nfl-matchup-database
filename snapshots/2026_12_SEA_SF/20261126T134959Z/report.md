# Locked snapshot SEA @ SF (2026_12_SEA_SF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:49:59+00:00  | kickoff (UTC): 2026-11-29T21:25:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `sea_sf_2026-11-29_data_only_nfl43`; code commit `b68cdbf1bc673c358fef26671d2b063e3bcf2512`
- Trials: 100,000 in 3 chunks, seed 761353172, runtime 637.3 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| SF points | 31.67 |
| SEA points | 20.08 |
| home margin | 11.59 (sd 14.28) |
| total | 51.75 (sd 13.35) |
| P(home win) / P(away win) / P(tie) | 0.793 / 0.201 / 0.0061 |
| P(OT) | 0.028 |
| penalties per game / yards home, away | 12.42 / 48.8, 55.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Seattle Seahawks | 2.5 | 0.245 | 0.4854 |
| spread | pinnacle (ref) | Seattle Seahawks | 2.5 | 0.245 | 0.4885 |
| spread | consensus (ref) | Seattle Seahawks | 2.5 | 0.245 | 0.4892 |
| spread | draftkings | Seattle Seahawks | 2.5 | 0.245 | 0.4773 |
| spread | betrivers | Seattle Seahawks | 2.5 | 0.245 | 0.481 |
| spread | betmgm | Seattle Seahawks | 2.5 | 0.245 | 0.4892 |
| spread | bet365 | Seattle Seahawks | 2.5 | 0.245 | 0.4892 |
| spread | williamhill_us | Seattle Seahawks | 2.5 | 0.245 | 0.4783 |
| spread | open (ref) | Seattle Seahawks | 1.5 | 0.232 | 0.5325 |
| total | fanduel | Over | 44.5 | 0.696 | 0.5 |
| total | pinnacle (ref) | Over | 44.5 | 0.696 | 0.4911 |
| total | consensus (ref) | Over | 44.5 | 0.696 | 0.4989 |
| total | draftkings | Over | 44.5 | 0.696 | 0.4989 |
| total | betrivers | Over | 44.5 | 0.696 | 0.5022 |
| total | betmgm | Over | 44.5 | 0.696 | 0.4978 |
| total | bet365 | Over | 44.5 | 0.696 | 0.5022 |
| total | williamhill_us | Over | 44.5 | 0.696 | 0.4957 |
| total | open (ref) | Over | 46.5 | 0.653 | 0.5 |
| moneyline | fanduel | Seattle Seahawks |  | 0.202 | 0.4329 |
| moneyline | pinnacle (ref) | Seattle Seahawks |  | 0.202 | 0.4335 |
| moneyline | consensus (ref) | Seattle Seahawks |  | 0.202 | 0.4322 |
| moneyline | open (ref) | Seattle Seahawks |  | 0.202 | 0.5 |
| moneyline | draftkings | Seattle Seahawks |  | 0.202 | 0.4286 |
| moneyline | betrivers | Seattle Seahawks |  | 0.202 | 0.4277 |
| moneyline | betmgm | Seattle Seahawks |  | 0.202 | 0.4344 |
| moneyline | bet365 | Seattle Seahawks |  | 0.202 | 0.4304 |
| moneyline | williamhill_us | Seattle Seahawks |  | 0.202 | 0.4347 |

Market divergence: {'max_abs_moneyline_gap': 0.2975189150032196, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
