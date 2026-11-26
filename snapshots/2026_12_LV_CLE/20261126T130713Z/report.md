# Locked snapshot LV @ CLE (2026_12_LV_CLE)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T13:07:13+00:00  | kickoff (UTC): 2026-11-30T01:20:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `lv_cle_2026-11-29_data_only_nfl43`; code commit `46b799460a56ad1d76a8e794fce8d25dd1d28530`
- Trials: 100,000 in 4 chunks, seed 1286330650, runtime 770.1 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| CLE points | 22.26 |
| LV points | 23.98 |
| home margin | -1.72 (sd 13.89) |
| total | 46.24 (sd 12.78) |
| P(home win) / P(away win) / P(tie) | 0.444 / 0.548 / 0.0082 |
| P(OT) | 0.039 |
| penalties per game / yards home, away | 14.62 / 54.5, 44.0 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Las Vegas Raiders | 5.5 | 0.685 | 0.5042 |
| spread | pinnacle (ref) | Las Vegas Raiders | 5.0 | 0.669 | 0.5011 |
| spread | consensus (ref) | Las Vegas Raiders | 4.5 | 0.669 | 0.4978 |
| spread | draftkings | Las Vegas Raiders | 4.5 | 0.669 | 0.5098 |
| spread | betrivers | Las Vegas Raiders | 4.5 | 0.669 | 0.4946 |
| spread | betmgm | Las Vegas Raiders | 4.5 | 0.669 | 0.4978 |
| spread | bet365 | Las Vegas Raiders | 4.5 | 0.669 | 0.4957 |
| spread | williamhill_us | Las Vegas Raiders | 4.5 | 0.669 | 0.5065 |
| spread | open (ref) | Las Vegas Raiders | 1.5 | 0.577 | 0.5 |
| total | fanduel | Over | 39.5 | 0.695 | 0.5146 |
| total | pinnacle (ref) | Over | 40.0 | 0.658 | 0.5045 |
| total | open (ref) | Over | 39.5 | 0.695 | 0.5 |
| total | bet365 | Over | 39.5 | 0.695 | 0.5195 |
| total | draftkings | Over | 40.5 | 0.658 | 0.4848 |
| total | consensus (ref) | Over | 40.0 | 0.658 | 0.4978 |
| total | betrivers | Over | 40.0 | 0.658 | 0.5054 |
| total | betmgm | Over | 40.0 | 0.658 | 0.4978 |
| total | williamhill_us | Over | 40.0 | 0.658 | 0.4935 |
| moneyline | fanduel | Las Vegas Raiders |  | 0.553 | 0.331 |
| moneyline | pinnacle (ref) | Las Vegas Raiders |  | 0.553 | 0.3227 |
| moneyline | consensus (ref) | Las Vegas Raiders |  | 0.553 | 0.3252 |
| moneyline | draftkings | Las Vegas Raiders |  | 0.553 | 0.319 |
| moneyline | betrivers | Las Vegas Raiders |  | 0.553 | 0.3349 |
| moneyline | betmgm | Las Vegas Raiders |  | 0.553 | 0.3258 |
| moneyline | bet365 | Las Vegas Raiders |  | 0.553 | 0.3244 |
| moneyline | williamhill_us | Las Vegas Raiders |  | 0.553 | 0.3258 |

Market divergence: {'max_abs_moneyline_gap': 0.2337491253012291, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
