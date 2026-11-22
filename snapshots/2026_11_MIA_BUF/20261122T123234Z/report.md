# Locked snapshot MIA @ BUF (2026_11_MIA_BUF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T12:32:34+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `mia_buf_2026-11-22_data_only_nfl43`; code commit `6051281f02cace71e36085bec74da69d47126d76`
- Trials: 100,000 in 7 chunks, seed 964813532, runtime 576.1 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| BUF points | 31.33 |
| MIA points | 20.19 |
| home margin | 11.14 (sd 14.36) |
| total | 51.53 (sd 12.72) |
| P(home win) / P(away win) / P(tie) | 0.780 / 0.215 / 0.0043 |
| P(OT) | 0.026 |
| penalties per game / yards home, away | 14.14 / 62.1, 40.3 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | draftkings | BUF | -16.5 | 0.360 | 0.4945 |
| spread | williamhill_us | BUF | -16.5 | 0.360 | 0.5108 |
| spread | fanduel | BUF | -16.5 | 0.360 | 0.5 |
| spread | betmgm | BUF | -16.5 | 0.360 | 0.4978 |
| total | pinnacle (ref) | Over | 44.5 | 0.695 | 0.5045 |
| total | draftkings | Over | 44.5 | 0.695 | 0.5098 |
| total | williamhill_us | Over | 44.5 | 0.695 | 0.5108 |
| total | fanduel | Over | 44.5 | 0.695 | 0.5108 |
| total | betmgm | Over | 44.5 | 0.695 | 0.5022 |
| moneyline | draftkings | BUF |  | 0.784 | 0.9058 |
| moneyline | williamhill_us | BUF |  | 0.784 | 0.8997 |
| moneyline | fanduel | BUF |  | 0.784 | 0.904 |
| moneyline | betmgm | BUF |  | 0.784 | 0.9074 |

Market divergence: {'max_abs_moneyline_gap': 0.12365639016943364, 'flag': 'WITHIN_0.15'}

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
