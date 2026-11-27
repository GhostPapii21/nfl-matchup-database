# Locked snapshot WAS @ ARI (2026_12_WAS_ARI)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T14:00:44+00:00  | kickoff (UTC): 2026-11-29T21:25:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `was_ari_2026-11-29_data_only_nfl43`; code commit `f853538e5a75401b2b0c7e85e0cc777b2b0ddb50`
- Trials: 100,000 in 3 chunks, seed 881127275, runtime 644.3 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| ARI points | 17.03 |
| WAS points | 23.29 |
| home margin | -6.26 (sd 12.70) |
| total | 40.32 (sd 11.57) |
| P(home win) / P(away win) / P(tie) | 0.308 / 0.683 / 0.0091 |
| P(OT) | 0.037 |
| penalties per game / yards home, away | 13.24 / 52.1, 50.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Washington Commanders | -7.0 | 0.450 | 0.4892 |
| spread | pinnacle (ref) | Washington Commanders | -7.0 | 0.450 | 0.4852 |
| spread | consensus (ref) | Washington Commanders | -7.0 | 0.450 | 0.4978 |
| spread | betrivers | Washington Commanders | -7.0 | 0.450 | 0.5117 |
| spread | betmgm | Washington Commanders | -7.0 | 0.450 | 0.4978 |
| spread | williamhill_us | Washington Commanders | -7.0 | 0.450 | 0.4935 |
| spread | open (ref) | Washington Commanders | -4.5 | 0.556 | 0.5 |
| spread | draftkings | Washington Commanders | -6.5 | 0.497 | 0.5108 |
| spread | bet365 | Washington Commanders | -6.5 | 0.497 | 0.5108 |
| total | fanduel | Over | 41.5 | 0.446 | 0.5 |
| total | pinnacle (ref) | Over | 41.5 | 0.446 | 0.4977 |
| total | consensus (ref) | Over | 41.5 | 0.446 | 0.5 |
| total | draftkings | Over | 41.5 | 0.446 | 0.5033 |
| total | betrivers | Over | 41.5 | 0.446 | 0.5074 |
| total | betmgm | Over | 41.5 | 0.446 | 0.4978 |
| total | bet365 | Over | 41.5 | 0.446 | 0.5 |
| total | williamhill_us | Over | 41.5 | 0.446 | 0.5043 |
| total | open (ref) | Over | 47.5 | 0.255 | 0.5 |
| moneyline | fanduel | Washington Commanders |  | 0.689 | 0.7532 |
| moneyline | pinnacle (ref) | Washington Commanders |  | 0.689 | 0.7419 |
| moneyline | consensus (ref) | Washington Commanders |  | 0.689 | 0.7447 |
| moneyline | open (ref) | Washington Commanders |  | 0.689 | 0.6575 |
| moneyline | draftkings | Washington Commanders |  | 0.689 | 0.7276 |
| moneyline | betrivers | Washington Commanders |  | 0.689 | 0.7559 |
| moneyline | betmgm | Washington Commanders |  | 0.689 | 0.7447 |
| moneyline | bet365 | Washington Commanders |  | 0.689 | 0.7447 |
| moneyline | williamhill_us | Washington Commanders |  | 0.689 | 0.7484 |

Market divergence: {'max_abs_moneyline_gap': 0.06660361698692074, 'flag': 'WITHIN_0.15'}

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
