# Locked snapshot ARI @ KC (2026_11_ARI_KC)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-22T12:40:43+00:00  | kickoff (UTC): 2026-11-22T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `ari_kc_2026-11-22_data_only_nfl43`; code commit `6051281f02cace71e36085bec74da69d47126d76`
- Trials: 100,000 in 4 chunks, seed 1007185783, runtime 1226.8 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (strictly before week 11); PBP sha256 `24ea364cccf8d9d0...`

| | mean |
|---|---|
| KC points | 30.08 |
| ARI points | 19.67 |
| home margin | 10.41 (sd 13.86) |
| total | 49.74 (sd 12.57) |
| P(home win) / P(away win) / P(tie) | 0.775 / 0.219 / 0.0064 |
| P(OT) | 0.030 |
| penalties per game / yards home, away | 13.22 / 58.3, 51.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | draftkings | KC | -16.5 | 0.335 | 0.4924 |
| spread | williamhill_us | KC | -16.5 | 0.335 | 0.4989 |
| spread | fanduel | KC | -15.5 | 0.348 | 0.5108 |
| spread | betmgm | KC | -16.0 | 0.335 | 0.5022 |
| total | pinnacle (ref) | Over | 41.0 | 0.731 | 0.491 |
| total | betmgm | Over | 41.0 | 0.731 | 0.4923 |
| total | draftkings | Over | 40.5 | 0.763 | 0.5098 |
| total | williamhill_us | Over | 40.5 | 0.763 | 0.5108 |
| total | fanduel | Over | 41.5 | 0.731 | 0.4783 |
| moneyline | draftkings | KC |  | 0.780 | 0.8978 |
| moneyline | williamhill_us | KC |  | 0.780 | 0.8989 |
| moneyline | fanduel | KC |  | 0.780 | 0.9009 |
| moneyline | betmgm | KC |  | 0.780 | 0.9074 |

Market divergence: {'max_abs_moneyline_gap': 0.12784422974346588, 'flag': 'WITHIN_0.15'}

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
