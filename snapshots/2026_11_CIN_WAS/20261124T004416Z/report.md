# Locked snapshot CIN @ WAS (2026_11_CIN_WAS)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-24T00:44:16+00:00  | kickoff (UTC): 2026-11-24T01:15:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `cin_was_2026-11-23_data_only_nfl43`; code commit `82846d0ed0d16d2026fdecded036a5bc05512fd3`
- Trials: 100,000 in 4 chunks, seed 1482608122, runtime 2291.4 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| WAS points | 22.05 |
| CIN points | 30.75 |
| home margin | -8.70 (sd 14.23) |
| total | 52.79 (sd 12.70) |
| P(home win) / P(away win) / P(tie) | 0.263 / 0.731 / 0.0052 |
| P(OT) | 0.028 |
| penalties per game / yards home, away | 13.30 / 50.3, 45.6 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Cincinnati Bengals | -6.5 | 0.579 | 0.4958 |
| spread | pinnacle (ref) | Cincinnati Bengals | -6.5 | 0.579 | 0.493 |
| spread | consensus (ref) | Cincinnati Bengals | -6.5 | 0.579 | 0.5022 |
| spread | betrivers | Cincinnati Bengals | -6.5 | 0.579 | 0.5 |
| spread | betmgm | Cincinnati Bengals | -6.5 | 0.579 | 0.5077 |
| spread | bet365 | Cincinnati Bengals | -6.5 | 0.579 | 0.4978 |
| spread | williamhill_us | Cincinnati Bengals | -6.5 | 0.579 | 0.4989 |
| spread | open (ref) | Cincinnati Bengals | -1.5 | 0.700 | 0.5 |
| spread | draftkings | Cincinnati Bengals | -6.0 | 0.579 | 0.5217 |
| total | fanduel | Over | 54.5 | 0.435 | 0.4854 |
| total | pinnacle (ref) | Over | 54.0 | 0.435 | 0.4966 |
| total | open (ref) | Over | 52.5 | 0.500 | 0.5 |
| total | consensus (ref) | Over | 54.5 | 0.435 | 0.5044 |
| total | draftkings | Over | 54.5 | 0.435 | 0.5076 |
| total | bet365 | Over | 54.5 | 0.435 | 0.5 |
| total | williamhill_us | Over | 54.5 | 0.435 | 0.5011 |
| total | betrivers | Over | 54.0 | 0.435 | 0.5032 |
| total | betmgm | Over | 54.0 | 0.435 | 0.5077 |
| moneyline | fanduel | Cincinnati Bengals |  | 0.735 | 0.7213 |
| moneyline | pinnacle (ref) | Cincinnati Bengals |  | 0.735 | 0.72 |
| moneyline | consensus (ref) | Cincinnati Bengals |  | 0.735 | 0.7242 |
| moneyline | draftkings | Cincinnati Bengals |  | 0.735 | 0.722 |
| moneyline | betrivers | Cincinnati Bengals |  | 0.735 | 0.7237 |
| moneyline | betmgm | Cincinnati Bengals |  | 0.735 | 0.7335 |
| moneyline | bet365 | Cincinnati Bengals |  | 0.735 | 0.7258 |
| moneyline | williamhill_us | Cincinnati Bengals |  | 0.735 | 0.7175 |

Market divergence: {'max_abs_moneyline_gap': 0.017748587684204065, 'flag': 'WITHIN_0.15'}

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
