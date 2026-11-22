# Locked snapshot JAX @ NYG (2026_11_JAX_NYG)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T13:21:12+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `jax_nyg_2026-11-22_data_only_nfl43`; code commit `463c78f891c9ea8203102d19074e3cc9dbeb1719`
- Trials: 100,000 in 4 chunks, seed 873228321, runtime 1173.4 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| NYG points | 21.04 |
| JAX points | 26.25 |
| home margin | -5.21 (sd 13.84) |
| total | 47.28 (sd 12.61) |
| P(home win) / P(away win) / P(tie) | 0.348 / 0.643 / 0.0089 |
| P(OT) | 0.039 |
| penalties per game / yards home, away | 14.41 / 49.8, 63.8 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | NYG | 5.5 | 0.492 | 0.4783 |
| spread | williamhill_us | NYG | 6.0 | 0.492 | 0.4957 |
| total | fanduel | Over | 46.5 | 0.521 | 0.4783 |
| total | pinnacle (ref) | Over | 45.0 | 0.540 | 0.4977 |
| total | williamhill_us | Over | 46.5 | 0.521 | 0.5 |
| moneyline | fanduel | NYG |  | 0.351 | 0.3053 |
| moneyline | williamhill_us | NYG |  | 0.351 | 0.3042 |

Market divergence: {'max_abs_moneyline_gap': 0.046907837597869095, 'flag': 'WITHIN_0.15'}

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
