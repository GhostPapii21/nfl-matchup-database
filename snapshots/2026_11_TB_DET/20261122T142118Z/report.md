# Locked snapshot TB @ DET (2026_11_TB_DET)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T14:21:18+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `tb_det_2026-11-22_data_only_nfl43`; code commit `832c5693255e4b481bc1c4bfe12c175fb4173edd`
- Trials: 100,000 in 4 chunks, seed 1819562, runtime 1218.7 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| DET points | 30.53 |
| TB points | 15.25 |
| home margin | 15.28 (sd 13.61) |
| total | 45.79 (sd 12.01) |
| P(home win) / P(away win) / P(tie) | 0.868 / 0.126 / 0.0056 |
| P(OT) | 0.024 |
| penalties per game / yards home, away | 12.20 / 45.3, 42.2 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | DET | -3.5 | 0.813 | 0.5123 |
| spread | williamhill_us | DET | -6.0 | 0.753 | 0.5087 |
| total | fanduel | Over | 47.5 | 0.428 | 0.5 |
| total | pinnacle (ref) | Over | 47.5 | 0.428 | 0.4977 |
| total | williamhill_us | Over | 45.5 | 0.494 | 0.5 |
| moneyline | fanduel | DET |  | 0.873 | 0.6411 |
| moneyline | williamhill_us | DET |  | 0.873 | 0.7012 |

Market divergence: {'max_abs_moneyline_gap': 0.23181962067959894, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
