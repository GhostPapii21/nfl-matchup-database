# Locked snapshot NYJ @ LAC (2026_11_NYJ_LAC)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T15:03:40+00:00  | kickoff (UTC): 2026-11-22T21:05:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `nyj_lac_2026-11-22_data_only_nfl43`; code commit `92e120bef37d42c5a334d639017e6979f30e47e7`
- Trials: 100,000 in 4 chunks, seed 1833934677, runtime 1231.7 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| LAC points | 16.56 |
| NYJ points | 24.46 |
| home margin | -7.91 (sd 13.37) |
| total | 41.02 (sd 11.91) |
| P(home win) / P(away win) / P(tie) | 0.272 / 0.721 / 0.0073 |
| P(OT) | 0.032 |
| penalties per game / yards home, away | 15.53 / 56.6, 57.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | LAC | -3.0 | 0.205 | 0.513 |
| spread | williamhill_us | LAC | -3.0 | 0.205 | 0.5043 |
| total | fanduel | Over | 42.5 | 0.445 | 0.5 |
| total | pinnacle (ref) | Over | 42.0 | 0.445 | 0.5022 |
| total | williamhill_us | Over | 42.0 | 0.445 | 0.4935 |
| moneyline | fanduel | LAC |  | 0.274 | 0.6183 |
| moneyline | williamhill_us | LAC |  | 0.274 | 0.6028 |

Market divergence: {'max_abs_moneyline_gap': 0.34409832779288807, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
