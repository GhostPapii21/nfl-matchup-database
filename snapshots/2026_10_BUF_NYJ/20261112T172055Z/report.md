# Locked snapshot BUF @ NYJ (2026_10_BUF_NYJ)

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.

- Locked (UTC): 2026-11-12T17:20:55+00:00  | kickoff (UTC): 2026-11-15T18:00:00+00:00
- Engine: core/possession_engine_v0 + NFL-43 semantics; config `buf_nyj_2026-11-15_data_only_nfl43`; code commit `a7a1a9fddff2abdd9b2278d02f695d088b517a1a`
- Trials: 100,000 in 7 chunks, seed 1797353313, runtime 376.6 s
- History: weeks [1, 2, 3, 4, 5, 6, 7, 8, 9] (strictly before week 10); PBP sha256 `1028614beb746bea...`

| | mean |
|---|---|
| NYJ points | 17.11 |
| BUF points | 20.77 |
| home margin | -3.66 (sd 11.65) |
| total | 37.87 (sd 10.62) |
| P(home win) / P(away win) / P(tie) | 0.367 / 0.622 / 0.0111 |
| P(OT) | 0.043 |
| penalties per game / yards home, away | 13.57 / 48.2, 54.6 |

## Against the frozen book lines (research comparison, not an edge claim)

| market | book | side | line | model P | book no-vig P |
|---|---|---|---|---|---|
| spread | draftkings | NYJ | 8.5 | 0.658 | 0.5043 |
| spread | fanduel | NYJ | 7.5 | 0.634 | 0.4892 |
| spread | pinnacle (ref) | NYJ | 8.5 | 0.658 | 0.5171 |
| total | draftkings | Over | 50.5 | 0.119 | 0.5174 |
| total | fanduel | Over | 50.5 | 0.119 | 0.5217 |
| total | pinnacle (ref) | Over | 51.0 | 0.101 | 0.4978 |
| moneyline | draftkings | NYJ |  | 0.371 | 0.2181 |
| moneyline | fanduel | NYJ |  | 0.371 | 0.2045 |
| moneyline | pinnacle (ref) | NYJ |  | 0.371 | 0.2197 |

Market divergence: {'max_abs_moneyline_gap': 0.16626026940112862, 'flag': 'LARGE_DIVERGENCE_TREAT_AS_MODEL_ERROR_UNTIL_SHOWN_OTHERWISE'}

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
