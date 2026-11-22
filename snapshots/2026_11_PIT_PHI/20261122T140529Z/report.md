# Locked snapshot PIT @ PHI (2026_11_PIT_PHI)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T14:05:29+00:00  | kickoff (UTC): 2026-11-22T21:25:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `pit_phi_2026-11-22_data_only_nfl43`; code commit `0b5052dee2b624b9a1b679f90e815e6073180518`
- Trials: 100,000 in 7 chunks, seed 2040983328, runtime 970.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| PHI points | 17.08 |
| PIT points | 22.67 |
| home margin | -5.60 (sd 13.29) |
| total | 39.75 (sd 11.50) |
| P(home win) / P(away win) / P(tie) | 0.330 / 0.660 / 0.0090 |
| P(OT) | 0.040 |
| penalties per game / yards home, away | 12.53 / 45.6, 47.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | PHI | 3.5 | 0.433 | 0.5 |
| spread | williamhill_us | PHI | 4.5 | 0.464 | 0.5076 |
| total | fanduel | Over | 37.5 | 0.549 | 0.5 |
| total | pinnacle (ref) | Over | 37.5 | 0.549 | 0.4955 |
| total | williamhill_us | Over | 38.0 | 0.532 | 0.5011 |
| moneyline | fanduel | PHI |  | 0.333 | 0.3614 |
| moneyline | williamhill_us | PHI |  | 0.333 | 0.3433 |

Market divergence: {'max_abs_moneyline_gap': 0.027905207071930227, 'flag': 'WITHIN_0.15'}

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
