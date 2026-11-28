# Decision board — 2026_12_SEA_SF

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.
An edge figure, when present, is model probability minus the two-way no-vig price. It is not an edge claim.
This board does not target a number of picks and does not compute a hit rate. Empty sections stay empty.

- Kickoff (UTC): None
- projection_ready: false
- edge_claim_allowed: false
- Section counts: {'strong_reads': 0, 'soft_leans': 0, 'avoids': 0, 'no_plays': 2}

## Market snapshots

Book, market, line, price, timestamp and missing-line status are recorded for every comparison. Implied probability and edge are blank when either input is missing.

| subject | market | side | book | line | price | timestamp | missing line | model P | implied | no-vig | edge | edge status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SF | spread | SF | — | — | — | — | yes | — | — | — | — | NOT_COMPUTED_MISSING_LINE |
| GAME | total | SF | — | — | — | — | yes | — | — | — | — | NOT_COMPUTED_MISSING_LINE |

## Model probabilities

### team:spread:SF:None — consensus absent
Threshold probability: — (withheld_no_model_probability). Disagreement: —.
No model probability was published.

### team:total:SF:None — consensus absent
Threshold probability: — (withheld_no_model_probability). Disagreement: —.
No model probability was published.

## Adversarial review

### team:spread:SF:None — reject / no_plays
Supporting evidence:
- none supplied (unspecified)
Contradicting evidence:
- Script branches were retained separately and were not pooled into one probability. (unspecified)
Red-team checks:
- Defensive suppression: none supplied; material=False
- Role/volume fragility: tag=team_score, fragile=False. 
- Efficiency dependence: depends=False, support cited=False
- Injury contingency:
- Weather contingency:
- Game script contingency:
- Sample quality: n=None, withheld=True, blocks_reads=True. no single model probability; branches were not averaged
- Decision: NO PLAY: model probability is absent, so implied probability and edge were not calculated.
- Decision: NO PLAY: sportsbook line is also missing.

### team:total:SF:None — reject / no_plays
Supporting evidence:
- none supplied (unspecified)
Contradicting evidence:
- Script branches were retained separately and were not pooled into one probability. (unspecified)
Red-team checks:
- Defensive suppression: none supplied; material=False
- Role/volume fragility: tag=team_score, fragile=False. 
- Efficiency dependence: depends=False, support cited=False
- Injury contingency:
- Weather contingency:
- Game script contingency:
- Sample quality: n=None, withheld=True, blocks_reads=True. no single model probability; branches were not averaged
- Decision: NO PLAY: model probability is absent, so implied probability and edge were not calculated.
- Decision: NO PLAY: sportsbook line is also missing.

## Final board

Columns: player/team, market, projection, threshold probability, role tag, confidence, model consensus, warnings.

### Strong Reads

None.

### Soft Leans

None.

### Avoids

None.

### No Plays

| player/team | market | side | projection | threshold probability | role tag | confidence | model consensus | warnings |
|---|---|---|---|---|---|---|---|---|
| SF | spread  | SF | not published | — | team_score | none | absent | research_only; projection_ready_false; not_a_pick; edge_is_not_a_claim; red_team_categories_not_supplied:defensive_suppression,role_volume_fragility,efficiency_dependence,injury,weather,game_script; sample_limitation |
| | | | | | | | | NO PLAY: model probability is absent, so implied probability and edge were not calculated. |
| | | | | | | | | NO PLAY: sportsbook line is also missing. |
| GAME | total  | SF | not published | — | team_score | none | absent | research_only; projection_ready_false; not_a_pick; edge_is_not_a_claim; red_team_categories_not_supplied:defensive_suppression,role_volume_fragility,efficiency_dependence,injury,weather,game_script; sample_limitation |
| | | | | | | | | NO PLAY: model probability is absent, so implied probability and edge were not calculated. |
| | | | | | | | | NO PLAY: sportsbook line is also missing. |

## Abstentions

- team:spread:SF:None (reject): NO PLAY: model probability is absent, so implied probability and edge were not calculated. NO PLAY: sportsbook line is also missing.
- team:total:SF:None (reject): NO PLAY: model probability is absent, so implied probability and edge were not calculated. NO PLAY: sportsbook line is also missing.

## Boundaries

- Sections are a result of the review. An empty section is a valid result.
- Implied probability and edge are omitted unless a timestamped price and a model probability both exist.
- A computed edge is model probability minus the two-way no-vig price. It is not a bet.
- Model probabilities are not shrunk, capped, or averaged across a disagreement.
- No hit rate is computed.
