# Decision board — 2026_12_NO_CIN

RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.
An edge figure, when present, is model probability minus the two-way no-vig price. It is not an edge claim.
This board does not target a number of picks and does not compute a hit rate. Empty sections stay empty.

- Kickoff (UTC): 2026-11-29T18:00:00+00:00
- projection_ready: false
- edge_claim_allowed: false
- Section counts: {'strong_reads': 0, 'soft_leans': 0, 'avoids': 0, 'no_plays': 4}

## Market snapshots

Book, market, line, price, timestamp and missing-line status are recorded for every comparison. Implied probability and edge are blank when either input is missing.

| subject | market | side | book | line | price | timestamp | missing line | model P | implied | no-vig | edge | edge status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CIN | spread | CIN | — | — | — | — | yes | — | — | — | — | NOT_COMPUTED_MISSING_LINE |
| GAME | total | CIN | — | — | — | — | yes | — | — | — | — | NOT_COMPUTED_MISSING_LINE |
| T.Shough | pass_yds | over | — | — | — | — | yes | — | — | — | — | NOT_COMPUTED_MISSING_LINE |
| J.Burrow | pass_yds | over | — | — | — | — | yes | — | — | — | — | NOT_COMPUTED_MISSING_LINE |

## Model probabilities

### team:spread:CIN:None — consensus absent
Threshold probability: — (withheld_no_model_probability). Disagreement: —.
No model probability was published.

### team:total:CIN:None — consensus absent
Threshold probability: — (withheld_no_model_probability). Disagreement: —.
No model probability was published.

### player:T.Shough:pass — consensus absent
Threshold probability: — (withheld_no_model_probability). Disagreement: —.
No model probability was published.

### player:J.Burrow:pass — consensus absent
Threshold probability: — (withheld_no_model_probability). Disagreement: —.
No model probability was published.

## Adversarial review

### team:spread:CIN:None — reject / no_plays
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

### team:total:CIN:None — reject / no_plays
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

### player:T.Shough:pass — reject / no_plays
Supporting evidence:
- none supplied (unspecified)
Contradicting evidence:
- No 100k sim_v6 probability was joined, so this passing row cannot support a read. (unspecified)
Red-team checks:
- Defensive suppression: none supplied; material=False
- Role/volume fragility: tag=volume, fragile=False. 
- Efficiency dependence: depends=True, support cited=False
- Injury contingency:
- Weather contingency:
- Game script contingency:
- Sample quality: n=None, withheld=True, blocks_reads=True. Passing and touchdown distributions stay on the script branch artifacts. They were not turned into one probability.
- Decision: NO PLAY: model probability is absent, so implied probability and edge were not calculated.
- Decision: NO PLAY: sportsbook line is also missing.

### player:J.Burrow:pass — reject / no_plays
Supporting evidence:
- none supplied (unspecified)
Contradicting evidence:
- No 100k sim_v6 probability was joined, so this passing row cannot support a read. (unspecified)
Red-team checks:
- Defensive suppression: none supplied; material=False
- Role/volume fragility: tag=volume, fragile=False. 
- Efficiency dependence: depends=True, support cited=False
- Injury contingency:
- Weather contingency:
- Game script contingency:
- Sample quality: n=None, withheld=True, blocks_reads=True. Passing and touchdown distributions stay on the script branch artifacts. They were not turned into one probability.
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
| CIN | spread  | CIN | not published | — | team_score | none | absent | research_only; projection_ready_false; not_a_pick; edge_is_not_a_claim; red_team_categories_not_supplied:defensive_suppression,role_volume_fragility,efficiency_dependence,injury,weather,game_script; sample_limitation |
| | | | | | | | | NO PLAY: model probability is absent, so implied probability and edge were not calculated. |
| | | | | | | | | NO PLAY: sportsbook line is also missing. |
| GAME | total  | CIN | not published | — | team_score | none | absent | research_only; projection_ready_false; not_a_pick; edge_is_not_a_claim; red_team_categories_not_supplied:defensive_suppression,role_volume_fragility,efficiency_dependence,injury,weather,game_script; sample_limitation |
| | | | | | | | | NO PLAY: model probability is absent, so implied probability and edge were not calculated. |
| | | | | | | | | NO PLAY: sportsbook line is also missing. |
| T.Shough | pass_yds  | over | not published | — | volume | none | absent | research_only; projection_ready_false; not_a_pick; edge_is_not_a_claim; red_team_categories_not_supplied:defensive_suppression,role_volume_fragility,injury,weather,game_script; sample_limitation |
| | | | | | | | | NO PLAY: model probability is absent, so implied probability and edge were not calculated. |
| | | | | | | | | NO PLAY: sportsbook line is also missing. |
| J.Burrow | pass_yds  | over | not published | — | volume | none | absent | research_only; projection_ready_false; not_a_pick; edge_is_not_a_claim; red_team_categories_not_supplied:defensive_suppression,role_volume_fragility,injury,weather,game_script; sample_limitation |
| | | | | | | | | NO PLAY: model probability is absent, so implied probability and edge were not calculated. |
| | | | | | | | | NO PLAY: sportsbook line is also missing. |

## Abstentions

- team:spread:CIN:None (reject): NO PLAY: model probability is absent, so implied probability and edge were not calculated. NO PLAY: sportsbook line is also missing.
- team:total:CIN:None (reject): NO PLAY: model probability is absent, so implied probability and edge were not calculated. NO PLAY: sportsbook line is also missing.
- player:T.Shough:pass (reject): NO PLAY: model probability is absent, so implied probability and edge were not calculated. NO PLAY: sportsbook line is also missing.
- player:J.Burrow:pass (reject): NO PLAY: model probability is absent, so implied probability and edge were not calculated. NO PLAY: sportsbook line is also missing.

## Boundaries

- Sections are a result of the review. An empty section is a valid result.
- Implied probability and edge are omitted unless a timestamped price and a model probability both exist.
- A computed edge is model probability minus the two-way no-vig price. It is not a bet.
- Model probabilities are not shrunk, capped, or averaged across a disagreement.
- No hit rate is computed.
