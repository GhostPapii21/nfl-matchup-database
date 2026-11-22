# Locked snapshot LV @ DEN (2026_11_LV_DEN)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T20:28:26+00:00  | kickoff (UTC): 2026-11-22T21:25:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `lv_den_2026-11-22_data_only_nfl43`; code commit `aadce43b1b33168b1285fbe990490966c59cb729`
- Trials: 100,000 in 4 chunks, seed 1476728154, runtime 1096.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| DEN points | 19.85 |
| LV points | 22.06 |
| home margin | -2.21 (sd 13.26) |
| total | 41.91 (sd 12.10) |
| P(home win) / P(away win) / P(tie) | 0.424 / 0.564 / 0.0121 |
| P(OT) | 0.048 |
| penalties per game / yards home, away | 13.50 / 48.5, 43.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Las Vegas Raiders | 10.5 | 0.832 | 0.4958 |
| spread | pinnacle (ref) | Las Vegas Raiders | 11.5 | 0.856 | 0.5 |
| spread | consensus (ref) | Las Vegas Raiders | 10.5 | 0.832 | 0.4978 |
| spread | draftkings | Las Vegas Raiders | 10.5 | 0.832 | 0.4967 |
| spread | betrivers | Las Vegas Raiders | 10.5 | 0.832 | 0.4957 |
| spread | bet365 | Las Vegas Raiders | 10.5 | 0.832 | 0.4957 |
| spread | williamhill_us | Las Vegas Raiders | 11.5 | 0.856 | 0.5087 |
| spread | open (ref) | Las Vegas Raiders | 7.5 | 0.777 | 0.5 |
| spread | betmgm | Las Vegas Raiders | 11.0 | 0.832 | 0.507 |
| total | fanduel | Over | 41.5 | 0.488 | 0.4958 |
| total | pinnacle (ref) | Over | 41.5 | 0.488 | 0.4977 |
| total | consensus (ref) | Over | 41.5 | 0.488 | 0.4923 |
| total | open (ref) | Over | 41.5 | 0.488 | 0.5 |
| total | betrivers | Over | 41.5 | 0.488 | 0.486 |
| total | betmgm | Over | 41.5 | 0.488 | 0.4923 |
| total | bet365 | Over | 41.5 | 0.488 | 0.4935 |
| total | williamhill_us | Over | 41.5 | 0.488 | 0.4892 |
| total | draftkings | Over | 40.5 | 0.535 | 0.5152 |
| moneyline | fanduel | Las Vegas Raiders |  | 0.571 | 0.1659 |
| moneyline | pinnacle (ref) | Las Vegas Raiders |  | 0.571 | 0.1604 |
| moneyline | consensus (ref) | Las Vegas Raiders |  | 0.571 | 0.1613 |
| moneyline | open (ref) | Las Vegas Raiders |  | 0.571 | 0.2591 |
| moneyline | draftkings | Las Vegas Raiders |  | 0.571 | 0.1767 |
| moneyline | betrivers | Las Vegas Raiders |  | 0.571 | 0.1824 |
| moneyline | betmgm | Las Vegas Raiders |  | 0.571 | 0.1613 |
| moneyline | bet365 | Las Vegas Raiders |  | 0.571 | 0.16 |
| moneyline | williamhill_us | Las Vegas Raiders |  | 0.571 | 0.1742 |

Market divergence: {'max_abs_moneyline_gap': 0.41112199862331456, 'flag': 'QUARANTINE_LIKELY_MODEL_ERROR'}

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
