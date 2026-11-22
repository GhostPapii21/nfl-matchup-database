# Locked snapshot NO @ CHI (2026_11_NO_CHI)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T14:00:56+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `no_chi_2026-11-22_data_only_nfl43`; code commit `bd6c9de6f9a19c9eeb49eb124ee28bc6fc8e09e5`
- Trials: 100,000 in 4 chunks, seed 948196875, runtime 1213.7 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| CHI points | 25.78 |
| NO points | 19.81 |
| home margin | 5.97 (sd 14.29) |
| total | 45.59 (sd 12.04) |
| P(home win) / P(away win) / P(tie) | 0.662 / 0.330 / 0.0083 |
| P(OT) | 0.036 |
| penalties per game / yards home, away | 12.35 / 49.3, 37.4 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | CHI | -11.5 | 0.341 | 0.5 |
| spread | williamhill_us | CHI | -11.5 | 0.341 | 0.4892 |
| total | fanduel | Over | 48.5 | 0.386 | 0.502 |
| total | pinnacle (ref) | Over | 48.0 | 0.386 | 0.5022 |
| total | williamhill_us | Over | 48.5 | 0.386 | 0.5087 |
| moneyline | fanduel | CHI |  | 0.667 | 0.8448 |
| moneyline | williamhill_us | CHI |  | 0.667 | 0.8258 |

Market divergence: {'max_abs_moneyline_gap': 0.17730642867947366, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
