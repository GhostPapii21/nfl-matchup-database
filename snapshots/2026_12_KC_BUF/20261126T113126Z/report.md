# Locked snapshot KC @ BUF (2026_12_KC_BUF)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-26T11:31:26+00:00  | kickoff (UTC): 2026-11-27T01:20:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `kc_buf_2026-11-26_data_only_nfl43`; code commit `2b33647ccd84ef8515e122c291705fdfe7b1d2cd`
- Trials: 100,000 in 7 chunks, seed 1700585865, runtime 514.5 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] (strictly before week 12); PBP sha256 `7232b5520edfe2a9...`

| | mean |
|---|---|
| BUF points | 29.82 |
| KC points | 33.02 |
| home margin | -3.20 (sd 14.67) |
| total | 62.84 (sd 13.52) |
| P(home win) / P(away win) / P(tie) | 0.410 / 0.584 / 0.0060 |
| P(OT) | 0.035 |
| penalties per game / yards home, away | 14.81 / 62.6, 57.5 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | fanduel | BUF | -2.5 | 0.370 | 0.5239 |
| spread | pinnacle (ref) | BUF | -2.5 | 0.370 | 0.5216 |
| spread | open | BUF | -2.5 | 0.370 | 0.5108 |
| spread | bet365 | BUF | -2.5 | 0.370 | 0.5217 |
| spread | williamhill_us | BUF | -2.5 | 0.370 | 0.5239 |
| spread | consensus | BUF | -3.0 | 0.331 | 0.5022 |
| spread | draftkings | BUF | -3.0 | 0.331 | 0.4783 |
| spread | betrivers | BUF | -3.0 | 0.331 | 0.485 |
| spread | betmgm | BUF | -3.0 | 0.331 | 0.4826 |
| total | fanduel | Over | 46.5 | 0.893 | 0.5 |
| total | pinnacle (ref) | Over | 46.5 | 0.893 | 0.5023 |
| total | consensus | Over | 46.5 | 0.893 | 0.4989 |
| total | draftkings | Over | 46.5 | 0.893 | 0.4967 |
| total | betrivers | Over | 46.5 | 0.893 | 0.5054 |
| total | betmgm | Over | 46.5 | 0.893 | 0.4978 |
| total | bet365 | Over | 46.5 | 0.893 | 0.5 |
| total | williamhill_us | Over | 46.5 | 0.893 | 0.5065 |
| total | open | Over | 50.5 | 0.820 | 0.5 |
| moneyline | fanduel | BUF |  | 0.413 | 0.579 |
| moneyline | pinnacle (ref) | BUF |  | 0.413 | 0.5761 |
| moneyline | consensus | BUF |  | 0.413 | 0.5751 |
| moneyline | open | BUF |  | 0.413 | 0.5745 |
| moneyline | draftkings | BUF |  | 0.413 | 0.5731 |
| moneyline | betrivers | BUF |  | 0.413 | 0.5723 |
| moneyline | betmgm | BUF |  | 0.413 | 0.5745 |
| moneyline | bet365 | BUF |  | 0.413 | 0.5796 |
| moneyline | williamhill_us | BUF |  | 0.413 | 0.583 |

Market divergence: {'max_abs_moneyline_gap': 0.170447058941883, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
