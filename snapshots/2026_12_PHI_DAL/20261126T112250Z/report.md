# Locked snapshot PHI @ DAL (2026_12_PHI_DAL)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T11:22:50+00:00  | kickoff (UTC): 2026-11-26T21:30:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `phi_dal_2026-11-26_data_only_nfl43`; code commit `2b33647ccd84ef8515e122c291705fdfe7b1d2cd`
- Trials: 100,000 in 7 chunks, seed 258085159, runtime 569.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| DAL points | 28.56 |
| PHI points | 17.01 |
| home margin | 11.55 (sd 13.26) |
| total | 45.57 (sd 11.37) |
| P(home win) / P(away win) / P(tie) | 0.807 / 0.188 / 0.0050 |
| P(OT) | 0.027 |
| penalties per game / yards home, away | 13.93 / 53.4, 45.8 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | DAL | -8.5 | 0.595 | 0.5 |
| spread | pinnacle (ref) | DAL | -9.0 | 0.567 | 0.4966 |
| spread | consensus | DAL | -8.5 | 0.595 | 0.5 |
| spread | draftkings | DAL | -8.5 | 0.595 | 0.5033 |
| spread | betrivers | DAL | -8.5 | 0.595 | 0.5011 |
| spread | betmgm | DAL | -8.5 | 0.595 | 0.4978 |
| spread | bet365 | DAL | -8.5 | 0.595 | 0.5022 |
| spread | williamhill_us | DAL | -8.5 | 0.595 | 0.5011 |
| spread | open | DAL | -1.5 | 0.792 | 0.4892 |
| total | fanduel | Over | 48.5 | 0.390 | 0.4854 |
| total | pinnacle (ref) | Over | 48.0 | 0.390 | 0.4978 |
| total | consensus | Over | 47.5 | 0.413 | 0.5183 |
| total | draftkings | Over | 47.5 | 0.413 | 0.5142 |
| total | bet365 | Over | 47.5 | 0.413 | 0.5195 |
| total | open | Over | 49.5 | 0.364 | 0.5108 |
| total | betrivers | Over | 48.0 | 0.390 | 0.4957 |
| total | betmgm | Over | 48.0 | 0.390 | 0.4978 |
| total | williamhill_us | Over | 48.0 | 0.390 | 0.4935 |
| moneyline | fanduel | DAL |  | 0.811 | 0.7955 |
| moneyline | pinnacle (ref) | DAL |  | 0.811 | 0.7823 |
| moneyline | consensus | DAL |  | 0.811 | 0.7955 |
| moneyline | draftkings | DAL |  | 0.811 | 0.7955 |
| moneyline | betrivers | DAL |  | 0.811 | 0.781 |
| moneyline | betmgm | DAL |  | 0.811 | 0.7969 |
| moneyline | bet365 | DAL |  | 0.811 | 0.7937 |
| moneyline | williamhill_us | DAL |  | 0.811 | 0.7833 |

Market divergence: {'max_abs_moneyline_gap': 0.02979587139827733, 'flag': 'WITHIN_0.15'}

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
