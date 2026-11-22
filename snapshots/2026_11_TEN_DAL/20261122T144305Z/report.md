# Locked snapshot TEN @ DAL (2026_11_TEN_DAL)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T14:43:05+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `ten_dal_2026-11-22_data_only_nfl43`; code commit `d8783fac9d9ebae6f7e87b4d8a3fdb0b81c5b163`
- Trials: 100,000 in 4 chunks, seed 2073881056, runtime 1302.9 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| DAL points | 26.35 |
| TEN points | 18.50 |
| home margin | 7.85 (sd 12.92) |
| total | 44.86 (sd 11.23) |
| P(home win) / P(away win) / P(tie) | 0.724 / 0.269 / 0.0065 |
| P(OT) | 0.034 |
| penalties per game / yards home, away | 11.62 / 51.5, 37.1 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | DAL | -7.5 | 0.502 | 0.4896 |
| spread | williamhill_us | DAL | -8.0 | 0.478 | 0.5011 |
| total | fanduel | Over | 54.5 | 0.190 | 0.5146 |
| total | pinnacle (ref) | Over | 55.0 | 0.174 | 0.4933 |
| total | williamhill_us | Over | 55.0 | 0.174 | 0.4968 |
| moneyline | fanduel | DAL |  | 0.729 | 0.7567 |
| moneyline | williamhill_us | DAL |  | 0.729 | 0.7723 |

Market divergence: {'max_abs_moneyline_gap': 0.043055324717155896, 'flag': 'WITHIN_0.15'}

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
