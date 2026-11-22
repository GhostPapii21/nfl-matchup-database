# Locked snapshot TB @ DET (2026_11_TB_DET)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T13:10:09+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `tb_det_2026-11-22_data_only_nfl43`; code commit `6051281f02cace71e36085bec74da69d47126d76`
- Trials: 100,000 in 7 chunks, seed 1819562, runtime 514.1 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| DET points | 30.56 |
| TB points | 15.26 |
| home margin | 15.31 (sd 13.60) |
| total | 45.82 (sd 11.96) |
| P(home win) / P(away win) / P(tie) | 0.869 / 0.126 / 0.0055 |
| P(OT) | 0.025 |
| penalties per game / yards home, away | 12.21 / 45.2, 42.3 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | draftkings | DET | -6.0 | 0.752 | 0.4989 |
| spread | williamhill_us | DET | -6.0 | 0.752 | 0.5087 |
| spread | betmgm | DET | -6.0 | 0.752 | 0.4978 |
| spread | fanduel | DET | -6.5 | 0.752 | 0.4783 |
| total | pinnacle (ref) | Over | 45.0 | 0.497 | 0.509 |
| total | draftkings | Over | 45.5 | 0.497 | 0.4945 |
| total | williamhill_us | Over | 45.5 | 0.497 | 0.5 |
| total | fanduel | Over | 45.5 | 0.497 | 0.5108 |
| total | betmgm | Over | 45.5 | 0.497 | 0.5022 |
| moneyline | draftkings | DET |  | 0.873 | 0.6928 |
| moneyline | williamhill_us | DET |  | 0.873 | 0.7012 |
| moneyline | fanduel | DET |  | 0.873 | 0.6947 |
| moneyline | betmgm | DET |  | 0.873 | 0.7012 |

Market divergence: {'max_abs_moneyline_gap': 0.1806501794925941, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
