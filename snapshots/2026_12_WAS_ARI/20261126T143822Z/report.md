# Locked snapshot WAS @ ARI (2026_12_WAS_ARI)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T14:38:22+00:00  | kickoff (UTC): 2026-11-29T21:25:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `was_ari_2026-11-29_data_only_nfl43`; code commit `d8bfbc76c093aba8955b0247caf58ba513f1b49b`
- Trials: 100,000 in 4 chunks, seed 881127275, runtime 792.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| ARI points | 17.06 |
| WAS points | 23.28 |
| home margin | -6.23 (sd 12.71) |
| total | 40.34 (sd 11.59) |
| P(home win) / P(away win) / P(tie) | 0.308 / 0.683 / 0.0089 |
| P(OT) | 0.037 |
| penalties per game / yards home, away | 13.25 / 52.2, 50.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | Washington Commanders | -7.0 | 0.449 | 0.4892 |
| spread | pinnacle (ref) | Washington Commanders | -6.5 | 0.497 | 0.5158 |
| spread | consensus (ref) | Washington Commanders | -7.0 | 0.449 | 0.4923 |
| spread | draftkings | Washington Commanders | -7.0 | 0.449 | 0.488 |
| spread | betrivers | Washington Commanders | -7.0 | 0.449 | 0.5142 |
| spread | betmgm | Washington Commanders | -7.0 | 0.449 | 0.4923 |
| spread | williamhill_us | Washington Commanders | -7.0 | 0.449 | 0.4935 |
| spread | open (ref) | Washington Commanders | -4.5 | 0.556 | 0.5 |
| spread | bet365 | Washington Commanders | -6.5 | 0.497 | 0.5174 |
| total | fanduel | Over | 41.5 | 0.446 | 0.5 |
| total | pinnacle (ref) | Over | 41.5 | 0.446 | 0.4932 |
| total | consensus (ref) | Over | 41.5 | 0.446 | 0.5 |
| total | draftkings | Over | 41.5 | 0.446 | 0.5033 |
| total | betrivers | Over | 41.5 | 0.446 | 0.5085 |
| total | betmgm | Over | 41.5 | 0.446 | 0.4978 |
| total | bet365 | Over | 41.5 | 0.446 | 0.5 |
| total | williamhill_us | Over | 41.5 | 0.446 | 0.5043 |
| total | open (ref) | Over | 47.5 | 0.255 | 0.5 |
| moneyline | fanduel | Washington Commanders |  | 0.689 | 0.7472 |
| moneyline | pinnacle (ref) | Washington Commanders |  | 0.689 | 0.7411 |
| moneyline | consensus (ref) | Washington Commanders |  | 0.689 | 0.7447 |
| moneyline | open (ref) | Washington Commanders |  | 0.689 | 0.6575 |
| moneyline | draftkings | Washington Commanders |  | 0.689 | 0.7353 |
| moneyline | betrivers | Washington Commanders |  | 0.689 | 0.7559 |
| moneyline | betmgm | Washington Commanders |  | 0.689 | 0.7447 |
| moneyline | bet365 | Washington Commanders |  | 0.689 | 0.7484 |
| moneyline | williamhill_us | Washington Commanders |  | 0.689 | 0.7484 |

Market divergence: {'max_abs_moneyline_gap': 0.06701581963656911, 'flag': 'WITHIN_0.15'}

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
