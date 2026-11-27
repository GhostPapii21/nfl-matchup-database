# Locked snapshot NYJ @ MIA (2026_12_NYJ_MIA)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:07:17+00:00  | kickoff (UTC): 2026-11-29T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `nyj_mia_2026-11-29_data_only_nfl43`; code commit `e47f8d76ea3f90a1740ee881ebdb2770a8f202d7`
- Trials: 100,000 in 3 chunks, seed 2122944308, runtime 613.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| MIA points | 16.80 |
| NYJ points | 22.96 |
| home margin | -6.16 (sd 12.97) |
| total | 39.77 (sd 11.68) |
| P(home win) / P(away win) / P(tie) | 0.314 / 0.676 / 0.0096 |
| P(OT) | 0.038 |
| penalties per game / yards home, away | 13.78 / 40.3, 55.4 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | New York Jets | -4.5 | 0.552 | 0.4896 |
| spread | pinnacle (ref) | New York Jets | -5.0 | 0.533 | 0.5045 |
| spread | consensus (ref) | New York Jets | -4.5 | 0.552 | 0.4967 |
| spread | betmgm | New York Jets | -4.5 | 0.552 | 0.4978 |
| spread | bet365 | New York Jets | -4.5 | 0.552 | 0.4957 |
| spread | williamhill_us | New York Jets | -4.5 | 0.552 | 0.4838 |
| spread | open (ref) | New York Jets | 1.5 | 0.713 | 0.5 |
| spread | draftkings | New York Jets | -3.5 | 0.586 | 0.512 |
| total | fanduel | Over | 40.5 | 0.455 | 0.5 |
| total | pinnacle (ref) | Over | 40.5 | 0.455 | 0.4978 |
| total | consensus (ref) | Over | 40.5 | 0.455 | 0.4922 |
| total | open (ref) | Over | 40.5 | 0.455 | 0.5 |
| total | draftkings | Over | 40.5 | 0.455 | 0.488 |
| total | betrivers | Over | 40.5 | 0.455 | 0.5043 |
| total | bet365 | Over | 40.5 | 0.455 | 0.4935 |
| total | williamhill_us | Over | 40.5 | 0.455 | 0.5 |
| total | betmgm | Over | 40.0 | 0.455 | 0.5022 |
| moneyline | fanduel | New York Jets |  | 0.683 | 0.6565 |
| moneyline | pinnacle (ref) | New York Jets |  | 0.683 | 0.674 |
| moneyline | consensus (ref) | New York Jets |  | 0.683 | 0.6571 |
| moneyline | draftkings | New York Jets |  | 0.683 | 0.6464 |
| moneyline | betrivers | New York Jets |  | 0.683 | 0.6612 |
| moneyline | betmgm | New York Jets |  | 0.683 | 0.6704 |
| moneyline | bet365 | New York Jets |  | 0.683 | 0.6581 |
| moneyline | williamhill_us | New York Jets |  | 0.683 | 0.6629 |

Market divergence: {'max_abs_moneyline_gap': 0.03661056160261722, 'flag': 'WITHIN_0.15'}

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
