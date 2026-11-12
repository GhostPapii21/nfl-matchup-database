# Locked snapshot WAS @ NYG (2026_10_WAS_NYG)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-12T17:12:58+00:00  | kickoff (UTC): 2026-11-13T01:15:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `was_nyg_2026-11-12_data_only_nfl43`; code commit `79f0ca78ebbd0c4bc2aba0467f5530bd88c9b152`
- Trials: 100,000 in 7 chunks, seed 1918467127, runtime 661.0 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9] (strictly before week 10); PBP sha256 `1028614beb746bea...`

| | mean |
|---|---|
| NYG points | 12.55 |
| WAS points | 22.06 |
| home margin | -9.51 (sd 11.96) |
| total | 34.61 (sd 10.75) |
| P(home win) / P(away win) / P(tie) | 0.209 / 0.780 / 0.0102 |
| P(OT) | 0.034 |
| penalties per game / yards home, away | 11.98 / 45.3, 44.7 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | draftkings | Washington Commanders | 2.5 | 0.829 | 0.5 |
| spread | williamhill_us | Washington Commanders | 2.0 | 0.817 | 0.5011 |
| spread | fanduel | Washington Commanders | 1.5 | 0.817 | 0.4783 |
| spread | hardrockbet | Washington Commanders | 2.0 | 0.817 | 0.5 |
| spread | pinnacle (ref) | Washington Commanders | 2.5 | 0.829 | 0.5127 |
| total | draftkings | Over | 40.5 | 0.281 | 0.5174 |
| total | williamhill_us | Over | 41.0 | 0.253 | 0.4946 |
| total | fanduel | Over | 41.5 | 0.253 | 0.4783 |
| total | hardrockbet | Over | 41.0 | 0.253 | 0.5108 |
| total | pinnacle (ref) | Over | 40.5 | 0.281 | 0.5171 |
| moneyline | draftkings | Washington Commanders |  | 0.788 | 0.4486 |
| moneyline | williamhill_us | Washington Commanders |  | 0.788 | 0.4505 |
| moneyline | fanduel | Washington Commanders |  | 0.788 | 0.4533 |
| moneyline | hardrockbet | Washington Commanders |  | 0.788 | 0.4474 |
| moneyline | pinnacle (ref) | Washington Commanders |  | 0.788 | 0.456 |

Market divergence: {'max_abs_moneyline_gap': 0.3410261784971004, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

## Known limits
- Vertical slice: empirical team-only snap resampling + explicit same-team coarser fallbacks
- Clock costs use empirical median deltas when available else fixed means — not a situational clock model
- OT rule: official 2025 regular-season (both possess, then sudden death, ties allowed)
- No league silent pool; proposed pooling config default false
- W1-8 development set; no betting edge claim
- Inspired conceptually by NFLSimulatoR/nflfastR (MIT); no R source copied
- See FEATURE_MATRIX.md for unimplemented coverage/route/pressure fields
- data_only config: no injury/inactive adjustment; Phase 15 inactives not applied to the sim
- team scores only; player yards are bootstrap credits, not a player projection model
