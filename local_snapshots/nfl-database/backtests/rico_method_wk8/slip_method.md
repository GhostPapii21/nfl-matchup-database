# Slip method (written and committed before grading)
1. Legs = picks_locked.csv after hard stops (weather, injuries/inactives). A removed leg is replaced by the next-best candidate from the same game in candidates.csv passing the same filters (no player already used); if none, the game contributes fewer legs.
2. Slates: Sunday (11 x 1PM/4PM games + SNF PHI@WAS = 12 games) builds 8-leg slips; TNF CAR@GB (1 game) and MNF CHI@SEA (1 game) each build one 2-leg slip (short slate -> short slip).
3. Sunday assignment: sort legs by score (edge x clear-rate). Slip S1 = the best leg from each of the 8 best games; S2 = next 8 legs in score order; S3 = remaining legs (max 8). Cross-game; at most 2 legs from one game per slip; one market per player; no TDs.
4. Variant B (7 legs): drop the lowest-score leg of each Sunday 8-leg slip.
5. Pricing: product of decimal prices of each leg's pre-kick book (FanDuel first, else first book) from the Odds API kickoff-30m snapshot. Real SGP/parlay pricing differs (correlation, boosts, DFS payout tables); this is an approximation. $10 per slip; $10 flat per single.
6. Pushes: leg removed, slip priced without it. Leg with player inactive -> void (removed).
