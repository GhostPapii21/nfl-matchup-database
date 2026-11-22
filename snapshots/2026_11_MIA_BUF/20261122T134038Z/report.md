# Locked snapshot MIA @ BUF (2026_11_MIA_BUF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T13:40:38+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `mia_buf_2026-11-22_data_only_nfl43`; code commit `79ad60929eb624727f133b8fa035714efd53880a`
- Trials: 100,000 in 4 chunks, seed 964813532, runtime 1144.6 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| BUF points | 31.29 |
| MIA points | 20.22 |
| home margin | 11.08 (sd 14.38) |
| total | 51.51 (sd 12.76) |
| P(home win) / P(away win) / P(tie) | 0.779 / 0.217 / 0.0044 |
| P(OT) | 0.026 |
| penalties per game / yards home, away | 14.14 / 62.1, 40.4 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | BUF | -16.5 | 0.359 | 0.5 |
| spread | williamhill_us | BUF | -16.5 | 0.359 | 0.5108 |
| total | fanduel | Over | 44.5 | 0.694 | 0.5146 |
| total | pinnacle (ref) | Over | 44.5 | 0.694 | 0.5045 |
| total | williamhill_us | Over | 44.5 | 0.694 | 0.5108 |
| moneyline | fanduel | BUF |  | 0.782 | 0.904 |
| moneyline | williamhill_us | BUF |  | 0.782 | 0.8997 |

Market divergence: {'max_abs_moneyline_gap': 0.12150572542086868, 'flag': 'WITHIN_0.15'}

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
